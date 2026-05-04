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

1. `V2.S7` - Optional curated live inference mode.
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
- `.gitignore` additions: `frontend/node_modules/`, `frontend/dist/`
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
- `frontend/public/samples/` contains the curated runtime bundle.

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

Status: done

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

Status: done

Status note:
README, `start_demo.sh`, Vercel configuration, and the public curated artifact
deployment are implemented. The public production URL is live at
`https://fetal-head-measurement.vercel.app/`, the app now prefers
`/samples/manifest.json` on every host, and the root README presents the
repository as a v2 portfolio project rather than a course submission.

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
  - Path A is now approved for the public static site: commit the curated
    derivative bundle under `frontend/public/samples/`, keep raw HC18 data and
    checkpoints private, and retain `frontend/public/demo-samples/` as a
    fallback preview bundle.
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
- Confirm `frontend/public/samples/` is intentionally committed for the public
  curated bundle and remains a mirror of `outputs/demo_samples/`.
- Record the public URL in `handoff.md` and `DECISIONS.md`.

Verification:

- `bash start_demo.sh` runs from a clean shell after export artifacts exist.
- Public URL loads the app with the real curated artifact bundle.
- README renders correctly on GitHub.
- `git status` confirms no raw HC18 files or checkpoints are staged.

Done criteria:

- public URL is live and loads the app,
- public URL serves the real curated saved-output bundle,
- README explains the demo and gives the live URL,
- `start_demo.sh` works for local reviewers who have HC18 data,
- no raw HC18 files or checkpoints are committed or deployed.

## V2.S7 - Optional Curated Live Inference Mode

Status: in_progress

Status note:
`V2.S7.1` is complete. The shared Python live inference core now exists under
`src/inference/live.py`, exporter helper logic has been refactored to reuse it,
and contract tests cover both synthetic output shape/field validation and one
local curated-sample smoke run when HC18 artifacts are available.

Roadmap phase:
`V2.P4`

Target window:
Post-MVP, after `V2.S6`

Estimated effort:
8-14 hours across sub-sessions

Goal:
Add optional checkpoint-backed inference for curated samples without disturbing
the static saved-output mode.

Outcome:
A "Run live" mode lets a viewer select one of the curated samples, run the
checkpoint through a FastAPI demo server, and render returned outputs through
the same React `Sample` interface and image components used by static replay.

Planning source:
`docs/v2_demo/live-inference-plan.md`

Scope locks:

- Static saved-output mode remains the default and must work with no backend.
- First live mode is curated-sample-only. Arbitrary public upload is out of
  scope unless explicitly approved later.
- Do not publish checkpoints, raw HC18 data, or curated medical-image bundles
  without explicit user approval.
- Use `demo_live/` for the FastAPI companion server, not a generic `backend/`
  directory.

Expected files:

- `src/inference/live.py`
- `demo_live/app.py`
- `demo_live/live_service.py`
- `demo_live/schemas.py`
- `requirements-live.txt`
- `tests/test_live_inference_contract.py`
- `tests/test_live_api.py`
- `frontend/src/data/live-api.ts`
- `frontend/src/types/live.ts`
- `frontend/src/components/live/ModeToggle.tsx`
- `frontend/src/components/live/LiveRunPanel.tsx`
- `frontend/src/components/live/RunStatus.tsx`
- `frontend/src/utils/assets.ts` (shared `getSampleAssets` helper)
- README/docs updates for static vs live mode
- root `handoff.md`

### V2.S7.1 - Live Inference Core

Status: done

Goal:
Extract the single-sample inference transform into an importable utility shared
by the exporter and live server.

Subtasks:

- Factor the relevant logic from `scripts/export_demo_artifacts.py` into
  `src/inference/live.py`.
- Reuse `src.inference.predict.load_model_from_checkpoint`,
  `src.data.dataset.HC18Dataset`, and `src.utils.geometry`.
- Return a result object that can be converted to the frontend `Sample`
  contract plus `SampleAssets`.
- Support the local HC18 input source first and leave a clear interface for a
  hosted curated-bundle source.
- Keep `scripts/export_demo_artifacts.py` behavior stable after refactor.

