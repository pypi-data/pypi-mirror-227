import argparse
import datetime
import logging as lg
import math
import sys
import time
from typing import Dict, List, Optional, Tuple

import datasets.utils.logging
import numpy as np
import torch
from dataclass import LRSchedulerArgs, OptimizerArgs, TrainingModelArgs
from dataloader import dummy_infinite_data_generator, get_dataloader, mlm_process
from datasets import concatenate_datasets, load_dataset
from flops import get_flops_per_sec
from generation import GenerationConfig, GenerationInput, greedy_search
from modeling_t5 import T5ForTraining, T5LayerCrossAttention, T5LayerFF, T5LayerSelfAttention
from torch import nn
from torch.nn.parallel import DistributedDataParallel
from torch.optim.lr_scheduler import LambdaLR
from transformers import AutoTokenizer, T5Config
from upath import UPath

from brrr.core import distributed as dist
from brrr.core import logging
from brrr.core.dataclass import RandomStates
from brrr.core.gradient_accumulator import (
    FP32GradBucketManager,
    FP32GradientAccumulator,
    GradientAccumulator,
    get_fp32_accum_hook,
)
from brrr.core.logging import get_library_root_logger, log_levels, log_rank
from brrr.core.optimizer.base import BaseOptimizer, Optimizer
from brrr.core.optimizer.named_optimizer import NamedOptimizer
from brrr.core.optimizer.optimizer_from_gradient_accumulator import (
    OptimizerFromGradientAccumulator,
)
from brrr.core.optimizer.zero import ZeroDistributedOptimizer
from brrr.core.parallelism.parameters import BRRRParameter, sanity_check
from brrr.core.parallelism.pipeline_parallelism.block import PipelineBlock
from brrr.core.parallelism.pipeline_parallelism.engine import (
    AllForwardAllBackwardPipelineEngine,
    OneForwardOneBackwardPipelineEngine,
    PipelineEngine,
)
from brrr.core.parallelism.pipeline_parallelism.tensor_pointer import TensorPointer
from brrr.core.parallelism.pipeline_parallelism.utils import get_pp_rank_of
from brrr.core.parallelism.tensor_parallelism.enum import TensorParallelLinearMode
from brrr.core.parallelism.tensor_parallelism.nn import TensorParallelColumnLinear
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
from brrr.core.serialize import load, load_random_states, save, save_random_states
from brrr.core.serialize.path import check_path_is_local
from brrr.core.utils import (
    assert_fail_except_rank_with,
    assert_tensor_synced_across_pg,
    init_on_device_and_dtype,
    main_rank_first,
)

logger = get_library_root_logger()
# TODO @thomasw21: Remove once we figure out how to reduce significantly the amount of logs.
datasets.utils.logging.set_verbosity(datasets.utils.logging.CRITICAL)

try:
    from apex.optimizers import FusedAdam as AdamW

    logger.warning("Discovered apex.optimizers.FusedAdam - will use it instead of torch.optim.AdamW")
except Exception:
    from torch.optim import AdamW

