# Test it over an arange of steps
import math
from dataclasses import dataclass

import matplotlib.pyplot as plt


@dataclass
class OptimizerArgs:
    lr: float


@dataclass
class LRSchedulerArgs:
    lr_warmup_style: str
    lr_warmup_steps: int
    lr_decay_style: str
    lr_decay_steps: int
    min_decay_lr: float


optimizer_args = OptimizerArgs(
    lr=2.0,
)

lr_scheduler_args = LRSchedulerArgs(
    lr_warmup_style="linear",
    lr_warmup_steps=100,
    lr_decay_style="cosine",
    lr_decay_steps=200,
    min_decay_lr=0.2,
)


# Build LR Scheduler
def lr_lambda(current_step: int):
    """LR Scheduling function, it has 3 phases: warmup, decay, then constant. Warmup starts at lr=0 and ends at `lr=lr`, then it decays until `min_decay_lr` and then stays constant."""
    # No warmup or decay
    if lr_scheduler_args.lr_warmup_steps == 0 and lr_scheduler_args.lr_decay_steps == 0:
        return optimizer_args.lr

    # Warmup phase
    elif lr_scheduler_args.lr_warmup_style is not None and current_step <= lr_scheduler_args.lr_warmup_steps:
        if lr_scheduler_args.lr_warmup_style == "linear":
            lmbda = optimizer_args.lr * current_step / max(lr_scheduler_args.lr_warmup_steps, 1)
        elif lr_scheduler_args.lr_warmup_style == "constant":
            lmbda = optimizer_args.lr
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
                + (optimizer_args.lr - lr_scheduler_args.min_decay_lr)
                * (
                    1
                    + math.cos(
                        math.pi * (current_step - lr_scheduler_args.lr_warmup_steps) / lr_scheduler_args.lr_decay_steps
                    )
                )
                / 2
            )
        elif lr_scheduler_args.lr_decay_style == "linear":
            lmbda = (
                lr_scheduler_args.min_decay_lr
                + (optimizer_args.lr - lr_scheduler_args.min_decay_lr)
                * (lr_scheduler_args.lr_decay_steps - (current_step - lr_scheduler_args.lr_warmup_steps))
                / lr_scheduler_args.lr_decay_steps
            )
        else:
            raise ValueError(f"Unknown decay style {lr_scheduler_args.lr_decay_style}")

    # Constant phase
    else:
        lmbda = lr_scheduler_args.min_decay_lr

    return lmbda


def test_lr_scheduler(steps=400):
    lr = []
    for i in range(1, steps):
        lr.append(lr_lambda(i))
    return lr


if __name__ == "__main__":
    lr = test_lr_scheduler()
    plt.plot(lr)
    plt.savefig(f"{lr_scheduler_args.lr_warmup_style}_{lr_scheduler_args.lr_decay_style}.png")
