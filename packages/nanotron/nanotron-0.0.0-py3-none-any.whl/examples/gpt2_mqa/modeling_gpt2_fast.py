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
""" PyTorch GPT model with Multi-Query Attention.

In order to use this, you can just set `export USE_FAST=1`

Some dependencies to update before using:
 - install `apex`
 - install `torch>=2.0`
 - install `flash-attn>=2.0`
"""
import math
from typing import Dict, Optional, Tuple, Union

import torch
from apex.normalization import FusedLayerNorm as LayerNorm
from config import ModelArgs, ParallelismArgs, RecomputeGranularity
from flash_attn.flash_attn_interface import flash_attn_varlen_func
from torch import nn
from torch.nn import functional as F
from torch.nn import init
from transformers.activations import ACT2FN

from brrr.core import distributed as dist
from brrr.core.dataclass import RandomStates
from brrr.core.distributed import get_global_rank
from brrr.core.parallelism.parameters import BRRRParameter
from brrr.core.parallelism.pipeline_parallelism.block import PipelineBlock, TensorPointer
from brrr.core.parallelism.pipeline_parallelism.p2p import P2P
from brrr.core.parallelism.sharded_parameters import SplitConfig, mark_all_parameters_in_module_as_sharded
from brrr.core.parallelism.tensor_parallelism.enum import TensorParallelLinearMode
from brrr.core.parallelism.tensor_parallelism.functional import column_linear, sharded_cross_entropy
from brrr.core.parallelism.tensor_parallelism.nn import (
    TensorParallelColumnLinear,
    TensorParallelEmbedding,
    TensorParallelRowLinear,
)
from brrr.core.parallelism.tied_parameters import create_tied_parameter
from brrr.core.process_groups_initializer import DistributedProcessGroups
from brrr.core.random import branch_random_state
from brrr.core.utils import checkpoint_method
from brrr.store import AttachableStore


class MLP(nn.Module):
    def __init__(
        self,
        config: ModelArgs,
        parallel_config: Optional[ParallelismArgs],
        tp_pg: dist.ProcessGroup,
    ):
        super().__init__()

        # TODO @thomasw21: refactor so that we store that default in a single place.
        tp_mode = parallel_config.tp_mode if parallel_config is not None else TensorParallelLinearMode.ALL_REDUCE
        tp_linear_async_communication = (
            parallel_config.tp_linear_async_communication if parallel_config is not None else False
        )

        d_ff = config.ffn_hidden_size
        self.c_fc = TensorParallelColumnLinear(
            config.hidden_size,
            d_ff,
            pg=tp_pg,
            mode=tp_mode,
            bias=True,
            async_communication=tp_linear_async_communication,
        )
        self.act = torch.jit.script(ACT2FN[config.activation_function])
        self.c_proj = TensorParallelRowLinear(
            d_ff,
            config.hidden_size,
            pg=tp_pg,
            mode=tp_mode,
            bias=True,
            async_communication=tp_linear_async_communication and tp_mode is TensorParallelLinearMode.REDUCE_SCATTER,
        )

    def forward(self, hidden_states):  # [seq_length, batch_size, hidden_dim]
        hidden_states = self.c_fc(hidden_states)
        hidden_states = self.act(hidden_states)
        hidden_states = self.c_proj(hidden_states)
        return {"hidden_states": hidden_states}


