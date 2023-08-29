import subprocess
from pathlib import Path
from typing import Optional

from upath import UPath

from brrr.core import distributed as dist
from brrr.core import logging
from brrr.core.logging import log_rank
from brrr.core.process_groups_initializer import DistributedProcessGroups

logger = logging.get_logger(__name__)


def upload_checkpoint(
    checkpoint_path: Path,
    upload_s3_path: UPath,
    upload_s3_num_workers: int,
    group: DistributedProcessGroups,
    previous_upload_process: Optional[subprocess.Popen] = None,
):
    """Upload checkpoint to S3 bucket"""
    upload_script_path = Path(__file__).parent / "s3_upload_checkpoints.py"
    upload_log_path = checkpoint_path / "upload_script.log"

    if dist.get_rank(group) == 0:
        if previous_upload_process is None:
            # if script not launched yet
            log_rank(
                f"[Upload checkpoint] Uploading checkpoint to S3. Please check {upload_log_path} for more details.",
                logger=logger,
                level=logging.INFO,
                rank=0,
            )
            # python examples/gpt2_mqa/s3_upload_checkpoints.py --checkpoints-path brrr-starcoder-5b-v1/checkpoints/ --upload-s3-path s3://huggingface-brrr/brrr-checkpoint/ --num-workers 48
            previous_upload_process = subprocess.Popen(
                f"python {upload_script_path} --checkpoints-path {str(checkpoint_path)} --upload-s3-path {str(upload_s3_path)} --num-workers {upload_s3_num_workers}".split(),
                stdout=open(upload_log_path, "a"),
                stderr=subprocess.STDOUT,
            )
        elif previous_upload_process.poll() is not None:
            # if script finished
            if previous_upload_process.returncode != 0:
                log_rank(
                    f"[Upload checkpoint] Checkpoint upload failed with error code {previous_upload_process.returncode}. Please check {upload_log_path} for more details.",
                    logger=logger,
                    level=logging.WARNING,
                    rank=0,
                    group=group,
                )
            else:
                log_rank(
                    f"[Upload checkpoint] Checkpoint(s) uploaded to S3. Please check {upload_log_path} for more details.",
                    logger=logger,
                    level=logging.INFO,
                    rank=0,
                )
            previous_upload_process = None
        else:
            # if script still running
            log_rank(
                f"[Upload checkpoint] Script still running. Please check {upload_log_path} for more details. Resuming training...",
                logger=logger,
                level=logging.INFO,
                rank=0,
            )
    return previous_upload_process
