# Fetal HC Pipeline Explorer

Public app:
`https://fetal-head-measurement.vercel.app/`

Educational demo only. Not for clinical use.

## Overview

This repository is now centered on a portfolio-ready web demo that explains how
a fetal head circumference pipeline works from segmentation to measurement.

The app turns a trained HC18 workflow into an interactive visual walkthrough:

```text
ultrasound -> target mask -> CNN probability -> thresholded mask -> ellipse fit -> HC measurement
```

It is designed for recruiters, interviewers, and ML learners who want to
understand the full pipeline, not just the final metric table.

## What The Demo Shows

- curated success, typical, and failure cases
- original ultrasound, target mask, prediction mask, and probability map
- a live threshold slider driven by exported `prob.png` artifacts
- contour-versus-ellipse circumference comparison
- per-case Dice, IoU, HD95, and HC error
- experiment summaries from the underlying v1 training runs

## Public Preview vs Local Real Mode

The public Vercel deployment uses a safe placeholder preview bundle, not real
HC18-derived sample images.

Public deployment data source:

- `frontend/public/demo-samples/`
- `frontend/public/experiments/summary.json`

Local real-artifact mode uses the generated saved-output bundle:

- `frontend/public/samples/`
- populated locally by `./start_demo.sh`

This split keeps the public site easy to review while avoiding committed
medical-image demo artifacts.

## Run Locally

Public-preview mode:

```bash
cd frontend
npm install
npm run dev
```

Real saved-output mode:

```bash
./start_demo.sh
```

`start_demo.sh` will:

1. export curated demo artifacts if they are missing
2. copy them into ignored `frontend/public/samples/`
3. start the Vite app on `http://localhost:5173`

Real local mode requires:

- local HC18 data under `data/raw/HC18/`
- the local checkpoint and run artifacts already used by the exporter

## Tech Stack

- frontend: Vite + React + TypeScript
- model/training code: PyTorch
- geometry/post-processing: OpenCV + NumPy
- hosting: Vercel static deployment

## Repository Focus

The active product is the v2 demo.

Key areas:

- `frontend/` — the deployed web app
- `docs/v2_demo/` — product plan, roadmap, deployment notes
- `scripts/export_demo_artifacts.py` — local artifact exporter
- `src/inference/live.py` — shared live-inference core for the next milestone

Archived/reference material:

- `docs/v1/` — the original v1 pipeline governance and report context

## Current Status

Completed:

- static saved-output React demo
- public Vercel production deployment
- local real-artifact export path
- live-inference core extraction for the next phase

Next:

- FastAPI live inference server
- React live-mode integration
- optional challenge-export tooling

## Docs

- [V2 project spec](docs/v2_demo/project-spec.md)
- [V2 roadmap](docs/v2_demo/roadmap.md)
- [V2 session tasks](docs/v2_demo/project-tasks.md)
- [Public deployment checklist](docs/v2_demo/public-deployment-checklist.md)
- [Live inference plan](docs/v2_demo/live-inference-plan.md)

## Data And Artifact Policy

- do not commit raw HC18 data
- do not commit local checkpoints unless explicitly approved
- `frontend/public/samples/` stays local and ignored
- public hosting should continue to use the placeholder preview unless artifact
  policy changes intentionally
