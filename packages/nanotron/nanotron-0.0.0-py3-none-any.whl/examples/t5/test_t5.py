from typing import Dict

import torch
from dataclass import TrainingModelArgs
from generation import GenerationConfig, GenerationInput, greedy_search
from main import init_model
from torch import nn
from torch.nn.parallel import DistributedDataParallel
from transformers import AutoConfig, AutoTokenizer, T5ForConditionalGeneration

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

    if name == "encoder_embedding.weight":
        return get_tensor("encoder.embed_tokens.weight")

    elif name == "decoder_embedding.weight":
        return get_tensor("decoder.embed_tokens.weight")

    elif name == "lm_head.weight":
        return get_tensor("lm_head.weight")

    elif name == "encoder_final_layer_norm.weight":
        return get_tensor("encoder.final_layer_norm.weight")

    elif name == "decoder_final_layer_norm.weight":
        return get_tensor("decoder.final_layer_norm.weight")

    # self attention qkv : 'model.decoder.7.self_attention_pp_block.qkv.weight' -> 'decoder.block.7.layer.0.SelfAttention.v.weight'
    if path[2] == "self_attention_pp_block":
        transformer_path = path[:1] + ["block"] + path[1:2] + ["layer", "0"]
        # layer norms
        if path[3] == "layer_norm":
            return get_tensor(".".join(transformer_path + ["layer_norm", path[-1]]))

        transformer_path = transformer_path + ["SelfAttention"]
        if path[-2] == "qkv":
            key_weight_path = ".".join(transformer_path + ["k", "weight"])
            query_weight_path = ".".join(transformer_path + ["q", "weight"])
            value_weight_path = ".".join(transformer_path + ["v", "weight"])

            key_weight = get_tensor(key_weight_path)
            query_weight = get_tensor(query_weight_path)
            value_weight = get_tensor(value_weight_path)

            return torch.cat([query_weight, key_weight, value_weight], dim=0)
        elif path[-2] == "o":
            return get_tensor(".".join(transformer_path + path[-2:]))
        elif path[-2] == "relative_attention_bias":
            # `transformers` T5 implementation only puts bias on the first layed id.
            transformer_path[2] = "0"
            # There's a duplicate `relative_attention_bias.relative_attention_bias`
            return get_tensor(".".join(transformer_path + path[-2:]))
        else:
            raise ValueError(f"Couldn't find transformer equivalent of {name}")

    # cross attention kv : 'decoder.7.cross_attention_pp_block.kv.weight' -> 'decoder.block.7.layer.1.EncDecAttention.v.weight'
    elif path[2] == "cross_attention_pp_block":
        transformer_path = path[:1] + ["block"] + path[1:2] + ["layer", "1"]

        # layer norms
        if path[3] == "layer_norm":
            return get_tensor(".".join(transformer_path + ["layer_norm", path[-1]]))

        # qkvo
        transformer_path = transformer_path + ["EncDecAttention"]
        if path[-2] == "kv":
            key_weight_path = ".".join(transformer_path + ["k", "weight"])
            value_weight_path = ".".join(transformer_path + ["v", "weight"])

            # TODO @thomasw21: That's actually interleaved, so I need to get a `[num_heads, head_dim, in_features]` segmentation
            key_weight = get_tensor(key_weight_path)
            value_weight = get_tensor(value_weight_path)

            return torch.cat([key_weight, value_weight], dim=0)
        elif path[-2] in ["q", "o"]:
            return get_tensor(".".join(transformer_path + path[-2:]))
        else:
            raise ValueError(f"Couldn't find transformer equivalent of {name}")

    elif path[2] == "ff_block":
        block_has_cross_attention = path[0] == "decoder"
        transformer_path = (
            path[:1] + ["block"] + path[1:2] + ["layer", "2" if block_has_cross_attention else "1"] + path[3:]
        )
        return get_tensor(".".join(transformer_path))

    else:
        raise ValueError(f"Couldn't find transformer equivalent of {name}")


