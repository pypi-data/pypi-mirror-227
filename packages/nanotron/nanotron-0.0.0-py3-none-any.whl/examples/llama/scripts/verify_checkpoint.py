"""Script that checks the integrity of a BRRR `gpt2_mqa` checkpoint

Usage:
python -m examples.llama.scripts.verify_checkpoint --checkpoint-path checkpoint/10 --model-name huggyllama/llama-7b
"""

import argparse
import glob
from collections import OrderedDict
from pathlib import Path

import torch
from tqdm import tqdm
from transformers import LlamaConfig, LlamaForCausalLM

from brrr.core.serialize.serialize import safe_open
from brrr.core.utils import init_on_device_and_dtype

from .convert_checkpoint import NAME_MAPPING


def get_args():
    parser = argparse.ArgumentParser()
    # CONFIG for checkpoint
    # TODO @nouamane: be able to load only safetensors metadata from s3 to compare shapes
    parser.add_argument("--checkpoint-path", type=Path, required=True, help="Path to the BRRR checkpoint")
    parser.add_argument("--model-name", type=str, required=True, help="HF model name")

    args = parser.parse_args()

    # Parse brrr config
    checkpoint_path = Path(args.checkpoint_path)
    model_name = args.model_name
    assert checkpoint_path.exists(), f"checkpoint_path {checkpoint_path} does not exist"

    return checkpoint_path, model_name


def verify_checkpoint(checkpoint_path, model_name):
    print("Loading checkpoint from:", checkpoint_path)

    # Initialise brrr model
    model_config = LlamaConfig.from_pretrained(model_name)
    with init_on_device_and_dtype("meta", model_config.torch_dtype):
        model = LlamaForCausalLM._from_config(model_config)

    trfrs_to_brrr_shards = OrderedDict()
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
        for k, v in NAME_MAPPING.items():
            name = name.replace(k, v)

        # skip buffers
        if name.endswith(".model_inv_freq"):
            continue

        assert name in trfrs_tensor_names, f"Couldn't find {name} in trfrs_tensor_names: {trfrs_tensor_names[:10]}..."
        if name in trfrs_to_brrr_shards:
            trfrs_to_brrr_shards[name].append({"brrr_path": path})
        else:
            trfrs_to_brrr_shards[name] = [{"brrr_path": path}]

    if tied_embeddings:
        # model.state_dict() will always have "lm_head.weight" and "lm_head.bias" even when tied
        assert (
            "lm_head.weight" not in trfrs_to_brrr_shards
        ), "LM head must be tied to input embeddings but found lm_head.weight in BRRR checkpoint."
        assert (
            "lm_head.bias" not in trfrs_to_brrr_shards
        ), "LM head must be tied to input embeddings but found lm_head.bias in BRRR checkpoint."

    # assert all keys in transformers are found in brrr checkpoint
    assert {n for n, _ in model.named_parameters()} == set(
        trfrs_to_brrr_shards.keys()
    ), f"Keys in transformers model not found in BRRR model: {set(n for n,_ in model.named_parameters()) - set(trfrs_to_brrr_shards.keys())}"  # noqa: C401

    state_dict = model.state_dict()
    for name, shards in tqdm(trfrs_to_brrr_shards.items(), desc="Matching tensors shapes"):
        # concatenate shards along `concat_dim`
        tensor = []
        for shard in shards:
            path = shard["brrr_path"]
            with safe_open(path, framework="pt", device="cpu") as fi:
                shard = fi.get_tensor("data")
                metadata = fi.metadata()
                if "concat_dim" in metadata:
                    assert len(shards) > 1, f"Found concat_dim in metadata but only 1 shard for {path}"
                    concat_dim = int(metadata["concat_dim"])
                    tensor.append(shard)
                else:
                    assert len(shards) == 1, f"Didn't find concat_dim in metadata but more than 1 shard for {path}"
                    concat_dim = None
                    tensor = shard
        if len(shards) > 1:
            tensor = torch.cat(tensor, dim=concat_dim)

        # if ".q_proj." in name:
        #     # get q from interleaved qkv
        #     qkv = tensor.view(3, -1, tensor.shape[-1])
        #     tensor = qkv[0, :, :]

        # elif ".k_proj." in name:
        #     tensor = qkv[1, :, :]

        # elif ".v_proj." in name:
        #     tensor = qkv[2, :, :]

        # slice vocab padding to be able to load model in transformers
        if name in ["model.embed_tokens.weight", "lm_head.weight"]:
            tensor = tensor[: model.config.vocab_size]

        trfrs_tensor = state_dict[name]  # pylint: disable=unsubscriptable-object
        assert trfrs_tensor.shape == tensor.shape, f"Shape mismatch for {name}: {trfrs_tensor.shape} != {tensor.shape}"


def main():
    checkpoint_path, model_name = get_args()
    verify_checkpoint(checkpoint_path, model_name)
    print(f"Checkpoint matches transformers model: {model_name}")


if __name__ == "__main__":
    main()
