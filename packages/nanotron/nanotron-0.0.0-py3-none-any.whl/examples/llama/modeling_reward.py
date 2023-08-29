""" PyTorch Reward model.

In order to use this, you can just set `export USE_FAST=1`

"""


import os
from typing import Dict, Optional, Union

import torch
from config import PPOParallelismArgs as ParallelismArgs
from torch import nn
from transformers import LlamaConfig

from brrr.core import distributed as dist
from brrr.core import logging
from brrr.core.parallelism.pipeline_parallelism.block import PipelineBlock, TensorPointer
from brrr.core.process_groups_initializer import DistributedProcessGroups

logger = logging.get_logger(__name__)
if os.environ.get("USE_FAST"):
    # We import the fast versions
    raise NotImplementedError("Masked inputs not supported yet when using `USE_FAST=1`")
    from modeling_llama_fast import LlamaModel
else:
    from modeling_llama import LlamaModel


class Loss(nn.Module):
    def __init__(self, tp_pg: dist.ProcessGroup):
        super().__init__()
        self.tp_pg = tp_pg

    def forward(
        self,
        policy_logits: torch.Tensor,  # [seq_length, chosen_bsz + rejected_bsz, vocab_size]
        chosen_rejected_sep_idx: torch.Tensor,  # [1]
    ) -> Dict[str, torch.Tensor]:

        policy_logits = policy_logits.transpose(
            0, 1
        ).contiguous()  # [chosen_bsz + rejected_bsz, seq_length, vocab_size]

        policy_chosen_logits = policy_logits[:chosen_rejected_sep_idx]  # [chosen_bsz, seq_length, vocab_size]
        policy_rejected_logits = policy_logits[chosen_rejected_sep_idx:]  # [rejected_bsz, seq_length, vocab_size]

        losses = -torch.nn.functional.logsigmoid(policy_chosen_logits - policy_rejected_logits).mean()

        stats = {
            "logits": {
                "rejected": policy_rejected_logits.detach().mean(),
                "chosen": policy_chosen_logits.detach().mean(),
            },
        }

        return {"loss": losses.mean(), **flatten_dict(stats)}


class RewardForTraining(nn.Module):
    def __init__(
        self,
        config: LlamaConfig,
        dpg: DistributedProcessGroups,
        parallel_config: Optional[ParallelismArgs],
    ):
        super().__init__()
        self.model = LlamaModel(config=config, dpg=dpg, parallel_config=parallel_config)

        self.loss = PipelineBlock(
            p2p=self.model.p2p,
            module_builder=Loss,
            module_kwargs={"tp_pg": dpg.tp_pg},
            module_input_keys={"chosen_rejected_sep_idx", "policy_logits"},
            module_output_keys={
                "loss",
                "logits/rejected",
                "logits/chosen",
            },
        )

    def forward(
        self,
        concatenated_input_ids: Union[torch.Tensor, TensorPointer],
        concatenated_attention_mask: Union[torch.Tensor, TensorPointer],
        chosen_rejected_sep_idx: Union[torch.Tensor, TensorPointer],
    ) -> Dict[str, Union[torch.Tensor, TensorPointer]]:
        policy_logits = self.model(
            concatenated_input_ids,  # (batch_size, sequence_length)
            concatenated_attention_mask,  # (batch_size, sequence_length)
        )  # (sequence_length, batch_size, vocab_size)
        # We return input_ids as well, to avoid having to communicate them from first rank

        return self.loss(
            policy_logits=policy_logits,
            chosen_rejected_sep_idx=chosen_rejected_sep_idx,
        )


def flatten_dict(nested, sep="/"):
    """Flatten dictionary and concatenate nested keys with separator."""

    def rec(nest, prefix, into):
        for k, v in nest.items():
            if sep in k:
                raise ValueError(f"separator '{sep}' not allowed to be in key '{k}'")
            if isinstance(v, dict):
                rec(v, prefix + k + sep, into)
            else:
                into[prefix + k] = v

    flat = {}
    rec(nested, "", flat)
    return flat
