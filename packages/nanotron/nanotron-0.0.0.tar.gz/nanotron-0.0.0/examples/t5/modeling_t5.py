# coding=utf-8
# Copyright 2018 Mesh TensorFlow authors, T5 Authors and HuggingFace Inc. team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" PyTorch T5 model."""

import math
from functools import cache
from typing import Dict, Optional, Tuple, Union

import torch
from dataclass import TrainingModelArgs
from torch import nn
from transformers.activations import ACT2FN
from transformers.models.t5.configuration_t5 import T5Config

from brrr.core import distributed as dist
from brrr.core import logging
from brrr.core.dataclass import RandomStates
from brrr.core.parallelism.pipeline_parallelism.block import PipelineBlock, TensorPointer
from brrr.core.parallelism.pipeline_parallelism.p2p import P2P
from brrr.core.parallelism.sharded_parameters import SplitConfig, mark_all_parameters_in_module_as_sharded
from brrr.core.parallelism.tensor_parallelism.enum import TensorParallelLinearMode
from brrr.core.parallelism.tensor_parallelism.functional import sharded_cross_entropy
from brrr.core.parallelism.tensor_parallelism.nn import (
    TensorParallelColumnLinear,
    TensorParallelEmbedding,
    TensorParallelRowLinear,
)
from brrr.core.process_groups_initializer import DistributedProcessGroups
from brrr.core.random import branch_random_state
from brrr.core.utils import checkpoint_method
from brrr.store import AttachableStore

logger = logging.get_logger(__name__)


try:
    # TODO @thomasw21: https://github.com/huggingface/brrr/issues/98
    from apex.normalization import FusedRMSNorm as RMSNorm
except Exception:

    class RMSNorm(nn.Module):
        def __init__(self, normalized_shape, eps=1e-6):
            """
            Construct a layernorm module in the T5 style. No bias and no subtraction of mean.
            """
            super().__init__()
            self.weight = nn.Parameter(torch.ones(normalized_shape))
            self.variance_epsilon = eps

        def forward(self, input):

            # T5 uses a layer_norm which only scales and doesn't shift, which is also known as Root Mean
            # Square Layer Normalization https://arxiv.org/abs/1910.07467 thus varience is calculated
            # w/o mean and there is no bias. Additionally we want to make sure that the accumulation for
            # half-precision inputs is done in fp32

            # TODO @thomasw21: This is actually stupid, it launches too many kernels for a very simple task, maybe I just need to run `torch.optimize`, maybe we need to build our own.
            variance = input.to(torch.float32).pow(2).mean(-1, keepdim=True)
            input = input * torch.rsqrt(variance + self.variance_epsilon)

            # convert into half-precision if necessary
            if self.weight.dtype in [torch.float16, torch.bfloat16]:
                input = input.to(self.weight.dtype)

            return self.weight * input


class T5DenseActDense(nn.Module):
    def __init__(self, config: T5Config, training_model_args: Optional[TrainingModelArgs], tp_pg: dist.ProcessGroup):
        super().__init__()

        # TODO @thomasw21: refactor so that we store that default in a single place.
        tp_mode = (
            training_model_args.tp_mode if training_model_args is not None else TensorParallelLinearMode.ALL_REDUCE
        )

        self.wi = TensorParallelColumnLinear(config.d_model, config.d_ff, pg=tp_pg, mode=tp_mode, bias=False)
        self.wo = TensorParallelRowLinear(config.d_ff, config.d_model, pg=tp_pg, mode=tp_mode, bias=False)
        self.dropout = nn.Dropout(config.dropout_rate)
        self.act = ACT2FN[config.dense_act_fn]

    def forward(self, hidden_states):
        hidden_states = self.wi(hidden_states)
        hidden_states = self.act(hidden_states)
        hidden_states = self.dropout(hidden_states)
        hidden_states = self.wo(hidden_states)
        return hidden_states


class T5DenseGatedActDense(nn.Module):
    def __init__(self, config: T5Config, training_model_args: Optional[TrainingModelArgs], tp_pg: dist.ProcessGroup):
        super().__init__()

        # TODO @thomasw21: refactor so that we store that default in a single place.
        tp_mode = (
            training_model_args.tp_mode if training_model_args is not None else TensorParallelLinearMode.ALL_REDUCE
        )

        self.wi_0 = TensorParallelColumnLinear(config.d_model, config.d_ff, pg=tp_pg, mode=tp_mode, bias=False)
        self.wi_1 = TensorParallelColumnLinear(config.d_model, config.d_ff, pg=tp_pg, mode=tp_mode, bias=False)
        self.wo = TensorParallelRowLinear(config.d_ff, config.d_model, pg=tp_pg, mode=tp_mode, bias=False)
        self.dropout = nn.Dropout(config.dropout_rate)
        self.act = ACT2FN[config.dense_act_fn]

    def forward(self, hidden_states):
        hidden_gelu = self.act(self.wi_0(hidden_states))
        hidden_linear = self.wi_1(hidden_states)
        hidden_states = hidden_gelu * hidden_linear
        hidden_states = self.dropout(hidden_states)

        # To make 8bit quantization work for google/flan-t5-xxl, self.wo is kept in float32.
        # See https://github.com/huggingface/transformers/issues/20287
        if hidden_states.dtype != self.wo.weight.dtype:
            hidden_states = hidden_states.to(self.wo.weight.dtype)

        hidden_states = self.wo(hidden_states)
        return hidden_states


