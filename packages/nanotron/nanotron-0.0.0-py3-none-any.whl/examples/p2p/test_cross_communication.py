import logging
import sys

import torch
from torch import distributed as torch_dist

from brrr.core import distributed as dist
from brrr.core.logging import set_verbosity
from brrr.core.parallelism.pipeline_parallelism.p2p import P2P
from brrr.core.process_groups_initializer import DistributedProcessGroups, get_process_groups

logger = logging.getLogger(__name__)


def async_operation_bypasses_deadlock(dpg: DistributedProcessGroups, p2p: P2P):
    # TURNS OUT THAT'S DEADLOCKING AS WELL ... so `i{send/recv}` is not going to save us
    logger.info("Start async experiment")
    x = torch.ones(2, dtype=torch.float, device="cuda")

    # Send message
    if dist.get_rank(dpg.world_pg) == 0:
        send_future = torch_dist.isend(x, dst=1, group=p2p.pg)
    else:
        send_future = torch_dist.isend(x, dst=0, group=p2p.pg)

    # Recv message
    output = torch.empty(2, dtype=torch.float, device="cuda")
    if dist.get_rank(dpg.world_pg) == 0:
        recv_future = torch_dist.irecv(output, src=1, group=p2p.pg)
    else:
        recv_future = torch_dist.irecv(output, src=0, group=p2p.pg)

    send_future.wait()
    recv_future.wait()

    logger.info(f"Received: {output}")

    logger.info("Async did not deadlock and was able to cross send data.")


def deadlock_experiment(dpg: DistributedProcessGroups, p2p: P2P):
    logger.info("Start deadlock experiment")
    x = torch.ones(2, dtype=torch.float, device="cuda")

    if dist.get_rank(dpg.world_pg) == 0:
        p2p.send_tensors([x], to_rank=1)
        # Send data
    else:
        p2p.send_tensors([x], to_rank=0)

    # Observe deadlock
    raise ValueError("This should never be printed at it deadlocks")


def main():
    dpg = get_process_groups(
        data_parallel_size=1,
        pipeline_parallel_size=2,
        tensor_parallel_size=1,
    )

    logging_level = logging.DEBUG
    logger.setLevel(logging_level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging_level)
    logger.addHandler(handler)

    set_verbosity(logging.DEBUG)

    p2p = P2P(pg=dpg.world_pg, device=torch.device("cuda"))

    async_operation_bypasses_deadlock(dpg=dpg, p2p=p2p)
    print("potato")
    torch_dist.barrier()
    deadlock_experiment(dpg=dpg, p2p=p2p)


if __name__ == "__main__":
    main()
