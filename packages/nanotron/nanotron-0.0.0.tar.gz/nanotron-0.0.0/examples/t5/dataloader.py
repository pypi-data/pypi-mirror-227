import dataclasses
from typing import Dict, Generator, List, Union

import numpy as np
import torch
from datasets import Dataset, Features, Sequence, Value
from modeling_t5 import T5ForTraining
from torch.utils.data import BatchSampler, DataLoader, RandomSampler
from transformers import PreTrainedTokenizerBase, T5Config

from brrr.core import distributed as dist
from brrr.core.parallelism.pipeline_parallelism.tensor_pointer import TensorPointer
from brrr.core.process_groups_initializer import DistributedProcessGroups
from brrr.core.random import set_random_seed


def dummy_infinite_data_generator(
    micro_batch_size: int,
    input_sequence_length: int,
    target_sequence_length: int,
    model: T5ForTraining,
    config: T5Config,
    seed: int,
    dpg: DistributedProcessGroups,
):
    encoder_input_pp_rank = model.model.encoder_embedding.rank
    decoder_input_pp_rank = model.model.decoder_embedding.rank
    output_pp_rank = model.loss.rank

    def dummy_infinite_data_generator() -> Generator[Dict[str, Union[torch.Tensor, TensorPointer]], None, None]:
        # Random generator
        generator = torch.Generator(device="cuda")
        # Make sure that TP are synced always
        generator.manual_seed(seed * (1 + dist.get_rank(dpg.dp_pg)) * (1 + dist.get_rank(dpg.pp_pg)))

        # TODO @thomasw21: randint has to be synchronized across TP
        while True:
            yield {
                "encoder_input_ids": torch.randint(
                    0,
                    config.vocab_size,
                    (micro_batch_size, input_sequence_length),
                    dtype=torch.long,
                    device="cuda",
                    generator=generator,
                )
                if dist.get_rank(dpg.pp_pg) == encoder_input_pp_rank
                else TensorPointer(group_rank=encoder_input_pp_rank),
                "encoder_input_mask": torch.ones(
                    micro_batch_size,
                    input_sequence_length,
                    dtype=torch.bool,
                    device="cuda",
                )
                if dist.get_rank(dpg.pp_pg) == encoder_input_pp_rank
                else TensorPointer(group_rank=encoder_input_pp_rank),
                "decoder_input_ids": torch.randint(
                    0,
                    config.vocab_size,
                    (micro_batch_size, target_sequence_length),
                    dtype=torch.long,
                    device="cuda",
                    generator=generator,
                )
                if dist.get_rank(dpg.pp_pg) == decoder_input_pp_rank
                else TensorPointer(group_rank=decoder_input_pp_rank),
                "decoder_input_mask": torch.ones(
                    micro_batch_size,
                    target_sequence_length,
                    dtype=torch.bool,
                    device="cuda",
                )
                if dist.get_rank(dpg.pp_pg) == decoder_input_pp_rank
                else TensorPointer(group_rank=decoder_input_pp_rank),
                "decoder_label_ids": torch.randint(
                    0,
                    config.vocab_size,
                    (micro_batch_size, target_sequence_length),
                    dtype=torch.long,
                    device="cuda",
                    generator=generator,
                )
                if dist.get_rank(dpg.pp_pg) == output_pp_rank
                else TensorPointer(group_rank=output_pp_rank),
                "decoder_label_mask": torch.ones(
                    micro_batch_size,
                    target_sequence_length,
                    dtype=torch.bool,
                    device="cuda",
                )
                if dist.get_rank(dpg.pp_pg) == output_pp_rank
                else TensorPointer(group_rank=output_pp_rank),
            }

    return dummy_infinite_data_generator


# Span corruption: https://cs.github.com/google-research/text-to-text-transfer-transformer/blob/f0cf9e8c51bd48699265763d01c2f8b24ae1098b/t5/data/tasks.py#L45

# Copied from: https://github.com/huggingface/transformers/blob/c59d71b28235bd75cf78ca31cee3b559284a232a/src/transformers/models/t5/modeling_flax_t5.py#L61
def shift_tokens_right(input_ids: np.array, pad_token_id: int, decoder_start_token_id: int) -> np.ndarray:
    """
    Shift input ids one token to the right.
    """
    shifted_input_ids = np.zeros_like(input_ids)
    shifted_input_ids[:, 1:] = input_ids[:, :-1]
    shifted_input_ids[:, 0] = decoder_start_token_id

    shifted_input_ids = np.where(shifted_input_ids == -100, pad_token_id, shifted_input_ids)
    return shifted_input_ids


