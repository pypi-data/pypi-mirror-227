"""
This module tests the correctness of our llama implementation by comparing it with the transformers implementation.

For llama:
    Quick test:
        CUDA_DEVICE_MAX_CONNECTIONS=1 torchrun --nproc_per_node=4 examples/llama/test_llama.py --dp 1 --pp 1 --tp 4
    Exact match, real setup:
        CUDA_DEVICE_MAX_CONNECTIONS=1 torchrun --nproc_per_node=1 examples/llama/test_llama.py --dp 1 --pp 1 --tp 1 --compare_logits --from_pretrained
For llama-v2:
    Quick test:
        CUDA_DEVICE_MAX_CONNECTIONS=1 torchrun --nproc_per_node=4 examples/llama/test_llama.py --dp 1 --pp 1 --tp 4 --v2
    Exact match, real setup:
        CUDA_DEVICE_MAX_CONNECTIONS=1 torchrun --nproc_per_node=1 examples/llama/test_llama.py --dp 1 --pp 1 --tp 1 --compare_logits --from_pretrained --v2
"""
import argparse
import os
from typing import Dict, List

import torch
from config import ParallelismArgs, RecomputeGranularity
from generation import GenerationConfig, GenerationInput, TokenizerConfig, greedy_search
from torch import nn
from torch.nn.parallel import DistributedDataParallel
from train import _vocab_size_with_padding, init_model
from transformers import AutoTokenizer, LlamaConfig, LlamaForCausalLM

import brrr.core.distributed as dist
from brrr.core.parallelism.parameters import BRRRParameter
from brrr.core.parallelism.pipeline_parallelism.engine import (
    AllForwardAllBackwardPipelineEngine,
)
from brrr.core.parallelism.pipeline_parallelism.tensor_pointer import TensorPointer
from brrr.core.parallelism.tensor_parallelism.nn import TensorParallelLinearMode
from brrr.core.parallelism.tied_parameters import sync_tied_weights_gradients
from brrr.core.process_groups_initializer import get_process_groups
from brrr.core.random import set_random_seed

if os.environ.get("USE_FAST"):
    # We import the fast versions
    from modeling_llama_fast import LlamaForTraining
else:
    from modeling_llama import LlamaForTraining


def get_args():
    parser = argparse.ArgumentParser(description="Test llama model")
    parser.add_argument("--from_pretrained", action="store_true")
    parser.add_argument("--compare_logits", action="store_true")
    parser.add_argument("--v2", action="store_true")
    parser.add_argument("--dp", type=int, default=1)
    parser.add_argument("--pp", type=int, default=1)
    parser.add_argument("--tp", type=int, default=2)
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
            tensor_list[0] = permute_for_rotary(
                tensor=tensor_list[0],
                num_heads=config.num_attention_heads,
                per_head_hidden_size=per_head_hidden_size,
                hidden_size=config.hidden_size,
            )
            # Permute k
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


