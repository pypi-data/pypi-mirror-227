"""Benchmark uploading a file to S3"""

import logging
import os
import time

import boto3
from botocore.exceptions import ClientError


def dump_dummy_checkpoint(filepath, single_file=True):
    """Dump a dummy 10GB checkpoint file

    :param filepath: File to dump to
    :return: True if file was dumped, else False
    """
    if single_file:
        with open(filepath, "wb") as f:
            f.write(os.urandom(10 * 1024 * 1024 * 1024))
    else:
        # Dump 20 500MB files
        for i in range(20):
            with open(filepath + f"_{i}", "wb") as f:
                f.write(os.urandom(500 * 1024 * 1024))
    return True


def upload_file_boto3(bucket_name, s3_path, file_name):
    """Upload a file to an S3 bucket using Boto3

    :param bucket_name: Bucket to upload to
    :param file_name: File to upload
    :return: True if file was uploaded, else False
    """
    # Upload the file
    s3_client = boto3.client("s3")
    try:
        s3_client.upload_file(file_name, bucket_name, s3_path)
    except ClientError as e:
        logging.error(e)
        return False
    return True


# "s5cmd sync {checkpoint_dir}/ s3://{bucket_name}/{bucket_path}/"
def upload_file_s5cmd(bucket_name, s3_path, file_name):
    """Upload a file to an S3 bucket using s5cmd

    :param bucket_name: Bucket to upload to
    :param file_name: File to upload
    :return: True if file was uploaded, else False
    """
    # Upload the file
    try:
        os.system(f"s5cmd sync {file_name} s3://{bucket_name}/{s3_path}")
    except ClientError as e:
        logging.error(e)
        return False
    return True


if __name__ == "__main__":
    # Benchmark dumping a dummy 10GB checkpoint

    local_rank = int(os.getenv("LOCAL_RANK", 0))
    world_rank = int(os.getenv("RANK", 0))

    for checkpoint_path in [
        f"/fsx/nouamane/projects/brrr/benchmarks/s3/dummy_checkpoint_{local_rank}_{world_rank}.pt",
        # f"/scratch/nouamane/checkpoints/dummy_checkpoint_{local_rank}_{world_rank}.pt"
    ]:
        # SINGLE FILE
        os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)
        print("Dumping dummy 10GB checkpoint to", checkpoint_path)
        start_time = time.time()
        dump_dummy_checkpoint(checkpoint_path, single_file=True)
        print(f"Dumped dummy checkpoint in {time.time() - start_time} seconds\n")

        # if world_rank == 0:
        #     os.system(f"rm -rf /fsx/nouamane/projects/brrr/benchmarks/s3/dummy_checkpoint_*.pt")
        #     os.system(f"rm -rf /scratch/nouamane/checkpoints/dummy_checkpoint_*.pt*")

        # MULTIPLE FILES
        # print("*" * 80)
        # print("Dumping 20 dummy 500MB checkpoints to", checkpoint_path)
        # start_time = time.time()
        # dump_dummy_checkpoint(checkpoint_path, single_file=False)
        # print(f"Dumped 20 dummy checkpoints in {time.time() - start_time} seconds\n")

        # if world_rank == 0:
        #     os.system(f"rm -rf /fsx/nouamane/projects/brrr/benchmarks/s3/dummy_checkpoint_*.pt*")
        #     os.system(f"rm -rf /scratch/nouamane/checkpoints/dummy_checkpoint_*.pt*")

        # # Benchmark uploading from local to S3
        # print("*" * 80)
        # bucket_name = "huggingface-brrr"
        # s3_path = f"nouamane/dummy_checkpoint_{local_rank}_{world_rank}.pt"
        # # checkpoint_path = "/fsx/nouamane/projects/brrr/benchmarks/s3/a.txt"
        # # remove old checkpoint from s3
        # print(f"Removing old checkpoint from S3: {bucket_name}/{s3_path}")
        # os.system(f"s5cmd rm s3://{bucket_name}/{s3_path}")
        # print(f"Uploading dummy 10GB checkpoint from {checkpoint_path}\nto s3://{bucket_name}/{s3_path}")
        # start_time = time.time()
        # # upload_file_boto3(bucket_name, s3_path, checkpoint_path)
        # upload_file_s5cmd(bucket_name, s3_path, checkpoint_path)
        # print(f"Uploaded dummy checkpoint in {time.time() - start_time} seconds")
        # print("*" * 80)
        # print("\n\n")
