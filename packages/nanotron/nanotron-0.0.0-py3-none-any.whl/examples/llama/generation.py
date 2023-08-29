import dataclasses
from itertools import chain, islice
from typing import Generator, Iterable, List, Optional, Tuple, Union

import torch
from modeling_llama import LlamaModel
from sampler import BasicSampler
from transformers import LlamaTokenizer

from brrr.core import distributed as dist
from brrr.core.dataclass import DistributedProcessGroups
from brrr.core.distributed import ProcessGroup, get_global_rank
from brrr.core.parallelism.pipeline_parallelism.context_manager import attach_pipeline_state_to_model
from brrr.core.parallelism.pipeline_parallelism.p2p import (
    P2P,
    TensorMetaData,
    view_as_contiguous,
)
from brrr.core.parallelism.pipeline_parallelism.state import PipelineEvalBatchState
from brrr.core.parallelism.pipeline_parallelism.tensor_pointer import TensorPointer
from brrr.core.utils import get_untyped_storage
from brrr.store import Store, attach_store


@dataclasses.dataclass
class GenerationInput:
    text: str


@dataclasses.dataclass
class GenerationInputs:
    input_ids: Union[torch.Tensor, TensorPointer]  # [B, S]
    input_masks: Union[torch.Tensor, TensorPointer]


@dataclasses.dataclass
class GenerationOutput:
    input_ids: Union[torch.Tensor, TensorPointer]
    generation_ids: Union[torch.Tensor, TensorPointer]


@dataclasses.dataclass
class GenerationStates:
    new_input_ids: Union[torch.Tensor, TensorPointer]
    new_input_mask: Union[torch.Tensor, TensorPointer]
    store: Store

    # The rest of the state I need to reconstruct the generated output
    generation_ids: List[Union[torch.Tensor, TensorPointer]]
    generation_mask: List[Union[torch.Tensor, TensorPointer]]


@dataclasses.dataclass
class GenerationConfig:
    max_new_tokens: int
    max_micro_batch_size: int


@dataclasses.dataclass
class TokenizerConfig:
    max_input_length: Optional[int]
    truncation: Optional[Union[str, bool]] = None
    padding: Optional[Union[str, bool]] = None


def chunks(iterable, chunk_size: int) -> Generator[List, None, None]:
    """Yield successive n-sized chunks from `iterable`"""
    assert chunk_size >= 1
    iterator = iter(iterable)
    for first in iterator:
        yield list(chain([first], islice(iterator, chunk_size - 1)))


def micro_batcher(
    input_iter: Iterable[GenerationInput],
    tokenizer: LlamaTokenizer,
    max_micro_batch_size: int,
    tokenizer_config: TokenizerConfig,
    dpg: DistributedProcessGroups,
    input_rank: int,
) -> Generator[GenerationInputs, None, None]:
    if tokenizer_config.padding is None:
        tokenizer_config.padding = "max_length" if tokenizer_config.max_input_length is not None else True
    if tokenizer_config.truncation is None:
        tokenizer_config.truncation = True if tokenizer_config.max_input_length is not None else None

    for micro_batch_id, micro_batch in enumerate(chunks(input_iter, chunk_size=max_micro_batch_size)):
        if len(micro_batch) == 0:
            # Empty micro batches don't matter
            return

        if micro_batch_id % dpg.dp_pg.size() != dist.get_rank(dpg.dp_pg):
            # Each dp is responsible for its own micro batches
            continue

        if dist.get_rank(dpg.pp_pg) == input_rank:
            encodings = tokenizer(
                [elt.text for elt in micro_batch],
                return_tensors="pt",
                return_attention_mask=True,
                padding=tokenizer_config.padding,
                max_length=tokenizer_config.max_input_length,
                truncation=tokenizer_config.truncation,
            )

            encodings["attention_mask"] = encodings.attention_mask.to(dtype=torch.bool, device="cuda")
            encodings.to("cuda")
            yield GenerationInputs(input_ids=encodings.input_ids, input_masks=encodings.attention_mask)
        else:
            yield GenerationInputs(
                input_ids=TensorPointer(group_rank=input_rank), input_masks=TensorPointer(group_rank=input_rank)
            )


