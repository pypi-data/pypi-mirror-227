"""Script that converts a BRRR `gpt2_mqa` checkpoint to transformers format.

Usage:
python examples/gpt2_mqa/convert_checkpoint_to_transformers.py --checkpoint-path /fsx/thomaswang/experiments/brrr-starcoder-5b-v1/checkpoints/7500/ --model-name HuggingFaceBR4/starcoder-5b --save-path converted/7500
"""

import argparse
from pathlib import Path

import torch
from config import ModelArgs, ParallelismArgs, RandomInit
from main import init_model
from torch import nn
from transformers import AutoModelForCausalLM, AutoTokenizer, GPTBigCodeConfig, GPTBigCodeForCausalLM

from brrr.core.parallelism.pipeline_parallelism.engine import AllForwardAllBackwardPipelineEngine
from brrr.core.parallelism.tensor_parallelism.enum import TensorParallelLinearMode
from brrr.core.process_groups_initializer import get_process_groups
from brrr.core.serialize import load_weights
from brrr.core.utils import (
    init_on_device_and_dtype,
)


def get_args():
    parser = argparse.ArgumentParser()
    # CONFIG for checkpoint
    parser.add_argument("--checkpoint-path", type=Path, required=True, help="Path to the BRRR checkpoint")
    parser.add_argument("--model-name", type=str, required=True, help="HF model name")

    # Save path
    parser.add_argument("--save-path", type=Path, required=True, help="Path to save the converted checkpoint")

    args = parser.parse_args()

    # Parse brrr config
    checkpoint_path = Path(args.checkpoint_path)
    save_path = Path(args.save_path)
    model_name = args.model_name
    assert checkpoint_path.exists(), f"checkpoint_path {checkpoint_path} does not exist"
    if save_path.exists() and len(list(save_path.iterdir())) > 0:
        raise ValueError(f"save_path {save_path} already exists and is not empty")

    return checkpoint_path, save_path, model_name


def get_name_mapping(model_config: ModelArgs):
    """Maps transformers name to `brrr` names"""
    decoder_mapping = {}
    trfs_name_to_brrr_names = {
        "ln_1.weight": ("ln_1.weight",),
        "ln_1.bias": ("ln_1.bias",),
        "attn.c_attn.weight": ("attn.qkv.q.weight", "attn.qkv.kv.weight"),
        "attn.c_attn.bias": ("attn.qkv.q.bias", "attn.qkv.kv.bias"),
        "attn.c_proj.weight": ("attn.o.weight",),
        "attn.c_proj.bias": ("attn.o.bias",),
        "ln_2.weight": ("ln_2.weight",),
        "ln_2.bias": ("ln_2.bias",),
        "mlp.c_fc.weight": ("ff.c_fc.weight",),
        "mlp.c_fc.bias": ("ff.c_fc.bias",),
        "mlp.c_proj.weight": ("ff.c_proj.weight",),
        "mlp.c_proj.bias": ("ff.c_proj.bias",),
    }
    for layer_id in range(model_config.num_layers):
        for trfs_suffix, brrr_suffixes in trfs_name_to_brrr_names.items():
            trfs_name = f"transformer.h.{layer_id}.{trfs_suffix}"
            brrr_names = tuple(f"model.decoder.{layer_id}.pp_block.{brrr_suffix}" for brrr_suffix in brrr_suffixes)
            decoder_mapping[trfs_name] = brrr_names
    return {
        "transformer.wte.weight": ("model.token_position_embeddings.pp_block.token_embedding.weight",),
        "transformer.wpe.weight": ("model.token_position_embeddings.pp_block.position_embedding.weight",),
        **decoder_mapping,
        "transformer.ln_f.weight": ("model.final_layer_norm.pp_block.weight",),
        "transformer.ln_f.bias": ("model.final_layer_norm.pp_block.bias",),
        "lm_head.weight": ("model.lm_head.pp_block.weight",),
    }


