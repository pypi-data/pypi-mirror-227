from deepspeed.runtime.pipe.schedule import BackwardPass, ForwardPass, TrainSchedule


def main():
    # Hyperparameters from https://arxiv.org/abs/2104.04473
    micro_batches = 8
    stage_ids = [0, 1, 2, 3]
    stages = len(stage_ids)

    for i, stage_id in enumerate(stage_ids):
        train_schedule = TrainSchedule(micro_batches=micro_batches, stage_id=stage_id, stages=stages)
        print(f"Rank {stage_id}/{stages}: {list(train_schedule.steps())}")

    print("")
    print("Print only fwd/bwd")

    def get_forward_or_backward(step):
        is_forward = False
        is_backward = False
        for elt in step:
            is_forward |= isinstance(elt, ForwardPass)
            is_backward |= isinstance(elt, BackwardPass)
        assert (is_forward and is_backward) is False, "Can't be both forward and backward"
        if is_forward:
            return ForwardPass(buffer_id=0)  # dummy forward
        if is_backward:
            return BackwardPass(buffer_id=0)
        return None

    # Deepspeed 1f1b is slightly different to the one from the original paper.
    for i, stage_id in enumerate(stage_ids):
        train_schedule = TrainSchedule(micro_batches=micro_batches, stage_id=stage_id, stages=stages)
        forward_backward_of_none = [get_forward_or_backward(step) for step in train_schedule.steps()]
        print(f"Rank {stage_id}/{stages}: {[elt for elt in forward_backward_of_none if elt is not None]}")


if __name__ == "__main__":
    main()