def test_t5():
    # Initialise all process groups
    dpg = get_process_groups(
        data_parallel_size=1,
        pipeline_parallel_size=2,
        tensor_parallel_size=2,
    )
    # params
    device = torch.device("cuda")
    dtype = torch.float32
    pipeline_engine = OneForwardOneBackwardPipelineEngine()
    seed = 42

    # data params
    micro_batch_size = 2
    input_sequence_length = 512
    target_sequence_length = 114

    # Initialise brrr T5 model
    model_name = "google/t5-v1_1-xl"
    config = AutoConfig.from_pretrained(model_name)

    # TODO @nouamanetazi: Remove once we're able to compare dropouts between brrr and transformers
    config.dropout_rate = 0.0
    training_model_args = TrainingModelArgs(recompute_mode="selective", tp_mode=TensorParallelLinearMode.ALL_REDUCE)
    model, random_states = init_model(
        config=config, dtype=dtype, dpg=dpg, training_model_args=training_model_args, make_ddp=False
    )

    # Initialise transformers T5 model
    set_random_seed(seed)  # Important to sync weights across processes
    model_ref = T5ForConditionalGeneration.from_pretrained(model_name)
    model_ref.to(device=device, dtype=dtype)

    ref_state_dict = model_ref.state_dict()

    if isinstance(model, DistributedDataParallel):
        # Remove the annoying "module." prefix
        normalized_model = model.module
    else:
        normalized_model = model

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

    # Check that we can generate with that same model
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
    dummy_inputs = [
        "Hello my name is <extra_id_0>",  # generates "'<pad><extra_id_0>.</s>'"
        "My dog is the sweetest thing. Please <extra_id_0> care of it.",  # generates "'<pad><extra_id_0> take<extra_id_1>..??</s>'"
    ] * 8
    assert config.decoder_start_token_id is not None
    model.eval()
    outputs = greedy_search(
        input_iter=(GenerationInput(text=text) for text in dummy_inputs),
        tokenizer=tokenizer,
        # TODO @thomasw21: From DDP extract the underlying model
        model=normalized_model.model,
        decoder_start_token_id=config.decoder_start_token_id,
        # TODO @thomasw21: Figure out how to pass p2p.
        p2p=normalized_model.model.p2p,
        generation_config=GenerationConfig(max_new_tokens=20),
        max_micro_batch_size=2,
        dpg=dpg,
    )
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

    model.train()
    # Create dummy micro batch
    decoder_input_mask = (
        torch.rand(
            micro_batch_size,
            target_sequence_length,
            device="cuda",
        )
        < 0.5
    )
    micro_batch_ref = {
        "encoder_input_ids": torch.randint(
            0,
            config.vocab_size,
            (micro_batch_size, input_sequence_length),
            dtype=torch.long,
            device="cuda",
        ),
        "encoder_input_mask": torch.rand(
            micro_batch_size,
            input_sequence_length,
            device="cuda",
        )
        < 0.5,
        "decoder_input_ids": torch.randint(
            0,
            config.vocab_size,
            (micro_batch_size, target_sequence_length),
            dtype=torch.long,
            device="cuda",
        ),
        "decoder_input_mask": decoder_input_mask,
        "decoder_label_ids": torch.randint(
            0,
            config.vocab_size,
            (micro_batch_size, target_sequence_length),
            dtype=torch.long,
            device="cuda",
        ),
        "decoder_label_mask": decoder_input_mask,
    }
    # Shard the micro batch across PP
    micro_batch = micro_batch_ref.copy()
    if dist.get_rank(dpg.pp_pg) != normalized_model.model.encoder_embedding.rank:
        micro_batch["encoder_input_ids"] = TensorPointer(group_rank=normalized_model.model.encoder_embedding.rank)
        micro_batch["encoder_input_mask"] = TensorPointer(group_rank=normalized_model.model.encoder_embedding.rank)

    if dist.get_rank(dpg.pp_pg) != normalized_model.model.decoder_embedding.rank:
        micro_batch["decoder_input_ids"] = TensorPointer(group_rank=normalized_model.model.decoder_embedding.rank)
        micro_batch["decoder_input_mask"] = TensorPointer(group_rank=normalized_model.model.decoder_embedding.rank)

    if dist.get_rank(dpg.pp_pg) != normalized_model.loss.rank:
        micro_batch["decoder_label_ids"] = TensorPointer(group_rank=normalized_model.loss.rank)
        micro_batch["decoder_label_mask"] = TensorPointer(group_rank=normalized_model.loss.rank)

    assert next(model.parameters()).grad is None
    outputs = pipeline_engine.train_batch_iter(model=model, pg=dpg.pp_pg, batch=[micro_batch], grad_accumulator=None)
    assert next(model.parameters()).grad is not None

    output_ref = model_ref(
        input_ids=micro_batch_ref["encoder_input_ids"],
        attention_mask=micro_batch_ref["encoder_input_mask"],
        decoder_input_ids=micro_batch_ref["decoder_input_ids"],
        decoder_attention_mask=micro_batch_ref["decoder_input_mask"],
    )
    # transformers T5 loss doesn't apply correct mask so we need to do this for now: https://github.com/huggingface/transformers/blob/820c46a707ddd033975bc3b0549eea200e64c7da/src/transformers/models/t5/modeling_t5.py#L1689-L1694
    lm_logits = output_ref.logits
    # TODO @nouamanetazi: compare masked logits
    # masked_lm_logits = lm_logits[micro_batch_ref["decoder_input_mask"].bool()]
    loss_fct = nn.CrossEntropyLoss(ignore_index=-100, reduction="none")
    loss = loss_fct(
        lm_logits.view(micro_batch_size * target_sequence_length, config.vocab_size),
        micro_batch_ref["decoder_label_ids"].view(micro_batch_size * target_sequence_length),
    ).view(micro_batch_size, target_sequence_length)
    masked_loss = loss[micro_batch_ref["decoder_input_mask"]]
    ref_loss = masked_loss.sum()
    assert next(model_ref.parameters()).grad is None
    ref_loss.backward()
    assert next(model_ref.parameters()).grad is not None

    # Only the last pipeline stage has the output
    if dist.get_rank(dpg.pp_pg) == dpg.pp_pg.size() - 1:
        # Check loss
        # transformers T5 use CE loss with 'mean' reduction by default, while _ShardedCrossEntropy uses `sum`
        torch.testing.assert_close(next(iter(outputs)), ref_loss)
        print(f"Losses match: {next(iter(outputs))} == {ref_loss}")

    # Manually sync tied parameters
    sync_tied_weights_gradients(module=normalized_model, dpg=dpg, grad_accumulator=None)

    # Test grads of the last DecoderBlock
    for name, param in normalized_model.named_parameters():
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
                print(f"Gradients are close at {name}", torch.isclose(ref_param_grad, param.grad).all())


if __name__ == "__main__":
    test_t5()