"""
Example on how to use `brrr` to build a t5 model with PP=2 and TP=2
"""


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dp", type=int, default=1)
    parser.add_argument("--tp", type=int, default=1)
    parser.add_argument("--pp", type=int, default=1)
    parser.add_argument(
        "--pp-engine",
        type=str,
        required=True,
        choices=["1f1b", "afab"],
        help="Choose which pipeline engine to use",
    )
    parser.add_argument("--dtype", type=str, default="float32")

    # Model
    parser.add_argument("--hf-t5-model-name", type=str, required=True)

    # Dataset processing
    parser.add_argument("--hf-dataset-name", type=str)
    parser.add_argument("--hf-dataset-config-name", type=str)
    parser.add_argument("--hf-dataset-split", type=str)
    parser.add_argument("--dataset-processing-num-proc-per-process", type=int)

    # Dataset loading
    parser.add_argument("--loading-num-proc-per-process", type=int)

    parser.add_argument("--seed", type=int, default=42)

    parser.add_argument("--num-batches", type=int, default=100)

    # Training model args
    parser.add_argument("--recompute-mode", type=str, choices=["selective"])
    parser.add_argument(
        "--tp-mode",
        type=lambda name: TensorParallelLinearMode[name.upper()],
        choices=list(TensorParallelLinearMode),
        default=TensorParallelLinearMode.ALL_REDUCE,
        help="Defines whether we run traditional TP or sequence parallel",
    )
    parser.add_argument("--micro-batch-size", type=int, default=2)
    parser.add_argument("--batch-accumulation-per-replica", type=int, default=64)
    parser.add_argument("--encoder-sequence-length", type=int, default=512)
    parser.add_argument("--decoder-sequence-length", type=int, default=114)

    # Gradient args
    parser.add_argument("--accumulate-grad-in-fp32", action="store_true")

    # Optimizer args
    parser.add_argument(
        "--zero-stage", type=int, choices=[0, 1], default=0, help="Zero stage to use. Can be 0 or 1. Default is 0."
    )
    parser.add_argument(
        "--weight-decay", type=float, default=0.01, help="Weight decay coefficient for L2 regularization."
    )
    parser.add_argument(
        "--adam-beta1",
        type=float,
        default=0.9,
        help="First coefficient for computing running averages " "of gradient and its square",
    )
    parser.add_argument(
        "--adam-beta2",
        type=float,
        default=0.999,
        help="Second coefficient for computing running averages " "of gradient and its square",
    )
    parser.add_argument(
        "--adam-eps", type=float, default=1e-08, help="Term added to the denominator to improve" "numerical stability"
    )

    # LR Scheduler args
    parser.add_argument("--learning-rate", type=float, required=True)
    parser.add_argument("--lr-warmup-style", type=str, default=None, choices=["linear"])
    parser.add_argument("--lr-warmup-steps", type=int, default=0, help="Number of steps to warmup LR over.")
    parser.add_argument("--lr-decay-style", type=str, default="linear", choices=["linear", "cosine"])
    parser.add_argument(
        "--lr-decay-steps",
        type=int,
        default=None,
        help="Number of steps to decay LR over, if None, will `--num-batches`.",
    )
    parser.add_argument("--min-decay-lr", type=float, default=0.0, help="Minimum LR to decay to.")

    # Checkpoint args
    # We use `upath.UPath` as it allows to have a Path implementation that works with other implementations of `fsspec`
    parser.add_argument(
        "--checkpoint-path", type=UPath, required=True, help="Where we store model weights/optimizer states."
    )

    parser.add_argument(
        "--log-level",
        type=str,
        choices=list(log_levels.keys()),
        required=True,
        help="Logger log level to use on the main process. Possible choices are the log levels as strings: 'debug', "
        "'info', 'warning', 'error' and 'critical', plus a 'passive' level which doesn't set anything and lets the "
        "application set the level.",
    )
    parser.add_argument(
        "--log-level-replica",
        type=str,
        choices=list(log_levels.keys()),
        required=True,
        help="Logger log level to use on replicas. Same choices as ``log_level``",
    )
    parser.add_argument(
        "--iteration-step-info-interval",
        type=int,
        default=1,
        help="Number of steps between each iteration step log message. Default is 1.",
    )

    # DEBUG
    parser.add_argument("--ignore-sanity-checks", action="store_true")

    args = parser.parse_args()

    str_to_dtype = {
        "float32": torch.float32,
        "float64": torch.float64,
        "complex64": torch.complex64,
        "complex128": torch.complex128,
        "float16": torch.float16,
        "bfloat16": torch.bfloat16,
        "uint8": torch.uint8,
        "int8": torch.int8,
        "int16": torch.int16,
        "int32": torch.int32,
        "int64": torch.int64,
        "bool": torch.bool,
    }
    args.dtype = str_to_dtype[args.dtype]

    set_random_seed(args.seed)

    # sanity check
    if args.accumulate_grad_in_fp32 and args.dtype == torch.float:
        raise ValueError(
            "Accumulating gradients in fp32 when model dtype is in fp32 is natively done via torch, no need to pass `--accumulate-grad-in-fp32`."
        )

    if args.hf_dataset_name is None:
        assert args.hf_dataset_split is None
        assert args.dataset_processing_num_proc_per_process is None
        assert args.loading_num_proc_per_process is None
    else:
        assert args.hf_dataset_split is not None
        assert args.dataset_processing_num_proc_per_process is not None
        assert args.loading_num_proc_per_process is not None

    if args.lr_decay_steps is None:
        args.lr_decay_steps = args.num_batches

    return args


