# Live Inference Plan

Date: 2026-05-02

Purpose:
Plan the post-MVP live inference extension so Claude Code can review the
architecture before implementation.

Review status:
Claude Code review has been integrated into this plan. The current version is
compatible with the React/static MVP as long as live inference stays optional,
curated-sample-first, and uses the same app-facing `Sample` contract with
asset overrides for live-generated images.

## 1. Recommendation

Build live inference as an optional mode after the static saved-output MVP is
complete.

The current React app should remain the default experience because it is fast,
stable, and deployable without raw HC18 data or checkpoints. Live inference
should add a second mode:

```text
Static replay  -> pre-generated manifest + PNGs, no backend
Live inference -> selected curated image + backend checkpoint inference
```

This keeps the resume demo dependable while adding the stronger interview
moment: "click Run live" and watch the model produce the probability map, mask,
ellipse, and HC measurement from the selected sample.

## 2. Scope

### First live milestone

Support live inference on curated samples only.

The first live version should not accept arbitrary public medical-image uploads.
It should let a viewer select one of the curated demo samples and trigger a live
run from the original ultrasound image.

Why:

- avoids public upload risk,
- lets the app reuse known pixel spacing and target HC metadata,
- keeps latency predictable,
- avoids needing to solve PHI/safety questions,
- still proves the real model pipeline is running.

Implementation constraint:
The static saved-output app must continue to run without a backend. The first
live implementation should add a second adapter path; it should not replace
manifest loading or require the backend during app startup.

### Later live milestone

Add optional local upload only after curated live inference is stable.

Upload mode would require explicit constraints:

- local-only or authenticated demo,
- no storage after request completion,
- accepted file types and size limits,
- clear disclaimer that measurements are educational only,
- no clinical claims,
- user-provided spacing or "pixel-only" mode if spacing is unknown.

## 3. What We Can Reuse

### Frontend reuse

The React frontend already has most of the visual system needed:

- `frontend/src/types/sample.ts`
  - keep the `Sample` interface as the shared app-facing contract.
- `frontend/src/components/gallery/SampleGallery.tsx`
  - reuse the selected sample and active state.
- `frontend/src/components/pipeline/PipelineStepper.tsx`
  - reuse for live progress stages.
- `frontend/src/components/pipeline/StageDetail.tsx`
  - reuse once live outputs are converted to the same asset paths or data URLs.
- `frontend/src/components/threshold/ThresholdViewer.tsx`
  - reuse if live inference returns a `prob.png` URL or same-origin data URL.
- `frontend/src/components/shared/SafetyChip.tsx`
  - keep always visible.
- `frontend/src/data/samples.ts`
  - keep static manifest loading; add a separate live API client rather than
    mixing API calls into the static loader.

Expected frontend additions:

```text
frontend/src/data/live-api.ts
frontend/src/types/live.ts
frontend/src/components/live/ModeToggle.tsx
frontend/src/components/live/LiveRunPanel.tsx
frontend/src/components/live/RunStatus.tsx
```

### Backend and v1 reuse

The Python pipeline already has the hard parts:

- `src.inference.predict.load_model_from_checkpoint`
  - load the trained Attention U-Net checkpoint.
- `src.data.dataset.HC18Dataset`
  - read image tensors, target masks, spacing, and annotation metadata.
- `src.utils.geometry.threshold_probability`
  - threshold probability maps.
- `src.utils.geometry.mask_to_measurement`
  - connected-component cleanup, ellipse fit, and HC measurement.
- `src.utils.geometry.mask_contour_length_mm`
  - contour-vs-ellipse measurement comparison.
- `src.inference.predict.save_mask`
  - save binary mask assets when returning files.
- `scripts/export_demo_artifacts.py`
  - already demonstrates the exact saved-output transform:
    image -> checkpoint logits -> sigmoid probability -> `prob.png` ->
    cleaned mask -> contour HC -> frontend manifest fields.

The live backend should not duplicate all exporter logic. It should factor the
shared single-sample path into an importable utility, then let both the exporter
and API use it.

Proposed shared module:

```text
src/inference/live.py
```

Core function:

```python
def run_live_inference(
    sample_id: str,
    *,
    checkpoint_path: Path,
    config_path: Path,
    split: str = "test",
    threshold: float = 0.5,
    device: str = "cpu",
    timeout_s: float = 30.0,
) -> LiveInferenceResult:
    ...
```