class T5LayerFF(nn.Module):
    def __init__(
        self,
        config: T5Config,
        training_model_args: Optional[TrainingModelArgs],
        tp_pg: dist.ProcessGroup,
        random_states: RandomStates,
    ):
        super().__init__()
        if config.is_gated_act:
            self.DenseReluDense = T5DenseGatedActDense(
                config=config, tp_pg=tp_pg, training_model_args=training_model_args
            )
        else:
            self.DenseReluDense = T5DenseActDense(config=config, tp_pg=tp_pg, training_model_args=training_model_args)

        self.layer_norm = RMSNorm(config.d_model, eps=config.layer_norm_epsilon)
        self.dropout = nn.Dropout(config.dropout_rate)

        # TODO @thomasw21: refactor so that we store that default in a single place.
        self.random_states = random_states

    def forward(self, hidden_states):
        forwarded_states = self.layer_norm(hidden_states)
        forwarded_states = self.DenseReluDense(forwarded_states)

        # Requires to run a synchronized random state across `tp` when using ALL_REDUCE
        with branch_random_state(
            self.random_states, "tp_synced", enabled=self.DenseReluDense.wo.mode is TensorParallelLinearMode.ALL_REDUCE
        ):
            hidden_states = hidden_states + self.dropout(forwarded_states)

        return {"hidden_states": hidden_states}


class T5CoreAttention(nn.Module):
    def __init__(self, config: T5Config, training_model_args: Optional[TrainingModelArgs]):
        super().__init__()
        self.is_decoder = config.is_decoder
        # TODO @thomasw21: T5 has a weird `d_kv` config which I'm guessing is essentially a `d_qkv`
        self.d_qk = config.d_kv
        self.d_v = config.d_kv
        self.dropout = config.dropout_rate

        self.gradient_checkpointing = False

        self.checkpoint_attention = (
            training_model_args is not None and training_model_args.recompute_mode == "selective"
        )

    @checkpoint_method(attr_name="checkpoint_attention")
    def forward(
        self,
        query_states: torch.Tensor,  # [batch_size, num_heads, q_length, inner_dim]
        key_states: torch.Tensor,  # [batch_size, num_heads, kv_length, inner_dim]
        value_states: torch.Tensor,  # [batch_size, num_heads, kv_length, inner_dim]
        attention_mask: torch.Tensor,  # torch.BoolTensor [batch_size, num_heads, q_length, kv_length] (can be broadcasted to that size)
        position_bias: Optional[torch.Tensor],  # [batch_size, num_heads, q_length, kv_length]
    ):
        # TODO @thomasw21: Megatron-LM stores states in (length, batch_size, num_heads * inner_dim). Maybe that's a bit faster.

        batch_size, n_heads, q_length, _ = query_states.shape
        kv_length = key_states.shape[2]

        if position_bias is not None:
            scores = torch.baddbmm(
                input=position_bias.view(batch_size * n_heads, q_length, kv_length),
                batch1=query_states.view(batch_size * n_heads, q_length, self.d_qk),
                batch2=key_states.view(batch_size * n_heads, kv_length, self.d_qk).transpose(1, 2),
                beta=1,
                alpha=1,
            )
        else:
            scores = torch.bmm(
                query_states.view(batch_size * n_heads, q_length, self.d_qk),
                key_states.view(batch_size * n_heads, kv_length, self.d_qk).transpose(1, 2),
            )

        dtype = scores.dtype
        if scores.dtype == torch.float16:
            scores = scores.float()

        scores = torch.masked_fill(
            scores.view(batch_size, n_heads, q_length, kv_length),
            ~attention_mask,
            torch.finfo(scores.dtype).min,
        )
        attn_weights = nn.functional.softmax(scores, dim=-1, dtype=torch.float).to(dtype=dtype)

        attn_weights = nn.functional.dropout(attn_weights, p=self.dropout, training=self.training)

        attn_output = torch.matmul(attn_weights, value_states).view(
            batch_size, n_heads, q_length, self.d_v
        )  # (batch_size, n_heads, seq_length, dim)
        return attn_output


