# Course Submission Packaging Guide

This guide explains what to submit for the course and how to package it without
mixing up GitHub, raw data, checkpoints, and report artifacts.

## Required Deliverables

The course submission should contain:

1. A final project report PDF, maximum 6 pages.
2. A code ZIP containing the project code.
3. An executable script named `Myproject.sh`.

This project uses `Myproject.sh`, not `Myproject.ipynb`.

## What The Report PDF Should Contain

Use `report/final-report-outline.md` as the starting point.

Required report sections:

- Introduction: why fetal head circumference measurement matters and why the
  problem is challenging.
- Method: U-Net, Attention U-Net, BCE+Dice, Dice-only ablation, augmentation
  ablation, and ellipse-based HC measurement.
- Experiments: HC18 split, local reduced-resource setup, metrics, main results,
  loss/augmentation ablations, and post-processing ablation.
- Conclusions: what worked, what did not, and future CHPC/full-scale runs.

The report must explicitly disclose the local reduced-resource setup:

```text
split id: seed42_train698_val152_test149
train/val/internal-test counts: 698 / 152 / 149
image size: 256x384
base channels: 16
epochs: 10
compute: MacBook MPS
```

The main reported internal-test result should match:

```text
run id: attention_unet_local_baseline
model: Attention U-Net + BCE/Dice
Dice: 0.9669
IoU: 0.9373
HD95: 2.38 mm
HC MAE: 3.37 mm
HC RMSE: 4.68 mm
```

## Report Assets To Use

Core summary:

```text
report/report-results-summary.md
report/final-report-outline.md
```

Tables:

```text
report/tables/main_test_results.csv
report/tables/main_test_results.md
report/tables/attention_unet_ablation_test_results.csv
report/tables/attention_unet_ablation_test_results.md
report/tables/postprocess_test_results.csv
report/tables/postprocess_test_results.md
```

Figures:

```text
report/figures/main_test_hc_mae.png
report/figures/main_test_dice.png
report/figures/postprocess_test_hc_mae.png
```

Optional qualitative figure:

```text
outputs/figures/attention_unet_local_baseline/test_qualitative_failures.png
```

## What To Include In The Code ZIP

Always include:

```text
AGENTS.md
Myproject.sh
README.md
requirements.txt
configs/
data/splits/
docs/
handoff.md
project-tasks.md
report/
scripts/
src/
tests/
```

Include these saved artifacts if the grader should be able to run fast
verification with `bash Myproject.sh`:

```text
outputs/runs/unet_local_baseline/config.json
outputs/runs/unet_local_baseline/evaluation/
outputs/runs/attention_unet_local_baseline/config.json
outputs/runs/attention_unet_local_baseline/evaluation/
outputs/runs/attention_unet_local_baseline/predictions/
outputs/runs/attention_unet_dice_loss/config.json
outputs/runs/attention_unet_dice_loss/evaluation/
outputs/runs/attention_unet_aug/config.json
outputs/runs/attention_unet_aug/evaluation/
outputs/tables/
```

Checkpoints are optional for the ZIP:

```text
outputs/runs/*/best_model.pt
```

Default `bash Myproject.sh` does not require checkpoints. It uses saved configs,
evaluation files, and prediction artifacts. Include checkpoints only if the ZIP
size is acceptable and you want future inference from checkpoints without
retraining.

## What Not To Include

Do not include unless explicitly allowed by course policy:

```text
data/raw/HC18/
```

Also exclude local environment/cache files:

```text
.venv/
.uv-cache/
.cache/
.matplotlib_cache/
__pycache__/
.pytest_cache/
.DS_Store
```

## Suggested ZIP Commands

Create a lean code ZIP without raw data, virtualenv, or checkpoints:

```bash
zip -r Fetal-Head-Measurement-code.zip \
  AGENTS.md Myproject.sh README.md requirements.txt \
  configs data/splits docs handoff.md project-tasks.md report scripts src tests \
  outputs/runs outputs/tables \
  -x "data/raw/*" ".venv/*" ".uv-cache/*" ".cache/*" ".matplotlib_cache/*" \
     "__pycache__/*" "*/__pycache__/*" ".pytest_cache/*" "*.pt" "*.pth" "*.ckpt"
```

Create a ZIP that includes checkpoints too:

```bash
zip -r Fetal-Head-Measurement-code-with-checkpoints.zip \
  AGENTS.md Myproject.sh README.md requirements.txt \
  configs data/splits docs handoff.md project-tasks.md report scripts src tests \
  outputs/runs outputs/tables \
  -x "data/raw/*" ".venv/*" ".uv-cache/*" ".cache/*" ".matplotlib_cache/*" \
     "__pycache__/*" "*/__pycache__/*" ".pytest_cache/*"
```

If the ZIP becomes too large, prefer excluding checkpoints and keeping the
report-only artifacts listed above.

## Verification Before Upload

From the project root:

```bash
bash Myproject.sh
```

Expected result:

```text
Report artifacts regenerated
Full test suite: 21 passed
```

For a full local rerun from raw data:

```bash
bash Myproject.sh --full-local
```

This retrains all local v1 runs and can take substantially longer.

## GitHub Versus Course ZIP

The GitHub repo can stay lean and omit large generated outputs. The course ZIP
can include saved `outputs/runs/` and `outputs/tables/` artifacts so
`bash Myproject.sh` works quickly in report-only mode.

If a grader clones only GitHub without outputs, they can still reproduce results
with:

```bash
bash Myproject.sh --full-local
```

as long as HC18 is placed under `data/raw/HC18/`.
