# V2 Demo Decisions

This file records durable, non-trivial v2 demo decisions. Use append-only
entries unless correcting an explicit error.

Each entry should include:

- date,
- decision,
- rationale,
- alternatives considered,
- impact on future work.

## 2026-05-03 - Public static deployment now serves the curated real HC18-derived bundle

Decision:
Approve Path A for the static public portfolio site. The production Vercel app
should prefer `frontend/public/samples/manifest.json` and serve the curated
real HC18-derived saved-output bundle publicly, while keeping
`frontend/public/demo-samples/` as a committed fallback preview bundle.

Rationale:
The HC18 licensing evidence is favorable for a tiny attributed educational
subset, and the static portfolio experience is meaningfully stronger when the
live site shows the real exported pipeline artifacts rather than placeholders.
This change preserves the saved-output-first architecture and does not require
publishing raw HC18 files or checkpoints.

Alternatives considered:
Keeping the public site on placeholder previews; jumping directly to live
inference before strengthening the static public artifact; publishing the raw
dataset or checkpoint.

Impact on future work:
- `frontend/public/samples/` is now an intentional public/runtime mirror rather
  than a local-only ignored directory.
- `outputs/demo_samples/` remains the generated source of truth.
- The app should try `/samples/manifest.json` first on all hosts and fall back
  to `/demo-samples/manifest.json` only when the curated real bundle is absent.
- README and deployment docs must include attribution and explain the curated
  derivative-bundle policy clearly.

## 2026-05-03 - Live inference core returns Sample-compatible data plus in-memory assets

Decision:
For `V2.S7.1`, put the reusable live inference transform in
`src/inference/live.py`. The core returns a frontend `Sample`-compatible dict
and in-memory asset arrays (`ultrasound`, `target`, `prob`, `pred`). Later API
or hosting layers will decide whether those arrays become file URLs or data
URLs.

Rationale:
This keeps the model/geometry path independent from FastAPI and React. It also
lets the existing exporter reuse shared helpers while preserving the static
saved-output bundle contract.

Alternatives considered:
Writing the live inference path directly inside FastAPI; having the core write
files unconditionally; returning only numeric fields and leaving image creation
to the API layer.

Impact on future work:
- `demo_live/` can load the model once and call `LiveInferenceRunner`.
- The API can map in-memory assets to local files for development or data URLs
  for hosted demos.
- The frontend should still consume assets through the planned `SampleAssets`
  override helper.

## 2026-05-03 - Public deployment uses a non-medical preview fallback

Decision:
For V2.S6, keep the real HC18 sample artifact bundle local and ignored, and add
a committed non-medical placeholder sample set under `frontend/public/demo-samples/`
for public static hosting. The frontend first tries `/samples/manifest.json` for
local real saved-output mode, then falls back to `/demo-samples/manifest.json`
when real sample artifacts are absent.

Rationale:
The portfolio site should load on Vercel or GitHub Pages without committing or
publishing generated medical-image artifacts. A public-safe preview keeps the UI
reviewable while preserving the stricter artifact policy for the actual HC18
sample bundle.

Alternatives considered:
Committing curated HC18 PNGs directly; publishing a demo artifact zip before a
distribution decision; letting the public site show a manifest error; requiring
raw HC18 data or checkpoints at app startup.

Impact on future work:
- Public hosting can be configured immediately with `vercel.json`.
- Local reviewers with HC18 artifacts still get the real saved-output demo via
  `./start_demo.sh`.
- README must clearly distinguish public preview mode from local real-artifact
  mode.
- A public URL can be added after the repository is connected to Vercel or
  GitHub Pages.

## 2026-05-02 - Curated live inference is the V2.S7 path

Decision:
Implement live inference, when started, as an optional curated-sample mode after
the static React MVP. Static saved-output replay remains the default. The first
live path uses a FastAPI companion server under `demo_live/`, returns data
compatible with the React `Sample` interface, and sends live image assets
through URL/data-URL overrides. Arbitrary public upload is not part of the first
live milestone.

Rationale:
Curated live inference gives the strongest interview moment while preserving the
reliability of the static portfolio demo. It lets the backend reuse known pixel
spacing, target masks, and sample metadata, and avoids turning the project into
a public medical-image upload/measurement service.

Alternatives considered:
Making live inference mandatory before deployment; adding public upload first;
using Vercel serverless for PyTorch inference; committing or deploying curated
medical-image bundles and checkpoints by default.