class CoreMQA(nn.Module):
    """
    Attention module similar to CoreAttention where only the query is multi-headed.
    """

    def __init__(self, config: ModelArgs, parallel_config: Optional[ParallelismArgs], layer_idx: int):
        super().__init__()
        assert (
            config.hidden_size % config.num_attention_heads == 0
        ), f"Hidden size {config.hidden_size} must be divisible by number of attention heads {config.num_attention_heads}."
        self.d_qk = config.hidden_size // config.num_attention_heads
        # we still divide the value dimension by the number of heads https://arxiv.org/pdf/1911.02150.pdf
        self.d_v = config.hidden_size // config.num_attention_heads
        self.dropout = config.attn_pdrop

        assert config.scale_attn_weights, "Scale is only supported in torch 2.1.0"
        # self.scale_factor = 1.0
        # if config.scale_attn_weights:
        #     self.scale_factor = self.scale_factor / (self.d_qk**0.5)

        self.checkpoint_attention = (
            parallel_config is not None and parallel_config.recompute_granularity is RecomputeGranularity.SELECTIVE
        )

    @checkpoint_method(attr_name="checkpoint_attention")
    def forward(
        self,
        query_states: torch.Tensor,  # [batch_size * q_length, num_heads, inner_dim]
        key_states: torch.Tensor,  # [batch_size * kv_length, 1, inner_dim]
        value_states: torch.Tensor,  # [batch_size * kv_length, 1, inner_dim]
        q_sequence_mask: torch.Tensor,  # torch.BoolTensor [batch_size, q_length] (can be broadcasted to that size)
        kv_sequence_mask: torch.Tensor,  # torch.BoolTensor [batch_size, kv_length] (can be broadcasted to that size)
    ):
        # #  we will uncomment as soon as I can use it.
        # with sdp_kernel(enable_flash=True, enable_math=False, enable_mem_efficient=True):
        #     attn_output = scaled_dot_product_attention(
        #         query=query_states,
        #         key=key_states,
        #         value=value_states,
        #         attn_mask=attention_mask,
        #         dropout_p=self.dropout,
        #         is_causal=False,  # We pass `attn_mask` instead
        #         # scale=self.scale # This is only going to be supported in torch 2.1.0
        #     )

        # TODO @thomasw21: Compute once, instead of computing for each layers.
        cu_seqlens_q = torch.zeros((q_sequence_mask.shape[0] + 1), dtype=torch.int32, device=query_states.device)
        cu_seqlens_k = torch.zeros((kv_sequence_mask.shape[0] + 1), dtype=torch.int32, device=query_states.device)
        torch.cumsum(q_sequence_mask.sum(-1, dtype=torch.int32), dim=0, dtype=torch.int32, out=cu_seqlens_q[1:])
        torch.cumsum(kv_sequence_mask.sum(-1, dtype=torch.int32), dim=0, dtype=torch.int32, out=cu_seqlens_k[1:])

        # TODO(kunhao): flash attn's causal means that the query can only attend to the keys before it. This is not
        # what we want if we are using kv cache. This is a hack as we always have q_length == 1 when using kv cache.
        causal = False if q_sequence_mask.shape[1] == 1 else True
        attn_output = flash_attn_varlen_func(
            q=query_states,
            k=key_states,
            v=value_states,
            cu_seqlens_q=cu_seqlens_q,
            cu_seqlens_k=cu_seqlens_k,
            max_seqlen_q=q_sequence_mask.shape[1],
            max_seqlen_k=kv_sequence_mask.shape[1],
            dropout_p=self.dropout if self.training else 0.0,
            softmax_scale=None,  # This already defaults to the scale I'm interested in
            causal=causal,
            return_attn_probs=False,
        )

        return attn_output


# Hack to propagage gradient correctly
def get_sliced_parameter(coalesced_tensor: torch.Tensor, slice_object: slice):
    with torch.no_grad():
        # This allows us to create a leaf tensor, despite sharing the underlying storage
        result = BRRRParameter(tensor=coalesced_tensor[slice_object])

    # We need sliced tensor to also get the gradient in order to run optimizer on them
    # TODO @thomasw21: It's really had to make sure that our sliced view keeps the same memory space as the original gradient
    def get_grad_view(orig_grad):
        assert orig_grad.is_contiguous()
        if result.grad is None:
            # The gradient was reset to None, we need to reset the coalesced_tensor.grad as well
            coalesced_tensor.grad = None

        # TODO @thomasw21: Can I trigger hooks that we've set in `register_hook`
        if coalesced_tensor.grad is None:
            result.grad = orig_grad[slice_object]
        else:
            result.grad = coalesced_tensor.grad[slice_object]
        return orig_grad

    # If `coalesced_tensor` requires gradient, then we need to update the `result` grad attribute upon backward step.
    if coalesced_tensor.requires_grad is True:
        coalesced_tensor.register_hook(get_grad_view)
    return result


