import contextlib
from enum import Enum
from pathlib import Path
from typing import List, Optional, Tuple, Union

import fsspec
from datasets.download.streaming_download_manager import xPath
from fsspec.implementations import local

from brrr.config import Config
from brrr.core import logging
from brrr.core.dataclass import DistributedProcessGroups
from brrr.core.logging import log_rank

logger = logging.get_logger(__name__)


class ObjectType(Enum):
    MODEL = "model"
    OPTIMIZER = "optimizer"
    LR_SCHEDULER = "lr_scheduler"


def parse_ckpt_path(config: Config):
    load_from_candidate = config.checkpoints.load_from_specific_checkpoint
    if load_from_candidate is None:
        latest_meta_path: xPath = config.checkpoints.checkpoints_path / "latest.txt"
        if latest_meta_path.exists():
            with fs_open(config.checkpoints.checkpoints_path / "latest.txt", mode="r") as fi:
                # TODO @thomasw21: make a better structure system so that we get typing correct
                load_from_candidate = int(fi.read())
        checkpoint_path = None
    else:
        checkpoint_path = config.checkpoints.checkpoints_path / str(load_from_candidate)
        log_rank(
            f"Loading checkpoint from {checkpoint_path}:",
            logger=logger,
            level=logging.INFO,
            rank=0,
        )
    return checkpoint_path


def get_tp_and_pp_rank_and_size_from(
    world_rank: int, dpg: DistributedProcessGroups
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    result = dpg.get_3d_ranks(world_rank=world_rank)
    return (result[2], dpg.tp_pg.size()), (result[0], dpg.pp_pg.size())


def get_path(
    tensor_name: str,
    type: ObjectType,
    # Return rank and size
    # TODO @thomasw21: make a topology agnostic system
    tp_and_pp_rank_and_size: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None,
) -> List[str]:
    suffix = tensor_name.split(".")
    suffix_path, suffix_name = suffix[:-1], suffix[-1]

    if tp_and_pp_rank_and_size:
        (tp_rank, tp_size), (pp_rank, pp_size) = tp_and_pp_rank_and_size
        suffix_name = (
            f"{type.value}_{suffix_name}_pp-rank-{pp_rank}-of-{pp_size}_tp-rank-{tp_rank}-of-{tp_size}.safetensors"
        )
    else:
        suffix_name = f"{type.value}_{suffix_name}.safetensors"

    suffix_path.append(suffix_name)
    return suffix_path


def get_filesystem_and_path(path: Path, storage_options=None) -> Tuple[fsspec.AbstractFileSystem, str]:
    # Use supported filesystems in `fsspec`. If you need another one, please use `fsspec.registry.register_implementation`
    # DO NOT USE `mode` argument as it adds a suffix `0.part` when using `mode="w"`.
    fs, _, paths = fsspec.core.get_fs_token_paths(str(path), storage_options=storage_options)
    assert len(paths) == 1
    return fs, paths[0]


@contextlib.contextmanager
def fs_open(
    file: Union[str, Path],
    mode="r",
):
    # TODO @thomasw21: pass storage options
    fs, path = get_filesystem_and_path(file)
    with fs.open(path, mode=mode) as f:
        yield f


def check_path_is_local(path: Path, storage_options=None) -> bool:
    return isinstance(get_filesystem_and_path(path=path, storage_options=storage_options)[0], local.LocalFileSystem)
