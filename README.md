# Fetal Head Circumference Measurement on HC18

This repository is a PyTorch project for automatic fetal head circumference
estimation from 2D ultrasound images using the HC18 dataset.

The v1 pipeline is segmentation-first:

```text
HC18 image
  -> ellipse-derived training mask
  -> U-Net / Attention U-Net segmentation
  -> predicted mask cleanup
  -> ellipse fitting
  -> head circumference in millimeters
  -> metrics, figures, and report tables
```

The project is built for a course final submission. The final deliverable will
use `Myproject.sh` as the executable runner, not `Myproject.ipynb`.

## Goals

- Train a non-trivial deep neural network for fetal head segmentation.
- Convert predicted masks into ellipse-based head circumference measurements.
- Evaluate both segmentation quality and HC measurement error.
- Produce report-ready tables, curves, and qualitative overlays.
- Keep the workflow reproducible locally and on university CHPC.

## Expected Repository Structure

```text
.
├── AGENTS.md
├── DECISIONS.md
├── README.md
├── Myproject.sh
├── configs/
├── data/
│   ├── raw/
│   │   └── HC18/
│   ├── processed/
│   └── splits/
├── docs/
│   ├── architecture.md
│   └── project-spec.md
├── handoff.md
├── outputs/
│   └── runs/
├── project-tasks.md
├── report/
├── scripts/
├── slurm/
├── src/
│   ├── data/
│   ├── evaluation/
│   ├── inference/
│   ├── models/
│   ├── training/
│   └── utils/
└── tests/
```

Some directories are created in later implementation tasks.

## Dataset

Download the HC18 dataset from the official challenge source and place it under:

```text
data/raw/HC18/
```

Raw data should not be committed to git. The code should treat `data/raw/` as
read-only and write generated masks, split files, and derived artifacts under
`data/processed/`, `data/splits/`, and `outputs/`.

Expected HC18 files include training images, annotation/pixel-size CSV files,
and the official test images. The exact local layout will be documented after
the dataset inspection task.

## Local Development Setup

Create and activate the project environment with `uv`:

```bash
UV_CACHE_DIR=.uv-cache uv venv .venv
source .venv/bin/activate
UV_CACHE_DIR=.uv-cache uv pip install -r requirements.txt
```

On Apple Silicon, install PyTorch using the official command appropriate for
your environment if the default requirements file is not sufficient.

## Local Smoke Runs

Local runs are intended for development and correctness checks, not final
reported training.

Planned commands:

```bash
.venv/bin/python -m src.data.make_splits --config configs/data.yaml
.venv/bin/python scripts/visualize_samples.py --config configs/data.yaml --n 10
.venv/bin/python scripts/run_smoke_train.py --config configs/unet_smoke.yaml
.venv/bin/python -m src.inference.predict --config outputs/runs/unet_baseline_smoke/config.json --checkpoint outputs/runs/unet_baseline_smoke/best_model.pt --split val --limit 2
.venv/bin/python -m src.evaluation.evaluate --config outputs/runs/unet_baseline_smoke/config.json --checkpoint outputs/runs/unet_baseline_smoke/best_model.pt --split val --limit 2
.venv/bin/python scripts/make_report_figures.py --run-id unet_baseline_smoke --split val
```

The data commands are implemented. They require HC18 files under
`data/raw/HC18/`; without the dataset, they exit with an actionable message.

## CHPC Workflow

Use university CHPC GPU nodes for long training runs and final ablations.

Planned workflow:

```bash
# From local machine
rsync -av --exclude data/raw --exclude outputs ./ <uNID>@<chpc-login>:/scratch/general/vast/<uNID>/fetal-hc/

# On CHPC
cd /scratch/general/vast/<uNID>/fetal-hc
UV_CACHE_DIR=.uv-cache uv venv .venv
source .venv/bin/activate
UV_CACHE_DIR=.uv-cache uv pip install -r requirements.txt
sbatch slurm/train_unet.sbatch
sbatch slurm/train_attention_unet.sbatch

# After runs complete, from local machine
rsync -av <uNID>@<chpc-login>:/scratch/general/vast/<uNID>/fetal-hc/outputs/runs/ outputs/runs/
```

Replace `<uNID>` and `<chpc-login>` with the correct university account and
cluster login host. The U-Net Slurm script is `slurm/train_unet.sbatch`.

## Planned Models

- U-Net baseline
- Attention U-Net improved model
- ResUNet only as fallback or stretch

All models must share the same contract:

```text
input:  [B, 1, H, W]
output: [B, 1, H, W] logits
```

## Planned Metrics

Segmentation:

- Dice
- IoU
- HD95 or Hausdorff distance

Measurement:

- signed HC error in mm
- absolute HC error in mm
- MAE
- RMSE

## Project Governance

Future Codex sessions must follow:

- `AGENTS.md` for operating rules,
- `project-tasks.md` for the approved task queue,
- `handoff.md` for current context,
- `DECISIONS.md` for durable project decisions.

Agents should work one task at a time and update the handoff after meaningful
work.

## Course Deliverable

The final submission should include:

- project report PDF, maximum 6 pages;
- code zip;
- `Myproject.sh` executable runner;
- saved configs, metrics, figures, and tables needed to reproduce the report.
