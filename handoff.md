# Handoff

This file preserves session-to-session context for Codex agents.

Every meaningful session must update this file. Keep entries concise and
specific. The newest entry should be at the top.

## Current Status

- V1 is checkpointed on `main` with commit `2290315` and pushed to GitHub.
- V2 demo work is happening on branch `v2-demo`.
- V2 planning docs live under `docs/v2_demo/`.
- V2 direction is a saved-output Streamlit ML pipeline explorer first, with
  live inference as a later extension.
- Phase 1, Phase 2, and Phase 3 implementation are complete through local smoke
  verification.
- First full-pipeline local U-Net baseline run is complete using MPS:
  `unet_local_baseline`.
- Data split and run artifact behavior is documented in
  `docs/splits-runs-and-outputs.md`.
- `P4.S1` / Task `M2` is complete: Attention U-Net is implemented, registered,
  tested, and configured for local training.
- `P4.S2` local Attention U-Net run is complete:
  `attention_unet_local_baseline`.
- `P4.S3` local ablations are complete:
  `attention_unet_dice_loss` and `attention_unet_aug`.
- `P4.S4` post-processing ablation is complete for
  `attention_unet_local_baseline`.
- `P5.S1` local report comparison artifacts are complete under `report/`.
- `P5.S2` runner/README reproducibility work is complete.
- `P5.S3` report packaging aids are complete under `report/`.
- Detailed course ZIP guidance is documented in
  `docs/submission-packaging.md`.
- Initial final report draft exists at `report/final-report-draft.md`.
- Reviewable final report files exist at `report/final-report.md` and
  `report/final-report.pdf`; current PDF is 4 pages after review edits.
- Final course submission archive exists at
  `Fetal-Head-Measurement-final-submission.zip`.
- V1 now prioritizes completing the course report with local/reduced-resource
  runs first; CHPC full-scale reruns are post-v1 strengthening, not a blocker.
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

Date: 2026-04-28

Task id: `V2.P0` / `V2.P1`

Phase/session:
V1 checkpoint and V2 demo planning docs

Goal:
Commit the completed v1 course pipeline on `main`, push it, create `v2-demo`,
and add v2 planning docs/governance pointers for the portfolio demo.

Files changed:

- `.gitignore`
- `AGENTS.md`
- `project-tasks.md`
- `DECISIONS.md`
- `handoff.md`
- `docs/v2_demo/AGENTS.md`
- `docs/v2_demo/architecture.md`
- `docs/v2_demo/project-spec.md`
- `docs/v2_demo/roadmap.md`

Commands run:

- `bash Myproject.sh`
- `git status --short`
- `git status --ignored --short Fetal-Head-Measurement-final-submission.zip data/raw .venv .uv-cache outputs/runs outputs/tables`
- `git add ...`
- `git commit -m "Complete v1 course submission pipeline"`
- `git push`
- `git checkout -b v2-demo`
- `rg --files docs/v2_demo`
- `sed -n '1,220p' docs/v2_demo/AGENTS.md`
- `sed -n '1,220p' docs/v2_demo/architecture.md`
- `sed -n '1,220p' docs/v2_demo/project-spec.md`
- `sed -n '1,220p' docs/v2_demo/roadmap.md`
- `rg -n "v2_demo|V2|Streamlit|saved-output|not for clinical use" AGENTS.md project-tasks.md DECISIONS.md handoff.md docs/v2_demo`
- `git commit -m "Add v2 demo planning docs"`

Verification:

- V1 runner completed in report-only mode.
- Full test suite passed: 21 passed.
- Final Canvas ZIP, raw data, venv/cache files, checkpoints, and generated run
  artifacts were not staged for the v1 checkpoint.
- `main` pushed successfully to GitHub at commit `2290315`.
- `v2-demo` branch was created from the v1 checkpoint.
- V2 docs and root governance pointers were created and verified.

Decisions made:

- Keep final Canvas ZIP local and ignored.
- Use `v2-demo` for demo work.
- Use Streamlit as the preferred v2 demo framework.
- Build saved-output explorer first, then live inference through a later
  adapter.

Open issues:

- `context-bridge-log.md` remains untracked and was not committed.
- V2 implementation has not started; next task is sample/artifact curation.

Next exact task:

- Review `docs/v2_demo/` and then implement `V2.P2`: curated sample manifest
  and saved demo artifact plan.

## Previous Session

Date: 2026-04-26

