# DECISIONS.md

This file records durable, non-trivial project decisions. Use append-only
entries unless correcting an explicit error.

Each entry should include:

- date,
- decision,
- rationale,
- alternatives considered,
- impact on future work.

## 2026-04-28 - V2 demo branch

Decision:
Create a `v2-demo` branch from the completed v1 checkpoint on `main`.

Rationale:
V1 is now a stable course-submission baseline. V2 should evolve as a portfolio
demo without blurring the history of the submitted pipeline.

Alternatives considered:
Continuing all work on `main`; creating a separate repository for the demo.

Impact on future work:
Demo planning and implementation should happen on `v2-demo` until it is ready
to merge or present.

## 2026-04-28 - Streamlit as preferred demo framework

Decision:
Use Streamlit as the default framework for the v2 educational demo.

Rationale:
The demo is a visual, Python-native ML pipeline explorer with images, sliders,
tables, and plots. Streamlit supports that workflow with minimal application
infrastructure.

Alternatives considered:
Gradio for a simpler model endpoint demo; React/FastAPI for a more custom web
app.

Impact on future work:
The first app implementation should target a local Streamlit workflow and add
dependencies only when the implementation task begins.

## 2026-04-28 - Saved-output-first demo strategy

Decision:
Build the first v2 demo milestone from saved v1 artifacts before adding live
checkpoint inference.

Rationale:
Saved-output mode gives the fastest reliable portfolio demo, avoids checkpoint
distribution issues, and keeps the first app milestone focused on explaining
the pipeline visually.

Alternatives considered:
Starting with live checkpoint inference; starting with HC18 challenge export.

Impact on future work:
The first demo implementation should use curated saved samples and a manifest.
It should not require retraining, raw data scanning, or checkpoint loading in
the default path.

## 2026-04-28 - Live inference as second milestone

Decision:
Treat live checkpoint inference as a later v2 milestone behind a swappable
adapter interface.

Rationale:
Live inference is valuable for demo polish but adds checkpoint handling,
preprocessing, runtime, and failure-mode complexity. A replaceable adapter lets
saved-output and live modes share the same UI concepts.

Alternatives considered:
Making live inference mandatory in the first app; never adding live inference.

Impact on future work:
The v2 architecture should separate app-stage data from the source that creates
it, so saved artifacts and live model outputs can feed the same visual
components.

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

## 2026-04-25 - Attention U-Net implementation shape

Decision:
Implement Attention U-Net with additive attention gates on each decoder skip
connection, reusing the existing U-Net double-convolution and downsampling
blocks.

Rationale:
This keeps the improved model comparable to the U-Net baseline while adding the
intended attention mechanism only at skip fusion points. Reusing shared blocks
also reduces implementation drift and makes the report comparison cleaner.

Alternatives considered:
Writing a completely separate U-Net implementation; adding residual blocks;
using transformer-style attention.

Impact on future work:
Attention U-Net can be selected with `model.name: attention_unet` and trained
with the same dataset, loss, optimizer, inference, and evaluation pipeline as
the U-Net baseline.

## 2026-04-25 - First local Attention U-Net run

Decision:
Use `attention_unet_local_baseline` as the first full-pipeline development run
for the improved model: same split id as `unet_local_baseline`, 10 epochs,
256x384 images, base channels 16, MPS backend.

Rationale:
The course report needs a baseline-versus-improved-model comparison on the same
data split. Running Attention U-Net locally provides a comparable development
result before any CHPC/report-grade reruns.

Alternatives considered:
Waiting for CHPC before training Attention U-Net; running only a smoke test;
changing image size or split while changing architecture.

Impact on future work:
Use these as local development comparison numbers. Any final CHPC comparison
should preserve the same split id and clearly label changes in image size,
epochs, or model capacity.

Results:
Validation: Dice 0.9631, IoU 0.9356, HD95 2.05 mm, HC MAE 2.74 mm, HC RMSE
4.30 mm. Internal test: Dice 0.9669, IoU 0.9373, HD95 2.38 mm, HC MAE 3.37 mm,
HC RMSE 4.68 mm.

## 2026-04-25 - V1 local reduced-resource report path

Decision:
Complete the v1 course-submission pipeline and report using local MacBook MPS
runs with clearly documented reduced-resource settings when needed. Treat CHPC
full-scale runs as a later strengthening step after the complete local pipeline,
configs, report artifacts, and runner are ready.

Rationale:
The course instructions allow reducing the number of instances and/or image
resolution within reasonable limits when the suggested dataset is too large for
available compute. The current local runs use the full labeled split but reduced
image resolution and model width, which is a reasonable development/report path
as long as it is disclosed.

Alternatives considered:
Blocking report work until CHPC full-scale U-Net and Attention U-Net runs are
complete; running only smoke/subsample experiments locally; depending on Colab.