Impact on future work:
- `docs/v2_demo/live-inference-plan.md` is the planning source for `V2.S7`.
- `V2.S7` is split into live core, FastAPI server, React live mode, and optional
  deployment packaging sub-sessions.
- Public checkpoint or curated-image hosting requires explicit user approval.
- Vercel/GitHub Pages remain the static frontend hosting path; Hugging Face
  Spaces is the preferred candidate if a hosted live ML backend is approved.

## 2026-05-01 - Claude Design pivot is the current MVP direction

Decision:
Treat the Claude Design handoff as the current portfolio MVP direction and
standardize the app plan on a Vite + React + TypeScript static frontend.

Rationale:
The React design gives the project a stronger resume artifact than the first
Streamlit prototype: sticky navigation, guided tour, visual gallery,
canvas-based thresholding from `prob.png`, contour/ellipse controls, and a
research dashboard that can be deployed as a static site. The user explicitly
did not like the original design and asked to align the plan with the Claude
Design output before continuing.

Alternatives considered:
Continuing the Streamlit implementation; embedding custom JavaScript in
Streamlit; rebuilding the design in a heavier Next.js app.

Impact on future work:
- Root governance and v2 docs now point to React/Vite for the MVP.
- Existing Streamlit files under `demo/` are superseded reference code, not the
  implementation path for the portfolio demo.
- The already-exported Streamlit artifact bundle must be revised to the React
  contract before frontend work continues.
- The current curated sample set in `docs/v2_demo/curated-samples.json`
  remains authoritative; design placeholder sample IDs and metrics are not.
- Live inference moves to an optional FastAPI-backed post-MVP milestone.

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

Superseded:
This framework decision was superseded by the 2026-05-01 Claude Design pivot.

Historical decision:
Use Streamlit as the default framework for the v2 educational demo.

Rationale:
The demo is a visual, Python-native ML pipeline explorer with images, sliders,
tables, and plots. Streamlit supports that workflow with minimal application
infrastructure.

Alternatives considered:
Gradio for a simpler model endpoint demo; React/FastAPI for a more custom web
app.

Historical impact:
The original app implementation targeted a local Streamlit workflow. Current
work should follow the newer React/Vite decision above.

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

## 2026-05-01 - React + Vite frontend replaces Streamlit

Decision:
Replace the Streamlit-based demo plan with a Vite + React + TypeScript static
single-page app, porting the design from the Claude Design handoff at
`/Users/shreyas/Downloads/design_handoff_fetal_hc_explorer/`.

Rationale:
The design handoff delivered a high-fidelity React prototype with interactions that
are not achievable in Streamlit: canvas-based real-time probability map thresholding
(`ThresholdViewer`), SVG contour/ellipse overlays with morph animation
(`ContourEllipse`), scrollspy navigation, and an animated pipeline stepper. The
static-output MVP requires no Python backend — the frontend reads `manifest.json`
and PNG assets from `public/samples/`, making it deployable to Vercel or GitHub Pages
without a running server.

Alternatives considered:
Keeping Streamlit with custom HTML/JS injection (too limited for canvas getImageData
and smooth animation); building a Gradio app (better than Streamlit but still
constrained); building a Next.js app (heavier than needed for a static MVP).

Impact on future work:
- Sessions V2.S3 (data layer), V2.S4 (pipeline explorer), V2.S5 (dashboard) are
  now React implementation sessions, not Streamlit.
- `requirements-demo.txt` is no longer the primary dependency file; `frontend/package.json` is.
- The `demo/` Python directory is removed from scope; replaced by `frontend/`.
- All frontend implementation details live in `docs/v2_demo/frontend-design-handoff.md`.
- The Python `DemoSample` dataclass is replaced by the TypeScript `Sample` interface.

## 2026-05-01 - V2.S2 export script must generate prob.png via checkpoint inference

Decision:
The artifact export script (V2.S2) must load `best_model.pt` and run a forward
pass to generate `prob.png` (raw sigmoid output as uint8 grayscale PNG) for each
curated sample, in addition to copying/rendering the other static artifacts.

Rationale:
The `ThresholdViewer` — the hero interactive element of the frontend — requires
pixel-level probability values from `prob.png` to re-threshold in canvas. v1 never
saved raw probability maps; it only saved thresholded binary masks. There is no
alternative source for this data. The checkpoint is already committed at
`outputs/runs/attention_unet_local_baseline/best_model.pt`.

