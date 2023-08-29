import dataclasses
import os
from contextlib import nullcontext
from dataclasses import dataclass
from typing import Dict, Generator, Iterator, List, Optional, Union

import datasets
import numpy as np
import torch
from config import Config, PretrainNemoArgs
from dataset import GPTDataset, build_train_valid_test_datasets
from datasets import Dataset, DatasetDict, Features, Sequence, Value, concatenate_datasets, load_dataset
from generation import GenerationConfig, GenerationInput, TokenizerConfig, broadcast_tensors, chunks, greedy_search
from modeling_llama import LlamaModel
from modeling_ppo import AdaptiveKLController, PPOForTraining, compute_rewards, masked_mean
from nemo_dataset.data_samplers import MegatronPretrainingRandomSampler, MegatronPretrainingSampler
from torch.nn.parallel import DistributedDataParallel
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import BatchSampler, DataLoader
from torch.utils.data.distributed import DistributedSampler
from transformers import (
    PreTrainedTokenizerBase,
    pipeline,
)
from transformers.trainer_pt_utils import DistributedSamplerWithLoop
from transformers.utils import PaddingStrategy

from brrr.core import distributed as dist
from brrr.core import logging
from brrr.core.distributed import get_global_rank
from brrr.core.logging import log_rank
from brrr.core.parallelism.pipeline_parallelism.tensor_pointer import TensorPointer
from brrr.core.parallelism.tensor_parallelism.functional import sharded_cross_entropy
from brrr.core.process_groups_initializer import DistributedProcessGroups
from brrr.core.random import set_random_seed
from brrr.core.utils import (
    assert_fail_except_rank_with,
    assert_tensor_synced_across_pg,
    main_rank_first,
)
from brrr.logger import LogItem

try:
    from brrr.logger import SummaryWriter

    tb_logger_available = True
except ImportError:
    tb_logger_available = False

logger = logging.get_logger(__name__)


def to_cuda(
    dataloader: Iterator[Dict[str, Union[torch.Tensor, TensorPointer]]], dpg: DistributedProcessGroups, config: Config
) -> Iterator[Dict[str, Union[torch.Tensor, TensorPointer]]]:
    for batch in dataloader:
        micro_batch = {
            k: v if isinstance(v, TensorPointer) else v.to("cuda", memory_format=torch.contiguous_format)
            for k, v in batch.items()
        }

        if not config.general.ignore_sanity_checks:
            # SANITY CHECK: Check input are not the same across DP
            for key, value in sorted(micro_batch.items(), key=lambda x: x[0]):
                if isinstance(value, TensorPointer):
                    continue

                if "mask" in key:
                    # It's fine if mask is the same across DP
                    continue

                with assert_fail_except_rank_with(AssertionError, rank_exception=0, pg=dpg.dp_pg):
                    assert_tensor_synced_across_pg(tensor=value, pg=dpg.dp_pg, msg=lambda err: f"{key} {err}")

            # SANITY CHECK: Check input are synchronized throughout TP
            for key, value in sorted(micro_batch.items(), key=lambda x: x[0]):
                if isinstance(value, TensorPointer):
                    continue
                assert_tensor_synced_across_pg(
                    tensor=value,
                    pg=dpg.tp_pg,
                    msg=lambda err: f"{key} are not synchronized throughout TP {err}",
                )

            # SANITY CHECK: Check that input are synchronized throughout PP
            # TODO @thomasw21: That's really hard to test as input gets sharded across the PP, let's assume it works for now.

        yield micro_batch


def dummy_infinite_data_generator(
    micro_batch_size: int,
    sequence_length: int,
    input_pp_rank: int,
    output_pp_rank: int,
    vocab_size: int,
    seed: int,
    dpg: DistributedProcessGroups,
):
    def dummy_infinite_data_generator() -> Generator[Dict[str, Union[torch.Tensor, TensorPointer]], None, None]:
        # Random generator
        generator = torch.Generator(device="cuda")
        # Make sure that TP are synced always
        generator.manual_seed(seed * (1 + dist.get_rank(dpg.dp_pg)) * (1 + dist.get_rank(dpg.pp_pg)))

        while True:
            yield {
                "input_ids": torch.randint(
                    0,
                    vocab_size,
                    (micro_batch_size, sequence_length),
                    dtype=torch.long,
                    device="cuda",
                    generator=generator,
                )
                if dist.get_rank(dpg.pp_pg) == input_pp_rank
                else TensorPointer(group_rank=input_pp_rank),
                "input_mask": torch.ones(
                    micro_batch_size,
                    sequence_length,
                    dtype=torch.bool,
                    device="cuda",
                )
                if dist.get_rank(dpg.pp_pg) == input_pp_rank
                else TensorPointer(group_rank=input_pp_rank),
                "label_ids": torch.randint(
                    0,
                    vocab_size,
                    (micro_batch_size, sequence_length),
                    dtype=torch.long,
                    device="cuda",
                    generator=generator,
                )
                if dist.get_rank(dpg.pp_pg) == output_pp_rank
                else TensorPointer(group_rank=output_pp_rank),
                "label_mask": torch.ones(
                    micro_batch_size,
                    sequence_length,
                    dtype=torch.bool,
                    device="cuda",
                )
                if dist.get_rank(dpg.pp_pg) == output_pp_rank
                else TensorPointer(group_rank=output_pp_rank),
            }

    return dummy_infinite_data_generator


# Adapted from https://github.com/huggingface/accelerate/blob/a73898027a211c3f6dc4460351b0ec246aa824aa/src/accelerate/data_loader.py#L781C1-L824C28
class SkipBatchSampler(BatchSampler):
    """
    A `torch.utils.data.BatchSampler` that skips the first `n` batches of another `torch.utils.data.BatchSampler`.
    Note that in case of DDP, we skip batches on each rank, so a total of `skip_batches * dpg.dp_pg.size()` batches
    """

    def __init__(self, batch_sampler: BatchSampler, skip_batches: int, dp_size: int):
        self.batch_sampler = batch_sampler
        # In case of DDP, we skip batches on each rank, so a total of `skip_batches * dpg.dp_pg.size()` batches
        self.skip_batches = skip_batches // dp_size

    def __iter__(self):
        for index, samples in enumerate(self.batch_sampler):
            if index >= self.skip_batches:
                yield samples

    @property
    def total_length(self):
        return len(self.batch_sampler)

    def __len__(self):
        return len(self.batch_sampler) - self.skip_batches


def set_tensor_pointers(
    input_dict: Dict[str, Union[torch.Tensor, TensorPointer]], group: dist.ProcessGroup, group_rank: int
) -> Dict[str, Union[torch.Tensor, TensorPointer]]:
    """Make sure only the group_rank rank has the data, others have TensorPointers."""
    return {
        k: v if dist.get_rank(group) == group_rank else TensorPointer(group_rank=group_rank)
        for k, v in input_dict.items()
    }


### PPO TRAINING ###
def get_queries_generator(
    hf_dataset_name: str,
    hf_dataset_config_name: Optional[str],
    hf_dataset_split: str,
    text_column_name: str,
    start_sample_idx: int,
    dp_pg: dist.ProcessGroup,
) -> Iterator[str]:
    """Returns an iterator over the queries from a given dataset."""
    # TODO @nouamane: fix for DP
    iterable_ds = load_dataset(
        hf_dataset_name,
        hf_dataset_config_name,
        split=hf_dataset_split + f"[{start_sample_idx}:]",
        # streaming=True,
    )

    # Keep only the text column
    iterable_ds = iterable_ds.remove_columns(set(iterable_ds.column_names) - {text_column_name})

    # Filter out the examples that are not on the current DP rank
    iterable_ds = iterable_ds.filter(
        lambda example, idx: idx % dp_pg.size() == dist.get_rank(dp_pg), with_indices=True
    )

    def queries_generator():
        for sample in iterable_ds:
            yield sample[text_column_name]

    return queries_generator()


