# Project Tasks

This file is the approved task queue for Codex agents. Agents must implement
one task at a time unless the user explicitly expands scope.

Task status values:

- `todo`
- `in_progress`
- `blocked`
- `done`

## V1 Completion Status

V1 is complete and frozen except for bug fixes, reproducibility fixes, or
explicit user-requested packaging/report updates. New portfolio/demo work should
use the V2 roadmap below and the root `AGENTS.md` operating contract.

## V1 Phase and Session Roadmap

Agents should work session-by-session. A session is sized so a coding agent can
finish implementation, verification, and handoff in one focused pass.

### Phase 1 - Foundation and Data Readiness

Goal:
Create the runnable project skeleton and make HC18 data trustworthy before any
modeling work begins.

Sessions:

- `P1.S1` - Create project skeleton and local/CHPC-ready scaffolding.
  - Primary task: `S1`
  - Outcome: directories, package files, `.gitignore`, `requirements.txt`, and
    placeholder `Myproject.sh` exist.
- `P1.S2` - Inspect the actual HC18 dataset layout.
  - Primary task: `D1`
  - Outcome: `docs/v1/dataset-format.md` documents observed files, columns,
    image dimensions, pixel spacing, and annotation format.
- `P1.S3` - Implement dataset parsing and ellipse mask generation.
  - Primary task: `D2`
  - Outcome: dataset returns image, mask, spacing, sample id, and annotation
    metadata with geometry-safe resizing.
- `P1.S4` - Create deterministic splits and visual sanity overlays.
  - Primary task: `D3`
  - Outcome: split CSVs and at least 10 overlay checks can be generated.

Phase 1 completion criteria:

- raw data layout is documented;
- dataloader works;
- generated masks have visual overlays;
- split files are reusable and not hidden inside training code.

### Phase 2 - U-Net Baseline Training

Goal:
Train the first reproducible segmentation baseline with logged metrics and a
checkpoint.

Sessions:

- `P2.S1` - Implement U-Net baseline.
  - Primary task: `M1`
  - Outcome: U-Net forward pass test works for `[B, 1, H, W] -> [B, 1, H, W]`.
- `P2.S2` - Implement losses, optimizer setup, trainer, and baseline config.
  - Primary task: `T1`
  - Outcome: config-driven training writes metrics and checkpoints.
- `P2.S3` - Run local tiny smoke training and fix only blocking issues.
  - Primary task: `T1`
  - Outcome: one tiny run completes on local machine.
- `P2.S4` - Prepare baseline CHPC run command/config.
  - Primary task: `C1`
  - Outcome: U-Net Slurm job calls existing training entrypoint.

Phase 2 completion criteria:

- baseline U-Net trains end-to-end;
- run artifacts include config, seed, split id, checkpoint, and metrics.

Status note:
Local MPS baseline `unet_local_baseline` completed for 10 epochs on the full
train split and was evaluated on val/internal-test splits.

### Phase 3 - Inference, Geometry, and Evaluation

Goal:
Convert segmentation outputs into HC measurements and report-ready metrics.

Sessions:

- `P3.S1` - Implement deterministic geometry utilities.
  - Primary task: `I1`
  - Outcome: cleanup, contour extraction, ellipse fitting, and circumference
    tests exist.
- `P3.S2` - Implement prediction script and artifact schema.
  - Primary task: `I1`
  - Outcome: predictions save mask, ellipse, HC pixels/mm, and overlays.
- `P3.S3` - Implement evaluation metrics.
  - Primary task: `E1`
  - Outcome: segmentation and HC metrics are saved per-sample and aggregated.
- `P3.S4` - Generate baseline report artifacts.
  - Primary task: `E1`
  - Outcome: baseline table rows, curves, and qualitative panels exist.

Phase 3 completion criteria:

- image -> mask -> ellipse -> HC mm works;
- Dice/IoU/HD and HC error metrics are generated;
- baseline results are ready for the report.

