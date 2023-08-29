from typing import Dict

import torch
from config import ModelArgs, ParallelismArgs, RandomInit, RecomputeGranularity
from generation import GenerationConfig, GenerationInput, greedy_search
from main import _vocab_size_with_padding, init_model
from torch import nn
from torch.nn.parallel import DistributedDataParallel
from transformers import AutoConfig, AutoTokenizer, GPTBigCodeForCausalLM

from brrr.core import distributed as dist
from brrr.core.parallelism.parameters import BRRRParameter
from brrr.core.parallelism.pipeline_parallelism.engine import (
    OneForwardOneBackwardPipelineEngine,
)
from brrr.core.parallelism.pipeline_parallelism.tensor_pointer import TensorPointer
from brrr.core.parallelism.tensor_parallelism.enum import TensorParallelLinearMode
from brrr.core.parallelism.tied_parameters import sync_tied_weights_gradients
from brrr.core.process_groups_initializer import get_process_groups
from brrr.core.random import set_random_seed


def get_transformers_weight(
    name: str, ref_module_state_dict: Dict[str, torch.Tensor], ref_module: nn.Module, get_grad: bool = False
) -> torch.Tensor:
    """From our brrr implementation, we get the equivalent tensor in transformers implementation"""
    brrr_prefix = "model."
    assert name.startswith(brrr_prefix)
    name = name[len(brrr_prefix) :]

    path = name.split(".")
    path.remove("pp_block")
    name = ".".join(path)

    if get_grad is False:

        def get_tensor(path: str):
            return ref_module_state_dict[path]

    else:

        def get_tensor(path: str):
            weight = ref_module.get_parameter(path)
            return weight.grad

    if name == "token_position_embeddings.token_embedding.weight":
        return get_tensor("transformer.wte.weight")

    elif name == "token_position_embeddings.position_embedding.weight":
        return get_tensor("transformer.wpe.weight")

    elif name == "lm_head.weight":
        # This only used when weights are not shared
        return get_tensor("lm_head.weight")

    elif name == "final_layer_norm.weight":
        return get_tensor("transformer.ln_f.weight")
    elif name == "final_layer_norm.bias":
        return get_tensor("transformer.ln_f.bias")

    # self attention q: 'module.model.decoder.0.pp_block.attn.q.weight'
    # now we have 'decoder.0.attn.qkv.q.weight' -> 'transformer.h.0.attn.c_attn.weight'
    if path[0] == "decoder":
        transformer_path = ["transformer"] + ["h"] + [path[1]]
        if path[3] == "qkv":
            path[3] = "c_attn"
            return get_tensor(".".join(transformer_path + path[2:4] + path[5:]))

        if path[3] == "o":
            path[3] = "c_proj"

        if path[2] == "ff":
            path[2] = "mlp"

        return get_tensor(".".join(transformer_path + path[2:]))

    else:
        raise ValueError(f"Couldn't find transformer equivalent of {name}")


