# Handoff

This file preserves current v2 demo session context for Codex agents. The
archived v1 history is under `docs/v1/handoff.md`.

Newest entry stays at the top.

## Current Status

- V1 course pipeline is complete and frozen except for bug fixes or explicit
  packaging/report updates.
- V1 governance and history live under `docs/v1/`.
- V2 demo work is on branch `v2-demo`.
- Root `AGENTS.md` is the active v2 operating contract.
- V2 planning docs live under `docs/v2_demo/`.
- V2 session-level task plan lives at `docs/v2_demo/project-tasks.md`.
- The v2 MVP direction is now a saved-output Vite + React + TypeScript pipeline
  explorer ported from the Claude Design handoff, with live checkpoint inference
  as a later backend/adapter-backed milestone.
- The previous Streamlit prototype under `demo/` is superseded for the
  portfolio MVP but remains available as local reference code.
- Existing v1 prediction artifacts already include per-sample raw masks,
  cleaned masks, overlays, prediction CSVs, and evaluation CSVs under
  `outputs/runs/<run_id>/predictions/` and `outputs/runs/<run_id>/evaluation/`.
- The local React scaffold now lives under `frontend/`, with the generated
  sample bundle copied to ignored `frontend/public/samples/` for development.
- V2.S4 core UI is implemented: sticky nav/tour, hero, sample gallery, pipeline
  stepper/detail, and threshold canvas. Geometry, metrics, and research
  dashboard sections are placeholders for V2.S5.

## Latest Session

Date: 2026-05-02

Task id:
`V2.S4` - React Pipeline Explorer (Core UI)

Branch:
`v2-demo`

Goal:
Port the core Claude Design React UI to the Vite TypeScript app and wire it to
the real schema-v2 sample manifest and generated PNG assets.

Files changed:

- `frontend/src/App.tsx`
- `frontend/src/styles.css`
- `frontend/src/components/nav/StickyNav.tsx`
- `frontend/src/components/nav/TourBar.tsx`
- `frontend/src/components/hero/Hero.tsx`
- `frontend/src/components/gallery/SampleGallery.tsx`
- `frontend/src/components/pipeline/PipelineStepper.tsx`
- `frontend/src/components/pipeline/StageDetail.tsx`
- `frontend/src/components/threshold/ThresholdViewer.tsx`
- `frontend/src/components/shared/SafetyChip.tsx`
- `frontend/src/components/shared/CategoryBadge.tsx`
- `docs/v2_demo/project-tasks.md`
- `handoff.md`

Commands run:

- `git status --short --branch`
- `rg --files docs/v2_demo docs/v1 frontend/src /Users/shreyas/Downloads/design_handoff_fetal_hc_explorer`
- `sed -n ... AGENTS.md project-tasks.md handoff.md docs/v2_demo/* docs/v1/*`
- `sed -n ... /Users/shreyas/Downloads/design_handoff_fetal_hc_explorer/{app.jsx,components/nav.jsx,components/gallery.jsx,components/pipeline.jsx,components/threshold.jsx,data.js,styles.css}`
- `mkdir -p frontend/src/components/nav frontend/src/components/hero frontend/src/components/gallery frontend/src/components/pipeline frontend/src/components/threshold frontend/src/components/shared`
- `cd frontend && npm run build`
- `ps -axo pid,command`
- `curl -I http://127.0.0.1:5173/`
- `curl -I http://127.0.0.1:5173/samples/manifest.json`
- `curl -I http://127.0.0.1:5173/samples/296_HC/prob.png`
- `rg -n "letter-spacing" frontend/src`
- `rg -n "V2\\.S4|SafetyChip|ThresholdViewer|SampleGallery|PipelineStepper|StageDetail|StickyNav|TourBar" frontend/src docs/v2_demo/project-tasks.md handoff.md`
- `find frontend/src/components -maxdepth 3 -type f`
- `git diff --check`

Verification result:

- `npm run build` passed with no TypeScript errors.
- Existing Vite dev server is reachable at `http://127.0.0.1:5173/`.
- `curl -I` confirmed the app root, `/samples/manifest.json`, and
  `/samples/296_HC/prob.png` are served.
- The threshold canvas reads same-origin `prob.png` and `ultrasound.png` paths
  through the same manifest-driven sample id convention as the design.
- CSS letter spacing declarations are all normalized to `0`.
- `git diff --check` passed.

Decisions made:

- Keep V2.S4 scoped to the core explorer UI only. Geometry controls, metrics
  gauges, and the real experiment dashboard remain in `V2.S5`, with placeholder
  section anchors so sticky nav and tour flow are already in place.
