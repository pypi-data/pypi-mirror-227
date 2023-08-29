import contextlib
import datetime
import os
import sys
import time
from pprint import pformat

import torch
from config import (
    ExistingCheckpointInit,
    HubLoggerConfig,
    PretrainDatasetsArgs,
    RewardArgs,
    TensorboardLoggerConfig,
    get_args_from_path,
)
from dataloader import reward_data_generator, to_cuda
from datasets.download.streaming_download_manager import xPath
from flops import get_flops_per_sec
from modeling_reward import RewardForTraining
from torch import nn
from torch.nn.parallel import DistributedDataParallel
from torch.profiler import ProfilerActivity, profile, tensorboard_trace_handler
from train import (
    _vocab_size_with_padding,
    get_args,
    init_model,
    init_optimizer_and_grad_accumulator,
    init_random_states,
    lr_scheduler_builder,
    save_checkpoint,
    set_logger_verbosity,
    test_equal_dict,
)
from transformers import AutoTokenizer, LlamaConfig

from brrr.clip_grads import clip_grad_norm
from brrr.core import distributed as dist
from brrr.core import logging
from brrr.core.logging import (
    log_rank,
)
from brrr.core.optimizer.zero import ZeroDistributedOptimizer
from brrr.core.parallelism.pipeline_parallelism.block import PipelineBlock
from brrr.core.parallelism.pipeline_parallelism.engine import (
    PipelineEngine,
)
from brrr.core.parallelism.tied_parameters import (
    get_tied_id_to_param,
)
from brrr.core.process_groups_initializer import get_process_groups
from brrr.core.random import (
    set_random_seed,
)
from brrr.core.serialize import (
    load,
    load_lr_scheduler,
    load_meta,
    load_optimizer,
    load_weights,
)
from brrr.core.serialize.serialize import fs_open
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


if os.environ.get("USE_FAST"):
    # We import the fast versions
    raise NotImplementedError("Masked inputs not supported yet when using `USE_FAST=1`")
    from modeling_llama_fast import LlamaDecoderLayer
else:
    from modeling_llama import LlamaDecoderLayer

"""
Example on how to use `brrr` to build a gpt model
"""