### Phase 4 - Attention U-Net and Focused Ablations

Goal:
Add the improved model and run a small, defensible experiment matrix.

Sessions:

- `P4.S1` - Implement Attention U-Net.
  - Primary task: `M2`
  - Outcome: model registry supports Attention U-Net with the same tensor
    contract as U-Net.
- `P4.S2` - Train Attention U-Net on the same split.
  - Primary task: `T1`
  - Outcome: Attention U-Net run artifacts are comparable to baseline.
  - Status: done locally with `attention_unet_local_baseline`.
- `P4.S3` - Run loss/augmentation ablations.
  - Primary task: `E1`
  - Outcome: focused ablation table compares 2-3 meaningful changes.
  - Status: done locally with Dice-loss and augmentation ablations.
- `P4.S4` - Run post-processing ablation.
  - Primary task: `I1` / `E1`
  - Outcome: raw mask measurement vs cleanup + ellipse fit is quantified.
  - Status: done locally for `attention_unet_local_baseline`.

Phase 4 completion criteria:

- U-Net and Attention U-Net are compared on the same split;
- at least 2-3 ablations are recorded with attributable run artifacts.

Status note:
Local MPS Attention U-Net `attention_unet_local_baseline` completed for 10
epochs on the same split as `unet_local_baseline` and was evaluated on
val/internal-test splits.
Local ablations `attention_unet_dice_loss` and `attention_unet_aug` completed
on the same split. The consolidated table is
`outputs/tables/local_ablation_summary.csv`.
Post-processing ablation completed for `attention_unet_local_baseline`; the
consolidated table is `outputs/tables/local_postprocess_ablation_summary.csv`.

### Phase 5 - CHPC Final Runs, Report, and Packaging

Goal:
Produce the final course submission and GitHub-ready project state using the
complete local/reduced-resource pipeline first. CHPC full-scale reruns are
valuable but should not block v1 report completion.

Sessions:

- `P5.S1` - Build local report comparison artifacts.
  - Primary task: `E1`
  - Outcome: comparison tables/figures clearly label local reduced-resource
    settings, split id, run ids, and metrics.
  - Status: done locally; artifacts are under `report/`.
- `P5.S2` - Finalize `Myproject.sh` and README reproducibility commands.
  - Primary task: `R1`
  - Outcome: course runner can reproduce the local v1 pipeline or regenerate
    report artifacts from saved outputs.
  - Status: done; default runner rebuilds report artifacts from saved outputs,
    and `--full-local` retrains/evaluates the local v1 experiment set.
- `P5.S3` - Package final report assets and submission checklist.
  - Primary task: `R1`
  - Outcome: code, report inputs, and run artifacts are ready for submission.
  - Status: done; report outline, asset index, and submission checklist are
    under `report/`.
- `P5.S4` - Finalize CHPC Slurm workflow for post-v1/full-scale reruns.
  - Primary task: `C1`
  - Outcome: train/evaluate Slurm scripts and README workflow are complete.

Phase 5 completion criteria:

- final reported numbers come from saved run artifacts;
- `Myproject.sh` reproduces the main pipeline;
- README explains local and CHPC use clearly;
- any reduced-resource settings are explicit in the report/configs.

Status note:
For v1, local MPS runs at 256x384 resolution and base channels 16 are acceptable
course-submission candidates if clearly disclosed. CHPC 352x512/base32/longer
runs become a post-v1 strengthening step rather than a blocker.
Local report comparison artifacts have been generated under `report/`, including
`report/report-results-summary.md`, report tables, and three summary figures.
`Myproject.sh` and README reproducibility commands have been finalized for the
local v1 report path.
Final report packaging aids have been created:
`report/final-report-outline.md`, `report/assets-index.md`, and
`report/submission-checklist.md`.
Initial final report draft has been created at `report/final-report-draft.md`.
Generated reviewable final report files:
`report/final-report.md` and `report/final-report.pdf` (4 pages after review
edits).

## V2 Demo Roadmap

