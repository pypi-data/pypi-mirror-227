""" PyTorch PPO model.

In order to use this, you can just set `export USE_FAST=1`

"""


import json
import os
from typing import Dict, Optional, Union

import numpy as np
import torch
from config import PPOArgs
from config import PPOParallelismArgs as ParallelismArgs
from torch import nn
from transformers import LlamaConfig

from brrr.core import distributed as dist
from brrr.core import logging
from brrr.core.parallelism.pipeline_parallelism.block import PipelineBlock, TensorPointer
from brrr.core.parallelism.tensor_parallelism.functional import sharded_cross_entropy
from brrr.core.parallelism.tensor_parallelism.nn import (
    TensorParallelLinearMode,
)
from brrr.core.process_groups_initializer import DistributedProcessGroups

logger = logging.get_logger(__name__)
if os.environ.get("USE_FAST"):
    # We import the fast versions
    from modeling_llama_fast import LlamaModel
else:
    from modeling_llama import LlamaModel


def masked_mean(values, mask, axis=None):
    """Compute mean of tensor with a masked values."""
    if axis is not None:
        return (values * mask).sum(axis=axis) / mask.sum(axis=axis)
    else:
        return (values * mask).sum() / mask.sum()


def masked_mean_and_var(values, mask, unbiased=True):
    """Compute variance of tensor with masked values."""
    mean = masked_mean(values, mask)
    centered_values = values - mean
    variance = masked_mean(centered_values**2, mask)
    if unbiased:
        mask_sum = mask.sum()
        bessel_correction = mask_sum / (mask_sum - 1)
        # TODO @nouamane: we can compute unbiased variance directly
        variance = variance * bessel_correction
    return mean, variance


def masked_whiten(values, mask, shift_mean=True):
    """Whiten values with masked values."""
    mean, var = masked_mean_and_var(values, mask)
    whitened = (values - mean) * torch.rsqrt(var + 1e-8)
    if not shift_mean:
        whitened += mean
    return whitened