def set_verbosity(logging_level: str):
    log_level = logging.log_levels[logging_level]
    logging.set_verbosity(log_level)
    logging.disable_default_handler()
    handler = lg.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    handler.flush = sys.stderr.flush
    logging.add_handler(handler)


def enable_explicit_format(dpg: DistributedProcessGroups) -> None:
    handlers = get_library_root_logger().handlers

    for handler in handlers:
        formatter = lg.Formatter(
            fmt=f"%(asctime)s [%(levelname)s|DP:{dist.get_rank(dpg.dp_pg)}|PP={dist.get_rank(dpg.pp_pg)}|TP={dist.get_rank(dpg.tp_pg)}|%(filename)s:%(lineno)s]: %(message)s",
            datefmt="%m/%d/%Y %H:%M:%S",
        )
        handler.setFormatter(formatter)


def init_model(
    config: T5Config,
    dtype: torch.dtype,
    dpg: DistributedProcessGroups,
    training_model_args: Optional[TrainingModelArgs],
    make_ddp: bool,
):
    # Get synchronized random states
    if training_model_args is None or training_model_args.tp_mode is TensorParallelLinearMode.ALL_REDUCE:
        random_states = RandomStates(
            {"tp_synced": get_synced_random_state(random_state=get_current_random_state(), pg=dpg.tp_pg)}
        )
    else:
        # We don't need to sync across TP when using sequence parallel (REDUCE_SCATTER)
        random_states = RandomStates({})

    # Load model
    model = T5ForTraining(config=config, dpg=dpg, training_model_args=training_model_args, random_states=random_states)

    # Set rank for each pipeline block
    pipeline_blocks: List[PipelineBlock] = [
        module for name, module in model.named_modules() if isinstance(module, PipelineBlock)
    ]
    # "cuda" is already defaulted for each process to it's own cuda device
    with init_on_device_and_dtype(device=torch.device("cuda"), dtype=dtype):
        # # Version 1: interleave layers, probably the worst thing one can do
        # for i, block in enumerate(pipeline_blocks):
        #     # WARNING: Highly inefficient mapping, as we interleave devices.
        #     block.build_and_set_rank(i % dpg.pp_pg.size())

        # # Version 2: Contiguous block of layers
        # contiguous_size = ceil(len(pipeline_blocks) / dpg.pp_pg.size())
        # for i, block in enumerate(pipeline_blocks):
        #     rank = i // contiguous_size
        #     block.build_and_set_rank(rank)

        # Version 3: Find only the blocks are are big
        block_compute_costs = {
            T5LayerSelfAttention: 4 * config.num_heads * config.d_kv * config.d_model,
            T5LayerCrossAttention: 4 * config.num_heads * config.d_kv * config.d_model,
            T5LayerFF: 2 * config.d_ff * config.d_model,
            # This is the last lm_head
            TensorParallelColumnLinear: config.vocab_size * config.d_model,
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
            "model.encoder_embedding.pp_block.weight",
            "model.decoder_embedding.pp_block.weight",
        ]
    ]
    tie_parameters(root_module=model, ties=shared_embeddings, dpg=dpg, reduce_op=dist.ReduceOp.SUM)

    # Tie relative position bias
    shared_encoder_position_bias = [
        (
            f"model.encoder.{layer_id}.self_attention_pp_block.pp_block.relative_attention_bias.relative_attention_bias.weight",
            (
                dpg.world_rank_matrix[
                    get_pp_rank_of(
                        f"model.encoder.{layer_id}.self_attention_pp_block.pp_block.relative_attention_bias.relative_attention_bias.weight",
                        module=model,
                    ),
                    dist.get_rank(dpg.dp_pg),
                    dist.get_rank(dpg.tp_pg),
                ],
            ),
        )
        for layer_id in range(config.num_layers)
    ]
    tie_parameters(root_module=model, ties=shared_encoder_position_bias, dpg=dpg, reduce_op=dist.ReduceOp.SUM)
    shared_decoder_position_bias = [
        (
            f"model.decoder.{layer_id}.self_attention_pp_block.pp_block.relative_attention_bias.relative_attention_bias.weight",
            (
                dpg.world_rank_matrix[
                    get_pp_rank_of(
                        f"model.decoder.{layer_id}.self_attention_pp_block.pp_block.relative_attention_bias.relative_attention_bias.weight",
                        module=model,
                    ),
                    dist.get_rank(dpg.dp_pg),
                    dist.get_rank(dpg.tp_pg),
                ],
            ),
        )
        for layer_id in range(config.num_decoder_layers)
    ]
    tie_parameters(root_module=model, ties=shared_decoder_position_bias, dpg=dpg, reduce_op=dist.ReduceOp.SUM)

    # Sync all parameters that have the same name and that are not sharded
    for name, param in model.named_parameters():
        if isinstance(param, BRRRParameter) and param.is_sharded:
            continue

        if "bias" in name:
            # bias parameters must not be tied because they only exist on first TP rank
            raise ValueError(f"T5 must not have any bias parameters, but found {name}")

        shared_weights = [
            (
                name,
                # This adds all the tp_ranks in one go
                tuple(sorted(dpg.world_rank_matrix[dist.get_rank(dpg.pp_pg), dist.get_rank(dpg.dp_pg), :])),
            )
        ]

        if training_model_args is None or training_model_args.tp_mode is TensorParallelLinearMode.ALL_REDUCE:
            # We add `reduce_op=None` in order to signal that the weight are synced by design without needing to reduce
            reduce_op = None
        else:
            reduce_op = dist.ReduceOp.SUM

        tie_parameters(root_module=model, ties=shared_weights, dpg=dpg, reduce_op=reduce_op)

    log_rank(
        "Finished making all tied parameters",
        logger=logger,
        level=logging.DEBUG,
    )

    create_pg_for_tied_weights(root_module=model, dpg=dpg)

    log_rank(
        "Finished creating all process groups",
        logger=logger,
        level=logging.DEBUG,
    )

    # Synchronize parameters so that the model is consistent
    for name, param in sorted(model.named_parameters(), key=lambda x: x[0]):
        # sync across dp
        dist.all_reduce(param, op=dist.ReduceOp.AVG, group=dpg.dp_pg)

    log_rank(
        "Finished syncing weights across data parallel",
        logger=logger,
        level=logging.DEBUG,
    )

    for (_, group_ranks), param in sorted(
        get_tied_id_to_param(parameters=model.parameters(), root_module=model).items(),
        key=lambda x: x[0],
    ):
        if len(group_ranks) == 1:
            continue
        group = dpg.world_ranks_to_pg[group_ranks]
        dist.all_reduce(param, op=dist.ReduceOp.AVG, group=group)

    log_rank(
        "Finished syncing weights across model parallel",
        logger=logger,
        level=logging.DEBUG,
    )

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
    module_id_to_prefix[id(normalized_model)] = ""

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
                lr=optimizer_args.lr,
                weight_decay=optimizer_args.weight_decay,
                eps=optimizer_args.adam_eps,
                betas=(optimizer_args.adam_beta1, optimizer_args.adam_beta2),
            ),
        )

    optimizer_builder = basic_optimizer_builder

    # Gradient accumulator builder
    grad_accumulator = None
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
    args = get_args()

    # Initialise all process groups
    dpg = get_process_groups(
        data_parallel_size=args.dp,
        pipeline_parallel_size=args.pp,
        tensor_parallel_size=args.tp,
    )

    # Set log levels
    if dist.get_rank(dpg.world_pg) == 0:
        if args.log_level is not None:
            set_verbosity(args.log_level)
    else:
        if args.log_level_replica is not None:
            set_verbosity(args.log_level_replica)
    enable_explicit_format(dpg)

    model_name = args.hf_t5_model_name
    config = T5Config.from_pretrained(model_name)
    training_model_args = TrainingModelArgs(recompute_mode=args.recompute_mode, tp_mode=args.tp_mode)
    optimizer_args = OptimizerArgs(
        zero_stage=args.zero_stage,
        accumulate_grad_in_fp32=args.accumulate_grad_in_fp32,
        weight_decay=args.weight_decay,
        adam_eps=args.adam_eps,
        adam_beta1=args.adam_beta1,
        adam_beta2=args.adam_beta2,
        lr=args.learning_rate,
    )
    model, random_states = init_model(
        config=config,
        dtype=args.dtype,
        dpg=dpg,
        training_model_args=training_model_args,
        # TODO @thomasw21: Figure out why using DDP with accumulate_in_fp_32 and ZeRO-1 performs poorly.
        make_ddp=not (optimizer_args.accumulate_grad_in_fp32 and optimizer_args.zero_stage > 0),
    )

    optimizer, grad_accumulator = init_optimizer_and_grad_accumulator(
        model=model, optimizer_args=optimizer_args, dpg=dpg
    )

    lr_scheduler_args = LRSchedulerArgs(
        lr_warmup_style=args.lr_warmup_style,
        lr_warmup_steps=args.lr_warmup_steps,
        lr_decay_style=args.lr_decay_style,
        lr_decay_steps=args.lr_decay_steps,
        min_decay_lr=args.min_decay_lr,
    )

    lr_scheduler = lr_scheduler_builder(
        optimizer=optimizer, learning_rate=optimizer_args.lr, lr_scheduler_args=lr_scheduler_args
    )

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
    micro_batch_size = args.micro_batch_size
    n_micro_batches_per_batch = args.batch_accumulation_per_replica
    global_batch_size = micro_batch_size * n_micro_batches_per_batch * dpg.dp_pg.size()
    input_sequence_length = args.encoder_sequence_length
    target_sequence_length = args.decoder_sequence_length

    # Create a dummy data loader
    if args.hf_dataset_name is None:
        data_iterator = dummy_infinite_data_generator(
            micro_batch_size=micro_batch_size,
            input_sequence_length=input_sequence_length,
            target_sequence_length=target_sequence_length,
            model=model.module,
            config=config,
            seed=args.seed,
            dpg=dpg,
        )()
    else:
        # TODO @thomasw21: We might want to do preprocessing somewhere else (ie in another script), and save the dataset
        # TODO @thomasw21: Test out dataset support of variable sized arrays.
        # TODO @thomasw21: If we change the number of process than the hash changes, figure out how I would get a persistent dataset. (see first todo)
        with main_rank_first(dpg.world_pg):
            ds = load_dataset(args.hf_dataset_name, args.hf_dataset_config_name, split=args.hf_dataset_split)
            tokenizer_model_name = model_name
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_model_name)

        shard_kwargs = {"num_shards": dpg.world_pg.size(), "contiguous": True}
        mean_noise_span_length = 5  # had to increase in order to use only 100 sentinel tokens
        process_kwargs = {
            "tokenizer": tokenizer,
            "text_column": "text",
            "input_sequence_length": input_sequence_length,
            "target_sequence_length": target_sequence_length,
            "mean_noise_span_length": mean_noise_span_length,
            "processing_num_proc": args.dataset_processing_num_proc_per_process,
        }

        # Run specific shards for each rank
        shard = ds.shard(index=dist.get_rank(dpg.world_pg), **shard_kwargs)

        mlm_process(dataset=shard, **process_kwargs)

        # Wait until every process has finished processing the shards
        dist.barrier(dpg.world_pg)

        # Now load all the shards
        # TODO @thomasw21: Is there a context, or argument that allows to be sure that we get from cache and not compute?
        ds = concatenate_datasets(
            [
                mlm_process(dataset=ds.shard(index=i, **shard_kwargs), **process_kwargs)
                for i in range(dpg.world_pg.size())
            ]
        )

        # TODO @thomasw21: We might want to suffle the entire dataset.

        # We care about loading only what necessary
        encoder_input_pp_rank = model.module.model.encoder_embedding.rank
        decoder_input_pp_rank = model.module.model.decoder_embedding.rank
        output_pp_rank = model.module.loss.rank

        dataloader = get_dataloader(
            dataset=ds,
            batch_size=micro_batch_size,
            input_length=input_sequence_length,
            target_length=target_sequence_length,
            mean_noise_span_length=mean_noise_span_length,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
            decoder_start_token_id=config.decoder_start_token_id,
            sentinel_tokens_ids=np.array(tokenizer.additional_special_tokens_ids),
            encoder_input_pp_rank=encoder_input_pp_rank,
            decoder_input_pp_rank=decoder_input_pp_rank,
            output_pp_rank=output_pp_rank,
            num_proc=args.loading_num_proc_per_process,
            seed=args.seed,
            dpg=dpg,
        )

        def to_cuda(dataloader):
            for batch in dataloader:
                micro_batch = {
                    k: v if isinstance(v, TensorPointer) else v.to("cuda", memory_format=torch.contiguous_format)
                    for k, v in batch.items()
                }

                if not args.ignore_sanity_checks:
                    # SANITY CHECK: Check input are not the same across DP
                    for key, value in sorted(micro_batch.items(), key=lambda x: x[0]):
                        if isinstance(value, TensorPointer):
                            continue

                        if "mask" in key:
                            # No need to test for mask as they would likely be the same here.
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

        data_iterator = to_cuda(dataloader)

    # Feed the model infinitely
    n_batches = 0
    with torch.inference_mode():
        for _ in range(n_batches):
            for _ in range(n_micro_batches_per_batch):
                data = next(data_iterator)
                model(**data)

    # Backward from time to time
    # TODO @thomasw21: Make a much better API
    pipeline_engine: PipelineEngine
    if args.pp_engine == "afab":
        pipeline_engine = AllForwardAllBackwardPipelineEngine()
    elif args.pp_engine == "1f1b":
        pipeline_engine = OneForwardOneBackwardPipelineEngine()
    else:
        raise ValueError(f"Got {args.pp_engine} as argument for pipeline engine.")

    log_rank(
        f"[Before the start of training] datetime: {datetime.datetime.now()}",
        logger=logger,
        level=logging.INFO,
        rank=0,
    )
    start_time = time.time()

    # Useful mapping
    normalized_model = model.module if isinstance(model, DistributedDataParallel) else model
    module_id_to_prefix = {id(module): f"{module_name}." for module_name, module in normalized_model.named_modules()}
    # Fix the root_model
    module_id_to_prefix[id(normalized_model)] = ""

    for n_iteration in range(args.num_batches):
        if not args.ignore_sanity_checks:
            # SANITY CHECK: Check that the model params are synchronized
            for name, param in sorted(model.named_parameters(), key=lambda x: x[0]):
                assert_tensor_synced_across_pg(
                    tensor=param, pg=dpg.dp_pg, msg=lambda err: f"{name} are not synchronized across DP {err}"
                )

        # SANITY CHECK: Check that the grad accumulator buffers are ready for DDP
        if not args.ignore_sanity_checks:
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

        if n_iteration == 0:
            log_rank(
                f"[After train batch iter] Memory usage: {torch.cuda.memory_allocated() / 1024**2:.2f}MB. Peak reserved memory: {torch.cuda.max_memory_reserved() / 1024**2:.2f}MB",
                logger=logger,
                level=logging.DEBUG,
                group=dpg.dp_pg,
                rank=0,
            )

        if not args.ignore_sanity_checks:
            # SANITY CHECK: Check that gradient flow on the entire model
            # SANITY CHECK: Check that all parameters that required gradients, have actually a gradient
            # SANITY CHECK: Check for nans
            # Normalize DDP
            for name, param in normalized_model.named_parameters():
                if param.is_tied:
                    tied_info = param.get_tied_info()
                    name = tied_info.get_full_name_from_module_id_to_prefix(module_id_to_prefix=module_id_to_prefix)

                if grad_accumulator is not None:
                    grad = grad_accumulator.get_grad_buffer(name=name)
                else:
                    grad = param.grad
                if torch.isnan(param).any() or torch.isinf(param).any():
                    raise ValueError("Parameter is nan or inf")
                if torch.isnan(grad).any() or torch.isinf(grad).any():
                    raise ValueError("Gradient is nan or inf")

                if not param.requires_grad:
                    continue

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
        # Apply gradient
        optimizer.step()
        # PT 2.0: will change default to None as it gains performance.
        # https://github.com/pytorch/pytorch/issues/92656
        optimizer.zero_grad(set_to_none=True)

        # Update the learning rate
        lr_scheduler.step()

        if not args.ignore_sanity_checks:
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
        n_iteration += 1
        if n_iteration % args.iteration_step_info_interval == 0:
            dist.barrier()
            # TODO @nouamanetazi: Megatron-LM seems to be using a barrier to report their interval time. Check if this is necessary. https://github.com/NouamaneTazi/Megatron-LM/blob/e241a96c3085b18e36c6cee1d68a8155de77b5a6/megatron/training.py#L607
            torch.cuda.synchronize()
            elapsed_time_per_iteration_ms = (time.time() - start_time) / args.iteration_step_info_interval * 1000
            # tokens_per_sec is calculated using target_sequence_length
            tokens_per_sec = global_batch_size * target_sequence_length / (elapsed_time_per_iteration_ms / 1000)
            model_tflops, hardware_tflops = get_flops_per_sec(
                iteration_time_in_sec=elapsed_time_per_iteration_ms / 1000,
                world_size=dpg.world_pg.size(),
                num_layers_enc=config.num_layers,
                num_layers_dec=config.num_decoder_layers,
                hidden_size=config.d_model,
                num_heads=config.num_heads,
                vocab_size=config.vocab_size,
                seq_len_enc=input_sequence_length,
                seq_len_dec=target_sequence_length,
                kv_channels=config.d_kv,
                ffn_hidden_size=config.d_ff,
                batch_size=global_batch_size,
                recompute_granularity=training_model_args.recompute_mode,
                glu_activation=config.is_gated_act,
            )
            if (
                dist.get_rank(dpg.pp_pg) == dpg.pp_pg.size() - 1
                and dist.get_rank(dpg.tp_pg) == 0
                and dist.get_rank(dpg.dp_pg) == 0
            ):
                assert not isinstance(outputs[0], TensorPointer)
                # This is an average on only one data rank.
                loss_avg_per_mbs = torch.tensor(outputs).mean().item()
                lr = lr_scheduler.get_last_lr()[0]
                log_rank(
                    f"iteration {n_iteration:8d}/{args.num_batches:8d} | consumed samples: {n_iteration * global_batch_size:12d} | elapsed time per iteration (ms): {elapsed_time_per_iteration_ms:.1f} | tokens per second: {tokens_per_sec:1.6E} | global batch size: {global_batch_size:5d} | lm loss: {loss_avg_per_mbs:1.6E} | lr: {lr:.3E} | model TFLOPs: {model_tflops:.2f} | hardware TFLOPs: {hardware_tflops:.2f}",
                    logger=logger,
                    level=logging.INFO,
                )
            start_time = time.time()

        if not args.ignore_sanity_checks:
            # SANITY CHECK: Check that the model params are synchronized
            for name, param in sorted(model.named_parameters(), key=lambda x: x[0]):
                assert_tensor_synced_across_pg(
                    tensor=param, pg=dpg.dp_pg, msg=lambda err: f"{name} is not synced across DP. {err}"
                )

            # SANITY CHECK: Tied weights are synchronized
            for (name, group_ranks), param in sorted(
                get_tied_id_to_param(
                    parameters=model.parameters(),
                    root_module=normalized_model,
                ).items(),
                key=lambda x: x[0],
            ):
                if not (isinstance(param, BRRRParameter) and param.is_tied):
                    continue

                group = dpg.world_ranks_to_pg[group_ranks]
                # Parameter is duplicated across TP let's make sure it's the same
                assert_tensor_synced_across_pg(
                    tensor=param,
                    pg=group,
                    msg=lambda err: f"Tied weights {name} are not synchronized. {err}",
                )

    # Test saving
    checkpoint_path = args.checkpoint_path
    if check_path_is_local(checkpoint_path):
        if dist.get_rank(dpg.world_pg) == 0:
            checkpoint_path.mkdir()
        dist.barrier(dpg.world_pg)
    log_rank("Saving", logger=logger, level=logging.INFO, rank=0)
    save(model=model, optimizer=optimizer, lr_scheduler=lr_scheduler, dpg=dpg, root_folder=checkpoint_path)
    save_random_states(random_states=random_states, dpg=dpg, root_folder=checkpoint_path)

    # Wait til everything is saved to begin loading
    dist.barrier()

    # Test that saved checkpoint has save everything correctly.
    # NOTE: it's important to have same zero stage to be able to compare the optimizer state dict
    new_model, new_random_states = init_model(
        config=config,
        dtype=args.dtype,
        dpg=dpg,
        # We load the model without passing a training args since we don't actually compare any training dynamics.
        training_model_args=None,
        # TODO @thomasw21: Figure out why using DDP with accumulate_in_fp_32 and ZeRO-1 performs poorly.
        make_ddp=not (optimizer_args.accumulate_grad_in_fp32 and optimizer_args.zero_stage > 0),
    )
    new_optimizer, new_grad_accumulator = init_optimizer_and_grad_accumulator(
        model=new_model, optimizer_args=optimizer_args, dpg=dpg
    )
    new_lr_scheduler = lr_scheduler_builder(
        optimizer=new_optimizer, learning_rate=optimizer_args.lr, lr_scheduler_args=lr_scheduler_args
    )
    load(
        model=new_model,
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

    # Check that we can generate with that same model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    dummy_inputs = ["Hello my name is <extra_id_0>", "My dog is the sweetest thing. Please <extra_id_0> care of it."]
    assert config.decoder_start_token_id is not None
    outputs = greedy_search(
        input_iter=(GenerationInput(text=text) for text in dummy_inputs),
        tokenizer=tokenizer,
        # TODO @thomasw21: From DDP extract the underlying model
        model=model.module.model,
        decoder_start_token_id=config.decoder_start_token_id,
        # TODO @thomasw21: Figure out how to pass p2p.
        p2p=model.module.model.p2p,
        generation_config=GenerationConfig(max_new_tokens=20),
        max_micro_batch_size=16,
        dpg=dpg,
    )
    for output in outputs:
        input_ids = output.input_ids
        generated_ids = output.generation_ids
        if isinstance(input_ids, TensorPointer):
            assert isinstance(generated_ids, TensorPointer)
            continue
        assert isinstance(generated_ids, torch.Tensor)
        print(
            {
                "input": tokenizer.decode(input_ids, clean_up_tokenization_spaces=False),
                "generation": tokenizer.decode(generated_ids, clean_up_tokenization_spaces=False),
            }
        )


if __name__ == "__main__":
    main()
