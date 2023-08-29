"""

You can run using command:
```
CUDA_DEVICE_MAX_CONNECTIONS=1 torchrun --nproc_per_node=4 examples/use_trainer.py
```
"""
from brrr.config import (
    Config,
    get_args_from_path,
)
from brrr.trainer import DistributedTrainer

if __name__ == "__main__":
    config: Config = get_args_from_path("examples/llama/configs/config_nouamane_llama_test_trainer.yaml")
    trainer = DistributedTrainer(config=config)

    trainer.train()