The `timeout_s` parameter should raise `TimeoutError` if the forward pass plus
geometry steps exceed the limit. CPU inference on 256×384 typically takes
~300–800 ms; 30 s is generous but prevents hung requests on overloaded hosts.

## 4. Target Architecture

```text
React frontend (Vite)
  |
  | static mode
  v
frontend/public/samples/manifest.json + PNGs

React frontend (Vite)
  |
  | live mode
  v
FastAPI backend
  |
  +-- load checkpoint once at startup
  +-- load curated sample image/metadata
  +-- run sigmoid inference
  +-- threshold probability map
  +-- cleanup largest component
  +-- fit ellipse
  +-- compute HC and contour HC
  +-- return Sample-compatible JSON + image URLs/data URLs
```

## 5. API Contract

### `GET /health`

Purpose:
Frontend/backend readiness check.

Response:

```json
{
  "ok": true,
  "model_loaded": true,
  "device": "cpu",
  "run_id": "attention_unet_local_baseline"
}
```

### `GET /live/samples`

Purpose:
Return curated sample IDs available for live inference.

Response:

```json
{
  "samples": ["296_HC", "217_HC", "663_HC", "025_HC", "793_HC", "032_HC"]
}
```

### `POST /live/infer`

Request:

```json
{
  "sample_id": "296_HC",
  "threshold": 0.5
}
```

Response:

```json
{
  "mode": "live",
  "runtime_ms": 742,
  "sample": {
    "id": "296_HC",
    "label": "Strong prediction: near-perfect HC",
    "cat": "strong",
    "split": "test",
    "summary": "Live checkpoint inference on the curated ultrasound.",
    "metrics": {
      "dice": 0.9907,
      "iou": 0.9816,
      "hd95_mm": 0.70,
      "hcErr": 0.03,
      "predHC": 191.44,
      "targetHC": 191.47
    },
    "predEllipse": {
      "cx": 198.02,
      "cy": 129.62,
      "rx": 133.68,
      "ry": 112.09,
      "rot": 1.527
    },
    "contourHC": 203.09,
    "confidence": 0.984,
    "spacingXMm": 0.2457,
    "spacingYMm": 0.2488,
    "resolution": { "w": 384, "h": 256 },
    "notes": "Generated live from checkpoint."
  },
  "assets": {
    "ultrasound": "/live/runs/abc123/ultrasound.png",
    "target": "/live/runs/abc123/target.png",
    "prob": "/live/runs/abc123/prob.png",
    "pred": "/live/runs/abc123/pred.png"
  }
}
```

### Error response schema

On validation or inference failure, `POST /live/infer` should return a 4xx or
5xx with a consistent body:

```json
{
  "error": "invalid_sample_id",
  "detail": "'999_HC' is not in the curated sample list.",
  "runtime_ms": 0
}
```

Defined error codes:

| code | HTTP | meaning |
|---|---|---|
| `invalid_sample_id` | 422 | `sample_id` not in curated list |
| `invalid_threshold` | 422 | `threshold` outside (0.0, 1.0) |
| `inference_timeout` | 504 | forward pass exceeded `timeout_s` |
| `checkpoint_not_loaded` | 503 | model failed to load at startup |
| `inference_error` | 500 | unexpected exception during forward pass |

The frontend `live-api.ts` should map these codes to user-visible messages:

```text
inference_timeout  -> "Model is taking longer than expected. Try again."
checkpoint_not_loaded -> "Live backend unavailable. Static mode still works."
```

### Asset strategy

For local development, file URLs are simplest:

```text
demo_live/.cache/live_runs/<run_id>/{ultrasound,target,prob,pred}.png
GET /live/runs/<run_id>/<asset>.png
```

For hosted free-tier deployment, data URLs may be simpler because free storage
can be ephemeral. The frontend can support both:

```typescript
type SampleAssets = {
  ultrasound: string; // URL or data URL
  target: string;
  prob: string;
  pred: string;
};
```

Then `StageDetail` and `ThresholdViewer` should accept asset overrides instead
of always deriving `/samples/<id>/<file>.png`.