class Loss(nn.Module):
    def __init__(self, tp_pg: dist.ProcessGroup, ppo_config: PPOArgs):
        super().__init__()
        self.tp_pg = tp_pg
        self.gamma = ppo_config.gamma
        self.lam = ppo_config.lam
        self.cliprange_value = ppo_config.cliprange_value
        self.cliprange = ppo_config.cliprange
        self.vf_coef = ppo_config.vf_coef

    def forward(
        self,
        input_ids: torch.Tensor,  # [batch_size, seq_length]
        sharded_logits: torch.Tensor,  # [seq_length, batch_size, vocab_size]
        old_logits: torch.Tensor,  # [seq_length, batch_size, vocab_size]
        values: torch.Tensor,  # [seq_length, batch_size, 1]
        vpreds: torch.Tensor,  # [seq_length, batch_size, 1]
        rewards: torch.Tensor,  # [batch_size, seq_length-1]
        mask: torch.Tensor,  # [batch_size, seq_length-1]
    ) -> Dict[str, torch.Tensor]:
        input_ids = input_ids[:, 1:].contiguous()  # [batch_size, seq_length-1]
        sharded_logits = sharded_logits.transpose(0, 1)  # (b,s,v)
        sharded_logits = sharded_logits[:, :-1].contiguous()  # [batch_size, seq_length-1, vocab_size
        old_logits = old_logits.transpose(0, 1)  # (b,s,v)
        old_logits = old_logits[:, :-1].contiguous()  # [batch_size, seq_length-1, vocab_size]

        logprobs = -sharded_cross_entropy(
            sharded_logits, input_ids, group=self.tp_pg, dtype=torch.float
        )  # [batch_size, seq_length-1]
        old_logprobs = -sharded_cross_entropy(
            old_logits, input_ids, group=self.tp_pg, dtype=torch.float
        )  # [batch_size, seq_length-1]

        values = values.squeeze(-1).transpose(0, 1)[:, :-1]  # [batch_size, seq_length-1]
        vpreds = vpreds.squeeze(-1).transpose(0, 1)[:, :-1]  # [batch_size, seq_length-1]

        lastgaelam = 0
        advantages_reversed = []
        gen_len = rewards.shape[-1]

        values = values * mask
        masked_rewards = rewards * mask

        for t in reversed(range(gen_len)):
            # TODO @nouamane: check batched computation
            nextvalues = values[:, t + 1] if t < gen_len - 1 else 0.0
            delta = masked_rewards[:, t] + self.gamma * nextvalues - values[:, t]
            lastgaelam = delta + self.gamma * self.lam * lastgaelam
            advantages_reversed.append(lastgaelam)
        advantages = torch.stack(advantages_reversed[::-1]).transpose(0, 1)

        returns = advantages + values  # [batch_size, seq_length-1]
        with torch.no_grad():
            advantages = masked_whiten(advantages, mask)

        vpredclipped = torch.clamp(vpreds, values - self.cliprange_value, values + self.cliprange_value)

        vf_losses1 = (vpreds - returns) ** 2
        vf_losses2 = (vpredclipped - returns) ** 2
        vf_loss = 0.5 * masked_mean(torch.max(vf_losses1, vf_losses2), mask)
        vf_clipfrac = masked_mean(torch.gt(vf_losses2, vf_losses1).double(), mask)

        ratio = torch.exp(logprobs - old_logprobs)
        pg_losses = -advantages * ratio
        pg_losses2 = -advantages * torch.clamp(ratio, 1.0 - self.cliprange, 1.0 + self.cliprange)

        pg_loss = masked_mean(torch.max(pg_losses, pg_losses2), mask)
        pg_clipfrac = masked_mean(torch.gt(pg_losses2, pg_losses).double(), mask)

        loss = pg_loss + self.vf_coef * vf_loss

        # TODO @nouamane: fix entropy with TP
        entropy = masked_mean(entropy_from_logits(sharded_logits), mask)
        approxkl = 0.5 * masked_mean((logprobs - old_logprobs) ** 2, mask)
        policykl = masked_mean(old_logprobs - logprobs, mask)
        return_mean, return_var = masked_mean_and_var(returns, mask)
        value_mean, value_var = masked_mean_and_var(values, mask)
        reward_mean, reward_var = masked_mean_and_var(rewards, mask)

        stats = {
            "loss": {"policy": pg_loss.detach(), "value": vf_loss.detach()},
            "policy": {
                "entropy": entropy.detach(),
                "approxkl": approxkl.detach(),
                "policykl": policykl.detach(),
                "clipfrac": pg_clipfrac.detach(),
                "advantages": advantages.detach(),
                "advantages_mean": masked_mean(advantages, mask).detach(),
                "ratio": ratio.detach(),
            },
            "returns": {"mean": return_mean.detach(), "var": return_var.detach()},
            "val": {
                "vpred": masked_mean(vpreds, mask).detach(),
                "error": masked_mean((vpreds - returns) ** 2, mask).detach(),
                "clipfrac": vf_clipfrac.detach(),
                "mean": value_mean.detach(),
                "var": value_var.detach(),
            },
            "reward": {
                "reward_mean": reward_mean.detach(),
                "reward_var": reward_var.detach(),
                "reward_dist": rewards.detach(),
            },
        }

        return {"loss": loss, **flatten_dict(stats)}


class LlamaModelWithValueHead(nn.Module):
    def __init__(
        self,
        config: LlamaConfig,
        dpg: DistributedProcessGroups,
        parallel_config: Optional[ParallelismArgs],
    ):
        super().__init__()
        self.tp_mode = parallel_config.tp_mode if parallel_config is not None else TensorParallelLinearMode.ALL_REDUCE

        self.model = LlamaModel(config=config, dpg=dpg, parallel_config=parallel_config)
        self.p2p = self.model.p2p
        self.v_head = PipelineBlock(
            p2p=self.p2p,
            module_builder=nn.Linear,
            module_kwargs={
                "in_features": config.hidden_size,
                "out_features": 1,
                "bias": False,
                # "dtype": torch.float32, # TODO @nouamane: this doesn't work
            },
            module_input_keys={"input"},
            module_output_keys={"value"},
        )
        # TODO @nouamane: init weights
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
        sharded_logits, hidden_states = self.model.forward_with_hidden_states(
            input_ids=input_ids,
            input_mask=input_mask,
        )
        value = self.v_head(input=hidden_states)["value"]
        value = self.cast_to_fp32(x=value)["output"]
        return sharded_logits, value, input_ids