V2 turns the completed v1 pipeline into an educational React/Vite demo. Agents
must read root `AGENTS.md`, `docs/v2_demo/architecture.md`,
`docs/v2_demo/project-spec.md`, `docs/v2_demo/roadmap.md`,
`docs/v2_demo/project-tasks.md`, and `docs/v2_demo/DECISIONS.md` before v2
work. Use `docs/v2_demo/project-tasks.md` for session-level implementation
order.

### V2.P0 - V1 checkpoint and branch setup

Status: done

Goal:
Commit the completed v1 pipeline on `main`, push it, and create the
`v2-demo` branch.

Done criteria:

- v1 checkpoint commit exists on `main`;
- `main` is pushed;
- v2 work is on `v2-demo`;
- final Canvas ZIP remains local and uncommitted.

### V2.P1 - Planning docs and governance pointers

Status: done

Goal:
Create `docs/v2_demo/` planning docs and add root governance pointers.

Done criteria:

- root `AGENTS.md` contains the v2 operating contract;
- `docs/v2_demo/architecture.md` exists;
- `docs/v2_demo/project-spec.md` exists;
- `docs/v2_demo/roadmap.md` exists;
- `docs/v2_demo/DECISIONS.md` exists;
- `docs/v1/AGENTS.md` and `docs/v1/DECISIONS.md` preserve v1 governance;
- `project-tasks.md` and `handoff.md` reference the v2 plan.

### V2.P2 - Saved artifact curation and sample manifest

Status: done

Goal:
Choose curated examples and define the manifest-backed saved artifacts needed by
the demo.

Done criteria:

- the manifest schema in `docs/v2_demo/architecture.md` is treated as the app
  contract;
- `docs/v2_demo/curated-samples.md` and
  `docs/v2_demo/curated-samples.json` define the selected sample set;
- selected examples include strong and high-error/failure cases from the
  internal-test split;
- no raw data or checkpoints are committed without explicit approval.

### V2.P2.5 - Demo artifact export and manifest validation

Status: done

Goal:
Revise the small raw-data-free saved-output bundle for the React design contract
and validate its manifest. A previous Streamlit-oriented export exists, but it
does not satisfy the current `prob.png` and TypeScript manifest requirements.

Done criteria:

- `scripts/export_demo_artifacts.py` creates `outputs/demo_samples/`;
- `scripts/validate_demo_manifest.py` validates required fields and paths;
- exported samples include `ultrasound.png`, `target.png`, `pred.png`, and
  `prob.png`;
- manifest schema version 2 includes real metrics, `predEllipse`, `contourHC`,
  `confidence`, pixel spacing, and resolution;
- raw HC18 is required only for export, not for app runtime;
- the saved-output app can read the exported bundle without raw HC18 data or
  checkpoints.

### V2.P3 - React saved-output explorer

Status: done

Goal:
Build the portfolio app using saved v1 artifacts, not live model inference.

Done criteria:

- `npm run dev` launches the app from `frontend/`;
- user can select a sample from the visual gallery;
- app shows the design's six sections: cases, pipeline, threshold, geometry,
  metrics, and research;
- app reads `frontend/public/samples/manifest.json`;
- threshold slider re-thresholds real `prob.png` files in canvas;
- app shows contour-vs-ellipse comparison when both values are available;
- app includes training/validation loss curves from saved v1 metrics;
- fixed safety chip says the demo is educational and not for clinical use.

### V2.P4 - Live inference integration

Status: in_progress

Status note:
`V2.S7.1` is complete: `src/inference/live.py` provides the reusable
single-sample inference core and exporter helper reuse, with contract tests and
a local curated-sample smoke path.

Goal:
Add optional curated-sample checkpoint inference through a swappable adapter.
Detailed planning lives in `docs/v2_demo/live-inference-plan.md`.

Done criteria:

- live mode works on at least one local sample;
- live mode returns JSON compatible with the React `Sample` interface;
- saved-output mode still works without checkpoints;
- arbitrary public upload and artifact/checkpoint publishing remain out of
  scope unless explicitly approved.

### V2.P5 - Portfolio README polish and screenshots

Status: in_progress

Status note:
README polish, `start_demo.sh`, Vercel config, and public-safe preview assets
are prepared, and the public production URL is now live at
`https://fetal-head-measurement.vercel.app/`. Remaining work is presentation
polish rather than deployment unblock.

Goal:
Make the project easy to review from GitHub and interview demos.

Done criteria:

- README includes demo run instructions;
- screenshots or GIF references are added when available;
- README or helper script includes a one-command local start path for reviewers;
- portfolio framing is concise and accurate.

### V2.P6 - Optional HC18 challenge exporter

Status: todo

Goal:
Add official-test CSV export tooling for a learning-oriented HC18 challenge
submission.

Done criteria:

- exported CSV matches challenge columns, row count, filenames, and units;
- no official labels are assumed.

## Task G0 - Documentation and Governance Cleanup

Status: done

Role: Planner Agent

Goal:
Create the repository governance files that future Codex sessions must follow.

Allowed files:

- `AGENTS.md`
- `README.md`
- `project-tasks.md`
- `handoff.md`
- `docs/v1/DECISIONS.md`
- `docs/v1/architecture.md`
- `docs/v1/project-spec.md`

Out of scope:

- source code implementation
- dependency installation
- dataset download
- training or evaluation runs

Done criteria:

- root contains `AGENTS.md`, `README.md`, `project-tasks.md`, `handoff.md`,
  with v1 decisions archived under `docs/v1/DECISIONS.md`;
- long planning docs live under `docs/`;
- stale references to the deleted legacy handoff file are removed;
- governance docs reference `handoff.md` and the relevant decision log.

Verification:

- `rg --files -g '*.md'`
- search the repository for the deleted legacy handoff filename and confirm no
  matches
- `test -f AGENTS.md`
- `test -f README.md`
- `test -f project-tasks.md`
- `test -f handoff.md`
- `test -f docs/v1/DECISIONS.md`

## Task G1 - V1 Phase and Session Roadmap

Status: done

Role: Planner Agent

Goal:
Divide v1 into phases and implementation sessions that future coding agents can
complete one at a time.

Allowed files:

- `AGENTS.md`
- `project-tasks.md`
- `handoff.md`
- `docs/v1/DECISIONS.md`

Out of scope:

- source code implementation
- project skeleton creation
- dataset inspection

Done criteria:

- `project-tasks.md` has a phase/session roadmap;
- `AGENTS.md` tells agents to follow the phase/session roadmap;
- `docs/v1/DECISIONS.md` records the roadmap decision;
- `handoff.md` points the next agent to `P1.S1`.

Verification:

- `rg "P1.S1|Phase 1|Phase 5" project-tasks.md`
- `rg "phase/session" AGENTS.md project-tasks.md handoff.md docs/v1/DECISIONS.md`

## Task S1 - Create Project Skeleton

Status: done

Phase/session: `P1.S1`

Role: Planner Agent

Goal:
Create the script-first repository structure for data, configs, source code,
outputs, report assets, scripts, Slurm jobs, and tests.

Allowed files:

- package/source directories under `src/`
- `configs/`
- `scripts/`
- `slurm/`
- `tests/`
- `report/`
- `.gitignore`
- `requirements.txt`
- `Myproject.sh`

Out of scope:

- implementing dataset parsing
- implementing model code
- running training

Done criteria:

- expected directories exist;
- Python packages have `__init__.py` where needed;
- raw data and outputs are ignored by git;
- `Myproject.sh` exists as a placeholder runner with clear TODOs.

Verification:

- `find . -maxdepth 3 -type d | sort`
- `rg --files`

## Task D1 - Inspect HC18 Dataset Layout

Status: done

Phase/session: `P1.S2`

Role: Data Agent