class T5LayerSelfAttention(nn.Module, AttachableStore):
    def __init__(
        self,
        config,
        training_model_args: Optional[TrainingModelArgs],
        tp_pg: dist.ProcessGroup,
        random_states: RandomStates,
        is_causal: bool,
    ):
        super().__init__()
        # Tensor parallel considerations: We split tensors along head dimension
        assert config.num_heads % tp_pg.size() == 0
        self.n_heads = config.num_heads // tp_pg.size()
        # TODO @thomasw21: `T5` in `transformers` has a weird `d_kv` config which I'm guessing is essentically a `d_qkv`
        self.d_qk = config.d_kv
        self.d_v = config.d_kv
        self.d_model = config.d_model

        # TODO @thomasw21: refactor so that we store that default in a single place.
        tp_mode = (
            training_model_args.tp_mode if training_model_args is not None else TensorParallelLinearMode.ALL_REDUCE
        )

        # build the slice config for self.qkv for save/load
        # shard are done within the contiguous chunk
        qkv_contiguous_chunks = (
            config.num_attention_heads * self.d_qk,  # shape of q
            config.num_attention_heads * self.d_qk,  # shape of k
            config.num_attention_heads * self.d_qk,  # shape of v
        )
        self.qkv = TensorParallelColumnLinear(
            self.d_model,
            3 * config.num_heads * self.d_qk,
            pg=tp_pg,
            mode=tp_mode,
            bias=False,
            contiguous_chunks=qkv_contiguous_chunks,
        )

        self.relative_attention_bias = RelativeAttentionBias(
            config=config, tp_pg=tp_pg, is_bidirectional=not is_causal
        )
        self.o = TensorParallelRowLinear(
            config.num_heads * self.d_qk, self.d_model, pg=tp_pg, mode=tp_mode, bias=False
        )

        self.attention = T5CoreAttention(
            config,
            training_model_args=training_model_args,
        )
        self.layer_norm = RMSNorm(config.d_model, eps=config.layer_norm_epsilon)
        self.dropout = nn.Dropout(config.dropout_rate)

        self.random_states = random_states
        self.is_causal = is_causal

    def forward(
        self,
        hidden_states: torch.Tensor,  # [batch_size, length, hidden_dim] (can be broadcasted to that size)
        sequence_mask: torch.Tensor,  # (batch_size, length)
    ):
        normed_hidden_states = self.layer_norm(hidden_states)

        def split(states, num_batch_tensors: int):
            """Given a (batch_dim, seq_length, num_batch_tensors * n_heads * d_qk) tensor, return a Tuple of size `num_batch_tensors` containing tensors of size (batch_dim, n_heads, seq_length, d_qk)

            num_batch_tensors: int, whether that's `qkv` or just `kv` or just `q`
            """
            batch_size, seq_length = states.shape[:2]
            # TODO @thomasw21: Figure out how to not make copies, ie `contiguous`
            return tuple(
                elt.squeeze(dim=2).transpose(1, 2).contiguous()
                for elt in torch.split(
                    states.view(
                        batch_size,
                        seq_length,
                        num_batch_tensors,
                        self.n_heads,
                        self.d_qk,
                    ),
                    split_size_or_sections=1,
                    dim=2,
                )
            )

        def unshape(states):
            """Given a (batch_dim, num_heads, seq_length, d_qk) returns a (batch_dim, seq_length, num_heads * d_qk)"""
            batch_size, _, seq_length = states.shape[:3]
            # TODO @thomasw21: Figure out how to not make copies, ie `reshape`
            return states.transpose(1, 2).reshape(batch_size, seq_length, self.n_heads * self.d_v)

        # get query/key/value states
        query_states, key_states, value_states = split(
            self.qkv(normed_hidden_states), num_batch_tensors=3
        )  # (batch_size, n_heads, seq_length, dim_per_head)

        if self.is_causal:
            store = self.get_local_store()
            if store is not None:
                # Double check that we use store only at inference time
                assert key_states.requires_grad is False
                assert value_states.requires_grad is False

                # Pull pre-computed key/value states
                if "key" in store:
                    # We assume that "key"/"value"/"sequence_mask" are all added once initialized
                    old_key = store["key"]
                    old_value = store["value"]
                    old_sequence_mask = store["sequence_mask"]

                    # Concatenate with new key/value
                    key_states = torch.concat([old_key, key_states], dim=-2)
                    value_states = torch.concat([old_value, value_states], dim=-2)
                    all_sequence_mask = torch.concat([old_sequence_mask, sequence_mask], dim=-1)
                    attention_mask = _prepare_causal_attention_mask(
                        sequence_mask,
                        past_key_values_length=old_sequence_mask.shape[-1],
                    )  # (batch_size, 1, tgt_length, src_length) (True upper)
                else:
                    attention_mask = _prepare_causal_attention_mask(
                        sequence_mask,
                    )  # (batch_size, 1, tgt_length, src_length) (True upper)
                    all_sequence_mask = sequence_mask

                # Store new key/value in store
                store.update({"key": key_states, "value": value_states, "sequence_mask": all_sequence_mask})
            else:
                attention_mask = _prepare_causal_attention_mask(
                    sequence_mask,
                )  # (batch_size, 1, tgt_length, src_length) (True upper)
        else:
            attention_mask = (
                sequence_mask[:, None, :, None] * sequence_mask[:, None, None, :]
            )  # (batch_size, 1, seq_length, seq_length)

        position_bias = self.relative_attention_bias(
            batch_size=query_states.shape[0],
            q_length=query_states.shape[2],
            kv_length=key_states.shape[2],
            device=query_states.device,
        )

        attention_output = self.attention(
            query_states=query_states,
            key_states=key_states,
            value_states=value_states,
            attention_mask=attention_mask,
            position_bias=position_bias,
        )

        output = self.o(unshape(attention_output))

        # Requires to run a synchronized random state across `tp` when using ALL_REDUCE
        with branch_random_state(
            self.random_states, "tp_synced", enabled=self.o.mode is TensorParallelLinearMode.ALL_REDUCE
        ):
            hidden_states = hidden_states + self.dropout(output)

        return {"hidden_states": hidden_states, "sequence_mask": sequence_mask}


