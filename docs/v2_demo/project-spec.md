# V2 Demo Project Specification

## 1. Project summary

Build an interactive Streamlit demo that turns the completed v1 fetal head
circumference pipeline into a visual ML learning tool.

The app should help a user understand this sequence:

```text
ultrasound image -> target mask -> CNN prediction -> mask cleanup -> ellipse fit -> HC measurement
```

The first milestone uses saved v1 outputs. The app should be designed so live
checkpoint inference can be added later without rewriting the UI.

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
- the app shows the saved prediction or thresholded mask,
- the app shows cleaned mask and ellipse overlay,
- the app reports predicted HC in millimeters when available,
- the app includes a contour-vs-ellipse measurement comparison where feasible,
- the app includes v1 experiment summary results,
- the app clearly says: "Educational demo only. Not for clinical use.",
- the app can run locally without retraining.

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

- Use Streamlit for the first web demo.
- Prefer saved-output mode first for speed and reliability.
- Keep the UI focused on stage-by-stage visual comparison.
- Keep long text out of the main app. Use concise captions and visual panels.
- Keep v1 pipeline code stable unless a demo task reveals a real bug.

## 7. Future extensions

After saved-output MVP:

- add live checkpoint inference,
- add an upload/select-image workflow,
- add probability heatmaps,
- add failure-case gallery,
- add a model comparison view,
- add README screenshots or an animated GIF,
- add optional HC18 challenge CSV export.
