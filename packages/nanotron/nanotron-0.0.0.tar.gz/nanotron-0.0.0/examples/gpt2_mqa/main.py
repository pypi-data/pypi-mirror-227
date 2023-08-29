import argparse
import contextlib
import datetime
import logging as lg
import math
import os
import sys
import time
from math import ceil
from pathlib import Path
from pprint import pformat
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
from config import (
    ExistingCheckpointInit,
    HubLoggerConfig,
    LRSchedulerArgs,
    ModelArgs,
    OptimizerArgs,
    ParallelismArgs,
    PretrainDatasetsArgs,
    PretrainNemoArgs,
    RandomInit,
    TensorboardLoggerConfig,
    get_args_from_path,
)
from dataloader import (
    clm_process,
    dummy_infinite_data_generator,
    get_nemo_dataloader,
    get_nemo_datasets,
    get_train_dataloader,
)
from datasets import load_dataset
from flops import get_flops_per_sec
from torch import nn
from torch.nn.parallel import DistributedDataParallel
from torch.optim.lr_scheduler import LambdaLR
from torch.profiler.profiler import ProfilerActivity, profile, tensorboard_trace_handler
from transformers import AutoTokenizer
from upload import upload_checkpoint

from brrr.clip_grads import clip_grad_norm
from brrr.core import distributed as dist
from brrr.core import logging
from brrr.core.dataclass import RandomStates
from brrr.core.gradient_accumulator import (
    FP32GradBucketManager,
    FP32GradientAccumulator,
    GradientAccumulator,
    get_fp32_accum_hook,
)
from brrr.core.logging import log_rank
from brrr.core.optimizer.base import BaseOptimizer, Optimizer
from brrr.core.optimizer.named_optimizer import NamedOptimizer
from brrr.core.optimizer.optimizer_from_gradient_accumulator import (
    OptimizerFromGradientAccumulator,
)
from brrr.core.optimizer.zero import ZeroDistributedOptimizer
from brrr.core.parallelism.data_parallelism.utils import sync_gradients_across_dp
from brrr.core.parallelism.parameters import BRRRParameter, sanity_check
from brrr.core.parallelism.pipeline_parallelism.block import PipelineBlock
from brrr.core.parallelism.pipeline_parallelism.engine import (
    PipelineEngine,
)
from brrr.core.parallelism.pipeline_parallelism.tensor_pointer import TensorPointer
from brrr.core.parallelism.pipeline_parallelism.utils import get_pp_rank_of
from brrr.core.parallelism.tensor_parallelism.nn import (
    TensorParallelColumnLinear,
    TensorParallelEmbedding,
    TensorParallelLinearMode,
    TensorParallelRowLinear,
)
from brrr.core.parallelism.tied_parameters import (
    create_pg_for_tied_weights,
    get_tied_id_to_param,
    sync_tied_weights_gradients,
    tie_parameters,
)
from brrr.core.process_groups_initializer import DistributedProcessGroups, get_process_groups
from brrr.core.random import (
    get_current_random_state,
    get_synced_random_state,
    set_random_seed,
)
from brrr.core.serialize import (
    load,
    load_lr_scheduler,
    load_meta,
    load_optimizer,
    load_random_states,
    load_weights,
    save,
    save_random_states,
)
from brrr.core.serialize.path import check_path_is_local
from brrr.core.serialize.serialize import fs_open
from brrr.core.tensor_init import init_method_normal, scaled_init_method_normal
from brrr.core.utils import (
    assert_fail_except_rank_with,
    assert_tensor_synced_across_pg,
    init_on_device_and_dtype,
    main_rank_first,
)
from brrr.logger import LoggerWriter, LogItem

logger = logging.get_logger(__name__)

try:
    from brrr.logger import BatchSummaryWriter

    tb_logger_available = True
except ImportError:
    tb_logger_available = False

try:
    from brrr.logger import HubSummaryWriter

    hub_logger_available = True
except ImportError:
    hub_logger_available = False


# TODO @nouamane: `AdamW` doesn't support `set_to_none=True`
# try:
#     from apex.optimizers import FusedAdam as AdamW
#
#     logger.warning("Discovered apex.optimizers.FusedAdam - will use it instead of torch.optim.AdamW")
# except Exception:
#     from torch.optim import AdamW
from torch.optim import AdamW  # noqa

# Use `USE_FAST` env variable to determine is one should run fast version or not
if os.environ.get("USE_FAST"):
    # We import the fast versions
    from modeling_gpt2_fast import GPTBlock, GPTForTraining, LayerNorm, MQAColumnLinears
else:
    from modeling_gpt2 import GPTBlock, GPTForTraining, LayerNorm


"""
Example on how to use `brrr` to build a gpt model
"""


def get_args():
    parser = argparse.ArgumentParser()
    # CONFIG for YAML
    parser.add_argument("--config-file", type=str, required=True, help="Path to the YAML config file")
    return parser.parse_args()


def set_logger_verbosity(logging_level: str, dpg: DistributedProcessGroups):
    formatter = lg.Formatter(
        fmt=f"%(asctime)s [%(levelname)s|DP={dist.get_rank(dpg.dp_pg)}|PP={dist.get_rank(dpg.pp_pg)}|TP={dist.get_rank(dpg.tp_pg)}]: %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
    )
    # TODO @thomasw21: `logging.log_levels` returns valid lg log levels
    log_level = logging.log_levels[logging_level]

    # main root logger
    root_logger = logging.get_logger()
    root_logger.setLevel(log_level)
    handler = logging.NewLineStreamHandler(sys.stdout)
    handler.setLevel(log_level)
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # Brrr
    logging.set_verbosity(log_level)
    logging.set_formatter(formatter=formatter)


def _vocab_size_with_padding(orig_vocab_size: int, pg_size: int, make_vocab_size_divisible_by: int):
    """Pad vocab size so it is divisible by pg_size * make_vocab_size_divisible_by."""

    multiple = make_vocab_size_divisible_by * pg_size
    after = int(ceil(orig_vocab_size / multiple) * multiple)

    if after != orig_vocab_size:
        log_rank(
            f"[Vocab Size Padding] Padded vocab (size: {orig_vocab_size}) with {after - orig_vocab_size} dummy tokens (new size: {after})",
            logger=logger,
            level=logging.WARNING,
            rank=0,
        )
    return after


def get_checkpoint_path(root_path: Path, iteration_step: int, train_steps: int):
    num_digits = len(str(train_steps))
    checkpoint_path = root_path / f"iter_{iteration_step:0{num_digits}d}"
    return checkpoint_path