def ppo_data_generator(
    dpg: DistributedProcessGroups,
    model: PPOForTraining,
    ref_model: LlamaModel,
    tokenizer: PreTrainedTokenizerBase,
    queries_generator: Iterator[str],
    sequence_length: int,
    micro_batch_size: int,
    n_micro_batches_per_mini_batch: int,
    n_mini_batches_per_batch: int,
    ppo_epochs: int,
    queries_length: int,
    kl_controller: AdaptiveKLController,
    global_mini_batch_size: int,
    tb_writer: Optional[Union[nullcontext[None], SummaryWriter]],
    generation_batch_size: int,
    start_iteration_step: int,
):
    """Preprocesses a batch of queries and returns the corresponding responses."""

    if isinstance(model, DistributedDataParallel):
        # HACK @nouamane: we could have a brrr.unwrap_model() method
        model = model.module

    model_input_pp_rank = model.active_model_with_value.model.token_position_embeddings.rank
    model_output_pp_rank = model.active_model_with_value.v_head.rank
    ref_model_input_pp_rank = ref_model.token_position_embeddings.rank
    ref_model_output_pp_rank = ref_model.cast_to_fp32.rank

    batch_size = n_mini_batches_per_batch * n_micro_batches_per_mini_batch * micro_batch_size

    def _data_generator() -> Generator[Dict[str, Union[torch.Tensor, TensorPointer]], None, None]:
        iteration_step = start_iteration_step
        for queries_gen in chunks(queries_generator, chunk_size=batch_size):
            assert (
                len(queries_gen) == batch_size
            ), f"Not enough samples in the dataset for a new batch. Please set `train_steps` to the previous iteration step (={iteration_step}) to stop training before the end of the dataset."

            ## ROLLOUT
            # Get responses from active model
            model.active_model_with_value.eval()

            outputs_iter = greedy_search(
                input_iter=(GenerationInput(text=text) for text in queries_gen),
                tokenizer=tokenizer,
                model=model.active_model_with_value.model,
                p2p=model.active_model_with_value.model.p2p,
                dpg=dpg,
                generation_config=GenerationConfig(
                    max_new_tokens=sequence_length - queries_length,
                    max_micro_batch_size=generation_batch_size,
                ),
                tokenizer_config=TokenizerConfig(max_input_length=queries_length),
            )
            queries, input_ids = [], []
            for output in outputs_iter:
                queries.append(output.input_ids)
                input_ids.append(output.generation_ids)  # query + response

            queries = broadcast_tensors(queries, group_src=model_input_pp_rank, group=dpg.pp_pg)
            input_ids = broadcast_tensors(input_ids, group_src=model_input_pp_rank, group=dpg.pp_pg)

            texts = tokenizer.batch_decode(input_ids, clean_up_tokenization_spaces=False)
            responses = [ids[len(query) :] for ids, query in zip(input_ids, queries)]
            responses = tokenizer.batch_decode(responses, clean_up_tokenization_spaces=False)

            model.active_model_with_value.v_head.train()

            ## EVALUATION
            # compute scores
            # TODO: fix this once transformers releases fix: https://github.com/huggingface/transformers/pull/24396
            sentiment_pipe = pipeline(
                "sentiment-analysis",
                model="lvwerra/distilbert-imdb",
                # top_k=2,
                truncation=True,
                device="cuda:" + os.environ["LOCAL_RANK"],
            )
            pipe_outputs = sentiment_pipe(
                texts,
                return_all_scores=True,
                function_to_apply="none",
                batch_size=generation_batch_size,
            )
            scores = torch.tensor([output[1]["score"] for output in pipe_outputs], device="cuda")

            ### PPO OPTIMIZATION
            # no grad forward pass
            input_data = tokenizer.pad(
                [{"input_ids": ids, "attention_mask": torch.ones_like(ids)} for ids in input_ids],
                return_tensors="pt",
                pad_to_multiple_of=None,
            )
            # TODO @nouamane: pad across DP
            input_data = {
                "input_mask": input_data["attention_mask"].to("cuda", torch.bool),
                "input_ids": input_data["input_ids"].to("cuda"),
            }
            attention_mask = input_data["input_mask"]
            input_ids = input_data["input_ids"]

            with torch.no_grad():
                # TODO @nouamane: should we use Modules for this?
                # logits: (seq_len, bsz, vocab_size) / values: (seq_len, bsz, 1)
                if model_input_pp_rank <= dist.get_rank(dpg.pp_pg) <= model_output_pp_rank:
                    # Set TensorPointers to avoid sending data to other ranks
                    input_data = set_tensor_pointers(input_data, dpg.pp_pg, model_input_pp_rank)
                    logits, values, _ = model.active_model_with_value(**input_data)

                p2p = model.active_model_with_value.p2p  # uses dpg.pp_pg
                if model_output_pp_rank != model.loss.rank:
                    if dist.get_rank(dpg.pp_pg) == model_output_pp_rank:
                        p2p.send_tensors(tensors=[values], to_rank=model.loss.rank)
                    if dist.get_rank(dpg.pp_pg) == model.loss.rank:
                        values = p2p.recv_tensors(num_tensors=1, from_rank=model_output_pp_rank)[0]

                if model_output_pp_rank != model.loss.rank:
                    if dist.get_rank(dpg.pp_pg) == model_output_pp_rank:
                        p2p.send_tensors(tensors=[logits], to_rank=model.loss.rank)
                    if dist.get_rank(dpg.pp_pg) == model.loss.rank:
                        logits = p2p.recv_tensors(num_tensors=1, from_rank=model_output_pp_rank)[0]

                # Mask out everything but the response
                # TODO @nouamane: have a fancier attention mask (0: mask, 1: prompt, 2: response)
                mask = torch.zeros_like(attention_mask)
                mask[:, :-1] = attention_mask[:, 1:]
                for j in range(len(input_ids)):
                    start = len(queries[j]) - 1
                    if not attention_mask[j, 0].is_nonzero():  # offset left padding
                        start += attention_mask[j, :].nonzero()[0]
                    end = start + len(responses[j])
                    mask[j, :start] = 0
                    mask[j, end:] = 0

                mask = mask[:, :-1]  # should have same seq_len as logprobs (bsz, seq_len-1)
                mask = mask.contiguous()  # TODO @nouamane: solves `view_as_contiguous` assert

                if ref_model_input_pp_rank <= dist.get_rank(dpg.pp_pg) <= ref_model_output_pp_rank:
                    # Set TensorPointers to avoid sending data to other ranks
                    input_data = set_tensor_pointers(input_data, dpg.pp_pg, ref_model_input_pp_rank)
                    ref_logits = ref_model(**input_data)
                else:
                    ref_logits = TensorPointer(group_rank=ref_model_output_pp_rank)

                if dist.get_rank(dpg.pp_pg) == model_output_pp_rank:
                    logprobs = -sharded_cross_entropy(
                        logits.transpose(0, 1)[:, :-1, :].contiguous(),
                        input_ids[:, 1:].contiguous(),
                        group=dpg.tp_pg,
                        dtype=torch.float,
                    )  # (bsz, seq_len-1)
                    p2p.send_tensors(tensors=[logprobs], to_rank=ref_model_output_pp_rank)

                if dist.get_rank(dpg.pp_pg) == ref_model_output_pp_rank:
                    ref_logprobs = -sharded_cross_entropy(
                        ref_logits.transpose(0, 1)[:, :-1, :].contiguous(),
                        input_ids[:, 1:].contiguous(),
                        group=dpg.tp_pg,
                        dtype=torch.float,
                    )
                    logprobs = p2p.recv_tensors(num_tensors=1, from_rank=model_output_pp_rank)[0]

                    # compute rewards
                    rewards, non_score_reward = compute_rewards(
                        scores, logprobs, ref_logprobs, mask, kl_ctl=kl_controller.value
                    )

                    kl_sum = ((logprobs - ref_logprobs) * mask).sum(axis=-1)
                    mean_kl = kl_sum.mean()
                    p2p.send_tensors(tensors=[rewards, non_score_reward, kl_sum], to_rank=model.loss.rank)
                else:
                    mean_kl = torch.empty(1, device="cuda")

                if dist.get_rank(dpg.pp_pg) == model.loss.rank:
                    rewards, non_score_reward, kl_sum = p2p.recv_tensors(
                        num_tensors=3, from_rank=ref_model_output_pp_rank
                    )

            # Update KL Control
            dist.broadcast(
                mean_kl, src=get_global_rank(group_rank=ref_model_output_pp_rank, group=dpg.pp_pg), group=dpg.pp_pg
            )
            kl_controller.update(
                current=mean_kl.item(), n_steps=global_mini_batch_size
            )  # TODO @nouamane: multiply by n_mini_batches_per_batch?

            if isinstance(tb_writer, SummaryWriter):
                mean_scores = scores.mean()
                min_scores_idx = scores.argmin()
                max_scores_idx = scores.argmax()
                min_scores = scores[min_scores_idx]
                max_scores = scores[max_scores_idx]

                log_rank(
                    f"\nmean_scores: {mean_scores.item():1.6E} | min_scores: {min_scores.item():1.6E} | max_scores: {max_scores.item():1.6E}\nmin_scores_text: {texts[min_scores_idx]}\nmax_scores_text: {texts[max_scores_idx]}",
                    logger=logger,
                    level=logging.INFO,
                )

                mean_kl = kl_sum.mean()
                min_kl_idx = kl_sum.argmin()
                min_kl = kl_sum[min_kl_idx]
                max_kl = kl_sum.max()
                max_kl_idx = kl_sum.argmax()
                mean_kl_item = mean_kl.item()
                log_rank(
                    f"\nmean_kl: {mean_kl_item:1.6E} | min_kl: {min_kl.item():1.6E} | max_kl: {max_kl.item():1.6E}\nmin_kl_text: {texts[min_kl_idx]}\nmax_kl_text: {texts[max_kl_idx]}",
                    logger=logger,
                    level=logging.INFO,
                )

                rewards_sum = (rewards * mask).sum(-1)
                rewards_sum_min_idx = rewards_sum.argmin()
                rewards_sum_max_idx = rewards_sum.argmax()
                rewards_max = rewards_sum[rewards_sum_max_idx]
                rewards_min = rewards_sum[rewards_sum_min_idx]
                log_rank(
                    f"\nmean_rewards: {rewards.mean().item():1.6E} | min_rewards: {rewards_min.item():1.6E} | max_rewards: {rewards_max.item():1.6E}\nmin_rewards_text: {texts[rewards_sum_min_idx]}\nmax_rewards_text: {texts[rewards_sum_max_idx]}",
                    logger=logger,
                    level=logging.INFO,
                )

                log_entries = [
                    LogItem("objective/kl", mean_kl_item, "1.6E"),
                    LogItem("objective/kl_min", min_kl.item(), "1.6E"),
                    LogItem("objective/kl_max", max_kl.item(), "1.6E"),
                    LogItem("env/scores_mean", scores.mean().item(), "1.6E"),
                    LogItem("env/scores_std", scores.std().item(), "1.6E"),
                    LogItem("env/scores_min", min_scores.item(), "1.6E"),
                    LogItem("env/scores_max", max_scores.item(), "1.6E"),
                    LogItem("ppo/mean_rewards", masked_mean(rewards, mask).item(), "1.6E"),
                    LogItem("ppo/rewards_min", rewards_min.item(), "1.6E"),
                    LogItem("ppo/rewards_max", rewards_max.item(), "1.6E"),
                    LogItem("ppo/mean_non_score_reward", masked_mean(non_score_reward, mask).item(), "1.6E"),
                ]
                tb_writer.add_scalars_from_list(log_entries, iteration_step)

                tb_writer.add_text(
                    "min_scores_text",
                    texts[min_scores_idx]
                    + f"\n(score: {scores[min_scores_idx].item():.3f} | kl: {kl_sum[min_scores_idx].item():.3f} | rewards: {rewards_sum[min_scores_idx].item():.3f})",
                    iteration_step,
                )
                tb_writer.add_text(
                    "max_scores_text",
                    texts[max_scores_idx]
                    + f"\n(score: {scores[max_scores_idx].item():.3f} | kl: {kl_sum[max_scores_idx].item():.3f} | rewards: {rewards_sum[max_scores_idx].item():.3f})",
                    iteration_step,
                )
                tb_writer.add_text(
                    "min_kl_text",
                    texts[min_kl_idx]
                    + f"\n(score: {scores[min_kl_idx].item():.3f} | kl: {kl_sum[min_kl_idx].item():.3f} | rewards: {rewards_sum[min_kl_idx].item():.3f})",
                    iteration_step,
                )
                tb_writer.add_text(
                    "max_kl_text",
                    texts[max_kl_idx]
                    + f"\n(score: {scores[max_kl_idx].item():.3f} | kl: {kl_sum[max_kl_idx].item():.3f} | rewards: {rewards_sum[max_kl_idx].item():.3f})",
                    iteration_step,
                )
                tb_writer.add_text(
                    "min_rewards_text",
                    texts[rewards_sum_min_idx]
                    + f"\n(score: {scores[rewards_sum_min_idx].item():.3f} | kl: {kl_sum[rewards_sum_min_idx].item():.3f} | rewards: {rewards_sum[rewards_sum_min_idx].item():.3f})",
                    iteration_step,
                )
                tb_writer.add_text(
                    "max_rewards_text",
                    texts[rewards_sum_max_idx]
                    + f"\n(score: {scores[rewards_sum_max_idx].item():.3f} | kl: {kl_sum[rewards_sum_max_idx].item():.3f} | rewards: {rewards_sum[rewards_sum_max_idx].item():.3f})",
                    iteration_step,
                )
                for i in range(len(texts)):
                    tb_writer.add_text(
                        "texts",
                        texts[i]
                        + f"\n(score: {scores[i].item():.3f} | kl: {kl_sum[i].item():.3f} | rewards: {rewards_sum[i].item():.3f})",
                        iteration_step,
                    )
                    tb_writer.add_text("responses", responses[i], iteration_step)

            input_ids = input_data["input_ids"]
            input_mask = input_data["input_mask"]  # False = hidden

            # we recycle this batch of inputs `ppo_epochs` times, unless early_stopping is triggered, then we move on to the next batch
            indices = torch.arange(0, batch_size, micro_batch_size, device="cuda", dtype=torch.long)

            # Repeat the tensor ppo_epochs times
            indices = indices.repeat(ppo_epochs, 1)

            # Shuffle each row of the tensor independently
            for i in range(indices.size()[0]):
                indices[i] = indices[i][torch.randperm(indices.size()[1])]

            # synchronize ppo_epoch_indices across all ranks to keep the same order of micro_batches
            dist.broadcast(
                indices,
                src=get_global_rank(group_rank=model_input_pp_rank, group=dpg.pp_pg),
                group=dpg.pp_pg,
            )

            # TODO @nouamane: refactor code to have seq_len instead of seq_len-1
            for ppo_epoch in range(ppo_epochs):
                ppo_epoch_indices = indices[ppo_epoch]
                for i, mbs_start_idx in enumerate(ppo_epoch_indices):
                    # We run train_batch_iter every mini_batch
                    if i % n_micro_batches_per_mini_batch == 0:
                        iteration_step += 1

                    o = {
                        "input_ids": input_ids[
                            mbs_start_idx : mbs_start_idx + micro_batch_size
                        ]  # (micro_batch_size, sequence_length)
                        if dist.get_rank(dpg.pp_pg) == model_input_pp_rank
                        else TensorPointer(group_rank=model_input_pp_rank),
                        "input_mask": input_mask[
                            mbs_start_idx : mbs_start_idx + micro_batch_size
                        ]  # (micro_batch_size, sequence_length)
                        if dist.get_rank(dpg.pp_pg) == model_input_pp_rank
                        else TensorPointer(group_rank=model_input_pp_rank),
                        "old_logits": logits[
                            :, mbs_start_idx : mbs_start_idx + micro_batch_size
                        ]  # (sequence_length, micro_batch_size, vocab_size)
                        if dist.get_rank(dpg.pp_pg) == model.loss.rank
                        else TensorPointer(group_rank=model.loss.rank),
                        "old_values": values[
                            :, mbs_start_idx : mbs_start_idx + micro_batch_size
                        ]  # (sequence_length, micro_batch_size, 1)
                        if dist.get_rank(dpg.pp_pg) == model.loss.rank
                        else TensorPointer(group_rank=model.loss.rank),
                        "rewards": rewards[
                            mbs_start_idx : mbs_start_idx + micro_batch_size
                        ]  # (micro_batch_size, sequence_length-1)
                        if dist.get_rank(dpg.pp_pg) == model.loss.rank
                        else TensorPointer(group_rank=model.loss.rank),
                        "mask": mask[
                            mbs_start_idx : mbs_start_idx + micro_batch_size
                        ]  # (micro_batch_size, sequence_length-1)
                        if dist.get_rank(dpg.pp_pg) == model.loss.rank
                        else TensorPointer(group_rank=model.loss.rank),
                    }
                    yield o

    return _data_generator