class PPOForTraining(nn.Module):
    def __init__(
        self,
        config: LlamaConfig,
        dpg: DistributedProcessGroups,
        parallel_config: Optional[ParallelismArgs],
        ppo_config: PPOArgs,
    ):
        super().__init__()
        self.active_model_with_value = LlamaModelWithValueHead(
            config=config,
            dpg=dpg,
            parallel_config=parallel_config,
        )

        self.loss = PipelineBlock(
            p2p=self.active_model_with_value.p2p,
            module_builder=Loss,
            module_kwargs={"tp_pg": dpg.tp_pg, "ppo_config": ppo_config},
            module_input_keys={"input_ids", "values", "sharded_logits", "old_logits", "vpreds", "rewards", "mask"},
            module_output_keys={
                "policy/ratio",
                "policy/policykl",
                "val/clipfrac",
                "returns/mean",
                "loss/value",
                "val/vpred",
                "policy/clipfrac",
                "val/var",
                "reward/reward_mean",
                "reward/reward_dist",
                "policy/entropy",
                "loss",
                "loss/policy",
                "policy/advantages_mean",
                "policy/approxkl",
                "reward/reward_var",
                "val/mean",
                "val/error",
                "policy/advantages",
                "returns/var",
            },
        )

    def forward(
        self,
        input_ids: Union[torch.Tensor, TensorPointer],
        input_mask: Union[torch.Tensor, TensorPointer],
        old_logits: Union[torch.Tensor, TensorPointer],
        old_values: Union[torch.Tensor, TensorPointer],
        rewards: Union[torch.Tensor, TensorPointer],
        mask: Union[torch.Tensor, TensorPointer],
    ) -> Dict[str, Union[torch.Tensor, TensorPointer]]:
        # (seq_len, bsz, vocab_size), (seq_len, bsz, 1)
        sharded_logits, vpreds, input_ids = self.active_model_with_value(
            input_ids=input_ids,
            input_mask=input_mask,
        )
        # We return input_ids as well, to avoid having to communicate them from first rank

        return self.loss(
            input_ids=input_ids,
            sharded_logits=sharded_logits,
            values=old_values,
            old_logits=old_logits,
            vpreds=vpreds,
            rewards=rewards,
            mask=mask,
        )


def entropy_from_logits(logits):
    """Calculate entropy from logits."""
    pd = torch.nn.functional.softmax(logits, dim=-1)
    # TODO @nouamane: use cross_entropy
    entropy = torch.logsumexp(logits, axis=-1) - torch.sum(pd * logits, axis=-1)
    return entropy


def compute_rewards(
    scores: torch.FloatTensor,
    logprobs: torch.FloatTensor,
    ref_logprobs: torch.FloatTensor,
    masks: torch.BoolTensor,
    kl_ctl: float,
):
    """
    Compute per token rewards from scores and KL-penalty.

    Args:
        scores (`torch.FloatTensor`):
            Scores from the reward model, shape (`batch_size`)
        logprobs (`torch.FloatTensor`):
            Log probabilities of the model, shape (`batch_size`, `response_length`)
        ref_logprobs (`torch.FloatTensor`):
            Log probabilities of the reference model, shape (`batch_size`, `response_length`)
    """
    rewards, non_score_rewards = [], []
    # TODO @nouamane: refactor this
    for score, logprob, ref_logprob, mask in zip(scores, logprobs, ref_logprobs, masks):
        # compute KL penalty (from difference in logprobs)
        kl = logprob - ref_logprob
        non_score_reward = -kl_ctl * kl
        non_score_rewards.append(non_score_reward)
        reward = non_score_reward.clone()
        last_non_masked_index = mask.nonzero()[-1]

        # reward is preference model score + KL penalty
        reward[last_non_masked_index] += score
        rewards.append(reward)
    return torch.stack(rewards), torch.stack(non_score_rewards)


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


class AdaptiveKLController:
    """
    Adaptive KL controller described in the paper:
    https://arxiv.org/pdf/1909.08593.pdf
    """

    def __init__(self, value, target, horizon):
        self.value = value
        self.target = target
        self.horizon = horizon

    def update(self, current, n_steps):
        # TODO @nouamane: should we use torch tensors here?
        target = self.target
        proportional_error = np.clip(current / target - 1, -0.2, 0.2)
        mult = 1 + proportional_error * n_steps / self.horizon
        self.value *= mult

    def save(self, path):
        with open(path, "w") as f:
            json.dump(self.__dict__, f)

    @classmethod
    def load(cls, path):
        with open(path, "r") as f:
            state = json.load(f)
        assert set(state.keys()) == {"value", "target", "horizon"}, "Invalid AdaptiveKLController state"
        return cls(**state)
