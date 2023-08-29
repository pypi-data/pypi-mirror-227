# coding=utf-8
# Copyright 2018 HuggingFace Inc. team.
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
""" PyTorch GPT model."""

from functools import lru_cache
from typing import Dict, Optional, Union

import torch
from config import ParallelismArgs, RecomputeGranularity
from torch import nn
from torch.nn import LayerNorm
from transformers import GPT2Config
from transformers.activations import ACT2FN

from brrr.core import distributed as dist
from brrr.core.dataclass import RandomStates
from brrr.core.parallelism.pipeline_parallelism.block import PipelineBlock, TensorPointer
from brrr.core.parallelism.pipeline_parallelism.p2p import P2P
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


class MLP(nn.Module):
    def __init__(
        self,
        config: GPT2Config,
        parallel_config: Optional[ParallelismArgs],
        tp_pg: dist.ProcessGroup,
    ):
        super().__init__()

        # TODO @thomasw21: refactor so that we store that default in a single place.
        tp_mode = parallel_config.tp_mode if parallel_config is not None else TensorParallelLinearMode.ALL_REDUCE

        d_ff = config.n_inner if config.n_inner is not None else 4 * config.hidden_size
        self.c_fc = TensorParallelColumnLinear(config.hidden_size, d_ff, pg=tp_pg, mode=tp_mode, bias=True)
        self.act = ACT2FN[config.activation_function]
        self.c_proj = TensorParallelRowLinear(d_ff, config.hidden_size, pg=tp_pg, mode=tp_mode, bias=True)

    def forward(self, hidden_states):
        hidden_states = self.c_fc(hidden_states)
        hidden_states = self.act(hidden_states)
        hidden_states = self.c_proj(hidden_states)
        return {"hidden_states": hidden_states}


class CoreAttention(nn.Module):
    def __init__(self, config: GPT2Config, parallel_config: Optional[ParallelismArgs], layer_idx: int):
        super().__init__()
        # TODO @thomasw21: GPT has a weird `d_kv` config which I'm guessing is essentically a `d_qkv`
        assert (
            config.hidden_size % config.num_attention_heads == 0
        ), f"Hidden size {config.hidden_size} must be divisible by number of attention heads {config.num_attention_heads}."
        self.d_qk = config.hidden_size // config.num_attention_heads
        self.d_v = config.hidden_size // config.num_attention_heads
        self.dropout = config.attn_pdrop

        self.scale_factor = 1.0
        if config.scale_attn_weights:
            self.scale_factor = self.scale_factor / (self.d_qk**0.5)

        # Layer-wise attention scaling
        if config.scale_attn_by_inverse_layer_idx:
            self.scale_factor = self.scale_factor / float(layer_idx + 1)

        self.checkpoint_attention = (
            parallel_config is not None and parallel_config.recompute_granularity is RecomputeGranularity.SELECTIVE
        )

    @checkpoint_method(attr_name="checkpoint_attention")
    def forward(
        self,
        query_states: torch.Tensor,  # [batch_size, num_heads, q_length, inner_dim]
        key_states: torch.Tensor,  # [batch_size, num_heads, kv_length, inner_dim]
        value_states: torch.Tensor,  # [batch_size, num_heads, kv_length, inner_dim]
        attention_mask: torch.Tensor,  # torch.BoolTensor [batch_size, num_heads, q_length, kv_length] (can be broadcasted to that size)
    ):
        # TODO @thomasw21: Megatron-LM stores states in (length, batch_size, num_heads * inner_dim). Maybe that's a bit faster.

        batch_size, n_heads, q_length, _ = query_states.shape
        kv_length = key_states.shape[2]

        scores = torch.bmm(
            query_states.view(batch_size * n_heads, q_length, self.d_qk),
            key_states.view(batch_size * n_heads, kv_length, self.d_qk).transpose(1, 2),
        )

        if self.scale_factor != 1.0:
            scores = scores * self.scale_factor

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