### DPO TRAINING ###
@dataclass
class DPODataCollatorWithPadding:
    r"""
    DPO DataCollator class that pads the inputs to the maximum length of the batch.
    Args:
        tokenizer (`PreTrainedTokenizerBase`):
            The tokenizer used for encoding the data.
        padding (`Union[bool, str, `PaddingStrategy`]`, `optional`, defaults to `True`):
            padding_strategy to pass to the tokenizer.
        max_length (`int`, defaults to `2048`)
            The maximum length of the sequence to be processed.
        max_prompt_length (`int`, defaults to `256`)
            The maximum length of the prompt to be processed.
        label_pad_token_id (`int`, defaults to -100):
            The label used for masking.
        padding_value (`int`, defaults to 0):
            The value used for padding.
        truncation_mode: (`str`, acceptable values are "keep_start", "keep_end"):
            The truncation mode to use when truncating the prompt.
    """
    tokenizer: PreTrainedTokenizerBase
    padding: Union[bool, str, PaddingStrategy]
    max_length: int
    max_prompt_length: int
    truncation_mode: str
    label_pad_token_id: int
    padding_value: int = 0

    def tokenize_batch_element(
        self,
        prompt: str,
        chosen: str,
        rejected: str,
    ) -> Dict[str, Union[str, List[int]]]:
        """Tokenize a single batch element.

        At this stage, we don't convert to PyTorch tensors yet; we just handle the truncation
            in case the prompt + chosen or prompt + rejected responses is/are too long. First
            we truncate the prompt; if we're still too long, we truncate the chosen/rejected.

        We also create the labels for the chosen/rejected responses, which are of length equal to
            the sum of the length of the prompt and the chosen/rejected response, with
            label_pad_token_id for the prompt tokens.
        """
        # Tokenize the prompt, chosen, and rejected responses. Get a dict with keys "input_ids", "attention_mask"
        chosen_tokens: Dict[str, List[int]] = self.tokenizer(chosen, add_special_tokens=False)
        rejected_tokens: Dict[str, List[int]] = self.tokenizer(rejected, add_special_tokens=False)
        prompt_tokens: Dict[str, List[int]] = self.tokenizer(prompt, add_special_tokens=False)

        assert self.tokenizer.eos_token_id not in prompt_tokens["input_ids"], f"Prompt contains EOS token: {prompt}"
        assert (
            self.tokenizer.eos_token_id not in chosen_tokens["input_ids"]
        ), f"Chosen response contains EOS token: {chosen}"
        assert (
            self.tokenizer.eos_token_id not in rejected_tokens["input_ids"]
        ), f"Rejected response contains EOS token: {rejected}"

        chosen_tokens["input_ids"].append(self.tokenizer.eos_token_id)
        chosen_tokens["attention_mask"].append(1)

        rejected_tokens["input_ids"].append(self.tokenizer.eos_token_id)
        rejected_tokens["attention_mask"].append(1)

        longer_response_length = max(len(chosen_tokens["input_ids"]), len(rejected_tokens["input_ids"]))

        # if combined sequence is too long, truncate the prompt
        if len(prompt_tokens["input_ids"]) + longer_response_length > self.max_length:
            if self.truncation_mode == "keep_start":
                prompt_tokens = {k: v[: self.max_prompt_length] for k, v in prompt_tokens.items()}
            elif self.truncation_mode == "keep_end":
                prompt_tokens = {k: v[-self.max_prompt_length :] for k, v in prompt_tokens.items()}
            else:
                raise ValueError(
                    f"Unknown truncation mode: {self.truncation_mode}, expected values are 'keep_start', 'keep_end'."
                )

        # if that's still too long, truncate the response
        if len(prompt_tokens["input_ids"]) + longer_response_length > self.max_length:
            chosen_tokens = {k: v[: self.max_length - self.max_prompt_length] for k, v in chosen_tokens.items()}
            rejected_tokens = {k: v[: self.max_length - self.max_prompt_length] for k, v in rejected_tokens.items()}

        # Create labels
        chosen_sequence_tokens = {k: prompt_tokens[k] + chosen_tokens[k] for k in chosen_tokens}
        rejected_sequence_tokens = {k: prompt_tokens[k] + rejected_tokens[k] for k in rejected_tokens}
        chosen_sequence_tokens["labels"] = chosen_sequence_tokens["input_ids"][:]
        # Pad the prompt part for the labels
        chosen_sequence_tokens["labels"][: len(prompt_tokens["input_ids"])] = [self.label_pad_token_id] * len(
            prompt_tokens["input_ids"]
        )
        rejected_sequence_tokens["labels"] = rejected_sequence_tokens["input_ids"][:]
        # Pad the prompt part for the labels
        rejected_sequence_tokens["labels"][: len(prompt_tokens["input_ids"])] = [self.label_pad_token_id] * len(
            prompt_tokens["input_ids"]
        )

        batch = {
            # Texts
            "prompt": prompt,
            "chosen": prompt + chosen,
            "rejected": prompt + rejected,
            "chosen_response_only": chosen,
            "rejected_response_only": rejected,
            # Tokenized sequences
            "chosen_input_ids": chosen_sequence_tokens["input_ids"],
            "chosen_attention_mask": chosen_sequence_tokens["attention_mask"],
            "chosen_labels": chosen_sequence_tokens["labels"],
            "rejected_input_ids": rejected_sequence_tokens["input_ids"],
            "rejected_attention_mask": rejected_sequence_tokens["attention_mask"],
            "rejected_labels": rejected_sequence_tokens["labels"],
        }

        return batch

    def collate(self, batch: List[Dict[str, Union[str, List[int]]]]) -> Dict[str, Union[List[str], torch.Tensor]]:
        # We pad chosen and rejected sequences on the right to have same length
        padded_batch = {}
        for k in batch[0].keys():
            if k.endswith("_input_ids") or k.endswith("_attention_mask") or k.endswith("_labels"):
                # adapted from https://stackoverflow.com/questions/73256206
                to_pad = [torch.LongTensor(ex[k]) for ex in batch]
                if k.endswith("_input_ids"):
                    padding_value = self.tokenizer.pad_token_id
                elif k.endswith("_labels"):
                    padding_value = self.label_pad_token_id
                elif k.endswith("_attention_mask"):
                    padding_value = self.padding_value
                else:
                    raise ValueError(f"Unexpected key in batch '{k}'")

                padded_batch[k] = pad_sequence(to_pad, batch_first=True, padding_value=padding_value)
            else:
                padded_batch[k] = [ex[k] for ex in batch]

        return padded_batch

    def __call__(self, features: List[Dict[str, str]]) -> Dict[str, Union[List[str], torch.Tensor]]:
        tokenized_batch = []

        for feature in features:
            prompt: str = feature["prompt"]
            chosen: str = feature["chosen"]
            rejected: str = feature["rejected"]

            batch_element = self.tokenize_batch_element(prompt, chosen, rejected)
            tokenized_batch.append(batch_element)

        # return collated batch
        return self.collate(tokenized_batch)


