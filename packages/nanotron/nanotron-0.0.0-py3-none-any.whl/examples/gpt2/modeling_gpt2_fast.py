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
""" PyTorch GPT model.

In order to use this, you can just set `export USE_FAST=1`

Some dependencies to update before using:
 - install `apex`
 - install `flash-attn>=2.0`
"""

from typing import Dict, Optional, Union

import torch
from apex.normalization import FusedLayerNorm as LayerNorm
from config import ParallelismArgs, RecomputeGranularity
from flash_attn.flash_attn_interface import flash_attn_varlen_func as flash_attn_unpadded_func
from torch import nn
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
        self.act = torch.jit.script(ACT2FN[config.activation_function])
        self.c_proj = TensorParallelRowLinear(d_ff, config.hidden_size, pg=tp_pg, mode=tp_mode, bias=True)

    def forward(self, hidden_states):  # [seq_length, batch_size, hidden_dim]
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

        self.scale_attn_by_inverse_layer_idx = config.scale_attn_by_inverse_layer_idx
        # Layer-wise attention scaling
        if config.scale_attn_by_inverse_layer_idx:
            self.scale_factor = self.scale_factor / float(layer_idx + 1)

        self.checkpoint_attention = (
            parallel_config is not None and parallel_config.recompute_granularity is RecomputeGranularity.SELECTIVE
        )

    @checkpoint_method(attr_name="checkpoint_attention")
    def forward(
        self,
        query_states: torch.Tensor,  # [batch_size * q_length, num_heads, inner_dim]
        key_states: torch.Tensor,  # [batch_size * kv_length, num_heads, inner_dim]
        value_states: torch.Tensor,  # [batch_size * kv_length, num_heads, inner_dim]
        q_sequence_mask: torch.Tensor,  # torch.BoolTensor [batch_size, q_length] (can be broadcasted to that size)
        kv_sequence_mask: torch.Tensor,  # torch.BoolTensor [batch_size, kv_length] (can be broadcasted to that size)
    ):
        # TODO @thomasw21: Compute once, instead of computing for each layers.
        cu_seqlens_q = torch.zeros((q_sequence_mask.shape[0] + 1), dtype=torch.int32, device=query_states.device)
        cu_seqlens_k = torch.zeros((kv_sequence_mask.shape[0] + 1), dtype=torch.int32, device=query_states.device)
        torch.cumsum(q_sequence_mask.sum(-1, dtype=torch.int32), dim=0, dtype=torch.int32, out=cu_seqlens_q[1:])
        torch.cumsum(kv_sequence_mask.sum(-1, dtype=torch.int32), dim=0, dtype=torch.int32, out=cu_seqlens_k[1:])

        # TODO(kunhao): flash attn's causal means that the query can only attend to the keys before it. This is not
        # what we want if we are using kv cache. This is a hack as we always have q_length == 1 when using kv cache.
        causal = False if q_sequence_mask.shape[1] == 1 else True
        attn_output = flash_attn_unpadded_func(
            q=query_states,
            k=key_states,
            v=value_states,
            cu_seqlens_q=cu_seqlens_q,
            cu_seqlens_k=cu_seqlens_k,
            max_seqlen_q=q_sequence_mask.shape[1],
            max_seqlen_k=kv_sequence_mask.shape[1],
            dropout_p=self.dropout if self.training else 0.0,
            softmax_scale=self.scale_factor
            if self.scale_attn_by_inverse_layer_idx
            else None,  # This already defaults to the scale I'm interested in
            causal=causal,
            return_attn_probs=False,
        )

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
        hidden_states,  # [seq_length, batch_size, hidden_dim]
        sequence_mask,  # [batch_size, seq_length]
    ):
        batch_size = hidden_states.shape[1]

        def unshape(states):
            """Given a [batch_dim * seq_length, num_heads, d_v] returns a [seq_length, batch_dim, num_heads * d_v]"""
            total = states.shape[0]
            assert total % batch_size == 0
            seq_length = total // batch_size
            return (
                states.view(batch_size, seq_length, self.n_heads, self.d_v)
                .transpose(0, 1)
                .contiguous()
                .view(seq_length, batch_size, self.n_heads * self.d_v)
            )

        def shape(
            query_states,  # [q_length, batch_size, num_heads * d_qk]
            key_states,  # [kv_length, batch_size, num_heads * d_qk]
            value_states,  # [kv_length, batch_size, num_heads * d_v]
        ):
            # Shaping for use in `flash-attn` version of flash-attn: `flash_attn_unpadded_func`
            q_len = query_states.shape[0]
            kv_len = key_states.shape[0]
            # [batch_size * q_length, num_heads, d_qk]
            query_states = query_states.transpose(0, 1).contiguous().view(batch_size * q_len, self.n_heads, self.d_qk)
            # [batch_size * kv_length, num_heads, d_qk]
            key_states = key_states.transpose(0, 1).contiguous().view(batch_size * kv_len, self.n_heads, self.d_qk)
            # [batch_size * kv_length, num_heads, d_v]
            value_states = value_states.transpose(0, 1).contiguous().view(batch_size * kv_len, self.n_heads, self.d_v)
            return query_states, key_states, value_states

        qkv_states = self.qkv(hidden_states)  # [seq_length, batch_size, num_heads * 3 * d_qk]
        query_states, key_states, value_states = torch.split(
            qkv_states, self.n_heads * self.d_qk, dim=-1
        )  # [seq_length, batch_size, num_heads * d_qk]

        # Get cached key/values from store if available
        store = self.get_local_store()
        if store is not None:
            # Double check that we use store only at inference time
            assert key_states.requires_grad is False
            assert value_states.requires_grad is False

            # Pull pre-computed key/value states
            if "key_states" in store:
                # We assume that "key"/"value"/"sequence_mask" are all added once initialized
                old_key_states = store["key_states"]
                old_value_states = store["value_states"]
                old_kv_sequence_mask = store["kv_sequence_mask"]

                # Concatenate with new key/value on seq_length dim
                key_states = torch.cat([old_key_states, key_states], dim=0)
                value_states = torch.cat([old_value_states, value_states], dim=0)
                kv_sequence_mask = torch.concat([old_kv_sequence_mask, sequence_mask], dim=-1)
                q_sequence_mask = sequence_mask
            else:
                q_sequence_mask = sequence_mask
                kv_sequence_mask = sequence_mask

            # Store new key/value in store
            store.update(
                {"key_states": key_states, "value_states": value_states, "kv_sequence_mask": kv_sequence_mask}
            )
        else:
            q_sequence_mask = sequence_mask
            kv_sequence_mask = sequence_mask

        # Shape for multi-head attention
        query_states, key_states, value_states = shape(query_states, key_states, value_states)

        attention_output = self.attention(
            query_states=query_states,
            key_states=key_states,
            value_states=value_states,
            q_sequence_mask=q_sequence_mask,
            kv_sequence_mask=kv_sequence_mask,
        )

        output = self.o(unshape(attention_output))

        return {"hidden_states": output, "sequence_mask": sequence_mask}