class CausalSelfAttention(nn.Module, AttachableStore):
    def __init__(
        self,
        config: GPT2Config,
        parallel_config: Optional[ParallelismArgs],
        tp_pg: dist.ProcessGroup,
        layer_idx: int,
    ):
        super().__init__()
        # Tensor parallel considerations: We split tensors along head dimension
        assert (
            config.num_attention_heads % tp_pg.size() == 0
        ), f"Number of attention heads ({config.num_attention_heads}) must be divisible by TP size ({tp_pg.size()})."
        self.n_heads = config.num_attention_heads // tp_pg.size()
        self.d_qk = config.hidden_size // config.num_attention_heads
        self.d_v = config.hidden_size // config.num_attention_heads
        self.d_model = config.hidden_size

        # TODO @thomasw21: refactor so that we store that default in a single place.
        tp_mode = parallel_config.tp_mode if parallel_config is not None else TensorParallelLinearMode.ALL_REDUCE

        # build the slice config for self.qkv for save/load
        # shard are done within the contiguous chunk
        qkv_contiguous_chunks = (
            config.num_attention_heads * self.d_qk,  # shape of q
            config.num_attention_heads * self.d_qk,  # shape of k
            config.num_attention_heads * self.d_qk,  # shape of v
        )
        self.qkv = TensorParallelColumnLinear(
            self.d_model,
            3 * config.num_attention_heads * self.d_qk,
            pg=tp_pg,
            mode=tp_mode,
            bias=True,
            contiguous_chunks=qkv_contiguous_chunks,
        )

        self.o = TensorParallelRowLinear(
            config.num_attention_heads * self.d_qk, self.d_model, pg=tp_pg, mode=tp_mode, bias=True
        )

        self.attention = CoreAttention(
            config,
            parallel_config=parallel_config,
            layer_idx=layer_idx,
        )

    def forward(
        self,
        # [batch_size, length, hidden_dim] (can be broadcasted to that size)
        hidden_states,
        sequence_mask,  # (batch_size, length)
    ):
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
            self.qkv(hidden_states), num_batch_tensors=3
        )  # (batch_size, n_heads, seq_length, dim_per_head)

        # Get cached key/values from store if available
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
                    q_sequence_mask=sequence_mask,
                    k_sequence_mask=all_sequence_mask,
                )  # (batch_size, 1, query_length, key_length) (True upper)
            else:
                attention_mask = _prepare_causal_attention_mask(
                    q_sequence_mask=sequence_mask,
                    k_sequence_mask=sequence_mask,
                )  # (batch_size, 1, query_length, key_length) (True upper)
                all_sequence_mask = sequence_mask

            # Store new key/value in store
            store.update({"key": key_states, "value": value_states, "sequence_mask": all_sequence_mask})
        else:
            attention_mask = _prepare_causal_attention_mask(
                q_sequence_mask=sequence_mask,
                k_sequence_mask=sequence_mask,
            )  # (batch_size, 1, query_length, key_length) (True upper)

        attention_output = self.attention(
            query_states=query_states,
            key_states=key_states,
            value_states=value_states,
            attention_mask=attention_mask,
        )

        output = self.o(unshape(attention_output))

        return {"hidden_states": output, "sequence_mask": sequence_mask}


