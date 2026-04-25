# DECISIONS.md

This file records durable, non-trivial project decisions. Use append-only
entries unless correcting an explicit error.

Each entry should include:

- date,
- decision,
- rationale,
- alternatives considered,
- impact on future work.

## 2026-04-25 - Script-first workflow

Decision:
Use scripts and configs as the primary workflow for v1. Do not maintain a
parallel notebook implementation.

Rationale:
The course submission needs to be reproducible, and scripts are easier to run
locally, on CHPC, and from `Myproject.sh`.

Alternatives considered:
Maintaining both notebooks and scripts; using Colab notebooks as the main
workflow.

Impact on future work:
All core logic must live in importable modules and script entrypoints. Notebooks
may be added later only as optional exploration/reporting helpers.

## 2026-04-25 - Local plus CHPC compute plan

Decision:
Use the MacBook M1 Air for development, unit tests, and tiny smoke runs. Use
university CHPC Slurm GPU nodes for long/full training and final ablations.
Do not depend on Google Colab for v1.

Rationale:
The dataset and architecture are manageable enough for local development, while
CHPC provides a more appropriate path for repeatable long runs.

Alternatives considered:
Google Colab Pro GPU workflow through VS Code; TPU support through PyTorch/XLA.

Impact on future work:
Training scripts must be portable and avoid hard-coded local paths. Slurm job
files will be added for final runs.

## 2026-04-25 - U-Net baseline

Decision:
Implement U-Net as the required baseline model.

Rationale:
U-Net is a standard, defensible biomedical segmentation baseline and directly
supports the assignment requirement for a non-trivial deep neural network.

Alternatives considered:
Starting directly with Attention U-Net, ResUNet, or transformer-based models.

Impact on future work:
All improved models must use the same tensor contract as U-Net so experiments
remain comparable.

## 2026-04-25 - Attention U-Net improved model

Decision:
Use Attention U-Net as the main improved model for v1.

Rationale:
Attention gates give a clear report story for noisy ultrasound segmentation by
encouraging the model to focus on relevant head structures.

Alternatives considered:
ResUNet, U-Net++, DeepLabV3+, SegFormer.

Impact on future work:
Attention U-Net should be implemented after the U-Net baseline and evaluated on
the same split. ResUNet remains fallback/stretch only.

## 2026-04-25 - No v1 web demo

Decision:
Do not build a web demo in v1.

Rationale:
The course grade depends on a complete, reproducible experiment pipeline and
report. A demo is useful for resume v2 but would distract from v1 deliverables.

Alternatives considered:
Building a Streamlit or Gradio app during v1.

Impact on future work:
Inference should still expose a clean script/API so a v2 demo can be added
without rewriting the pipeline.

## 2026-04-25 - `Myproject.sh` course runner

Decision:
Use `Myproject.sh` as the final course runner instead of `Myproject.ipynb`.

Rationale:
A shell runner fits the script-first workflow and is easier to execute on local
machines and CHPC.

Alternatives considered:
Submitting a notebook as the primary reproducibility artifact.

Impact on future work:
All major pipeline stages must be callable from command-line scripts.

## 2026-04-25 - Root governance files

Decision:
Keep `project-tasks.md`, `handoff.md`, and `DECISIONS.md` at repository root.

Rationale:
Future Codex sessions need immediate access to the approved task queue, latest
handoff context, and durable decisions.

Alternatives considered:
Moving all governance files under `docs/`.

Impact on future work:
Every session must read the root governance files before implementation.

## 2026-04-25 - V1 phase/session roadmap

Decision:
Divide v1 into five implementation phases with agent-sized sessions:
foundation/data readiness, U-Net baseline training, inference/evaluation,
Attention U-Net plus ablations, and final CHPC/report packaging.

Rationale:
Small sessions keep Codex agents disciplined, make handoffs easier, and preserve
the required baseline-first build order.

Alternatives considered:
Using only a flat task list; planning by broad milestones without session-sized
implementation units.

Impact on future work:
Agents should pick the next phase/session from `project-tasks.md`, starting
with `P1.S1`, and update `handoff.md` after each completed session.

## 2026-04-25 - HC18 target source support

Decision:
Support both paired HC18 annotation images and explicit ellipse metadata as
segmentation target sources, preferring annotation images when present.

Rationale:
The raw dataset was not present locally during Phase 1, and HC18 distributions
may expose supervision as paired annotation images and/or ellipse-like metadata.
Supporting both paths keeps parsing explicit without hard-coding an unverified
local layout.

Alternatives considered:
Only supporting ellipse CSV columns; delaying all data code until the dataset is
available.

Impact on future work:
Once the real dataset is copied into `data/raw/HC18/`, `docs/dataset-format.md`
must be updated with observed columns and filenames, and the parser should be
adjusted only if the real layout differs.

