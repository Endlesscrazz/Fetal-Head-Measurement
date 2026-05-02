# V2 Demo Session Task Plan

This file breaks the v2 roadmap into implementation sessions. It is the
session-level queue for the v2 demo; the root `project-tasks.md` remains the
repository-wide task index.

Agents should complete one session at a time unless the user explicitly expands
scope. Every session must end with verification and a root `handoff.md` update.

Task status values:

- `todo`
- `in_progress`
- `blocked`
- `done`

## Session Order

Critical path for the resume/LinkedIn MVP:

1. `V2.S0` - Create this session task plan. (done)
2. `V2.S1` - Curate demo sample set.
3. `V2.S2` - Export demo artifacts and validate manifest (includes prob.png via checkpoint).
4. `V2.S3` - React app scaffold and data layer.
5. `V2.S4` - React pipeline explorer (core UI — gallery, stepper, threshold).
6. `V2.S5` - Geometry panel, metrics, and experiment dashboard with real data.
7. `V2.S6` - Build, deploy to Vercel/GitHub Pages, and portfolio polish.

Post-MVP:

1. `V2.S7` - Optional live inference FastAPI backend.
2. `V2.S8` - Optional HC18 challenge exporter.

Frontend: Vite + React + TypeScript. No Streamlit. No backend for MVP.
Design reference: `docs/v2_demo/frontend-design-handoff.md`

Planning note:
Sessions `V2.S2` through `V2.S4` were previously completed for a Streamlit
prototype. The Claude Design pivot supersedes that path. Current work resumes
at `V2.S2` as a React artifact-contract revision, using the already-curated
sample list rather than the design prototype's placeholder sample IDs.

## V2.S0 - Session Plan

Status: done

Roadmap phase:
`V2.P1` planning refinement

Goal:
Create a session-sized execution plan for the v2 demo before implementation
starts.

Outcome:
Future agents can pick a single v2 session with clear outcomes, expected files,
subtasks, and verification.

Expected files:

- `docs/v2_demo/project-tasks.md`
- `docs/v2_demo/roadmap.md`
- root `handoff.md`

Subtasks:

- Review root `AGENTS.md`, root `project-tasks.md`, root `handoff.md`, and all
  `docs/v2_demo/` files.
- Convert roadmap phases into one-session units.
- Preserve the saved-output-first MVP as the critical path.
- Keep live inference and HC18 challenge export clearly post-MVP.

Verification:

- `test -f docs/v2_demo/project-tasks.md`
- `rg -n "V2.S1|V2.S2|V2.S6|V2.S7|V2.S8" docs/v2_demo/project-tasks.md`
- `git diff --check`

Done criteria:

- session plan exists,
- next exact session is unambiguous,
- no implementation code is added.

## V2.S1 - Curate Demo Sample Set

Status: done

Roadmap phase:
`V2.P2`

Target window:
Week of 2026-05-05

Estimated effort:
1-2 hours

Goal:
Choose the small set of samples that will make the demo educational and
interview-friendly.

Outcome:
A documented curated sample list exists before artifact export starts.

Expected files:

- `docs/v2_demo/curated-samples.md`
- `docs/v2_demo/curated-samples.json`
- root `handoff.md`

Allowed implementation files:

- `docs/v2_demo/curated-samples.md`
- `docs/v2_demo/curated-samples.json`
- root `handoff.md`

Subtasks:

- Inspect `outputs/runs/attention_unet_local_baseline/evaluation/test/per_sample_metrics.csv`.
- Inspect `outputs/runs/attention_unet_local_baseline/predictions/test/predictions.csv`.
- Pick at least five internal-test samples:
  - two strong predictions,
  - one typical/median case,
  - one high-HC-error case,
  - one visibly instructive cleanup or ellipse case.
- Record sample id, category, reason for inclusion, Dice, HC error, and source
  run/split.
- Write `docs/v2_demo/curated-samples.json` as the machine-readable input for
  artifact export. The Markdown file is human rationale only and must not be
  parsed by exporter code.
- Confirm selected samples have prediction rows, raw masks, cleaned masks, and
  overlays available.

Verification:

- `test -f docs/v2_demo/curated-samples.md`
- `test -f docs/v2_demo/curated-samples.json`
- `rg -n "strong|typical|high-error|cleanup|ellipse" docs/v2_demo/curated-samples.md`
- `.venv/bin/python -m json.tool docs/v2_demo/curated-samples.json`
- For each selected sample, verify paths exist under
  `outputs/runs/attention_unet_local_baseline/predictions/test/`.

Done criteria:

- selected samples cover success and failure modes,
- sample rationale is clear enough to drive app labels,
- no raw data, checkpoints, or generated demo artifacts are committed.

## V2.S2 - Export Demo Artifacts And Validate Manifest

Status: done

Status note:
The original Streamlit export session completed, but it produced schema version
1 files (`image.png`, `target_mask.png`, `raw_mask.png`, `cleaned_mask.png`,
`ellipse_overlay.png`) and no `prob.png`. This session revises that existing
work to the React schema version 2 contract.

Roadmap phase:
`V2.P2.5`

Target window:
Week of 2026-05-05

Estimated effort:
4-6 hours (increased from 3-5 — now includes checkpoint inference for prob.png)

Goal:
Create the complete saved-output artifact bundle required by the React frontend.
This session REQUIRES the checkpoint and raw HC18 data locally. After this
session the React app runs without either.

Outcome:
`outputs/demo_samples/manifest.json` and all per-sample assets exist, pass
validation, and match the React frontend's expected file names and manifest schema.

IMPORTANT — Required reading before this session:
`docs/v2_demo/frontend-design-handoff.md` Sections 4 and 10 (full list of what
the frontend needs and the exact filenames it expects).

Expected files:

- `scripts/export_demo_artifacts.py`
- `scripts/validate_demo_manifest.py`
- `tests/test_demo_manifest.py` (if validation logic is factored for testing)
- `outputs/demo_samples/manifest.json` (schema version 2 from architecture.md)
- `outputs/demo_samples/<sample_id>/ultrasound.png`   ← exact name required by frontend
- `outputs/demo_samples/<sample_id>/target.png`       ← exact name required by frontend
- `outputs/demo_samples/<sample_id>/pred.png`         ← exact name (cleaned binary mask)
- `outputs/demo_samples/<sample_id>/prob.png`         ← exact name, RAW probability map
- `outputs/demo_samples/<sample_id>/metadata.json`
- root `handoff.md`

Subtasks:

- Before starting: confirm prerequisites are present locally:
  `test -d data/raw/HC18/training_set && test -f outputs/runs/attention_unet_local_baseline/best_model.pt`
- Read curated sample IDs from `docs/v2_demo/curated-samples.json`.
  Confirm all selected IDs exist in `outputs/runs/attention_unet_local_baseline/evaluation/test/per_sample_metrics.csv`.
  At least two IDs must have genuine failure behavior (high HC error or low Dice)
  from the real metrics, not from the design's placeholder values. The current
  curated sample set is authoritative: do not replace it with the handoff's
  placeholder IDs unless the user explicitly asks.
- For each selected sample:
  a. Copy original image from `data/raw/HC18/training_set/<id>.png` →
     `outputs/demo_samples/<id>/ultrasound.png`
  b. Generate annotation-derived target mask using v1 mask utilities →
     `outputs/demo_samples/<id>/target.png`
  c. Copy cleaned binary prediction from
     `outputs/runs/attention_unet_local_baseline/predictions/test/masks/<id>_cleaned.png` →
     `outputs/demo_samples/<id>/pred.png`
  d. Load `best_model.pt`, run forward pass, apply sigmoid (NO threshold),
     save sigmoid output as uint8 grayscale PNG →
     `outputs/demo_samples/<id>/prob.png`
     (pixel value = round(sigmoid_value * 255))
  e. Compute `contourHC` in mm from cleaned mask using `src/utils/geometry.py`.
  f. Compute `confidence` = mean(prob_map[cleaned_mask == 1]) from prob.png.
  g. Parse `predEllipse` from `predictions.csv` — convert `ellipse_angle_deg`
     to radians for the `rot` field.
  h. Write `outputs/demo_samples/<id>/metadata.json` with all numeric fields.
- Write `outputs/demo_samples/manifest.json` using schema version 2 from
  `docs/v2_demo/architecture.md` Section 6. Include all fields from the
  TypeScript `Sample` interface.