class GPTBlock(nn.Module):
    def __init__(
        self,
        config: GPT2Config,
        parallel_config: Optional[ParallelismArgs],
        tp_pg: dist.ProcessGroup,
        random_states: RandomStates,
        layer_idx: int,
    ):
        super(GPTBlock, self).__init__()
        self.ln_1 = LayerNorm(config.hidden_size, eps=config.layer_norm_epsilon)
        self.attn = CausalSelfAttention(
            config=config,
            parallel_config=parallel_config,
            tp_pg=tp_pg,
            layer_idx=layer_idx,
        )
        self.attn_dropout = nn.Dropout(config.attn_pdrop)

        self.ln_2 = LayerNorm(config.hidden_size, eps=config.layer_norm_epsilon)
        self.ff = MLP(config=config, parallel_config=parallel_config, tp_pg=tp_pg)
        self.ff_dropout = nn.Dropout(config.resid_pdrop)

        self.random_states = random_states
        self.tp_mode = parallel_config.tp_mode if parallel_config is not None else TensorParallelLinearMode.ALL_REDUCE

    def forward(
        self,
        hidden_states: Union[torch.Tensor, TensorPointer],
        sequence_mask: Union[torch.Tensor, TensorPointer],
    ) -> Dict[str, Union[torch.Tensor, TensorPointer]]:
        residual = hidden_states
        hidden_states = self.ln_1(hidden_states)
        output = self.attn(hidden_states=hidden_states, sequence_mask=sequence_mask)

        with branch_random_state(
            self.random_states, "tp_synced", enabled=self.tp_mode is TensorParallelLinearMode.ALL_REDUCE
        ):
            hidden_states = self.attn_dropout(output["hidden_states"])

        hidden_states = residual + hidden_states

        residual = hidden_states
        hidden_states = self.ln_2(hidden_states)
        hidden_states = self.ff(hidden_states=hidden_states)["hidden_states"]

        with branch_random_state(
            self.random_states, "tp_synced", enabled=self.tp_mode is TensorParallelLinearMode.ALL_REDUCE
        ):
            hidden_states = self.ff_dropout(hidden_states)

        hidden_states = residual + hidden_states
        return {
            "hidden_states": hidden_states,
            "sequence_mask": output["sequence_mask"],
        }


@lru_cache(maxsize=1)
def _make_causal_mask(
    q_sequence_mask_shape: torch.Size,
    k_sequence_mask_shape: torch.Size,
    device: torch.device,
) -> torch.BoolTensor:
    """
    Make causal mask used for self-attention. (True upper). The mask is broadcasted to
    shape (batch_size, 1, query_length, key_length) from (query_length, key_length).
    """
    batch_size, query_length = q_sequence_mask_shape
    batch_size, key_length = k_sequence_mask_shape
    past_key_length = key_length - query_length
    mask = torch.empty((query_length, key_length), dtype=torch.bool, device=device)
    # ONNX doesn't support `torch.Tensor.triu` properly, thus we use this workaround
    seq_ids = torch.arange(query_length, device=device)
    mask[:, past_key_length:] = seq_ids[:, None] < seq_ids[None, :]
    if past_key_length > 0:
        mask[:, :past_key_length] = False

    expanded_mask = mask[None, None, :, :].expand(batch_size, 1, query_length, key_length)
    return expanded_mask


def _prepare_causal_attention_mask(q_sequence_mask: torch.Tensor, k_sequence_mask: torch.Tensor) -> torch.BoolTensor:
    """
    Prepare causal attention mask used for multi-head self-attention. (False upper)
    Adapted from transformers.models.bloom.modeling_bloom.BloomModel._prepare_attn_mask

    Input:
    q_sequence_mask: [batch_size, query_length]
    k_sequence_mask: [batch_size, key_length]
    Output:
    [batch_size, 1, query_length, key_length]

    Note:
    The dimension 1 is added to be broadcastable to [batch_size, number_of_heads, query_length, key_length].
    """
    _, key_length = k_sequence_mask.shape
    if key_length > 1:
        causal_mask = ~_make_causal_mask(
            q_sequence_mask_shape=q_sequence_mask.shape,
            k_sequence_mask_shape=k_sequence_mask.shape,
            device=q_sequence_mask.device,
        )  # False upper [batch_size, 1, query_length, key_length]
        combined_attention_mask = causal_mask * k_sequence_mask[:, None, None, :]
    else:
        combined_attention_mask = k_sequence_mask[:, None, None, :]
    return combined_attention_mask