class T5LayerCrossAttention(nn.Module, AttachableStore):
    def __init__(
        self,
        config,
        tp_pg: dist.ProcessGroup,
        training_model_args: Optional[TrainingModelArgs],
        random_states: RandomStates,
    ):
        super().__init__()
        # Tensor parallel considerations: We split tensors along head dimension
        assert config.num_heads % tp_pg.size() == 0
        self.n_heads = config.num_heads // tp_pg.size()
        # TODO @thomasw21: `T5` in `transformers` has a weird `d_kv` config which I'm guessing is essentially a `d_qkv`
        self.d_qk = config.d_kv
        self.d_v = config.d_kv
        self.d_model = config.d_model

        # TODO @thomasw21: refactor so that we store that default in a single place.
        tp_mode = (
            training_model_args.tp_mode if training_model_args is not None else TensorParallelLinearMode.ALL_REDUCE
        )

        self.q = TensorParallelColumnLinear(
            self.d_model, config.num_heads * self.d_qk, pg=tp_pg, mode=tp_mode, bias=False
        )
        kv_contiguous_chunks = (
            config.num_attention_heads * self.d_qk,  # shape of k
            config.num_attention_heads * self.d_qk,  # shape of v
        )
        self.kv = TensorParallelColumnLinear(
            self.d_model,
            2 * config.num_heads * self.d_qk,
            pg=tp_pg,
            mode=tp_mode,
            bias=False,
            contiguous_chunks=kv_contiguous_chunks,
        )
        self.o = TensorParallelRowLinear(
            config.num_heads * self.d_qk, self.d_model, pg=tp_pg, mode=tp_mode, bias=False
        )

        self.attention = T5CoreAttention(config, training_model_args=training_model_args)
        self.layer_norm = RMSNorm(config.d_model, eps=config.layer_norm_epsilon)
        self.dropout = nn.Dropout(config.dropout_rate)

        self.random_states = random_states

    def forward(
        self,
        q_hidden_states,  # (batch_size, q_length, d_model)
        q_sequence_mask,  # (batch_size, q_length)
        kv_hidden_states,  # (batch_size, kv_length, d_model)
        kv_sequence_mask,  # (batch_size, kv_length)
    ):
        normed_hidden_states = self.layer_norm(q_hidden_states)

        def split(states, num_batch_tensors: int = 2):
            """Given a (batch_dim, seq_length, num_batch_tensors * n_heads * d_qk) tensor, return a Tuple of size `num_batch_tensors` containing tensors of size (batch_dim, n_heads, seq_length, d_qk)

            num_batch_tensors: int, whether that's `qkv` or just `kv` or just `q`
            """
            batch_size, seq_length = states.shape[:2]
            return tuple(
                elt.squeeze(dim=2).transpose(1, 2).contiguous()
                for elt in torch.split(
                    states.view(
                        batch_size,
                        seq_length,
                        num_batch_tensors,
                        self.n_heads,
                        self.d_qk,
                    ),
                    split_size_or_sections=1,
                    dim=2,
                )
            )

        def unshape(states):
            """Given a (batch_dim, num_heads, seq_length, d_qk) returns a (batch_dim, seq_length, num_heads * d_qk)"""
            batch_size, _, seq_length = states.shape[:3]
            return states.transpose(1, 2).reshape(batch_size, seq_length, self.n_heads * self.d_v)

        # get query states
        (query_states,) = split(
            self.q(normed_hidden_states), num_batch_tensors=1
        )  # (batch_size, n_heads, q_seq_length, dim_per_head)

        # get key/value states
        store = self.get_local_store()
        if store is not None:
            # Double check that we use store only at inference time
            assert normed_hidden_states.requires_grad is False

            # Pull pre-computed key/value states
            if "key" in store:
                # We assume that "key"/"value"/"sequence_mask" are all added once initialized
                key_states = store["key"]
                value_states = store["value"]
                all_kv_sequence_mask = store["sequence_mask"]
            else:
                key_states, value_states = split(
                    self.kv(kv_hidden_states), num_batch_tensors=2
                )  # (batch_size, n_heads, kv_seq_length, dim_per_head)
                all_kv_sequence_mask = kv_sequence_mask

                # Store new key/value in store
                store.update({"key": key_states, "value": value_states, "sequence_mask": all_kv_sequence_mask})
        else:
            key_states, value_states = split(
                self.kv(kv_hidden_states), num_batch_tensors=2
            )  # (batch_size, n_heads, kv_seq_length, dim_per_head)
            all_kv_sequence_mask = kv_sequence_mask

        attention_mask = (
            q_sequence_mask[:, None, :, None] * all_kv_sequence_mask[:, None, None, :]
        )  # (batch_size, 1, q_seq_length, kv_seq_length)

        attention_output = self.attention(
            query_states=query_states,
            key_states=key_states,
            value_states=value_states,
            attention_mask=attention_mask,
            position_bias=None,
        )

        output = self.o(unshape(attention_output))

        # Requires to run a synchronized random state across `tp`
        with branch_random_state(
            self.random_states, "tp_synced", enabled=self.o.mode is TensorParallelLinearMode.ALL_REDUCE
        ):
            q_hidden_states = q_hidden_states + self.dropout(output)

        return {
            "q_hidden_states": q_hidden_states,
            "q_sequence_mask": q_sequence_mask,
            "kv_hidden_states": kv_hidden_states,
            "kv_sequence_mask": kv_sequence_mask,
        }


