# Handoff

This file preserves session-to-session context for Codex agents.

Every meaningful session must update this file. Keep entries concise and
specific. The newest entry should be at the top.

## Current Status

- Phase 1, Phase 2, and Phase 3 implementation are complete through local smoke
  verification.
- First full-pipeline local U-Net baseline run is complete using MPS:
  `unet_local_baseline`.
- V1 plan is script-first PyTorch with local smoke runs and CHPC Slurm for long
  training.
- Current approved task queue lives in `project-tasks.md`.
- Durable decisions live in `DECISIONS.md`.
- V1 is divided into phase/session units in `project-tasks.md`.
- `P1.S1`, `P1.S2`, `P1.S3`, and `P1.S4` are done.
- `P2.S1`, `P2.S2`, `P2.S3`, and `P2.S4` are done for the U-Net baseline.
- `P3.S1`, `P3.S2`, `P3.S3`, and `P3.S4` are done using the smoke checkpoint
  as a wiring check.
- Local uv environment exists at `.venv/`.
- HC18 is extracted under `data/raw/HC18/`.

## Latest Session

Date: 2026-04-25

Task id: Local MPS U-Net baseline run

Phase/session:
Baseline full-pipeline run before Phase 4

Goal:
Use MacBook MPS to train and evaluate the U-Net baseline locally before moving
to Attention U-Net.

Files changed:

- `configs/unet_local_baseline.yaml`
- `src/training/trainer.py`
- `src/inference/predict.py`
- `AGENTS.md`
- `project-tasks.md`
- `DECISIONS.md`
- `handoff.md`

Commands run:

- `.venv/bin/python -c "import torch; ..."` for MPS diagnostics
- `ps -axo pid,command | grep 'src.training.train' | grep -v grep`
- `kill 77215`
- `.venv/bin/python -m pytest tests`
- `.venv/bin/python -c "from src.training.trainer import select_device; ..."`
- `.venv/bin/python -m src.training.train --config configs/unet_local_baseline.yaml`
- `.venv/bin/python -m src.evaluation.evaluate --config outputs/runs/unet_local_baseline/config.json --checkpoint outputs/runs/unet_local_baseline/best_model.pt --split val`
- `.venv/bin/python -m src.evaluation.evaluate --config outputs/runs/unet_local_baseline/config.json --checkpoint outputs/runs/unet_local_baseline/best_model.pt --split test`
- `.venv/bin/python scripts/make_report_figures.py --run-id unet_local_baseline --split val`
- `.venv/bin/python scripts/make_report_figures.py --run-id unet_local_baseline --split test`

Verification:

- Sandbox reported `mps_available=False`, but escalated execution reported
  `mps_available=True` and selected `mps`.
- Full local U-Net baseline completed 10 epochs on MPS.
- Best training-loop validation Dice was 0.9545 at epoch 8.
- Full evaluation val results: Dice 0.9598, IoU 0.9296, HD95 2.36 mm, HC MAE
  3.13 mm, HC RMSE 4.51 mm.
- Full evaluation internal-test results: Dice 0.9600, IoU 0.9261, HD95 3.02 mm,
  HC MAE 3.78 mm, HC RMSE 5.56 mm.
- Report figures generated under `outputs/figures/unet_local_baseline/`.

Decisions made:

- Local baseline training should request MPS with `mps: true`.
- Use `unet_local_baseline` as development baseline numbers before Phase 4.

Open issues:

- Larger CHPC/report-grade baseline config has not been run yet.
- Attention U-Net is not implemented yet.

Next exact task:

- Continue with `P4.S1` / Task `M2` - Implement Attention U-Net.

## Previous Session

Date: 2026-04-25

Task id: Phase 3 implementation - `I1`, `E1`

Phase/session:
`P3.S1`, `P3.S2`, `P3.S3`, `P3.S4`

Goal:
Implement deterministic inference geometry, prediction artifacts, evaluation
metrics, and report figure generation.

Files changed:

- `src/utils/geometry.py`
- `tests/test_geometry.py`
- `src/inference/predict.py`
- `src/inference/__init__.py`
- `src/evaluation/metrics.py`
- `src/evaluation/evaluate.py`
- `src/evaluation/__init__.py`
- `tests/test_metrics.py`
- `scripts/make_report_figures.py`
- `README.md`
- `project-tasks.md`
- `DECISIONS.md`
- `handoff.md`

Commands run:

- `.venv/bin/python -m pytest tests/test_geometry.py`
- `.venv/bin/python -m src.inference.predict --config outputs/runs/unet_baseline_smoke/config.json --checkpoint outputs/runs/unet_baseline_smoke/best_model.pt --split val --limit 2`
- `.venv/bin/python -m pytest tests/test_geometry.py tests/test_metrics.py`
- `.venv/bin/python -m src.evaluation.evaluate --config outputs/runs/unet_baseline_smoke/config.json --checkpoint outputs/runs/unet_baseline_smoke/best_model.pt --split val --limit 2`
- `.venv/bin/python scripts/make_report_figures.py --run-id unet_baseline_smoke --split val`
- `.venv/bin/python -m compileall src scripts`
- `.venv/bin/python -m pytest tests`
- `bash -n slurm/train_unet.sbatch`

Verification:

- Geometry tests passed.
- Metrics tests passed.
- Prediction artifacts were generated for two smoke validation samples.
- Evaluation wrote per-sample and aggregate metrics for the smoke checkpoint.
- Report figure script generated Dice histogram, HC error histogram, and a
  qualitative panel for the smoke checkpoint.
- Full local test suite passes: 15 tests.
- Python compile check passed.

Decisions made:

- HC measurement uses threshold -> largest connected component -> contour ->
  ellipse fit -> sampled ellipse circumference in physical mm.
- Smoke evaluation artifacts prove wiring only and must not be used as final
  report numbers.

Open issues:

- Full baseline U-Net training has not been run yet.
- Phase 4 Attention U-Net is not implemented yet.
- Final reported metrics need a real baseline checkpoint, not the smoke
  checkpoint.

Next exact task:

- Continue with `P4.S1` / Task `M2` - Implement Attention U-Net, or run the
  full U-Net baseline on CHPC before comparing models.

## Previous Session

Date: 2026-04-25

Task id: Phase 2 implementation - `M1`, `T1`, baseline `C1`

Phase/session:
`P2.S1`, `P2.S2`, `P2.S3`, `P2.S4`

Goal:
Implement the U-Net baseline, config-driven trainer, local smoke training, and
baseline CHPC Slurm script.

Files changed:

- `src/models/unet.py`
- `src/models/__init__.py`
- `tests/test_models.py`
- `src/training/losses.py`
- `src/training/optim.py`
- `src/training/trainer.py`
- `src/training/train.py`
- `src/training/__init__.py`
- `configs/unet_baseline.yaml`
- `configs/unet_smoke.yaml`
- `scripts/run_smoke_train.py`
- `slurm/train_unet.sbatch`
- `README.md`
- `project-tasks.md`
- `DECISIONS.md`
- `handoff.md`

Commands run:

- `.venv/bin/python -m pytest tests/test_models.py`
- `.venv/bin/python -m pytest tests/test_models.py tests/test_data.py`
- `.venv/bin/python scripts/run_smoke_train.py --config configs/unet_smoke.yaml`
- `bash -n slurm/train_unet.sbatch`

Verification:

- Model tests passed.
- Data + model tests passed: 7 tests.
- Smoke training completed on CPU and wrote `outputs/runs/unet_baseline_smoke`.
- Baseline Slurm script passed shell syntax check.

Decisions made:

- U-Net returns logits and does not apply sigmoid internally.
- Training uses BCE+Dice by default.
- `configs/unet_smoke.yaml` is for local smoke checks; `configs/unet_baseline.yaml`
  is for real baseline/CHPC runs.

Open issues:

- Full baseline training has not been run yet.
- Attention U-Net and evaluation Slurm scripts are still future tasks.

Next exact task:

- Continue with `P3.S1` / Task `I1` - Implement deterministic geometry
  utilities.

## Previous Session

Date: 2026-04-25

Task id: Environment, dataset, and initial git push setup

Phase/session:
Phase 1 completion support

Goal:
Create the uv virtual environment, unpack and inspect the local HC18 dataset,
generate splits/overlays, update governance docs, initialize git, and push the
initial repository to GitHub.

Files changed:

- `.gitignore`
- `AGENTS.md`
- `README.md`
- `DECISIONS.md`
- `docs/dataset-format.md`
- `project-tasks.md`
- `handoff.md`
- `configs/data.yaml`
- `src/data/dataset.py`
- `src/data/make_splits.py`
- `src/data/masks.py`
- `scripts/visualize_samples.py`
- `tests/test_data.py`

Commands run:

- `UV_CACHE_DIR=.uv-cache uv venv .venv`
- `UV_CACHE_DIR=.uv-cache uv pip install -r requirements.txt`
- `unzip -q /Users/shreyas/Downloads/1327317.zip -d data/raw/HC18`
- `unzip -q data/raw/HC18/training_set.zip -d data/raw/HC18`
- `unzip -q data/raw/HC18/test_set.zip -d data/raw/HC18`
- `.venv/bin/python -m pytest tests/test_data.py`
- `.venv/bin/python -m src.data.make_splits --config configs/data.yaml`
- `.venv/bin/python scripts/visualize_samples.py --config configs/data.yaml --n 10`
- `git init`
- `git branch -M main`
- `git remote add origin https://github.com/Endlesscrazz/Fetal-Head-Measurement.git`
- `git commit -m "Initial project scaffold"`
- `git push -u origin main`

Verification:

- uv environment created and dependencies installed.
- HC18 training discovery finds 999 labeled training records.
- Split generation produced train 698, val 152, test 149.
- Overlay generation produced 10 visual checks under
  `outputs/figures/data_overlays/`.
- `pytest` passes: 4 tests.
- Initial commit `e0ef61b` was pushed to GitHub on branch `main`.

Decisions made:

- Future sessions should use uv and `.venv/bin/python`.
- Keep HC18 raw data under `data/raw/HC18/` and ignored by git.
- Use training subset only for v1 split generation.
- Fill HC18 annotation contours for `target_type: filled`.

Open issues:

- The compatibility symlink from the old misspelled workspace path to the
  current project folder exists one level above the repo for tooling continuity.

Next exact task:

- Continue with `P2.S1` / Task `M1` - Implement U-Net Baseline.

## Previous Session

Date: 2026-04-25

Task id: Phase 1 implementation - `S1`, `D1`, `D2`, `D3`

Phase/session:
`P1.S1`, `P1.S2`, `P1.S3`, `P1.S4`

Goal:
Implement Phase 1 session-wise: project skeleton, dataset inspection notes,
dataset parser/mask generation, split creation script, and overlay script.

Files changed:

- `.gitignore`
- `Myproject.sh`
- `README.md`
- `requirements.txt`
- `configs/data.yaml`
- `docs/dataset-format.md`
- `src/__init__.py`
- `src/data/__init__.py`
- `src/data/dataset.py`
- `src/data/make_splits.py`
- `src/data/masks.py`
- `src/data/transforms.py`
- `src/evaluation/__init__.py`
- `src/inference/__init__.py`
- `src/models/__init__.py`
- `src/training/__init__.py`
- `src/utils/__init__.py`
- `scripts/visualize_samples.py`
- `tests/test_data.py`
- `project-tasks.md`
- `handoff.md`
- `DECISIONS.md`

Commands run:

- `find data/raw/HC18 -maxdepth 3 -type f | wc -l`
- `python3 -m compileall src scripts`
- `python3 -m pytest tests/test_data.py`
- direct synthetic data smoke check with `python3 -c ...`
- `python3 -m src.data.make_splits --config configs/data.yaml`
- `python3 scripts/visualize_samples.py --config configs/data.yaml --n 10`
- `find . -maxdepth 3 -type d | sort`
- `find . -maxdepth 3 -type f | sort`

Verification:

- `python3 -m compileall src scripts` passed.
- Direct synthetic data smoke check passed.
- `python3 -m pytest tests/test_data.py` could not run because `pytest` is not
  installed in the current Python environment.
- `make_splits` exits clearly because `data/raw/HC18/` has no HC18 images.
- `visualize_samples.py` exits clearly because no samples are available.

Decisions made:

- Support paired annotation images and explicit ellipse metadata as target
  sources, with annotation images preferred when present.
- Mark `D3` as blocked until the raw dataset is copied in, because real split
  files and overlays cannot be generated yet.

Open issues:

- HC18 raw data is not present under `data/raw/HC18/`.
- `pytest` is not installed in the current Python environment.
- Real dataset columns and annotation filenames still need validation once data
  is copied into the project.

Next exact task:

- Copy/place HC18 under `data/raw/HC18/`, then rerun `P1.S2` validation and
  unblock `P1.S4` by running split creation and overlay visualization.

## Previous Session

Date: 2026-04-25

Task id: G1 - V1 Phase and Session Roadmap

Phase/session:
Planning session for roadmap creation.

Goal:
Divide v1 into implementation phases and agent-sized sessions.

Files changed:

- `AGENTS.md`
- `project-tasks.md`
- `handoff.md`
- `DECISIONS.md`

Commands run:

- `sed -n '1,260p' AGENTS.md`
- `sed -n '1,260p' project-tasks.md`
- `sed -n '1,220p' handoff.md`
- `sed -n '1,240p' docs/project-spec.md`
- `sed -n '1,240p' docs/architecture.md`

Verification:

- Verified `project-tasks.md` contains `P1.S1`, Phase 1, and Phase 5 markers.
- Verified `AGENTS.md`, `project-tasks.md`, `handoff.md`, and `DECISIONS.md`
  reference the phase/session roadmap.
- Verified only one `DECISIONS.md` exists, at the repository root.

Decisions made:

- V1 is divided into five phases and session-sized implementation units.
- Next implementation session is `P1.S1 - Create project skeleton and
  local/CHPC-ready scaffolding`.

Open issues:

- Project source tree is not created yet.
- Dataset has not been inspected yet.
- The IDE may still show a stale tab for the deleted legacy handoff file; the
  repo now uses `handoff.md`.

Next exact task:

- `P1.S1` / Task `S1` - Create Project Skeleton.

## Previous Session

Date: 2026-04-25

Task id: G0 - Documentation and Governance Cleanup

Goal:
Implement documentation governance cleanup requested by the user.

Files changed:

- `AGENTS.md`
- `README.md`
- `project-tasks.md`
- `handoff.md`
- `DECISIONS.md`
- `docs/architecture.md`
- `docs/project-spec.md`

Commands run:

- `mkdir -p docs`
- `mv Agents.md AGENTS.md`
- `mv architecture.md docs/architecture.md`
- `mv project-spec.md docs/project-spec.md`

Verification:

- Verified root governance files exist: `AGENTS.md`, `README.md`,
  `project-tasks.md`, `handoff.md`, and `DECISIONS.md`.
- Verified long planning docs exist under `docs/`.
- Verified deleted legacy handoff filename has no remaining references.
- Verified `AGENTS.md` references `handoff.md` and `DECISIONS.md`.

Decisions made:

- Use root `AGENTS.md`, `project-tasks.md`, `handoff.md`, and `DECISIONS.md`
  as governance files.
- Move long planning docs into `docs/`.
- Use `Myproject.sh` rather than a notebook as the course runner.

Open issues:

- Project source tree is not created yet.
- Dataset has not been inspected yet.

Next exact task:

- Task S1 - Create Project Skeleton.
