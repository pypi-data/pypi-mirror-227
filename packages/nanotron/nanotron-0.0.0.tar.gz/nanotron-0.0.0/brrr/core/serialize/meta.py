import dataclasses
import json
from pathlib import Path
from typing import Any, Callable, ClassVar, Dict, List, Tuple, Type, Union

import dacite
import torch
from dacite import from_dict
from packaging.version import Version

from brrr.core import distributed as dist
from brrr.core.dataclass import DistributedProcessGroups
from brrr.core.parallelism.parameters import SlicesPair
from brrr.core.serialize.constants import CHECKPOINT_VERSION
from brrr.core.serialize.serialize import fs_open


@dataclasses.dataclass
class CheckpointMetadata:
    version: Version
    tp: int
    dp: int
    # Anything users want to store
    metas: Dict


@dataclasses.dataclass
class TensorMetadata:
    # Anything users want to store
    # Info of to what slice of the unsharded tensor (global_slices) the current sharded tensor corresponds (local_slices)
    local_global_slices_pairs: Tuple[SlicesPair, ...]
    # The shape of the unsharded tensor
    unsharded_shape: Tuple[int, ...]

    _metadata_config: ClassVar[dacite.Config] = dacite.Config(
        type_hooks={
            Tuple[SlicesPair, ...]: SlicesPair.tuple_from_str,
            Tuple[int, ...]: lambda x: torch.Size(int(size) for size in x.strip("()").split(",") if size),
        },
        strict=True,
    )

    def to_str_dict(self) -> Dict[str, str]:
        return {
            "local_global_slices_pairs": SlicesPair.tuple_to_str(self.local_global_slices_pairs),
            "unsharded_shape": str(tuple(self.unsharded_shape)),
        }

    @classmethod
    def from_str_dict(cls, dictionary: Dict[str, str]) -> "TensorMetadata":
        tensor_metadata: TensorMetadata = dacite.from_dict(
            data_class=TensorMetadata,
            data=dictionary,
            config=cls._metadata_config,
        )
        return tensor_metadata


@dataclasses.dataclass
class TensorMetadataV2:
    # Mandatory for checkpoint version higher than 1.2
    version: Version
    # Anything users want to store
    # Info of to what slice of the unsharded tensor (global_slices) the current sharded tensor corresponds (local_slices)
    local_global_slices_pairs: Tuple[SlicesPair, ...]
    # The shape of the unsharded tensor
    unsharded_shape: Tuple[int, ...]

    _metadata_config: ClassVar[dacite.Config] = dacite.Config(
        cast=[Version],
        type_hooks={
            Tuple[SlicesPair, ...]: SlicesPair.tuple_from_str,
            Tuple[int, ...]: lambda x: torch.Size(int(size) for size in x.strip("()").split(",") if size),
        },
        strict=True,
    )

    def to_str_dict(self) -> Dict[str, str]:
        return {
            "version": str(self.version),
            "local_global_slices_pairs": SlicesPair.tuple_to_str(self.local_global_slices_pairs),
            "unsharded_shape": str(tuple(self.unsharded_shape)),
        }

    @classmethod
    def from_str_dict(cls, dictionary: Dict[str, str]) -> "TensorMetadataV2":
        tensor_metadata: TensorMetadataV2 = dacite.from_dict(
            data_class=TensorMetadataV2,
            data=dictionary,
            config=cls._metadata_config,
        )
        return tensor_metadata


def process_type(elt: Any, type_hooks: Dict[Type, Callable[[Any], Any]]):
    if isinstance(elt, dict):
        return to_dict(elt, type_hooks=type_hooks)
    elif elt.__class__ in type_hooks:
        return type_hooks[elt.__class__](elt)
    elif isinstance(elt, (list, tuple)):
        return to_list(elt, type_hooks=type_hooks)
    else:
        return elt


def to_dict(dict_: Dict, type_hooks: Dict[Type, Callable[[Any], Any]]):
    result = {}
    for key, value in dict_.items():
        result[key] = process_type(value, type_hooks=type_hooks)
    return result


def to_list(list_: Union[List, Tuple], type_hooks: Dict[Type, Callable[[Any], Any]]):
    return list_.__class__((process_type(elt, type_hooks=type_hooks) for elt in list_))


def save_meta(dpg: DistributedProcessGroups, root_folder: Path, checkpoint_metadata: dict):
    if dist.get_rank(dpg.world_pg) != 0:
        return

    checkpoint_metadata = CheckpointMetadata(
        version=CHECKPOINT_VERSION, tp=dpg.tp_pg.size(), dp=dpg.dp_pg.size(), metas=checkpoint_metadata
    )

    # There are some types that require manual casting in order to work correctly.
    processed_metadata = process_type(dataclasses.asdict(checkpoint_metadata), type_hooks={Version: lambda x: str(x)})

    with fs_open(root_folder / "checkpoint_metadata.json", mode="w") as fo:
        json.dump(processed_metadata, fo, indent=2, sort_keys=True)


def load_meta(dpg: DistributedProcessGroups, root_folder: Path) -> CheckpointMetadata:
    with fs_open(root_folder / "checkpoint_metadata.json", mode="r") as fi:
        checkpoint_metadata = json.load(fi)
        checkpoint_metadata = from_dict(
            data_class=CheckpointMetadata,
            data=checkpoint_metadata,
            config=dacite.Config(
                cast=[Version],
            ),
        )
        # Assume that we're always backward compatible, we only increment CHECKPOINT_VERSION when there's a breaking change.
        assert (
            checkpoint_metadata.version <= CHECKPOINT_VERSION
        ), f"Checkpoint is of version {checkpoint_metadata.version}, Current `brrr` checkpoint version is {CHECKPOINT_VERSION}"
    return checkpoint_metadata