def init_model(
    model_config: ModelArgs,
    dtype: torch.dtype,
    dpg: DistributedProcessGroups,
    parallel_config: Optional[ParallelismArgs],
    make_ddp: bool,
    device: torch.device = torch.device("cuda"),
):
    # Get synchronized random states
    if parallel_config is None or parallel_config.tp_mode is TensorParallelLinearMode.ALL_REDUCE:
        random_states = RandomStates(
            {"tp_synced": get_synced_random_state(random_state=get_current_random_state(), pg=dpg.tp_pg)}
        )
    else:
        # We don't need to sync across TP when using sequence parallel (REDUCE_SCATTER)
        random_states = RandomStates({})

    # Load model
    # TODO @thomasw21: Fix the `training_args` refactor
    model = GPTForTraining(config=model_config, dpg=dpg, parallel_config=parallel_config, random_states=random_states)

    # Set rank for each pipeline block
    pipeline_blocks = [module for name, module in model.named_modules() if isinstance(module, PipelineBlock)]
    # "cuda" is already defaulted for each process to it's own cuda device
    with init_on_device_and_dtype(device=device, dtype=dtype):
        # TODO: https://github.com/huggingface/brrr/issues/65

        # Balance compute across PP blocks
        d_ff = model_config.ffn_hidden_size
        d_qkv = model_config.hidden_size // model_config.num_attention_heads
        block_compute_costs = {
            # MQA CausalSelfAttention (q proj + attn out + kv proj) + MLP
            GPTBlock: 2 * (model_config.num_attention_heads + dpg.tp_pg.size()) * d_qkv * model_config.hidden_size
            + 2 * d_ff * model_config.hidden_size,
            # This is the last lm_head
            TensorParallelColumnLinear: model_config.vocab_size * model_config.hidden_size,
        }
        block_cumulative_costs = np.cumsum(
            [
                block_compute_costs[module.module_builder] if module.module_builder in block_compute_costs else 0
                for module in pipeline_blocks
            ]
        )
        thresholds = [block_cumulative_costs[-1] * ((rank + 1) / dpg.pp_pg.size()) for rank in range(dpg.pp_pg.size())]
        assert thresholds[-1] >= block_cumulative_costs[-1]
        target_pp_rank = 0
        for block, cumulative_cost in zip(pipeline_blocks, block_cumulative_costs):
            assert target_pp_rank < dpg.pp_pg.size()
            block.build_and_set_rank(target_pp_rank)

            if cumulative_cost > thresholds[target_pp_rank]:
                target_pp_rank += 1

    # Mark some parameters as tied
    # Tie embeddings
    shared_embeddings = [
        (
            target,
            (
                dpg.world_rank_matrix[
                    get_pp_rank_of(target, module=model), dist.get_rank(dpg.dp_pg), dist.get_rank(dpg.tp_pg)
                ],
            ),
        )
        for target in [
            "model.token_position_embeddings.pp_block.token_embedding.weight",
            "model.lm_head.pp_block.weight",
        ]
    ]
    tie_parameters(root_module=model, ties=shared_embeddings, dpg=dpg, reduce_op=dist.ReduceOp.SUM)

    # Sync all parameters that have the same name and that are not sharded
    for module_name, module in model.named_modules():
        for param_name, param in module.named_parameters(recurse=False):
            name = f"{module_name}.{param_name}"

            if ".qkv.kv." in name:
                assert param.is_tied, f"Expected {name} to already be synced"
                # kv is deliberately skipped as it's tied in model init
                continue

            if isinstance(param, BRRRParameter) and param.is_sharded:
                continue

            if isinstance(module, TensorParallelRowLinear) and "bias" == param_name:
                # bias for TensorParallelRowLinear only exists on TP=0 so we don't need to tie it
                continue

            shared_weights = [
                (
                    name,
                    # This adds all the tp_ranks in one go
                    tuple(sorted(dpg.world_rank_matrix[dist.get_rank(dpg.pp_pg), dist.get_rank(dpg.dp_pg), :])),
                )
            ]

            # TODO @thomasw21: Somehow declaring tied weights at local level doesn't work correctly.
            if parallel_config is None or parallel_config.tp_mode is TensorParallelLinearMode.ALL_REDUCE:
                # We add `reduce_op=None` in order to signal that the weight are synced by design without needing to reduce
                # when TP=2 we have LN that is duplicated across TP, so by design it's tied
                reduce_op = None
            else:
                reduce_op = dist.ReduceOp.SUM

            tie_parameters(root_module=model, ties=shared_weights, dpg=dpg, reduce_op=reduce_op)

    create_pg_for_tied_weights(root_module=model, dpg=dpg)

    # count number of parameters
    num_params = sum(p.numel() for p in model.parameters())
    size_params = sum(p.numel() * p.element_size() for p in model.parameters())

    # TODO @nouamanetazi: better memory logs
    log_rank(
        f"Number of parameters: {num_params} ({size_params / 1024**2:.2f}MB). Expecting peak 4*param_size={4*size_params / 1024**2:.2f}MB with grads and Adam optim states (w/o memory optims)",
        logger=logger,
        level=logging.INFO,
        group=dpg.dp_pg,
        rank=0,
    )
    log_rank(
        f"[After model building] Memory usage: {torch.cuda.memory_allocated() / 1024**2:.2f}MB. Peak reserved memory: {torch.cuda.max_memory_reserved() / 1024**2:.2f}MB",
        logger=logger,
        level=logging.INFO,
        group=dpg.dp_pg,
        rank=0,
    )

    # Model make it DDP
    if make_ddp is True:
        model = DistributedDataParallel(model, process_group=dpg.dp_pg)

    # Sanity check the model
    sanity_check(root_module=model)

    return model, random_states


def lr_scheduler_builder(optimizer: Optimizer, learning_rate: float, lr_scheduler_args: LRSchedulerArgs):
    def lr_lambda(current_step: int):
        """LR Scheduling function, it has 3 phases: warmup, decay, then constant. Warmup starts at lr=0 and ends at `lr=lr`, then it decays until `min_decay_lr` and then stays constant."""
        # No warmup or decay
        if lr_scheduler_args.lr_warmup_steps == 0 and lr_scheduler_args.lr_decay_steps == 0:
            return learning_rate

        # Warmup phase
        elif lr_scheduler_args.lr_warmup_style is not None and current_step <= lr_scheduler_args.lr_warmup_steps:
            if lr_scheduler_args.lr_warmup_style == "linear":
                lmbda = learning_rate * current_step / max(lr_scheduler_args.lr_warmup_steps, 1)
            elif lr_scheduler_args.lr_warmup_style == "constant":
                lmbda = learning_rate
            else:
                raise ValueError(f"Unknown warmup style {lr_scheduler_args.lr_warmup_style}")

        # Decay phase
        elif (
            lr_scheduler_args.lr_decay_style is not None
            and current_step < lr_scheduler_args.lr_decay_steps + lr_scheduler_args.lr_warmup_steps
        ):
            if lr_scheduler_args.lr_decay_style == "cosine":
                lmbda = (
                    lr_scheduler_args.min_decay_lr
                    + (learning_rate - lr_scheduler_args.min_decay_lr)
                    * (
                        1
                        + math.cos(
                            math.pi
                            * (current_step - lr_scheduler_args.lr_warmup_steps)
                            / lr_scheduler_args.lr_decay_steps
                        )
                    )
                    / 2
                )
            elif lr_scheduler_args.lr_decay_style == "linear":
                lmbda = (
                    lr_scheduler_args.min_decay_lr
                    + (learning_rate - lr_scheduler_args.min_decay_lr)
                    * (lr_scheduler_args.lr_decay_steps - (current_step - lr_scheduler_args.lr_warmup_steps))
                    / lr_scheduler_args.lr_decay_steps
                )
            else:
                raise ValueError(f"Unknown decay style {lr_scheduler_args.lr_decay_style}")

        # Constant phase
        else:
            lmbda = lr_scheduler_args.min_decay_lr

        lmbda /= learning_rate
        return lmbda

    lr_scheduler = LambdaLR(optimizer.get_base_optimizer(), lr_lambda=lr_lambda)
    return lr_scheduler