def test_gpt2():
    parallel_config = ParallelismArgs(
        dp=1,
        pp=2,
        tp=2,
        pp_engine=OneForwardOneBackwardPipelineEngine(),
        tp_mode=TensorParallelLinearMode.ALL_REDUCE,
        tp_linear_async_communication=False,
        recompute_granularity=RecomputeGranularity.SELECTIVE,
    )
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

    # data params
    micro_batch_size = 2
    sequence_length = 2048

    # Initialise brrr model
    model_name = "bigcode/gpt_bigcode-santacoder"
    trfs_model_config = AutoConfig.from_pretrained(model_name, trust_remote_code=True)
    # Initialise brrr model
    config = ModelArgs(
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

    config.vocab_size = _vocab_size_with_padding(
        config.vocab_size, pg_size=dpg.tp_pg.size(), make_vocab_size_divisible_by=1
    )

    model, random_states = init_model(
        model_config=config,
        parallel_config=parallel_config,
        dtype=dtype,
        dpg=dpg,
        # TODO @thomasw21: Figure out why using DDP with accumulate_in_fp_32 and ZeRO-1 performs poorly.
        make_ddp=True,
    )

    # Initialise transformers GPTBigCode model
    set_random_seed(seed)  # Important to sync weights across processes
    model_ref = GPTBigCodeForCausalLM.from_pretrained(model_name)
    # TODO @nouamanetazi: Remove once we're able to compare dropouts between brrr and transformers
    model.eval()
    model_ref.eval()
    model_ref.to(device=device, dtype=dtype)

    if isinstance(model, DistributedDataParallel):
        # Remove the annoying "module." prefix
        normalized_model = model.module
    else:
        normalized_model = model

    ref_state_dict = model_ref.state_dict()
    for name, param in normalized_model.named_parameters():
        ref_param = get_transformers_weight(name=name, ref_module_state_dict=ref_state_dict, ref_module=model_ref)

        param_is_tp_sharded = (
            isinstance(param, BRRRParameter)
            and param.is_sharded
            and dpg.world_ranks_to_pg[param.get_sharded_info().global_ranks] == dpg.tp_pg
        )
        if ".attn.qkv.q.weight" in name or ".attn.qkv.q.bias" in name:
            ref_param = ref_param[: config.hidden_size, ...]
        if ".attn.qkv.kv.weight" in name or ".attn.qkv.kv.bias" in name:
            ref_param = ref_param[config.hidden_size :, ...]

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
    # Shard the micro batch across PP
    micro_batch = micro_batch_ref.copy()
    if dist.get_rank(dpg.pp_pg) != normalized_model.model.token_position_embeddings.rank:
        micro_batch["input_ids"] = TensorPointer(group_rank=normalized_model.model.token_position_embeddings.rank)
        micro_batch["input_mask"] = TensorPointer(group_rank=normalized_model.model.token_position_embeddings.rank)

    if dist.get_rank(dpg.pp_pg) != normalized_model.loss.rank:
        micro_batch["label_ids"] = TensorPointer(group_rank=normalized_model.loss.rank)
        micro_batch["label_mask"] = TensorPointer(group_rank=normalized_model.loss.rank)

    assert next(model.parameters()).grad is None
    outputs = parallel_config.pp_engine.train_batch_iter(
        model=model, pg=dpg.pp_pg, batch=[micro_batch], grad_accumulator=None
    )
    assert next(model.parameters()).grad is not None

    output_ref = model_ref(input_ids=micro_batch_ref["input_ids"], attention_mask=micro_batch_ref["input_mask"])
    lm_logits = output_ref.logits
    loss_fct = nn.CrossEntropyLoss(ignore_index=-100, reduction="none")
    loss = loss_fct(
        lm_logits.view(micro_batch_size * sequence_length, config.vocab_size),
        micro_batch_ref["label_ids"].view(micro_batch_size * sequence_length),
    ).view(micro_batch_size, sequence_length)
    masked_loss = loss[micro_batch_ref["label_mask"]]
    ref_loss = masked_loss.mean()
    assert next(model_ref.parameters()).grad is None
    ref_loss.backward()
    assert next(model_ref.parameters()).grad is not None

    # Only the last pipeline stage has the output
    if dist.get_rank(dpg.pp_pg) == dpg.pp_pg.size() - 1:
        # Check loss
        brrr_loss = next(iter(outputs)).to(dtype)  # We cast original loss in the correct precision
        trfs_loss = ref_loss
        try:
            torch.testing.assert_close(brrr_loss, trfs_loss)
            print(f"Losses match: {brrr_loss} == {ref_loss}")
        except Exception as e:
            print(f"Losses don't match: {brrr_loss} != {ref_loss}")
            raise e

    dist.barrier()

    # Test generation
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"
    dummy_inputs = [
        "def fibonacci(",
    ] * 8

    outputs = greedy_search(
        input_iter=(GenerationInput(text=text) for text in dummy_inputs),
        tokenizer=tokenizer,
        # TODO @thomasw21: From ModelWithLoss extract the model.
        model=normalized_model.model,
        # TODO @thomasw21: Figure out how to pass p2p.
        p2p=normalized_model.model.p2p,
        dpg=dpg,
        generation_config=GenerationConfig(max_new_tokens=20),
        max_micro_batch_size=8,
    )

    # Generation for model_ref
    model_ref_inputs = tokenizer(dummy_inputs, return_tensors="pt", return_attention_mask=True, padding=True)
    model_ref_inputs.attention_mask = model_ref_inputs.attention_mask.to(dtype=torch.bool, device="cuda")
    model_ref_inputs.to("cuda")
    model_ref_outputs = model_ref.generate(**model_ref_inputs, max_new_tokens=20)
    model_ref_output_texts = tokenizer.batch_decode(model_ref_outputs, clean_up_tokenization_spaces=False)

    for output, model_ref_output_text in zip(outputs, model_ref_output_texts):
        input_ids = output.input_ids
        generated_ids = output.generation_ids
        if isinstance(input_ids, TensorPointer):
            assert isinstance(generated_ids, TensorPointer)
            continue
        assert isinstance(generated_ids, torch.Tensor)
        output_text = tokenizer.decode(generated_ids, clean_up_tokenization_spaces=False)
        print(
            {
                "input": tokenizer.decode(input_ids, clean_up_tokenization_spaces=False),
                "generation": output_text,
            }
        )
        assert output_text == model_ref_output_text, f"Output text don't match\n{output_text}\n{model_ref_output_text}"

    dist.barrier()

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

        if ".attn.qkv.q.weight" in name or ".attn.qkv.q.bias" in name:
            ref_param_grad = ref_param_grad[: config.hidden_size, ...]
        if ".attn.qkv.kv.weight" in name or ".attn.qkv.kv.bias" in name:
            ref_param_grad = ref_param_grad[config.hidden_size :, ...]

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
                print(f"Gradients are close at {name}", torch.isclose(ref_param_grad, param.grad).all())


if __name__ == "__main__":
    test_gpt2()