class EncoderBlock(nn.Module):
    def __init__(self, self_attention_pp_block: PipelineBlock, ff_block: PipelineBlock):
        super(EncoderBlock, self).__init__()
        self.self_attention_pp_block = self_attention_pp_block
        self.ff_block = ff_block

    def forward(
        self,
        hidden_states: Union[torch.Tensor, TensorPointer],
        sequence_mask: Union[torch.Tensor, TensorPointer],
    ) -> Dict[str, Union[torch.Tensor, TensorPointer]]:
        output = self.self_attention_pp_block(hidden_states=hidden_states, sequence_mask=sequence_mask)
        hidden_states = self.ff_block(hidden_states=output["hidden_states"])["hidden_states"]
        return {
            "hidden_states": hidden_states,
            "sequence_mask": output["sequence_mask"],
        }

    def set_rank(self, pp_rank: int):
        self.self_attention_pp_block.build_and_set_rank(pp_rank)
        self.ff_block(pp_rank)


# TODO @nouamanetazi: need to cache this value
def _make_causal_mask(
    input_ids_shape: torch.Size, device: torch.device, past_key_values_length: int
) -> torch.BoolTensor:
    """
    Make causal mask used for self-attention. (True upper)
    """
    batch_size, target_length = input_ids_shape
    mask = torch.empty((target_length, target_length + past_key_values_length), dtype=torch.bool, device=device)
    # ONNX doesn't support `torch.Tensor.triu` properly, thus we use this workaround
    seq_ids = torch.arange(target_length, device=device)
    mask[:, past_key_values_length:] = seq_ids[:, None] < seq_ids[None, :]

    if past_key_values_length > 0:
        mask[:, :past_key_values_length] = False

    expanded_mask = mask[None, None, :, :].expand(batch_size, 1, target_length, target_length + past_key_values_length)
    return expanded_mask


def _expand_mask(mask: torch.Tensor, tgt_length: int) -> torch.BoolTensor:
    """
    Expands attention_mask from `[batch_size, src_length]` to `[batch_size, 1, tgt_length, src_length]`.
    """
    batch_size, src_length = mask.shape
    tgt_length = tgt_length if tgt_length is not None else src_length

    expanded_mask = mask[:, None, None, :]
    return expanded_mask.expand(batch_size, 1, tgt_length, src_length)


# Adapted from transformers.models.bloom.modeling_bloom.BloomModel._prepare_attn_mask
def _prepare_causal_attention_mask(sequence_mask: torch.Tensor, past_key_values_length: int = 0) -> torch.BoolTensor:
    # create causal mask
    # [batch_size, seq_length] -> [batch_size, 1, tgt_length, src_length]
    _, src_length = sequence_mask.shape

    # [batch_size, seq_length] -> [batch_size, 1, tgt_length, src_length]
    if src_length > 1:
        causal_mask = ~_make_causal_mask(
            sequence_mask.shape, device=sequence_mask.device, past_key_values_length=past_key_values_length
        )  # False upper [batch_size, 1, tgt_length, src_length]
        combined_attention_mask = causal_mask * sequence_mask[:, None, None, :]
    else:
        combined_attention_mask = sequence_mask[:, None, None, :]
    return combined_attention_mask


class DecoderBlock(nn.Module):
    def __init__(
        self,
        self_attention_pp_block: PipelineBlock,
        cross_attention_pp_block: PipelineBlock,
        ff_block: PipelineBlock,
    ):
        super(DecoderBlock, self).__init__()
        self.self_attention_pp_block = self_attention_pp_block
        self.cross_attention_pp_block = cross_attention_pp_block
        self.ff_block = ff_block

    def forward(
        self,
        decoder_q_hidden_states: Union[torch.Tensor, TensorPointer],
        decoder_q_sequence_mask: Union[torch.Tensor, TensorPointer],
        encoder_kv_hidden_states: Union[torch.Tensor, TensorPointer],
        encoder_kv_sequence_mask: Union[torch.Tensor, TensorPointer],
    ) -> Dict[str, Union[torch.Tensor, TensorPointer]]:
        output = self.self_attention_pp_block(
            hidden_states=decoder_q_hidden_states,
            sequence_mask=decoder_q_sequence_mask,
        )
        output = self.cross_attention_pp_block(
            q_hidden_states=output["hidden_states"],
            q_sequence_mask=output["sequence_mask"],
            kv_hidden_states=encoder_kv_hidden_states,
            kv_sequence_mask=encoder_kv_sequence_mask,
            # TODO @nouamanetazi : transformers use `encoder_decoder_position_bias` which seem to be set to zeros (checked experimentally)? Actually I have no idea how it works
        )
        q_hidden_states = self.ff_block(hidden_states=output["q_hidden_states"])["hidden_states"]
        return {
            "decoder_q_hidden_states": q_hidden_states,
            "decoder_q_sequence_mask": output["q_sequence_mask"],
            "encoder_kv_hidden_states": output["kv_hidden_states"],
            "encoder_kv_sequence_mask": output["kv_sequence_mask"],
        }

    def set_rank(self, pp_rank: int):
        self.self_attention_pp_block.build_and_set_rank(pp_rank)
        self.cross_attention_pp_block.build_and_set_rank(pp_rank)
        self.ff_block(pp_rank)