# Adapted from: https://github.com/huggingface/transformers/blob/32525428e131c44f7237d05d676df9460f86bbfb/examples/flax/language-modeling/run_t5_mlm_flax.py#L249
def compute_input_and_target_lengths(inputs_length, noise_density, mean_noise_span_length):
    """This function is copy of `random_spans_helper <https://github.com/google-research/text-to-text-transfer-transformer/blob/84f8bcc14b5f2c03de51bd3587609ba8f6bbd1cd/t5/data/preprocessors.py#L2466>`__ .
    Training parameters to avoid padding with random_spans_noise_mask.
    When training a model with random_spans_noise_mask, we would like to set the other
    training hyperparmeters in a way that avoids padding.
    This function helps us compute these hyperparameters.
    We assume that each noise span in the input is replaced by extra_tokens_per_span_inputs sentinel tokens,
    and each non-noise span in the targets is replaced by extra_tokens_per_span_targets sentinel tokens.
    This function tells us the required number of tokens in the raw example (for split_tokens())
    as well as the length of the encoded targets. Note that this function assumes
    the inputs and targets will have EOS appended and includes that in the reported length.
    Args:
        inputs_length: an integer - desired length of the tokenized inputs sequence
        noise_density: a float
        mean_noise_span_length: a float
    Returns:
        tokens_length: length of original text in tokens
        targets_length: an integer - length in tokens of encoded targets sequence
    """

    def _tokens_length_to_inputs_length_targets_length(tokens_length):
        num_noise_tokens = int(round(tokens_length * noise_density))
        num_nonnoise_tokens = tokens_length - num_noise_tokens
        num_noise_spans = int(round(num_noise_tokens / mean_noise_span_length))
        # inputs contain all nonnoise tokens, sentinels for all noise spans
        # and one EOS token.
        _input_length = num_nonnoise_tokens + num_noise_spans + 1
        _output_length = num_noise_tokens + num_noise_spans + 1
        return _input_length, _output_length

    tokens_length = inputs_length

    while _tokens_length_to_inputs_length_targets_length(tokens_length + 1)[0] <= inputs_length:
        tokens_length += 1

    inputs_length, targets_length = _tokens_length_to_inputs_length_targets_length(tokens_length)

    # minor hack to get the targets length to be equal to inputs length
    # which is more likely to have been set to a nice round number.
    if noise_density == 0.5 and targets_length > inputs_length:
        tokens_length -= 1
        targets_length -= 1
    return tokens_length, targets_length


def compute_original_num_tokens(input_length: int, target_length: int, mean_noise_span_length: int):
    """
    Args:
        input_length: int, desired length of the tokenized input sequence
        target_length: int, desired length of tokenizer output sequence
        mean_noise_span_length: a float
    Returns:
        original_num_tokens: int, number of tokens you need to extract from raw text
    """
    # TODO @thomasw21: Do I have to round that?
    num_spans = int(target_length / (mean_noise_span_length + 1))
    original_num_tokens = input_length + target_length - 2 * (num_spans + 1)
    return original_num_tokens, num_spans