Task id: Final submission ZIP packaging

Phase/session:
Submission packaging

Goal:
Create the final course ZIP with required code, report, configs, split files,
and report-result artifacts while excluding agent governance files, raw data,
virtual environments, caches, and model checkpoints.

Files changed:

- `Fetal-Head-Measurement-final-submission.zip`
- `handoff.md`

Commands run:

- `zip -r Fetal-Head-Measurement-final-submission.zip ...`
- `ls -lh Fetal-Head-Measurement-final-submission.zip`
- `zipinfo -1 Fetal-Head-Measurement-final-submission.zip | head -80`
- `zipinfo -1 Fetal-Head-Measurement-final-submission.zip | rg 'AGENTS|DECISIONS|handoff|project-tasks|docs/|data/raw|\.venv|\.uv-cache|best_model\.pt|\.pth|\.ckpt|report/.*\.md|report/.*\.tex'`
- `zipinfo -1 Fetal-Head-Measurement-final-submission.zip | wc -l`

Verification:

- Archive size is about 1.3 MB.
- Archive contains 703 entries.
- Required files are present, including `Myproject.sh`, `README.md`,
  `requirements.txt`, `configs/`, `src/`, `scripts/`, `tests/`,
  `data/splits/`, `report/final-report.pdf`, report figures/tables, and
  minimal output artifacts used by report-only reproduction.
- Forbidden-pattern scan returned no matches for agent governance files,
  `docs/`, raw data, virtualenv/cache files, checkpoints, or report source
  Markdown/LaTeX files.

Decisions made:

- Include `README.md` because it is a standard course/GitHub run guide, not an
  agent governance file.
- Exclude raw HC18 data and checkpoints from the submission ZIP to keep the
  archive lightweight and avoid redistributing dataset/model artifacts.

Open issues:

- Full retraining still requires placing HC18 under `data/raw/HC18/`.
- The packaged runner can reproduce/report from included artifacts; fresh
  training requires environment setup and dataset placement.

Next exact task:

- Submit `report/final-report.pdf` and
  `Fetal-Head-Measurement-final-submission.zip`, or request final packaging
  tweaks before submission.

## Previous Session

Date: 2026-04-26

Task id: Final report review edits

Phase/session:
Final PDF review

Goal:
Apply user-requested report edits: add teammate names, explain losses and
metrics, explain figures, keep post-processing table on one page, and prevent
post-processing figure from floating after references.

Files changed:

- `report/final-report.md`
- `report/final-report.pdf`
- `report/final-report.tex`
- `report/submission-checklist.md`
- `project-tasks.md`
- `handoff.md`

Commands run:

- `pandoc -s final-report.md -o final-report.tex -V geometry:margin=0.65in -V fontsize=10pt`
- `pdflatex -interaction=nonstopmode -halt-on-error final-report.tex`

Verification:

- PDF rebuilt successfully.
- LaTeX reported: `Output written on final-report.pdf (4 pages, 345562 bytes)`.
- Figure 2 from the previous version was removed to keep the report compact;
  the remaining figures are HC MAE by experiment and HC MAE by post-processing
  variant.

Decisions made:

- Remove the Dice bar-chart figure and keep the two figures most directly tied
  to the HC measurement objective.
- Use LaTeX `[H]` float placement for the remaining figures and post-processing
  table to keep them before the conclusion/references.

Open issues:

- User should review the updated 4-page PDF before final ZIP packaging.

Next exact task:

- Make any final report edits requested by the user, then assemble the course
  ZIP using `docs/submission-packaging.md`.

## Previous Session

Date: 2026-04-25

Task id: Generate final report for review

Phase/session:
Final PDF writing

Goal:
Create the final report Markdown and PDF from the draft for user review.

Files changed:

- `report/final-report.md`
- `report/final-report.pdf`
- `report/final-report.tex`
- `report/assets-index.md`
- `report/submission-checklist.md`
- `project-tasks.md`
- `handoff.md`

Commands run:

- `command -v pandoc`
- `command -v pdflatex`
- `pandoc report/final-report.md -o report/final-report.pdf --pdf-engine=pdflatex -V geometry:margin=0.65in -V fontsize=10pt`
- `pandoc final-report.md -o final-report.pdf --pdf-engine=pdflatex -V geometry:margin=0.65in -V fontsize=10pt`
- `pandoc -s final-report.md -o final-report.tex -V geometry:margin=0.65in -V fontsize=10pt`
- `pdflatex -interaction=nonstopmode -halt-on-error final-report.tex`