class RelativeAttentionBias(nn.Module):
    def __init__(self, tp_pg: dist.ProcessGroup, config: T5Config, is_bidirectional: bool):
        super().__init__()
        self.relative_attention_num_buckets = config.relative_attention_num_buckets
        self.relative_attention_max_distance = config.relative_attention_max_distance
        assert config.num_heads % tp_pg.size() == 0
        self.n_heads = config.num_heads // tp_pg.size()
        self.is_bidirectional = is_bidirectional

        self.relative_attention_bias = nn.Embedding(self.relative_attention_num_buckets, self.n_heads)
        mark_all_parameters_in_module_as_sharded(
            self.relative_attention_bias, pg=tp_pg, split_config=SplitConfig(split_dim=1)
        )

    @staticmethod
    def _relative_position_bucket(
        relative_position: torch.Tensor, bidirectional: bool, num_buckets: int, max_distance: int
    ):
        """
        Adapted from Mesh Tensorflow:
        https://github.com/tensorflow/mesh/blob/0cb87fe07da627bf0b7e60475d59f95ed6b5be3d/mesh_tensorflow/transformer/transformer_layers.py#L593

        Translate relative position to a bucket number for relative attention. The relative position is defined as
        memory_position - query_position, i.e. the distance in tokens from the attending position to the attended-to
        position. If bidirectional=False, then positive relative positions are invalid. We use smaller buckets for
        small absolute relative_position and larger buckets for larger absolute relative_positions. All relative
        positions >=max_distance map to the same bucket. All relative positions <=-max_distance map to the same bucket.
        This should allow for more graceful generalization to longer sequences than the model has been trained on

        Args:
            relative_position: an int32 Tensor
            bidirectional: a boolean - whether the attention is bidirectional
            num_buckets: an integer
            max_distance: an integer

        Returns:
            a Tensor with the same shape as relative_position, containing int32 values in the range [0, num_buckets)
        """
        relative_buckets = 0
        if bidirectional:
            num_buckets //= 2
            relative_buckets += (relative_position > 0).to(torch.long) * num_buckets
            relative_position = torch.abs(relative_position)
        else:
            relative_position = -torch.min(relative_position, torch.zeros_like(relative_position))
        # now relative_position is in the range [0, inf)

        # half of the buckets are for exact increments in positions
        max_exact = num_buckets // 2
        is_small = relative_position < max_exact

        # The other half of the buckets are for logarithmically bigger bins in positions up to max_distance
        relative_position_if_large = max_exact + (
            torch.log(relative_position.float() / max_exact)
            / math.log(max_distance / max_exact)
            * (num_buckets - max_exact)
        ).to(torch.long)
        relative_position_if_large = torch.min(
            relative_position_if_large,
            torch.full_like(relative_position_if_large, num_buckets - 1),
        )

        relative_buckets += torch.where(is_small, relative_position, relative_position_if_large)
        return relative_buckets

    @cache
    @torch.no_grad()
    def compute_position_bucket(self, q_length: int, kv_length: int, device: torch.device):
        """Compute binned relative position bias"""
        context_position = torch.arange(q_length, dtype=torch.long, device=device)[:, None]
        memory_position = torch.arange(kv_length, dtype=torch.long, device=device)[None, :]
        relative_position = memory_position - context_position  # shape (query_length, key_length)
        return self._relative_position_bucket(
            relative_position,  # shape (query_length, key_length)
            bidirectional=self.is_bidirectional,
            num_buckets=self.relative_attention_num_buckets,
            max_distance=self.relative_attention_max_distance,
        )

    def forward(self, batch_size: int, q_length: int, kv_length: int, device: torch.device):
        relative_position_bucket = self.compute_position_bucket(
            q_length=q_length,
            kv_length=kv_length,
            device=device,
        )
        # shape (query_length, key_length, num_heads)
        values = self.relative_attention_bias(relative_position_bucket)
        # shape (1, num_heads, query_length, key_length)
        values = values.permute([2, 0, 1])
        if batch_size == 1 or self.n_heads == 1:
            return values
        else:
            return values.repeat(batch_size, 1, 1)


