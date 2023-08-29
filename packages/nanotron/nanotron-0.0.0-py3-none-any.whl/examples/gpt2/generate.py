from pathlib import Path

import torch
from config import ParallelismArgs
from generation import GenerationConfig, GenerationInput, greedy_search
from main import (
    _vocab_size_with_padding,
    init_model,
)
from transformers import AutoTokenizer, GPT2Config

from brrr.core import distributed as dist
from brrr.core import logging
from brrr.core.logging import log_rank
from brrr.core.parallelism.pipeline_parallelism.engine import OneForwardOneBackwardPipelineEngine
from brrr.core.parallelism.pipeline_parallelism.tensor_pointer import TensorPointer
from brrr.core.parallelism.tensor_parallelism.nn import TensorParallelLinearMode
from brrr.core.process_groups_initializer import get_process_groups
from brrr.core.random import (
    set_random_seed,
)
from brrr.core.serialize.weights import load_weights

logger = logging.get_logger(__name__)


def main():
    checkpoint_path = Path("/fsx/kunhao/checkpoints/brrr/gpt2-v3/new")

    parallel_config = ParallelismArgs(
        dp=1,
        pp=1,
        tp=4,
        pp_engine=OneForwardOneBackwardPipelineEngine(),
        tp_mode=TensorParallelLinearMode.ALL_REDUCE,
        recompute_granularity=None,
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

    model_name = "gpt2"
    model_config = GPT2Config.from_pretrained(model_name)
    model_config.vocab_size = _vocab_size_with_padding(
        model_config.vocab_size,
        pg_size=dpg.tp_pg.size(),
        make_vocab_size_divisible_by=256 // dpg.tp_pg.size(),
    )
    model, random_states = init_model(
        model_config=model_config, parallel_config=parallel_config, dtype=dtype, dpg=dpg, make_ddp=False
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
        "Hello, my name is",
    ] * 8

    outputs = greedy_search(
        input_iter=(GenerationInput(text=text) for text in dummy_inputs),
        tokenizer=tokenizer,
        # TODO @thomasw21: From ModelWithLoss extract the model.
        model=model.model,
        # TODO @thomasw21: Figure out how to pass p2p.
        p2p=model.model.p2p,
        dpg=dpg,
        generation_config=GenerationConfig(max_new_tokens=20),
        max_micro_batch_size=8,
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