def main():
    config_file = get_args().config_file
    config = get_args_from_path(config_file)

    assert isinstance(
        config.reward, RewardArgs
    ), f"`config.reward` must be defined in {config_file} if you want to run Reward training"

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

    # Choosing checkpoint path
    load_from_candidate = config.checkpoints.load_from_specific_checkpoint
    if load_from_candidate is None:
        latest_meta_path: xPath = config.checkpoints.checkpoints_path / "latest.txt"
        if latest_meta_path.exists():
            with fs_open(config.checkpoints.checkpoints_path / "latest.txt", mode="r") as fi:
                # TODO @thomasw21: make a better structure system so that we get typing correct
                load_from_candidate = int(fi.read())
    checkpoint_path = (
        config.checkpoints.checkpoints_path / str(load_from_candidate) if load_from_candidate is not None else None
    )
    if checkpoint_path is not None:
        log_rank(
            f"Loading checkpoint from {checkpoint_path}:",
            logger=logger,
            level=logging.INFO,
            rank=0,
        )

    # Init model config
    model_name = config.model.hf_llama_model_name
    model_config: LlamaConfig = LlamaConfig.from_pretrained(model_name)
    model_config.vocab_size = _vocab_size_with_padding(
        model_config.vocab_size,
        pg_size=dpg.tp_pg.size(),
        make_vocab_size_divisible_by=config.model.make_vocab_size_divisible_by,
    )
    assert (
        model_config.max_position_embeddings >= config.tokens.sequence_length
    ), f"max_position_embeddings ({model_config.max_position_embeddings}) must be >= sequence_length ({config.tokens.sequence_length})"

    log_rank(pformat(config), logger=logger, level=logging.INFO, rank=0)
    log_rank(str(model_config), logger=logger, level=logging.INFO, rank=0)

    optimizer_args = config.optimizer

    random_states = init_random_states(parallel_config=config.parallelism, tp_pg=dpg.tp_pg)

    # Initialize model
    model = init_model(
        model_builder=lambda: RewardForTraining(
            config=model_config,
            dpg=dpg,
            parallel_config=config.parallelism,
        ),
        model_config=model_config,
        parallel_config=config.parallelism,
        dtype=config.model.dtype,
        dpg=dpg,
        # TODO @thomasw21: Figure out why using DDP with accumulate_in_fp_32 and ZeRO-1 performs poorly.
        make_ddp=not (optimizer_args.accumulate_grad_in_fp32 and optimizer_args.zero_stage > 0),
    )

    # freeze all params in `model` besides last `num_layers_unfrozen` layers
    def freeze_bottom_causal_layers(model: nn.Module, num_layers_unfrozen: int = 0):
        """Freezes the bottom transformer block layers of the specified model."""
        hidden_layers = tuple(layer for layer in model.modules() if isinstance(layer, LlamaDecoderLayer))
        if num_layers_unfrozen == 0:
            hidden_layers_to_freeze = list(hidden_layers)
        elif num_layers_unfrozen > 0:
            hidden_layers_to_freeze = list(hidden_layers)[:-num_layers_unfrozen]
        else:
            hidden_layers_to_freeze = []
        for layer in hidden_layers_to_freeze:
            layer.requires_grad_(False)

    freeze_bottom_causal_layers(model, num_layers_unfrozen=config.reward.num_layers_unfrozen)

    # Load model from checkpoint or initialize from a pretrained model
    if checkpoint_path is not None:
        # Load model from checkpoint path
        load_weights(model=model, dpg=dpg, root_folder=checkpoint_path)
    else:
        # We initialize the model.
        if isinstance(config.model.init_method, ExistingCheckpointInit):
            # Initialize model from an existing model checkpoint
            ignored_param_names = []
            load_weights(
                model=model,
                dpg=dpg,
                root_folder=config.model.init_method.path,
                filtered_state_dict={
                    name: param
                    for name, param in model.state_dict().items()
                    if not any(ignored_param_name in name for ignored_param_name in ignored_param_names)
                },
            )

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
            raise ValueError(f"Unsupported init_method '{config.model.init_method}' for Reward training")

    # Init optimizer
    optimizer, grad_accumulator = init_optimizer_and_grad_accumulator(
        model=model, optimizer_args=optimizer_args, dpg=dpg
    )
    if checkpoint_path is not None:
        load_optimizer(optimizer=optimizer, dpg=dpg, root_folder=checkpoint_path)

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
    consumed_new_train_samples: int
    if checkpoint_path is not None:
        checkpoint_metadata = load_meta(dpg=dpg, root_folder=checkpoint_path)
        log_rank(
            f"Loaded checkpoint metadata from {checkpoint_path}: \n{str(checkpoint_metadata)}",
            logger=logger,
            level=logging.INFO,
            rank=0,
        )
        start_iteration_step = checkpoint_metadata.metas["last_train_step"]
        consumed_new_train_samples = checkpoint_metadata.metas["consumed_train_samples"]
        assert (
            config.tokens.train_steps > start_iteration_step
        ), f"Loaded checkpoint has already trained {start_iteration_step} batches, you need to specify a higher `config.tokens.train_steps`"
    else:
        start_iteration_step = 0
        consumed_new_train_samples = 0
    consumed_train_samples = (
        consumed_new_train_samples * 2
    )  # Each dataset sample corresponds to two training samples (chosen/rejected)

    # Setup all writers
    if (
        dist.get_rank(dpg.pp_pg) in [model.loss.rank]
        and dist.get_rank(dpg.tp_pg) == 0
        and dist.get_rank(dpg.dp_pg) == 0
    ):
        if config.logging.tensorboard_logger is None:
            tb_context = contextlib.nullcontext()
        elif isinstance(config.logging.tensorboard_logger, HubLoggerConfig):
            current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            logdir = str(config.logging.tensorboard_logger.tensorboard_dir / f"{config.general.name}_{current_time}")
            assert (
                hub_logger_available
            ), 'Hub Tensorboard Logger is not available. Please install brrr with `pip install -e ".[hf-logger]"` or modify your config file'
            tb_context = HubSummaryWriter(
                logdir=logdir,
                repo_id=config.logging.tensorboard_logger.repo_id,
                path_in_repo=f"tensorboard/{config.general.name}_{current_time}",
            )
        elif isinstance(config.logging.tensorboard_logger, TensorboardLoggerConfig):
            current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            logdir = str(config.logging.tensorboard_logger.tensorboard_dir / f"{config.general.name}_{current_time}")
            assert (
                tb_logger_available
            ), 'Tensorboard Logger is not available. Please install brrr with `pip install -e ".[tb-logger]"` or modify your config file'
            tb_context = BatchSummaryWriter(
                logdir=logdir,
                flush_secs=config.logging.tensorboard_logger.flush_secs,
            )
        else:
            raise ValueError(f"Unsupported tensorboard logger type: {type(config.logging.tensorboard_logger)}")
        loggerwriter = LoggerWriter(global_step=config.tokens.train_steps)
    else:
        tb_context = contextlib.nullcontext()

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

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"

    if isinstance(config.data.dataset, PretrainDatasetsArgs):
        log_rank("Using `datasets` library", logger=logger, level=logging.INFO, rank=0)

        data_iterator = reward_data_generator(
            dpg=dpg,
            model=model,
            tokenizer=tokenizer,
            sequence_length=sequence_length,
            micro_batch_size=config.tokens.micro_batch_size,
            dataset_mixer=config.data.dataset.hf_dataset_mixer,
            dataset_config_name=config.data.dataset.hf_dataset_config_name,
            dataset_splits=config.data.dataset.hf_dataset_splits,
            dataset_processing_num_proc_per_process=config.data.dataset.dataset_processing_num_proc_per_process,
        )()
        data_iterator = to_cuda(dataloader=data_iterator, dpg=dpg, config=config)
    else:
        raise ValueError(f"Unhandled case of `config.data.dataset`. Got: {config.data.dataset}")

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
            schedule=torch.profiler.schedule(wait=1, warmup=1, active=3, repeat=1, skip_first=1),
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
            for iteration_step in range(start_iteration_step + 1, config.tokens.train_steps + 1):
                if isinstance(prof, torch.profiler.profile):
                    prof.step()
                start_time = time.time()

                if iteration_step < 5:
                    log_rank(
                        f"[Before train batch iter] Memory usage: {torch.cuda.memory_allocated() / 1024**2:.2f}MB. Peak reserved memory: {torch.cuda.max_memory_reserved() / 1024**2:.2f}MB",
                        logger=logger,
                        level=logging.INFO,
                        group=dpg.dp_pg,
                        rank=0,
                    )

                outputs = pipeline_engine.train_batch_iter(
                    model=model,
                    pg=dpg.pp_pg,
                    batch=(next(data_iterator) for _ in range(n_micro_batches_per_batch)),
                    grad_accumulator=grad_accumulator,
                )

                if iteration_step < 5:
                    log_rank(
                        f"[After train batch iter] Memory usage: {torch.cuda.memory_allocated() / 1024**2:.2f}MB. Peak reserved memory: {torch.cuda.max_memory_reserved() / 1024**2:.2f}MB",
                        logger=logger,
                        level=logging.INFO,
                        group=dpg.dp_pg,
                        rank=0,
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
                        if param.requires_grad
                    ]
                    # TODO @nouamane: we need to split `world_rank_matrix` along PP axis, to separate ref from active model
                    grad_norm_unclipped = clip_grad_norm(
                        mp_pg=dpg.world_ranks_to_pg[
                            tuple(sorted(dpg.world_rank_matrix[:, dist.get_rank(dpg.dp_pg), :].reshape(-1)))
                        ],
                        named_parameters=named_parameters,
                        grad_accumulator=grad_accumulator,
                        max_norm=config.optimizer.clip_grad,
                    )

                # Apply gradient
                optimizer.step()
                # PT 2.0: will change default to None as it gains performance.
                # https://github.com/pytorch/pytorch/issues/92656
                optimizer.zero_grad(set_to_none=True)

                # Update the learning rate
                lr_scheduler.step()

                # Training Logs
                consumed_train_samples += global_batch_size
                consumed_new_train_samples += (
                    global_batch_size // 2
                )  # chosen and rejected samples accounts for 1 sample

                if iteration_step % config.logging.iteration_step_info_interval == 0:
                    # TODO @nouamanetazi: Megatron-LM seems to be using a barrier to report their interval time. Check if this is necessary. https://github.com/NouamaneTazi/Megatron-LM/blob/e241a96c3085b18e36c6cee1d68a8155de77b5a6/megatron/training.py#L607
                    dist.barrier()
                    torch.cuda.synchronize()
                    elapsed_time_per_iteration_ms = (time.time() - start_time) * 1000
                    tokens_per_sec = (
                        global_batch_size * sequence_length / (elapsed_time_per_iteration_ms / 1000)
                    )  # tokens_per_sec is calculated using sequence_length
                    model_tflops, hardware_tflops = get_flops_per_sec(
                        iteration_time_in_sec=elapsed_time_per_iteration_ms / 1000,
                        world_size=dpg.world_pg.size(),
                        num_layers=model_config.num_hidden_layers,
                        hidden_size=model_config.hidden_size,
                        num_heads=model_config.num_attention_heads,
                        vocab_size=model_config.vocab_size,
                        ffn_hidden_size=model_config.intermediate_size,
                        seq_len=sequence_length,  # TODO @nouamane: how to get sequence length used in training?
                        batch_size=global_batch_size,
                        recompute_granularity=config.parallelism.recompute_granularity,
                    )
                    if (
                        dist.get_rank(dpg.pp_pg) == model.loss.rank
                        and dist.get_rank(dpg.tp_pg) == 0
                        and dist.get_rank(dpg.dp_pg) == 0
                    ):
                        # This is an average on only one data rank.
                        loss_avg_per_mbs = torch.tensor([output["loss"] for output in outputs]).mean().item()

                        lr = lr_scheduler.get_last_lr()[0]

                        log_entries = [
                            LogItem("consumed_samples", consumed_train_samples, "7d"),
                            LogItem("elapsed_time_per_iteration_ms", elapsed_time_per_iteration_ms, ".1f"),
                            LogItem("tokens_per_sec", tokens_per_sec, "1.6E"),
                            LogItem("tokens_per_sec_per_gpu", tokens_per_sec / dpg.world_pg.size(), "1.6E"),
                            LogItem("global_batch_size", global_batch_size, "5d"),
                            LogItem("reward_loss", loss_avg_per_mbs, "1.6E"),
                            LogItem("lr", lr, ".3E"),
                            # LogItem("model_tflops_per_gpu", model_tflops, ".2f"),
                            # LogItem("hardware_tflops_per_gpu", hardware_tflops, ".2f"),
                        ]
                        if grad_norm_unclipped is not None:
                            log_entries.append(LogItem("grad_norm", grad_norm_unclipped, ".3f"))
                        loggerwriter.add_scalars_from_list(log_entries, iteration_step)

                        if tb_writer is not None:
                            # This is an average on only one data rank.
                            log_entries.extend(
                                [
                                    LogItem(
                                        "logits/rejected",
                                        torch.tensor([output["logits/rejected"] for output in outputs]).mean().item(),
                                        "1.6E",
                                    ),
                                    LogItem(
                                        "logits/chosen",
                                        torch.tensor([output["logits/chosen"] for output in outputs]).mean().item(),
                                        "1.6E",
                                    ),
                                ]
                            )
                            tb_writer.add_scalars_from_list(log_entries, iteration_step)

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
                        model_config=model_config,
                        config=config,
                        iteration_step=iteration_step,
                        consumed_train_samples=consumed_new_train_samples,
                        checkpoints_path=config.checkpoints.checkpoints_path,
                        dpg=dpg,
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
                        model_config=model_config,
                        config=config,
                        iteration_step=iteration_step,
                        consumed_train_samples=consumed_new_train_samples,
                        checkpoints_path=config.checkpoints.checkpoints_path,
                        dpg=dpg,
                    )

                # Push to Hub
                if (
                    isinstance(config.logging.tensorboard_logger, HubLoggerConfig)
                    and isinstance(tb_writer, HubSummaryWriter)
                    and iteration_step % config.logging.tensorboard_logger.push_to_hub_interval == 0
                ):
                    # tb_writer only exists on a single rank
                    log_rank(
                        f"Push Tensorboard logging to Hub at iteration {iteration_step}",
                        logger=logger,
                        level=logging.INFO,
                    )
                    # it is a future that queues to avoid concurrent push
                    tb_writer.scheduler.trigger()

    if isinstance(prof, profile):
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
        model_config=model_config,
        config=config,
        iteration_step=config.tokens.train_steps,
        consumed_train_samples=consumed_new_train_samples,
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
    new_model = init_model(
        model_builder=lambda: RewardForTraining(
            config=model_config,
            dpg=dpg,
            parallel_config=config.parallelism,
        ),
        model_config=model_config,
        parallel_config=config.parallelism,
        dtype=config.model.dtype,
        dpg=dpg,
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

    # Check that it converges.

    # Check TFLOPS


if __name__ == "__main__":
    main()