class T5(nn.Module):
    """Build pipeline graph"""

    def __init__(
        self,
        config: T5Config,
        dpg: DistributedProcessGroups,
        training_model_args: Optional[TrainingModelArgs],
        random_states: RandomStates,
    ):
        super(T5, self).__init__()

        # Declare all the nodes
        self.p2p = P2P(dpg.pp_pg, device=torch.device("cuda"))
        self.random_states = random_states

        # TODO @thomasw21: refactor so that we store that default in a single place.
        self.tp_mode = (
            training_model_args.tp_mode if training_model_args is not None else TensorParallelLinearMode.ALL_REDUCE
        )

        self.encoder_embedding = PipelineBlock(
            p2p=self.p2p,
            module_builder=TensorParallelEmbedding,
            module_kwargs={
                "pg": dpg.tp_pg,
                "num_embeddings": config.vocab_size,
                "embedding_dim": config.d_model,
                "mode": self.tp_mode,
            },
            module_input_keys={"input_ids"},
            module_output_keys={"input_embeds"},
        )

        self.encoder_embeds_dropout = PipelineBlock(
            p2p=self.p2p,
            module_builder=nn.Dropout,
            module_kwargs={"p": config.dropout_rate},
            module_input_keys={"input"},
            module_output_keys={"hidden_states"},
        )

        self.encoder = nn.ModuleList(
            [
                EncoderBlock(
                    self_attention_pp_block=PipelineBlock(
                        p2p=self.p2p,
                        module_builder=T5LayerSelfAttention,
                        module_kwargs={
                            "tp_pg": dpg.tp_pg,
                            "config": config,
                            "training_model_args": training_model_args,
                            "random_states": random_states,
                            "is_causal": False,
                        },
                        module_input_keys={"hidden_states", "sequence_mask"},
                        module_output_keys={"hidden_states", "sequence_mask"},
                    ),
                    ff_block=PipelineBlock(
                        p2p=self.p2p,
                        module_builder=T5LayerFF,
                        module_kwargs={
                            "tp_pg": dpg.tp_pg,
                            "config": config,
                            "random_states": random_states,
                            "training_model_args": training_model_args,
                        },
                        module_input_keys={"hidden_states"},
                        module_output_keys={"hidden_states"},
                    ),
                )
                for _ in range(config.num_layers)
            ]
        )

        self.encoder_final_layer_norm = PipelineBlock(
            p2p=self.p2p,
            module_builder=RMSNorm,
            module_kwargs={"normalized_shape": config.d_model, "eps": config.layer_norm_epsilon},
            module_input_keys={"input"},
            module_output_keys={"hidden_states"},
        )
        self.encoder_dropout = PipelineBlock(
            p2p=self.p2p,
            module_builder=nn.Dropout,
            module_kwargs={"p": config.dropout_rate},
            module_input_keys={"input"},
            module_output_keys={"hidden_states"},
        )

        self.decoder_embedding = PipelineBlock(
            p2p=self.p2p,
            module_builder=TensorParallelEmbedding,
            module_kwargs={
                "pg": dpg.tp_pg,
                "num_embeddings": config.vocab_size,
                "embedding_dim": config.d_model,
                "mode": self.tp_mode,
            },
            module_input_keys={"input_ids"},
            module_output_keys={"input_embeds"},
        )

        self.decoder_embeds_dropout = PipelineBlock(
            p2p=self.p2p,
            module_builder=nn.Dropout,
            module_kwargs={"p": config.dropout_rate},
            module_input_keys={"input"},
            module_output_keys={"hidden_states"},
        )

        self.decoder = nn.ModuleList(
            [
                DecoderBlock(
                    self_attention_pp_block=PipelineBlock(
                        p2p=self.p2p,
                        module_builder=T5LayerSelfAttention,
                        module_kwargs={
                            "tp_pg": dpg.tp_pg,
                            "config": config,
                            "training_model_args": training_model_args,
                            "random_states": random_states,
                            "is_causal": True,
                        },
                        module_input_keys={"hidden_states", "sequence_mask"},
                        module_output_keys={"hidden_states", "sequence_mask"},
                    ),
                    cross_attention_pp_block=PipelineBlock(
                        p2p=self.p2p,
                        module_builder=T5LayerCrossAttention,
                        module_kwargs={
                            "tp_pg": dpg.tp_pg,
                            "config": config,
                            "training_model_args": training_model_args,
                            "random_states": random_states,
                        },
                        module_input_keys={
                            "q_hidden_states",
                            "q_sequence_mask",
                            "kv_hidden_states",
                            "kv_sequence_mask",
                        },
                        module_output_keys={
                            "q_hidden_states",
                            "q_sequence_mask",
                            "kv_hidden_states",
                            "kv_sequence_mask",
                        },
                    ),
                    ff_block=PipelineBlock(
                        p2p=self.p2p,
                        module_builder=T5LayerFF,
                        module_kwargs={
                            "tp_pg": dpg.tp_pg,
                            "config": config,
                            "random_states": random_states,
                            "training_model_args": training_model_args,
                        },
                        module_input_keys={"hidden_states"},
                        module_output_keys={"hidden_states"},
                    ),
                )
                for _ in range(config.num_decoder_layers)
            ]
        )

        self.decoder_final_layer_norm = PipelineBlock(
            p2p=self.p2p,
            module_builder=RMSNorm,
            module_kwargs={"normalized_shape": config.d_model, "eps": config.layer_norm_epsilon},
            module_input_keys={"input"},
            module_output_keys={"hidden_states"},
        )
        self.decoder_dropout = PipelineBlock(
            p2p=self.p2p,
            module_builder=nn.Dropout,
            module_kwargs={"p": config.dropout_rate},
            module_input_keys={"input"},
            module_output_keys={"hidden_states"},
        )

        self.lm_head = PipelineBlock(
            p2p=self.p2p,
            # Understand that this means that we return sharded logits that are going to need to be gathered
            module_builder=TensorParallelColumnLinear,
            module_kwargs={
                "in_features": config.d_model,
                "out_features": config.vocab_size,
                "pg": dpg.tp_pg,
                "bias": False,
                "mode": self.tp_mode,
            },
            module_input_keys={"x"},
            module_output_keys={"logits"},
        )

    def forward_encoder(
        self,
        encoder_input_ids: Union[torch.Tensor, TensorPointer],
        encoder_input_mask: Union[torch.Tensor, TensorPointer],
    ) -> Tuple[Union[torch.Tensor, TensorPointer], Union[torch.Tensor, TensorPointer]]:
        # All inputs can be TensorPointer, many ranks will actually receive TensorPointers instead of Tensors

        input_embeds = self.encoder_embedding(input_ids=encoder_input_ids)["input_embeds"]

        # Requires to run a synchronized random state across `tp`
        with branch_random_state(
            self.random_states, "tp_synced", enabled=self.tp_mode is TensorParallelLinearMode.ALL_REDUCE
        ):
            hidden_states = self.encoder_embeds_dropout(input=input_embeds)["hidden_states"]

        hidden_encoder_states = {
            "hidden_states": hidden_states,
            "sequence_mask": encoder_input_mask,
        }
        for encoder_block in self.encoder:
            hidden_encoder_states = encoder_block(**hidden_encoder_states)

        hidden_states = self.encoder_final_layer_norm(input=hidden_encoder_states["hidden_states"])["hidden_states"]
        return self.encoder_dropout(input=hidden_states)["hidden_states"], hidden_encoder_states["sequence_mask"]

    def forward_decoder(
        self,
        decoder_input_ids: Union[torch.Tensor, TensorPointer],
        decoder_input_mask: Union[torch.Tensor, TensorPointer],
        encoder_last_hidden_states: Union[torch.Tensor, TensorPointer],
        encoder_mask: Union[torch.Tensor, TensorPointer],
    ) -> Union[torch.Tensor, TensorPointer]:
        input_embeds = self.decoder_embedding(input_ids=decoder_input_ids)["input_embeds"]

        # Requires to run a synchronized random state across `tp`
        with branch_random_state(
            self.random_states, "tp_synced", enabled=self.tp_mode is TensorParallelLinearMode.ALL_REDUCE
        ):
            hidden_states = self.decoder_embeds_dropout(input=input_embeds)["hidden_states"]

        hidden_decoder_states = {
            "decoder_q_hidden_states": hidden_states,
            "decoder_q_sequence_mask": decoder_input_mask,
            "encoder_kv_hidden_states": encoder_last_hidden_states,
            "encoder_kv_sequence_mask": encoder_mask,
        }
        for decoder_block in self.decoder:
            hidden_decoder_states = decoder_block(**hidden_decoder_states)

        hidden_states = self.decoder_final_layer_norm(input=hidden_decoder_states["decoder_q_hidden_states"])[
            "hidden_states"
        ]
        hidden_states = self.decoder_dropout(input=hidden_states)["hidden_states"]
        sharded_logits = self.lm_head(x=hidden_states)["logits"]

        return sharded_logits

    def forward(
        self,
        encoder_input_ids: Union[torch.Tensor, TensorPointer],
        encoder_input_mask: Union[torch.Tensor, TensorPointer],
        decoder_input_ids: Union[torch.Tensor, TensorPointer],
        decoder_input_mask: Union[torch.Tensor, TensorPointer],
    ) -> Union[torch.Tensor, TensorPointer]:
        encoder_last_hidden_states, encoder_mask = self.forward_encoder(
            encoder_input_ids=encoder_input_ids,
            encoder_input_mask=encoder_input_mask,
        )

        return self.forward_decoder(
            decoder_input_ids=decoder_input_ids,
            decoder_input_mask=decoder_input_mask,
            encoder_last_hidden_states=encoder_last_hidden_states,
            encoder_mask=encoder_mask,
        )