def convert_checkpoint_and_save(checkpoint_path: Path, save_path: Path, model_name: str):
    dp, tp, pp = 1, 1, 1
    dtype = torch.float

    print("Loading checkpoint from:", checkpoint_path)

    dpg = get_process_groups(data_parallel_size=dp, tensor_parallel_size=tp, pipeline_parallel_size=pp)

    parallel_config = ParallelismArgs(
        dp=dp,
        tp=tp,
        pp=pp,
        pp_engine=AllForwardAllBackwardPipelineEngine(),
        recompute_granularity=None,
        tp_linear_async_communication=False,
        tp_mode=TensorParallelLinearMode.ALL_REDUCE,
    )

    # Initialise brrr model
    trfs_model_config = GPTBigCodeConfig.from_pretrained(model_name)
    brrr_model_config = ModelArgs(
        hidden_size=trfs_model_config.n_embd,
        num_attention_heads=trfs_model_config.n_head,
        ffn_hidden_size=trfs_model_config.n_inner
        if trfs_model_config.n_inner is not None
        else 4 * trfs_model_config.n_embd,
        num_layers=trfs_model_config.n_layer,
        max_position_embeddings=trfs_model_config.n_positions,
        vocab_size=trfs_model_config.vocab_size,
        layer_norm_epsilon=trfs_model_config.layer_norm_epsilon,
        scale_attn_weights=trfs_model_config.scale_attn_weights,
        activation_function=trfs_model_config.activation_function,
        resid_pdrop=trfs_model_config.resid_pdrop,
        attn_pdrop=trfs_model_config.attn_pdrop,
        embd_pdrop=trfs_model_config.embd_pdrop,
        assert_make_sharded_vocab_size_divisible_by=1,
        dtype=trfs_model_config.torch_dtype,
        init_method=RandomInit(std=trfs_model_config.initializer_range),
        seed=42,
    )
    brrr_model, _ = init_model(
        model_config=brrr_model_config,
        parallel_config=parallel_config,
        dpg=dpg,
        dtype=dtype,
        make_ddp=False,
        device=torch.device("cpu"),
    )

    # Load checkpoint directly in memory and then only keep the state dictionary
    load_weights(model=brrr_model, dpg=dpg, root_folder=checkpoint_path)
    brrr_state_dict = brrr_model.state_dict()
    del brrr_model

    # Get `trfs` mapping to `brrr` names
    trfs_name_to_brrr_names = get_name_mapping(model_config=brrr_model_config)

    # Initialised `trfs` model in `meta` device.
    with init_on_device_and_dtype(torch.device("meta"), trfs_model_config.torch_dtype):
        trfs_model = GPTBigCodeForCausalLM._from_config(trfs_model_config)

    # This is useful in order to track tied parameters
    trfs_meta_param_id_to_brr_param = {}

    for trfs_module_name, trfs_module in trfs_model.named_modules():
        for trfs_param_name, trfs_param in trfs_module.named_parameters(recurse=False):
            if id(trfs_param) in trfs_meta_param_id_to_brr_param:
                # TODO @thomasw21: Figure out why torch doesn't allow to populate meta tensor in a better way ...
                trfs_module._parameters[trfs_param_name] = trfs_meta_param_id_to_brr_param[id(trfs_param)]
                continue

            trfs_name = f"{trfs_module_name}.{trfs_param_name}"
            # Get all `brrr` parameters
            brrr_params = [brrr_state_dict[brrr_name] for brrr_name in trfs_name_to_brrr_names[trfs_name]]

            # Assert that we haven't release the parameter yet
            assert all(brrr_param.device.type != "meta" for brrr_param in brrr_params)

            # Merge them if necessary
            brrr_param: torch.Tensor
            if len(brrr_params) > 1:
                if "c_attn" in trfs_name:
                    q_param, kv_param = brrr_params
                    brrr_param = torch.cat([q_param, kv_param], dim=0)
                else:
                    raise ValueError(f"Who the fuck needs multiple `brrr` params? {trfs_name}")
            else:
                brrr_param = brrr_params[0]

            # Check that the parameters has the correct metadatas
            assert trfs_param.shape == brrr_param.shape

            # Assign the new parameter
            trfs_meta_param_id_to_brr_param[id(trfs_param)] = nn.Parameter(brrr_param)
            # TODO @thomasw21: Figure out why torch doesn't allow to populate meta tensor in a better way ...
            trfs_module._parameters[trfs_param_name] = trfs_meta_param_id_to_brr_param[id(trfs_param)]

            # release memory from `brrr` model. We just assume that a `brrr` parameter only appears once
            # TODO @thomasw21: Figure out how we need to make sure we release memory
            for brrr_name in trfs_name_to_brrr_names[trfs_name]:
                brrr_state_dict[brrr_name] = brrr_state_dict[brrr_name].to("meta")

    print("Saving transformers model to:", save_path)
    trfs_model.save_pretrained(save_path)


def test_conversion(checkpoint_path: Path, model_name: str):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(checkpoint_path)
    inputs = tokenizer("def fibonnaci(", return_tensors="pt")
    print("Testing generation with prompt 'def fibonnaci('")
    output = model.generate(**inputs, max_length=100, do_sample=False, num_beams=1)
    print(tokenizer.decode(output[0]))


def main():
    checkpoint_path, save_path, model_name = get_args()
    convert_checkpoint_and_save(checkpoint_path=checkpoint_path, save_path=save_path, model_name=model_name)

    # Test generation
    test_conversion(checkpoint_path=save_path, model_name=model_name)


if __name__ == "__main__":
    main()
