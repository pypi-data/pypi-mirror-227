"""Script that converts a BRRR `llama` checkpoint to transformers format.

Usage:
python examples/llama/scripts/convert_checkpoint.py --checkpoint-path checkpoint/10 --model-name huggyllama/llama-7b  --save-path converted/10
"""

import argparse
import glob
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List, Tuple

import torch
from tqdm import tqdm
from transformers import AutoConfig, AutoTokenizer, LlamaConfig, LlamaForCausalLM

from brrr.core.parallelism.parameters import SlicesPair
from brrr.core.serialize.meta import TensorMetadataV2
from brrr.core.serialize.serialize import safe_open

BRRR_TRFRS_NAME_MAPPING = [
    ("model_weight", "weight"),
    ("model_bias", "bias"),
    ("token_position_embeddings.token_embedding", "embed_tokens"),
    ("token_position_embeddings.position_embedding", "wpe"),
    (".decoder.", ".layers."),
    (".attn.", ".self_attn."),
    (".o.", ".o_proj."),
    (".ff.", ".mlp."),
    (".final_layer_norm.", ".norm."),
]

BRRR_TRFRS_VAR_MAPPING = [
    (".qkv_proj.", ".q_proj."),
    (".qkv_proj.", ".k_proj."),
    (".qkv_proj.", ".v_proj."),
    (".gate_up_proj.", ".gate_proj."),
    (".gate_up_proj.", ".up_proj."),
]
IGNORED_TRANSFORMER_KEYS = []


def apply_mappings(name: str, mappings: List[Tuple[str, str]], reverse: bool = False) -> str:
    for brrr_name, trfr_name in mappings:
        if reverse:
            name = name.replace(trfr_name, brrr_name)
        else:
            name = name.replace(brrr_name, trfr_name)
    return name


