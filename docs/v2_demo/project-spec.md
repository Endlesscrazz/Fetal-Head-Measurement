# V2 Demo Project Specification

## 1. Project summary

Build an interactive Vite + React + TypeScript demo that turns the completed v1
fetal head circumference pipeline into a visual ML learning tool.

The app should help a user understand this sequence:

```text
ultrasound image -> target mask -> CNN prediction -> mask cleanup -> ellipse fit -> HC measurement
```

The first milestone is a static saved-output single-page app ported from the
Claude Design handoff at
`/Users/shreyas/Downloads/design_handoff_fetal_hc_explorer/`. The app should be
designed so live checkpoint inference can be added later through a separate
backend without rewriting the visual frontend.

## 2. Audience

Primary audience:

- recruiters,
- interviewers,
- ML learners,
- the project author during interviews and demos.

Secondary audience:

- classmates or instructors who want to understand the v1 pipeline visually,
- future contributors who need a quick mental model of the system.

## 3. Product goals

- Make the v1 pipeline understandable in under one minute.
- Show that the project is more than model training: it includes data handling,
  segmentation, deterministic geometry, and evaluation.
- Provide a polished resume artifact that can be shown locally or through a
  short demo video.
- Keep the implementation small enough to build on top of the existing v1 code.

## 4. MVP success criteria

The v2 MVP is successful when:

- a user can select a saved sample,
- the app shows the original ultrasound image,
- the app shows the target mask derived from annotation,
- the app shows the saved prediction, probability map, and thresholded mask,
- the app shows cleaned mask and ellipse overlay,
- the app includes a live threshold slider driven by exported `prob.png` files,
- the app reports predicted HC in millimeters when available,
- the app includes a contour-vs-ellipse measurement comparison whenever both
  measurements are available,
- the app includes v1 experiment summary results,
- the app clearly says: "Educational demo only. Not for clinical use.",
- the app can run locally without retraining,
- the default saved-output mode can run without raw HC18 data or checkpoints
  after a curated demo artifact bundle has been exported.

## 5. Out of scope for the first milestone

- training from the UI,
- clinical diagnosis or medical decision support,
- public upload of arbitrary medical images,
- official challenge leaderboard optimization,
- web backend or REST API deployment,
- user accounts or persistent storage,
- automatic dataset download,
- requiring checkpoints for the default demo mode.

## 6. Implementation preferences

- Use Vite + React + TypeScript for the portfolio web demo.
- Prefer saved-output static mode first for speed, reliability, and public
  deployability.
- Build the app under `frontend/`, with reusable components under
  `frontend/src/components/`.
- Port the design tokens and interactions from
  `docs/v2_demo/frontend-design-handoff.md`.
- Export curated samples to `outputs/demo_samples/`, then copy them to
  `frontend/public/samples/` for local frontend development. The stable runtime
  input is `frontend/public/samples/manifest.json`.
- Export artifact filenames expected by the design:
  `ultrasound.png`, `target.png`, `pred.png`, and `prob.png`.
- Compute contour HC during artifact export and store it in the React manifest
  as `contourHC` so the app can show the contour-vs-ellipse comparison without
  recomputing geometry in the UI.
- Generate `prob.png` during artifact export by running local checkpoint
  inference once. The frontend must not load a checkpoint at runtime.
- Keep the UI focused on stage-by-stage visual comparison.
- Keep long text out of the main app. Use concise captions and visual panels.
- Keep v1 pipeline code stable unless a demo task reveals a real bug.
- Document frontend dependencies in `frontend/package.json`. Python demo
  dependencies are only needed for artifact export and validation.

## 7. Future extensions

After saved-output MVP:

- add curated-sample live checkpoint inference through a FastAPI companion
  server,
- add an upload/select-image workflow only after curated live inference is
  stable and explicitly approved,
- add failure-case gallery,
- add a model comparison view,
- add README screenshots or an animated GIF,
- add optional HC18 challenge CSV export.