def init_optimizer_and_grad_accumulator(
    model: nn.Module, optimizer_args: OptimizerArgs, dpg: DistributedProcessGroups
) -> Tuple[BaseOptimizer, GradientAccumulator]:
    # Normalize DDP
    normalized_model = model.module if isinstance(model, DistributedDataParallel) else model

    module_id_to_prefix = {id(module): f"{module_name}." for module_name, module in normalized_model.named_modules()}
    # Fix the root_model
    root_model_id = id(normalized_model)
    module_id_to_prefix[root_model_id] = ""

    # named parameters
    named_parameters = [
        (
            param.get_tied_info().get_full_name_from_module_id_to_prefix(module_id_to_prefix=module_id_to_prefix)
            if param.is_tied
            else name,
            param,
        )
        for name, param in normalized_model.named_parameters()
    ]

    # Basic optimizer builder
    def basic_optimizer_builder(named_param_groups):
        return NamedOptimizer(
            named_params_or_groups=named_param_groups,
            optimizer_builder=lambda param_groups: AdamW(
                param_groups,
                lr=optimizer_args.learning_rate,
                weight_decay=optimizer_args.weight_decay,
                eps=optimizer_args.adam_eps,
                betas=(optimizer_args.adam_beta1, optimizer_args.adam_beta2),
            ),
        )

    optimizer_builder = basic_optimizer_builder

    # Gradient accumulator builder
    grad_accumulator: Optional[GradientAccumulator] = None
    if optimizer_args.accumulate_grad_in_fp32:
        # TODO @thomasw21: Make an optimizer builder system, instead of doing everything in functional manner
        def grad_optimizer_builder(named_param_groups):
            result = OptimizerFromGradientAccumulator(
                gradient_accumulator_builder=lambda named_params: FP32GradientAccumulator(
                    named_parameters=named_params,
                    grad_buckets_named_params=named_parameters,
                ),
                named_params_or_groups=named_param_groups,
                optimizer_builder=basic_optimizer_builder,
            )

            # TODO @thomasw21: get better API to get the grad_accumulator
            nonlocal grad_accumulator
            grad_accumulator = result.gradient_accumulator

            return result

        optimizer_builder = grad_optimizer_builder

    if optimizer_args.zero_stage > 0:
        # Build optimizer
        optimizer = ZeroDistributedOptimizer(
            named_params_or_groups=named_parameters,
            # TODO @thomasw21: We need a better API for gradient accumulation/zero etc ...
            optimizer_builder=optimizer_builder,
            dp_pg=dpg.dp_pg,
        )

        # SANITY CHECK: assert that optimizer's named_params point to model's params (check only the first one)
        if len(optimizer.zero_named_param_groups[0]["named_params"]) > 0:
            optim_model_param_name, optim_model_param = optimizer.zero_named_param_groups[0]["named_params"][0]
            if isinstance(model, DistributedDataParallel):
                optim_model_param_name = f"module.{optim_model_param_name}"
            param = model.get_parameter(optim_model_param_name)
            assert param.data_ptr() == optim_model_param.data_ptr()
    else:
        # Build optimizer
        optimizer = optimizer_builder(named_parameters)

    if grad_accumulator is not None and optimizer_args.zero_stage > 0:
        # There's a way to only require to reduce_scatter the gradients instead of all_reducing
        # In order to do so I need to pass which segments of each parameter should be reduced on which dp rank.
        assert isinstance(optimizer, ZeroDistributedOptimizer)
        param_name_to_dp_rank_offsets = optimizer.param_name_to_dp_rank_offsets

        assert isinstance(grad_accumulator, FP32GradientAccumulator)
        grad_accumulator.assign_param_offsets(
            dp_rank=dist.get_rank(dpg.dp_pg),
            param_name_to_offsets=param_name_to_dp_rank_offsets,
        )

    # Register DDP hook to make fp32 grad accumulation work
    if isinstance(model, DistributedDataParallel) and grad_accumulator is not None:
        assert isinstance(grad_accumulator, FP32GradientAccumulator)
        model.register_comm_hook(
            state=FP32GradBucketManager(
                dp_pg=dpg.dp_pg,
                accumulator=grad_accumulator,
                param_id_to_name={
                    id(param): param.get_tied_info().get_full_name_from_module_id_to_prefix(
                        module_id_to_prefix=module_id_to_prefix
                    )
                    if param.is_tied
                    else name
                    for name, param in normalized_model.named_parameters()
                },
            ),
            hook=get_fp32_accum_hook(
                reduce_scatter=optimizer.inherit_from(ZeroDistributedOptimizer), reduce_op=dist.ReduceOp.AVG
            ),
        )

    return optimizer, grad_accumulator


def save_checkpoint(
    model,
    optimizer,
    lr_scheduler,
    random_states: RandomStates,
    iteration_step: int,
    consumed_train_samples: int,
    train_steps: int,
    checkpoints_path: Path,
    dpg: DistributedProcessGroups,
) -> Path:
    checkpoint_path = get_checkpoint_path(checkpoints_path, iteration_step, train_steps)
    if check_path_is_local(checkpoint_path):
        if dist.get_rank(dpg.world_pg) == 0:
            checkpoint_path.mkdir(parents=True, exist_ok=True)
        dist.barrier(dpg.world_pg)
    log_rank(f"Saving checkpoint at {checkpoint_path}", logger=logger, level=logging.INFO, rank=0)
    checkpoint_metadata = {
        "last_train_step": iteration_step,
        # TODO: @nouamanetazi: Add more metadata to the checkpoint to be able to resume dataloader states properly
        "consumed_train_samples": consumed_train_samples,
    }
    save(
        model=model,
        optimizer=optimizer,
        lr_scheduler=lr_scheduler,
        dpg=dpg,
        root_folder=checkpoint_path,
        checkpoint_metadata=checkpoint_metadata,
    )
    save_random_states(random_states=random_states, dpg=dpg, root_folder=checkpoint_path)
    if dist.get_rank(dpg.world_pg) == 0:
        with fs_open(checkpoints_path / "latest.txt", mode="w") as fo:
            fo.write(f"{iteration_step}")
        (checkpoint_path / "finished-save-checkpoint").touch()
    return checkpoint_path


def test_equal_dict(first: Dict, second: Dict, sub_paths: Optional[List[str]] = None) -> None:
    """Raise if doesn't match"""
    if sub_paths is None:
        sub_paths = []

    first_keys = set(first.keys())
    second_keys = set(second.keys())
    assert first_keys == second_keys, f"Keys don't match.\nFirst: {first_keys}\nSecond: {second_keys}"
    for key in first_keys:
        first_elt = first[key]
        second_elt = second[key]

        if isinstance(first_elt, dict):
            assert isinstance(second_elt, dict), f"{first_elt} doesn't match {second_elt}"
            test_equal_dict(first_elt, second_elt, sub_paths=sub_paths + [str(key)])
        elif isinstance(first_elt, torch.Tensor):
            assert isinstance(second_elt, torch.Tensor), f"{first_elt} doesn't match {second_elt}"
            torch.testing.assert_close(
                first_elt,
                second_elt,
                atol=0.0,
                rtol=0.0,
                msg=lambda msg: f"tensor at {'.'.join(sub_paths + [str(key)])} don't match.\nCur: {first_elt}\nRef: {second_elt}\n{msg}",
            )
        else:
            assert (
                first_elt == second_elt
            ), f"{first_elt} doesn't match {second_elt} at key {'.'.join(sub_paths + [str(key)])}"