# TODO @thomasw21: It's a bit weird that our loss needs to be wrapped inside a `nn.Module`. The issue is that PipelineBlock essentially defines where the compute happens
class Loss(nn.Module):
    def __init__(self, tp_pg: dist.ProcessGroup):
        super().__init__()
        self.tp_pg = tp_pg

    def forward(
        self,
        decoder_sharded_logits: torch.Tensor,  # (batch_size, length, logits)
        decoder_label_ids: torch.Tensor,  # (batch_size, length)
        decoder_label_mask: torch.Tensor,  # (batch_size, length)
    ) -> Dict[str, torch.Tensor]:
        loss = sharded_cross_entropy(decoder_sharded_logits, decoder_label_ids, group=self.tp_pg)
        # TODO @thomasw21: It's unclear what kind of normalization we want to do.
        loss = loss[decoder_label_mask].sum()
        return {"loss": loss}


class T5ForTraining(nn.Module):
    def __init__(
        self,
        config: T5Config,
        dpg: DistributedProcessGroups,
        training_model_args: Optional[TrainingModelArgs],
        random_states: RandomStates,
    ):
        super().__init__()
        self.model = T5(config=config, dpg=dpg, training_model_args=training_model_args, random_states=random_states)
        self.loss = PipelineBlock(
            p2p=self.model.p2p,
            module_builder=Loss,
            module_kwargs={"tp_pg": dpg.tp_pg},
            module_input_keys={
                "decoder_sharded_logits",
                "decoder_label_ids",
                "decoder_label_mask",
            },
            module_output_keys={"loss"},
        )

    def forward(
        self,
        encoder_input_ids: Union[torch.Tensor, TensorPointer],
        encoder_input_mask: Union[torch.Tensor, TensorPointer],
        decoder_input_ids: Union[torch.Tensor, TensorPointer],
        decoder_input_mask: Union[torch.Tensor, TensorPointer],
        decoder_label_ids: Union[torch.Tensor, TensorPointer],
        decoder_label_mask: Union[torch.Tensor, TensorPointer],
    ) -> Union[torch.Tensor, TensorPointer]:
        sharded_logits = self.model(
            encoder_input_ids=encoder_input_ids,
            encoder_input_mask=encoder_input_mask,
            decoder_input_ids=decoder_input_ids,
            decoder_input_mask=decoder_input_mask,
        )
        return self.loss(
            decoder_sharded_logits=sharded_logits,
            decoder_label_ids=decoder_label_ids,
            decoder_label_mask=decoder_label_mask,
        )["loss"]