def dropout_add(x, residual, prob, training):
    # type: (Tensor, Tensor, float, bool) -> Tensor
    # From: https://github.com/NVIDIA/Megatron-LM/blob/285068c8108e0e8e6538f54fe27c3ee86c5217a2/megatron/model/transformer.py#L586
    out = torch.nn.functional.dropout(x, p=prob, training=training)
    out = residual + out
    return out


@torch.jit.script
def dropout_add_fused_train(x: torch.Tensor, residual: torch.Tensor, prob: float) -> torch.Tensor:
    return dropout_add(x, residual, prob, True)


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
        self.attn_dropout = config.attn_pdrop

        self.ln_2 = LayerNorm(config.hidden_size, eps=config.layer_norm_epsilon)
        self.ff = MLP(config=config, parallel_config=parallel_config, tp_pg=tp_pg)
        self.ff_dropout = config.resid_pdrop

        self.random_states = random_states
        self.tp_mode = parallel_config.tp_mode if parallel_config is not None else TensorParallelLinearMode.ALL_REDUCE

    def forward(
        self,
        hidden_states: Union[torch.Tensor, TensorPointer],  # [seq_length, batch_size, hidden_dim]
        sequence_mask: Union[torch.Tensor, TensorPointer],  # [batch_size, seq_length]
    ) -> Dict[str, Union[torch.Tensor, TensorPointer]]:
        residual = hidden_states
        hidden_states = self.ln_1(hidden_states)
        output = self.attn(hidden_states=hidden_states, sequence_mask=sequence_mask)
        hidden_states = output["hidden_states"]

        if self.training:
            with branch_random_state(
                self.random_states, "tp_synced", enabled=self.tp_mode is TensorParallelLinearMode.ALL_REDUCE
            ):
                hidden_states = dropout_add_fused_train(hidden_states, residual=residual, prob=self.attn_dropout)
        else:
            # No need for random state context manager
            hidden_states = hidden_states + residual

        residual = hidden_states
        hidden_states = self.ln_2(hidden_states)
        hidden_states = self.ff(hidden_states=hidden_states)["hidden_states"]

        if self.training:
            with branch_random_state(
                self.random_states, "tp_synced", enabled=self.tp_mode is TensorParallelLinearMode.ALL_REDUCE
            ):
                hidden_states = dropout_add_fused_train(hidden_states, residual=residual, prob=self.ff_dropout)
        else:
            # No need for random state context manager
            hidden_states = hidden_states + residual
        return {
            "hidden_states": hidden_states,
            "sequence_mask": output["sequence_mask"],
        }