- Validate manifest: all paths exist, all numeric fields are non-null floats,
  at least one 'strong' and one 'failure' sample are present, safety_text is present.
- Keep generated artifacts local. Do not commit PNGs or metadata.json.

Verification:

- `test -d data/raw/HC18/training_set`
- `.venv/bin/python scripts/export_demo_artifacts.py --run-id attention_unet_local_baseline --split test`
- `.venv/bin/python scripts/validate_demo_manifest.py --manifest outputs/demo_samples/manifest.json`
- `.venv/bin/python -m pytest tests/test_demo_manifest.py` if the test file is added
- `rg -n "Educational demo only. Not for clinical use." outputs/demo_samples/manifest.json`
- `rg -n "contourHC|confidence|predEllipse" outputs/demo_samples/manifest.json`
- Manually confirm at least one exported sample directory contains all required
  PNGs plus `metadata.json`.

Done criteria:

- manifest validation passes,
- at least five curated samples export successfully,
- exported manifest includes non-null `contourHC` when contour measurement
  succeeds,
- raw HC18 was required only for export and is not required by later saved-output
  app sessions,
- default future app mode can load from `outputs/demo_samples/` without raw HC18
  or checkpoints,
- root `handoff.md` records whether generated artifacts were left untracked.

## V2.S3 - React App Scaffold And Data Layer

Status: done

Roadmap phase:
`V2.P3`

Target window:
Week of 2026-05-12

Estimated effort:
2-3 hours

Goal:
Scaffold the Vite + React + TypeScript project, port design tokens, define the
TypeScript `Sample` interface, and wire the manifest loader before building any
UI panels.

Outcome:
`npm run dev` works, the design token CSS is active, and `manifest.json` can be
loaded into typed `Sample` objects in the browser.

Required reading before this session:
`docs/v2_demo/frontend-design-handoff.md` (full document)

Expected files:

- `frontend/package.json`
- `frontend/vite.config.ts`
- `frontend/tsconfig.json`
- `frontend/index.html`
- `frontend/src/styles.css` (ported from design handoff `styles.css`)
- `frontend/src/types/sample.ts`
- `frontend/src/data/stages.ts` (ported from handoff `data.js` STAGES)
- `frontend/src/data/metric-copy.ts` (ported from handoff `data.js` METRIC_COPY)
- `frontend/src/data/samples.ts` (fetches/imports `manifest.json`)
- `frontend/src/App.tsx` (shell only — no components yet)
- `frontend/src/main.tsx`
- `frontend/public/samples/` (copy of `outputs/demo_samples/` contents)
- `.gitignore` additions: `frontend/node_modules/`, `frontend/dist/`,
  `frontend/public/samples/`
- root `handoff.md`

Allowed implementation files:
`frontend/` tree, `.gitignore`, root `handoff.md`

Subtasks:

- `npm create vite@latest frontend -- --template react-ts`
- Install no additional dependencies beyond what Vite + React + TypeScript provide.
  The design uses no third-party UI library.
- Port `styles.css` from the design handoff into `frontend/src/styles.css`,
  applying the documented project corrections such as normalizing negative
  letter-spacing to `0`. Import it in `main.tsx`. Verify CSS custom properties
  resolve in the browser.
- Port the TypeScript `Sample` interface from `docs/v2_demo/architecture.md`
  Section 5 into `frontend/src/types/sample.ts`.
- Port `STAGES` array from `data.js` into `frontend/src/data/stages.ts`.
- Port `METRIC_COPY` object from `data.js` into `frontend/src/data/metric-copy.ts`.
- Implement `frontend/src/data/samples.ts` — fetch `/samples/manifest.json` at
  runtime (or import at build time via `?url` and `fetch`).
- Add `frontend/public/samples/` to `.gitignore`.
- Copy `outputs/demo_samples/` contents into `frontend/public/samples/` and confirm
  the manifest loads in the browser.
- Render a plain `<pre>{JSON.stringify(samples[0], null, 2)}</pre>` in `App.tsx`
  to confirm the data pipeline works end to end.

Verification:

