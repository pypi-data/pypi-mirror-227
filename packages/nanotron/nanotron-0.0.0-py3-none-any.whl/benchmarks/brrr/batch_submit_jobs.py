# Description: Batch submit jobs for experiments
# Usage: python batch_submit_jobs.py
import math
import os
from dataclasses import asdict, dataclass
from itertools import product
from typing import Dict

import dacite
import yaml
from jinja2 import Template


@dataclass
class UserConfig:
    log_parent_dir: str
    brrr_repo: str
    conda_env: str


@dataclass
class RunConfig:
    run_name: str
    config_model_kwargs: Dict[str, str]
    script_repo: str
    exc_file: str


@dataclass
class SweepConfig(RunConfig):
    job_name: str
    dp: int
    pp: int
    tp: int
    seq_len: int
    mbs: int


@dataclass
class SlurmConfig(UserConfig, SweepConfig):
    log_dir: str
    n_nodes: int
    config_file: str
    n_gpus_per_node: int
    ckpt_folder_name: str


def submit_job(slurm_job_script_path: str) -> None:
    os.system(f"sbatch {slurm_job_script_path}")


def make_config(template: str, template_out: str, sweep_config: SweepConfig) -> None:
    with open(template, "rt") as f:
        py_template = Template(f.read(), trim_blocks=True, lstrip_blocks=True)
        py_code = py_template.render(**asdict(sweep_config))
        with open(template_out, "wt") as out:
            out.write(py_code)


def make_slurm_job(template: str, template_out: str, slurm_config: SlurmConfig):
    with open(template, "rt") as f:
        py_template = Template(f.read(), trim_blocks=True, lstrip_blocks=True)
        py_code = py_template.render(**asdict(slurm_config))
        with open(template_out, "wt") as out:
            out.write(py_code)


def run_experiment(
    config_template: str,
    slurm_template: str,
    slurm_template_out: str,
    sweep_config: SweepConfig,
    slurm_config: SlurmConfig,
):
    print(f"Created config file {slurm_config.config_file}")
    make_config(template=config_template, template_out=slurm_config.config_file, sweep_config=sweep_config)
    print(f"Created slurm job file {slurm_template_out}")
    make_slurm_job(template=slurm_template, template_out=slurm_template_out, slurm_config=slurm_config)
    print(f"Submit job {sweep_config.job_name} with {sweep_config.dp} dp, {sweep_config.pp} pp, {sweep_config.tp} tp")
    submit_job(slurm_template_out)


def main():
    dir_name = os.path.dirname(__file__)

    config_yaml_file = os.path.join(dir_name, "hyperparam.yaml")

    with open(config_yaml_file, "rt") as f:
        config_yaml = yaml.safe_load(f)

    user_config = dacite.from_dict(
        data_class=UserConfig,
        data=config_yaml["user_config"],
        config=dacite.Config(strict=True),
    )

    for run in config_yaml["runs"]:
        run_config = dacite.from_dict(
            data_class=RunConfig,
            data=run["run_config"],
            config=dacite.Config(strict=True),
        )
        for dp, (pp, tp), (seq_len, mbs) in product(*run["sweeps"].values()):
            config_str = f"dp_{dp}_pp_{pp}_tp_{tp}_seq_len_{seq_len}_mbs_{mbs}"
            sweep_config = SweepConfig(
                **asdict(run_config),
                job_name=f"{run_config.run_name}_{config_str}",
                dp=dp,
                pp=pp,
                tp=tp,
                seq_len=seq_len,
                mbs=mbs,
            )
            slurm_config = SlurmConfig(
                **asdict(user_config),
                **asdict(sweep_config),
                log_dir=os.path.join(user_config.log_parent_dir, run_config.run_name),
                n_nodes=math.ceil(sweep_config.dp * sweep_config.pp * sweep_config.tp / 8),
                config_file=os.path.join(dir_name, f"config_{run_config.run_name}_{config_str}.yaml"),
                n_gpus_per_node=min(8, sweep_config.dp * sweep_config.pp * sweep_config.tp),
                ckpt_folder_name=f"ckpt_{run_config.run_name}_{config_str}",
            )
            # Create log_dir if not exists
            os.makedirs(slurm_config.log_dir, exist_ok=True)
            run_experiment(
                config_template=os.path.join(dir_name, "config.yaml.jinja"),
                slurm_template=os.path.join(dir_name, "train.slurm.jinja"),
                slurm_template_out=os.path.join(dir_name, f"train_{run_config.run_name}_{config_str}.slurm"),
                sweep_config=sweep_config,
                slurm_config=slurm_config,
            )


if __name__ == "__main__":
    main()