# Adapted from: https://github.com/huggingface/transformers/blob/32525428e131c44f7237d05d676df9460f86bbfb/examples/flax/language-modeling/run_t5_mlm_flax.py#LL297-L459
@dataclasses.dataclass
class DataCollatorForT5MLM:
    """
    Data collator used for T5 span-masked language modeling.
    It is made sure that after masking the inputs are of length `data_args.max_seq_length` and targets are also of fixed length.
    For more information on how T5 span-masked language modeling works, one can take a look
    at the `official paper <https://arxiv.org/pdf/1910.10683.pdf>`__
    or the `official code for preprocessing <https://github.com/google-research/text-to-text-transfer-transformer/blob/master/t5/data/preprocessors.py>`__ .
    """

    input_length: int
    target_length: int
    num_spans: int
    eos_token_id: int
    pad_token_id: int
    decoder_start_token_id: int
    # Ordered in this order they are supposed to be consumed
    sentinel_tokens_ids: np.array
    encoder_input_pp_rank: int
    decoder_input_pp_rank: int
    output_pp_rank: int
    dpg: DistributedProcessGroups

    def __call__(self, examples: List[Dict[str, np.ndarray]]) -> Dict[str, np.array]:
        # Process the case when "input_ids" doesn't exist
        current_pp_rank = dist.get_rank(self.dpg.pp_pg)
        if current_pp_rank not in [
            self.encoder_input_pp_rank,
            self.decoder_input_pp_rank,
            self.output_pp_rank,
        ]:
            assert all(len(example) == 0 for example in examples)
            return {
                "encoder_input_ids": TensorPointer(self.encoder_input_pp_rank),
                "encoder_input_mask": TensorPointer(self.encoder_input_pp_rank),
                "decoder_input_ids": TensorPointer(self.decoder_input_pp_rank),
                "decoder_input_mask": TensorPointer(self.decoder_input_pp_rank),
                "decoder_label_ids": TensorPointer(self.output_pp_rank),
                "decoder_label_mask": TensorPointer(self.output_pp_rank),
            }

        # Make sure we load only what's necessary, ie we only load a `input_ids` column.
        assert all(list(example.keys()) == ["input_ids"] for example in examples)

        # Make sure that this is synchronized for TP and PP

        # TODO @thomasw21: This looks horrible, can this not run concatenation? We load an entire contiguous array? Probably not due to random sampling
        input_ids = np.vstack([examples[i]["input_ids"] for i in range(len(examples))])
        batch_size, expanded_input_length = input_ids.shape

        # TODO @thomasw21: Let's build a batched version of this.
        mask_indices = np.asarray(
            [self.random_spans_noise_mask(expanded_input_length) for _ in range(batch_size)],
            dtype=np.int8,
        )

        result: Dict[str, Union[np.array, TensorPointer]] = {}
        if current_pp_rank == self.encoder_input_pp_rank:
            input_ids_sentinel = self.create_sentinel_ids(mask_indices)
            result["encoder_input_ids"] = self.filter_input_ids(input_ids, input_ids_sentinel)
            result["encoder_input_mask"] = np.ones((batch_size, self.input_length), dtype=np.bool_)
        else:
            result["encoder_input_ids"] = TensorPointer(group_rank=self.encoder_input_pp_rank)
            result["encoder_input_mask"] = TensorPointer(group_rank=self.encoder_input_pp_rank)

        result["decoder_input_ids"] = TensorPointer(group_rank=self.decoder_input_pp_rank)
        result["decoder_input_mask"] = TensorPointer(group_rank=self.decoder_input_pp_rank)
        result["decoder_label_ids"] = TensorPointer(group_rank=self.output_pp_rank)
        result["decoder_label_mask"] = TensorPointer(group_rank=self.output_pp_rank)
        if current_pp_rank in [self.decoder_input_pp_rank, self.output_pp_rank]:
            labels_mask = 1 - mask_indices
            labels_sentinel = self.create_sentinel_ids(labels_mask)
            label_ids = self.filter_input_ids(input_ids, labels_sentinel)

            if current_pp_rank == self.decoder_input_pp_rank:
                result["decoder_input_ids"] = shift_tokens_right(
                    label_ids, self.pad_token_id, self.decoder_start_token_id
                )
                result["decoder_input_mask"] = np.ones((batch_size, self.target_length), dtype=np.bool_)

            if current_pp_rank == self.output_pp_rank:
                result["decoder_label_ids"] = label_ids
                result["decoder_label_mask"] = np.ones((batch_size, self.target_length), dtype=np.bool_)

        if (
            isinstance(result["encoder_input_ids"], torch.Tensor)
            and result["encoder_input_ids"].shape[-1] != self.input_length
        ):
            raise ValueError(
                f"`input_ids` are incorrectly preprocessed. `input_ids` length is {result['encoder_input_ids'].shape[-1]}, but"
                f" should be {self.input_length}."
            )

        if (
            isinstance(result["decoder_input_ids"], torch.Tensor)
            and result["decoder_input_ids"].shape[-1] != self.target_length
        ):
            raise ValueError(
                f"`labels` are incorrectly preprocessed. `labels` length is {result['decoder_input_ids'].shape[-1]}, but should be"
                f" {self.target_length}."
            )

        if (
            isinstance(result["decoder_label_ids"], torch.Tensor)
            and result["decoder_label_ids"].shape[-1] != self.target_length
        ):
            raise ValueError(
                f"`labels` are incorrectly preprocessed. `labels` length is {result['decoder_label_ids'].shape[-1]}, but should be"
                f" {self.target_length}."
            )

        # Cast np.array to torch.Tensor
        result = {k: v if isinstance(v, TensorPointer) else torch.from_numpy(v) for k, v in result.items()}

        # Check that all tensors are contiguous
        # TODO @thomasw21: Remove once I don't need it anymore.
        for k, v in result.items():
            if isinstance(v, torch.Tensor) and not v.is_contiguous():
                print(f"Somehow {k} was not contiguous")

        return result

    def create_sentinel_ids(self, mask_indices):
        """
        Sentinel ids creation given the indices that should be masked.
        The start indices of each mask are replaced by the sentinel ids in increasing
        order. Consecutive mask indices to be deleted are replaced with `-1`.
        """
        # TODO @thomasw21: This is computed during the random mask generator, no need to redo it no?
        start_indices = mask_indices - np.roll(mask_indices, 1, axis=-1) * mask_indices
        # TODO @thomasw21: Isn't that not always `False`? Since the first token is always False.
        start_indices[:, 0] = mask_indices[:, 0]

        # TODO @thomasw21: start_indices is just like `span_start_indices` but only counting which ones are labels, which ones are not.

        # TODO @thomas: change this in order to support arbitrary support of tokenizer
        sentinel_ids = np.where(
            start_indices != 0,
            self.sentinel_tokens_ids[np.cumsum(start_indices, axis=-1)],
            0,
        )
        sentinel_ids -= mask_indices - start_indices

        return sentinel_ids

    def filter_input_ids(self, input_ids, sentinel_ids):
        """
        Puts sentinel mask on `input_ids` and fuse consecutive mask tokens into a single mask token by deleting.
        This will reduce the sequence length from `expanded_inputs_length` to `input_length`.
        """
        batch_size = input_ids.shape[0]

        input_ids_full = np.where(sentinel_ids != 0, sentinel_ids, input_ids)
        # input_ids tokens and sentinel tokens are >= 0, tokens < 0 are
        # masked tokens coming after sentinel tokens and should be removed
        input_ids = input_ids_full[input_ids_full >= 0].reshape((batch_size, -1))
        # Add trailing <eos>
        input_ids = np.concatenate(
            [
                input_ids,
                np.full((batch_size, 1), self.eos_token_id, dtype=np.int32),
            ],
            axis=-1,
        )
        return input_ids

    def random_spans_noise_mask(self, length):
        """This function is copy of `random_spans_helper <https://github.com/google-research/text-to-text-transfer-transformer/blob/84f8bcc14b5f2c03de51bd3587609ba8f6bbd1cd/t5/data/preprocessors.py#L2682>`__ .
        Noise mask consisting of random spans of noise tokens.
        The number of noise tokens and the number of noise spans and non-noise spans
        are determined deterministically as follows:
        num_noise_tokens = round(length * noise_density)
        num_nonnoise_spans = num_noise_spans = round(num_noise_tokens / mean_noise_span_length)
        Spans alternate between non-noise and noise, beginning with non-noise.
        Subject to the above restrictions, all masks are equally likely.
        Args:
            length: an int32 scalar (length of the incoming token sequence)
        Returns:
            a boolean tensor with shape [length]
        """

        orig_length = length

        num_noise_spans = self.num_spans
        # -1 is because of extra <eos> at the end
        num_noise_tokens = self.target_length - num_noise_spans - 1
        num_nonnoise_tokens = self.input_length - num_noise_spans - 1

        # TODO @thomasw21, If that's true I can remove the need for `orig_length`
        assert num_noise_tokens + num_nonnoise_tokens == orig_length

        # pick the lengths of the noise spans and the non-noise spans
        def _random_segmentation(num_items, num_segments):
            """Partition a sequence of items randomly into non-empty segments.
            Args:
                num_items: an integer scalar > 0
                num_segments: an integer scalar in [1, num_items]
            Returns:
                a Tensor with shape [num_segments] containing positive integers that add
                up to num_items
            """
            # TODO @thomasw21: Maybe run preprocessing in another precision to be faster?
            mask_indices = np.arange(num_items - 1) < (num_segments - 1)
            np.random.shuffle(mask_indices)
            first_in_segment = np.pad(mask_indices, [[1, 0]])

            # TODO @thomasw21: Check if this operation is equivalent to the top one, if so let's use it.
            # # Thomas' version of `first_in_segment`
            # mask_indices = np.arange(num_items) > num_items - num_segments
            # np.random.shuffle(mask_indices[1:])
            # first_in_segment = mask_indices

            segment_id = np.cumsum(first_in_segment)
            # count length of sub segments assuming that list is sorted
            _, segment_length = np.unique(segment_id, return_counts=True)
            return segment_length

        # TODO @thomasw21: can't I just run this using `_random_segmentation(orig_length, 2 * num_noise_spans)
        noise_span_lengths = _random_segmentation(num_noise_tokens, num_noise_spans)
        nonnoise_span_lengths = _random_segmentation(num_nonnoise_tokens, num_noise_spans)

        # TODO @thomasw21: Assuming that lengths are always strictly positive, the first token can never be noise.
        interleaved_span_lengths = np.reshape(
            np.stack([nonnoise_span_lengths, noise_span_lengths], axis=1),
            [num_noise_spans * 2],
        )
        span_starts = np.cumsum(interleaved_span_lengths[:-1])
        span_start_indicator = np.zeros((length,), dtype=np.int8)
        span_start_indicator[span_starts] = True
        span_num = np.cumsum(span_start_indicator)
        is_noise = np.equal(span_num % 2, 1)

        return is_noise


