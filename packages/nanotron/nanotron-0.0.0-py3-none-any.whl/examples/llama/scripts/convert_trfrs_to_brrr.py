# ruff: noqa: E402
"""
This module converts a transformers LlamaForCausalLM to a brrr model

Command:
    torchrun  --nproc_per_node=8 examples/llama/scripts/convert_trfrs_to_brrr.py --pp 8 --model_name huggyllama/llama-65b --save_path pretrained/llama-65b
    torchrun  --nproc_per_node=4 examples/llama/scripts/convert_trfrs_to_brrr.py --pp 4 --model_name huggyllama/llama-7b --save_path pretrained/llama-7bz
    torchrun  --nproc_per_node=4 examples/llama/scripts/convert_trfrs_to_brrr.py --pp 4 --model_name  meta-llama/Llama-2-7b-chat-hf --save_path pretrained/llama-2-7b-chat
"""
import argparse
import sys
from pathlib import Path
from typing import Dict, List

import torch

sys.path.append(Path(__file__).parent.parent.as_posix())
import os

from config import ParallelismArgs, RecomputeGranularity
from train import init_model
from transformers import LlamaConfig, LlamaForCausalLM

import brrr.core.distributed as dist
from brrr.core.parallelism.parameters import BRRRParameter
from brrr.core.parallelism.pipeline_parallelism.engine import (
    AllForwardAllBackwardPipelineEngine,
)
from brrr.core.parallelism.tensor_parallelism.nn import TensorParallelLinearMode
from brrr.core.process_groups_initializer import get_process_groups
from brrr.core.serialize import save_meta, save_weights

if os.environ.get("USE_FAST"):
    # We import the fast versions
    from modeling_llama_fast import LlamaForTraining
else:
    from modeling_llama import LlamaForTraining


def get_args():
    parser = argparse.ArgumentParser(description="Convert transformers weights to brrr weights")
    parser.add_argument("--model_name", type=str, default="huggyllama/llama-7b")
    parser.add_argument("--save_path", type=str, default="pretrained/llama-7b")
    parser.add_argument("--dp", type=int, default=1)
    parser.add_argument("--pp", type=int, default=2)
    parser.add_argument("--tp", type=int, default=1)
    return parser.parse_args()