class _MQAColumnLinearReduceScatterAsyncCommunication(torch.autograd.Function):
    """This computes `q` and `kv` computation in MQA setting.

    Basic assumptions:
     - `kv.weight` and `kv.bias` (if not None) are duplicated across tp_pg
     - `tp_mode` is REDUCE_SCATTER
     - `async_communication` is set to True

    What this function does:
     - in the forward pass:
       - overlap input `all_gather` with `kv` computation
       - overlap kv output `all_gather` with `q` computation
     - in the backward pass:
       - overlap input `all_gather` with gradient_input computation
       - overlap gradient_input `reduce_scatter` with `kv` and `q` gradient computation
    """

    @staticmethod
    def forward(
        ctx,
        x: torch.Tensor,
        q_weight: torch.Tensor,
        q_bias: Optional[torch.Tensor],
        kv_weight: torch.Tensor,
        kv_bias: Optional[torch.Tensor],
        # Basically we assume that `qkv_weight` is already the concatenated version of `q.weight` and `kv.weight`
        qkv_weight: torch.Tensor,
        tp_pg: dist.ProcessGroup,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        ctx.tp_pg = tp_pg
        ctx.use_q_bias = q_bias is not None
        ctx.use_kv_bias = kv_bias is not None
        ctx.split_q_and_kv_id = q_weight.shape[0]

        # All gather x if needed
        gathered_x: torch.Tensor
        gather_x_handle: Optional[dist.Work] = None
        if tp_pg.size() == 1:
            gathered_x = x
        else:
            first_dim = x.shape[0]
            last_dims = x.shape[1:]

            unsharded_first_dim = first_dim * tp_pg.size()

            gathered_x = torch.empty(
                unsharded_first_dim,
                *last_dims,
                device=x.device,
                dtype=x.dtype,
                requires_grad=x.requires_grad,
            )

            # `tensor` can sometimes not be contiguous
            # https://cs.github.com/pytorch/pytorch/blob/2b267fa7f28e18ca6ea1de4201d2541a40411457/torch/distributed/nn/functional.py#L317
            x = x.contiguous()

            gather_x_handle = dist.all_gather_into_tensor(gathered_x, x, group=tp_pg, async_op=True)

        # Compute kv (we assume that kv is duplicated across TP)
        kv_out = F.linear(x, kv_weight, kv_bias)

        # Wait for communication to finish
        if gather_x_handle is not None:
            gather_x_handle.wait()

        # All gather `kv` output
        gathered_kv_out: torch.Tensor
        gather_kv_out_handle: Optional[dist.Work] = None
        if tp_pg.size() == 1:
            gathered_kv_out = kv_out
        else:
            first_dim = kv_out.shape[0]
            last_dims = kv_out.shape[1:]

            unsharded_first_dim = first_dim * tp_pg.size()

            gathered_kv_out = torch.empty(
                unsharded_first_dim,
                *last_dims,
                device=x.device,
                dtype=x.dtype,
                requires_grad=x.requires_grad,
            )

            gather_kv_out_handle = dist.all_gather_into_tensor(gathered_kv_out, kv_out, group=tp_pg, async_op=True)

        # Compute q
        q_out = F.linear(gathered_x, q_weight, q_bias)

        # Wait for communication to finish
        if gather_kv_out_handle is not None:
            gather_kv_out_handle.wait()

        ctx.save_for_backward(x, qkv_weight)

        return q_out, gathered_kv_out

    @staticmethod
    def backward(
        ctx, grad_q: torch.Tensor, grad_kv: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor, Optional[torch.Tensor], torch.Tensor, Optional[torch.Tensor], None, None]:
        tp_pg = ctx.tp_pg
        split_q_and_kv_id = ctx.split_q_and_kv_id
        use_q_bias = ctx.use_q_bias
        use_kv_bias = ctx.use_kv_bias

        x, qkv_weight = ctx.saved_tensors

        # Gather `x`
        gathered_x: torch.Tensor
        gather_x_handle: Optional[dist.Work] = None
        if tp_pg.size() == 1:
            gathered_x = x
        else:
            first_dim = x.shape[0]
            last_dims = x.shape[1:]
            unsharded_batch_size = first_dim * tp_pg.size()

            gathered_x = torch.empty(
                unsharded_batch_size,
                *last_dims,
                device=x.device,
                dtype=x.dtype,
                requires_grad=False,
            )
            gather_x_handle = dist.all_gather_into_tensor(gathered_x, x, group=tp_pg, async_op=True)

        # Backward computation on `kv` and `q` with regards to input
        grad_qkv = torch.concat([grad_q, grad_kv], dim=-1)
        grad_tensor = grad_qkv.matmul(qkv_weight)

        # Wait for gather `x` to finish
        if gather_x_handle is not None:
            gather_x_handle.wait()

        # Reduce scatter gradients with regards to input
        sub_gradient_tensor: torch.Tensor
        sub_gradient_tensor_handle: Optional[dist.Work] = None
        if tp_pg.size() == 1:
            sub_gradient_tensor = grad_tensor
        else:
            sub_gradient_tensor = torch.empty(
                x.shape, dtype=grad_tensor.dtype, device=grad_tensor.device, requires_grad=False
            )
            # reduce_scatter
            sub_gradient_tensor_handle = dist.reduce_scatter_tensor(
                sub_gradient_tensor, grad_tensor, group=tp_pg, async_op=True
            )

        # Backward computation for `q` and `kv` with regards to
        # flat_gathered_x = gathered_x.view(math.prod(gathered_x.shape[:-1]), gathered_x.shape[-1])
        # flat_grad_kv = grad_kv.reshape(math.prod(grad_kv.shape[:-1]), grad_kv.shape[-1])
        # flat_grad_q = grad_q.reshape(math.prod(grad_q.shape[:-1]), grad_q.shape[-1])
        # grad_kv_weight = flat_grad_kv.t().matmul(flat_gathered_x)
        # grad_kv_bias = flat_grad_kv.sum(dim=0) if use_kv_bias else None
        # grad_q_weight = flat_grad_q.t().matmul(flat_gathered_x)
        # grad_q_bias = flat_grad_q.sum(dim=0) if use_q_bias else None

        flat_gathered_x = gathered_x.view(math.prod(gathered_x.shape[:-1]), gathered_x.shape[-1])
        flat_grad_qkv = grad_qkv.view(math.prod(grad_qkv.shape[:-1]), grad_qkv.shape[-1])
        grad_q_weight, grad_kv_weight = torch.split(
            flat_grad_qkv.t().matmul(flat_gathered_x),
            split_size_or_sections=[split_q_and_kv_id, grad_qkv.shape[-1] - split_q_and_kv_id],
            dim=0,
        )
        if use_q_bias is True:
            if use_kv_bias is True:
                grad_qkv_bias = flat_grad_qkv.sum(dim=0)
                grad_q_bias, grad_kv_bias = torch.split(
                    grad_qkv_bias,
                    split_size_or_sections=[split_q_and_kv_id, grad_qkv.shape[-1] - split_q_and_kv_id],
                    dim=0,
                )
            else:
                grad_kv_bias = None
                grad_q_bias = flat_grad_qkv[:, :split_q_and_kv_id].sum(dim=0)
        else:
            grad_q_bias = None
            if use_kv_bias is False:
                grad_kv_bias = flat_grad_qkv[:, split_q_and_kv_id:].sum(dim=0)
            else:
                grad_kv_bias = None

        # Wait for `reduce_scatter`
        if sub_gradient_tensor_handle is not None:
            sub_gradient_tensor_handle.wait()

        return sub_gradient_tensor, grad_q_weight, grad_q_bias, grad_kv_weight, grad_kv_bias, None, None


class MQAColumnLinears(nn.Module):
    def __init__(
        self,
        in_features: int,
        q_out_features: int,
        kv_out_features: int,
        pg: dist.ProcessGroup,
        mode: TensorParallelLinearMode,
        bias=True,
        device=None,
        dtype=None,
        async_communication: bool = False,
    ):
        super().__init__()
        self.pg = pg
        self.world_size = pg.size()

        assert in_features % self.world_size == 0

        self.in_features = in_features
        self.q_out_features = q_out_features // self.world_size
        self.kv_out_features = kv_out_features

        # Tp mode
        self.mode = mode
        self.async_communication = async_communication
        self.use_MQAColumnLinearReduceScatterAsyncCommunication = (
            self.mode is TensorParallelLinearMode.REDUCE_SCATTER and self.async_communication is True
        )

        # allocating tensor
        # We don't need to make them persistent as we expose this storage via `self.q` and `self.kv`
        self.register_buffer(
            "_qkv_weight",
            torch.empty(
                self.q_out_features + self.kv_out_features,
                self.in_features,
                device=device,
                dtype=dtype,
                # We use another specific path that doesn't use `_qkv_weight`
                requires_grad=not self.use_MQAColumnLinearReduceScatterAsyncCommunication,
            ),
            persistent=False,
        )
        if bias is True:
            self.register_buffer(
                "_qkv_bias",
                torch.empty(
                    self.q_out_features + self.kv_out_features,
                    device=device,
                    dtype=dtype,
                    requires_grad=not self.use_MQAColumnLinearReduceScatterAsyncCommunication,
                ),
                persistent=False,
            )
        else:
            self._qkv_bias = None

        # Register parameters
        # We are very lucky because the sharding allows parameters to still be contiguous.
        # We use a hack to propagate gradients
        q_param_dict = {"weight": get_sliced_parameter(self._qkv_weight, slice_object=slice(self.q_out_features))}
        kv_param_dict = {
            "weight": get_sliced_parameter(self._qkv_weight, slice_object=slice(self.q_out_features, None))
        }
        if bias is True:
            q_param_dict["bias"] = get_sliced_parameter(self._qkv_bias, slice_object=slice(self.q_out_features))
            kv_param_dict["bias"] = get_sliced_parameter(self._qkv_bias, slice_object=slice(self.q_out_features, None))
        self.q = nn.ParameterDict(q_param_dict)
        self.kv = nn.ParameterDict(kv_param_dict)

        # Marking as tied/sharded
        mark_all_parameters_in_module_as_sharded(self.q, pg=self.pg, split_config=SplitConfig(split_dim=0))
        self._mark_kv_parameters_in_module_as_tied()

        # Init
        self.reset_parameters()

    def reset_parameters(self) -> None:
        """Copied from nn.Linear.reset_parameters"""
        # Setting a=sqrt(5) in kaiming_uniform is the same as initializing with
        # uniform(-1/sqrt(in_features), 1/sqrt(in_features)). For details, see
        # https://github.com/pytorch/pytorch/issues/57109
        init.kaiming_uniform_(self._qkv_weight, a=math.sqrt(5))
        if self._qkv_bias is not None:
            fan_in, _ = init._calculate_fan_in_and_fan_out(self._qkv_weight)
            bound = 1 / math.sqrt(fan_in) if fan_in > 0 else 0
            init.uniform_(self._qkv_bias, -bound, bound)

    def _mark_kv_parameters_in_module_as_tied(self):
        for name, param in list(self.kv.named_parameters()):
            new_param = create_tied_parameter(
                parameter=param,
                name=name,
                global_ranks=tuple(sorted((get_global_rank(self.pg, i) for i in range(self.pg.size())))),
                # Always has to be ReduceOp SUM as now this is always duplicated regardless of tp mode
                reduce_op=dist.ReduceOp.SUM,
                root_module=self.kv,
            )
            setattr(self.kv, name, new_param)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        if self.use_MQAColumnLinearReduceScatterAsyncCommunication:
            assert self._qkv_weight.requires_grad is False
            assert self._qkv_bias is None or self._qkv_bias.requires_grad is False
            return _MQAColumnLinearReduceScatterAsyncCommunication.apply(
                x, self.q.weight, self.q.bias, self.kv.weight, self.kv.bias, self._qkv_weight, self.pg
            )
        qkv = column_linear(
            input=x,
            weight=self._qkv_weight,
            bias=self._qkv_bias,
            group=self.pg,
            tp_mode=self.mode,
            async_communication=self.async_communication,
        )
        q, kv = torch.split(qkv, dim=-1, split_size_or_sections=[self.q_out_features, self.kv_out_features])
        return q, kv


class CausalSelfMQA(nn.Module, AttachableStore):
    def __init__(
        self,
        config: ModelArgs,
        parallel_config: Optional[ParallelismArgs],
        tp_pg: dist.ProcessGroup,
        layer_idx: int,
    ):
        super().__init__()
        # Tensor parallel considerations: We split tensors along head dimension
        assert (
            config.num_attention_heads % tp_pg.size() == 0
        ), f"Number of attention heads ({config.num_attention_heads}) must be divisible by TP size ({tp_pg.size()})."
        self.tp_pg_size = tp_pg.size()
        self.n_heads = config.num_attention_heads // tp_pg.size()
        self.d_qk = config.hidden_size // config.num_attention_heads
        self.d_v = config.hidden_size // config.num_attention_heads
        self.d_model = config.hidden_size

        # TODO @thomasw21: refactor so that we store that default in a single place.
        tp_mode = parallel_config.tp_mode if parallel_config is not None else TensorParallelLinearMode.ALL_REDUCE
        tp_linear_async_communication = (
            parallel_config.tp_linear_async_communication if parallel_config is not None else False
        )

        self.mode = tp_mode
        self.pg = tp_pg

        # only Q_size is parallelized
        self.qkv = MQAColumnLinears(
            in_features=self.d_model,
            q_out_features=config.num_attention_heads * self.d_qk,
            kv_out_features=self.d_qk + self.d_v,
            pg=tp_pg,
            mode=tp_mode,
            bias=True,
            async_communication=tp_linear_async_communication,
        )

        self.o = TensorParallelRowLinear(
            config.num_attention_heads * self.d_v,
            self.d_model,
            pg=tp_pg,
            mode=tp_mode,
            bias=True,
            async_communication=tp_linear_async_communication and tp_mode is TensorParallelLinearMode.REDUCE_SCATTER,
        )

        self.attention = CoreMQA(
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
            kv_states,  # [kv_length, batch_size, d_qk + d_v]
        ):
            # # Shaping for use in torch version of flash-attn: `scaled_dot_product_attention`
            # q_length, batch_size = query_states.shape[:2]
            # kv_length = query_states.shape[0]
            # query_states = query_states.view(
            #     q_length, batch_size, self.n_heads, self.d_qk
            # )  # [q_length, batch_size, num_heads,  d_qk]
            # query_states = query_states.permute(1, 2, 0, 3).contiguous()  # [batch_size, num_heads, q_length, d_qk]
            # key_states, value_states = torch.split(
            #     kv_states, [self.d_qk, self.d_v], dim=-1
            # )  # [kv_length, batch_size, d_qk], [kv_length, batch_size, d_v]
            # key_states = key_states.transpose(0, 1).contiguous().unsqueeze(dim=1)  # [batch_size, 1, kv_length, d_qk]
            # value_states = (
            #     value_states.transpose(0, 1).contiguous().unsqueeze(dim=1)
            # )  # [batch_size, 1, kv_length, d_v]
            # key_states = key_states.expand(
            #     batch_size, self.n_heads, kv_length, self.d_qk
            # )  # [batch_size, num_heads, kv_length, inner_dim]
            # value_states = value_states.expand(
            #     batch_size, self.n_heads, kv_length, self.d_v
            # )  # [batch_size, num_heads, kv_length, inner_dim]

            # Shaping for use in `flash-attn` version of flash-attn: `flash_attn_unpadded_func`
            q_length = query_states.shape[0]
            kv_length = kv_states.shape[0]
            query_states = query_states.view(
                q_length, batch_size, self.n_heads, self.d_qk
            )  # [q_length, batch_size, num_heads,  d_qk]
            query_states = (
                query_states.permute(1, 0, 2, 3).contiguous().view(batch_size * q_length, self.n_heads, self.d_qk)
            )  # [batch_size * q_length, num_heads, d_qk]
            key_states, value_states = torch.split(
                kv_states, [self.d_qk, self.d_v], dim=-1
            )  # [kv_length, batch_size, d_qk], [kv_length, batch_size, d_v]
            key_states = (
                key_states.transpose(0, 1).contiguous().view(batch_size * kv_length, self.d_qk).unsqueeze(dim=1)
            )  # [batch_size * kv_length, 1, d_qk]
            value_states = (
                value_states.transpose(0, 1).contiguous().view(batch_size * kv_length, self.d_v).unsqueeze(dim=1)
            )  # [batch_size * kv_length, 1, d_v]
            return query_states, key_states, value_states

        # get query/key/value states
        query_states, kv_states = self.qkv(
            hidden_states
        )  # [seq_length, batch_size, num_heads * d_qk], [seq_length, batch_size, d_qk + d_v]

        # Get cached key/values from store if available
        store = self.get_local_store()
        if store is not None:
            # Double check that we use store only at inference time
            assert kv_states.requires_grad is False

            # Pull pre-computed key/value states
            if "kv_states" in store:
                # We assume that "key"/"value"/"sequence_mask" are all added once initialized
                old_kv_states = store["kv_states"]
                old_kv_sequence_mask = store["kv_sequence_mask"]

                # Concatenate with new key/value on seq_length dim
                kv_states = torch.cat([old_kv_states, kv_states], dim=0)
                kv_sequence_mask = torch.concat([old_kv_sequence_mask, sequence_mask], dim=-1)
                q_sequence_mask = sequence_mask
            else:
                q_sequence_mask = sequence_mask
                kv_sequence_mask = sequence_mask

            # Store new key/value in store
            store.update({"kv_states": kv_states, "kv_sequence_mask": kv_sequence_mask})
        else:
            q_sequence_mask = sequence_mask
            kv_sequence_mask = sequence_mask

        query_states, key_states, value_states = shape(query_states=query_states, kv_states=kv_states)

        attention_output = self.attention(
            query_states=query_states,
            key_states=key_states,
            value_states=value_states,
            q_sequence_mask=q_sequence_mask,
            kv_sequence_mask=kv_sequence_mask,
        )  # [batch_size, num_heads, seq_length, d_v]

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
        config: ModelArgs,
        parallel_config: Optional[ParallelismArgs],
        tp_pg: dist.ProcessGroup,
        random_states: RandomStates,
        layer_idx: int,
    ):
        super(GPTBlock, self).__init__()
        self.ln_1 = LayerNorm(config.hidden_size, eps=config.layer_norm_epsilon)
        self.attn = CausalSelfMQA(
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
        hidden_states: Union[torch.Tensor, TensorPointer],
        sequence_mask: Union[torch.Tensor, TensorPointer],
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
    def __init__(self, tp_pg: dist.ProcessGroup, config: ModelArgs, parallel_config: Optional[ParallelismArgs]):
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
        self.pg = tp_pg

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
        config: ModelArgs,
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
                for layer_idx in range(config.num_layers)
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
                "async_communication": parallel_config.tp_linear_async_communication
                if parallel_config is not None
                else False,
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
        sharded_logits: torch.Tensor,  # [seq_length, batch_size, logits]
        label_ids: torch.Tensor,  # [batch_size, seq_length]
        label_mask: torch.Tensor,  # [batch_size, seq_length]
    ) -> Dict[str, torch.Tensor]:
        # Megatron by defaults cast everything in fp32. `--f16-lm-cross-entropy` is an option you can use to keep current precision.
        # https://github.com/NVIDIA/Megatron-LM/blob/f267e6186eae1d6e2055b412b00e2e545a8e896a/megatron/model/gpt_model.py#L38
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
        config: ModelArgs,
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
