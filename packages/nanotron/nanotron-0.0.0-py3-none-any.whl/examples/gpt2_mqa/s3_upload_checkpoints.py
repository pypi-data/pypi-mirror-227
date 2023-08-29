#!/usr/bin/env python

#
# This tool uploads any new checkpoints found at given path to s3
#
# Example:
#
# python examples/gpt2_mqa/s3_upload_checkpoints.py --checkpoints-path brrr-starcoder-5b-v1/checkpoints/ --upload-s3-path s3://huggingface-brrr/brrr-checkpoint/
#
# It requires `s5cmd` to be installed and configured with your s3 credentials. https://github.com/peak/s5cmd#installation
#

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

from upath import UPath

# we have to deal with potentially overlapping slurm jobs running on different nodes, so we can't
# rely on PIDs of a running process. Will use a control file instead as the filesystem is shared.
#
# If that file is there it means:
#
# 1. either the upload is still running
# 2. the upload got aborted (e.g. cpu-oom)
#
control_file_name = "started-upload-checkpoint"
finished_uploading_file_name = "finished-upload-checkpoint"


def run_cmd(cmd, check=True):
    try:
        response = subprocess.run(
            cmd,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            check=check,
            encoding="utf-8",
        ).stdout.strip()
    except subprocess.CalledProcessError as exc:
        raise EnvironmentError(exc.stderr)

    return response


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoints-path", type=Path, help="base dir with checkpoints")
    parser.add_argument(
        "--upload-s3-path",
        type=UPath,
        help="s3 path to upload checkpoints to (e.g. s3://huggingface-brrr/brrr-checkpoint/)",
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="force uploading of all checkpoint even if alrdy uploaded/uploading"
    )
    parser.add_argument("--rm-after-upload", action="store_true", help="remove checkpoints after uploading")

    # s5cmd options
    parser.add_argument(
        "--num-workers",
        type=int,
        default=48,
        help="[s5cmd] number of workers execute operation on each object (default: 48)",
    )

    return parser.parse_args()


def exit(msg):
    print(msg)
    sys.exit()


def should_process(path: Path, force: bool, control_file_path: Path, finished_uploading_file_path: Path) -> bool:
    """Heuristics to decide whether to upload this checkpoint or not"""

    # check if checkpoint is fully saved
    finished_saving_path = path / "finished-save-checkpoint"
    if not finished_saving_path.exists():
        print(f"[N] {path} isn't finished saving. Skipping")
        return False

    if force:
        print(f"[Y] Forced to re-process {path}")
        return True

    # check if already uploaded
    if finished_uploading_file_path.exists():
        print(f"[N] {path} has already been uploaded. Skipping")
        return False

    # complicated checks - has another job already started uploading? or did it crash?
    if control_file_path.exists():
        print(
            f"[N] {path} either another job is uploading it or it crashed doing so. Needs manual intervention. Skipping"
        )
        return False

    print(f"[Y] {path} is a new checkpoint. Uploading")
    return True


def main():
    print("\n\n", "*" * 80)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    args = get_args()

    checkpoints_path = args.checkpoints_path
    upload_s3_path = args.upload_s3_path
    if not (checkpoints_path.exists() and checkpoints_path.is_dir()):
        raise FileNotFoundError(f"can't find a directory '{checkpoints_path}'")

    # list all dirs under checkpoints_path that are numbers in name
    checkpoint_dirs = [d for d in checkpoints_path.iterdir() if d.is_dir() and d.name.isdigit()]
    checkpoint_dirs.sort(key=lambda x: int(x.name))

    if len(checkpoint_dirs) == 0:
        exit("No checkpoints found, exiting")

    # Check each folder in real time to allow for overlapping jobs starting at different times
    for checkpoint_dir in checkpoint_dirs:
        print(f"*** Checking {checkpoint_dir}")

        control_file_path = checkpoint_dir / control_file_name
        finished_uploading_file_path = checkpoint_dir / finished_uploading_file_name

        if not should_process(checkpoint_dir, args.force, control_file_path, finished_uploading_file_path):
            continue

        print(f"Launching upload for {checkpoint_dir} - it could take a long time")
        cmd = f"s5cmd sync --numworkers {args.num_workers} {checkpoint_dir}/ {upload_s3_path}/{checkpoint_dir.name}/".split()
        print(" ".join(cmd))
        # TODO @nouamane: we could use flock here, to avoid a race condition, but it'd be pointless since each
        # cronjob is likely to run on a different node and flock only works within a single node
        control_file_path.touch()
        # print(f"mock running {cmd}")
        response = run_cmd(cmd)
        print(f"Uploaded {checkpoint_dir}:")
        print(response)

        # for now disable this as large files don't have sha256 checksums
        # result = integrity_check_recursive(checkpoint_dir, bucket_name, bucket_path)
        # print(f"Integrity check was {result}")

        control_file_path.unlink()
        finished_uploading_file_path.touch()

        # Remove folder after upload
        if args.rm_after_upload:
            print(f"Removing {checkpoint_dir}")
            shutil.rmtree(checkpoint_dir)


if __name__ == "__main__":
    main()
