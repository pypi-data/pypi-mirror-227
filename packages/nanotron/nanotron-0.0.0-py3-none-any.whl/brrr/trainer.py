import contextlib
import datetime
import sys
import time
from pprint import pformat
from typing import List, Optional

import numpy as np
import torch
from torch.nn.parallel import DistributedDataParallel
from torch.profiler import ProfilerActivity, profile, tensorboard_trace_handler
from transformers import AutoConfig, AutoTokenizer

from brrr.clip_grads import clip_grad_norm
from brrr.config import (
    Config,
    ExistingCheckpointInit,
    HubLoggerConfig,
    RandomInit,
    TensorboardLoggerConfig,
    get_args_from_path,
)
from brrr.core import distributed as dist
from brrr.core import logging
from brrr.core.dataclass import RandomStates
from brrr.core.logging import log_rank
from brrr.core.optimizer.zero import ZeroDistributedOptimizer
from brrr.core.parallelism.parameters import BRRRParameter, sanity_check
from brrr.core.parallelism.pipeline_parallelism.block import PipelineBlock
from brrr.core.parallelism.pipeline_parallelism.engine import (
    PipelineEngine,
)
from brrr.core.parallelism.tensor_parallelism.nn import (
    TensorParallelLinearMode,
    TensorParallelRowLinear,
)
from brrr.core.parallelism.tied_parameters import (
    create_pg_for_tied_weights,
    tie_parameters,
)
from brrr.core.process_groups_initializer import DistributedProcessGroups, get_process_groups
from brrr.core.random import (
    set_random_seed,
)
from brrr.core.serialize import (
    load_lr_scheduler,
    load_meta,
    load_optimizer,
    load_weights,
)
from brrr.core.serialize.path import parse_ckpt_path
from brrr.core.tensor_init import init_method_normal, scaled_init_method_normal
from brrr.core.utils import (
    init_on_device_and_dtype,
)
from brrr.dataloader import (
    dummy_infinite_data_generator,
)
from brrr.helpers import (
    CONFIG_TO_MODEL_CLASS,
    _vocab_size_with_padding,
    init_optimizer_and_grad_accumulator,
    init_random_states,
    lr_scheduler_builder,
    save_checkpoint,
    set_logger_verbosity,
)
from brrr.logger import LoggerWriter, LogItem
from brrr.models.gpt2 import GPTForTraining
from brrr.models.llama import RotaryEmbedding

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