Goal:
Inspect the actual HC18 files available locally and document the observed image,
annotation, and pixel-spacing layout.

Allowed files:

- `docs/v1/dataset-format.md`
- `handoff.md`
- `docs/v1/DECISIONS.md` if needed

Out of scope:

- writing the final dataset class
- generating splits
- training

Done criteria:

- observed file names and annotation columns are documented;
- image dimensions and pixel-spacing sources are confirmed;
- any ambiguity is recorded explicitly.

Verification:

- file listing commands over `data/raw/HC18/`
- small metadata inspection command once data exists

## Task D2 - Implement Dataset Parser and Mask Generation

Status: done

Phase/session: `P1.S3`

Role: Data Agent

Goal:
Implement HC18 loading, annotation parsing, and deterministic ellipse-derived
mask generation.

Allowed files:

- `src/data/dataset.py`
- `src/data/masks.py`
- `src/data/transforms.py`
- `tests/test_data.py`
- `docs/v1/dataset-format.md`

Out of scope:

- model implementation
- training loop
- inference geometry

Done criteria:

- dataset returns image, mask, spacing, sample id, and annotation metadata;
- mask/image shapes match;
- resize behavior is explicit and geometry-safe;
- unit tests cover at least one synthetic annotation case.

Verification:

- `pytest tests/test_data.py`

## Task D3 - Create Splits and Overlay Sanity Checks

Status: done

Phase/session: `P1.S4`

Role: Data Agent

Goal:
Create deterministic train/val/internal-test splits and visual overlay checks
for generated masks.

Allowed files:

- `src/data/make_splits.py`
- `scripts/visualize_samples.py`
- `configs/data.yaml`
- `data/splits/`
- `outputs/figures/`

Out of scope:

- model training
- architecture changes

Done criteria:

- reusable split files are saved;
- at least 10 random overlay images can be generated;
- split seed is configurable and recorded.

Verification:

- `python -m src.data.make_splits --config configs/data.yaml`
- `python scripts/visualize_samples.py --config configs/data.yaml --n 10`

## Task M1 - Implement U-Net Baseline

Status: done

Phase/session: `P2.S1`

Role: Modeling Agent

Goal:
Implement the baseline U-Net with the stable segmentation interface.

Allowed files:

- `src/models/unet.py`
- `src/models/__init__.py`
- `tests/test_models.py`

Out of scope:

- Attention U-Net
- training loop
- data parsing changes

Done criteria:

- model accepts `[B, 1, H, W]`;
- model returns `[B, 1, H, W]` logits;
- parameter count can be computed.

Verification:

- `pytest tests/test_models.py`

## Task T1 - Implement Training Loop

Status: done

Phase/session: `P2.S2`, `P2.S3`, `P4.S2`

Role: Training Agent

Goal:
Implement config-driven training with metrics logging and checkpointing.

Allowed files:

- `src/training/train.py`
- `src/training/trainer.py`
- `src/training/losses.py`
- `src/training/optim.py`
- `configs/unet_baseline.yaml`
- `configs/unet_smoke.yaml`
- `scripts/run_smoke_train.py`

Out of scope:

- Attention U-Net
- final long runs
- web demo

Done criteria:

- one tiny local smoke run completes;
- metrics CSV/JSON is written;
- best checkpoint is saved;
- seed, split id, and config are recorded.

Verification:

- `python scripts/run_smoke_train.py --config configs/unet_smoke.yaml`

Progress:
Training loop supports both U-Net and Attention U-Net through the model
registry. Local Attention U-Net run `attention_unet_local_baseline` completed
using the same split id as the U-Net local baseline.

## Task I1 - Implement Inference and Geometry

Status: done

Phase/session: `P3.S1`, `P3.S2`, `P4.S4`

Role: Inference + Geometry Agent

Goal:
Convert model probabilities into cleaned masks, fitted ellipses, and HC in mm.

Allowed files:

- `src/inference/predict.py`
- `src/utils/geometry.py`
- `tests/test_geometry.py`