Scope note: attention gate hook registration was added to this subtask list after
V2.S7.1 was already marked done and `src/inference/live.py` was implemented. The
hook is NOT part of the completed V2.S7.1 work. It belongs in V2.S7.2 — the
FastAPI server layer is the right place to register hooks and encode attention
maps into the API response. The `run_live_inference` signature should expose an
`include_attention: bool = False` parameter; the hook registration and PNG encoding
belong in the server, not in the reusable core.

Verification:

- `.venv/bin/python -m pytest tests/test_live_inference_contract.py`
- Run one curated sample locally and confirm `prob`, `pred`, ellipse, HC, and
  confidence values are shape/unit consistent.

Done criteria:

- one curated sample can run live inference locally,
- output has the same required fields as frontend `Sample`,
- exporter still produces schema-version-2 saved artifacts.

### V2.S7.2 - FastAPI Demo Server

Status: todo

Goal:
Expose curated live inference over HTTP.

Subtasks:

- Implement `GET /health`, `GET /live/samples`, and `POST /live/infer`.
- Load the checkpoint once at startup and return `checkpoint_not_loaded` if
  startup fails.
- Validate `sample_id` and threshold with consistent error codes.
- Add CORS support for Vite dev/preview and future deployed frontend origins.
- Cache deterministic curated-sample results by `(sample_id, threshold)`.
- Register forward hooks on `model.decoder4.gate.attention` (and equivalent gates
  for other decoder levels) to capture attention coefficient maps ([B, 1, H, W],
  sigmoid 0–1) during inference. Encode each map as a grayscale PNG and include
  it in the `/live/infer` response under `assets.attention` (key = decoder gate
  name, value = URL or data URL). No model changes required — hook the existing
  `attention` sub-module. See `docs/v2_demo/production-and-visualization-roadmap.md`
  Section 6.3.
- Include `step_times_ms` in the `/live/infer` response (keys: `preprocess`,
  `inference`, `threshold`, `cleanup`, `ellipse`, `measurement`).

Verification:

- `uvicorn demo_live.app:app --reload --port 8000`
- `curl http://127.0.0.1:8000/health`
- `curl -X POST http://127.0.0.1:8000/live/infer ...`
- `.venv/bin/python -m pytest tests/test_live_api.py`

Done criteria:

- backend loads checkpoint once,
- `POST /live/infer` works for at least one curated sample,
- response includes `step_times_ms` and `assets.attention` maps,
- saved-output frontend still works when the backend is not running.

### V2.S7.3 - React Live Mode

Status: todo

Goal:
Add the frontend mode toggle, backend readiness handling, and live asset
rendering.

Subtasks:

- Add `frontend/src/types/live.ts` — include `liveStatus` as
  `"idle" | "waking" | "running" | "done" | "error"`.
- Add `frontend/src/data/live-api.ts`.
- Implement `getSampleAssets` helper in `frontend/src/utils/assets.ts` — the
  single place that derives image paths for static mode or forwards live asset
  URLs/data URLs. All image-consuming components must use this helper.
- Add `frontend/src/components/live/ModeToggle.tsx`.
- Add `frontend/src/components/live/RunStatus.tsx` — renders waking/running/done/
  error states; used inside `LiveRunPanel`.
- Add `frontend/src/components/live/LiveRunPanel.tsx` — wraps RunStatus and the
  Run live button.
- Add `assetOverrides` support to `StageDetail` and `ThresholdViewer`.
- Poll `GET /health` and show backend-offline or backend-waking states without
  breaking static replay.
- Keep SafetyChip visible in both modes.

Verification:

- `cd frontend && npm run build`
- Static mode works with no backend.
- Live mode shows an unavailable state if the server is down.
- Live mode runs one curated sample when the server is up.
- Threshold viewer works on the live `prob` asset.

Done criteria:

- live and static modes share the same visual components,
- backend failure does not block the main demo,
- no arbitrary upload UI is added.

### V2.S7.4 - Live Deployment Packaging

Status: todo

Goal:
Choose and document the public/private live deployment path.

Subtasks:

- Keep Vercel or GitHub Pages as the static frontend path.
- Prefer local FastAPI live mode plus a recorded video until artifact
  publication is explicitly approved.