# Adapted from: https://github.com/huggingface/transformers/blob/8ad06b7c13871dc08e985a61ef35d69c0a23bd6d/examples/pytorch/language-modeling/run_mlm.py#L467-L483
# Main data processing function that will concatenate all texts from our dataset and generate chunks of
# max_seq_length.
def group_texts(max_seq_length: int):
    def _group_texts(examples: Dict[str, List[np.array]]) -> Dict[str, List[np.array]]:
        # TODO @thomasw21: Figure out if we need to get original document belonging or if this doesn't matter at all
        # Concatenate all texts.
        concatenated_examples = {k: np.concatenate(v) for k, v in examples.items()}
        # We assume that all column have the same lengths, and thus the same concatenated length
        total_length = len(next(iter(concatenated_examples.values())))
        # We drop the small remainder, we could add padding if the model supported it instead of this drop, you can
        # customize this part to your needs.
        # TODO @thomasw21: We might want to mimick original implementation and get a random chunck
        assert total_length >= max_seq_length, "The document you provided is too small"

        # Split by chunks of max_len.
        result = {
            k: [t[end - max_seq_length : end] for end in range(max_seq_length, total_length, max_seq_length)]
            for k, t in concatenated_examples.items()
        }
        return result

    return _group_texts


def tokenize_and_group_texts(tokenizer: PreTrainedTokenizerBase, max_seq_length: int):
    grouper = group_texts(max_seq_length)

    def _tokenize_and_group_texts(texts: List[str]) -> Dict[str, List[np.array]]:
        # TODO @thomasw21: Maybe using attention mask to get segment ids makes sense
        tokenized_batch = tokenizer.batch_encode_plus(texts, return_attention_mask=False)
        tokenized_batch = {k: [np.array(tokenized_texts) for tokenized_texts in v] for k, v in tokenized_batch.items()}
        return grouper(tokenized_batch)

    return _tokenize_and_group_texts