**Required `StageDetail` refactor:** add an `assetOverrides` prop so live mode
can supply URLs without changing how static mode works:

```typescript
interface StageDetailProps {
  sample: Sample;
  stageIndex: number;
  assetOverrides?: SampleAssets; // undefined = static mode, derive paths from id
}
```

Static paths are derived as before when `assetOverrides` is undefined.
Live mode passes `liveRun.assets`. `ThresholdViewer` needs the same treatment
so it reads from `assetOverrides.prob` in live mode instead of
`/samples/<id>/prob.png`.

**Required adapter boundary:** keep path derivation in a small helper so all
image-consuming components use the same source:

```typescript
function getSampleAssets(sample: Sample, overrides?: SampleAssets): SampleAssets {
  return overrides ?? {
    ultrasound: `/samples/${sample.id}/ultrasound.png`,
    target: `/samples/${sample.id}/target.png`,
    prob: `/samples/${sample.id}/prob.png`,
    pred: `/samples/${sample.id}/pred.png`,
  };
}
```

This is the integration point between saved-output replay and live inference.
Components should consume `SampleAssets`; they should not know whether the
assets came from `frontend/public/samples/`, `demo_live/.cache/`, or data URLs.

Place this helper at `frontend/src/utils/assets.ts`. Import it in `StageDetail`,
`ThresholdViewer`, and `LiveRunPanel` — nowhere else should derive image paths.

## 6. Frontend Integration Plan

### State model

Add one top-level mode and live result state:

```typescript
type DemoMode = "static" | "live";

const [mode, setMode] = useState<DemoMode>("static");
const [liveRun, setLiveRun] = useState<LiveRunResult | null>(null);
const [liveStatus, setLiveStatus] = useState<"idle" | "waking" | "running" | "done" | "error">("idle");
```

Rendering rule:

```text
activeDisplaySample =
  mode === "live" && liveRun?.sample ? liveRun.sample : staticActiveSample

activeDisplayAssets =
  mode === "live" && liveRun?.assets ? liveRun.assets : derived static paths
```

### UI changes

Add a compact mode control near the active sample strip:

```text
[Static replay] [Run live]
```

When the user clicks "Run live":

1. lock the button and show progress,
2. call `POST /live/infer`,
3. animate the pipeline stages as responses arrive or after the response returns,
4. replace the displayed assets with live assets,
5. keep the threshold slider interactive against the live `prob.png`.

### Progress events

V1 can start with a single request/response. For better theatre, add server-sent
events later:

```text
preprocess -> inference -> threshold -> cleanup -> ellipse -> measurement
```

This is optional because the model should be small enough for a curated CPU
request to finish quickly.

## 7. Backend Implementation Plan

### Proposed files

```text
demo_live/
  app.py
  live_service.py
  schemas.py
  static/
  README.md
requirements-live.txt
```

### CORS configuration

The Vite frontend (port 5173) calls the FastAPI server (port 8000), which is
a cross-origin request. Add CORS middleware in `demo_live/app.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:4173",  # Vite preview
        "https://<your-vercel-slug>.vercel.app",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
```

For HF Spaces Combination 3 (Vercel → HF Space), set `CORS_ORIGINS` as a
comma-separated environment variable and read it at startup rather than
hard-coding the Vercel URL.

### Response caching

Curated-sample inference is deterministic at a fixed threshold. Cache the
result in `live_service.py` to eliminate redundant forward passes for repeated
requests (e.g., demo visitor clicks Run live multiple times):

```python
from functools import lru_cache

@lru_cache(maxsize=64)
def _cached_infer(sample_id: str, threshold: float) -> LiveInferenceResult:
    return run_live_inference(sample_id, threshold=threshold, ...)
```

The cache key is `(sample_id, threshold)`. Cache is in-process memory — it
resets on restart, which is fine for a demo. Do not cache across different
threshold values for the same sample if memory is tight; `maxsize=64` covers
six samples × ~10 threshold increments.

### Startup behavior

At startup:

1. read `outputs/runs/attention_unet_local_baseline/config.json`,
2. load `outputs/runs/attention_unet_local_baseline/best_model.pt`,
3. build an index of curated sample IDs from `docs/v2_demo/curated-samples.json`
   plus either local HC18 paths or a curated live bundle,
4. keep the model in memory,
5. use CPU by default for portability.