Verification:

- `report/final-report.pdf` compiled successfully.
- LaTeX reported: `Output written on final-report.pdf (5 pages, 347471 bytes)`.
- The report is below the 6-page maximum.

Decisions made:

- Use `report/final-report.md` as the clean final report source and
  `report/final-report.pdf` as the reviewable PDF.

Open issues:

- User should review the final PDF content and request edits before submission.
- Final code ZIP still needs to be assembled after report approval.

Next exact task:

- Review/edit `report/final-report.pdf`, then assemble the final course ZIP
  using `docs/submission-packaging.md`.

## Previous Session

Date: 2026-04-25

Task id: Final report draft

Phase/session:
Final PDF writing start

Goal:
Start the final course report by turning the report outline, checklist, and
saved result artifacts into a concise draft.

Files changed:

- `report/final-report-draft.md`
- `report/assets-index.md`
- `project-tasks.md`
- `handoff.md`

Commands run:

- `cat report/submission-checklist.md`
- `cat report/final-report-outline.md`
- `cat report/report-results-summary.md`
- `cat report/tables/main_test_results.md`
- `cat report/tables/postprocess_test_results.md`
- `wc -w report/final-report-draft.md`
- `sed -n '1,260p' report/final-report-draft.md`
- `cat report/assets-index.md`

Verification:

- Draft follows the checklist sections: introduction, method, experiments, and
  conclusions.
- Draft includes reduced-resource disclosure, internal-test results, ablations,
  post-processing ablation, and references.
- Draft is about 1,500 words before final PDF formatting.

Decisions made:

- Use `report/final-report-draft.md` as the source text for the final PDF.

Open issues:

- Final PDF formatting/export is not done yet.
- User should review wording, citations, and figure/table placement before PDF
  submission.

Next exact task:

- Convert/refine `report/final-report-draft.md` into the final PDF report,
  keeping it under 6 pages.

## Previous Session

Date: 2026-04-25

Task id: Documentation - course submission packaging guide

Phase/session:
Before final report writing / optional `P5.S4`

Goal:
Document exactly what to include in the course PDF and code ZIP, how to handle
saved artifacts, and what commands to use for packaging and verification.

Files changed:

- `docs/submission-packaging.md`
- `README.md`
- `report/submission-checklist.md`
- `handoff.md`

Commands run:

- `rg --files docs report | sort`
- `cat report/submission-checklist.md`
- `cat .gitignore`

Verification:

- Packaging guide exists under `docs/`.
- README and submission checklist point to the detailed guide.

Decisions made:

- Course ZIP guidance distinguishes lean GitHub contents from the richer course
  ZIP that may include saved `outputs/runs/` artifacts for fast report-only
  verification.

Open issues:

- Final PDF report text still needs to be written.
- CHPC full-scale reruns remain post-v1 optional strengthening.

Next exact task:

- Continue with final report writing from `report/final-report-outline.md`, or
  proceed to `P5.S4` CHPC workflow polish if report writing is handled outside
  Codex.

## Previous Session

Date: 2026-04-25

Task id: `P5.S3` - Package final report assets and submission checklist

Phase/session:
`P5.S3`

Goal:
Create final report-writing and course ZIP packaging aids from the generated
local v1 artifacts.

Files changed:

- `Myproject.sh`
- `README.md`
- `report/final-report-outline.md`
- `report/assets-index.md`
- `report/submission-checklist.md`
- `project-tasks.md`
- `DECISIONS.md`
- `handoff.md`

Commands run:

- `find report -maxdepth 2 -type f -print | sort`
- `rg -n "submission-checklist|final-report-outline|assets-index|report-only" README.md report/*.md`
- `bash -n Myproject.sh`
- `bash Myproject.sh`

Verification:

- `bash Myproject.sh` completed in default `report-only` mode.
- Report artifacts regenerated under `report/`.
- Full test suite passed during runner execution: `21 passed`.

Decisions made:

- Keep final report outline, report asset index, and submission checklist under
  `report/`.
- Default `Myproject.sh` report-only mode no longer requires `.pt` checkpoints;
  it requires saved configs/evaluation/prediction artifacts.

Open issues:

- Final PDF report text still needs to be written from the outline.
- CHPC full-scale reruns remain post-v1 optional strengthening.