def main():
    config_file = get_args().config_file
    config = get_args_from_path(config_file)

    # Initialise all process groups
    dpg = get_process_groups(
        data_parallel_size=config.parallelism.dp,
        pipeline_parallel_size=config.parallelism.pp,
        tensor_parallel_size=config.parallelism.tp,
    )

    # Set random states
    set_random_seed(config.model.seed)

    # Set log levels
    if dist.get_rank(dpg.world_pg) == 0:
        if config.logging.log_level is not None:
            set_logger_verbosity(config.logging.log_level, dpg=dpg)
    else:
        if config.logging.log_level_replica is not None:
            set_logger_verbosity(config.logging.log_level_replica, dpg=dpg)

    # Setup all writers
    if (
        dist.get_rank(dpg.pp_pg) == dpg.pp_pg.size() - 1
        and dist.get_rank(dpg.tp_pg) == 0
        and dist.get_rank(dpg.dp_pg) == 0
    ):
        if config.logging.tensorboard_logger is None:
            tb_context = contextlib.nullcontext()
        else:
            current_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            logdir = str(config.logging.tensorboard_logger.tensorboard_dir / f"{config.general.name}_{current_time}")

            if isinstance(config.logging.tensorboard_logger, HubLoggerConfig):
                assert (
                    hub_logger_available
                ), 'Hub Tensorboard Logger is not available. Please install brrr with `pip install -e ".[hf-logger]"` or modify your config file'
                tb_context = HubSummaryWriter(
                    logdir=logdir,
                    repo_id=config.logging.tensorboard_logger.repo_id,
                    path_in_repo=f"tensorboard/{config.general.name}_{current_time}",
                    commit_every=config.logging.tensorboard_logger.commit_every_x_minutes,
                )
            if isinstance(config.logging.tensorboard_logger, TensorboardLoggerConfig):
                assert (
                    tb_logger_available
                ), 'Tensorboard Logger is not available. Please install brrr with `pip install -e ".[tb-logger]"` or modify your config file'
                tb_context = BatchSummaryWriter(logdir=logdir)
        loggerwriter = LoggerWriter(global_step=config.tokens.train_steps)
    else:
        tb_context = contextlib.nullcontext()

    # Choosing checkpoint path
    load_from_candidate = config.checkpoints.load_from_specific_checkpoint
    if load_from_candidate is None:
        latest_meta_path = config.checkpoints.checkpoints_path / "latest.txt"
        if latest_meta_path.exists():
            with fs_open(config.checkpoints.checkpoints_path / "latest.txt", mode="r") as fi:
                # TODO @thomasw21: make a better structure system so that we get typing correct
                load_from_candidate = int(fi.read())
    checkpoint_path = (
        get_checkpoint_path(config.checkpoints.checkpoints_path, load_from_candidate, config.tokens.train_steps)
        if load_from_candidate is not None
        else None
    )
    if checkpoint_path is not None:
        log_rank(
            f"Loading checkpoint from {checkpoint_path}:",
            logger=logger,
            level=logging.INFO,
            rank=0,
        )

    # Handler for checkpoint upload script. Ensures that only one upload script is running at a time.
    previous_upload_process = None

    # Init model
    model_config = config.model

    assert model_config.vocab_size == _vocab_size_with_padding(
        model_config.vocab_size,
        pg_size=dpg.tp_pg.size(),
        make_vocab_size_divisible_by=config.model.assert_make_sharded_vocab_size_divisible_by,
    )
    assert (
        model_config.max_position_embeddings >= config.tokens.sequence_length
    ), f"max_position_embeddings ({model_config.max_position_embeddings}) must be >= sequence_length ({config.tokens.sequence_length})"

    log_rank(pformat(config), logger=logger, level=logging.INFO, rank=0)
    log_rank(str(model_config), logger=logger, level=logging.INFO, rank=0)

    optimizer_args = config.optimizer

    model, random_states = init_model(
        model_config=model_config,
        parallel_config=config.parallelism,
        dtype=config.model.dtype,
        dpg=dpg,
        # TODO @thomasw21: Figure out why using DDP with accumulate_in_fp_32 and ZeRO-1 performs poorly.
        make_ddp=False,
    )

    if checkpoint_path is not None:
        load_weights(model=model, dpg=dpg, root_folder=checkpoint_path)
    else:
        # We initialize the model.
        if isinstance(config.model.init_method, ExistingCheckpointInit):
            # Initialize model from an existing model checkpoint
            load_weights(model=model, dpg=dpg, root_folder=config.model.init_method.path)
        elif isinstance(config.model.init_method, RandomInit):
            # Initialize model randomly

            # Used for embedding/position/qkv weight in attention/first layer weight of mlp/ /lm_head/
            init_method_ = init_method_normal(config.model.init_method.std)
            # Used for o weight in attention/second layer weight of mlp/
            scaled_init_method_ = scaled_init_method_normal(config.model.init_method.std, model_config.num_layers)
            # Layernorm weight all 0 or 1 depending on `apply_layernorm_1p`
            # Set to 0: layernorm bias / all bias

            initialized_parameters = set()
            # Handle tensor parallelism
            with torch.no_grad():
                module_id_to_prefix = {id(module): f"{module_name}." for module_name, module in model.named_modules()}
                # Fix the root_model
                module_id_to_prefix[id(model)] = ""

                for module_name, module in model.named_modules():
                    if isinstance(module, TensorParallelColumnLinear):
                        # Somehow Megatron-LM does something super complicated, https://github.com/NVIDIA/Megatron-LM/blob/2360d732a399dd818d40cbe32828f65b260dee11/megatron/core/tensor_parallel/layers.py#L96
                        # What it does:
                        #  - instantiate a buffer of the `full size` in fp32
                        #  - run init method on it
                        #  - shard result to get only a specific shard
                        # Instead I'm lazy and just going to run init_method, since they are scalar independent
                        assert {"weight", "bias"} == {name for name, _ in module.named_parameters()} or {"weight"} == {
                            name for name, _ in module.named_parameters()
                        }
                        for param_name, param in module.named_parameters():
                            assert isinstance(param, BRRRParameter)
                            if param.is_tied:
                                tied_info = param.get_tied_info()
                                full_param_name = tied_info.get_full_name_from_module_id_to_prefix(
                                    module_id_to_prefix=module_id_to_prefix
                                )
                            else:
                                full_param_name = f"{module_name}.{param_name}"

                            if full_param_name in initialized_parameters:
                                # Already initialized
                                continue

                            if "weight" == param_name:
                                init_method_(param)
                            elif "bias" == param_name:
                                param.zero_()
                            else:
                                raise ValueError(f"Who the fuck is {param_name}?")

                            assert full_param_name not in initialized_parameters
                            initialized_parameters.add(full_param_name)
                    elif isinstance(module, TensorParallelRowLinear):
                        # Somehow Megatron-LM does something super complicated, https://github.com/NVIDIA/Megatron-LM/blob/2360d732a399dd818d40cbe32828f65b260dee11/megatron/core/tensor_parallel/layers.py#L96
                        # What it does:
                        #  - instantiate a buffer of the `full size` in fp32
                        #  - run init method on it
                        #  - shard result to get only a specific shard
                        # Instead I'm lazy and just going to run init_method, since they are scalar independent
                        assert {"weight", "bias"} == {name for name, _ in module.named_parameters()} or {"weight"} == {
                            name for name, _ in module.named_parameters()
                        }
                        for param_name, param in module.named_parameters():
                            assert isinstance(param, BRRRParameter)
                            if param.is_tied:
                                tied_info = param.get_tied_info()
                                full_param_name = tied_info.get_full_name_from_module_id_to_prefix(
                                    module_id_to_prefix=module_id_to_prefix
                                )
                            else:
                                full_param_name = f"{module_name}.{param_name}"

                            if full_param_name in initialized_parameters:
                                # Already initialized
                                continue

                            if "weight" == param_name:
                                scaled_init_method_(param)
                            elif "bias" == param_name:
                                param.zero_()
                            else:
                                raise ValueError(f"Who the fuck is {param_name}?")

                            assert full_param_name not in initialized_parameters
                            initialized_parameters.add(full_param_name)
                    elif isinstance(module, LayerNorm):
                        assert {"weight", "bias"} == {name for name, _ in module.named_parameters()}
                        for param_name, param in module.named_parameters():
                            assert isinstance(param, BRRRParameter)
                            if param.is_tied:
                                tied_info = param.get_tied_info()
                                full_param_name = tied_info.get_full_name_from_module_id_to_prefix(
                                    module_id_to_prefix=module_id_to_prefix
                                )
                            else:
                                full_param_name = f"{module_name}.{param_name}"

                            if full_param_name in initialized_parameters:
                                # Already initialized
                                continue

                            if "weight" == param_name:
                                # TODO @thomasw21: Sometimes we actually want 0
                                param.fill_(1)
                            elif "bias" == param_name:
                                param.zero_()
                            else:
                                raise ValueError(f"Who the fuck is {param_name}?")

                            assert full_param_name not in initialized_parameters
                            initialized_parameters.add(full_param_name)
                    elif os.environ.get("USE_FAST") and isinstance(module, MQAColumnLinears):
                        # TODO @thomasw21: Handle the non fast version
                        # Somehow Megatron-LM does something super complicated, https://github.com/NVIDIA/Megatron-LM/blob/2360d732a399dd818d40cbe32828f65b260dee11/megatron/core/tensor_parallel/layers.py#L96
                        # What it does:
                        #  - instantiate a buffer of the `full size` in fp32
                        #  - run init method on it
                        #  - shard result to get only a specific shard
                        # Instead I'm lazy and just going to run init_method, since they are scalar independent
                        # TODO @thomasw21: handle the case there's no bias
                        assert {"q.weight", "q.bias", "kv.weight", "kv.bias"} == {
                            name for name, _ in module.named_parameters()
                        }
                        for param_name, param in module.named_parameters():
                            assert isinstance(param, BRRRParameter)
                            if param.is_tied:
                                tied_info = param.get_tied_info()
                                full_param_name = tied_info.get_full_name_from_module_id_to_prefix(
                                    module_id_to_prefix=module_id_to_prefix
                                )
                            else:
                                full_param_name = f"{module_name}.{param_name}"

                            if full_param_name in initialized_parameters:
                                # Already initialized
                                continue

                            if ".weight" in param_name:
                                init_method_(param)
                            elif ".bias" in param_name:
                                param.zero_()
                            else:
                                raise ValueError(f"Who the fuck is {param_name}?")

                            assert full_param_name not in initialized_parameters
                            initialized_parameters.add(full_param_name)
                    elif isinstance(module, TensorParallelEmbedding):
                        # TODO @thomasw21: Handle tied embeddings
                        # Somehow Megatron-LM does something super complicated, https://github.com/NVIDIA/Megatron-LM/blob/2360d732a399dd818d40cbe32828f65b260dee11/megatron/core/tensor_parallel/layers.py#L96
                        # What it does:
                        #  - instantiate a buffer of the `full size` in fp32
                        #  - run init method on it
                        #  - shard result to get only a specific shard
                        # Instead I'm lazy and just going to run init_method, since they are scalar independent
                        assert {"weight"} == {name for name, _ in module.named_parameters()}

                        assert isinstance(module.weight, BRRRParameter)
                        if module.weight.is_tied:
                            tied_info = module.weight.get_tied_info()
                            full_param_name = tied_info.get_full_name_from_module_id_to_prefix(
                                module_id_to_prefix=module_id_to_prefix
                            )
                        else:
                            full_param_name = f"{module_name}.weight"

                        if full_param_name in initialized_parameters:
                            # Already initialized
                            continue

                        init_method_(module.weight)
                        assert full_param_name not in initialized_parameters
                        initialized_parameters.add(full_param_name)

            assert initialized_parameters == {
                param.get_tied_info().get_full_name_from_module_id_to_prefix(module_id_to_prefix=module_id_to_prefix)
                if param.is_tied
                else name
                for name, param in model.named_parameters()
            }, f"Somehow the initialized set of parameters don't match:\n - Expected: { {name for name, _ in model.named_parameters()} }\n - Got: {initialized_parameters}"

            # Synchronize parameters so that the model is consistent
            for name, param in sorted(model.named_parameters(), key=lambda x: x[0]):
                # sync across dp
                dist.all_reduce(param, op=dist.ReduceOp.AVG, group=dpg.dp_pg)

            for (_, group_ranks), param in sorted(
                get_tied_id_to_param(
                    parameters=model.parameters(),
                    root_module=model.module if isinstance(model, DistributedDataParallel) else model,
                ).items(),
                key=lambda x: x[0],
            ):
                group = dpg.world_ranks_to_pg[group_ranks]
                dist.all_reduce(param, op=dist.ReduceOp.AVG, group=group)
        else:
            raise ValueError(f"Unsupported {config.model.init_method}")

    # Init optimizer
    optimizer, grad_accumulator = init_optimizer_and_grad_accumulator(
        model=model, optimizer_args=optimizer_args, dpg=dpg
    )
    if checkpoint_path is not None:
        # TODO @thomasw21: @loubnabnl had issues loading an optimizer state causing OOM errors (something like memory fragmentation)
        # Setting map_location to "cuda" in such case. This is a hotfix to get it back up and running.
        load_optimizer(optimizer=optimizer, dpg=dpg, root_folder=checkpoint_path, map_location="cuda")

    # Init learning rate scheduler
    lr_scheduler_args = config.learning_rate_scheduler
    lr_scheduler = lr_scheduler_builder(
        optimizer=optimizer, learning_rate=config.optimizer.learning_rate, lr_scheduler_args=lr_scheduler_args
    )
    if checkpoint_path is not None:
        load_lr_scheduler(
            lr_scheduler=lr_scheduler,
            dpg=dpg,
            root_folder=checkpoint_path,
            is_zero=optimizer.inherit_from(ZeroDistributedOptimizer),
        )

    # Define iteration start state
    start_iteration_step: int
    consumed_train_samples: int
    if checkpoint_path is not None:
        checkpoint_metadata = load_meta(dpg=dpg, root_folder=checkpoint_path)
        log_rank(str(checkpoint_metadata), logger=logger, level=logging.INFO, rank=0)
        start_iteration_step = checkpoint_metadata.metas["last_train_step"]
        consumed_train_samples = checkpoint_metadata.metas["consumed_train_samples"]
        assert (
            config.tokens.train_steps > start_iteration_step
        ), f"Loaded checkpoint has already trained {start_iteration_step} batches, you need to specify a higher `config.tokens.train_steps`"
    else:
        start_iteration_step = 0
        consumed_train_samples = 0

    # Log where each module is instantiated
    for name, module in model.named_modules():
        if not isinstance(module, PipelineBlock):
            continue
        log_rank(
            f"module_name: {name} | PP: {module.rank}/{dpg.pp_pg.size()}",
            logger=logger,
            level=logging.DEBUG,
            group=dpg.world_pg,
            rank=0,
        )

    dist.barrier()
    log_rank(
        f"Global rank: { dist.get_rank(dpg.world_pg)}/{dpg.world_pg.size()} | PP: {dist.get_rank(dpg.pp_pg)}/{dpg.pp_pg.size()} | DP: {dist.get_rank(dpg.dp_pg)}/{dpg.dp_pg.size()} | TP: {dist.get_rank(dpg.tp_pg)}/{dpg.tp_pg.size()}",
        logger=logger,
        level=logging.INFO,
    )
    dist.barrier()

    # Dummy hyper parameter
    micro_batch_size = config.tokens.micro_batch_size
    n_micro_batches_per_batch = config.tokens.batch_accumulation_per_replica
    global_batch_size = micro_batch_size * n_micro_batches_per_batch * dpg.dp_pg.size()
    sequence_length = config.tokens.sequence_length

    # Create a dummy data loader
    if isinstance(model, DistributedDataParallel):
        input_pp_rank = model.module.model.token_position_embeddings.rank
        output_pp_rank = model.module.loss.rank
    else:
        input_pp_rank = model.model.token_position_embeddings.rank
        output_pp_rank = model.loss.rank

    def to_cuda(dataloader):
        for batch in dataloader:
            micro_batch = {
                k: v if isinstance(v, TensorPointer) else v.to("cuda", memory_format=torch.contiguous_format)
                for k, v in batch.items()
            }

            if not config.general.ignore_sanity_checks:
                # SANITY CHECK: Check input are not the same across DP
                for key, value in sorted(micro_batch.items(), key=lambda x: x[0]):
                    if isinstance(value, TensorPointer):
                        continue

                    if "mask" in key:
                        # It's fine if mask is the same across DP
                        continue

                    with assert_fail_except_rank_with(AssertionError, rank_exception=0, pg=dpg.dp_pg):
                        assert_tensor_synced_across_pg(tensor=value, pg=dpg.dp_pg, msg=lambda err: f"{key} {err}")

                # SANITY CHECK: Check input are synchronized throughout TP
                for key, value in sorted(micro_batch.items(), key=lambda x: x[0]):
                    if isinstance(value, TensorPointer):
                        continue
                    assert_tensor_synced_across_pg(
                        tensor=value,
                        pg=dpg.tp_pg,
                        msg=lambda err: f"{key} are not synchronized throughout TP {err}",
                    )

                # SANITY CHECK: Check that input are synchronized throughout PP
                # TODO @thomasw21: That's really hard to test as input gets sharded across the PP, let's assume it works for now.

            yield micro_batch

    if config.data.dataset is None:
        log_rank("Using dummy data generator", logger=logger, level=logging.INFO, rank=0)
        data_iterator = dummy_infinite_data_generator(
            micro_batch_size=micro_batch_size,
            sequence_length=sequence_length,
            input_pp_rank=input_pp_rank,
            output_pp_rank=output_pp_rank,
            vocab_size=model_config.vocab_size,
            seed=config.data.seed,
            dpg=dpg,
        )()
    elif isinstance(config.data.dataset, PretrainNemoArgs):
        log_rank("Using Nemo Dataloader", logger=logger, level=logging.INFO, rank=0)

        train_dataset, valid_dataset, test_datasets = get_nemo_datasets(
            config=config.data.dataset,
            global_batch_size=global_batch_size,
            sequence_length=config.tokens.sequence_length,
            train_steps=config.tokens.train_steps,
            limit_val_batches=config.tokens.limit_val_batches,
            val_check_interval=config.tokens.val_check_interval,
            test_iters=config.tokens.limit_test_batches,
            seed=config.data.seed,
            dpg=dpg,
        )
        dataloader = get_nemo_dataloader(
            dataset=train_dataset,
            sequence_length=sequence_length,
            micro_batch_size=micro_batch_size,
            global_batch_size=global_batch_size,
            num_workers=config.data.num_loading_workers,
            cfg=config.data.dataset,
            consumed_samples=consumed_train_samples,
            dpg=dpg,
            input_pp_rank=input_pp_rank,
            output_pp_rank=output_pp_rank,
            dataloader_drop_last=True,
        )
        data_iterator = to_cuda(dataloader)
    elif isinstance(config.data.dataset, PretrainDatasetsArgs):
        log_rank("Using `datasets` library", logger=logger, level=logging.INFO, rank=0)

        with main_rank_first(dpg.world_pg):
            # TODO @nouamanetazi: this may timeout before 1st device finishes processing dataset. Can we have a ctxmanager to modify timeout?
            # 1st device processes dataset and cache it, then other devices load from cache
            raw_dataset = load_dataset(
                config.data.dataset.hf_dataset_name,
                config.data.dataset.hf_dataset_config_name,
                split=config.data.dataset.hf_dataset_split,
            )
            tokenizer_name = config.tokenizer.hf_tokenizer_name
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

        train_dataset = clm_process(
            raw_dataset=raw_dataset,
            tokenizer=tokenizer,
            text_column_name=config.data.dataset.text_column_name,
            dataset_processing_num_proc_per_process=config.data.dataset.dataset_processing_num_proc_per_process,
            dataset_overwrite_cache=config.data.dataset.dataset_overwrite_cache,
            sequence_length=sequence_length,
        )
        dataloader = get_train_dataloader(
            train_dataset=train_dataset,
            sequence_length=sequence_length,
            dpg=dpg,
            input_pp_rank=input_pp_rank,
            output_pp_rank=output_pp_rank,
            micro_batch_size=micro_batch_size,
            dataloader_num_workers=config.data.num_loading_workers,
            seed_worker=config.data.seed,
            dataloader_drop_last=True,
        )
        data_iterator = to_cuda(dataloader)
    else:
        raise ValueError(f"Unhandled case of `config.data.dataset`. Got: {config.data.dataset}")

    # Backward from time to time
    # TODO @thomasw21: Make a much better API
    pipeline_engine: PipelineEngine = config.parallelism.pp_engine

    log_rank(
        f"[Before the start of training] datetime: {datetime.datetime.now()}",
        logger=logger,
        level=logging.INFO,
        rank=0,
    )
    start_time = time.time()

    if config.profile is not None:
        if config.profile.profiler_export_path is not None:
            on_trace_ready = tensorboard_trace_handler(config.profile.profiler_export_path)
        else:
            on_trace_ready = None
        prof = profile(
            activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
            # schedule=torch.profiler.schedule(wait=1, warmup=1, active=3, repeat=2),
            on_trace_ready=on_trace_ready,
            record_shapes=True,
            profile_memory=True,
            with_stack=True,
        )
    else:
        prof = contextlib.nullcontext()

    # Kill switch
    if config.general.kill_switch_path.exists():
        log_rank(
            f"Detected kill switch at {config.general.kill_switch_path}. Exiting",
            logger=logger,
            level=logging.INFO,
            rank=0,
        )
        sys.exit(0)

    # Useful mapping
    normalized_model = model.module if isinstance(model, DistributedDataParallel) else model
    module_id_to_prefix = {id(module): f"{module_name}." for module_name, module in normalized_model.named_modules()}
    # Fix the root_model
    module_id_to_prefix[id(normalized_model)] = ""

    with tb_context as tb_writer:
        with prof:
            for iteration_step in range(start_iteration_step, config.tokens.train_steps):
                if not config.general.ignore_sanity_checks:
                    # SANITY CHECK: Check that the model params are synchronized across dp
                    for name, param in sorted(model.named_parameters(), key=lambda x: x[0]):
                        assert_tensor_synced_across_pg(
                            tensor=param, pg=dpg.dp_pg, msg=lambda err: f"{name} are not synchronized across DP {err}"
                        )

                    # SANITY CHECK: Tied weights are synchronized
                    tied_params_list = sorted(
                        get_tied_id_to_param(
                            parameters=normalized_model.parameters(),
                            root_module=normalized_model,
                        ).items(),
                        key=lambda x: x[0],
                    )

                    tied_params_list_kv_name = [
                        name for (name, _group_ranks), param in tied_params_list if ".qkv.kv." in name
                    ]
                    assert len(tied_params_list_kv_name) != 0, "kv weights and bias are not tied"

                    for (name, group_ranks), param in tied_params_list:
                        group = dpg.world_ranks_to_pg[group_ranks]
                        assert_tensor_synced_across_pg(
                            tensor=param,
                            pg=group,
                            msg=lambda err: f"[Before train] Tied weights {name} are not synchronized. {err}",
                        )

                # SANITY CHECK: Check that the grad accumulator buffers are ready for DDP
                if not config.general.ignore_sanity_checks:
                    if grad_accumulator is not None:
                        for _, elt in grad_accumulator.fp32_grad_buffers.items():
                            fp32_grad_buffer = elt["fp32_grad"]
                            torch.testing.assert_close(
                                fp32_grad_buffer,
                                torch.zeros_like(fp32_grad_buffer),
                                atol=0,
                                rtol=0,
                                msg="Grad accumulator buffers must be zeroed in first accumulation step.",
                            )

                outputs = pipeline_engine.train_batch_iter(
                    model=model,
                    pg=dpg.pp_pg,
                    batch=(next(data_iterator) for _ in range(n_micro_batches_per_batch)),
                    grad_accumulator=grad_accumulator,
                )

                if iteration_step == 0:
                    log_rank(
                        f"[After train batch iter] Memory usage: {torch.cuda.memory_allocated() / 1024**2:.2f}MB. Peak reserved memory: {torch.cuda.max_memory_reserved() / 1024**2:.2f}MB",
                        logger=logger,
                        level=logging.DEBUG,
                        group=dpg.dp_pg,
                        rank=0,
                    )

                if not config.general.ignore_sanity_checks:
                    # SANITY CHECK: Check that gradient flow on the entire model
                    # SANITY CHECK: Check that all parameters that required gradients, have actually a gradient
                    # SANITY CHECK: Check for nan/inf
                    for name, param in normalized_model.named_parameters():
                        if not param.requires_grad:
                            continue

                        if param.is_tied:
                            tied_info = param.get_tied_info()
                            name = tied_info.get_full_name_from_module_id_to_prefix(
                                module_id_to_prefix=module_id_to_prefix
                            )

                        if grad_accumulator is not None:
                            grad = grad_accumulator.get_grad_buffer(name=name)
                        else:
                            grad = param.grad

                        if torch.isnan(grad).any() or torch.isinf(grad).any():
                            raise ValueError("Gradient is nan or inf")
                        if grad is None:
                            log_rank(
                                f"Process rank { dist.get_rank(dpg.world_pg)}/{dpg.world_pg.size()}: {name} is missing gradient",
                                logger=logger,
                                level=logging.ERROR,
                            )

                # Sync tied weights
                # TODO @thomasw21: Put this in hooks so we can overlap communication with gradient computation on the last backward pass.
                sync_tied_weights_gradients(
                    module=normalized_model,
                    dpg=dpg,
                    grad_accumulator=grad_accumulator,
                )
                if not isinstance(model, DistributedDataParallel):
                    # Manually sync across DP if it's not handled by DDP
                    sync_gradients_across_dp(
                        module=model,
                        dp_pg=dpg.dp_pg,
                        reduce_op=dist.ReduceOp.AVG,
                        # TODO @thomasw21: This is too memory hungry, instead we run all_reduce
                        reduce_scatter=False,  # optimizer.inherit_from(ZeroDistributedOptimizer),
                        grad_accumulator=grad_accumulator,
                    )

                if not config.general.ignore_sanity_checks:
                    # SANITY CHECK: Test tied weights gradients are synchronized
                    for (name, group_ranks), param in sorted(
                        get_tied_id_to_param(
                            parameters=normalized_model.parameters(),
                            root_module=normalized_model,
                        ).items(),
                        key=lambda x: x[0],
                    ):
                        if not param.requires_grad:
                            continue

                        if grad_accumulator is not None:
                            grad = grad_accumulator.get_grad_buffer(name=name)
                        else:
                            grad = param.grad

                        assert grad is not None, f"Grad is None for {name}"
                        group = dpg.world_ranks_to_pg[group_ranks]
                        assert_tensor_synced_across_pg(
                            tensor=grad,
                            pg=group,
                            msg=lambda err: f"[Before gradient clipping] Tied weights grads for {name} are not synchronized. {err}",
                        )

                    # SANITY CHECK: Test gradients are synchronized across DP
                    for name, param in sorted(normalized_model.named_parameters(), key=lambda x: x[0]):
                        if not param.requires_grad:
                            continue

                        if param.is_tied:
                            tied_info = param.get_tied_info()
                            name = tied_info.get_full_name_from_module_id_to_prefix(
                                module_id_to_prefix=module_id_to_prefix
                            )

                        if grad_accumulator is not None:
                            grad = grad_accumulator.get_grad_buffer(name=name)
                        else:
                            grad = param.grad

                        assert grad is not None, f"Grad is None for {name}"
                        assert_tensor_synced_across_pg(
                            tensor=grad,
                            pg=dpg.dp_pg,
                            msg=lambda err: f"[Before gradient clipping] weights grads for {name} are not synchronized across DP. {err}",
                        )

                # Clip gradients
                grad_norm_unclipped = None
                if config.optimizer.clip_grad is not None:
                    # Normalize DDP
                    named_parameters = [
                        (
                            param.get_tied_info().get_full_name_from_module_id_to_prefix(
                                module_id_to_prefix=module_id_to_prefix
                            )
                            if param.is_tied
                            else name,
                            param,
                        )
                        for name, param in normalized_model.named_parameters()
                    ]
                    grad_norm_unclipped = clip_grad_norm(
                        mp_pg=dpg.world_ranks_to_pg[
                            tuple(sorted(dpg.world_rank_matrix[:, dist.get_rank(dpg.dp_pg), :].reshape(-1)))
                        ],
                        named_parameters=named_parameters,
                        grad_accumulator=grad_accumulator,
                        max_norm=config.optimizer.clip_grad,
                    )

                if not config.general.ignore_sanity_checks:
                    # SANITY CHECK: Test tied weights gradients are synchronized
                    for (name, group_ranks), param in sorted(
                        get_tied_id_to_param(
                            parameters=normalized_model.parameters(), root_module=normalized_model
                        ).items(),
                        key=lambda x: x[0],
                    ):
                        if not param.requires_grad:
                            continue

                        if grad_accumulator is not None:
                            grad = grad_accumulator.get_grad_buffer(name=name)
                        else:
                            grad = param.grad

                        assert grad is not None, f"Grad is None for {name}"
                        group = dpg.world_ranks_to_pg[group_ranks]
                        assert_tensor_synced_across_pg(
                            tensor=grad,
                            pg=group,
                            msg=lambda err: f"[Before optimizer step] Tied weights grads for {name} are not synchronized. {err}",
                        )

                    # SANITY CHECK: Test gradients are synchronized across DP
                    for name, param in sorted(normalized_model.named_parameters(), key=lambda x: x[0]):
                        if not param.requires_grad:
                            continue

                        if param.is_tied:
                            tied_info = param.get_tied_info()
                            name = tied_info.get_full_name_from_module_id_to_prefix(
                                module_id_to_prefix=module_id_to_prefix
                            )

                        if grad_accumulator is not None:
                            grad = grad_accumulator.get_grad_buffer(name=name)
                        else:
                            grad = param.grad

                        assert grad is not None, f"Grad is None for {name}"
                        assert_tensor_synced_across_pg(
                            tensor=grad,
                            pg=dpg.dp_pg,
                            msg=lambda err: f"[Before optimizer step] weights grads for {name} are not synchronized across DP. {err}",
                        )

                if not config.general.ignore_sanity_checks:
                    # SANITY CHECK: Check that the model params are synchronized across dp
                    for name, param in sorted(model.named_parameters(), key=lambda x: x[0]):
                        assert_tensor_synced_across_pg(
                            tensor=param, pg=dpg.dp_pg, msg=lambda err: f"{name} are not synchronized across DP {err}"
                        )

                    # SANITY CHECK: Tied weights are synchronized
                    tied_params_list = sorted(
                        get_tied_id_to_param(
                            parameters=normalized_model.parameters(), root_module=normalized_model
                        ).items(),
                        key=lambda x: x[0],
                    )

                    tied_params_list_kv_name = [
                        name for (name, _group_ranks), param in tied_params_list if ".qkv.kv." in name
                    ]
                    assert len(tied_params_list_kv_name) != 0, "kv weights and bias are not tied"

                    for (name, group_ranks), param in tied_params_list:
                        group = dpg.world_ranks_to_pg[group_ranks]
                        assert_tensor_synced_across_pg(
                            tensor=param,
                            pg=group,
                            msg=lambda err: f"[Before optimizer step] Tied weights {name} are not synchronized. {err}",
                        )

                # Apply gradient
                optimizer.step()
                # PT 2.0: will change default to None as it gains performance.
                # https://github.com/pytorch/pytorch/issues/92656
                optimizer.zero_grad(set_to_none=True)

                # Update the learning rate
                lr_scheduler.step()

                if not config.general.ignore_sanity_checks:
                    # SANITY CHECK: Check that gradients is cleared
                    for name, param in model.named_parameters():
                        if not param.requires_grad:
                            continue

                        if param.grad is not None:
                            log_rank(
                                f"Process rank { dist.get_rank(dpg.world_pg)}/{dpg.world_pg.size()}: {name} still has gradient despite having ran the optimizer",
                                logger=logger,
                                level=logging.ERROR,
                            )

                # Training Logs
                iteration_step += 1
                consumed_train_samples += global_batch_size

                if iteration_step % config.logging.iteration_step_info_interval == 0:
                    # TODO @nouamanetazi: Megatron-LM seems to be using a barrier to report their interval time. Check if this is necessary. https://github.com/NouamaneTazi/Megatron-LM/blob/e241a96c3085b18e36c6cee1d68a8155de77b5a6/megatron/training.py#L607
                    dist.barrier()
                    torch.cuda.synchronize()
                    elapsed_time_per_iteration_ms = (
                        (time.time() - start_time) / config.logging.iteration_step_info_interval * 1000
                    )
                    tokens_per_sec = (
                        global_batch_size * sequence_length / (elapsed_time_per_iteration_ms / 1000)
                    )  # tokens_per_sec is calculated using sequence_length
                    model_tflops, hardware_tflops = get_flops_per_sec(
                        iteration_time_in_sec=elapsed_time_per_iteration_ms / 1000,
                        world_size=dpg.world_pg.size(),
                        num_layers=model_config.num_layers,
                        hidden_size=model_config.hidden_size,
                        num_heads=model_config.num_attention_heads,
                        vocab_size=model_config.vocab_size,
                        seq_len=sequence_length,
                        ffn_hidden_size=model_config.ffn_hidden_size,
                        batch_size=global_batch_size,
                        recompute_granularity=config.parallelism.recompute_granularity,
                    )
                    if (
                        dist.get_rank(dpg.pp_pg) == dpg.pp_pg.size() - 1
                        and dist.get_rank(dpg.tp_pg) == 0
                        and dist.get_rank(dpg.dp_pg) == 0
                    ):
                        assert all(not isinstance(output, TensorPointer) for output in outputs)
                        # This is an average on only one data rank.
                        loss_avg_per_mbs = torch.tensor(outputs).mean().item()
                        lr = lr_scheduler.get_last_lr()[0]

                        log_entries = [
                            LogItem("consumed_samples", iteration_step * global_batch_size, "12d"),
                            LogItem("elapsed_time_per_iteration_ms", elapsed_time_per_iteration_ms, ".1f"),
                            LogItem("tokens_per_sec", tokens_per_sec, "1.6E"),
                            LogItem("tokens_per_sec_per_gpu", tokens_per_sec / dpg.world_pg.size(), "1.6E"),
                            LogItem("global_batch_size", global_batch_size, "5d"),
                            LogItem("lm_loss", loss_avg_per_mbs, "1.6E"),
                            LogItem("lr", lr, ".3E"),
                            LogItem("model_tflops_per_gpu", model_tflops, ".2f"),
                            LogItem("hardware_tflops_per_gpu", hardware_tflops, ".2f"),
                        ]

                        if grad_norm_unclipped is not None:
                            log_entries.append(LogItem("grad_norm", grad_norm_unclipped, ".3f"))

                        if tb_writer is not None:
                            tb_writer.add_scalars_from_list(log_entries, iteration_step)
                        loggerwriter.add_scalars_from_list(log_entries, iteration_step)

                    start_time = time.time()

                # Kill switch
                if config.general.kill_switch_path.exists():
                    log_rank(
                        f"Detected kill switch at {config.general.kill_switch_path}. Exiting",
                        logger=logger,
                        level=logging.INFO,
                        rank=0,
                    )

                    # Save checkpoint
                    save_checkpoint(
                        model=model,
                        optimizer=optimizer,
                        lr_scheduler=lr_scheduler,
                        random_states=random_states,
                        iteration_step=iteration_step,
                        consumed_train_samples=consumed_train_samples,
                        train_steps=config.tokens.train_steps,
                        checkpoints_path=config.checkpoints.checkpoints_path,
                        dpg=dpg,
                    )
                    # Upload checkpoint
                    if config.checkpoints.upload_s3_path is not None:
                        previous_upload_process = upload_checkpoint(
                            checkpoint_path=config.checkpoints.checkpoints_path,
                            upload_s3_path=config.checkpoints.upload_s3_path,
                            upload_s3_num_workers=config.checkpoints.upload_s3_num_workers,
                            previous_upload_process=previous_upload_process,
                            group=dpg.world_pg,
                        )

                    # TODO @thomasw21: Do I need to return a barrier in order to be sure everyone saved before exiting.
                    sys.exit(0)

                # Checkpoint
                if iteration_step % config.checkpoints.checkpoint_interval == 0:
                    save_checkpoint(
                        model=normalized_model,
                        optimizer=optimizer,
                        lr_scheduler=lr_scheduler,
                        random_states=random_states,
                        iteration_step=iteration_step,
                        consumed_train_samples=consumed_train_samples,
                        train_steps=config.tokens.train_steps,
                        checkpoints_path=config.checkpoints.checkpoints_path,
                        dpg=dpg,
                    )
                    # Upload checkpoint
                    if config.checkpoints.upload_s3_path:
                        previous_upload_process = upload_checkpoint(
                            checkpoint_path=config.checkpoints.checkpoints_path,
                            upload_s3_path=config.checkpoints.upload_s3_path,
                            upload_s3_num_workers=config.checkpoints.upload_s3_num_workers,
                            previous_upload_process=previous_upload_process,
                            group=dpg.world_pg,
                        )

                if not config.general.ignore_sanity_checks:
                    # SANITY CHECK: Check that the model params are synchronized
                    for name, param in sorted(model.named_parameters(), key=lambda x: x[0]):
                        assert_tensor_synced_across_pg(
                            tensor=param, pg=dpg.dp_pg, msg=lambda err: f"{name} is not synced across DP. {err}"
                        )

                    # SANITY CHECK: Tied weights are synchronized
                    for (name, group_ranks), param in sorted(
                        get_tied_id_to_param(
                            parameters=normalized_model.parameters(), root_module=normalized_model
                        ).items(),
                        key=lambda x: x[0],
                    ):
                        group = dpg.world_ranks_to_pg[group_ranks]
                        assert_tensor_synced_across_pg(
                            tensor=param,
                            pg=group,
                            msg=lambda err: f"[After train] Tied weights {name} are not synchronized. {err}",
                        )

    if isinstance(prof, profile) and prof.on_trace_ready is None:
        log_rank(
            prof.key_averages(group_by_stack_n=5).table(
                sort_by="self_cuda_time_total", row_limit=20, max_name_column_width=150
            ),
            logger=logger,
            level=logging.INFO,
            rank=0,
        )

    # Test saving
    checkpoint_path = save_checkpoint(
        model=normalized_model,
        optimizer=optimizer,
        lr_scheduler=lr_scheduler,
        random_states=random_states,
        iteration_step=config.tokens.train_steps,
        consumed_train_samples=consumed_train_samples,
        train_steps=config.tokens.train_steps,
        checkpoints_path=config.checkpoints.checkpoints_path,
        dpg=dpg,
    )

    # Done training: we run a set of validation at the end
    log_rank(
        f"Finished training with iteration {config.tokens.train_steps}", logger=logger, level=logging.INFO, rank=0
    )

    # Wait til everything is saved to begin loading
    dist.barrier()

    # Test that saved checkpoint has save everything correctly.
    # NOTE: it's important to have same zero stage to be able to compare the optimizer state dict
    new_model, new_random_states = init_model(
        model_config=model_config,
        dtype=config.model.dtype,
        dpg=dpg,
        # We load the model without passing a training args since we don't actually compare any training dynamics.
        parallel_config=None,
        # TODO @thomasw21: Figure out why using DDP with accumulate_in_fp_32 and ZeRO-1 performs poorly.
        make_ddp=not (optimizer_args.accumulate_grad_in_fp32 and optimizer_args.zero_stage > 0),
    )
    new_optimizer, new_grad_accumulator = init_optimizer_and_grad_accumulator(
        model=new_model, optimizer_args=optimizer_args, dpg=dpg
    )
    new_lr_scheduler = lr_scheduler_builder(
        optimizer=new_optimizer, learning_rate=optimizer_args.learning_rate, lr_scheduler_args=lr_scheduler_args
    )
    load(
        model=new_model.module if isinstance(new_model, DistributedDataParallel) else new_model,
        optimizer=new_optimizer,
        lr_scheduler=new_lr_scheduler,
        dpg=dpg,
        root_folder=checkpoint_path,
    )

    # SANITY CHECK: Check that the loaded model match
    test_equal_dict(new_model.state_dict(), model.state_dict())
    # SANITY CHECK: Check that the loaded optimizer match
    if optimizer.inherit_from(ZeroDistributedOptimizer):
        assert new_optimizer.inherit_from(ZeroDistributedOptimizer)
        # TODO @thomasw21: Check that the optimizer state corresponds to the non zero version
    else:
        assert not new_optimizer.inherit_from(ZeroDistributedOptimizer)
    test_equal_dict(new_optimizer.state_dict(), optimizer.state_dict())
    # SANITY CHECK: Check that the loaded optim scheduler match
    test_equal_dict(new_lr_scheduler.state_dict(), lr_scheduler.state_dict())

    # Check that random states are unequal
    assert new_random_states != random_states
    # TODO @thomasw21: The issue is that the random_states is already dispatched everywhere in the model.
    new_random_states = load_random_states(dpg=dpg, root_folder=checkpoint_path)
    assert new_random_states == random_states

    # Check that it converges.

    # Check TFLOPS


if __name__ == "__main__":
    main()
