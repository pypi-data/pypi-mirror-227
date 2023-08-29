from dataclasses import dataclass

from brrr.core.parallelism.tensor_parallelism.enum import TensorParallelLinearMode


@dataclass
class TrainingModelArgs:
    recompute_mode: str  # "selective"
    tp_mode: TensorParallelLinearMode


@dataclass
class OptimizerArgs:
    zero_stage: int
    accumulate_grad_in_fp32: bool
    weight_decay: float
    adam_eps: float
    adam_beta1: float
    adam_beta2: float
    lr: float


@dataclass
class LRSchedulerArgs:
    lr_decay_style: str
    lr_decay_steps: int
    min_decay_lr: float
    lr_warmup_style: str
    lr_warmup_steps: int