Next exact task:

- Continue with final report writing from `report/final-report-outline.md`, or
  proceed to `P5.S4` CHPC workflow polish if the PDF text is handled outside
  Codex.

## Previous Session

Date: 2026-04-25

Task id: `P5.S2` - Finalize runner and README reproducibility commands

Phase/session:
`P5.S2`

Goal:
Make `Myproject.sh` and README usable for final local v1 verification and for
optional full local reruns.

Files changed:

- `Myproject.sh`
- `README.md`
- `project-tasks.md`
- `DECISIONS.md`
- `handoff.md`

Commands run:

- `bash -n Myproject.sh`
- `bash Myproject.sh --help`
- `rg -n "Myproject.sh|report-only|full-local|attention_unet_local_baseline|reduced-resource|CHPC" README.md`
- `bash Myproject.sh`
- `chmod +x Myproject.sh`

Verification:

- `bash Myproject.sh` completed in default `report-only` mode.
- Report artifacts regenerated under `report/`.
- Full test suite passed during runner execution: `21 passed`.

Decisions made:

- `Myproject.sh` defaults to `report-only` for fast course review and supports
  `--full-local` for retraining/evaluating all local v1 experiments.

Open issues:

- Final PDF report text still needs to be written.
- Final package/submission checklist remains.
- CHPC full-scale reruns remain post-v1 optional strengthening.

Next exact task:

- Continue with `P5.S3` - package final report assets and submission checklist,
  including a report-writing outline from generated artifacts.

## Previous Session

Date: 2026-04-25

Task id: `P5.S1` - Build local report comparison artifacts

Phase/session:
`P5.S1`

Goal:
Create reproducible report-ready tables, figures, and a concise results summary
from saved local v1 run artifacts.

Files changed:

- `scripts/build_report_artifacts.py`
- `report/report-results-summary.md`
- `report/tables/main_test_results.csv`
- `report/tables/main_test_results.md`
- `report/tables/attention_unet_ablation_test_results.csv`
- `report/tables/attention_unet_ablation_test_results.md`
- `report/tables/postprocess_test_results.csv`
- `report/tables/postprocess_test_results.md`
- `report/figures/main_test_hc_mae.png`
- `report/figures/main_test_dice.png`
- `report/figures/postprocess_test_hc_mae.png`
- `project-tasks.md`
- `DECISIONS.md`
- `handoff.md`

Commands run:

- `.venv/bin/python scripts/build_report_artifacts.py`
- `find report -maxdepth 3 -type f -print | sort`
- `cat report/report-results-summary.md`
- `cat report/tables/main_test_results.csv`
- `cat report/tables/postprocess_test_results.csv`
- `.venv/bin/python -m compileall scripts`
- `.venv/bin/python -m pytest tests`
- `.venv/bin/python -c "from pathlib import Path; from PIL import Image; ..."` to verify figure dimensions

Verification:

- Report artifacts generated under `report/`.
- Full test suite passed: `21 passed`.
- Report figures exist and are non-empty PNGs at 1440x720.
- Best local internal-test model by HC MAE remains
  `attention_unet_local_baseline`.

Decisions made:

- Use `scripts/build_report_artifacts.py` as the reproducible report artifact
  builder for local v1 and future CHPC refreshes.

Open issues:

- `Myproject.sh` and README reproducibility commands still need finalization.
- Final PDF report text still needs to be written using the generated artifacts.
- CHPC full-scale reruns remain post-v1 optional strengthening.

Next exact task:

- Continue with `P5.S2` - finalize `Myproject.sh` and README reproducibility
  commands.

## Previous Session

Date: 2026-04-25

Task id: `P4.S4` - Post-processing ablation

Phase/session:
`P4.S4`

Goal:
Quantify raw mask measurement versus cleaned/ellipse geometry for the best local
Attention U-Net run.

Files changed:

- `src/utils/geometry.py`
- `tests/test_geometry.py`
- `scripts/postprocess_ablation.py`
- `project-tasks.md`
- `DECISIONS.md`
- `handoff.md`

Run artifacts generated:

- `outputs/runs/attention_unet_local_baseline/evaluation/val/postprocess_ablation_per_sample.csv`
- `outputs/runs/attention_unet_local_baseline/evaluation/val/postprocess_ablation_aggregate.csv`
- `outputs/runs/attention_unet_local_baseline/evaluation/test/postprocess_ablation_per_sample.csv`
- `outputs/runs/attention_unet_local_baseline/evaluation/test/postprocess_ablation_aggregate.csv`
- `outputs/tables/attention_unet_local_baseline_val_postprocess_ablation.csv`
- `outputs/tables/attention_unet_local_baseline_test_postprocess_ablation.csv`
- `outputs/tables/local_postprocess_ablation_summary.csv`

Commands run:

- `.venv/bin/python -m pytest tests/test_geometry.py`
- `.venv/bin/python -m compileall src scripts`
- `.venv/bin/python scripts/postprocess_ablation.py --run-id attention_unet_local_baseline --split val`
- `.venv/bin/python scripts/postprocess_ablation.py --run-id attention_unet_local_baseline --split test`
- `.venv/bin/python -c "import pandas as pd; ..."` to combine val/test post-processing tables
- `.venv/bin/python -m pytest tests`

Verification:

- Geometry tests passed: `7 passed`.
- Full test suite passed: `21 passed`.
- Internal-test post-processing results:
  - raw all-contour HC MAE 16.73 mm, RMSE 21.27 mm;
  - cleaned contour HC MAE 14.04 mm, RMSE 16.18 mm;
  - cleaned ellipse HC MAE 3.37 mm, RMSE 4.68 mm.

Decisions made:

- Use cleaned ellipse fitting as the final HC measurement method.
- Use direct contour measurements only as ablation/report analysis.

Open issues:

- Phase 5 local report comparison artifacts and `Myproject.sh` remain.
- CHPC full-scale reruns remain post-v1 optional strengthening.

Next exact task:

- Continue with `P5.S1` - build local report comparison artifacts and report
  tables/figures from saved runs.

## Previous Session

Date: 2026-04-25

Task id: `P4.S3` - Local loss/augmentation ablations

Phase/session:
`P4.S3`

Goal:
Run focused local ablations for the report using the same split, image size,
architecture family, and training length as the Attention U-Net local baseline.

Files changed:

- `src/data/augmentations.py`
- `src/data/dataset.py`
- `src/training/trainer.py`
- `tests/test_data.py`
- `configs/attention_unet_dice_loss.yaml`
- `configs/attention_unet_aug.yaml`
- `scripts/compare_runs.py`
- `project-tasks.md`
- `DECISIONS.md`
- `handoff.md`

Run artifacts generated:

- `outputs/runs/attention_unet_dice_loss/`
- `outputs/runs/attention_unet_aug/`
- `outputs/figures/attention_unet_dice_loss/`
- `outputs/figures/attention_unet_aug/`
- `outputs/tables/attention_unet_dice_loss_val_summary.csv`
- `outputs/tables/attention_unet_dice_loss_test_summary.csv`
- `outputs/tables/attention_unet_aug_val_summary.csv`
- `outputs/tables/attention_unet_aug_test_summary.csv`
- `outputs/tables/local_ablation_summary.csv`

Commands run:

- `.venv/bin/python -m pytest tests/test_data.py tests/test_models.py`
- `.venv/bin/python -m compileall src`
- `.venv/bin/python -m src.training.train --config configs/attention_unet_dice_loss.yaml`
- `.venv/bin/python -m src.evaluation.evaluate --config outputs/runs/attention_unet_dice_loss/config.json --checkpoint outputs/runs/attention_unet_dice_loss/best_model.pt --split val`
- `.venv/bin/python -m src.evaluation.evaluate --config outputs/runs/attention_unet_dice_loss/config.json --checkpoint outputs/runs/attention_unet_dice_loss/best_model.pt --split test`
- `.venv/bin/python -m src.training.train --config configs/attention_unet_aug.yaml`
- `.venv/bin/python -m src.evaluation.evaluate --config outputs/runs/attention_unet_aug/config.json --checkpoint outputs/runs/attention_unet_aug/best_model.pt --split val`
- `.venv/bin/python -m src.evaluation.evaluate --config outputs/runs/attention_unet_aug/config.json --checkpoint outputs/runs/attention_unet_aug/best_model.pt --split test`
- `.venv/bin/python scripts/make_report_figures.py --run-id attention_unet_dice_loss --split val`
- `.venv/bin/python scripts/make_report_figures.py --run-id attention_unet_dice_loss --split test`
- `.venv/bin/python scripts/make_report_figures.py --run-id attention_unet_aug --split val`
- `.venv/bin/python scripts/make_report_figures.py --run-id attention_unet_aug --split test`
- `.venv/bin/python scripts/compare_runs.py --runs unet_local_baseline attention_unet_local_baseline attention_unet_dice_loss attention_unet_aug --splits val test --output outputs/tables/local_ablation_summary.csv`