- Use each sample's exported `resolution`, `spacingXMm`, and `spacingYMm`
  rather than the design prototype's hardcoded 480x360 / 0.184 mm-pixel labels.
- Keep the safety chip visible with the manifest text:
  "Educational demo only. Not for clinical use."

Open issues:

- Full visual/browser interaction testing was limited to local serving checks
  and TypeScript build; no Playwright suite exists yet.
- The current server process at port 5173 was already running from the previous
  frontend session and is still serving the app.
- V2.S5 still needs the contour-vs-ellipse panel, metric gauges, and real
  experiment dashboard.
- Public artifact distribution remains undecided for portfolio polish.

Next exact task:

- Start `V2.S5 - Geometry Panel, Metrics, And Experiment Dashboard`: port the
  remaining sections and replace design placeholders with real v1 metrics,
  contour/ellipse values, sparklines, and ablation tables.

## Previous Session

Date: 2026-05-01

Task id:
`V2.S3` - React App Scaffold And Data Layer

Branch:
`v2-demo`

Goal:
Create the Vite + React + TypeScript frontend shell, port the design/data
contract into typed frontend modules, copy the saved-output sample bundle into
the app's public directory, and verify local dev/build flow.

Files changed:

- `.gitignore`
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/index.html`
- `frontend/tsconfig.json`
- `frontend/tsconfig.app.json`
- `frontend/tsconfig.node.json`
- `frontend/vite.config.ts`
- `frontend/src/main.tsx`
- `frontend/src/App.tsx`
- `frontend/src/styles.css`
- `frontend/src/types/sample.ts`
- `frontend/src/data/samples.ts`
- `frontend/src/data/stages.ts`
- `frontend/src/data/metric-copy.ts`
- `docs/v2_demo/project-tasks.md`
- `handoff.md`

Generated local artifacts:

- `frontend/public/samples/manifest.json`
- `frontend/public/samples/<sample_id>/ultrasound.png`
- `frontend/public/samples/<sample_id>/target.png`
- `frontend/public/samples/<sample_id>/pred.png`
- `frontend/public/samples/<sample_id>/prob.png`
- `frontend/public/samples/<sample_id>/metadata.json`
- `frontend/dist/`
- `frontend/node_modules/`

Commands run:

- `node --version`
- `npm --version`
- `mkdir -p frontend/src/data frontend/src/types frontend/public/samples`
- `cp -R outputs/demo_samples/. frontend/public/samples/`
- `cd frontend && npm install`
- `cd frontend && npm run build`
- `cd frontend && npm run dev -- --host 127.0.0.1 --port 5173`
- `curl -L http://127.0.0.1:5173/samples/manifest.json`
- `curl -L http://127.0.0.1:5173/`
- `curl -I http://127.0.0.1:5173/`
- `curl -I http://127.0.0.1:5173/samples/manifest.json`
- `find frontend/public/samples -maxdepth 2 -type f | sort | head -30`
- `test -f frontend/public/samples/manifest.json && test -f frontend/public/samples/296_HC/prob.png`
- `git status --short --ignored frontend`
- `git diff --check`

Verification result:

- `npm install` completed successfully with no reported vulnerabilities.
- `npm run build` completed successfully with no TypeScript errors.
- The Vite dev server is running at `http://127.0.0.1:5173/`.
- `curl -I` confirmed the app root and `/samples/manifest.json` are served
  from the unrestricted local shell. Sandboxed curl could not connect to the
  long-running Vite process even though the server was active.
- The fetched manifest is schema version 2 and includes the six curated samples.
- `frontend/public/samples/296_HC/prob.png` exists, confirming the copied
  bundle has the React-required image set.
- `frontend/public/samples/`, `frontend/dist/`, and `frontend/node_modules/`
  are gitignored.
- `git diff --check` passed.

Decisions made:

- Scaffolded Vite files manually instead of using the generator so the resulting
  files stayed deterministic in the existing dirty worktree.
- Kept the V2.S3 app as a typed shell/data proof only; full design components
  remain scoped to `V2.S4`.
- Normalized imported design letter spacing to `0` for frontend rule
  compliance.

Open issues:

- The full core explorer UI is not implemented yet.
- Local ignored sample folders still include older Streamlit-named artifacts
  alongside the required React files; this is harmless for the frontend but can
  be cleaned in a later exporter housekeeping pass.
- Public artifact distribution remains undecided for portfolio polish.

Next exact task:

- Start `V2.S4 - React Pipeline Explorer (Core UI)`: port the core explorer
  layout, stage selector, image panels, metric tiles, and safety copy using the
  typed sample data.

## Previous Session

Date: 2026-05-01

Task id:
`V2.S2` - React Demo Artifact Export And Manifest Validation

Branch:
`v2-demo`

Goal:
Revise the saved-output demo exporter from the old Streamlit bundle contract to
the React/Vite design contract, including checkpoint-generated `prob.png` and
schema version 2 manifest fields.

Files changed:

- `scripts/export_demo_artifacts.py`
- `scripts/validate_demo_manifest.py`
- `tests/test_demo_manifest.py`
- `docs/v2_demo/project-tasks.md`
- `docs/v2_demo/roadmap.md`
- `project-tasks.md`
- `handoff.md`

Generated local artifacts:

- `outputs/demo_samples/manifest.json`
- `outputs/demo_samples/<sample_id>/ultrasound.png`
- `outputs/demo_samples/<sample_id>/target.png`
- `outputs/demo_samples/<sample_id>/pred.png`
- `outputs/demo_samples/<sample_id>/prob.png`
- `outputs/demo_samples/<sample_id>/metadata.json`

Commands run:

- `test -d data/raw/HC18/training_set && test -f outputs/runs/attention_unet_local_baseline/best_model.pt`
- `.venv/bin/python -m compileall scripts/export_demo_artifacts.py scripts/validate_demo_manifest.py`
- `.venv/bin/python -m pytest tests/test_demo_manifest.py`
- `.venv/bin/python scripts/export_demo_artifacts.py --run-id attention_unet_local_baseline --split test`
- `.venv/bin/python scripts/validate_demo_manifest.py --manifest outputs/demo_samples/manifest.json`
- `rg -n "Educational demo only. Not for clinical use.|contourHC|confidence|predEllipse|schema_version" outputs/demo_samples/manifest.json`
- `.venv/bin/python - <<'PY' ...` image-shape/probability smoke check
- `rg -n "data/raw|best_model|\\.pt|\\.ckpt" outputs/demo_samples || true`
- `.venv/bin/python -m pytest tests/test_demo_manifest.py tests/test_demo_saved_output.py`
- `git diff --check`

Verification result:

- Prerequisites were present locally: raw HC18 training data and
  `attention_unet_local_baseline/best_model.pt`.
- Exported six curated samples: `296_HC`, `217_HC`, `663_HC`, `025_HC`,
  `793_HC`, and `032_HC`.
- Manifest validation passed with `schema_version: 2`.
- Every exported React artifact has shape 256x384:
  `ultrasound.png`, `target.png`, `pred.png`, and `prob.png`.
- Manifest includes `predEllipse`, `contourHC`, `confidence`, spacing,
  resolution, real metrics, and safety text.
- Focused tests passed: 5 tests.
- `outputs/demo_samples/` contains no raw-data paths or checkpoint references.
- `outputs/demo_samples/` remains ignored by git.
- `git diff --check` passed.

Decisions made:

- Use CPU checkpoint inference inside the exporter for `prob.png` generation so
  export does not depend on sandbox-visible MPS.
- Keep paths out of the React manifest and derive frontend image paths from
  `/samples/<id>/<file>.png`.
- Leave old ignored Streamlit-named files in `outputs/demo_samples/` if already
  present; the schema-v2 validator only requires the React artifact set.

Open issues:

- No `frontend/` project exists yet.
- `frontend/public/samples/` still needs to be created and gitignored in
  `V2.S3`.
- Public artifact distribution is still undecided for portfolio polish.

Next exact task:

- Start `V2.S3 - React App Scaffold And Data Layer`: scaffold the Vite React
  TypeScript app, port design tokens, define the TypeScript `Sample` contract,
  copy `outputs/demo_samples/` into `frontend/public/samples/`, and verify
  `npm run dev` plus `npm run build`.

## Previous Session

Date: 2026-05-01

Task id:
`V2.S2` / planning reconciliation - Claude Design React pivot

Branch:
`v2-demo`

Goal:
Analyze the Claude Design handoff at
`/Users/shreyas/Downloads/design_handoff_fetal_hc_explorer/`, reconcile it with
the existing v2 plan, and update Markdown contracts before implementation
continues.

Files changed:

- `AGENTS.md`
- `project-tasks.md`
- `docs/v2_demo/DECISIONS.md`
- `docs/v2_demo/architecture.md`
- `docs/v2_demo/project-spec.md`
- `docs/v2_demo/roadmap.md`
- `docs/v2_demo/project-tasks.md`
- `docs/v2_demo/frontend-design-handoff.md`
- `docs/v2_demo/CLAUDE-CODE-V2-REVIEW.md`
- `docs/v2_demo/curated-samples.md`
- `docs/v2_demo/curated-samples.json`
- `handoff.md`

Commands run:

- `find /Users/shreyas/Downloads/design_handoff_fetal_hc_explorer -maxdepth 3 -type f | sort`
- `sed -n ...` reads across root governance, v2 docs, v1 docs, and the design
  handoff files
- `rg -n "Streamlit|React|Vite|prob.png|..." AGENTS.md project-tasks.md handoff.md docs/v2_demo`
- `rg -n "142_HC|073_HC|511_HC|..."`
  `outputs/runs/attention_unet_local_baseline/evaluation/test/per_sample_metrics.csv`
- `.venv/bin/python -m json.tool docs/v2_demo/curated-samples.json`
- `git diff --check`

Verification result:

- Confirmed the design handoff is a high-fidelity React prototype, not
  production code.
- Confirmed the design sample metrics and some sample IDs are placeholders.
- Confirmed the current curated sample set already provides a stronger real
  success/typical/failure story than the design IDs.
- `docs/v2_demo/curated-samples.json` remains valid JSON after category
  normalization.
- `git diff --check` passed.

Decisions made:

- Current MVP framework is Vite + React + TypeScript, not Streamlit.
- Existing Streamlit work is superseded reference code.
- Keep the current curated samples: `296_HC`, `217_HC`, `663_HC`, `025_HC`,
  `793_HC`, and `032_HC`.
- Normalize frontend categories to `strong`, `typical`, and `failure`; preserve
  cleanup/error nuance in labels and tags.
- Resume implementation at the React artifact-contract revision: export
  `ultrasound.png`, `target.png`, `pred.png`, and `prob.png`; produce manifest
  schema version 2.

Open issues:

- `scripts/export_demo_artifacts.py` and `scripts/validate_demo_manifest.py`
  still need to be revised to the React schema.
- No `frontend/` project exists yet.
- Generated medical-image artifacts remain local/ignored unless the user
  approves a distribution policy.

Next exact task:

- Implement `V2.S2 - Export Demo Artifacts And Validate Manifest` for the React
  contract, including checkpoint-generated `prob.png` and manifest schema
  version 2.

## Previous Session

Date: 2026-05-01

Task id:
`V2.S4` - Streamlit Import-Path Hotfix

Branch:
`v2-demo`

Goal:
Fix the local Streamlit launch error where `demo/app.py` could not import the
`demo.adapters` package when executed as a script by Streamlit.

Files changed:

- `demo/app.py`
- `handoff.md`

Commands run:

- `.venv/bin/python -m compileall demo/app.py`
- `.venv/bin/python - <<'PY' ...` Streamlit `AppTest` smoke check
- `.venv/bin/python -m pytest tests/test_demo_manifest.py tests/test_demo_saved_output.py`
- `curl -L http://localhost:8501/_stcore/health`
- `git diff --check`

Verification result:

- App entrypoint compiles.
- Streamlit `AppTest` renders without app exceptions.
- Focused demo tests still pass: 5 tests.
- Existing local Streamlit server health endpoint returns `ok`.
- `git diff --check` passed.

Decisions made:

- Add the repository root to `sys.path` at the app entrypoint before importing
  the local `demo` package so `streamlit run demo/app.py` works from localhost.

Open issues:

- `V2.S5` still needs to add the experiment dashboard and measurement story.

Next exact task:

- Refresh the local Streamlit page and then start `V2.S5 - Experiment Dashboard
  And Measurement Story` once the app launch is confirmed.

## Previous Session

Date: 2026-05-01

Task id:
`V2.S4` - Streamlit Pipeline Explorer

Branch:
`v2-demo`

Goal:
Build the first saved-output Streamlit app screen with sample selection, visible
safety language, core pipeline stage images, and concise metrics.

Files changed:

- `requirements-demo.txt`
- `demo/app.py`
- `demo/components/__init__.py`
- `demo/components/sample_selector.py`
- `demo/components/pipeline_views.py`
- `docs/v2_demo/project-tasks.md`
- `handoff.md`

Commands run:

- `sed -n '276,333p' docs/v2_demo/project-tasks.md`
- `.venv/bin/python -c "import streamlit; print(streamlit.__version__)"` before install
- `.venv/bin/python -m compileall demo`
- `.venv/bin/python -m pytest tests/test_demo_manifest.py tests/test_demo_saved_output.py`
- `UV_CACHE_DIR=.uv-cache uv pip install -r requirements-demo.txt` (failed because uv targeted an unrelated active environment and network was sandboxed)
- `.venv/bin/python -m pip install -r requirements-demo.txt` (failed because `.venv` has no pip module)
- `VIRTUAL_ENV= UV_CACHE_DIR=.uv-cache uv pip install --python .venv/bin/python -r requirements-demo.txt`
- `.venv/bin/streamlit --version`
- `.venv/bin/streamlit run demo/app.py --server.port 8501 --server.headless true`
- `curl -L http://localhost:8501`
- `.venv/bin/python - <<'PY' ...` saved-output loader smoke check
- `.venv/bin/python - <<'PY' ...` Streamlit `AppTest` smoke check
- `curl -L http://localhost:8501/_stcore/health`

Verification result:

- Streamlit 1.57.0 installed in project `.venv`.
- `compileall demo` passed.
- Focused demo tests passed: 5 tests.
- Streamlit app started successfully at `http://localhost:8501`.
- Health endpoint returned `ok`.
- Streamlit `AppTest` smoke check confirmed the title, safety warning, and two
  selectboxes render without app exceptions.
- Saved-output loader confirmed all six samples load with expected 256x384 image
  and mask arrays.
- Marked `V2.S4` as done.

Decisions made:

- Keep the first app screen focused on the actual pipeline explorer.
- Add demo dependencies in `requirements-demo.txt`, separate from v1
  `requirements.txt`.
- Use the generated saved-output bundle as the only app data source for this
  milestone.

Open issues:

- `V2.S5` still needs to add the experiment dashboard and fuller measurement
  story.
- `outputs/demo_samples/` remains generated and ignored.
- `context-bridge-log.md` and `context-bridge-state.db` are untracked and were
  not changed.

Next exact task:

- Start `V2.S5 - Experiment Dashboard And Measurement Story`: add result-table
  loading, training/validation loss curves, post-processing comparison, and a
  clearer contour-vs-ellipse panel while keeping saved-output mode raw-data-free.

## Previous Session

Date: 2026-05-01

Task id:
`V2.S3` - Saved-Output Data Layer

Branch:
`v2-demo`

Goal:
Build the app-facing saved-output adapter and `DemoSample` contract without
Streamlit-specific code.

Files changed:

- `demo/__init__.py`
- `demo/adapters/__init__.py`
- `demo/adapters/saved_output.py`
- `demo/types.py`
- `tests/test_demo_saved_output.py`
- `docs/v2_demo/project-tasks.md`
- `handoff.md`

Commands run:

- `sed -n '223,276p' docs/v2_demo/project-tasks.md`
- `sed -n '1,220p' outputs/demo_samples/manifest.json`
- `sed -n '1,220p' outputs/demo_samples/025_HC/metadata.json`
- `.venv/bin/python -m pytest tests/test_demo_saved_output.py`
- `.venv/bin/python -m compileall demo`
- `.venv/bin/python -c "from demo.adapters.saved_output import load_manifest; print('import ok')"`
- `.venv/bin/python -c "from demo.adapters.saved_output import load_manifest; print(load_manifest('outputs/demo_samples/manifest.json').safety_text)"`
- `.venv/bin/python - <<'PY' ...` to load the real manifest and `025_HC`
- `rg -n "streamlit|torch" demo tests/test_demo_saved_output.py`
- `.venv/bin/python -m pytest tests/test_demo_manifest.py tests/test_demo_saved_output.py`

Verification result:

- `tests/test_demo_saved_output.py` passed: 3 tests.
- Combined demo tests passed: 5 tests.
- `compileall demo` passed.
- Import smoke check printed `import ok`.
- Artifact-bundle smoke check printed the required safety text.
- Real manifest loads six sample ids.
- Real sample `025_HC` loads with image/mask shape 256x384, overlay shape
  256x384x3, category `cleanup_ellipse`, and non-null `contour_hc_mm`.
- `rg -n "streamlit|torch" demo tests/test_demo_saved_output.py` found no
  matches, confirming the saved-output layer does not import Streamlit or
  PyTorch.
- Marked `V2.S3` as done.

Decisions made:

- Load masks as binary `uint8` arrays with values 0/1.
- Load ellipse overlays as RGB `uint8` arrays for future Streamlit rendering.
- Keep `DemoManifest` separate from `DemoSample` so UI code can list samples
  without loading every image.

Open issues:

- Streamlit UI is not implemented yet.
- `outputs/demo_samples/` remains a generated ignored local artifact bundle.
- `context-bridge-log.md` and `context-bridge-state.db` are untracked and were
  not changed.

Next exact task:

- Start `V2.S4 - Streamlit Pipeline Explorer`: add `requirements-demo.txt`,
  `demo/app.py`, `demo/components/sample_selector.py`, and
  `demo/components/pipeline_views.py`; render sample selection and the original,
  target, raw prediction, cleaned mask, and ellipse overlay views with visible
  safety language.

## Previous Session

Date: 2026-05-01

Task id:
`V2.S2` - Export Demo Artifacts And Validate Manifest

Branch:
`v2-demo`

Goal:
Create a raw-data-free saved-output artifact bundle for the Streamlit MVP and
validate the manifest.

Files changed:

- `scripts/export_demo_artifacts.py`
- `scripts/validate_demo_manifest.py`
- `tests/test_demo_manifest.py`
- `outputs/demo_samples/manifest.json` (generated and ignored)
- `outputs/demo_samples/<sample_id>/...` (generated and ignored)
- `docs/v2_demo/project-tasks.md`
- `docs/v2_demo/roadmap.md`
- `project-tasks.md`
- `handoff.md`

Commands run:

- `test -d data/raw/HC18/training_set`
- `.venv/bin/python -m pytest tests/test_demo_manifest.py`
- `.venv/bin/python -m compileall scripts/export_demo_artifacts.py scripts/validate_demo_manifest.py`
- `.venv/bin/python -m json.tool docs/v2_demo/curated-samples.json`
- `.venv/bin/python scripts/export_demo_artifacts.py --run-id attention_unet_local_baseline --split test`
- `.venv/bin/python scripts/validate_demo_manifest.py --manifest outputs/demo_samples/manifest.json`
- `rg -n "Educational demo only. Not for clinical use." outputs/demo_samples/manifest.json`
- `rg -n "contour_hc_mm" outputs/demo_samples/*/metadata.json`
- `find outputs/demo_samples -maxdepth 2 -type f | sort`
- `rg -n "data/raw|best_model|\\.pt|\\.ckpt" outputs/demo_samples || true`
- `.venv/bin/python - <<'PY' ...` to confirm exported image/mask/overlay shapes
- `git status --short --ignored outputs/demo_samples data/raw .venv .uv-cache`

Verification result:

- Manifest validation passed.
- `tests/test_demo_manifest.py` passed: 2 tests.
- Exported six curated samples: `296_HC`, `217_HC`, `663_HC`, `025_HC`,
  `793_HC`, and `032_HC`.
- Each sample has `image.png`, `target_mask.png`, `raw_mask.png`,
  `cleaned_mask.png`, `ellipse_overlay.png`, and `metadata.json`.
- Each exported image/mask is aligned at 256x384; overlays are 256x384x3.
- Each metadata file includes non-null `contour_hc_mm`.
- `outputs/demo_samples/` contains no `data/raw`, checkpoint, `.pt`, or `.ckpt`
  references.
- `outputs/demo_samples/` remains ignored by git, as intended.
- Marked `V2.S2` and roadmap/root `V2.P2.5` as done.

Decisions made:

- Exported model-space/preprocessed grayscale images at 256x384 so image,
  target mask, prediction masks, and overlays align in the saved-output app.
- Kept generated demo medical-image assets under ignored `outputs/demo_samples/`.

Open issues:

- `outputs/demo_samples/` is generated locally and ignored; future portfolio
  polish still needs to choose the public artifact distribution strategy.
- Streamlit data loading is not implemented yet.
- `context-bridge-log.md` and `context-bridge-state.db` are untracked and were
  not changed.

Next exact task:

- Start `V2.S3 - Saved-Output Data Layer`: add `demo/types.py`,
  `demo/adapters/saved_output.py`, and tests that load
  `outputs/demo_samples/manifest.json` into the `DemoSample` contract without
  importing Streamlit or PyTorch.

## Previous Session

Date: 2026-05-01

Task id:
`V2.S1` - Curate Demo Sample Set

Branch:
`v2-demo`

Goal:
Choose the saved-output demo sample set and write both human-readable rationale
and machine-readable exporter input.

Files changed:

- `docs/v2_demo/curated-samples.md`
- `docs/v2_demo/curated-samples.json`
- `docs/v2_demo/project-tasks.md`
- `docs/v2_demo/roadmap.md`
- `project-tasks.md`
- `handoff.md`

Commands run:

- `sed -n '75,138p' docs/v2_demo/project-tasks.md`
- `sed -n '1,260p' docs/v2_demo/architecture.md`
- `head -5 outputs/runs/attention_unet_local_baseline/evaluation/test/per_sample_metrics.csv`
- `head -5 outputs/runs/attention_unet_local_baseline/predictions/test/predictions.csv`
- `.venv/bin/python - <<'PY' ...` to rank best, median, high-error, and low-Dice candidates
- `.venv/bin/python - <<'PY' ...` to inspect post-processing variants for candidate samples
- `.venv/bin/python -m json.tool docs/v2_demo/curated-samples.json`
- `rg -n "strong|typical|high-error|cleanup|ellipse|failure" docs/v2_demo/curated-samples.md`
- `.venv/bin/python - <<'PY' ...` to verify selected prediction rows, raw masks, cleaned masks, and overlays
- `test -f docs/v2_demo/curated-samples.md && test -f docs/v2_demo/curated-samples.json`

Verification result:

- Curated six samples from `attention_unet_local_baseline` internal test:
  `296_HC`, `217_HC`, `663_HC`, `025_HC`, `793_HC`, and `032_HC`.
- JSON is valid.
- Markdown rationale includes strong, typical, cleanup/ellipse, high-error, and
  failure categories.
- Each selected sample has a prediction row, metrics row, raw mask, cleaned
  mask, and overlay path present under the v1 output tree.
- Marked `V2.S1` and roadmap/root `V2.P2` as done.

Decisions made:

- Use six curated samples rather than the minimum five to cover both a large-HC
  high-error case and a low-Dice small-HC failure case.
- Keep `docs/v2_demo/curated-samples.md` human-readable and
  `docs/v2_demo/curated-samples.json` machine-readable.

Open issues:

- `V2.S2` still needs to export original images, target masks, copied masks,
  overlays, per-sample metadata, and `outputs/demo_samples/manifest.json`.
- `V2.S2` must compute `contour_hc_mm` from cleaned masks.
- `V2.S2` requires local `data/raw/HC18/training_set/` for export only.
- `outputs/demo_samples/` has not been generated yet.
- `context-bridge-log.md` and `context-bridge-state.db` are untracked and were
  not changed.

Next exact task:

- Start `V2.S2 - Export Demo Artifacts And Validate Manifest`: implement
  `scripts/export_demo_artifacts.py` and `scripts/validate_demo_manifest.py`,
  export the six curated samples, compute `contour_hc_mm`, and validate
  `outputs/demo_samples/manifest.json`.

## Previous Session

Date: 2026-05-01

Task id:
V2 Round 2 plan review incorporation

Branch:
`v2-demo`

Goal:
Analyze the updated Claude Code review and tighten v2 planning docs before
implementation starts.

Files changed:

- `docs/v2_demo/project-tasks.md`
- `docs/v2_demo/architecture.md`
- `docs/v2_demo/project-spec.md`
- `docs/v2_demo/roadmap.md`
- `docs/v2_demo/DECISIONS.md`
- `project-tasks.md`
- `handoff.md`

Commands run:

- `git status --short --branch`
- `sed -n ... AGENTS.md project-tasks.md handoff.md docs/v2_demo/* docs/v1/*`
- `rg -n "contour|circumference|ellipse|clean" src/utils/geometry.py src/evaluation src/inference scripts/postprocess_ablation.py`
- `sed -n '1,260p' src/utils/geometry.py`
- `head -5 outputs/runs/attention_unet_local_baseline/predictions/test/predictions.csv`
- `head -5 outputs/runs/attention_unet_local_baseline/evaluation/test/per_sample_metrics.csv`

Verification result:

- Confirmed v1 prediction/evaluation CSVs do not contain `contour_hc_mm`.
- Confirmed `src/utils/geometry.py` exposes `mask_contour_length_mm`.
- Updated v2 session tasks so V2.S2 computes contour HC from cleaned masks.
- Documented that V2.S2 requires local `data/raw/HC18/training_set/` for export
  only; saved-output app runtime remains raw-data-free.
- Replaced Markdown parsing with machine-readable
  `docs/v2_demo/curated-samples.json`.

Decisions made:

- `curated-samples.md` is human rationale only.
- `curated-samples.json` is the exporter input, with repeated `--sample-id`
  arguments allowed for one-off tests.
- `contour_hc_mm` should be computed during artifact export and stored in
  per-sample metadata, not recomputed in the Streamlit UI.

Open issues:

- `docs/v2_demo/curated-samples.md` and `docs/v2_demo/curated-samples.json` do
  not exist yet.
- No implementation has started yet.
- `outputs/demo_samples/` has not been generated yet.
- `context-bridge-log.md` and `context-bridge-state.db` are untracked and were
  not changed.

Next exact task:

- Start `V2.S1 - Curate Demo Sample Set`: inspect internal-test metrics, choose
  at least five samples, and write both `docs/v2_demo/curated-samples.md` and
  `docs/v2_demo/curated-samples.json`.

## Previous Session

Date: 2026-05-01

Task id:
V2 session task planning

Branch:
`v2-demo`

Goal:
Divide the v2 roadmap into implementation sessions with outcomes, subtasks,
expected files, verification, and done criteria before starting code work.

Files changed:

- `docs/v2_demo/project-tasks.md`
- `docs/v2_demo/roadmap.md`
- `project-tasks.md`
- `handoff.md`

Commands run:

- `sed -n ... AGENTS.md project-tasks.md handoff.md docs/v2_demo/*`
- `test -f docs/v2_demo/project-tasks.md`
- `rg -n "V2.S1|V2.S2|V2.S6|V2.S7|V2.S8" docs/v2_demo/project-tasks.md`
- `git diff --check`

Verification result:

- Added `docs/v2_demo/project-tasks.md` with sessions `V2.S0` through `V2.S8`.
- Confirmed the critical path is `V2.S1` through `V2.S6` for the saved-output
  MVP and portfolio polish.
- Confirmed post-MVP live inference and challenge export are separated as
  optional sessions.

Decisions made:

- Use `docs/v2_demo/project-tasks.md` as the detailed v2 execution queue.
- Keep root `project-tasks.md` as the repository-wide index.

Open issues:

- No implementation has started yet.
- Next session still needs to curate samples before artifact export.

Next exact task:

- Start `V2.S1 - Curate Demo Sample Set`: inspect internal-test metrics,
  choose at least five samples, and write `docs/v2_demo/curated-samples.md`.

## Previous Session

Date: 2026-05-01

Task id:
V2 plan review and documentation hardening

Branch:
`v2-demo`

Goal:
Review the v2 demo plan and Claude Code review, identify implementation
blockers, and update planning docs so the next implementation task has a clear
artifact/export/UI contract.

Files changed:

- `README.md`
- `project-tasks.md`
- `handoff.md`
- `docs/v2_demo/architecture.md`
- `docs/v2_demo/project-spec.md`
- `docs/v2_demo/roadmap.md`
- `docs/v2_demo/DECISIONS.md`
- `report/submission-checklist.md`

Commands run:

- `rg --files`
- `git status --short --branch`
- `sed -n ... AGENTS.md project-tasks.md docs/v2_demo/* docs/v1/* README.md`
- `find outputs -maxdepth ...`
- `head -5 outputs/runs/attention_unet_local_baseline/evaluation/test/per_sample_metrics.csv`
- `head -5 outputs/runs/attention_unet_local_baseline/predictions/test/predictions.csv`

Verification result:

- Confirmed v2 docs exist and Claude review has been incorporated.
- Confirmed root `handoff.md` was missing in the working tree and recreated as
  the active v2 handoff.
- Confirmed existing v1 artifacts are useful but not sufficient for raw-data-free
  demo runtime because image and target-mask exports still need to be bundled.

Decisions made:

- Use `demo/app.py` as the Streamlit entrypoint.
- Use `demo/components/` for reusable panels and `demo/adapters/` for sample
  loading/inference adapters.
- Use `outputs/demo_samples/manifest.json` as the saved-output app input.
- Add `V2.P2.5` before Streamlit work to export and validate the demo bundle.
- Keep generated demo medical-image artifacts local until the user explicitly
  approves a public distribution policy.

Open issues:

- `scripts/export_demo_artifacts.py` and `scripts/validate_demo_manifest.py` do
  not exist yet.
- `outputs/demo_samples/` has not been generated yet.
- Demo dependencies are not defined yet; use `requirements-demo.txt` during
  `V2.P3`.
- Public demo artifact distribution still needs a final choice during portfolio
  polish.
- `context-bridge-log.md` and `context-bridge-state.db` are untracked and were
  not changed.

Next exact task:

- Implement `V2.P2.5`: create `scripts/export_demo_artifacts.py` and
  `scripts/validate_demo_manifest.py`, export at least five curated samples from
  `attention_unet_local_baseline` internal-test outputs, and validate
  `outputs/demo_samples/manifest.json`.
