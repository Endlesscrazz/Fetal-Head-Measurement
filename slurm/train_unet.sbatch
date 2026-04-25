#!/usr/bin/env bash
#SBATCH --job-name=fetal-hc-unet
#SBATCH --output=outputs/runs/slurm-%j-unet.out
#SBATCH --error=outputs/runs/slurm-%j-unet.err
#SBATCH --time=04:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --gres=gpu:1

set -euo pipefail

cd "${SLURM_SUBMIT_DIR}"

source .venv/bin/activate
.venv/bin/python -m src.training.train --config configs/unet_baseline.yaml