class Embedding(nn.Module, AttachableStore):
    def __init__(self, tp_pg: dist.ProcessGroup, config: GPT2Config, parallel_config: Optional[ParallelismArgs]):
        super().__init__()
        self.token_embedding = TensorParallelEmbedding(
            num_embeddings=config.vocab_size,
            embedding_dim=config.hidden_size,
            pg=tp_pg,
            mode=parallel_config.tp_mode if parallel_config is not None else TensorParallelLinearMode.ALL_REDUCE,
        )
        # TODO @nouamanetazi: make RowParallelEmbedding (shard across embedding_dim) in case of seq parallel
        self.position_embedding = nn.Embedding(
            num_embeddings=config.max_position_embeddings,
            embedding_dim=config.hidden_size,
        )

    def forward(self, input_ids: torch.Tensor, input_mask: torch.Tensor):
        input_embeds = self.token_embedding(input_ids)

        store = self.get_local_store()
        if store is not None:
            if "past_length" in store:
                past_length = store["past_length"]
            else:
                past_length = torch.zeros(1, dtype=torch.long, device=input_ids.device).expand(input_ids.shape[0])

            cumsum_mask = input_mask.cumsum(-1, dtype=torch.long)
            position_ids = cumsum_mask + (past_length[:, None] - 1)
            # Store new past_length in store
            store["past_length"] = past_length + cumsum_mask[:, -1]

        else:
            position_ids = input_mask.cumsum(-1, dtype=torch.long) - 1

        # fill the -1 position with value 0
        position_ids.masked_fill_(input_mask == 0, 0)

        position_bias = self.position_embedding(position_ids)
        return {"input_embeds": input_embeds + position_bias}


class GPTModel(nn.Module):
    """Build pipeline graph"""

    def __init__(
        self,
        config: GPT2Config,
        dpg: DistributedProcessGroups,
        parallel_config: Optional[ParallelismArgs],
        random_states: RandomStates,
    ):
        super().__init__()

        # Declare all the nodes
        self.p2p = P2P(dpg.pp_pg, device=torch.device("cuda"))
        self.random_states = random_states
        self.tp_mode = parallel_config.tp_mode if parallel_config is not None else TensorParallelLinearMode.ALL_REDUCE

        self.token_position_embeddings = PipelineBlock(
            p2p=self.p2p,
            module_builder=Embedding,
            module_kwargs={
                "tp_pg": dpg.tp_pg,
                "config": config,
                "parallel_config": parallel_config,
            },
            module_input_keys={"input_ids", "input_mask"},
            module_output_keys={"input_embeds"},
        )

        self.embeds_dropout = PipelineBlock(
            p2p=self.p2p,
            module_builder=nn.Dropout,
            module_kwargs={"p": config.embd_pdrop},
            module_input_keys={"input"},
            module_output_keys={"hidden_states"},
        )

        self.decoder = nn.ModuleList(
            [
                PipelineBlock(
                    p2p=self.p2p,
                    module_builder=GPTBlock,
                    module_kwargs={
                        "config": config,
                        "parallel_config": parallel_config,
                        "tp_pg": dpg.tp_pg,
                        "random_states": random_states,
                        "layer_idx": layer_idx,
                    },
                    module_input_keys={"hidden_states", "sequence_mask"},
                    module_output_keys={"hidden_states", "sequence_mask"},
                )
                for layer_idx in range(config.n_layer)
            ]
        )

        self.final_layer_norm = PipelineBlock(
            p2p=self.p2p,
            module_builder=LayerNorm,
            module_kwargs={"normalized_shape": config.hidden_size, "eps": config.layer_norm_epsilon},
            module_input_keys={"input"},
            module_output_keys={"hidden_states"},
        )

        self.lm_head = PipelineBlock(
            p2p=self.p2p,
            # Understand that this means that we return sharded logits that are going to need to be gathered
            module_builder=TensorParallelColumnLinear,
            module_kwargs={
                "in_features": config.hidden_size,
                "out_features": config.vocab_size,
                "pg": dpg.tp_pg,
                "bias": False,
                # TODO @thomasw21: refactor so that we store that default in a single place.
                "mode": self.tp_mode,
            },
            module_input_keys={"x"},
            module_output_keys={"logits"},
        )

        self.cast_to_fp32 = PipelineBlock(
            p2p=self.p2p,
            module_builder=lambda: lambda x: x.float(),
            module_kwargs={},
            module_input_keys={"x"},
            module_output_keys={"output"},
        )

    def forward(
        self,
        input_ids: Union[torch.Tensor, TensorPointer],
        input_mask: Union[torch.Tensor, TensorPointer],
    ):
        # all tensors are optional as most ranks don't need anything from the dataloader.

        input_embeds = self.token_position_embeddings(input_ids=input_ids, input_mask=input_mask)["input_embeds"]

        with branch_random_state(
            self.random_states, "tp_synced", enabled=self.tp_mode == TensorParallelLinearMode.ALL_REDUCE
        ):
            hidden_states = self.embeds_dropout(input=input_embeds)["hidden_states"]

        hidden_encoder_states = {"hidden_states": hidden_states, "sequence_mask": input_mask}
        for encoder_block in self.decoder:
            hidden_encoder_states = encoder_block(**hidden_encoder_states)

        hidden_states = self.final_layer_norm(input=hidden_encoder_states["hidden_states"])["hidden_states"]

        sharded_logits = self.lm_head(x=hidden_states)["logits"]

        fp32_sharded_logits = self.cast_to_fp32(x=sharded_logits)["output"]

        return fp32_sharded_logits