- `cd frontend && npm install && npm run dev` — dev server starts.
- Open `localhost:5173` — page loads, background gradient visible (from `app-bg`
  class in styles.css).
- `fetch('/samples/manifest.json')` resolves with correct sample count.
- `cd frontend && npm run build` — build succeeds with no TypeScript errors.

Done criteria:

- dev server runs and the design background is visible,
- `Sample` type compiles with no errors,
- manifest loads into typed objects in the browser,
- `frontend/public/samples/` is gitignored.

## V2.S4 - React Pipeline Explorer (Core UI)

Status: done

Roadmap phase:
`V2.P3`

Target window:
Week of 2026-05-12

Estimated effort:
6-8 hours

Goal:
Port the core UI components from the design handoff and wire them to real data.

Outcome:
A viewer can pick a sample, step through the pipeline, drag the threshold slider,
and see real ultrasound images and masks — all from a local `npm run dev`.

Required reading before this session:
`docs/v2_demo/frontend-design-handoff.md` Sections 3, 4, 7 (interactions checklist)

Expected files:

- `frontend/src/App.tsx` (full, with all state and section wiring)
- `frontend/src/components/nav/StickyNav.tsx`
- `frontend/src/components/nav/TourBar.tsx`
- `frontend/src/components/hero/Hero.tsx`
- `frontend/src/components/gallery/SampleGallery.tsx`
- `frontend/src/components/pipeline/PipelineStepper.tsx`
- `frontend/src/components/pipeline/StageDetail.tsx`
- `frontend/src/components/threshold/ThresholdViewer.tsx`
- `frontend/src/components/shared/SafetyChip.tsx`
- `frontend/src/components/shared/CategoryBadge.tsx`
- root `handoff.md`

Allowed implementation files:
`frontend/src/` tree, root `handoff.md`

Subtasks:

- Port components from the design handoff JSX to TypeScript. Follow the file
  mapping in `docs/v2_demo/frontend-design-handoff.md` Section 3 exactly.
- Wire `App.tsx` state: `activeId`, `filter`, `stageIdx`, `activeSection`,
  `tourActive`, `tourStep`. These are the same six top-level states from `app.jsx`.
- Implement `SafetyChip` first — it is non-negotiable and must be visible at all
  times. Fixed bottom-right, `z-index: 50`.
- Port `ThresholdViewer` with full canvas logic. Keep the exact pixel-level
  soft-edge blend from `threshold.jsx`. This is the hero interaction — do not
  simplify it.
- Use real `sample.id` to construct image paths: `/samples/${id}/ultrasound.png`,
  `/samples/${id}/prob.png`, etc.
- Replace `category: 'edge'` with `cat: 'failure'` throughout. Update filter tab
  label to "Failure".
- Preserve pipeline auto-advance `useEffect` (3 stages × 220 ms on `activeId` change).
- Preserve `IntersectionObserver` scrollspy with `rootMargin: '-20% 0px -60% 0px'`.
- Add `scroll-margin-top: 80px` to every section element.

Verification:

- `npm run dev` — app loads with real sample images.
- Click a sample card — pipeline stepper auto-advances through stages 0→2.
- Drag threshold slider — canvas updates in real time with cyan mask overlay.
- Toggle "Show P(skull) heat" — heatmap mode activates.
- Scrollspy — sticky nav active pill updates correctly while scrolling.
- `npm run build` — TypeScript build passes with no errors.
- SafetyChip is visible at all scroll positions.

Done criteria:

- all five core components render with real data,
- threshold slider works end-to-end with real `prob.png`,
- safety chip is always visible,
- no TypeScript errors on build.

## V2.S5 - Geometry Panel, Metrics, And Experiment Dashboard

Status: todo

Roadmap phase:
`V2.P3`

Target window:
Week of 2026-05-19

Estimated effort:
4-6 hours

Goal:
Port the remaining sections: ContourEllipse comparison, MetricsPanel, and
ExperimentDashboard — with real v1 data replacing all placeholders.

Outcome:
The full page is complete with all six sections showing real data and the
experiment dashboard reflecting the actual v1 runs.

Required reading before this session:
`docs/v2_demo/frontend-design-handoff.md` Section 4.2 (experiment corrections)

Expected files:

- `frontend/src/components/geometry/ContourEllipse.tsx`
- `frontend/src/components/metrics/MetricsPanel.tsx`
- `frontend/src/components/experiments/ExperimentDashboard.tsx`
- `frontend/public/experiments/` (optional — if serving run metrics as static JSON)
- root `handoff.md`

Allowed implementation files:
`frontend/src/` tree, `frontend/public/experiments/`, root `handoff.md`

Subtasks:

- Port `ContourEllipse` from `insight.jsx`. Use `sample.predEllipse` and
  `sample.contourHC` from the manifest. Keep Contour/Ellipse/Both/Morph toggles.
- Port `MetricsPanel` with `ArcMetric` (Dice, IoU) and `ScaleMetric` (HC error,
  HD95) from `insight.jsx`. Use `METRIC_COPY` interpret functions verbatim.
- Port `ExperimentDashboard`. Replace the three design runs with real v1 runs:
  - `unet_local_baseline` (U-Net, baseline)
  - `attention_unet_local_baseline` (Attention U-Net, best)
  - `attention_unet_aug` (Attn U-Net + Aug)
- Load real sparkline data from `outputs/runs/*/metrics.csv` (`val_dice` column).
  Serve these as static JSON under `frontend/public/experiments/` or import at
  build time. Do not use the synthetic `makeCurve` function.
- Replace the augmentation ablation table with real data from
  `outputs/tables/local_ablation_summary.csv`. Keep the horizontal bar chart style.
- Add a post-processing ablation section using
  `outputs/tables/local_postprocess_ablation_summary.csv`.
- Add disclaimer: "Local training: 10 epochs, 256×384, base channels 16."
- Keep the contour-vs-ellipse HC comparison panel visible. If `contourHC` is null
  for a sample, show "—" rather than hiding the row.

Verification:

- `npm run dev` — full page loads with all six sections.
- ContourEllipse morph slider animates between contour and ellipse paths.
- Metrics panel arc gauges color correctly (green/cyan/amber by threshold).
- Experiment dashboard shows three real run cards with real sparklines.
- Augmentation ablation bar chart shows real progression.
- `npm run build` — build succeeds.

Done criteria:

- all six page sections are complete and show real data,
- experiment dashboard shows only runs that actually exist in `outputs/runs/`,
- no synthetic data remains in any component.

## V2.S6 - Build, Deploy, And Portfolio Polish

Status: todo

Roadmap phase:
`V2.P5`

Target window:
Week of 2026-05-19

Estimated effort:
3-4 hours

Goal:
Ship the demo to a public URL, write the README, and create the start script so
the project reads as a polished portfolio artifact.

Outcome:
The demo is live at a public URL. A reviewer can understand the project in under
one minute from the GitHub repo page.

Expected files:

- `README.md` (v2 demo section)
- `start_demo.sh` (wraps npm install + copy artifacts + npm run dev)
- `vercel.json` or `.github/workflows/deploy.yml` (deployment config)
- screenshot/GIF assets under `docs/screenshots/` (only if user approves committing)
- root `handoff.md`

Allowed implementation files:
`README.md`, `start_demo.sh`, `vercel.json` or deploy workflow,
`docs/screenshots/` (if approved), root `handoff.md`

Subtasks:

- Deploy to Vercel (preferred) or GitHub Pages:
  - Vercel: connect repo, set build command `cd frontend && npm run build`,
    output dir `frontend/dist`. Add `vercel.json` at repo root if needed.
  - GitHub Pages: use `gh-pages` action or `peaceiris/actions-gh-pages`.
  - The deployment must NOT include `frontend/public/samples/` (medical images).
    Ship the app with placeholder sample paths; add a README note that local
    artifact export is required to see real data.
- Write the `README.md` v2 demo section:
  - One-line description of what the demo shows.
  - Live URL (once deployed).
  - Local run instructions (for reviewers who have HC18 data).
  - Screenshot or GIF (if approved and committed).
  - Safety language: "Educational demo only. Not for clinical use."
- Write `start_demo.sh`:
  ```bash
  #!/usr/bin/env bash
  set -e
  python scripts/export_demo_artifacts.py --run-id attention_unet_local_baseline --split test
  cp -r outputs/demo_samples/* frontend/public/samples/
  cd frontend && npm install && npm run dev
  ```