Out of scope:

- training loop changes
- new model architecture

Done criteria:

- thresholding and largest connected component cleanup exist;
- contour extraction and ellipse fitting exist;
- Ramanujan circumference calculation exists;
- ellipse failure cases are explicit.

Verification:

- `pytest tests/test_geometry.py`

## Task E1 - Implement Evaluation and Report Artifacts

Status: done

Phase/session: `P3.S3`, `P3.S4`, `P4.S3`, `P4.S4`, `P5.S2`

Role: Evaluation Agent

Goal:
Compute segmentation and HC metrics and generate report-ready tables/figures.

Allowed files:

- `src/evaluation/metrics.py`
- `src/evaluation/evaluate.py`
- `scripts/make_report_figures.py`
- `outputs/tables/`
- `outputs/figures/`

Out of scope:

- model architecture changes
- new training strategy

Done criteria:

- Dice, IoU, HD95 or Hausdorff, signed HC error, absolute HC error, MAE, and
  RMSE are computed consistently;
- per-sample and aggregate metrics are saved separately;
- qualitative best/worst panels can be generated.

Verification:

- `python -m src.evaluation.evaluate --config <config> --run-id <run_id>`

Progress:
Core Phase 3 evaluation and report-artifact generation are implemented. Future
sessions reuse this task surface for ablations and final report regeneration.

## Task M2 - Implement Attention U-Net

Status: done

Phase/session: `P4.S1`

Role: Modeling Agent

Goal:
Implement Attention U-Net as the main improved model.

Allowed files:

- `src/models/attention_unet.py`
- `src/models/__init__.py`
- `tests/test_models.py`
- `configs/attention_unet.yaml`

Out of scope:

- ResUNet unless explicitly requested
- dataset changes
- evaluation metric changes

Done criteria:

- same tensor contract as U-Net;
- model is selectable by config name;
- forward-pass test passes.

Verification:

- `pytest tests/test_models.py`

Progress:
Attention U-Net is implemented in `src/models/attention_unet.py`, registered as
`attention_unet`, covered by forward-shape tests, and has a local training
config at `configs/attention_unet.yaml`.

## Task C1 - Add CHPC Slurm Workflow

Status: todo

Phase/session: `P2.S4`, `P5.S1`

Role: Reproducibility + Packaging Agent

Goal:
Create Slurm scripts and README instructions for running final experiments on
university CHPC.

Progress:
`P2.S4` baseline U-Net Slurm script exists. Full task remains open for
Attention U-Net and evaluation Slurm scripts in Phase 5.

Allowed files:

- `slurm/train_unet.sbatch`
- `slurm/train_attention_unet.sbatch`
- `slurm/evaluate.sbatch`
- `README.md`

Out of scope:

- changing training logic solely for CHPC
- adding Colab workflow

Done criteria:

- Slurm scripts call existing Python entrypoints;
- output paths go under `outputs/runs/`;
- README explains copy-to-scratch, submit, and sync-back workflow.

Verification:

- shell syntax check where practical

## Task R1 - Package Final Course Submission

Status: todo

Phase/session: `P5.S2`, `P5.S3`, `P5.S4`

Role: Reproducibility + Packaging Agent

Goal:
Prepare the reproducible course deliverable and report assets.

Allowed files:

- `README.md`
- `Myproject.sh`
- `report/`
- `outputs/tables/`
- `outputs/figures/`

Out of scope:

- adding new models
- broad new experiments

Done criteria:

- `Myproject.sh` runs the main reproducible pipeline;
- README has final commands;
- report tables and figures are generated;
- final results match saved run artifacts.

Verification:

- `bash Myproject.sh`

Progress:
`P5.S2` is complete: `Myproject.sh` supports default `report-only` mode and
`--full-local` mode. README documents local v1 results and reproducibility
commands. `P5.S3` is complete: final report outline, asset index, and
submission checklist are available under `report/`. PDF report writing remains.