Verification:

- Focused tests passed: `11 passed`.
- Dice-loss ablation completed 10 epochs on MPS.
- Dice-loss internal-test results: Dice 0.9615, IoU 0.9293, HD95 2.48 mm, HC
  MAE 3.45 mm, HC RMSE 5.13 mm.
- Augmentation ablation completed 10 epochs on MPS.
- Augmentation internal-test results: Dice 0.9606, IoU 0.9275, HD95 2.83 mm, HC
  MAE 3.72 mm, HC RMSE 5.85 mm.
- `outputs/tables/local_ablation_summary.csv` compares U-Net, Attention U-Net,
  Dice-only loss, and augmentation runs.

Decisions made:

- Keep Attention U-Net + BCE/Dice without augmentation as the best local v1
  model so far.

Open issues:

- Post-processing ablation `P4.S4` is not complete yet.
- `Myproject.sh` and report packaging still need finalization.

Next exact task:

- Continue with `P4.S4` - quantify raw mask vs cleaned/ellipse post-processing,
  then move into `P5.S1` local report comparison artifacts.

## Previous Session

Date: 2026-04-25

Task id: Governance update - local reduced-resource v1 report path

Phase/session:
Planning update before `P4.S3` / `P5`

Goal:
Align the project roadmap with the course instruction that allows reducing
image resolution and/or dataset size when compute is limited, so v1 can be
completed locally before optional CHPC full-scale reruns.

Files changed:

- `AGENTS.md`
- `project-tasks.md`
- `DECISIONS.md`
- `handoff.md`

Commands run:

- `sed -n '1,170p' project-tasks.md`
- `sed -n '170,270p' project-tasks.md`
- `tail -n 90 DECISIONS.md`
- `sed -n '1,120p' handoff.md`

Verification:

- `AGENTS.md` now allows clearly documented local/reduced-resource v1 results.
- `project-tasks.md` Phase 5 now prioritizes local report artifacts and runner
  packaging before CHPC full-scale reruns.
- `DECISIONS.md` records the local reduced-resource report path.

Decisions made:

- Complete v1 locally first using documented reduced-resource settings when
  needed; use CHPC later for full-scale reruns.

Open issues:

- Focused local ablations are not complete yet.
- `Myproject.sh` and report packaging still need finalization.

Next exact task:

- Continue with `P4.S3` using local-friendly ablations, then move into `P5.S1`
  local report comparison artifacts.

## Previous Session

Date: 2026-04-25

Task id: `P4.S2` - Train Attention U-Net on the same split

Phase/session:
`P4.S2`

Goal:
Train Attention U-Net with the same local full-split setup as the U-Net
baseline, then evaluate val and internal-test splits.

Files changed:

- `project-tasks.md`
- `handoff.md`
- `DECISIONS.md`

Run artifacts generated:

- `outputs/runs/attention_unet_local_baseline/config.json`
- `outputs/runs/attention_unet_local_baseline/metrics.csv`
- `outputs/runs/attention_unet_local_baseline/best_model.pt`
- `outputs/runs/attention_unet_local_baseline/predictions/val/`
- `outputs/runs/attention_unet_local_baseline/predictions/test/`
- `outputs/runs/attention_unet_local_baseline/evaluation/val/`
- `outputs/runs/attention_unet_local_baseline/evaluation/test/`
- `outputs/figures/attention_unet_local_baseline/`
- `outputs/tables/attention_unet_local_baseline_val_summary.csv`
- `outputs/tables/attention_unet_local_baseline_test_summary.csv`

Commands run:

- `.venv/bin/python -m src.training.train --config configs/attention_unet.yaml`
- `.venv/bin/python -m src.evaluation.evaluate --config outputs/runs/attention_unet_local_baseline/config.json --checkpoint outputs/runs/attention_unet_local_baseline/best_model.pt --split val`
- `.venv/bin/python -m src.evaluation.evaluate --config outputs/runs/attention_unet_local_baseline/config.json --checkpoint outputs/runs/attention_unet_local_baseline/best_model.pt --split test`
- `.venv/bin/python scripts/make_report_figures.py --run-id attention_unet_local_baseline --split val`
- `.venv/bin/python scripts/make_report_figures.py --run-id attention_unet_local_baseline --split test`