def mlm_process(
    tokenizer: PreTrainedTokenizerBase,
    dataset: Dataset,
    text_column: str,
    input_sequence_length: int,
    target_sequence_length: int,
    mean_noise_span_length: int,
    processing_num_proc: int,
):
    """Given a dataset holding tokenized text, this method does the following:
    - tokenizer data using given tokenizer
    - concatenate file and return chunks of `a defined size`
    - run mlm (t5 style) and return a DataLoader

    It should be roughly equivalent to https://cs.github.com/google-research/text-to-text-transfer-transformer/blob/f0cf9e8c51bd48699265763d01c2f8b24ae1098b/t5/data/preprocessors.py#L1923
    """
    # # TODO @thomasw21: We should probably change this function in order to support `target_sequence_length` as an argument.
    # original_tokens_length_to_extract, _target_sequence_length = compute_input_and_target_lengths(
    #     inputs_length=input_sequence_length,
    #     noise_density=noise_density,
    #     mean_noise_span_length=mean_noise_span_length,
    # )
    # assert _target_sequence_length == target_sequence_length

    # Interestingly T5 have the same number of spans in each sample, ie it's not that random
    # https://cs.github.com/google-research/text-to-text-transfer-transformer/blob/f0cf9e8c51bd48699265763d01c2f8b24ae1098b/t5/data/preprocessors.py#L2940
    # for (512,114) the number of spans is 28
    # therefore given a target_length, we can compute the original_tokens_length_to_extract
    original_tokens_length_to_extract, num_spans = compute_original_num_tokens(
        input_length=input_sequence_length,
        target_length=target_sequence_length,
        mean_noise_span_length=mean_noise_span_length,
    )

    # Check that we have enough sentinel tokens
    assert num_spans <= len(
        tokenizer.additional_special_tokens_ids
    ), f"We need to generate {num_spans} when we only have {len(tokenizer.additional_special_tokens_ids)} sentinel tokens to use."

    # tokenize data and group tests
    dataset = dataset.map(
        # TODO @thomasw21: Make sure that all the tokenization options are good.
        tokenize_and_group_texts(tokenizer=tokenizer, max_seq_length=original_tokens_length_to_extract),
        input_columns=text_column,
        features=Features(
            {"input_ids": Sequence(feature=Value(dtype="int64"), length=original_tokens_length_to_extract)}
        ),
        remove_columns=dataset.column_names,
        batched=True,
        num_proc=processing_num_proc,
    )

    # TODO @thomasw21: Save dataset, and reuse if we already have access to it already (ie build a caching mechanism)

    return dataset