### Request behavior

For curated sample inference:

1. validate `sample_id` is in curated list,
2. load the sample through `HC18Dataset` in local/dev mode, or through a
   curated live bundle in hosted mode,
3. run checkpoint forward pass,
4. compute sigmoid probability map,
5. save or encode `prob.png`,
6. threshold at request threshold,
7. compute cleaned mask, ellipse, predicted HC, contour HC, confidence,
8. return `Sample`-compatible JSON plus asset URLs.

### Tests

Add backend tests before UI integration:

```text
tests/test_live_inference_contract.py
tests/test_live_api.py
```

Minimum assertions:

- model-loading function can be imported without starting FastAPI,
- single-sample live output includes all `Sample` fields,
- `prob` asset has same resolution as ultrasound,
- `predEllipse.rot` is radians,
- safety text remains present in frontend mode.

## 8. Artifact And Checkpoint Policy

Local developer live mode can reuse the v1 dataset and run outputs:

```text
outputs/runs/attention_unet_local_baseline/best_model.pt
outputs/runs/attention_unet_local_baseline/config.json
data/raw/HC18/training_set/
docs/v2_demo/curated-samples.json
```

Hosted live mode should not assume the raw HC18 dataset is present.

Therefore `src/inference/live.py` should separate the inference transform from
the input source:

```text
LiveInputSource
  local_hc18_dataset -> used for development and exporter parity
  curated_bundle     -> used for hosted/private live demos
```

The live service should call the same transform in both cases. This prevents the
hosted path from depending on `data/raw/HC18/training_set/` while still letting
local development reuse `HC18Dataset`.

For a public hosted demo, choose one of these policies:

### Option A - Curated live bundle

Bundle only:

- six curated original ultrasound images,
- six target masks,
- pixel spacing and target HC metadata,
- trained checkpoint.

The backend runs live inference on only those curated images.

Pros:
Small and reliable.

Cons:
Requires explicit user approval before publishing generated medical-image
artifacts and checkpoint weights.

### Option B - Private/local live only

Host only the static app publicly. Run live inference locally during interviews
or record a short video/GIF.

Pros:
No artifact-distribution problem.

Cons:
Public link cannot run live inference by itself.

### Option C - Private Hugging Face Space

Use a protected/private Hugging Face Space for live inference, and share it only
when needed.

Pros:
Closest to the real live experience without making artifacts broadly public.

Cons:
Access control may be less convenient for recruiters.

Recommendation:
Use Option B until the static MVP is portfolio-polished. Then decide between
Option A and C.

## 9. Hosting Options

Checked against official docs on 2026-05-02.

### Vercel

Best use:
Host the static Vite frontend.

Official docs:

- Vercel limits overview: https://vercel.com/docs/limits/overview
- Vercel functions limitations: https://vercel.com/docs/functions/limitations

Relevant current limits:

- Hobby projects can deploy static frontend builds.
- Hobby static file upload limit is documented as 100 MB.
- Hobby functions have 2 GB memory.
- Python function uncompressed bundle size is documented as 500 MB.
- Hobby function duration can be enough for small requests, but cold starts and
  PyTorch packaging are the risk.

Assessment:
Vercel is a good frontend host. It is not my recommended live PyTorch inference
host because PyTorch plus OpenCV plus model files can strain serverless bundle
limits and cold starts. It could work for a tiny CPU model, but it is the brittle
path.

### GitHub Pages

Best use:
Host a static Vite build only.

Official docs:

- GitHub Pages limits: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits

Relevant current limits:

- Available for public repositories on GitHub Free.
- Published Pages sites may be no larger than 1 GB.
- Soft bandwidth limit is documented as 100 GB per month.
- Pages is static hosting. It does not run a Python checkpoint inference server.

Assessment:
GitHub Pages is fine for the static portfolio page. It cannot host live
inference directly.

### Hugging Face Spaces

Best use:
Host the live ML demo backend, or host a full-stack Docker demo.

Official docs:

- Spaces overview: https://huggingface.co/docs/hub/spaces-overview
- Spaces GPU/hardware: https://huggingface.co/docs/hub/spaces-gpus
- Spaces storage: https://huggingface.co/docs/hub/spaces-storage
- Pricing: https://huggingface.co/pricing

