import argparse
import logging as lg
import math
import os
import sys
from math import ceil
from pprint import pformat
from typing import Dict, List, Optional, Tuple

import torch
from datasets.download.streaming_download_manager import xPath
from torch import nn
from torch.nn.parallel import DistributedDataParallel
from torch.optim import AdamW
from torch.optim.lr_scheduler import LambdaLR
from transformers import GPTBigCodeConfig, LlamaConfig

from brrr.config import (
    Config,
    LRSchedulerArgs,
    OptimizerArgs,
    ParallelismArgs,
)
from brrr.core import distributed as dist
from brrr.core import logging
from brrr.core.dataclass import RandomStates
from brrr.core.distributed import ProcessGroup
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
from brrr.core.parallelism.tensor_parallelism.nn import (
    TensorParallelLinearMode,
)
from brrr.core.process_groups_initializer import DistributedProcessGroups
from brrr.core.random import (
    get_current_random_state,
    get_synced_random_state,
)
from brrr.core.serialize import (
    save,
    save_random_states,
)
from brrr.core.serialize.path import check_path_is_local
from brrr.core.serialize.serialize import fs_open
from brrr.models.gpt2 import GPTForTraining
from brrr.models.llama import LlamaForTraining

logger = logging.get_logger(__name__)

try:

    tb_logger_available = True
except ImportError:
    tb_logger_available = False

try:

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
if os.environ.get("USE_FAST"):
    # We import the fast versions
    pass
else:
    pass


CONFIG_TO_MODEL_CLASS = {
    LlamaConfig: LlamaForTraining,
    GPTBigCodeConfig: GPTForTraining,
}


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


def init_random_states(parallel_config: ParallelismArgs, tp_pg: ProcessGroup):
    # Get synchronized random states
    if parallel_config is None or parallel_config.tp_mode is TensorParallelLinearMode.ALL_REDUCE:
        random_states = RandomStates(
            {"tp_synced": get_synced_random_state(random_state=get_current_random_state(), pg=tp_pg)}
        )
    else:
        # We don't need to sync across TP when using sequence parallel (REDUCE_SCATTER)
        random_states = RandomStates({})
    return random_states


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
                fused=optimizer_args.torch_adam_is_fused,
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
        if (
            len(optimizer.zero_named_param_groups) > 0
            and len(optimizer.zero_named_param_groups[0]["named_params"]) > 0
        ):
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
    model_config: LlamaConfig,
    config: Config,
    iteration_step: int,
    consumed_train_samples: int,
    checkpoints_path: xPath,
    dpg: DistributedProcessGroups,
) -> xPath:
    checkpoint_path = checkpoints_path / f"{iteration_step}"
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
    with fs_open(checkpoints_path / "latest.txt", mode="w") as fo:
        fo.write(f"{iteration_step}")
    with fs_open(checkpoint_path / "config.txt", mode="w") as fo:
        # TODO @nouamane: save as yaml
        fo.write(pformat(config))
    model_config.to_json_file(checkpoint_path / "model_config.json")
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