def get_dataloader(
    dataset: Dataset,
    input_length: int,
    target_length: int,
    mean_noise_span_length: int,
    eos_token_id: int,
    pad_token_id: int,
    decoder_start_token_id: int,
    sentinel_tokens_ids: np.array,
    encoder_input_pp_rank: int,
    decoder_input_pp_rank: int,
    output_pp_rank: int,
    num_proc: int,
    batch_size: int,
    seed: int,
    dpg: DistributedProcessGroups,
):
    # TODO @thomasw21: This doesn't work super well with datasets, as loading a entire batch runs `batch_size` query, we can probably build a better one
    _, num_spans = compute_original_num_tokens(
        input_length=input_length,
        target_length=target_length,
        mean_noise_span_length=mean_noise_span_length,
    )

    # Only some rank require to run the dataloader.
    if dist.get_rank(dpg.pp_pg) not in [
        encoder_input_pp_rank,
        decoder_input_pp_rank,
        output_pp_rank,
    ]:
        # dataset has to have a single column, with `input_ids` as the column name
        assert dataset.column_names == ["input_ids"]
        dataset_length = len(dataset)
        dataset = dataset.remove_columns(column_names="input_ids")
        assert (
            len(dataset) == 0
        ), f"Dataset has to be empty after removing the `input_ids` column. Current dataset: {dataset}"
        # HACK as if we remove the last column of a dataset, it becomes empty and it's number of rows becomes empty.
        dataset = EmptyInfiniteDataset(length=dataset_length)
        # No need to spawn a lot of workers, we can just use main
        num_proc = 0
    else:
        dataset = dataset.with_format(type="numpy", columns=["input_ids"], output_all_columns=True)

    # TODO @thomasw21: Make sure that tp_pg/pp_pg are synchronized in the sampling ... I need to fucking make sure of that which is fucking tricky.

    return DataLoader(
        dataset=dataset,
        num_workers=num_proc,
        # TODO @thomasw21: Do I actually want to drop the last one?
        # TODO @thomasw21: This is not efficient when using with dataset.
        batch_sampler=BatchSampler(RandomSampler(dataset), batch_size=batch_size, drop_last=True),
        collate_fn=DataCollatorForT5MLM(
            input_length=input_length,
            target_length=target_length,
            num_spans=num_spans,
            eos_token_id=eos_token_id,
            pad_token_id=pad_token_id,
            decoder_start_token_id=decoder_start_token_id,
            sentinel_tokens_ids=sentinel_tokens_ids,
            encoder_input_pp_rank=encoder_input_pp_rank,
            decoder_input_pp_rank=decoder_input_pp_rank,
            output_pp_rank=output_pp_rank,
            dpg=dpg,
        ),
        pin_memory=True,
        worker_init_fn=get_dataloader_worker_init(dp_rank=dist.get_rank(dpg.dp_pg)),
        # TODO @thomasw21: I'm not sure but this doesn't seem to work at all.
        # pin_memory_device="cuda",
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