Relevant current limits:

- CPU Basic is listed as free.
- CPU Basic includes 2 vCPU, 16 GB RAM, and 50 GB non-persistent disk.
- Free hardware sleeps when inactive and restarts when visited.
- Paid GPUs are available if CPU latency is too slow.
- Persistent storage is a paid add-on; free storage is ephemeral.

Assessment:
Hugging Face Spaces is the best public live-inference option for this project.
It is designed for ML demos and can run Python apps. CPU Basic should be enough
to test curated single-sample inference, especially because the model is small
and the image size is 256×384.

**Cold start and sleep behavior (important for demo reliability):**

- Free CPU Basic Spaces sleep after ~15–20 minutes of inactivity.
- Wake-up on the first request takes approximately 20–30 seconds for a Docker
  Space that must reload the PyTorch checkpoint into memory.
- During wake-up, all API calls block or timeout.
- **Mitigation for demos:** the React frontend should show a distinct
  "Backend waking up, please wait…" state during the wake delay. The
  `GET /health` endpoint provides a readiness check. Poll it every 3 s
  until `model_loaded: true` before enabling the "Run live" button.
- **Mitigation for interviews:** open the Space URL 2–3 minutes before the
  demo to pre-warm it.
- Persistent storage add-on is not needed — the checkpoint and curated images
  can be bundled in the Docker image (user approval required before publishing).

### Recommended deployment combinations

#### Combination 1 - safest portfolio path

```text
Vercel or GitHub Pages -> static React demo
Local FastAPI backend  -> live mode for interviews/video
```

Use this first.

#### Combination 2 - best public live demo

```text
Hugging Face Space -> Docker/FastAPI backend + built React frontend
```

Use this if we decide it is acceptable to package curated images and checkpoint
for public or protected hosting.

#### Combination 3 - split public frontend and ML backend

```text
Vercel frontend -> calls Hugging Face Space API
```

This is also workable. It needs CORS configuration, a backend URL environment
variable, and graceful UI handling for HF Space cold starts.

## 10. Proposed Sessions

**Session reconciliation:** `docs/v2_demo/project-tasks.md` now mirrors this
breakdown. Treat V2.S7.1–S7.4 as the authoritative live-inference sequence.

### V2.S7.1 - Live Inference Core

Goal:
Create a reusable Python single-sample live inference function.

Expected files:

```text
src/inference/live.py
tests/test_live_inference_contract.py
```

Key scope:

- extract the single-sample transform currently demonstrated by
  `scripts/export_demo_artifacts.py`,
- support a local HC18 input source first,
- define the interface so a curated bundle source can be added without changing
  the FastAPI or React contracts,
- keep exporter behavior stable while sharing the new utility.

Verification:

```bash
.venv/bin/python -m pytest tests/test_live_inference_contract.py
```

Done criteria:

- one curated sample can run live inference locally,
- output has the same fields as frontend `Sample`,
- generated `prob`, `pred`, and geometry outputs are shape-consistent.

### V2.S7.2 - FastAPI Backend

Goal:
Expose live inference over HTTP.

Expected files:

```text
demo_live/app.py
demo_live/live_service.py
demo_live/schemas.py
requirements-live.txt
tests/test_live_api.py
```

Verification:

```bash
uvicorn demo_live.app:app --reload --port 8000
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/live/infer ...
```

Done criteria:

- backend loads checkpoint once,
- `POST /live/infer` works for at least one curated sample,
- saved-output frontend still works without backend.

### V2.S7.3 - React Live Mode

Goal:
Add mode toggle and live result rendering.

Expected files:

```text
frontend/src/data/live-api.ts
frontend/src/types/live.ts
frontend/src/components/live/ModeToggle.tsx
frontend/src/components/live/LiveRunPanel.tsx
```

Verification:

```bash
cd frontend && npm run build
npm run dev
```

Manual checks:

- static mode still works with no backend,
- live mode shows backend unavailable state if server is down,
- live mode shows a backend waking/readiness state when `/health` is not ready,
- live mode runs one curated sample when backend is up,
- threshold viewer works on live `prob.png`.

### V2.S7.4 - Live Deployment Packaging

Goal:
Choose public/private hosting and package it.

Expected files, depending on option:

```text
Dockerfile
demo_live/README.md
vercel.json or Space metadata
```