def permute_for_rotary(tensor, num_heads, per_head_hidden_size, hidden_size):
    return (
        tensor.view(num_heads, 2, per_head_hidden_size // 2, hidden_size)
        .transpose(1, 2)
        .contiguous()
        .view(num_heads * per_head_hidden_size, hidden_size)
    )


def get_transformers_weight(
    name: str, ref_module_state_dict: Dict[str, torch.Tensor], ref_module: LlamaForCausalLM, get_grad: bool = False
) -> torch.Tensor:
    """From our brrr implementation, we get the equivalent tensor in transformers implementation"""
    config = ref_module.config
    brrr_prefix = "model."
    assert name.startswith(brrr_prefix)
    name = name[len(brrr_prefix) :]

    path = name.split(".")
    path.remove("pp_block")
    name = ".".join(path)

    if get_grad is False:

        def get_tensor(path: str):
            return ref_module_state_dict[path]

        def get_tensors(path: List[str]):
            return [get_tensor(p) for p in path]

    else:

        def get_tensor(path: str):
            weight = ref_module.get_parameter(path)
            return weight.grad

        def get_tensors(path: List[str]):
            return [get_tensor(p) for p in path]

    if name == "token_position_embeddings.token_embedding.weight":
        return get_tensor("model.embed_tokens.weight")

    elif name == "lm_head.weight":
        # This only used when weights are not shared
        return get_tensor("lm_head.weight")

    elif name == "final_layer_norm.weight":
        return get_tensor("model.norm.weight")

    if path[0] == "decoder":
        transformer_path = ["model"] + ["layers"] + [path[1]]

        if path[2] == "attn":
            path[2] = "self_attn"

        if path[2] == "ff":
            path[2] = "mlp"

        if path[3] == "qkv_proj":
            proj_names = ["q_proj", "k_proj", "v_proj"]
            tensor_list = get_tensors(
                [".".join(transformer_path + path[2:3] + [proj_name] + path[4:]) for proj_name in proj_names]
            )
            # Permute q/k
            per_head_hidden_size = config.hidden_size // config.num_attention_heads
            # Permute q
            print(f"Permuting q {tensor_list[0].shape}")
            tensor_list[0] = permute_for_rotary(
                tensor=tensor_list[0],
                num_heads=config.num_attention_heads,
                per_head_hidden_size=per_head_hidden_size,
                hidden_size=config.hidden_size,
            )
            # Permute k
            print(f"Permuting k {tensor_list[1].shape}")
            tensor_list[1] = permute_for_rotary(
                tensor=tensor_list[1],
                num_heads=config.num_key_value_heads,
                per_head_hidden_size=per_head_hidden_size,
                hidden_size=config.hidden_size,
            )
            return torch.cat(tensor_list, dim=0)

        if path[3] == "gate_up_proj":
            tensor_list = get_tensors(
                [
                    ".".join(transformer_path + path[2:3] + [proj_name] + path[4:])
                    for proj_name in ["gate_proj", "up_proj"]
                ]
            )
            return torch.cat(tensor_list, dim=0)

        return get_tensor(".".join(transformer_path + path[2:]))

    else:
        raise ValueError(f"Couldn't find transformer equivalent of {name}")


def convert_trfrs_to_brrr(dp, pp, tp, model_name="huggyllama/llama-7b", save_path="pretrained/llama-7b"):
    # check save_path doesnt exist or is empty
    save_path = Path(save_path)
    assert not save_path.exists() or len(list(save_path.iterdir())) == 0, f"save_path {save_path} is not empty"

    parallel_config = ParallelismArgs(
        dp=dp,
        pp=pp,
        tp=tp,
        # pp_engine=OneForwardOneBackwardPipelineEngine(),
        pp_engine=AllForwardAllBackwardPipelineEngine(),
        tp_mode=TensorParallelLinearMode.ALL_REDUCE,
        recompute_granularity=RecomputeGranularity.SELECTIVE,
        tp_linear_async_communication=True,
    )

    # Initialise all process groups
    dpg = get_process_groups(
        data_parallel_size=parallel_config.dp,
        pipeline_parallel_size=parallel_config.pp,
        tensor_parallel_size=parallel_config.tp,
    )
    # params
    torch.device("cuda")
    dtype = torch.bfloat16  # Flash attention doesn't support fp32

    # Initialise brrr model
    config: LlamaConfig = LlamaConfig.from_pretrained(model_name)
    model: LlamaForTraining = init_model(
        model_builder=lambda: LlamaForTraining(config=config, dpg=dpg, parallel_config=parallel_config),
        model_config=config,
        parallel_config=parallel_config,
        dtype=dtype,
        dpg=dpg,
        make_ddp=False,
    )

    # Initialise transformers model
    device_map = {}
    current_pp_rank = dist.get_rank(group=dpg.pp_pg)
    device_map["model.embed_tokens"] = (
        model.model.token_position_embeddings.rank
        if current_pp_rank == model.model.token_position_embeddings.rank
        else "meta"
    )
    for i in range(config.num_hidden_layers):
        device_map[f"model.layers.{i}"] = (
            model.model.decoder[i].rank if current_pp_rank == model.model.decoder[i].rank else "meta"
        )
    device_map["model.norm"] = (
        model.model.final_layer_norm.rank if current_pp_rank == model.model.final_layer_norm.rank else "meta"
    )
    device_map["lm_head"] = model.model.lm_head.rank if current_pp_rank == model.model.lm_head.rank else "meta"
    model_ref = LlamaForCausalLM.from_pretrained(model_name, torch_dtype=dtype, device_map=device_map)

    # Sync weights
    ref_state_dict = model_ref.state_dict()
    for name, param in model.named_parameters():
        print(f"Syncing {name}")
        ref_param = get_transformers_weight(name=name, ref_module_state_dict=ref_state_dict, ref_module=model_ref)

        param_is_tp_sharded = (
            isinstance(param, BRRRParameter)
            and param.is_sharded
            and dpg.world_ranks_to_pg[param.get_sharded_info().global_ranks] == dpg.tp_pg
        )

        if param_is_tp_sharded:
            sharded_info = param.get_sharded_info()
            # copy param data (not just the reference)
            with torch.no_grad():
                for local_global_slices_pair in sharded_info.local_global_slices_pairs:
                    local_slices = local_global_slices_pair.local_slices
                    global_slices = local_global_slices_pair.global_slices
                    param[local_slices].copy_(ref_param[global_slices])
        else:
            assert (
                ref_param.shape == param.shape
            ), f"Parameter shape don't match for {name}\n{ref_param.shape} != {param.shape}"
            # copy param data (not just the reference)
            with torch.no_grad():
                param.copy_(ref_param)

    # TODO @nouamanetazi: assert weights are the same

    save_weights(model=model, dpg=dpg, root_folder=save_path)
    checkpoint_metadata = {
        "last_train_step": 0,
        "consumed_train_samples": 0,
    }
    save_meta(root_folder=save_path, dpg=dpg, checkpoint_metadata=checkpoint_metadata)


def main():
    args = get_args()
    convert_trfrs_to_brrr(**vars(args))


if __name__ == "__main__":
    main()