@torch.inference_mode()
def greedy_search(
    input_iter: Iterable[GenerationInput],
    tokenizer: LlamaTokenizer,
    model: LlamaModel,
    p2p: P2P,
    dpg: DistributedProcessGroups,
    generation_config: GenerationConfig,
    tokenizer_config: Optional[TokenizerConfig],
) -> Generator[GenerationOutput, None, None]:
    """We assume the following:
    - Everyone receives ALL the input text. # TODO @thomasw21: technically only specific ranks need to receive input.
    - Only a specific rank will output the generated text_ids as `torch.Tensor`, the others return a `TensorPointer`. # TODO @thomasw21: Maybe all ranks should return the text.
    - We assume that within a model replica, the inputs are already synchronized.
    """

    # TODO @thomasw21: Fix this issue of knowing there the `decoder_input_rank`/`decode_logit_rank` is
    decoder_input_rank = model.token_position_embeddings.rank
    decoder_logit_rank = model.cast_to_fp32.rank

    # Compute flag
    is_decoder_input_rank = dist.get_rank(dpg.pp_pg) == decoder_input_rank
    is_decoder_logit_rank = dist.get_rank(dpg.pp_pg) == decoder_logit_rank
    max_nb_microbatches = decoder_logit_rank - decoder_input_rank + 1

    # TODO @thomasw21: Fix this as we shouldn't get P2P like that
    p2p = model.p2p

    # That's annoying but I need this as soon as there's a change communication "cross"
    pipeline_state = PipelineEvalBatchState()
    with attach_pipeline_state_to_model(model=model, pipeline_state=pipeline_state):
        # We query the first `pipeline_size` batches
        for batches in chunks(
            iterable=micro_batcher(
                input_iter=input_iter,
                tokenizer=tokenizer,
                max_micro_batch_size=generation_config.max_micro_batch_size,
                tokenizer_config=tokenizer_config,
                input_rank=decoder_input_rank,
                dpg=dpg,
            ),
            chunk_size=max_nb_microbatches,
        ):
            if len(batches) == 0:
                # It means we're out of element
                return

            # Number of micro batches
            number_states_in_buffer = len(batches)
            # Otherwise the pipelining doesn't work
            assert number_states_in_buffer <= max_nb_microbatches
            is_max_nb_microbatches = number_states_in_buffer == max_nb_microbatches

            # Initialize decoder states
            decoder_states: Iterable[GenerationStates] = (
                GenerationStates(
                    new_input_ids=batch.input_ids,
                    new_input_mask=batch.input_masks,
                    store=Store(),
                    generation_ids=[batch.input_ids],
                    generation_mask=[batch.input_masks],
                )
                for batch in batches
            )

            for generation_iter in range(generation_config.max_new_tokens):
                all_new_decoder_input_ids_and_mask_same_rank: List[
                    Tuple[Union[torch.LongTensor, TensorPointer], Union[torch.BoolTensor, TensorPointer]]
                ] = []
                new_decoder_states: List[GenerationStates] = []
                for state_id, state in enumerate(decoder_states):
                    new_decoder_states.append(state)
                    # Get the new logits
                    with attach_store(model=model, store=state.store):
                        # transpose: [sequence_length, batch_size, vocab_size] -> [batch_size, sequence_length, vocab_size]
                        sharded_logits = model(
                            input_ids=state.new_input_ids,
                            input_mask=state.new_input_mask,
                        )
                        if isinstance(sharded_logits, torch.Tensor):
                            sharded_logits = sharded_logits.transpose(0, 1)

                    # Communicate
                    # TODO @thomasw21: Make a diagram to show how this works
                    nb_send: int = 0
                    if is_decoder_input_rank:
                        if is_max_nb_microbatches:
                            if generation_iter == 0:
                                if state_id == number_states_in_buffer - 1:
                                    # `2` is because we receive decoder_ids AND decoder_mask from last rank
                                    nb_send = len(pipeline_state.microbatches_activations_to_send) - 2
                                else:
                                    # Send everything
                                    nb_send = len(pipeline_state.microbatches_activations_to_send)
                            else:
                                # `2` is because we receive decoder_ids AND decoder_mask from last rank
                                nb_send = len(pipeline_state.microbatches_activations_to_send) - 2
                        else:
                            if number_states_in_buffer - 1 == state_id or generation_iter == 0:
                                # Send everything
                                nb_send = len(pipeline_state.microbatches_activations_to_send)
                            else:
                                # `2` is because we receive decoder_ids AND decoder_mask from last rank
                                nb_send = len(pipeline_state.microbatches_activations_to_send) - 2
                    else:
                        if state_id == number_states_in_buffer - 1:
                            if not is_max_nb_microbatches:
                                nb_send = len(pipeline_state.microbatches_activations_to_send)
                    for _ in range(nb_send):
                        pipeline_state.run_communication()

                    if is_decoder_logit_rank:
                        assert isinstance(sharded_logits, torch.Tensor)

                        # run a logit chooser.
                        sampler = BasicSampler(pg=dpg.tp_pg)

                        new_decoder_input_ids = sampler(sharded_logits=sharded_logits[:, -1, :])

                        # TODO @thomasw21: Handle this correctly, ie from some point after <eos> this should only generate masked tokens
                        # TODO @thomasw21: Actually I can probably build this thing on the next device directly. Will save some communication
                        new_decoder_input_mask = torch.ones(
                            size=(new_decoder_input_ids.shape[0], 1),
                            dtype=torch.bool,
                            device=new_decoder_input_ids.device,
                        )

                        # TODO @thomasw21: We need to have stop condition.

                        # broadcast new_tokens to everyone
                        if decoder_input_rank == decoder_logit_rank:
                            # It's the same rank so no need to do anything too fancy
                            all_new_decoder_input_ids_and_mask_same_rank.append(
                                (new_decoder_input_ids, new_decoder_input_mask)
                            )
                        else:
                            pipeline_state.register_send_activation(
                                new_decoder_input_ids, to_rank=decoder_input_rank, p2p=p2p
                            )
                            pipeline_state.register_send_activation(
                                new_decoder_input_mask, to_rank=decoder_input_rank, p2p=p2p
                            )
                            if not is_max_nb_microbatches and state_id == number_states_in_buffer - 1:
                                # Send new_decoder_input_ids AND new_decoder_input_ids
                                pipeline_state.run_communication()
                                pipeline_state.run_communication()

                    else:
                        assert isinstance(sharded_logits, TensorPointer)

                all_new_decoder_input_ids_and_mask: Iterable[
                    Tuple[Union[torch.LongTensor, TensorPointer], Union[torch.BoolTensor, TensorPointer]]
                ]
                if is_decoder_input_rank:
                    # We receive the tensor from other ranks unless `decoder_input_rank` == `decoder_logit_rank` in which case `all_new_decoder_input_ids` is already populated.
                    if decoder_input_rank == decoder_logit_rank:
                        # `all_new_decoder_input_ids_and_mask_same_rank` is already populated. Since `decoder_input_rank` and `decoder_logit_rank` are the same, there's no need to communicate as we can just store the new input_ids in a list.
                        assert len(all_new_decoder_input_ids_and_mask_same_rank) == number_states_in_buffer
                        all_new_decoder_input_ids_and_mask = all_new_decoder_input_ids_and_mask_same_rank
                    else:

                        def generator():
                            for _ in range(number_states_in_buffer):
                                pipeline_state.register_recv_activation(from_rank=decoder_logit_rank, p2p=p2p)
                                pipeline_state.register_recv_activation(from_rank=decoder_logit_rank, p2p=p2p)
                                while len(pipeline_state.activations_buffer) < 2:
                                    pipeline_state.run_communication()
                                new_decoder_input_ids = pipeline_state.activations_buffer.popleft()
                                new_decoder_input_mask = pipeline_state.activations_buffer.popleft()
                                yield new_decoder_input_ids, new_decoder_input_mask

                        all_new_decoder_input_ids_and_mask = iter(generator())
                else:
                    all_new_decoder_input_ids_and_mask = (
                        (TensorPointer(group_rank=decoder_input_rank), TensorPointer(group_rank=decoder_input_rank))
                        for _ in range(number_states_in_buffer)
                    )

                # Create new decoder states
                decoder_states = (
                    GenerationStates(
                        new_input_ids=new_decoder_input_ids_and_mask[0],
                        new_input_mask=new_decoder_input_ids_and_mask[1],
                        store=state.store,
                        generation_ids=state.generation_ids + [new_decoder_input_ids_and_mask[0]],
                        generation_mask=state.generation_mask + [new_decoder_input_ids_and_mask[1]],
                    )
                    for state, new_decoder_input_ids_and_mask in zip(
                        new_decoder_states, all_new_decoder_input_ids_and_mask
                    )
                )

            # Flush communication
            for _ in range(
                max(
                    len(pipeline_state.microbatches_activations_to_send),
                    len(pipeline_state.microbatches_activations_to_recv),
                )
            ):
                pipeline_state.run_communication()
            assert len(pipeline_state.microbatches_activations_to_send) == 0
            assert len(pipeline_state.microbatches_activations_to_recv) == 0

            # Yield result
            decoder_states = list(decoder_states)
            for state, batch in zip(decoder_states, batches):
                if is_decoder_input_rank:
                    assert all(isinstance(elt, torch.Tensor) for elt in state.generation_ids)
                    batch_generated_ids = torch.cat(state.generation_ids, dim=-1)
                    batch_generated_mask = torch.cat(state.generation_mask, dim=-1)
                else:
                    assert all(isinstance(elt, TensorPointer) for elt in state.generation_ids)
                    batch_generated_ids = TensorPointer(group_rank=decoder_input_rank)
                    batch_generated_mask = TensorPointer(group_rank=decoder_input_rank)

                # Broadcast all data
                batch_generated_ids, batch_generated_mask = broadcast_tensors(
                    [batch_generated_ids, batch_generated_mask], group_src=decoder_input_rank, group=dpg.pp_pg
                )
                batch.input_ids, batch.input_masks = broadcast_tensors(
                    [batch.input_ids, batch.input_masks], group_src=decoder_input_rank, group=dpg.pp_pg
                )

                # Flush the store to release memory
                state.store.flush()
                assert len(state.store) == 0

                if dist.get_rank(dpg.pp_pg) == decoder_input_rank:
                    assert (
                        batch_generated_ids.shape[0] == batch.input_ids.shape[0]
                    ), f"Batch size needs to match {batch_generated_ids.shape[0]} != {batch.input_ids.shape[0]}"
                    assert (
                        batch_generated_mask.shape[0] == batch.input_ids.shape[0]
                    ), f"Batch size needs to match {batch_generated_mask.shape[0]} != {batch.input_ids.shape[0]}"
                    assert (
                        batch_generated_ids.shape[1] == batch_generated_mask.shape[1]
                    ), f"Sequence length needs to match {batch_generated_ids.shape[1]} != {batch_generated_mask.shape[0]}"

                for i, (generated_ids, generated_mask) in enumerate(zip(batch_generated_ids, batch_generated_mask)):
                    # TODO @thomasw21: We could actually have all ranks return the output, since it's been already broadcasted
                    if dist.get_rank(dpg.pp_pg) == decoder_input_rank:
                        input_ids = batch.input_ids[i]
                        input_mask = batch.input_masks[i]
                        yield GenerationOutput(
                            input_ids=input_ids[input_mask],
                            generation_ids=generated_ids[generated_mask],
                        )
                    else:
                        yield GenerationOutput(
                            input_ids=TensorPointer(group_rank=decoder_input_rank),
                            generation_ids=TensorPointer(group_rank=decoder_input_rank),
                        )


