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
- Complete v1 locally with clearly documented reduced-resource settings, then
  optionally rerun larger configs on CHPC.

## V2 Portfolio Demo

The v2 demo is a Vite + React + TypeScript pipeline explorer that turns the v1
saved outputs into an interactive visual walkthrough:

```text
ultrasound -> target mask -> CNN probability -> thresholded mask -> ellipse fit -> HC measurement
```

Educational demo only. Not for clinical use.

What the demo shows:

- curated saved-output cases with successes, typical behavior, and failures,
- stage-by-stage mask/probability/ellipse visualization,
- a live threshold slider driven by exported `prob.png` probability maps,
- contour-vs-ellipse HC comparison,
- selected-case Dice, IoU, HD95, and HC error,
- real local v1 experiment cards, sparklines, and ablation summaries.

### Public Preview And Real Local Mode

The repository does not commit or deploy the generated HC18 sample image bundle.
If `frontend/public/samples/manifest.json` is absent, the app automatically loads
a committed non-medical placeholder preview from `frontend/public/demo-samples/`.
That keeps the public site safe to host while preserving the full UI.

To view the public-safe preview locally:

```bash
cd frontend
npm install
npm run dev
```

To view the real saved-output demo locally after exporting the curated HC18
artifacts:

```bash
./start_demo.sh
```

`start_demo.sh` uses `outputs/demo_samples/` when present. If that bundle is
missing, it runs:

```bash
.venv/bin/python scripts/export_demo_artifacts.py --run-id attention_unet_local_baseline --split test
```

Then it copies the generated bundle into ignored `frontend/public/samples/` and
starts Vite at `http://localhost:5173`.

### Deployment

Vercel configuration is included in `vercel.json`.
Public URL: `https://fetal-head-measurement.vercel.app/`

Recommended Vercel settings:

```text
Framework preset: Other
Install command: npm --prefix frontend install
Build command: npm --prefix frontend run build
Output directory: frontend/dist
```

Until a public artifact policy is approved, deploy the placeholder preview only.
The real HC18 sample bundle should remain local or be distributed separately
after explicit approval.

## Expected Repository Structure

```text
.
├── AGENTS.md
├── README.md
├── Myproject.sh
├── configs/
├── data/
│   ├── raw/
│   │   └── HC18/
│   ├── processed/
│   └── splits/
├── docs/
│   ├── v1/
│   │   ├── AGENTS.md
│   │   ├── DECISIONS.md
│   │   ├── architecture.md
│   │   ├── dataset-format.md
│   │   ├── project-spec.md
│   │   ├── splits-runs-and-outputs.md
│   │   └── submission-packaging.md
│   └── v2_demo/
├── handoff.md
├── frontend/
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

Expected HC18 files include:

```text
data/raw/HC18/
├── training_set/
├── test_set/
├── training_set_pixel_size_and_HC.csv
└── test_set_pixel_size.csv
```

The local v1 report uses the labeled `training_set/` split into train,
validation, and internal-test partitions. The internal `test.csv` split is not
the official unlabeled HC18 challenge test set.

## Local Development Setup

Create and activate the project environment with `uv`:

```bash
UV_CACHE_DIR=.uv-cache uv venv .venv
source .venv/bin/activate
UV_CACHE_DIR=.uv-cache uv pip install -r requirements.txt
```

On Apple Silicon, install PyTorch using the official command appropriate for
your environment if the default requirements file is not sufficient.

## Course Runner

The course runner is:

```bash
bash Myproject.sh
```

By default, this runs in `report-only` mode. It expects saved local run
artifacts under `outputs/runs/`, regenerates comparison tables/figures, and runs
the test suite. This is the fastest way to verify the submitted local v1
results.

To retrain and regenerate the full local v1 experiment set:

```bash
bash Myproject.sh --full-local
```

`--full-local` regenerates splits, trains U-Net, trains Attention U-Net, runs
the Dice-loss and augmentation ablations, evaluates val/internal-test splits,
and rebuilds report artifacts. This can take a while on the MacBook.

To skip tests during a local rerun:

```bash
bash Myproject.sh --full-local --skip-tests
```

## Local V1 Results

The local v1 report uses reduced-resource settings that should be disclosed in
the PDF report:

```text
split id: seed42_train698_val152_test149
train/val/internal-test: 698 / 152 / 149 labeled images
image size: 256x384
base channels: 16
epochs: 10
compute: MacBook MPS
```

Best local internal-test result:

```text
model: Attention U-Net + BCE/Dice
run id: attention_unet_local_baseline
Dice: 0.9669
IoU: 0.9373
HD95: 2.38 mm
HC MAE: 3.37 mm
HC RMSE: 4.68 mm
```

Report-ready artifacts are generated under:

```text
report/report-results-summary.md
report/final-report-outline.md
report/assets-index.md
report/submission-checklist.md
report/tables/
report/figures/
```

## Local Smoke Runs

Smoke runs are intended for development and correctness checks, not reported
training.

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

## Local Experiment Commands

The local v1 experiment configs are:

```text
configs/unet_local_baseline.yaml
configs/attention_unet.yaml
configs/attention_unet_dice_loss.yaml
configs/attention_unet_aug.yaml
```

Train one run:

```bash
.venv/bin/python -m src.training.train --config configs/attention_unet.yaml
```

Evaluate one run:

```bash
.venv/bin/python -m src.evaluation.evaluate \
  --config outputs/runs/attention_unet_local_baseline/config.json \
  --checkpoint outputs/runs/attention_unet_local_baseline/best_model.pt \
  --split test
```

Regenerate comparison/report artifacts:

```bash
.venv/bin/python scripts/compare_runs.py \
  --runs unet_local_baseline attention_unet_local_baseline attention_unet_dice_loss attention_unet_aug \
  --splits val test \
  --output outputs/tables/local_ablation_summary.csv

.venv/bin/python scripts/postprocess_ablation.py \
  --run-id attention_unet_local_baseline \
  --split test

.venv/bin/python scripts/build_report_artifacts.py
```

## CHPC Workflow

Use university CHPC GPU nodes for post-v1 full-scale reruns and stronger
ablations. CHPC is not a blocker for the local v1 course report.

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

# After runs complete, from local machine
rsync -av <uNID>@<chpc-login>:/scratch/general/vast/<uNID>/fetal-hc/outputs/runs/ outputs/runs/
```

Replace `<uNID>` and `<chpc-login>` with the correct university account and
cluster login host. The current U-Net Slurm script is
`slurm/train_unet.sbatch`; Attention U-Net and evaluation Slurm scripts are
post-v1 workflow polish.

## Models

- U-Net baseline
- Attention U-Net improved model
- ResUNet only as fallback or stretch

All models must share the same contract:

```text
input:  [B, 1, H, W]
output: [B, 1, H, W] logits
```

## Metrics

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

- `AGENTS.md` for current v2 operating rules,
- `project-tasks.md` for the approved task queue,
- `handoff.md` for current context,
- `docs/v1/DECISIONS.md` for archived v1 decisions,
- `docs/v2_demo/DECISIONS.md` for v2 demo decisions.

Agents should work one task at a time and update the handoff after meaningful
work.

## Course Deliverable

The final submission should include:

- project report PDF, maximum 6 pages;
- code zip;
- `Myproject.sh` executable runner;
- saved configs, metrics, figures, and tables needed to reproduce the report.

The v1 submission uses `Myproject.sh`, not `Myproject.ipynb`.

Use `report/submission-checklist.md` before packaging the final ZIP.
See `docs/v1/submission-packaging.md` for detailed ZIP contents and example
packaging commands.