# TODO @thomasw21: It's a bit weird that our loss needs to be wrapped inside a `nn.Module`. The issue is that PipelineBlock essentially defines where the compute happens
class Loss(nn.Module):
    def __init__(self, tp_pg: dist.ProcessGroup):
        super().__init__()
        self.tp_pg = tp_pg

    def forward(
        self,
        sharded_logits: torch.Tensor,  # (batch_size, length, logits)
        label_ids: torch.Tensor,  # (batch_size, length)
        label_mask: torch.Tensor,  # (batch_size, length)
    ) -> Dict[str, torch.Tensor]:
        loss = sharded_cross_entropy(sharded_logits, label_ids, group=self.tp_pg, dtype=torch.float)
        # TODO @thomasw21: It's unclear what kind of normalization we want to do.
        loss = (loss * label_mask).sum(dtype=torch.float) / label_mask.sum()
        return {"loss": loss}


class GPTForTraining(nn.Module):
    def __init__(
        self,
        config: GPT2Config,
        dpg: DistributedProcessGroups,
        parallel_config: Optional[ParallelismArgs],
        random_states: RandomStates,
    ):
        super().__init__()
        self.model = GPTModel(config=config, dpg=dpg, parallel_config=parallel_config, random_states=random_states)
        self.loss = PipelineBlock(
            p2p=self.model.p2p,
            module_builder=Loss,
            module_kwargs={"tp_pg": dpg.tp_pg},
            module_input_keys={
                "sharded_logits",
                "label_ids",
                "label_mask",
            },
            module_output_keys={"loss"},
        )

    def forward(
        self,
        input_ids: Union[torch.Tensor, TensorPointer],
        input_mask: Union[torch.Tensor, TensorPointer],
        label_ids: Union[torch.Tensor, TensorPointer],
        label_mask: Union[torch.Tensor, TensorPointer],
    ) -> Union[torch.Tensor, TensorPointer]:
        sharded_logits = self.model(
            input_ids=input_ids,
            input_mask=input_mask,
        )
        return self.loss(
            sharded_logits=sharded_logits,
            label_ids=label_ids,
            label_mask=label_mask,
        )["loss"]