# TODO @nouamane: add abstract class
class DistributedTrainer:
    def __init__(self, config: Config):
        super().__init__()
        self.config = config

        # Initialise all process groups
        self.dpg = get_process_groups(
            data_parallel_size=self.config.parallelism.dp,
            pipeline_parallel_size=self.config.parallelism.pp,
            tensor_parallel_size=self.config.parallelism.tp,
        )

        # Set random states
        set_random_seed(self.config.model.seed)

        # Set log levels
        if dist.get_rank(self.dpg.world_pg) == 0:
            if self.config.logging.log_level is not None:
                set_logger_verbosity(self.config.logging.log_level, dpg=self.dpg)
        else:
            if self.config.logging.log_level_replica is not None:
                set_logger_verbosity(self.config.logging.log_level_replica, dpg=self.dpg)

        # Parsing checkpoint path
        checkpoint_path = parse_ckpt_path(config=self.config)

        # Init model and build on pp ranks
        self.random_states = init_random_states(parallel_config=self.config.parallelism, tp_pg=self.dpg.tp_pg)
        self.model_config, self.model = self.init_model(config=self.config, dpg=self.dpg)

        # Load or initialize model weights
        if checkpoint_path is not None:
            # Load from checkpoint
            load_weights(model=self.model, dpg=self.dpg, root_folder=checkpoint_path)
        else:
            # We initialize the model.
            if isinstance(self.config.model.init_method, ExistingCheckpointInit):
                # Initialize model from an existing model checkpoint
                load_weights(model=self.model, dpg=self.dpg, root_folder=self.config.model.init_method.path)
            elif isinstance(self.config.model.init_method, RandomInit):
                # Initialize model randomly
                self.model.init_model_randomly(
                    init_method=init_method_normal(self.config.model.init_method.std),
                    scaled_init_method=scaled_init_method_normal(
                        self.config.model.init_method.std, self.model_config.num_hidden_layers
                    ),
                )
            else:
                raise ValueError(f"Unsupported {self.config.model.init_method}")

        # Init optimizer
        self.optimizer, self.grad_accumulator = init_optimizer_and_grad_accumulator(
            model=self.model, optimizer_args=self.config.optimizer, dpg=self.dpg
        )
        if checkpoint_path is not None:
            load_optimizer(optimizer=self.optimizer, dpg=self.dpg, root_folder=checkpoint_path)

        # Init learning rate scheduler
        self.lr_scheduler = lr_scheduler_builder(
            optimizer=self.optimizer,
            learning_rate=self.config.optimizer.learning_rate,
            lr_scheduler_args=self.config.learning_rate_scheduler,
        )
        if checkpoint_path is not None:
            load_lr_scheduler(
                lr_scheduler=self.lr_scheduler,
                dpg=self.dpg,
                root_folder=checkpoint_path,
                is_zero=self.optimizer.inherit_from(ZeroDistributedOptimizer),
            )

        # Define iteration start state
        self.start_iteration_step: int
        self.consumed_train_samples: int
        if checkpoint_path is not None:
            checkpoint_metadata = load_meta(dpg=self.dpg, root_folder=checkpoint_path)
            log_rank(str(checkpoint_metadata), logger=logger, level=logging.INFO, rank=0)
            self.start_iteration_step = checkpoint_metadata.metas["last_train_step"]
            self.consumed_train_samples = checkpoint_metadata.metas["consumed_train_samples"]
            assert (
                self.config.tokens.train_steps > self.start_iteration_step
            ), f"Loaded checkpoint has already trained {self.start_iteration_step} batches, you need to specify a higher `config.tokens.train_steps`"
        else:
            self.start_iteration_step = 0
            self.consumed_train_samples = 0

        # Setup all writers
        if (
            dist.get_rank(self.dpg.pp_pg) in [self.model.loss.rank]
            and dist.get_rank(self.dpg.tp_pg) == 0
            and dist.get_rank(self.dpg.dp_pg) == 0
        ):
            self.tb_context, self.loggerwriter = self.setup_log_writers(config=self.config)
        else:
            self.tb_context = contextlib.nullcontext()

        # Log where each module is instantiated
        for name, module in self.model.named_modules():
            if not isinstance(module, PipelineBlock):
                continue
            log_rank(
                f"module_name: {name} | PP: {module.rank}/{self.dpg.pp_pg.size()}",
                logger=logger,
                level=logging.DEBUG,
                group=self.dpg.world_pg,
                rank=0,
            )

        dist.barrier()
        log_rank(
            f"Global rank: { dist.get_rank(self.dpg.world_pg)}/{self.dpg.world_pg.size()} | PP: {dist.get_rank(self.dpg.pp_pg)}/{self.dpg.pp_pg.size()} | DP: {dist.get_rank(self.dpg.dp_pg)}/{self.dpg.dp_pg.size()} | TP: {dist.get_rank(self.dpg.tp_pg)}/{self.dpg.tp_pg.size()}",
            logger=logger,
            level=logging.INFO,
        )
        dist.barrier()

        # Dummy hyper parameter
        self.micro_batch_size = self.config.tokens.micro_batch_size
        self.n_micro_batches_per_batch = self.config.tokens.batch_accumulation_per_replica
        self.global_batch_size = self.micro_batch_size * self.n_micro_batches_per_batch * self.dpg.dp_pg.size()
        self.sequence_length = self.config.tokens.sequence_length

        tokenizer = AutoTokenizer.from_pretrained(self.config.model.hf_model_name)
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "left"

        # Prepare data_iterator
        if isinstance(self.model, DistributedDataParallel):
            input_pp_rank = self.model.module.model.token_position_embeddings.rank
            output_pp_rank = self.model.module.loss.rank
        else:
            input_pp_rank = self.model.model.token_position_embeddings.rank
            output_pp_rank = self.model.loss.rank

        if self.config.data.dataset is None:
            log_rank("Using dummy data generator", logger=logger, level=logging.INFO, rank=0)
            self.data_iterator = dummy_infinite_data_generator(
                micro_batch_size=self.micro_batch_size,
                sequence_length=self.sequence_length,
                input_pp_rank=input_pp_rank,
                output_pp_rank=output_pp_rank,
                vocab_size=self.model_config.vocab_size,
                seed=self.config.data.seed,
                dpg=self.dpg,
            )()
        else:
            raise ValueError(f"Unhandled case of `self.config.data.dataset`. Got: {self.config.data.dataset}")

        self.pipeline_engine: PipelineEngine = self.config.parallelism.pp_engine

        log_rank(
            f"[Before the start of training] datetime: {datetime.datetime.now()}",
            logger=logger,
            level=logging.INFO,
            rank=0,
        )
        time.time()

        def get_profiler(config: Config):
            if self.config.profile is not None:
                if self.config.profile.profiler_export_path is not None:
                    on_trace_ready = tensorboard_trace_handler(self.config.profile.profiler_export_path)
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
            return prof

        self.prof = get_profiler(config=self.config)

        # Kill switch
        if self.config.general.kill_switch_path.exists():
            log_rank(
                f"Detected kill switch at {self.config.general.kill_switch_path}. Exiting",
                logger=logger,
                level=logging.INFO,
                rank=0,
            )
            sys.exit(0)

        # Useful mapping
        self.normalized_model = self.model.module if isinstance(self.model, DistributedDataParallel) else self.model
        self.module_id_to_prefix = {
            id(module): f"{module_name}." for module_name, module in self.normalized_model.named_modules()
        }
        # Fix the root_model
        self.module_id_to_prefix[id(self.normalized_model)] = ""

    @classmethod
    def from_config_file(cls, config_file: str):
        config = get_args_from_path(config_file)
        return cls(config=config)

    def train(self):
        with self.tb_context as tb_writer:
            with self.prof:
                for self.iteration_step in range(self.start_iteration_step + 1, self.config.tokens.train_steps + 1):
                    if isinstance(self.prof, torch.profiler.profile):
                        self.prof.step()
                    start_time = time.time()

                    # Training step
                    outputs, grad_norm_unclipped = self.training_step()

                    # Training Logs
                    self.consumed_train_samples += self.global_batch_size
                    self.consumed_train_samples += (
                        self.global_batch_size // 2
                    )  # chosen and rejected samples accounts for 1 sample

                    if self.iteration_step % self.config.logging.iteration_step_info_interval == 0:
                        # TODO @nouamanetazi: Megatron-LM seems to be using a barrier to report their interval time. Check if this is necessary. https://github.com/NouamaneTazi/Megatron-LM/blob/e241a96c3085b18e36c6cee1d68a8155de77b5a6/megatron/training.py#L607
                        dist.barrier()
                        torch.cuda.synchronize()
                        elapsed_time_per_iteration_ms = (time.time() - start_time) * 1000
                        tokens_per_sec = (
                            self.global_batch_size * self.sequence_length / (elapsed_time_per_iteration_ms / 1000)
                        )  # tokens_per_sec is calculated using sequence_length
                        model_tflops, hardware_tflops = self.model.get_flops_per_sec(
                            iteration_time_in_sec=elapsed_time_per_iteration_ms / 1000,
                            sequence_length=self.sequence_length,
                            global_batch_size=self.global_batch_size,
                        )
                        if (
                            dist.get_rank(self.dpg.pp_pg) == self.model.loss.rank
                            and dist.get_rank(self.dpg.tp_pg) == 0
                            and dist.get_rank(self.dpg.dp_pg) == 0
                        ):
                            # This is an average on only one data rank.
                            loss_avg_per_mbs = torch.tensor([output["loss"] for output in outputs]).mean().item()

                            lr = self.lr_scheduler.get_last_lr()[0]

                            log_entries = [
                                LogItem("consumed_samples", self.iteration_step * self.global_batch_size, "12d"),
                                LogItem("elapsed_time_per_iteration_ms", elapsed_time_per_iteration_ms, ".1f"),
                                LogItem("tokens_per_sec", tokens_per_sec, "1.6E"),
                                LogItem("tokens_per_sec_per_gpu", tokens_per_sec / self.dpg.world_pg.size(), "1.6E"),
                                LogItem("global_batch_size", self.global_batch_size, "5d"),
                                LogItem("lm_loss", loss_avg_per_mbs, "1.6E"),
                                LogItem("lr", lr, ".3E"),
                                LogItem("model_tflops_per_gpu", model_tflops, ".2f"),
                                LogItem("hardware_tflops_per_gpu", hardware_tflops, ".2f"),
                            ]

                            if grad_norm_unclipped is not None:
                                log_entries.append(LogItem("grad_norm", grad_norm_unclipped.item(), ".3f"))

                            if tb_writer is not None:
                                tb_writer.add_scalars_from_list(log_entries, self.iteration_step)
                            self.loggerwriter.add_scalars_from_list(log_entries, self.iteration_step)

                    # Kill switch
                    if self.config.general.kill_switch_path.exists():
                        log_rank(
                            f"Detected kill switch at {self.config.general.kill_switch_path}. Exiting",
                            logger=logger,
                            level=logging.INFO,
                            rank=0,
                        )

                        # Save checkpoint
                        save_checkpoint(
                            model=self.model,
                            optimizer=self.optimizer,
                            lr_scheduler=self.lr_scheduler,
                            random_states=self.random_states,
                            model_config=self.model_config,
                            config=self.config,
                            iteration_step=self.iteration_step,
                            consumed_train_samples=self.consumed_train_samples,
                            checkpoints_path=self.config.checkpoints.checkpoints_path,
                            dpg=self.dpg,
                        )

                        # TODO @thomasw21: Do I need to return a barrier in order to be sure everyone saved before exiting.
                        sys.exit(0)

                    # Checkpoint
                    if self.iteration_step % self.config.checkpoints.checkpoint_interval == 0:
                        save_checkpoint(
                            model=self.normalized_model,
                            optimizer=self.optimizer,
                            lr_scheduler=self.lr_scheduler,
                            random_states=self.random_states,
                            model_config=self.model_config,
                            config=self.config,
                            iteration_step=self.iteration_step,
                            consumed_train_samples=self.consumed_train_samples,
                            checkpoints_path=self.config.checkpoints.checkpoints_path,
                            dpg=self.dpg,
                        )

                    # Push to Hub
                    if (
                        isinstance(self.config.logging.tensorboard_logger, HubLoggerConfig)
                        and isinstance(tb_writer, HubSummaryWriter)
                        and self.iteration_step % self.config.logging.tensorboard_logger.push_to_hub_interval == 0
                    ):
                        # tb_writer only exists on a single rank
                        log_rank(
                            f"Push Tensorboard logging to Hub at iteration {self.iteration_step}",
                            logger=logger,
                            level=logging.INFO,
                        )
                        # it is a future that queues to avoid concurrent push
                        tb_writer.scheduler.trigger()

    def training_step(self):
        if self.iteration_step < 5:
            log_rank(
                f"[Before train batch iter] Memory usage: {torch.cuda.memory_allocated() / 1024**2:.2f}MB. Peak reserved memory: {torch.cuda.max_memory_reserved() / 1024**2:.2f}MB",
                logger=logger,
                level=logging.INFO,
                group=self.dpg.dp_pg,
                rank=0,
            )

        outputs = self.pipeline_engine.train_batch_iter(
            model=self.model,
            pg=self.dpg.pp_pg,
            batch=(next(self.data_iterator) for _ in range(self.n_micro_batches_per_batch)),
            grad_accumulator=self.grad_accumulator,
        )

        if self.iteration_step < 5:
            log_rank(
                f"[After train batch iter] Memory usage: {torch.cuda.memory_allocated() / 1024**2:.2f}MB. Peak reserved memory: {torch.cuda.max_memory_reserved() / 1024**2:.2f}MB",
                logger=logger,
                level=logging.INFO,
                group=self.dpg.dp_pg,
                rank=0,
            )

        # Clip gradients
        grad_norm_unclipped = None
        if self.config.optimizer.clip_grad is not None:
            # Normalize DDP
            named_parameters = [
                (
                    param.get_tied_info().get_full_name_from_module_id_to_prefix(
                        module_id_to_prefix=self.module_id_to_prefix
                    )
                    if param.is_tied
                    else name,
                    param,
                )
                for name, param in self.normalized_model.named_parameters()
                if param.requires_grad
            ]
            # TODO @nouamane: we need to split `world_rank_matrix` along PP axis, to separate ref from active model
            grad_norm_unclipped = clip_grad_norm(
                mp_pg=self.dpg.world_ranks_to_pg[
                    tuple(sorted(self.dpg.world_rank_matrix[:, dist.get_rank(self.dpg.dp_pg), :].reshape(-1)))
                ],
                named_parameters=named_parameters,
                grad_accumulator=self.grad_accumulator,
                max_norm=self.config.optimizer.clip_grad,
            )

        # Apply gradient
        self.optimizer.step()
        # PT 2.0: will change default to None as it gains performance.
        # https://github.com/pytorch/pytorch/issues/92656
        self.optimizer.zero_grad(set_to_none=True)

        # Update the learning rate
        self.lr_scheduler.step()

        return outputs, grad_norm_unclipped

    @staticmethod
    def build_model(
        config: Config,
        model_config: AutoConfig,
        dpg: DistributedProcessGroups,
        random_states: RandomStates,
        target_pp_ranks: Optional[List[int]] = None,
    ):
        if model_config.__class__ not in CONFIG_TO_MODEL_CLASS:
            raise ValueError(
                f"Unsupported model config {model_config.__class__}. Only {CONFIG_TO_MODEL_CLASS.keys()} are supported"
            )

        # TODO: classes dont take same args
        model = CONFIG_TO_MODEL_CLASS[model_config.__class__](
            config=model_config, dpg=dpg, parallel_config=config.parallelism, random_states=random_states
        )

        # If no target pp ranks are specified, we assume that we want to use all pp ranks
        if target_pp_ranks is None:
            pp_size = dpg.pp_pg.size()
            target_pp_ranks = list(range(pp_size))
        else:
            pp_size = len(target_pp_ranks)

        # Set rank for each pipeline block
        pipeline_blocks = [module for name, module in model.named_modules() if isinstance(module, PipelineBlock)]
        # "cuda" is already defaulted for each process to it's own cuda device
        with init_on_device_and_dtype(device=torch.device("cuda"), dtype=config.model.dtype):
            # TODO: https://github.com/huggingface/brrr/issues/65

            # Balance compute across PP blocks
            block_compute_costs = model.get_block_compute_costs()
            block_cumulative_costs = np.cumsum(
                [
                    block_compute_costs[module.module_builder] if module.module_builder in block_compute_costs else 0
                    for module in pipeline_blocks
                ]
            )

            thresholds = [block_cumulative_costs[-1] * ((rank + 1) / pp_size) for rank in range(pp_size)]
            assert thresholds[-1] >= block_cumulative_costs[-1]
            target_pp_rank_idx = 0
            for block, cumulative_cost in zip(pipeline_blocks, block_cumulative_costs):
                assert target_pp_rank_idx < pp_size
                block.build_and_set_rank(target_pp_ranks[target_pp_rank_idx])

                if cumulative_cost > thresholds[target_pp_rank_idx]:
                    target_pp_rank_idx += 1

        # Initialize rotary embeddings
        for module in model.modules():
            if not isinstance(module, RotaryEmbedding):
                continue
            module.init_rotary_embeddings()

        return model

    def init_model(self, config: Config, dpg: DistributedProcessGroups, target_pp_ranks: Optional[List[int]] = None):
        model_config = AutoConfig.from_pretrained(config.model.hf_model_name)
        model_config.vocab_size = _vocab_size_with_padding(
            model_config.vocab_size,
            pg_size=dpg.tp_pg.size(),
            make_vocab_size_divisible_by=config.model.make_vocab_size_divisible_by,
        )
        model_config.num_hidden_layers = 5  # TODO: remove this
        assert (
            model_config.max_position_embeddings >= config.tokens.sequence_length
        ), f"max_position_embeddings ({model_config.max_position_embeddings}) must be >= sequence_length ({config.tokens.sequence_length})"

        log_rank(pformat(config), logger=logger, level=logging.INFO, rank=0)
        log_rank(str(model_config), logger=logger, level=logging.INFO, rank=0)

        parallel_config = config.parallelism
        make_ddp = not (config.optimizer.accumulate_grad_in_fp32 and config.optimizer.zero_stage > 0)

        # Build model
        model = self.build_model(
            config=config,
            model_config=model_config,
            dpg=dpg,
            random_states=self.random_states,
            target_pp_ranks=target_pp_ranks,
        )

        # Sync all parameters that have the same name and that are not sharded
        for module_name, module in model.named_modules():
            for param_name, param in module.named_parameters(recurse=False):
                name = f"{module_name}.{param_name}"

                if isinstance(model, GPTForTraining) and ".qkv.kv." in name:
                    assert param.is_tied, f"Expected {name} to already be synced"
                    # kv is deliberately skipped as it's tied in model init (_mark_kv_parameters_in_module_as_tied)
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
            f"Number of parameters: {num_params} ({size_params / 1024**2:.2f}MB)",
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
            # TODO @thomasw21: DDP doesn't support broadcasting complex buffers (and we don't really need that broadcasting anyway)
            model = DistributedDataParallel(model, process_group=dpg.dp_pg, broadcast_buffers=False)

        # Sanity check the model
        sanity_check(root_module=model)

        return model_config, model

    @staticmethod
    def setup_log_writers(config: Config):
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
                )
            if isinstance(config.logging.tensorboard_logger, TensorboardLoggerConfig):
                assert (
                    tb_logger_available
                ), 'Tensorboard Logger is not available. Please install brrr with `pip install -e ".[tb-logger]"` or modify your config file'
                tb_context = BatchSummaryWriter(logdir=logdir)
        loggerwriter = LoggerWriter(global_step=config.tokens.train_steps)
        return tb_context, loggerwriter
