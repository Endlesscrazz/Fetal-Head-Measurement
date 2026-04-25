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
