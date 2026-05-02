# Splits, Runs, and Outputs

This document explains how HC18 data is split, how run artifacts are organized,
and how configs control experiments.

## Data Split Policy

Raw HC18 data is expected under:

```text
data/raw/HC18/
  training_set/
  test_set/
  training_set_pixel_size_and_HC.csv
  test_set_pixel_size.csv
```

For supervised training and evaluation, v1 uses the labeled HC18
`training_set/`. The official HC18 `test_set/` does not include local ground
truth labels in the same way, so it is reserved for unlabeled inference unless a
future task adds an official submission workflow.

The reusable split files live under:

```text
data/splits/
  train.csv
  val.csv
  test.csv
  summary.csv
```

Current split id:

```text
seed42_train698_val152_test149
```

Current counts:

```text
train: 698 images
val:   152 images
test:  149 images
total: 999 labeled training images
```

The `test.csv` file is an internal held-out test split from the labeled
`training_set/`. It is not the official HC18 challenge `test_set/`.

## Leakage Controls

Splits are created by `src/data/make_splits.py`.

The split script:

1. discovers records from the configured dataset subset,
2. groups images by exam prefix using the part of the sample id before the first
   underscore,
3. shuffles groups with a fixed seed,
4. writes separate `train.csv`, `val.csv`, and `test.csv` files.

The grouped split matters because files such as repeated acquisitions from the
same exam should not be scattered across train and validation/test splits.

The baseline split audit showed:

```text
filename overlaps:
train-val:  0
train-test: 0
val-test:   0

group_id overlaps:
train-val:  0
train-test: 0
val-test:   0
```

When comparing models, do not regenerate `data/splits/` unless the experiment
is explicitly labeled as a new split. U-Net, Attention U-Net, and ablations
should use the same split id for fair comparison.

## Which Split Is Used Where

Training uses:

```text
data/splits/train.csv
```

Validation during training uses:

```text
data/splits/val.csv
```

The best checkpoint is selected using validation Dice only.

After training, evaluation can be run on either:

```text
data/splits/val.csv
data/splits/test.csv
```

Use `val` to understand the split used for model selection. Use the internal
`test` split for a less biased held-out estimate after model selection.

## Why Runs Have `predictions/` and `evaluation/`

Each run lives under:

```text
outputs/runs/<run_id>/
```

For example:

```text
outputs/runs/unet_local_baseline/
```

Inside a run, `predictions/` and `evaluation/` are separate because they answer
different questions.

`predictions/` contains model outputs and geometry artifacts:

```text
outputs/runs/<run_id>/predictions/<split>/
  predictions.csv
  predictions.json
  masks/
    <sample_id>_raw.png
    <sample_id>_cleaned.png
  overlays/
    <sample_id>_overlay.png
```

These files answer:

- What mask did the model predict?
- Did ellipse fitting succeed?
- What HC in mm did the model estimate?
- What does the prediction look like overlaid on the ultrasound image?

`evaluation/` contains metric summaries computed from predictions and ground
truth:

```text
outputs/runs/<run_id>/evaluation/<split>/
  per_sample_metrics.csv
  aggregate_metrics.csv
```

These files answer:

- What was Dice/IoU/HD95 for each sample?
- What was HC error for each sample?
- What are the aggregate report numbers for the split?

The evaluation script calls inference first, so running evaluation creates or
refreshes matching files in both `predictions/<split>/` and
`evaluation/<split>/`.

## Why `val/` and `test/` Exist Under Both Folders

The subfolder name is the evaluated split.

For the local U-Net baseline:

```text
outputs/runs/unet_local_baseline/predictions/val/
outputs/runs/unet_local_baseline/evaluation/val/
```

These were generated from `data/splits/val.csv`.

```text
outputs/runs/unet_local_baseline/predictions/test/
outputs/runs/unet_local_baseline/evaluation/test/
```

These were generated from `data/splits/test.csv`, the internal held-out test
split.

The model was trained on `data/splits/train.csv`, selected with
`data/splits/val.csv`, then evaluated on both `val` and internal `test`.

## Core Run Files

Every real run should contain:

```text
outputs/runs/<run_id>/
  config.json
  metrics.csv
  best_model.pt
  predictions/
  evaluation/
```

`config.json` is the exact config saved at training time.

`metrics.csv` contains training-loop metrics by epoch:

```text
epoch, train_loss, val_loss, val_dice
```

`best_model.pt` is the checkpoint selected by best validation Dice during
training.

`predictions/` and `evaluation/` are created later by inference/evaluation
commands.

## Current Baseline Run

Current local baseline run:

```text
run_id: unet_local_baseline
config: configs/unet_local_baseline.yaml
saved config: outputs/runs/unet_local_baseline/config.json
checkpoint: outputs/runs/unet_local_baseline/best_model.pt
```

This run used:

```text
dataset subset: training
splits dir:     data/splits
split id:       seed42_train698_val152_test149
train split:    data/splits/train.csv
val split:      data/splits/val.csv
test split:     data/splits/test.csv
```

The local baseline was trained with MPS enabled:

```yaml
training:
  device: auto
  mps: true
```

## Config-Driven Experiments

Configs live under:

```text
configs/
```

To run a different model or experiment, copy an existing config and change only
the experiment-specific fields.

Common fields to change:

```yaml
run:
  id: attention_unet_local_baseline

model:
  name: attention_unet
  in_channels: 1
  out_channels: 1
  base_channels: 16
  dropout: 0.0

loss:
  name: bce_dice
  bce_weight: 0.5
  dice_weight: 0.5

training:
  seed: 42
  device: auto
  mps: true
  epochs: 10
  batch_size: 4
```

Fields that should stay the same for fair model comparisons:

```yaml
dataset:
  root: data/raw/HC18
  subset: training
  image_size: [256, 384]
  target_type: filled
  band_width: 3

splits:
  dir: data/splits
  split_id: seed42_train698_val152_test149
```

Changing `model.name` compares architectures. Changing `loss` compares loss
functions. Changing `dataset.image_size`, `target_type`, or `band_width`
changes the task setup and should be clearly labeled as an ablation.

## Standard Commands

Train from a config:

```bash
.venv/bin/python -m src.training.train --config configs/unet_local_baseline.yaml
```

Evaluate validation split:

```bash
.venv/bin/python -m src.evaluation.evaluate \
  --config outputs/runs/unet_local_baseline/config.json \
  --checkpoint outputs/runs/unet_local_baseline/best_model.pt \
  --split val
```

Evaluate internal test split:

```bash
.venv/bin/python -m src.evaluation.evaluate \
  --config outputs/runs/unet_local_baseline/config.json \
  --checkpoint outputs/runs/unet_local_baseline/best_model.pt \
  --split test
```

Generate report figures:

```bash
.venv/bin/python scripts/make_report_figures.py \
  --run-id unet_local_baseline \
  --split val
```

Use the saved run config under `outputs/runs/<run_id>/config.json` for
evaluation so the dataset size, model settings, and split settings match the
checkpoint.

## Report Guidance

For the course report, keep the split language explicit:

- training split: used to fit model weights;
- validation split: used during training and checkpoint selection;
- internal test split: used after training for held-out labeled evaluation;
- official HC18 test set: not used for current reported metrics unless a future
  task adds official unlabeled inference/submission handling.

When reporting model comparisons, include:

- run id,
- config path,
- split id,
- checkpoint path,
- evaluated split,
- Dice,
- IoU,
- HD95 in mm,
- HC MAE in mm,
- HC RMSE in mm.