- If publishing live inference, prefer Hugging Face Spaces over Vercel
  serverless for PyTorch.
- Add README instructions for static-only, local-live, and any approved hosted
  live path.

Verification:

- deployed static frontend still loads,
- local or hosted live backend health check works,
- README explains any artifact/checkpoint prerequisites clearly.

Done criteria:

- live inference works on at least one local sample,
- static saved-output mode still works when backend is not running,
- no retraining occurs from the web UI,
- no checkpoint or curated medical-image artifact is published without explicit
  approval.

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

## V2.S9 - Optional Visualization Improvements

Status: todo

Roadmap phase:
`V2.P7` (post live-inference)

Target window:
Post-V2.S7

Estimated effort:
6-10 hours

Goal:
Add research-inspired interactive visualizations that strengthen the educational
and portfolio impact of the demo beyond the core pipeline walkthrough.

Outcome:
The demo has at least two new interactive elements from the visualization
improvements shortlist, each backed by pre-computed data from the export script.

Planning source:
`docs/v2_demo/production-and-visualization-roadmap.md` Section 3

Scope locks:

- MC Dropout is BLOCKED — `dropout: 0.0` in current checkpoint. Do not implement
  uncertainty estimation without retraining.
- Fetal growth chart is BLOCKED — HC18 has no gestational age column.
- All improvements must be additive. Saved-output static mode must remain fully
  functional with no backend.

Expected files:

- `scripts/export_demo_artifacts.py` (updated to pre-compute `thresholdCurve`)
- `frontend/src/components/threshold/ThresholdViewer.tsx` (Play button)
- `frontend/src/components/geometry/ContourEllipse.tsx` (HC ruler overlay)
- `frontend/src/types/sample.ts` (verify `thresholdCurve?` field is present)
- root `handoff.md`

Subtasks:

1. Pre-compute threshold-Dice curve in export script:
   - For each curated sample, compute Dice at thresholds `[0.10, 0.15, ..., 0.90]`
     by thresholding `prob.png` against `target.png` at each step.
   - Store the result as the `thresholdCurve` field in `manifest.json`.
     (The field is already defined in the TypeScript `Sample` interface and
     architecture.md Section 5 — just not yet computed by the exporter.)
   - Do not compute this curve in the browser — pixel-level iteration across
     17 thresholds belongs at export time.

2. Threshold sweep Play button animation:
   - Add a Play/Stop button to `ThresholdViewer` that animates the threshold
     from 0.1 to 0.9 at approximately 8 fps, showing the canvas mask and
     histogram updating together.
   - Overlay a marker on the histogram strip at `sample.thresholdCurve.optimalThreshold`.
   - Keep the existing manual slider fully functional alongside the animation.

3. HC ruler overlay on ContourEllipse:
   - After ellipse fit, draw a diameter line across the major axis scaled to HC in mm.
   - Label it "Pred HC: X mm / True HC: Y mm" directly on the canvas.
   - Show only when both `predHC` and `targetHC` are present in `sample.metrics`.

4. Probability callout on canvas hover (optional):
   - In `ThresholdViewer`, show a tooltip near the cursor with the probability
     value at that pixel, read from the canvas pixel data of `prob.png`.
   - Keep interactions lightweight — no server calls required.

5. Attention gate overlay (depends on V2.S7 attention maps):
   - If attention map assets are present (from V2.S7.2), add a toggle to overlay
     them on the ultrasound in the pipeline stepper.
   - Match the existing overlay style (CSS mix-blend-mode or canvas composite).
   - Skip gracefully if the `attention` field is absent from the sample assets.

Verification:

- `.venv/bin/python scripts/export_demo_artifacts.py --run-id attention_unet_local_baseline --split test`
- `rg -n "thresholdCurve" frontend/public/samples/manifest.json` — field present for each sample.
- `cd frontend && npm run build` — no TypeScript errors.
- ThresholdViewer Play button animates in the browser.
- Ruler overlay renders on ContourEllipse canvas for a strong sample.

Done criteria:

- export script pre-computes `thresholdCurve` for all curated samples,
- at least two visualization improvements from the list above are live in the deployed app,
- saved-output static mode remains fully functional with no backend.

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