def test_correctness(from_pretrained=False, compare_logits=False, v2=False, dp=1, pp=1, tp=2):
    """Compare brrr and transformers implementations of llama model

    Args:
        from_pretrained (bool, optional): Whether to use a pretrained model and a real input.
        compare_logits (bool, optional): Whether to compare logits. If False, only compares the loss. Make sure to set TP=1.
    """
    parallel_config = ParallelismArgs(
        dp=dp,
        pp=pp,
        tp=tp,
        # pp_engine=OneForwardOneBackwardPipelineEngine(),
        pp_engine=AllForwardAllBackwardPipelineEngine(),
        tp_mode=TensorParallelLinearMode.ALL_REDUCE,
        recompute_granularity=RecomputeGranularity.SELECTIVE,
        tp_linear_async_communication=False,
    )
    if compare_logits:
        assert parallel_config.pp == 1, "Logits comparison only supported with pp=1"

    # Initialise all process groups
    dpg = get_process_groups(
        data_parallel_size=parallel_config.dp,
        pipeline_parallel_size=parallel_config.pp,
        tensor_parallel_size=parallel_config.tp,
    )
    # params
    device = torch.device("cuda")
    dtype = torch.bfloat16  # Flash attention doesn't support fp32
    seed = 42

    # Initialise brrr model
    if v2:
        model_name = "meta-llama/Llama-2-7b-hf" if from_pretrained else "HuggingFaceBR4/tiny-random-llama-v2"
    else:
        model_name = "huggyllama/llama-7b" if from_pretrained else "HuggingFaceBR4/tiny-random-llama"
    config: LlamaConfig = LlamaConfig.from_pretrained(model_name)

    config.vocab_size = _vocab_size_with_padding(
        config.vocab_size, pg_size=dpg.tp_pg.size(), make_vocab_size_divisible_by=1
    )

    model: LlamaForTraining = init_model(
        model_builder=lambda: LlamaForTraining(config=config, dpg=dpg, parallel_config=parallel_config),
        model_config=config,
        parallel_config=parallel_config,
        dtype=dtype,
        dpg=dpg,
        make_ddp=True,
    )

    # Initialise transformers model
    set_random_seed(seed)  # Important to sync weights across processes
    if not from_pretrained:
        model_ref = LlamaForCausalLM._from_config(config)
    else:
        model_ref = LlamaForCausalLM.from_pretrained(model_name, torch_dtype=dtype)
    # TODO @nouamanetazi: Remove once we're able to compare dropouts between brrr and transformers
    model.eval()
    model_ref.eval()
    model_ref.to(device=device, dtype=dtype)

    if isinstance(model, DistributedDataParallel):
        # Remove the annoying "module." prefix
        normalized_model = model.module
    else:
        normalized_model = model

    # Sync weights
    ref_state_dict = model_ref.state_dict()
    for name, param in normalized_model.named_parameters():
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

    if not from_pretrained:
        # data params
        micro_batch_size = 2
        sequence_length = 2048

        # Create dummy micro batch
        micro_batch_ref = {
            "input_ids": torch.randint(
                0,
                config.vocab_size,
                (micro_batch_size, sequence_length),
                dtype=torch.long,
                device="cuda",
            ),
            "input_mask": torch.ones(
                micro_batch_size,
                sequence_length,
                device="cuda",
            )
            > 0.5,
            "label_ids": torch.randint(
                0,
                config.vocab_size,
                (micro_batch_size, sequence_length),
                dtype=torch.long,
                device="cuda",
            ),
            "label_mask": torch.ones(
                micro_batch_size,
                sequence_length,
                device="cuda",
            )
            > 0.5,
        }
    else:
        input_texts = [
            """If the crew behind \'Zombieland\' had a sequel in mind, it would be \'Zombieland: Double Tap.\'\n\'Zombieland\' Sequel in the Works\nThe 2009 zombie comedy "Zombieland" is getting a sequel.\nThe original film, which starred Woody Harrelson, Jesse Eisenberg, Emma Stone and Abigail Breslin, was a box office hit, grossing $75 million domestically and $102 million worldwide.\nThe film\'s director, Ruben Fle"""
        ]
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        micro_batch_ref = {}
        tokenizer.pad_token = tokenizer.eos_token
        input_ids = tokenizer(input_texts, return_tensors="pt", padding=True).input_ids
        micro_batch_ref["input_ids"] = input_ids[:, :-1]
        micro_batch_ref["input_mask"] = input_ids[:, :-1] != tokenizer.pad_token_id
        micro_batch_ref["label_ids"] = input_ids[:, 1:].clone()
        micro_batch_ref["label_mask"] = input_ids[:, 1:] != tokenizer.pad_token_id

        outputs = greedy_search(
            input_iter=(GenerationInput(text=text) for text in input_texts),
            tokenizer=tokenizer,
            # TODO @thomasw21: From ModelWithLoss extract the model.
            model=model.module.model,
            # TODO @thomasw21: Figure out how to pass p2p.
            p2p=model.module.model.p2p,
            dpg=dpg,
            generation_config=GenerationConfig(max_new_tokens=10, max_micro_batch_size=8),
            tokenizer_config=TokenizerConfig(max_input_length=8),
        )
        dist.barrier()
        # TODO(kunhao): Add generation result for future debugging.
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

    position_ids = micro_batch_ref["input_mask"].long().cumsum(-1) - 1
    position_ids.masked_fill_(micro_batch_ref["input_mask"] == 0, 0)

    micro_batch_size, sequence_length = micro_batch_ref["input_ids"].shape
    micro_batch_ref = {k: v.to(device) for k, v in micro_batch_ref.items()}

    # Shard the micro batch across PP
    micro_batch = micro_batch_ref.copy()
    if dist.get_rank(dpg.pp_pg) != normalized_model.model.token_position_embeddings.rank:
        micro_batch["input_ids"] = TensorPointer(group_rank=normalized_model.model.token_position_embeddings.rank)
        micro_batch["input_mask"] = TensorPointer(group_rank=normalized_model.model.token_position_embeddings.rank)

    if dist.get_rank(dpg.pp_pg) != normalized_model.loss.rank:
        micro_batch["label_ids"] = TensorPointer(group_rank=normalized_model.loss.rank)
        micro_batch["label_mask"] = TensorPointer(group_rank=normalized_model.loss.rank)

    def compute_loss(lm_logits):
        lm_logits = lm_logits.to(torch.float32)
        loss_fct = nn.CrossEntropyLoss(ignore_index=-100, reduction="none")
        losses = loss_fct(
            lm_logits.view(micro_batch_size * sequence_length, config.vocab_size),
            micro_batch_ref["label_ids"].view(micro_batch_size * sequence_length),
        ).view(micro_batch_size, sequence_length)
        return losses

    # BRRR Model:
    if compare_logits:
        # we only do a forward pass to compare logits
        del micro_batch["label_ids"]
        del micro_batch["label_mask"]
        sharded_logits = normalized_model.model(**micro_batch)  # (sequence_length, batch_size, vocab_size)
        # all gather logits across TP
        lm_logits = [torch.empty_like(sharded_logits) for _ in range(dpg.tp_pg.size())]
        dist.all_gather(lm_logits, sharded_logits.contiguous(), group=dpg.tp_pg)
        lm_logits = torch.cat(lm_logits, dim=-1)  # [sequence_length, batch_size, vocab_size]
        lm_logits = lm_logits.transpose(0, 1).contiguous()  # [batch_size, sequence_length, vocab_size]
        losses = compute_loss(lm_logits)
        loss = losses[micro_batch_ref["label_mask"]].mean()
    else:
        # fwd + bwd using pipeline engine
        outputs = parallel_config.pp_engine.train_batch_iter(
            model=model, pg=dpg.pp_pg, batch=[micro_batch], grad_accumulator=None
        )
        assert next(model.parameters()).grad is not None
        loss = next(iter(outputs))

    # Transformers Model: Forward + Bwd pass
    output_ref = model_ref(
        input_ids=micro_batch_ref["input_ids"], attention_mask=micro_batch_ref["input_mask"], position_ids=position_ids
    )
    lm_logits_ref = output_ref.logits.to(torch.float32)
    ref_losses = compute_loss(lm_logits_ref)
    ref_loss = ref_losses[micro_batch_ref["label_mask"]].mean()
    assert next(model_ref.parameters()).grad is None
    ref_loss.backward()
    assert next(model_ref.parameters()).grad is not None

    # Only the last pipeline stage has the output
    if dist.get_rank(dpg.pp_pg) == dpg.pp_pg.size() - 1:
        if compare_logits is True:
            # Check logits
            try:
                torch.testing.assert_close(lm_logits, lm_logits_ref)
                print(f"Logits match. Absolute error: {torch.abs(lm_logits - lm_logits_ref).max()}")
                print(lm_logits, flush=True)
                print(lm_logits_ref, flush=True)
            except Exception:
                print(f"Logits don't match. Absolute error: {torch.abs(lm_logits - lm_logits_ref).max()}")
                print(lm_logits, flush=True)
                print(lm_logits_ref, flush=True)

            # Check losses
            try:
                torch.testing.assert_close(losses, ref_losses)
                print(f"Losses match: {losses} == {ref_losses}", flush=True)
            except Exception:
                print(f"Losses don't match: {losses} != {ref_losses}", flush=True)

        # Check loss
        try:
            torch.testing.assert_close(loss, ref_loss)
            print(f"Losses match: {loss} == {ref_loss}", flush=True)
        except Exception:
            print(f"Losses don't match: {loss} != {ref_loss}", flush=True)

    if compare_logits is True:
        # grads are not defined
        return

    # Manually sync tied parameters
    sync_tied_weights_gradients(module=normalized_model, dpg=dpg, grad_accumulator=None)

    # Test grads of the last DecoderBlock
    for name, param in reversed(list(normalized_model.named_parameters())):
        ref_param_grad = get_transformers_weight(
            name=name, ref_module_state_dict=ref_state_dict, ref_module=model_ref, get_grad=True
        )

        param_is_tp_sharded = (
            isinstance(param, BRRRParameter)
            and param.is_sharded
            and dpg.world_ranks_to_pg[param.get_sharded_info().global_ranks] == dpg.tp_pg
        )
        assert not torch.any(torch.isnan(ref_param_grad)), f"Reference gradient at {name} has Nan, not sure why"
        assert not torch.any(torch.isnan(param.grad)), f"Gradient at {name} has Nan, not sure why"

        if dist.get_rank(dpg.dp_pg) == 0:
            if param_is_tp_sharded:
                sharded_info = param.get_sharded_info()
                print(
                    f"Gradients are close at {name}",
                    all(
                        torch.isclose(
                            ref_param_grad[local_global_slices_pair.global_slices],
                            param.grad[local_global_slices_pair.local_slices],
                        ).all()
                        for local_global_slices_pair in sharded_info.local_global_slices_pairs
                    ),
                )
            else:
                print(f"Gradients are close at {name}", torch.isclose(ref_param_grad, param.grad).all(), flush=True)


def main():
    args = get_args()
    test_correctness(**vars(args))


if __name__ == "__main__":
    main()
