import dataclasses
import logging
from typing import Dict, Generator, List, Optional, Union

import datasets
import numpy as np
import torch
from config import PretrainNemoArgs
from dataset import GPTDataset, build_train_valid_test_datasets
from datasets import Dataset, Features, Sequence, Value
from nemo_dataset.data_samplers import MegatronPretrainingRandomSampler, MegatronPretrainingSampler
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler
from transformers import PreTrainedTokenizerBase
from transformers.trainer_pt_utils import DistributedSamplerWithLoop

from brrr.core import distributed as dist
from brrr.core.logging import log_rank
from brrr.core.parallelism.pipeline_parallelism.tensor_pointer import TensorPointer
from brrr.core.process_groups_initializer import DistributedProcessGroups
from brrr.core.random import set_random_seed

logger = logging.getLogger(__name__)


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
        tokenized_batch = tokenizer.batch_encode_plus(texts, return_attention_mask=False)
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
    micro_batch_size: Optional[int] = None,
    drop_last: Optional[bool] = True,
) -> Optional[torch.utils.data.Sampler]:
    """returns sampler that restricts data loading to a subset of the dataset proper to the DP rank"""

    # Build the sampler.
    # TODO @nouamanetazi: Support group_by_length: https://github.com/huggingface/transformers/blob/47e1676255e5dd86b9541f734cd4f4bdcbb50f4a/src/transformers/trainer.py#L783-L810

    if use_loop_to_round_batch_size:
        assert micro_batch_size is not None
        # loops at the end back to the beginning of the shuffled samples to make each process have a round multiple of batch_size samples.
        return DistributedSamplerWithLoop(
            train_dataset,
            batch_size=micro_batch_size,
            num_replicas=dp_size,
            rank=dp_rank,
            seed=seed,
            drop_last=drop_last,
        )
    else:
        return DistributedSampler(train_dataset, num_replicas=dp_size, rank=dp_rank, seed=seed, drop_last=drop_last)


# Adapted from https://github.com/huggingface/transformers/blob/47e1676255e5dd86b9541f734cd4f4bdcbb50f4a/src/transformers/trainer.py#L837
def get_train_dataloader(
    train_dataset: Dataset,
    sequence_length: int,
    dpg: DistributedProcessGroups,
    input_pp_rank: int,
    output_pp_rank: int,
    micro_batch_size: int,
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