- Confirm `frontend/public/samples/` is in `.gitignore`.
- Record the public URL in `handoff.md` and `DECISIONS.md`.

Verification:

- `bash start_demo.sh` runs from a clean shell after export artifacts exist.
- Public URL loads the app with placeholder images.
- README renders correctly on GitHub.
- `git status` confirms no medical image artifacts are staged.

Done criteria:

- public URL is live and loads the app,
- README explains the demo and gives the live URL,
- `start_demo.sh` works for local reviewers who have HC18 data,
- no medical images are committed or deployed.

## V2.S7 - Optional Live Inference FastAPI Backend

Status: todo

Roadmap phase:
`V2.P4`

Target window:
Post-MVP, after `V2.S6`

Estimated effort:
6-10 hours

Goal:
Add an optional FastAPI backend that serves live checkpoint inference to the
React frontend without disturbing the static saved-output mode.

Outcome:
A "Live mode" toggle in the app sends an image to the backend and receives
real-time predictions matching the `Sample` interface.

Expected files:

- `backend/main.py` (FastAPI app)
- `backend/inference.py` (wraps v1 model + geometry utilities)
- `backend/requirements.txt`
- `frontend/src/data/live-adapter.ts`
- `frontend/src/components/shared/ModeSelector.tsx`
- README/docs updates for backend mode
- root `handoff.md`

Subtasks:

- FastAPI endpoint: `POST /predict` — accepts an image upload or sample ID,
  returns JSON matching the `Sample` interface (excluding image paths, including
  computed `predEllipse`, `contourHC`, `confidence`, `metrics`).
- Reuse `src/models/`, `src/inference/predict.py`, `src/utils/geometry.py` from v1.
- Frontend: detect backend availability (health check); fall back to static mode
  if backend is not running.
- Keep uploaded arbitrary public medical images out of scope unless explicitly
  approved.

Done criteria:

- live inference works on at least one local sample,
- static saved-output mode still works when backend is not running,
- no retraining occurs from the web UI.

## V2.S8 - Optional HC18 Challenge Exporter

Status: todo

Roadmap phase:
`V2.P6`

Target window:
Post-MVP, after `V2.S6`

Estimated effort:
4-6 hours

Goal:
Add learning-oriented official-test CSV export tooling without changing the demo
MVP.

Outcome:
The project can produce a challenge-style prediction CSV for the unlabeled HC18
test set.

Expected files:

- challenge export script under `scripts/`
- validation helper or tests
- README/docs update for challenge export
- root `handoff.md`

Subtasks:

- Confirm required official HC18 submission columns and units before coding.
- Run inference over `data/raw/HC18/test_set/` using a local checkpoint.
- Export ellipse and/or HC fields in the required format.
- Validate row count, filenames, missing values, and units.
- Clearly document that official labels are not assumed.

Verification:

- Export command completes locally on the official test set.
- Validation command confirms expected columns and row count.
- Saved-output React mode still works.

Done criteria:

- generated CSV is structurally valid,
- no official test labels are required,
- challenge export remains optional and separate from v2 MVP.

## MVP Exit Checklist

The v2 MVP is complete when sessions `V2.S1` through `V2.S6` are done and:

- `npm run dev` inside `frontend/` launches the app at `localhost:5173`,
- the app is deployed to a public URL (Vercel or GitHub Pages),
- a user can select a sample from the visual card gallery,
- the app shows original ultrasound, target mask, CNN prediction, threshold slider,
  cleaned mask, ellipse overlay, and HC measurement in mm,
- the threshold slider re-thresholds `prob.png` in canvas in real time,
- the contour-vs-ellipse comparison panel shows real `contourHC` values,
- the metrics panel shows arc gauges with color-coded Dice and IoU,
- the experiment dashboard shows the three real v1 runs (not U-Net++),
- training sparklines show real `val_dice` from `outputs/runs/*/metrics.csv`,
- the SafetyChip is always visible ("Educational demo · Not for clinical use"),
- the guided tour works end-to-end through all six sections,
- `npm run build` produces no TypeScript errors,
- no medical image artifacts are committed to the repository,
- README includes the live public URL and local run instructions.