Verification:

- Training completed 10 epochs on MPS.
- Best training-loop validation Dice was 0.9589 at epoch 10.
- Full evaluation val results: Dice 0.9631, IoU 0.9356, HD95 2.05 mm, HC MAE
  2.74 mm, HC RMSE 4.30 mm.
- Full evaluation internal-test results: Dice 0.9669, IoU 0.9373, HD95 2.38 mm,
  HC MAE 3.37 mm, HC RMSE 4.68 mm.
- Report figures generated under `outputs/figures/attention_unet_local_baseline/`.

Decisions made:

- Use `attention_unet_local_baseline` as the first local development comparison
  against `unet_local_baseline`.

Open issues:

- Loss/augmentation/post-processing ablations are not implemented yet.
- Larger CHPC/report-grade configs have not been run yet.

Next exact task:

- Continue with `P4.S3` - run focused loss/augmentation ablations, or create a
  concise comparison table between `unet_local_baseline` and
  `attention_unet_local_baseline` first.

## Previous Session

Date: 2026-04-25

Task id: `M2` - Implement Attention U-Net

Phase/session:
`P4.S1`

Goal:
Implement Attention U-Net as the main improved model with the same tensor
contract as U-Net and make it selectable by config name.

Files changed:

- `src/models/attention_unet.py`
- `src/models/__init__.py`
- `tests/test_models.py`
- `configs/attention_unet.yaml`
- `project-tasks.md`
- `handoff.md`
- `DECISIONS.md`

Commands run:

- `rg -n "Task M2|P4.S1|Attention" project-tasks.md`
- `sed -n '1,260p' src/models/unet.py`
- `sed -n '1,220p' src/models/__init__.py`
- `sed -n '1,220p' tests/test_models.py`
- `sed -n '520,590p' project-tasks.md`
- `.venv/bin/python -m pytest tests/test_models.py`
- `tail -n 120 DECISIONS.md`

Verification:

- Model tests passed: `6 passed`.
- Attention U-Net forward pass preserves `[B, 1, H, W] -> [B, 1, H, W]` for
  regular and odd input sizes.
- Registry builds `attention_unet` successfully.

Decisions made:

- Attention U-Net uses additive attention gates on decoder skip connections,
  while reusing the existing U-Net convolution/downsampling blocks.

Open issues:

- Attention U-Net has not been trained yet.
- Larger CHPC/report-grade baseline config has not been run yet.

Next exact task:

- Continue with `P4.S2` - Train Attention U-Net on the same split using
  `configs/attention_unet.yaml`, then evaluate `val` and internal `test`.

## Previous Session

Date: 2026-04-25

Task id: Documentation - split and run output explainer

Phase/session:
Baseline review before Phase 4

Goal:
Explain why `outputs/runs/<run_id>/` contains separate `predictions/` and
`evaluation/` folders, which split each subfolder uses, how leakage is
controlled, and how configs should be changed for future model experiments.

Files changed:

- `docs/splits-runs-and-outputs.md`
- `handoff.md`

Commands run:

- `sed -n '1,220p' AGENTS.md`
- `sed -n '1,220p' project-tasks.md`
- `sed -n '1,220p' handoff.md`
- `sed -n '1,180p' DECISIONS.md`
- `rg --files docs`
- `find outputs/runs/unet_local_baseline -maxdepth 3 -type f | sort`
- `find outputs/runs/unet_local_baseline -maxdepth 4 -type d | sort`
- `find data/splits -maxdepth 1 -type f -print | sort`
- `sed -n '1,140p' configs/unet_smoke.yaml`
- `sed -n '1,140p' configs/unet_baseline.yaml`

Verification:

- Confirmed `unet_local_baseline` contains `config.json`, `metrics.csv`,
  `best_model.pt`, `predictions/{val,test}/`, and `evaluation/{val,test}/`.
- Confirmed split files exist under `data/splits/`.
- Added documentation explaining train/val/internal-test usage and config-driven
  experiment changes.

Decisions made:

- None; documentation clarifies existing behavior.

Open issues:

- Attention U-Net is not implemented yet.
- Larger CHPC/report-grade baseline config has not been run yet.

Next exact task:

- Continue with `P4.S1` / Task `M2` - Implement Attention U-Net.

## Previous Session

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