def dpo_data_generator(
    dpg: DistributedProcessGroups,
    model: PPOForTraining,
    ref_model: LlamaModel,
    tokenizer: PreTrainedTokenizerBase,
    hf_dataset_name: str,
    hf_dataset_split: str,
    micro_batch_size: int,
    sequence_length: int,
    max_prompt_length: int,
    truncation_mode: str,
    label_pad_token_id: int,
    padding: Union[bool, str, PaddingStrategy] = True,
    padding_value: int = 0,
):
    """Preprocesses a batch of queries and returns the corresponding responses."""

    def concatenated_inputs(batch: Dict[str, Union[List, torch.LongTensor]]) -> Dict[str, torch.LongTensor]:
        """Concatenate the chosen and rejected inputs along the batch dimension into a single tensor.

        Args:
            batch: A batch of data. Must contain the keys 'chosen_input_ids' and 'rejected_input_ids', which are tensors of shape (batch_size, sequence_length).

        Returns:
            A dictionary containing the concatenated inputs under the key 'concatenated_input_ids'.
        """

        def pad_to_length(
            tensor: torch.Tensor, length: int, pad_value: Union[int, float], dim: int = -1
        ) -> torch.Tensor:
            if tensor.size(dim) >= length:
                return tensor
            else:
                pad_size = list(tensor.shape)
                pad_size[dim] = length - tensor.size(dim)
                return torch.cat(
                    [
                        tensor,
                        pad_value * torch.ones(*pad_size, dtype=tensor.dtype, device=tensor.device),
                    ],
                    dim=dim,
                )

        max_length = max(batch["chosen_input_ids"].shape[1], batch["rejected_input_ids"].shape[1])
        # We pad to multiple of TP size
        max_length += dpg.tp_pg.size() - (max_length % dpg.tp_pg.size())

        concatenated_batch = {
            "concatenated_input_ids": torch.cat(
                (
                    pad_to_length(batch["chosen_input_ids"], max_length, pad_value=padding_value),
                    pad_to_length(batch["rejected_input_ids"], max_length, pad_value=padding_value),
                ),
                dim=0,
            ).to("cuda"),
            "concatenated_attention_mask": torch.cat(
                (
                    pad_to_length(batch["chosen_attention_mask"], max_length, pad_value=0),
                    pad_to_length(batch["rejected_attention_mask"], max_length, pad_value=0),
                ),
                dim=0,
            ).to("cuda"),
            "concatenated_labels": torch.cat(
                (
                    pad_to_length(batch["chosen_labels"], max_length, pad_value=label_pad_token_id),
                    pad_to_length(batch["rejected_labels"], max_length, pad_value=label_pad_token_id),
                ),
                dim=0,
            ).to("cuda"),
        }
        return concatenated_batch

    def get_hh_data(dataset_name: str, split: str):
        dataset = datasets.load_dataset(dataset_name, split=split)

        def extract_anthropic_prompt(prompt_and_response):
            """Extract the anthropic prompt from a prompt and response pair."""
            search_term = "\n\nAssistant:"
            search_term_idx = prompt_and_response.rfind(search_term)
            assert search_term_idx != -1, f"Prompt and response does not contain '{search_term}'"
            return prompt_and_response[: search_term_idx + len(search_term)]

        def split_prompt_and_responses(sample) -> Dict[str, str]:
            prompt = extract_anthropic_prompt(sample["chosen"])
            return {
                "prompt": prompt,
                "chosen": sample["chosen"][len(prompt) :],
                "rejected": sample["rejected"][len(prompt) :],
            }

        return dataset.map(split_prompt_and_responses)

    assert hf_dataset_name in [
        "Anthropic/hh-rlhf"
    ], f"Unknown dataset '{hf_dataset_name}'. We only support 'Anthropic/hh-rlhf' for now."
    dataset = get_hh_data(dataset_name=hf_dataset_name, split=hf_dataset_split)
    data_collator = DPODataCollatorWithPadding(
        tokenizer=tokenizer,
        max_length=sequence_length,
        max_prompt_length=max_prompt_length,
        label_pad_token_id=label_pad_token_id,
        padding_value=padding_value,
        truncation_mode=truncation_mode,
        padding=padding,
    )
    assert (
        micro_batch_size % 2 == 0
    ), f"micro_batch_size={micro_batch_size} must be even because chosen and rejected samples go in pairs"
    dataloader = DataLoader(dataset, batch_size=micro_batch_size // 2, collate_fn=data_collator)

    if isinstance(model, DistributedDataParallel):
        # HACK @nouamane: we could have a brrr.unwrap_model() method
        model = model.module
    model_input_pp_rank = model.model.token_position_embeddings.rank
    model_output_pp_rank = model.model.cast_to_fp32.rank
    ref_model_input_pp_rank = ref_model.token_position_embeddings.rank
    ref_model_output_pp_rank = ref_model.cast_to_fp32.rank
    p2p = model.model.p2p  # uses dpg.pp_pg

    def _data_generator() -> Generator[Dict[str, Union[torch.Tensor, TensorPointer]], None, None]:
        for batch in dataloader:
            concatenated_batch = concatenated_inputs(batch)
            concatenated_batch["concatenated_attention_mask"] = concatenated_batch["concatenated_attention_mask"].to(
                torch.bool
            )

            # Compute reference logprobs
            if ref_model_input_pp_rank <= dist.get_rank(dpg.pp_pg) <= ref_model_output_pp_rank:
                with torch.no_grad():
                    ref_logits = ref_model(
                        concatenated_batch["concatenated_input_ids"],  # (chosen_bsz + rejected_bsz, sequence_length)
                        concatenated_batch["concatenated_attention_mask"],
                    ).to(
                        torch.float32
                    )  # (sequence_length, chosen_bsz + rejected_bsz, vocab_size)
                    ref_logits = ref_logits.transpose(
                        0, 1
                    ).contiguous()  # [chosen_bsz + rejected_bsz, seq_length, vocab_size]
                    ref_logprobs = -sharded_cross_entropy(
                        ref_logits,
                        concatenated_batch["concatenated_labels"].contiguous(),
                        group=dpg.tp_pg,
                        dtype=torch.float,
                    )  # (chosen_bsz + rejected_bsz, sequence_length)
                    labels_mask = (
                        concatenated_batch["concatenated_labels"] != -100
                    )  # [chosen_bsz + rejected_bsz, seq_length]
                    ref_logprobs = (ref_logprobs * labels_mask).sum(-1)  # [chosen_bsz + rejected_bsz]

                    p2p.send_tensors(tensors=[ref_logprobs], to_rank=model.loss.rank)
            elif dist.get_rank(dpg.pp_pg) == model.loss.rank:
                ref_logprobs = p2p.recv_tensors(num_tensors=1, from_rank=ref_model_output_pp_rank)[0]

            # Index which separates chosen from rejected samples
            chosen_rejected_sep_idx = torch.tensor(batch["chosen_input_ids"].shape[0], device="cuda")

            o = {
                "concatenated_input_ids": concatenated_batch[
                    "concatenated_input_ids"
                ]  # [chosen_bsz + rejected_bsz, seq_length]
                if dist.get_rank(dpg.pp_pg) == model_input_pp_rank
                else TensorPointer(group_rank=model_input_pp_rank),
                "concatenated_attention_mask": concatenated_batch[
                    "concatenated_attention_mask"
                ]  # [chosen_bsz + rejected_bsz, seq_length]
                if dist.get_rank(dpg.pp_pg) == model_input_pp_rank
                else TensorPointer(group_rank=model_input_pp_rank),
                "concatenated_labels": concatenated_batch[
                    "concatenated_labels"
                ]  # [chosen_bsz + rejected_bsz, seq_length]
                if dist.get_rank(dpg.pp_pg) == model_output_pp_rank
                else TensorPointer(group_rank=model_output_pp_rank),
                "ref_logprobs": ref_logprobs  # [chosen_bsz + rejected_bsz]
                if dist.get_rank(dpg.pp_pg) == model.loss.rank
                else TensorPointer(group_rank=model.loss.rank),
                "chosen_rejected_sep_idx": chosen_rejected_sep_idx  # [1]
                if dist.get_rank(dpg.pp_pg) == model.loss.rank
                else TensorPointer(group_rank=model.loss.rank),
            }
            yield o

    return _data_generator


### REWARD MODELING ###
@dataclass
class RewardDataCollatorWithPadding:
    r"""
    Reward DataCollator class that pads the inputs to the maximum length of the batch.
    Args:
        tokenizer (`PreTrainedTokenizerBase`):
            The tokenizer used for encoding the data.
        padding (`Union[bool, str, `PaddingStrategy`]`, `optional`, defaults to `True`):
            padding_strategy to pass to the tokenizer.
        max_length (`Optional[int]`, `optional`, defaults to `None`):
            The maximum length of the sequence to be processed.
        pad_to_multiple_of (`Optional[int]`, `optional`, defaults to `None`):
            If set will pad the sequence to a multiple of the provided value.
        return_tensors (`str`, `optional`, defaults to `"pt"`):
            The tensor type to use.
    """
    tokenizer: PreTrainedTokenizerBase
    padding: Union[bool, str] = True
    max_length: Optional[int] = None
    pad_to_multiple_of: Optional[int] = None
    return_tensors: str = "pt"

    def __call__(self, features: List[Dict[str, Union[List[int], str]]]) -> Dict[str, torch.Tensor]:
        chosen_features = []
        rejected_features = []
        for feature in features:
            # check if the keys are named as expected
            if (
                "chosen_input_ids" not in feature
                or "rejected_input_ids" not in feature
                or "chosen_attention_mask" not in feature
                or "rejected_attention_mask" not in feature
            ):
                raise ValueError(
                    "The features should include `chosen_input_ids`, `chosen_attention_mask`, `rejected_input_ids` and `rejected_attention_mask`"
                )

            chosen_features.append(
                {
                    "input_ids": feature["chosen_input_ids"],
                    "attention_mask": feature["chosen_attention_mask"],
                }
            )
            rejected_features.append(
                {
                    "input_ids": feature["rejected_input_ids"],
                    "attention_mask": feature["rejected_attention_mask"],
                }
            )
        chosen_batch = self.tokenizer.pad(
            chosen_features,
            padding=self.padding,
            max_length=self.max_length,
            pad_to_multiple_of=self.pad_to_multiple_of,
            return_tensors=self.return_tensors,
        )
        rejected_batch = self.tokenizer.pad(
            rejected_features,
            padding=self.padding,
            max_length=self.max_length,
            pad_to_multiple_of=self.pad_to_multiple_of,
            return_tensors=self.return_tensors,
        )
        batch = {
            "chosen_input_ids": chosen_batch["input_ids"],
            "chosen_attention_mask": chosen_batch["attention_mask"],
            "rejected_input_ids": rejected_batch["input_ids"],
            "rejected_attention_mask": rejected_batch["attention_mask"],
        }
        return batch


# Adapted from h4/src/h4/data/loading.py
def get_datasets(
    dataset_mixer: Union[dict, str],
    splits: Optional[Union[List[str], str]] = ["train", "test"],
) -> DatasetDict:
    """
    Function to load dataset directly from DataArguments.

    Args:
        dataset_mixer (Union[dict, str]): dict or string. When all probabilities are 1, we concatenate the datasets instead of sampling from them.
        splits (Optional[List[str]], optional): Section of the dataset to load, defaults to "train", "test"
            Can be one of `train_ift`, `test_rl`, or `..._rm` etc. H4 datasets are divided into 6 subsets for training / testing.

    Returns
        DatasetDict: DatasetDict object containing the dataset of the appropriate section with test + train parts.
    """

    if type(splits) is str:
        splits = [splits]

    if type(dataset_mixer) is dict:
        # Structure of the config to read the datasets and their mix
        # datasets_mixer:
        #     - 'dataset1': 0.5
        #     - 'dataset2': 0.3
        #     - 'dataset3': 0.2
        raw_datasets = _get_dataset_mix(dataset_mixer, splits=splits)
    elif type(dataset_mixer) is str:
        # e.g. Dataset = "HuggingFaceH4/testing_alpaca_small"
        # Note this returns things other than just train/test, which may not be intended
        raw_datasets = DatasetDict()
        for split in splits:
            raw_datasets[split] = load_dataset(
                dataset_mixer,
                split=split,
            )
    else:
        raise ValueError(f"dataset_mixer must be a dict or string but is {type(dataset_mixer)}")

    return raw_datasets


# Adapted from h4/src/h4/data/loading.py
def _get_dataset_mix(dataset_dict: dict, splits: List[str] = None, seed=42) -> DatasetDict:
    """
    Helper function to load dataset mix from dict configuration.

    Args:
        dataset_dict (dict): Dictionary containing the dataset names and their training proportions. By default, all test proportions are 1.
        splits (Optional[List[str]], optional): Section of the dataset to load, defaults to "train", "test"
            Can be one of `train_{ift,rm,rl}` and `test_{ift,rm,rl}`. Our datasets are typically divided into 6 subsets for training / testing.
    """
    raw_datasets = DatasetDict()
    raw_train_datasets = []
    raw_test_datasets = []
    fracs = []
    for ds, frac in dataset_dict.items():
        if frac < 0:
            raise ValueError(f"Dataset fraction for dataset {ds} is negative. (= {frac})")

        fracs.append(frac)
        for split in splits:
            if "train" in split:
                raw_train_datasets.append(
                    load_dataset(
                        ds,
                        split=split,
                    )
                )
            elif "test" in split:
                raw_test_datasets.append(
                    load_dataset(
                        ds,
                        split=split,
                    )
                )
            else:
                raise ValueError(f"Split type {split} not recognized as one of test or train.")

    if len(raw_train_datasets) > 0:
        train_subsets = []
        for dataset, frac in zip(raw_train_datasets, fracs):
            train_subset = dataset.select(range(int(frac * len(dataset))))
            train_subsets.append(train_subset)
        raw_datasets["train"] = concatenate_datasets(train_subsets).shuffle(seed=seed)

    # No subsampling for test datasets to enable fair comparison across models
    if len(raw_test_datasets) > 0:
        raw_datasets["test"] = concatenate_datasets(raw_test_datasets).shuffle(seed=seed)

    if len(raw_datasets) == 0:
        raise ValueError(
            f"Dataset {dataset_dict} not recognized with split {split}. Check the dataset has been correctly formatted."
        )

    return raw_datasets


def reward_data_generator(
    dpg: DistributedProcessGroups,
    model: PPOForTraining,
    tokenizer: PreTrainedTokenizerBase,
    micro_batch_size: int,
    sequence_length: int,
    dataset_processing_num_proc_per_process,
    dataset_mixer: Union[str, List, Dict[str, float]],
    dataset_splits: Union[str, List[str]],
    dataset_config_name: Optional[str] = None,
    label_pad_token_id: int = -100,
    padding_value: int = 0,
):
    """Preprocesses a batch of queries and returns the corresponding responses."""

    def concatenated_inputs(batch: Dict[str, Union[List, torch.LongTensor]]) -> Dict[str, torch.LongTensor]:
        """Concatenate the chosen and rejected inputs along the batch dimension into a single tensor.

        Args:
            batch: A batch of data. Must contain the keys 'chosen_input_ids' and 'rejected_input_ids', which are tensors of shape (batch_size, sequence_length).

        Returns:
            A dictionary containing the concatenated inputs under the key 'concatenated_input_ids'.
        """

        def pad_to_length(
            tensor: torch.Tensor, length: int, pad_value: Union[int, float], dim: int = -1
        ) -> torch.Tensor:
            if tensor.size(dim) >= length:
                return tensor
            else:
                pad_size = list(tensor.shape)
                pad_size[dim] = length - tensor.size(dim)
                return torch.cat(
                    [
                        tensor,
                        pad_value * torch.ones(*pad_size, dtype=tensor.dtype, device=tensor.device),
                    ],
                    dim=dim,
                )

        max_length = max(batch["chosen_input_ids"].shape[1], batch["rejected_input_ids"].shape[1])
        # We pad to multiple of TP size
        max_length += dpg.tp_pg.size() - (max_length % dpg.tp_pg.size())

        concatenated_batch = {
            "concatenated_input_ids": torch.cat(
                (
                    pad_to_length(batch["chosen_input_ids"], max_length, pad_value=padding_value),
                    pad_to_length(batch["rejected_input_ids"], max_length, pad_value=padding_value),
                ),
                dim=0,
            ).to("cuda"),
            "concatenated_attention_mask": torch.cat(
                (
                    pad_to_length(batch["chosen_attention_mask"], max_length, pad_value=0),
                    pad_to_length(batch["rejected_attention_mask"], max_length, pad_value=0),
                ),
                dim=0,
            ).to("cuda"),
        }
        return concatenated_batch

    def get_dataset(
        dataset_mixer: Union[str, List, Dict[str, float]],
        dataset_splits: Union[str, List[str]],
        dataset_config_name: Optional[str] = None,
    ):
        # TODO @nouamane: use eval dataset for evaluation
        dataset = get_datasets(dataset_mixer=dataset_mixer, splits=dataset_splits)["train"]

        def preprocess_function(examples):
            new_examples = {
                "chosen_input_ids": [],
                "chosen_attention_mask": [],
                "rejected_input_ids": [],
                "rejected_attention_mask": [],
            }
            for chosen, rejected in zip(examples["chosen"], examples["rejected"]):
                tokenized_j = tokenizer(chosen, truncation=True)
                tokenized_k = tokenizer(rejected, truncation=True)

                new_examples["chosen_input_ids"].append(tokenized_j["input_ids"])
                new_examples["chosen_attention_mask"].append(tokenized_j["attention_mask"])
                new_examples["rejected_input_ids"].append(tokenized_k["input_ids"])
                new_examples["rejected_attention_mask"].append(tokenized_k["attention_mask"])

            return new_examples

        dataset = dataset.map(
            preprocess_function,
            num_proc=dataset_processing_num_proc_per_process,
            batched=True,
            load_from_cache_file=True,
        )
        return dataset.filter(
            lambda x: len(x["chosen_input_ids"]) <= sequence_length
            and len(x["rejected_input_ids"]) <= sequence_length,
        )

    with main_rank_first(dpg.world_pg):
        dataset = get_dataset(
            dataset_mixer=dataset_mixer, dataset_splits=dataset_splits, dataset_config_name=dataset_config_name
        )

    data_collator = RewardDataCollatorWithPadding(
        tokenizer, max_length=sequence_length, pad_to_multiple_of=dpg.tp_pg.size()
    )

    assert (
        micro_batch_size % 2 == 0
    ), f"micro_batch_size={micro_batch_size} must be even because chosen and rejected samples go in pairs"
    dataloader = DataLoader(dataset, batch_size=micro_batch_size // 2, collate_fn=data_collator)

    if isinstance(model, DistributedDataParallel):
        # HACK @nouamane: we could have a brrr.unwrap_model() method
        model = model.module
    model_input_pp_rank = model.model.token_position_embeddings.rank

    def _data_generator() -> Generator[Dict[str, Union[torch.Tensor, TensorPointer]], None, None]:
        for batch in dataloader:
            concatenated_batch = concatenated_inputs(batch)
            concatenated_batch["concatenated_attention_mask"] = concatenated_batch["concatenated_attention_mask"].to(
                torch.bool
            )

            # Index which separates chosen from rejected samples
            chosen_rejected_sep_idx = torch.tensor(batch["chosen_input_ids"].shape[0], device="cuda")

            o = {
                "concatenated_input_ids": concatenated_batch[
                    "concatenated_input_ids"
                ]  # [chosen_bsz + rejected_bsz, seq_length]
                if dist.get_rank(dpg.pp_pg) == model_input_pp_rank
                else TensorPointer(group_rank=model_input_pp_rank),
                "concatenated_attention_mask": concatenated_batch[
                    "concatenated_attention_mask"
                ]  # [chosen_bsz + rejected_bsz, seq_length]
                if dist.get_rank(dpg.pp_pg) == model_input_pp_rank
                else TensorPointer(group_rank=model_input_pp_rank),
                "chosen_rejected_sep_idx": chosen_rejected_sep_idx  # [1]
                if dist.get_rank(dpg.pp_pg) == model.loss.rank
                else TensorPointer(group_rank=model.loss.rank),
            }
            yield o

    return _data_generator


### CAUSAL LANGUAGE MODELING ###
def clm_process(
    raw_dataset: Dataset,
    tokenizer: PreTrainedTokenizerBase,
    text_column_name: str,
    dataset_processing_num_proc_per_process: int,
    dataset_overwrite_cache: bool,
    sequence_length: int,
):
    """Concatenate all texts from raw_dataset and generate chunks of `sequence_length + 1`, where chunks overlap by a single token."""
    # Adapted from https://github.com/huggingface/transformers/blob/47e1676255e5dd86b9541f734cd4f4bdcbb50f4a/examples/pytorch/language-modeling/run_clm.py#L391-L439

    def group_texts(examples: Dict[str, List[np.array]]) -> Dict[str, List[np.array]]:
        # Concatenate all texts.
        concatenated_examples = {k: np.concatenate(v) for k, v in examples.items()}
        total_length = len(concatenated_examples[next(iter(examples.keys()))])
        # WARNING: We drop the small remainder, we could add padding if the model supported it instead of this drop, you can
        # customize this part to your needs.
        if total_length >= sequence_length + 1:
            total_length = ((total_length - 1) // sequence_length) * sequence_length + 1
        # Split by chunks of sequence_length.
        result = {
            k: [
                t[i : i + sequence_length + 1] for i in range(0, total_length - (sequence_length + 1), sequence_length)
            ]
            for k, t in concatenated_examples.items()
        }
        return result

    def _tokenize_and_group_texts(texts: List[str]) -> Dict[str, List[np.array]]:
        tokenized_batch = tokenizer.batch_encode_plus(texts, return_attention_mask=False, return_token_type_ids=False)
        tokenized_batch = {k: [np.array(tokenized_texts) for tokenized_texts in v] for k, v in tokenized_batch.items()}
        return group_texts(tokenized_batch)

    train_dataset = raw_dataset.map(
        _tokenize_and_group_texts,
        input_columns=text_column_name,
        remove_columns=raw_dataset.column_names,
        features=Features({"input_ids": Sequence(feature=Value(dtype="int64"), length=sequence_length + 1)}),
        batched=True,
        num_proc=dataset_processing_num_proc_per_process,
        load_from_cache_file=not dataset_overwrite_cache,
        desc=f"Grouping texts in chunks of {sequence_length+1}",
    )
    return train_dataset


# Adapted from: https://github.com/huggingface/transformers/blob/47e1676255e5dd86b9541f734cd4f4bdcbb50f4a/src/transformers/data/data_collator.py#L607
@dataclasses.dataclass
class DataCollatorForCLM:
    """
    Data collator used for causal language modeling.

    GPT2Tokenizer doesn't have a _pad_token. For tokenizers that do, inputs can be dynamically padded to the maximum length of a batch if they
    are not all of the same length. see: https://github.com/huggingface/transformers/blob/47e1676255e5dd86b9541f734cd4f4bdcbb50f4a/src/transformers/data/data_collator.py#L394-L430
    """

    sequence_length: int
    input_pp_rank: int
    output_pp_rank: int
    dpg: DistributedProcessGroups

    def __call__(self, examples: List[Dict[str, List[np.array]]]) -> Dict[str, Union[torch.Tensor, TensorPointer]]:
        # Process the case when "input_ids" doesn't exist
        current_pp_rank = dist.get_rank(self.dpg.pp_pg)
        if current_pp_rank not in [
            self.input_pp_rank,
            self.output_pp_rank,
        ]:
            assert all(len(example) == 0 for example in examples)
            return {
                "input_ids": TensorPointer(self.input_pp_rank),
                "input_mask": TensorPointer(self.input_pp_rank),
                "label_ids": TensorPointer(self.output_pp_rank),
                "label_mask": TensorPointer(self.output_pp_rank),
            }

        # Make sure we load only what's necessary, ie we only load a `input_ids` column.
        assert all(list(example.keys()) == ["input_ids"] for example in examples)

        # TODO @nouamanetazi: Is it better to have examples as np.array or torch.Tensor?
        input_ids = np.vstack([examples[i]["input_ids"] for i in range(len(examples))])  # (b, s)
        batch_size, expanded_input_length = input_ids.shape

        result: Dict[str, Union[np.array, TensorPointer]] = {}

        result["input_ids"] = TensorPointer(group_rank=self.input_pp_rank)
        result["input_mask"] = TensorPointer(group_rank=self.input_pp_rank)
        result["label_ids"] = TensorPointer(group_rank=self.output_pp_rank)
        result["label_mask"] = TensorPointer(group_rank=self.output_pp_rank)

        assert (
            expanded_input_length == self.sequence_length + 1
        ), f"Samples should be of length {self.sequence_length + 1} (seq_len+1), but got {expanded_input_length}"

        # Process inputs: last token is the label
        if current_pp_rank == self.input_pp_rank:
            result["input_ids"] = input_ids[:, :-1]
            result["input_mask"] = np.ones((batch_size, self.sequence_length), dtype=np.bool_)

        # Process labels: shift them to the left
        if current_pp_rank == self.output_pp_rank:
            result["label_ids"] = input_ids[:, 1:]
            result["label_mask"] = np.ones((batch_size, self.sequence_length), dtype=np.bool_)

        if isinstance(result["input_ids"], torch.Tensor) and result["input_ids"].shape[-1] != self.sequence_length:
            raise ValueError(
                f"`labels` are incorrectly preprocessed. `labels` length is {result['input_ids'].shape[-1]}, but should be"
                f" {self.sequence_length}."
            )
        if isinstance(result["label_ids"], torch.Tensor) and result["label_ids"].shape[-1] != self.sequence_length:
            raise ValueError(
                f"`labels` are incorrectly preprocessed. `labels` length is {result['label_ids'].shape[-1]}, but should be"
                f" {self.sequence_length}."
            )

        # Cast np.array to torch.Tensor
        result = {k: v if isinstance(v, TensorPointer) else torch.from_numpy(v) for k, v in result.items()}
        return result


# Adapted from https://github.com/huggingface/transformers/blob/47e1676255e5dd86b9541f734cd4f4bdcbb50f4a/src/transformers/trainer.py#L763-L835
def _get_train_sampler(
    dp_size: int,
    dp_rank: int,
    train_dataset: Dataset,
    seed: int,
    use_loop_to_round_batch_size: bool,
    consumed_train_samples: int,
    micro_batch_size: Optional[int] = None,
    drop_last: Optional[bool] = True,
) -> Optional[torch.utils.data.Sampler]:
    """returns sampler that restricts data loading to a subset of the dataset proper to the DP rank"""

    # Build the sampler.
    # TODO @nouamanetazi: Support group_by_length: https://github.com/huggingface/transformers/blob/47e1676255e5dd86b9541f734cd4f4bdcbb50f4a/src/transformers/trainer.py#L783-L810

    if use_loop_to_round_batch_size:
        assert micro_batch_size is not None
        # loops at the end back to the beginning of the shuffled samples to make each process have a round multiple of batch_size samples.
        sampler = DistributedSamplerWithLoop(
            train_dataset,
            batch_size=micro_batch_size,
            num_replicas=dp_size,
            rank=dp_rank,
            seed=seed,
            drop_last=drop_last,
        )
    else:
        sampler = DistributedSampler(train_dataset, num_replicas=dp_size, rank=dp_rank, seed=seed, drop_last=drop_last)

    if consumed_train_samples > 0:
        sampler = SkipBatchSampler(sampler, skip_batches=consumed_train_samples, dp_size=dp_size)

    return sampler


# Adapted from https://github.com/huggingface/transformers/blob/47e1676255e5dd86b9541f734cd4f4bdcbb50f4a/src/transformers/trainer.py#L837
def get_train_dataloader(
    train_dataset: Dataset,
    sequence_length: int,
    dpg: DistributedProcessGroups,
    input_pp_rank: int,
    output_pp_rank: int,
    micro_batch_size: int,
    consumed_train_samples: int,
    dataloader_num_workers: int,
    seed_worker: int,
    dataloader_drop_last: bool = True,
    dataloader_pin_memory: bool = True,
    use_loop_to_round_batch_size: bool = False,
) -> DataLoader:
    if not isinstance(train_dataset, datasets.Dataset):
        raise ValueError(f"training requires a datasets.Dataset, but got {type(train_dataset)}")

    # Only some rank require to run the dataloader.
    if dist.get_rank(dpg.pp_pg) not in [
        input_pp_rank,
        output_pp_rank,
    ]:
        # dataset has to have a single column, with `input_ids` as the column name
        assert train_dataset.column_names == ["input_ids"]
        dataset_length = len(train_dataset)
        train_dataset = train_dataset.remove_columns(column_names="input_ids")
        assert (
            len(train_dataset) == 0
        ), f"Dataset has to be empty after removing the `input_ids` column. Current dataset: {train_dataset}"
        # HACK as if we remove the last column of a train_dataset, it becomes empty and it's number of rows becomes empty.
        train_dataset = EmptyInfiniteDataset(length=dataset_length)
        # No need to spawn a lot of workers, we can just use main
        dataloader_num_workers = 0
    else:
        train_dataset = train_dataset.with_format(type="numpy", columns=["input_ids"], output_all_columns=True)

    data_collator = DataCollatorForCLM(
        sequence_length=sequence_length,
        input_pp_rank=input_pp_rank,
        output_pp_rank=output_pp_rank,
        dpg=dpg,
    )

    # TODO @nouamanetazi: Remove unused columns: https://github.com/huggingface/transformers/blob/47e1676255e5dd86b9541f734cd4f4bdcbb50f4a/src/transformers/trainer.py#L852
    # TODO @nouamanetazi: Support torch.utils.data.IterableDataset: https://github.com/huggingface/transformers/blob/47e1676255e5dd86b9541f734cd4f4bdcbb50f4a/src/transformers/trainer.py#L855-L872

    train_sampler = _get_train_sampler(
        dp_size=dpg.dp_pg.size(),
        dp_rank=dist.get_rank(dpg.dp_pg),
        train_dataset=train_dataset,
        seed=seed_worker,
        use_loop_to_round_batch_size=use_loop_to_round_batch_size,
        micro_batch_size=micro_batch_size,
        drop_last=dataloader_drop_last,
        consumed_train_samples=consumed_train_samples,
    )

    return DataLoader(
        train_dataset,
        batch_size=micro_batch_size,
        sampler=train_sampler,
        collate_fn=data_collator,
        drop_last=dataloader_drop_last,  # we also drop_last in `clm_process()`
        num_workers=dataloader_num_workers,
        pin_memory=dataloader_pin_memory,
        worker_init_fn=get_dataloader_worker_init(dp_rank=dist.get_rank(dpg.dp_pg)),
        # TODO @thomasw21: I'm not sure but this doesn't seem to work at all.
        # pin_memory_device="cuda",
    )


def get_nemo_datasets(
    config: PretrainNemoArgs,
    sequence_length: int,
    global_batch_size: int,
    train_steps: int,
    limit_val_batches: int,
    val_check_interval: int,
    test_iters: int,
    seed,
    dpg: DistributedProcessGroups,
):
    log_rank("Building GPT datasets.", logger=logger, level=logging.INFO, rank=0)
    if limit_val_batches > 1.0 and isinstance(limit_val_batches, float):
        raise ValueError("limit_val_batches must be an integer or float less than or equal to 1.0.")
    eval_iters = (train_steps // val_check_interval + 1) * limit_val_batches

    train_valid_test_num_samples = [
        train_steps * global_batch_size,
        eval_iters * global_batch_size,
        test_iters * global_batch_size,
    ]

    if limit_val_batches <= 1.0 and isinstance(limit_val_batches, float):
        train_valid_test_num_samples[
            1
        ] = 1  # This is to make sure we only have one epoch on every validation iteration

    train_ds, validation_ds, test_ds = build_train_valid_test_datasets(
        cfg=config,
        data_prefix=config.data_prefix,
        splits_string=config.splits_string,
        train_valid_test_num_samples=train_valid_test_num_samples,
        seq_length=sequence_length,
        seed=seed,
        dpg=dpg,
        skip_warmup=config.skip_warmup,
    )

    return train_ds, validation_ds, test_ds


def get_nemo_dataloader(
    dataset: GPTDataset,
    sequence_length: int,
    micro_batch_size: int,
    global_batch_size: int,
    cfg: PretrainNemoArgs,
    num_workers: int,
    consumed_samples: int,
    dpg: DistributedProcessGroups,
    input_pp_rank: int,
    output_pp_rank: int,
    dataloader_drop_last: bool = True,
    dataloader_pin_memory: bool = True,
) -> DataLoader:
    # Only some rank require to run the dataloader.
    if dist.get_rank(dpg.pp_pg) not in [
        input_pp_rank,
        output_pp_rank,
    ]:
        dataset = EmptyInfiniteDataset(length=len(dataset))

    log_rank(
        f"Building dataloader with consumed samples: {consumed_samples}", logger=logger, level=logging.INFO, rank=0
    )
    # Megatron sampler
    if cfg.dataloader_type == "single":
        batch_sampler = MegatronPretrainingSampler(
            total_samples=len(dataset),
            consumed_samples=consumed_samples,
            micro_batch_size=micro_batch_size,
            data_parallel_rank=dist.get_rank(dpg.dp_pg),
            data_parallel_size=dpg.dp_pg.size(),
            drop_last=dataloader_drop_last,
            global_batch_size=global_batch_size,
            pad_samples_to_global_batch_size=cfg.pad_samples_to_global_batch_size,
        )
    elif cfg.dataloader_type == "cyclic":
        batch_sampler = MegatronPretrainingRandomSampler(
            total_samples=len(dataset),
            consumed_samples=consumed_samples,
            micro_batch_size=micro_batch_size,
            data_parallel_rank=dist.get_rank(dpg.dp_pg),
            data_parallel_size=dpg.dp_pg.size(),
            drop_last=dataloader_drop_last,
        )
    else:
        raise ValueError('cfg.dataloader_type must be "single" or "cyclic"')

    # We use the data collator to put the tensors on the right pipeline parallelism rank
    data_collator = DataCollatorForCLM(
        sequence_length=sequence_length,
        input_pp_rank=input_pp_rank,
        output_pp_rank=output_pp_rank,
        dpg=dpg,
    )

    return DataLoader(
        dataset,
        batch_sampler=batch_sampler,
        num_workers=num_workers,
        collate_fn=data_collator,
        pin_memory=dataloader_pin_memory,
        worker_init_fn=get_dataloader_worker_init(dp_rank=dist.get_rank(dpg.dp_pg)),
    )


def get_dataloader_worker_init(dp_rank: int):
    """Creates random states for each worker in order to get different state in each workers"""

    def dataloader_worker_init(worker_id):
        # Dataloader is TP/PP synced in random states
        seed = 2 ** (1 + worker_id) * 3 ** (1 + dp_rank) % (2**32)
        set_random_seed(seed)

    return dataloader_worker_init


class EmptyInfiniteDataset:
    """Hack as removing all columns from a datasets.Dataset makes the number of rows 0."""

    def __init__(self, length: int):
        self._length = length

    def __getitem__(self, item) -> Dict:
        if isinstance(item, int):
            return {}
        raise NotImplementedError(f"{item} of type {type(item)} is not supported yet")

    def __len__(self) -> int:
        return self._length