# Distributed utilities
def broadcast_tensors(
    tensors: List[Union[torch.Tensor, TensorPointer]], group_src: int, group: Optional[ProcessGroup] = None
) -> List[torch.Tensor]:
    result = []
    for tensor in tensors:
        if dist.get_rank(group) == group_src:
            assert isinstance(tensor, torch.Tensor)
            meta = [
                [
                    tensor.dtype,
                    tensor.requires_grad,
                    tensor.shape,
                    get_untyped_storage(tensor).size(),
                    tensor.stride(),
                    tensor.is_contiguous(),
                    tensor.storage_offset(),
                ]
            ]
        else:
            assert isinstance(tensor, TensorPointer)
            meta = [None]
        dist.broadcast_object_list(meta, src=get_global_rank(group_rank=group_src, group=group), group=group)
        dtype, requires_grad, shape, untyped_storage_size, stride, is_contiguous, storage_offset = meta[0]
        meta = TensorMetaData(
            dtype=dtype,
            requires_grad=requires_grad,
            shape=shape,
            untyped_storage_size=untyped_storage_size,
            stride=stride,
            is_contiguous=is_contiguous,
            storage_offset=storage_offset,
        )
        if dist.get_rank(group) != group_src:
            tensor = meta.create_empty_storage(device=torch.device("cuda"))
        else:
            tensor = view_as_contiguous(tensor)
        dist.broadcast(tensor, src=get_global_rank(group_rank=group_src, group=group), group=group)
        # Set shape and stride
        tensor = tensor.as_strided(size=tuple(meta.shape), stride=tuple(meta.stride))
        result.append(tensor)
    return result