## 2026-04-25 - uv-managed local environment

Decision:
Use `uv` to create and manage the project virtual environment at `.venv/`, with
a project-local cache directory `.uv-cache/` when sandbox/home-cache access is
restricted.

Rationale:
Future Codex sessions need a consistent environment with `pytest`, PyTorch,
OpenCV, pandas, and plotting dependencies available without installing into
system Python.

Alternatives considered:
Using system Python directly; using standard `venv` plus `pip`.

Impact on future work:
Agents should run project commands through `.venv/bin/python` or `uv` and avoid
system-level package installs.

## 2026-04-25 - HC18 local dataset placement

Decision:
Extract the downloaded HC18 archive from `/Users/shreyas/Downloads/1327317.zip`
into `data/raw/HC18/`.

Rationale:
The project needs local raw data to validate parsing, splits, and overlays.

Alternatives considered:
Leaving the dataset in Downloads and pointing configs there.

Impact on future work:
Configs can use the stable relative path `data/raw/HC18`. Raw data remains
ignored by git.

## 2026-04-25 - Baseline and smoke training configs

Decision:
Keep `configs/unet_baseline.yaml` for real baseline runs and
`configs/unet_smoke.yaml` for tiny local smoke training.

Rationale:
The baseline Slurm workflow should not accidentally run a tiny smoke
experiment, while local validation needs a fast CPU-friendly config.

Alternatives considered:
Using one config for both smoke and real training; overriding many values from
the smoke script.

Impact on future work:
Use `configs/unet_smoke.yaml` for quick local checks and
`configs/unet_baseline.yaml` for reported/CHPC baseline training.

## 2026-04-25 - Local CPU U-Net baseline config

Decision:
Add `configs/unet_local_baseline.yaml` for a full-split local U-Net baseline on
the MacBook with MPS requested: 256x384 images, base channels 16, 10 epochs, no
smoke sample limit.

Rationale:
Sandboxed commands report no MPS/CUDA backend, but escalated local execution can
access MPS. The full 352x512/base32/50-epoch baseline is still more appropriate
for CHPC, while this local baseline trains on the full train split and runs the
full inference/evaluation pipeline.

Alternatives considered:
Running the CHPC-sized baseline config locally; waiting until CHPC before
getting any baseline numbers.

Impact on future work:
Use local baseline metrics as development baseline numbers, and use
`configs/unet_baseline.yaml` later for stronger CHPC/report-grade baseline
training.

## 2026-04-25 - MPS execution requires non-sandboxed launch

Decision:
Use `mps: true` in local training configs and launch local training/evaluation
outside the sandbox when MPS is needed.

Rationale:
Inside the sandbox, PyTorch reported `mps_available=False`; outside the sandbox,
the same environment reported `mps_available=True` and successfully allocated a
tensor on `mps:0`.

Alternatives considered:
Training only on CPU; waiting for CHPC before baseline training.

Impact on future work:
Local Mac training commands that need MPS should be run with escalation/outside
the sandbox. CPU-only smoke tests can still run normally.

## 2026-04-25 - First local U-Net baseline numbers

Decision:
Use `unet_local_baseline` as the first full-pipeline development baseline:
full train split, 10 epochs, 256x384 images, base channels 16, MPS backend.

Rationale:
This produces real end-to-end U-Net numbers before implementing Attention U-Net,
while staying feasible on the MacBook Air.

Alternatives considered:
Running the larger CHPC baseline config locally; proceeding to Attention U-Net
without real baseline numbers.

Impact on future work:
These numbers are suitable as development baseline numbers. CHPC/report-grade
runs can later use the larger `configs/unet_baseline.yaml` if time allows.

Results:
Validation: Dice 0.9598, IoU 0.9296, HD95 2.36 mm, HC MAE 3.13 mm, HC RMSE
4.51 mm. Internal test: Dice 0.9600, IoU 0.9261, HD95 3.02 mm, HC MAE 3.78 mm,
HC RMSE 5.56 mm.

## 2026-04-25 - Geometry-based HC measurement

Decision:
Convert predicted masks into HC measurements with deterministic post-processing:
threshold probabilities, keep the largest connected component, extract the
outer contour, fit an ellipse, and compute HC from sampled ellipse points scaled
by pixel spacing.

Rationale:
This matches the assignment's segmentation-first requirement while keeping the
neural prediction and geometric measurement stages debuggable and ablatable.
Sampling ellipse points in physical units handles anisotropic spacing more
safely than multiplying a pixel circumference by a single scalar.

Alternatives considered:
Measuring raw mask contour length directly; using only Ramanujan pixel
circumference with average spacing; predicting HC directly with regression.

Impact on future work:
Evaluation can compare raw/cleaned/ellipse post-processing variants, and final
reported HC values should come from the geometry pipeline rather than raw model
logits.