Verification:

- deployed frontend URL works,
- deployed or local live backend health check works,
- README clearly explains static vs live mode.

## 11. Risks And Mitigations

### Risk: Live backend makes the main demo fragile

Mitigation:
Static replay remains default. Live mode is optional and has a clear "backend
offline" state.

### Risk: PyTorch CPU latency is slow

Mitigation:
Cache model at startup, restrict to curated samples, run at 256x384, benchmark
CPU first, then consider Hugging Face paid GPU only if necessary.

### Risk: Hosting checkpoint and medical-image samples publicly

Mitigation:
Do not publish checkpoint or curated medical-image artifacts until user
explicitly approves. Use local live mode or protected HF Space first.

### Risk: Vercel serverless packaging fails

Mitigation:
Do not use Vercel for live PyTorch inference. Use Vercel only for static
frontend, or call a Hugging Face Space backend.

### Risk: The live and static data contracts drift

Mitigation:
Define one `Sample` contract and add tests that validate both static manifest
samples and live API samples against the same required fields.

## 12. Design Decisions (Resolved)

These were open questions during planning. Answers recorded here so future
sessions do not re-litigate them.

**Q1 — Backend directory name**

Use `demo_live/` instead of `backend/`.

Rationale: `backend/` implies a general-purpose production API. This is a demo
companion server, not a clinical system. `demo_live/` keeps the purpose clear
and avoids any impression that it is the project's primary backend.

**Q2 — Asset strategy: data URLs vs file URLs**

Support both via the `SampleAssets` type (each field is a `string` — either a
path URL or a `data:image/png;base64,...` string). Default to file URLs in
local mode, data URLs for hosted mode where ephemeral storage cannot be
assumed.

The frontend must never assume an asset URL format. `ThresholdViewer` and
`StageDetail` should accept the URL string and let the browser or canvas API
handle both forms.

**Q3 — Refactor exporter before building backend?**

Yes, refactor `scripts/export_demo_artifacts.py` first (in V2.S7.1) to extract
the single-sample path into `src/inference/live.py`. This is not extra work —
the exporter already demonstrates the exact transform; extracting it prevents
the backend from duplicating or diverging from the exporter's behavior.

**Q4 — Portfolio deployment priority**

Use Combination 1 first (static public + local live mode + recorded video).

This gives a deployable portfolio link immediately and a compelling live demo
for interviews without requiring a decision on artifact publishing. Defer
Combination 2 or 3 until after the static MVP is polished and there is explicit
approval to publish the checkpoint and curated images.

**Q5 — Publishing checkpoint and curated images**

Do not publish until explicitly approved.

The checkpoint is a trained model on a medical dataset. Curated images are
derived from HC18. Neither should appear in a public repository or hosted
service without a deliberate distribution decision. Use local live inference or
a private/protected HF Space until that decision is made.

## 13. Preferred Path

The static MVP is on track with the React + Vite frontend (React pivot
confirmed 2026-05-01). Sessions V2.S3–S6 build the deployed static demo.
Live inference begins in V2.S7 only after the static demo is portfolio-ready.

Recommended sequence:

1. Complete V2.S2 (artifact export with `prob.png`) — prerequisite for everything.
2. Complete V2.S3–S5 (React scaffold, core UI, dashboard) — static demo is the
   primary portfolio artifact.
3. Complete V2.S6 (deploy to Vercel or GitHub Pages + README) — get a public link.
4. **Record a short demo video** of the deployed static app for LinkedIn/README.
   This is usable even if live inference never ships.
5. Implement V2.S7.1 (refactor exporter, create `src/inference/live.py`) locally.
6. Implement V2.S7.2 (FastAPI backend under `demo_live/`) locally.
7. Add the React live toggle in V2.S7.3.
8. Record a second video showing live inference running locally — add to README.
9. Decide on Hugging Face Space after explicit approval to publish checkpoint
   and curated images.

This gives the strongest portfolio sequence with clear stopping points:

```text
V2.S6 deployed static  →  V2.S7.3 local live toggle  →  optional HF Space
      ↓                              ↓
 public link now          interview-ready live demo
```

If time is tight before June 9 OPT deadline, stopping at the V2.S6 deployed
static demo is a strong portfolio artifact on its own.
