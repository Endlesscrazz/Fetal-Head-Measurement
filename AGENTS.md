# AGENTS.md - V2 Demo Operating Contract

This file is the source of truth for agents working on the v2 demo and current
repository direction. The completed v1 course pipeline contract is archived at
`docs/v1/AGENTS.md`.

## 1. V2 mission

Build a small educational web demo that explains the fetal HC18 CNN pipeline:

1. select a curated ultrasound example,
2. show the annotation-derived target mask,
3. show the CNN probability or saved prediction output,
4. show thresholded and cleaned masks,
5. fit an ellipse,
6. compute head circumference in millimeters,
7. summarize the v1 experiment results.

The v2 thesis:

> Turn the v1 research pipeline into an interactive ML pipeline explorer that
> helps a user understand how segmentation outputs become geometric
> measurements.

## 2. Required files to read before v2 changes

Every v2 session must read:

1. root `AGENTS.md`
2. root `project-tasks.md`
3. root `handoff.md`
4. `docs/v2_demo/DECISIONS.md`
5. `docs/v2_demo/project-tasks.md`
6. all files under `docs/v2_demo/`
7. relevant v1 docs under `docs/`

If a v2 task conflicts with v1 rules, the newest explicit user request wins,
but the conflict must be recorded in `handoff.md` and, if durable, in
`docs/v2_demo/DECISIONS.md`.

## 3. Scope locks

- V1 course pipeline is frozen except for bug fixes needed by the demo.
- The first v2 implementation milestone is a saved-output Vite + React +
  TypeScript explorer ported from the Claude Design handoff.
- The earlier Streamlit prototype under `demo/` is superseded for the portfolio
  MVP. Keep it only as local reference unless the user explicitly asks to revive
  it.
- Live checkpoint inference is a later milestone and must use a swappable
  adapter interface so the saved-output demo remains stable.
- Do not retrain models from the web UI.
- Do not build a clinical diagnosis tool.
- Do not expose arbitrary public medical-image upload in the first milestone.
- Do not commit raw HC18 data, virtual environments, caches, or checkpoints
  unless the user explicitly approves a different artifact policy.
- Include visible safety language in user-facing demo screens:
  "Educational demo only. Not for clinical use."

## 4. Development policy

- Use Vite + React + TypeScript as the v2 web framework unless the user
  explicitly changes it again.
- Keep v1 training, inference, and evaluation modules importable.
- Add demo-specific frontend code under `frontend/`.
- Prefer small curated sample manifests over scanning raw data at app startup.
- Keep expensive model inference optional until the live-inference milestone.
- Keep app copy concise and visual. The app should teach by showing pipeline
  stages, not by filling the screen with explanations.

## 5. Build order

Follow this order unless the user explicitly changes it:

1. checkpoint v1 on `main`,
2. create the `v2-demo` branch,
3. create v2 planning docs and root governance pointers,
4. curate saved demo artifacts and a sample manifest,
5. revise exported demo artifacts for the React contract, including `prob.png`,
6. build the React saved-output explorer,
7. add live inference through a replaceable backend/adapter,
8. polish README, screenshots, and portfolio materials,
9. optionally add HC18 challenge submission export.

## 6. Required handoff

After meaningful v2 work, update root `handoff.md` with:

- date,
- v2 task id,
- branch,
- goal,
- files changed,
- commands run,
- verification result,
- decisions made,
- open issues,
- next exact task.

## 7. Completion definition for v2 MVP

V2 MVP is complete when:

- a user can launch the demo locally,
- a user can select a curated saved sample,
- the app shows original image, target mask, prediction/mask stage, cleaned
  mask, fitted ellipse, and HC measurement,
- the app includes a small experiment dashboard from v1 results,
- the app includes the safety disclaimer,
- README explains how to run the demo,
- the default React app does not require raw HC18 data or checkpoints after the
  curated artifact bundle has been exported.