Impact on future work:
The next sessions should prioritize local report completeness: comparison
tables, focused ablations, report figures, and `Myproject.sh`. CHPC scripts and
larger configs should remain available for post-v1/full-scale reruns, and any
CHPC numbers must be clearly labeled separately from local results.

## 2026-04-25 - Local loss and augmentation ablations

Decision:
Use `attention_unet_dice_loss` and `attention_unet_aug` as the focused local
P4.S3 ablations against `attention_unet_local_baseline`.

Rationale:
The report needs analysis beyond a single model comparison. A Dice-only loss
tests the value of BCE+Dice, while training-only horizontal flip plus mild
intensity/noise augmentation tests whether simple ultrasound-safe augmentation
improves generalization.

Alternatives considered:
Running many hyperparameter sweeps; adding a third architecture; delaying
ablations until CHPC.

Impact on future work:
For local v1 results, Attention U-Net with BCE+Dice and no augmentation remains
the best model so far. The ablation table is generated at
`outputs/tables/local_ablation_summary.csv` and can be reused in the report.

Results:
Dice-only internal test: Dice 0.9615, IoU 0.9293, HD95 2.48 mm, HC MAE
3.45 mm, HC RMSE 5.13 mm. Augmented internal test: Dice 0.9606, IoU 0.9275,
HD95 2.83 mm, HC MAE 3.72 mm, HC RMSE 5.85 mm. Both underperformed the
non-augmented Attention U-Net baseline on internal-test HC error.

## 2026-04-25 - Post-processing ablation interpretation

Decision:
Use cleaned ellipse fitting as the final HC measurement method, and report
direct contour-length measurements as post-processing ablations.

Rationale:
Direct contour length from predicted binary masks overestimates HC because mask
boundaries are jagged and can include small noisy components. Ellipse fitting
regularizes the boundary into the clinically relevant head-shape assumption and
substantially reduces HC error.

Alternatives considered:
Measuring all raw mask contours directly; measuring the cleaned largest
component contour directly; fitting an ellipse without connected-component
cleanup.

Impact on future work:
Final report HC values should use the cleaned ellipse variant. The
post-processing ablation table is saved at
`outputs/tables/local_postprocess_ablation_summary.csv`.

Results:
On the Attention U-Net internal-test split, raw all-contour measurement had HC
MAE 16.73 mm, cleaned contour measurement had HC MAE 14.04 mm, and cleaned
ellipse measurement had HC MAE 3.37 mm.

## 2026-04-25 - Local report artifact bundle

Decision:
Generate the v1 local report artifact bundle under `report/` from saved run
artifacts using `scripts/build_report_artifacts.py`.

Rationale:
The report should cite reproducible CSVs and figures instead of manually copied
numbers. Building the report bundle from saved evaluation outputs keeps local
and future CHPC results on the same reporting path.

Alternatives considered:
Writing report tables manually; using only the raw `outputs/tables/` files;
waiting for CHPC before assembling report artifacts.

Impact on future work:
Use `report/report-results-summary.md`, `report/tables/`, and
`report/figures/` as the starting point for the final 6-page PDF report.
Regenerate them with `scripts/build_report_artifacts.py` after any future
reruns.

## 2026-04-25 - Course runner modes

Decision:
Make `Myproject.sh` default to a fast `report-only` mode that rebuilds report
artifacts from saved local run outputs, while also supporting `--full-local` for
retraining and reevaluating the complete local v1 experiment set.

Rationale:
The course runner must be easy for review, but retraining four local experiments
can take substantial time. A default report-only path verifies the submitted
results quickly when saved artifacts are included, and the full-local path
preserves end-to-end reproducibility.

Alternatives considered:
Always retraining by default; keeping the placeholder runner; only documenting
manual commands in README.

Impact on future work:
Use `bash Myproject.sh` for quick final verification. Use
`bash Myproject.sh --full-local` when the saved run artifacts need to be
regenerated from scratch.

## 2026-04-25 - Final report packaging files

Decision:
Keep final submission planning files under `report/`: `final-report-outline.md`,
`assets-index.md`, and `submission-checklist.md`.

Rationale:
The final course deliverable needs a short PDF report plus a code ZIP. Keeping
the outline, asset map, and checklist next to the generated report artifacts
reduces the chance of omitting required metrics, reduced-resource disclosures,
or saved outputs needed by `Myproject.sh`.

Alternatives considered:
Only relying on README; putting packaging notes in `handoff.md`; waiting until
after PDF writing to list assets.

Impact on future work:
Use these files to write the final PDF and assemble the course ZIP. The GitHub
repo can stay lean, while the course ZIP can include saved run artifacts needed
for fast report-only verification.
