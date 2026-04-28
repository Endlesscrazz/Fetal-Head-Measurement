# V2 Demo Decisions

This file records durable, non-trivial v2 demo decisions. Use append-only
entries unless correcting an explicit error.

Each entry should include:

- date,
- decision,
- rationale,
- alternatives considered,
- impact on future work.

## 2026-04-28 - V2 demo branch

Decision:
Create a `v2-demo` branch from the completed v1 checkpoint on `main`.

Rationale:
V1 is now a stable course-submission baseline. V2 should evolve as a portfolio
demo without blurring the history of the submitted pipeline.

Alternatives considered:
Continuing all work on `main`; creating a separate repository for the demo.

Impact on future work:
Demo planning and implementation should happen on `v2-demo` until it is ready
to merge or present.

## 2026-04-28 - Streamlit as preferred demo framework

Decision:
Use Streamlit as the default framework for the v2 educational demo.

Rationale:
The demo is a visual, Python-native ML pipeline explorer with images, sliders,
tables, and plots. Streamlit supports that workflow with minimal application
infrastructure.

Alternatives considered:
Gradio for a simpler model endpoint demo; React/FastAPI for a more custom web
app.

Impact on future work:
The first app implementation should target a local Streamlit workflow and add
dependencies only when the implementation task begins.

## 2026-04-28 - Saved-output-first demo strategy

Decision:
Build the first v2 demo milestone from saved v1 artifacts before adding live
checkpoint inference.

Rationale:
Saved-output mode gives the fastest reliable portfolio demo, avoids checkpoint
distribution issues, and keeps the first app milestone focused on explaining
the pipeline visually.

Alternatives considered:
Starting with live checkpoint inference; starting with HC18 challenge export.

Impact on future work:
The first demo implementation should use curated saved samples and a manifest.
It should not require retraining, raw data scanning, or checkpoint loading in
the default path.

## 2026-04-28 - Live inference as second milestone

Decision:
Treat live checkpoint inference as a later v2 milestone behind a swappable
adapter interface.

Rationale:
Live inference is valuable for demo polish but adds checkpoint handling,
preprocessing, runtime, and failure-mode complexity. A replaceable adapter lets
saved-output and live modes share the same UI concepts.

Alternatives considered:
Making live inference mandatory in the first app; never adding live inference.

Impact on future work:
The v2 architecture should separate app-stage data from the source that creates
it, so saved artifacts and live model outputs can feed the same visual
components.

## 2026-04-28 - Root v2 contract and archived v1 governance

Decision:
Use root `AGENTS.md` for the current v2 demo operating contract, archive v1
governance under `docs/v1/`, and keep v2 decisions in
`docs/v2_demo/DECISIONS.md`.

Rationale:
The active branch is now v2-focused. Root instructions should match the active
work, while v1 rules and decisions remain available for maintenance.

Alternatives considered:
Keeping the combined v1/v2 root contract; leaving all decisions in a root
`DECISIONS.md`; keeping the v2 contract under `docs/v2_demo/AGENTS.md`.

Impact on future work:
Future agents should start with root `AGENTS.md` for demo tasks and consult
`docs/v1/` only when touching v1 pipeline behavior.
