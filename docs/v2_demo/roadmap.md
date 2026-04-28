# V2 Demo Roadmap

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
- `rg -n "v2_demo|V2|Streamlit|saved-output|not for clinical use" AGENTS.md project-tasks.md handoff.md docs/v2_demo docs/v1`

Done criteria:

- all v2 planning docs exist,
- root governance points future agents to v2 docs,
- durable v2 decisions are logged.

## V2.P2 - Saved artifact curation and sample manifest

Status: todo

Goal:
Choose a small set of demo samples and describe the artifacts needed by the
saved-output app.

Expected files:

- a demo sample manifest,
- curated demo artifact paths or copies,
- documentation of selected samples.

Verification:

- manifest validates paths,
- samples include at least one strong example and one high-error or failure
  example,
- no raw data or checkpoint is committed without explicit approval.

Done criteria:

- saved-output app has a stable sample source,
- demo can be built without scanning the full raw dataset at startup.

## V2.P3 - Streamlit saved-output explorer

Status: todo

Goal:
Build the first app using saved v1 artifacts.

Expected behavior:

- sample selector,
- stage-by-stage pipeline view,
- target mask view,
- prediction/mask view,
- cleanup and ellipse view,
- contour-vs-ellipse comparison where feasible,
- v1 experiment dashboard,
- safety disclaimer.

Verification:

- app launches locally,
- selected samples render without raw training,
- no checkpoint is required for default mode.

Done criteria:

- a local reviewer can understand the pipeline visually in under one minute.

## V2.P4 - Live inference integration

Status: todo

Goal:
Add optional model inference through a swappable adapter.

Expected behavior:

- load a checkpoint when provided,
- run model prediction on selected or uploaded images,
- produce the same stage objects as saved-output mode,
- show probability heatmaps when available.

Verification:

- live mode works on at least one local sample,
- saved-output mode still works without checkpoint files.

Done criteria:

- live inference is an optional enhancement, not a dependency of the demo.

## V2.P5 - Portfolio README polish and screenshots

Status: todo

Goal:
Turn the v2 demo into a resume-ready artifact.

Expected files:

- README demo section,
- screenshots or GIF references,
- run instructions,
- concise safety language.

Verification:

- README tells a reviewer what the app does and how to run it,
- screenshots/GIF render correctly when present.

Done criteria:

- the GitHub project reads like a polished applied ML portfolio project.

## V2.P6 - Optional HC18 challenge exporter

Status: todo

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
