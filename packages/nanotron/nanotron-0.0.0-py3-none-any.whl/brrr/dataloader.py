from typing import Dict, Generator, Iterator, Union

import torch

from brrr.config import Config
from brrr.core import distributed as dist
from brrr.core import logging
from brrr.core.parallelism.pipeline_parallelism.tensor_pointer import TensorPointer
from brrr.core.process_groups_initializer import DistributedProcessGroups
from brrr.core.utils import (
    assert_fail_except_rank_with,
    assert_tensor_synced_across_pg,
)

try:

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
