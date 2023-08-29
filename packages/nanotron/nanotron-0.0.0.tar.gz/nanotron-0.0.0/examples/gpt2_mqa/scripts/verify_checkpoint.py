"""Script that checks the integrity of a BRRR `gpt2_mqa` checkpoint

Usage:
python examples/gpt2_mqa/scripts/verify_checkpoint.py --checkpoint-path /fsx/thomaswang/experiments/brrr-starcoder-5b-v1/checkpoints/7500/ --model-name HuggingFaceBR4/starcoder-5b
"""

import argparse
import glob
from pathlib import Path

import torch
from convert_checkpoint import NAME_MAPPING
from tqdm import tqdm
from transformers import GPTBigCodeConfig, GPTBigCodeForCausalLM

from brrr.core.serialize.serialize import safe_open
from brrr.core.utils import (
    init_on_device_and_dtype,
)


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
    model_config = GPTBigCodeConfig.from_pretrained(model_name)
    with init_on_device_and_dtype("meta", model_config.torch_dtype):
        model = GPTBigCodeForCausalLM._from_config(model_config)

    trfrs_to_brrr_shards = {}
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

        # add "transformer." prefix if not "lm_head"
        if not name.startswith("lm_head"):
            name = "transformer." + name

        # remove ".pp_block."
        name = name.replace(".pp_block.", ".")

        # apply mapping
        for k, v in NAME_MAPPING.items():
            name = name.replace(k, v)

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
        # process QKV separately
        if ".c_attn." in name:
            # concatenate q along `concat_dim`
            q, q_concat_dim = [], None
            for shard in shards:
                path = shard["brrr_path"]
                if "/q/" in path:
                    # load sharded q
                    with safe_open(path, framework="pt", device="cpu") as fi:
                        tensor = fi.get_tensor("data")
                        metadata = fi.metadata()
                        if "concat_dim" in metadata:
                            if q_concat_dim is None:
                                q_concat_dim = int(metadata["concat_dim"])
                            else:
                                assert q_concat_dim == int(metadata["concat_dim"])
                        else:
                            q_concat_dim = None
                    q.append(tensor)  # Warning: we make sure paths are sorted
                if "/kv/" in path:
                    # load sharded kv
                    with safe_open(path, framework="pt", device="cpu") as fi:
                        tensor = fi.get_tensor("data")
                    kv = tensor
            q = torch.cat(q, dim=q_concat_dim)
            # concatenate q and kv along `0`
            tensor = torch.cat([q, kv], dim=0)

        else:
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

        # TODO @nouamane: not sure if we should remove this
        # slice vocab padding
        # if name in ["transformer.wte.weight", "lm_head.weight"]:
        #     tensor = tensor[: model.config.vocab_size]

        trfrs_tensor = state_dict[name]  # pylint: disable=unsubscriptable-object

        assert trfrs_tensor.shape == tensor.shape, f"Shape mismatch for {name}: {trfrs_tensor.shape} != {tensor.shape}"


def main():
    checkpoint_path, model_name = get_args()
    verify_checkpoint(checkpoint_path, model_name)
    print(f"Checkpoint matches transformers model: {model_name}")


if __name__ == "__main__":
    main()