def anti_permute_for_rotary(tensor, num_heads, head_dim, hidden_size):
    """undo the permutation done by permute_for_rotary"""
    return (
        tensor.view(num_heads, head_dim // 2, 2, hidden_size)
        .transpose(1, 2)
        .contiguous()
        .view(num_heads * head_dim, hidden_size)
    )


def load_tensor_from_shard_paths(shard_paths: List[Dict[str, Any]]) -> torch.Tensor:
    checkpoint_unsharded_shape = None
    shards_and_slices_maps: List[Tuple[torch.Tensor, Tuple[SlicesPair, ...]]] = []
    if len(shard_paths) == 1:
        shard_path = shard_paths[0]
        with safe_open(shard_path, framework="pt", device="cpu") as fi:
            tensor = fi.get_tensor("data")
    else:
        for shard_path in shard_paths:
            with safe_open(shard_path, framework="pt", device="cpu") as fi:
                # TODO @thomasw21: Choose only a slice if we switch the TP topology
                param_metadata = fi.metadata()
                param_metadata = TensorMetadataV2.from_str_dict(param_metadata)
                shards_and_slices_maps.append((fi.get_tensor("data"), param_metadata.local_global_slices_pairs))
                if checkpoint_unsharded_shape is None:
                    checkpoint_unsharded_shape = param_metadata.unsharded_shape
                else:
                    assert checkpoint_unsharded_shape == param_metadata.unsharded_shape

        assert checkpoint_unsharded_shape is not None
        # TODO @thomasw21: Interestingly enough we don't actually need to instantiate the entire model at all.
        tensor = torch.empty(checkpoint_unsharded_shape, device="cpu")
        for shard, slices_pairs in shards_and_slices_maps:
            for slices_pair in slices_pairs:
                local_slices = slices_pair.local_slices
                global_slices = slices_pair.global_slices
                tensor[global_slices] = shard[local_slices]
    return tensor


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


def main():
    checkpoint_path, save_path, model_name = get_args()

    print("Loading checkpoint from:", checkpoint_path)

    # Initialise brrr model
    model_config: LlamaConfig = AutoConfig.from_pretrained(model_name)
    model = LlamaForCausalLM._from_config(model_config)

    brrr_name_2_shard_paths = OrderedDict()
    brrr_tensor_paths = glob.glob(str(checkpoint_path / "model" / "**/*.safetensors"), recursive=True)
    # named_parameters is better than state_dict here because it doesnt show tied parameters, but it doesnt work with "meta" device
    trfrs_tensor_names = list(model.state_dict().keys())

    # Check for tied lm head and word embeddings
    tied_embeddings = model.config.tie_word_embeddings is True

    # We must preprocess 'checkpoint/10/model/token_position_embeddings/pp_block/token_embedding/model_weight_pp-rank-0-of-2_tp-rank-0-of-2.safetensors'
    # to be like 'transformer.wte.weight
    for path in sorted(brrr_tensor_paths):
        name = path
        # remove `_pp-rank*` and what comes after
        name = name.split("_pp-rank-")[0]

        # remove `.safetensors`
        name = name.split(".safetensors")[0]

        # remove base path
        name = name.split(str(checkpoint_path) + "/model/")[1]

        # "/" -> "."
        name = name.replace("/", ".")

        # remove "model." prefix if lm_head
        if ".lm_head." in name:
            name = name[len("model.") :]

        # remove ".pp_block."
        name = name.replace(".pp_block.", ".")

        # apply mapping
        name = apply_mappings(name, BRRR_TRFRS_NAME_MAPPING)

        # skip buffers
        if name.endswith(".model_inv_freq"):
            continue

        if name in brrr_name_2_shard_paths:
            brrr_name_2_shard_paths[name].append(path)
        else:
            brrr_name_2_shard_paths[name] = [path]

        # apply variable mapping for verification
        name = apply_mappings(name, BRRR_TRFRS_VAR_MAPPING)
        assert name in trfrs_tensor_names, f"Couldn't find {name} in trfrs_tensor_names: {trfrs_tensor_names[:10]}..."

    if tied_embeddings:
        # model.state_dict() will always have "lm_head.weight" and "lm_head.bias" even when tied
        assert (
            "lm_head.weight" not in brrr_name_2_shard_paths
        ), "LM head must be tied to input embeddings but found lm_head.weight in BRRR checkpoint."
        assert (
            "lm_head.bias" not in brrr_name_2_shard_paths
        ), "LM head must be tied to input embeddings but found lm_head.bias in BRRR checkpoint."

    # assert all keys in transformers are found in brrr checkpoint
    trfrs_set = {
        apply_mappings(n, BRRR_TRFRS_VAR_MAPPING, reverse=True)
        for n, _ in model.named_parameters()
        if all(k not in n for k in IGNORED_TRANSFORMER_KEYS)
    }
    assert trfrs_set.issubset(
        set(brrr_name_2_shard_paths.keys())
    ), f"Keys in transformers model not found in BRRR model: {trfrs_set - set(brrr_name_2_shard_paths.keys())}"  # noqa: C401

    head_dim = model.config.hidden_size // model.config.num_attention_heads

    for trfr_name, trfrs_tensor in tqdm(model.state_dict().items()):
        brrr_name = apply_mappings(trfr_name, BRRR_TRFRS_VAR_MAPPING, reverse=True)
        brrr_shard_paths = brrr_name_2_shard_paths[brrr_name]
        loaded_tensor = load_tensor_from_shard_paths(brrr_shard_paths)

        # slice vocab padding to be able to load model in transformers
        if trfr_name in ["model.embed_tokens.weight", "lm_head.weight"]:
            tensor = loaded_tensor[: model.config.vocab_size]
        elif ".q_proj." in trfr_name:
            tensor = loaded_tensor[: head_dim * model_config.num_attention_heads]
            tensor = anti_permute_for_rotary(
                tensor=tensor,
                num_heads=model_config.num_attention_heads,
                head_dim=head_dim,
                hidden_size=model_config.hidden_size,
            )
        elif ".k_proj." in trfr_name:
            tensor = loaded_tensor[
                head_dim * model_config.num_attention_heads : head_dim * model_config.num_attention_heads
                + head_dim * model_config.num_key_value_heads
            ]
            tensor = anti_permute_for_rotary(
                tensor=tensor,
                num_heads=model_config.num_key_value_heads,
                head_dim=head_dim,
                hidden_size=model_config.hidden_size,
            )
        elif ".v_proj." in trfr_name:
            tensor = loaded_tensor[-head_dim * model_config.num_key_value_heads :]
        elif ".gate_proj." in trfr_name:
            assert loaded_tensor.shape[0] // 2 == model_config.intermediate_size
            tensor = loaded_tensor[: model_config.intermediate_size]
        elif ".up_proj." in trfr_name:
            assert loaded_tensor.shape[0] // 2 == model_config.intermediate_size
            tensor = loaded_tensor[model_config.intermediate_size :]
        else:
            tensor = loaded_tensor

        assert trfrs_tensor.shape == tensor.shape, f"Shape mismatch for {name}: {trfrs_tensor.shape} != {tensor.shape}"

        trfrs_tensor[:] = tensor  # pylint: disable=unsubscriptable-object

    print("Saving transformers model to:", save_path)
    model.save_pretrained(save_path)

    # Test generation
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    inputs = tokenizer("The quick brown fox jumps over the lazy dog", return_tensors="pt")
    print("Testing generation with prompt 'The quick brown fox jumps over the lazy dog'")
    output = model.generate(**inputs, max_length=100, do_sample=False, num_beams=1)
    print(tokenizer.decode(output[0]))


if __name__ == "__main__":
    main()