Alternatives considered:
Synthesising fake probability maps (would break the educational value of the
interaction — users would be exploring noise, not real model output); skipping the
threshold feature (eliminates the strongest interactive element); saving prob.png
during v1 training reruns (not feasible — v1 is frozen).

Impact on future work:
V2.S2 now requires the checkpoint to be present locally. The saved-output app still
runs without the checkpoint after export — `prob.png` is a pre-generated artifact,
not generated at app runtime.

## 2026-05-01 - Sample category key standardized to 'failure'

Decision:
Use `'failure'` as the category key for edge/failure cases in manifest.json and
the TypeScript Sample type, not `'edge'` as the design prototype used.

Rationale:
'failure' is more accurate (these cases have real measurable failure modes) and
was the term used consistently in all prior v2 planning docs.

Impact on future work:
The gallery filter tab label should read "Failure" or "Edge / Failure". Update
`SampleGallery` filter tabs accordingly.

## 2026-05-01 - Stable demo app and artifact contracts

Superseded:
This Streamlit entrypoint decision is superseded by the 2026-05-01 Claude
Design pivot. The current app entrypoint is the future React app under
`frontend/`; `demo/app.py` remains prototype/reference code.

Historical decision:
Use `demo/app.py` as the Streamlit entrypoint, organize reusable UI under
`demo/components/`, organize data-loading adapters under `demo/adapters/`, and
use `outputs/demo_samples/manifest.json` as the saved-output app input.

Rationale:
The v2 plan needed concrete file paths before implementation. A fixed app
entrypoint and manifest path make run instructions, validation scripts, and
future live-inference adapters easier to align.

Alternatives considered:
Top-level `streamlit_app.py`; `app/main.py`; reading directly from
`outputs/runs/<run_id>/` at app startup.

Historical impact:
`V2.P2.5` should export a demo bundle into `outputs/demo_samples/`, and the
old Streamlit `V2.P3` would have launched with `streamlit run demo/app.py`.

## 2026-05-01 - DemoSample app-facing interface

Superseded:
The Python `DemoSample` interface is superseded for the MVP by the TypeScript
`Sample` interface in `docs/v2_demo/architecture.md` and
`docs/v2_demo/frontend-design-handoff.md`.

Historical decision:
Saved-output mode and future live-inference mode should both return the same
app-facing `DemoSample`-style object described in
`docs/v2_demo/architecture.md`.

Rationale:
The UI should not care whether a sample came from saved PNG/JSON files or live
checkpoint inference. A shared contract keeps live inference as an additive
milestone instead of a UI rewrite.

Alternatives considered:
Letting each component read CSVs and image files directly; creating separate
saved-output and live-inference UI pages.

Historical impact:
The saved-output adapter was implemented first for the Streamlit prototype.
Current React work should conform to the TypeScript `Sample` interface instead.

## 2026-05-01 - Local generated demo bundle before distribution

Decision:
Treat `outputs/demo_samples/` as a generated local artifact bundle for the first
MVP. Do not commit raw HC18 images, checkpoints, or generated medical-image demo
bundles without explicit user approval.

Rationale:
The demo needs raw-data-free curated artifacts, but the repository policy still
protects raw HC18 data and large/generated artifacts. Keeping export local first
allows the React app to be built and verified before choosing a public
distribution method.

Alternatives considered:
Committing curated PNG samples directly; requiring raw HC18 data at app startup;
requiring checkpoints in the default app mode.

Impact on future work:
Portfolio polish must choose a distribution path, such as a GitHub Release zip
or screenshots/GIFs, before advertising the demo as clone-and-run.

## 2026-05-01 - Machine-readable curation and contour HC export

Decision:
Use `docs/v2_demo/curated-samples.json` as the machine-readable curated sample
input for export, keep `docs/v2_demo/curated-samples.md` as human rationale,
and compute contour HC during artifact export from each cleaned mask. For the
React manifest, expose this value as `contourHC`.

Rationale:
Parsing Markdown in exporter code is brittle. The contour-vs-ellipse comparison
is a core demo feature, but v1 prediction and evaluation CSVs do not contain a
per-sample contour HC value.

Alternatives considered:
Parsing `curated-samples.md`; passing only repeated `--sample-id` arguments;
leaving contour HC null until the UI session; recomputing contour HC in the
frontend.

Impact on future work:
`V2.S1` should write both curated sample files. `V2.S2` should read the JSON,
allow explicit `--sample-id` overrides for tests, require raw HC18 and the
checkpoint only for export, and store computed contour HC as `contourHC` in the
React manifest.
