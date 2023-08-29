""" Example of generation with a pretrained Llama model.

torchrun  --nproc_per_node=4 examples/llama/generate.py
"""
from pathlib import Path

import torch
from config import ParallelismArgs
from generation import GenerationConfig, GenerationInput, TokenizerConfig, greedy_search
from train import LlamaForTraining, init_model
from transformers import AutoTokenizer, LlamaConfig

from brrr.core import distributed as dist
from brrr.core import logging
from brrr.core.logging import log_rank
from brrr.core.parallelism.pipeline_parallelism.engine import OneForwardOneBackwardPipelineEngine
from brrr.core.parallelism.pipeline_parallelism.tensor_pointer import TensorPointer
from brrr.core.parallelism.tensor_parallelism.enum import TensorParallelLinearMode
from brrr.core.process_groups_initializer import get_process_groups
from brrr.core.random import (
    set_random_seed,
)
from brrr.core.serialize.weights import load_weights

logger = logging.get_logger(__name__)


def main():
    checkpoint_path = Path("/fsx/nouamane/projects/brrr/pretrained/llama-7b-orig")
    parallel_config = ParallelismArgs(
        dp=1,
        pp=2,
        tp=2,
        pp_engine=OneForwardOneBackwardPipelineEngine(),
        tp_mode=TensorParallelLinearMode.ALL_REDUCE,
        recompute_granularity=None,
        tp_linear_async_communication=False,
    )
    dtype = torch.bfloat16

    # Set random states
    set_random_seed(42)

    # Initialise all process groups
    dpg = get_process_groups(
        data_parallel_size=parallel_config.dp,
        pipeline_parallel_size=parallel_config.pp,
        tensor_parallel_size=parallel_config.tp,
    )

    model_name = "huggyllama/llama-7b"
    model_config: LlamaConfig = LlamaConfig.from_pretrained(model_name)

    model = init_model(
        model_builder=lambda: LlamaForTraining(config=model_config, dpg=dpg, parallel_config=parallel_config),
        model_config=model_config,
        parallel_config=parallel_config,
        dtype=dtype,
        dpg=dpg,
        make_ddp=False,
    )

    # Load checkpoint
    log_rank(
        f"Loading checkpoint from {checkpoint_path}:",
        logger=logger,
        level=logging.INFO,
        rank=0,
    )
    load_weights(model=model, dpg=dpg, root_folder=checkpoint_path)

    model.eval()
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"
    dummy_inputs = [
        "This film was probably inspired by Godzilla",
        "If the crew behind 'Zombieland' had a",
    ]

    outputs = greedy_search(
        input_iter=(GenerationInput(text=text) for text in dummy_inputs),
        tokenizer=tokenizer,
        # TODO @thomasw21: From ModelWithLoss extract the model.
        model=model.model,
        # TODO @thomasw21: Figure out how to pass p2p.
        p2p=model.model.p2p,
        dpg=dpg,
        generation_config=GenerationConfig(max_new_tokens=128, max_micro_batch_size=8),
        tokenizer_config=TokenizerConfig(max_input_length=8),
    )
    dist.barrier()
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
    dist.barrier()


if __name__ == "__main__":
    main()