class Embedding(nn.Module, AttachableStore):
    def __init__(self, tp_pg: dist.ProcessGroup, config: GPT2Config, parallel_config: Optional[ParallelismArgs]):
        super().__init__()
        self.token_embedding = TensorParallelEmbedding(
            num_embeddings=config.vocab_size,
            embedding_dim=config.hidden_size,
            pg=tp_pg,
            mode=parallel_config.tp_mode if parallel_config is not None else TensorParallelLinearMode.ALL_REDUCE,
        )
        self.position_embedding = TensorParallelEmbedding(
            num_embeddings=config.max_position_embeddings,
            embedding_dim=config.hidden_size,
            pg=tp_pg,
            mode=parallel_config.tp_mode if parallel_config is not None else TensorParallelLinearMode.ALL_REDUCE,
        )

    def forward(self, input_ids: torch.Tensor, input_mask: torch.Tensor):  # [batch_size, seq_length]
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
        position_ids.masked_fill_(input_mask == 0, 0)

        batch_size, seq_length = input_ids.shape

        # Format input in `[seq_length, batch_size]` to support high TP with low batch_size
        input_ids = input_ids.transpose(0, 1)
        position_ids = position_ids.transpose(0, 1)
        input_embeds = self.token_embedding(input_ids)
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
        input_ids: Union[torch.Tensor, TensorPointer],  # [batch_size, seq_length]
        input_mask: Union[torch.Tensor, TensorPointer],  # [batch_size, seq_length]
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


@torch.jit.script
def masked_mean(loss, label_mask, dtype):
    # type: (Tensor, Tensor, torch.dtype) -> Tensor
    return (loss * label_mask).sum(dtype=dtype) / label_mask.sum()


# TODO @thomasw21: It's a bit weird that our loss needs to be wrapped inside a `nn.Module`. The issue is that PipelineBlock essentially defines where the compute happens
class Loss(nn.Module):
    def __init__(self, tp_pg: dist.ProcessGroup):
        super().__init__()
        self.tp_pg = tp_pg

    def forward(
        self,
        sharded_logits: torch.Tensor,  # [batch_size, seq_length, logits]
        label_ids: torch.Tensor,  # [batch_size, seq_length]
        label_mask: torch.Tensor,  # [batch_size, seq_length]
    ) -> Dict[str, torch.Tensor]:
        loss = sharded_cross_entropy(
            sharded_logits, label_ids.transpose(0, 1).contiguous(), group=self.tp_pg, dtype=torch.float
        ).transpose(0, 1)
        # TODO @thomasw21: It's unclear what kind of normalization we want to do.
        loss = masked_mean(loss, label_mask, dtype=torch.float)
        # I think indexing causes a sync we don't actually want
        # loss = loss[label_mask].sum()
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
