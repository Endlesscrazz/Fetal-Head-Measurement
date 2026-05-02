# V2 Demo Roadmap

Detailed implementation sessions live in `docs/v2_demo/project-tasks.md`.
Use this roadmap for milestone direction and the session task plan for
day-to-day execution.

Task status values:

- `todo`
- `in_progress`
- `blocked`
- `done`

## V2.P0 - V1 checkpoint and branch setup

Status: done

Goal:
Preserve the completed v1 course pipeline on `main` and create a clean branch
for v2 demo work.

Expected files:

- `.gitignore`
- all v1 source, config, report, and governance files needed for the checkpoint

Verification:

- `bash Myproject.sh`
- `git status --short`
- `git push`
- `git checkout -b v2-demo`

Done criteria:

- v1 is committed on `main`,
- `main` is pushed,
- v2 work continues on `v2-demo`,
- final submission ZIP remains local and uncommitted.

## V2.P1 - Planning docs and governance pointers

Status: done

Goal:
Create the v2 planning docs and point root governance files at them.

Expected files:

- root `AGENTS.md`
- `docs/v2_demo/architecture.md`
- `docs/v2_demo/project-spec.md`
- `docs/v2_demo/roadmap.md`
- `docs/v2_demo/DECISIONS.md`
- `docs/v1/AGENTS.md`
- `docs/v1/DECISIONS.md`
- root `project-tasks.md`
- root `handoff.md`

Verification:

- `rg --files docs/v2_demo`
- `sed -n '1,220p' AGENTS.md`
- `sed -n '1,220p' docs/v2_demo/architecture.md`
- `sed -n '1,220p' docs/v2_demo/project-spec.md`
- `sed -n '1,220p' docs/v2_demo/roadmap.md`
- `sed -n '1,220p' docs/v2_demo/DECISIONS.md`
- `rg -n "v2_demo|V2|React|Vite|saved-output|not for clinical use" AGENTS.md project-tasks.md handoff.md docs/v2_demo docs/v1`

Done criteria:

- all v2 planning docs exist,
- root governance points future agents to v2 docs,
- durable v2 decisions are logged.

## V2.P2 - Saved artifact curation and sample manifest

Status: done

Estimated effort:
1-2 hours

Goal:
Choose a small set of demo samples and define the stable manifest used by the
saved-output app.

Expected files:

- `outputs/demo_samples/manifest.json` schema confirmed in
  `docs/v2_demo/architecture.md`,
- `docs/v2_demo/curated-samples.md`,
- `docs/v2_demo/curated-samples.json`,
- documentation of selected sample categories,
- selected examples from `attention_unet_local_baseline` internal-test
  prediction/evaluation artifacts.

Verification:

- `.venv/bin/python -m json.tool docs/v2_demo/curated-samples.json`,
- samples include at least one strong example and one high-error or failure
  example,
- no raw data or checkpoint is committed without explicit approval.

Done criteria:

- saved-output app has a planned stable sample source,
- sample categories are explicit before export starts.

## V2.P2.5 - Demo artifact export and manifest validation

Status: done

Status note:
The earlier Streamlit-oriented exporter was completed, but the Claude Design
pivot changed the required artifact names and manifest schema. This phase now
means "revise the exporter to schema version 2," not "start from scratch."

Estimated effort:
4-6 hours

Goal:
Revise the export scripts so they produce the raw-data-free React artifact
bundle required by the Claude Design handoff and validate the manifest before
frontend implementation continues.

Expected files:

- `scripts/export_demo_artifacts.py`,
- `scripts/validate_demo_manifest.py`,
- `outputs/demo_samples/manifest.json`,
- `outputs/demo_samples/<sample_id>/ultrasound.png`,
- `outputs/demo_samples/<sample_id>/target.png`,
- `outputs/demo_samples/<sample_id>/pred.png`,
- `outputs/demo_samples/<sample_id>/prob.png`,
- `outputs/demo_samples/<sample_id>/metadata.json`.

Verification:

- `test -d data/raw/HC18/training_set`,
- `.venv/bin/python scripts/export_demo_artifacts.py --run-id attention_unet_local_baseline --split test`,
- `.venv/bin/python scripts/validate_demo_manifest.py --manifest outputs/demo_samples/manifest.json`,
- exported manifest paths resolve without scanning `data/raw/HC18` from the app,
- exported manifest includes computed `contourHC`, `confidence`, `predEllipse`,
  pixel spacing, image resolution, and real v1 metrics,
- every selected sample has a real `prob.png` probability map,
- exported samples include at least one strong prediction and one high-error or
  failure example.

Done criteria:

- saved-output demo has a stable, checkpoint-independent artifact bundle,
- raw HC18 is needed only for export, not for app runtime,
- React work can start without inventing a manifest schema.

## V2.P3 - React saved-output explorer

Status: todo

Estimated effort:
8-12 hours

Goal:
Build the first portfolio app using saved v1 artifacts and the Claude Design
handoff.

Expected behavior:

- visual sample gallery,
- sticky navigation and guided tour,
- stage-by-stage pipeline view,
- target mask view,
- probability map and threshold/mask view,
- cleanup and ellipse view,
- contour-vs-ellipse comparison when both values are available,
- v1 experiment dashboard,
- training/validation loss curves from saved v1 metrics,
- safety disclaimer.

Expected files:

- `frontend/package.json`,
- `frontend/src/`,
- `frontend/public/samples/`,
- frontend dependency and build configuration.

Verification:

- app launches locally,
- selected samples render without raw training,
- no checkpoint is required for default mode,
- `npm run dev` from `frontend/` is the documented local run command,
- `npm run build` succeeds with no TypeScript errors.

Done criteria:

- a local reviewer can understand the pipeline visually in under one minute.

## V2.P4 - Live inference integration

Status: todo

Estimated effort:
6-10 hours

Goal:
Add optional model inference through a swappable adapter.

Expected behavior:

- load a checkpoint when provided,
- run model prediction on selected or uploaded images,
- produce JSON compatible with the React `Sample` interface defined in
  `docs/v2_demo/architecture.md`,
- show probability heatmaps when available.

Verification:

- live mode works on at least one local sample,
- saved-output mode still works without checkpoint files.

Done criteria:

- live inference is an optional enhancement, not a dependency of the demo.

## V2.P5 - Portfolio README polish and screenshots

Status: todo

Estimated effort:
3-4 hours

Goal:
Turn the v2 demo into a resume-ready artifact.

Expected files:

- README demo section,
- screenshots or GIF references,
- run instructions,
- concise safety language.

Verification:

- README tells a reviewer what the app does and how to run it,
- screenshots/GIF render correctly when present,
- there is a one-command local start path such as `make demo`, `./start_demo.sh`,
  or documented commands that export artifacts and start Vite after dependencies
  are installed.

Done criteria:

- the GitHub project reads like a polished applied ML portfolio project.

## V2.P6 - Optional HC18 challenge exporter

Status: todo

Estimated effort:
4-6 hours

Goal:
Add tooling to export official HC18 challenge-style CSV predictions.

Expected behavior:

- run inference on the official unlabeled test set,
- export the challenge-required ellipse CSV,
- validate row count, filenames, units, and missing values.

Verification:

- submission CSV has the required columns and expected number of rows,
- no official labels are assumed.

Done criteria:

- the project can produce a first learning-oriented challenge submission.
