# Production and Visualization Roadmap

Date: 2026-05-03

Purpose:
Document the two deployment paths, how to make live inference production-grade
without cost, and a research-backed set of visualization improvements to make
the demo meaningfully better than a generic ML project page.

Current project status (as of 2026-05-03):
- V2.S0 through V2.S6 are complete. The static MVP is live at
  https://fetal-head-measurement.vercel.app/
- V2.S7 is in_progress: V2.S7.1 (live inference core) is done; V2.S7.2–S7.4
  (FastAPI server, React live mode, deployment) are todo.
- Path A is now implemented locally: the app prefers `/samples/manifest.json`
  on every host, `frontend/public/samples/` is intended for the committed
  curated public bundle, and `frontend/public/demo-samples/` remains as a
  fallback preview bundle until the real bundle is absent.

---

## 0. Decision Gates Before Implementation

Before following either deployment path, the project needs explicit answers to
these policy and architecture questions:

1. **Public real artifacts**
   Are we willing to publish six curated HC18-derived ultrasound cases
   (`ultrasound.png`, `target.png`, `pred.png`, `prob.png`) on a public website?
   The latest Zenodo HC18 dataset record lists a CC BY 4.0 license, which is a
   strong signal that reuse and redistribution with attribution are allowed.
   At this point the blocker is less "can we legally reuse anything at all" and
   more "do we want this project to publicly republish a tiny curated derivative
   bundle, with proper attribution and scope notes?"

2. **Public checkpoint**
   Are we willing to publish the trained checkpoint publicly, or should live
   inference remain local/private/demo-only even if the static site uses real
   curated artifacts?

3. **Public live inference vs demo-grade live inference**
   Is the goal for live inference a stable public feature, or a high-quality
   interview/demo workflow that can be started on demand?

4. **One-storage architecture**
   If real curated assets become public, should the static site and future live
   backend read from the same object store, or should the static public site and
   live backend remain intentionally separate?

Current recommendation:

- treat public real artifacts as approved for the curated static portfolio demo
- treat public checkpoint publication as a separate, higher-risk decision
- keep the public static site and live backend decoupled until live-hosting
  decisions are explicitly approved

Why this matters:

- The current repo intentionally keeps `frontend/public/samples/` local-only.
- Reversing that policy changes both the public artifact story and the hosting
  architecture.
- The static Vercel site can be truly public today; the live backend has
  different security, cost, and reliability constraints.

Evidence reviewed:

- HC18 challenge page points to a public Zenodo dataset and asks users to cite
  both the paper and dataset.
- The paper states the ultrasound data has been made available through the
  challenge and Zenodo.
- The Zenodo HC18 dataset record lists the dataset license as
  Creative Commons Attribution 4.0 International (CC BY 4.0).
- Zenodo's own license guidance says CC BY 4.0 records may be reused, modified,
  and distributed with attribution.
- Taken together, the licensing evidence is favorable for publishing a very
  small curated educational derivative bundle with attribution.
- The remaining decision is product/presentation policy: whether we want the
  public portfolio site to include those real curated artifacts.

---

## 1. Two Deployment Paths

### Path A — Real Artifacts in the Static Demo

**What this path does:**
The six curated sample images (ultrasound, target mask, prediction mask, probability
map) are committed directly to the repo and deployed on Vercel alongside the app.
The ThresholdViewer, ContourEllipse, and MetricsPanel all work on real HC18-derived
data with no backend required.

**Current state:**

| Item | Status |
|---|---|
| Vercel deployment live | done — `https://fetal-head-measurement.vercel.app/` |
| All 6 real sample artifacts generated | done — `frontend/public/samples/` |
| Real manifest.json with correct metrics | done — 6 samples, real Dice/HC values |
| Artifact bundle size | 1.4 MB total (trivially small for Vercel) |
| Preferred public manifest path | `/samples/manifest.json` on all hosts |
| Fallback public manifest path | `/demo-samples/manifest.json` |
| Real images committed to repo | ready in workspace; commit/push required for deploy |

**What's needed for Path A:**

1. Commit and push `frontend/public/samples/` so Vercel can actually serve the
   curated real bundle.

2. Redeploy Vercel and verify the live site is rendering from
   `/samples/manifest.json`.

3. Keep attribution in the app footer and README, and keep
   `frontend/public/demo-samples/` as a fallback bundle rather than deleting it.

**Effort:** low — mostly repo sync + redeploy.
**Risk:** low. The main policy decision has already been made; remaining work is
shipping and verification.

---

### Path B — Live Inference

**What this path does:**
A "Run live" toggle in the React app sends a selected sample ID to a FastAPI
backend, which runs the checkpoint forward pass and returns the same `Sample`
JSON and image assets. The ThresholdViewer and StageDetail components render the
live outputs via `assetOverrides` — no duplicate UI.

**Current state:**

| Item | Status |
|---|---|
| `src/inference/live.py` — shared inference core | done (V2.S7.1) |
| Contract tests in `tests/test_live_inference_contract.py` | done |
| `demo_live/` FastAPI server | NOT STARTED (V2.S7.2) |
| React live mode toggle + RunStatus | NOT STARTED (V2.S7.3) |
| `frontend/src/utils/assets.ts` helper | NOT STARTED |
| Backend hosting | NOT DECIDED |

**What's needed for Path B:**

Backend (V2.S7.2):
- `demo_live/app.py` — FastAPI with CORS, startup checkpoint load
- `demo_live/live_service.py` — wraps `run_live_inference`, caches by `(sample_id, threshold)`
- `demo_live/schemas.py` — request/response Pydantic models, error codes
- `requirements-live.txt`
- `tests/test_live_api.py`

Frontend (V2.S7.3):
- `frontend/src/utils/assets.ts` — `getSampleAssets(sample, overrides?)` helper
- `frontend/src/types/live.ts` — `liveStatus: "idle"|"waking"|"running"|"done"|"error"`
- `frontend/src/data/live-api.ts` — `POST /live/infer`, `GET /health` polling
- `frontend/src/components/live/ModeToggle.tsx`
- `frontend/src/components/live/RunStatus.tsx`
- `frontend/src/components/live/LiveRunPanel.tsx`
- `StageDetail` and `ThresholdViewer`: add `assetOverrides?: SampleAssets` prop

Hosting decision (V2.S7.4):
See Section 2 — Google Colab Pro is the strongest no-cost option for a GPU backend.

**Effort:** 8–14 hours of implementation + hosting decision.
**Risk:** Backend cold start UX, CORS config, artifact publication policy.

---

## 2. Making Live Inference Demo-Ready at Low Cost

### 2.1 Google Colab Pro as the Live Inference Demo Backend

This is the single biggest demo-workflow upgrade you can make. Colab Pro gives a T4 GPU (16 GB
VRAM), longer session runtimes, and 1 TB Google Drive storage. With `pyngrok`, any
FastAPI server running in a Colab notebook can be exposed as a public HTTPS URL
in two lines of code.

**Why this is better than Hugging Face Spaces for interview/demo use:**

| Factor | HF Spaces CPU Basic (free) | Colab Pro T4 |
|---|---|---|
| Hardware | 2 vCPU, 16 GB RAM | T4 GPU, 16 GB VRAM + 12 GB RAM |
| Inference speed | ~400–800 ms CPU | ~20–50 ms GPU |
| Cold start | 20–30 s sleep wake | Pre-warm in notebook before demo |
| Storage | 50 GB non-persistent | 1 TB Google Drive (persistent) |
| Cost | Free | You already pay for Pro |
| Control | Limited — Docker redeploy | Full — just re-run a cell |

Important caveat:
This is best treated as a **demo-grade hosted backend**, not a stable production
service. The URL rotates, the session must be started manually, the runtime can
expire, and the frontend/backend integration is awkward for a public website.

**How the Colab backend works:**

```python
# In a Colab notebook cell:
from pyngrok import ngrok
import uvicorn
import threading

# Mount checkpoint from Google Drive (persistent across sessions)
from google.colab import drive
drive.mount('/content/drive')
CHECKPOINT = '/content/drive/MyDrive/fetal-hc/best_model.pt'

# Start FastAPI
def run():
    uvicorn.run("demo_live.app:app", host="0.0.0.0", port=8000)

thread = threading.Thread(target=run, daemon=True)
thread.start()

# Expose public URL
tunnel = ngrok.connect(8000, "http")
print("Backend URL:", tunnel.public_url)
# → https://abc123.ngrok-free.app
```

The frontend reads `VITE_BACKEND_URL` from a Vercel environment variable.
When you start a Colab session before a demo/interview, update this env var with
the new ngrok URL and trigger a Vercel redeploy, or use `.env.local` for local
frontend development. This is workable for demos, but it is not the right UX for
a stable public live feature.

**Google Drive storage plan:**
```
MyDrive/fetal-hc/
  best_model.pt           ← checkpoint (~50-200 MB, load once at startup)
  config.json             ← run config
  curated-samples/        ← 6 original ultrasound PNGs + metadata
    296_HC/ultrasound.png
    ...
```

This means hosted live mode does NOT need the full HC18 dataset — just the 6
curated images plus metadata in Drive. The backend reads them from
`/content/drive/MyDrive/fetal-hc/`.

**ngrok free tier limits:** 1 active tunnel, 20K requests/month. More than enough
for a demo. Colab Pro sessions last 24 hours. For an interview, spin up the session
30 minutes before.

---

### 2.2 Model Optimization (Free, Immediate Wins)

**Warm-up pass at startup:**
Run one dummy forward pass after loading the checkpoint so the first real request
does not pay initialization cost. Add this to FastAPI startup.

**TorchScript or compile path (benchmark first):**

```python
example_input = torch.zeros(1, 1, 256, 384).to(device)
traced = torch.jit.trace(model, example_input)
torch.jit.save(traced, 'best_model_traced.pt')
```

Potential wins here are real, but they should be benchmarked against the current
model and hardware rather than assumed.

**fp16 on Colab T4:**

```python
model = model.half()
image_tensor = image_tensor.half()
```

This is a strong candidate on a T4 because the model is convolution-heavy and
the input resolution is small enough to benefit from fast GPU inference.

**Dynamic quantization caveat:**
The current U-Net / Attention U-Net codebase is overwhelmingly `Conv2d` +
`BatchNorm2d`, not `Linear`-heavy. That means dynamic quantization is not an
automatic win and should be treated as experimental, not as a guaranteed
4x improvement.

Example only:

```python
import torch.quantization
model = load_model_from_checkpoint(checkpoint_path, config)
model_quantized = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear, torch.nn.Conv2d}, dtype=torch.qint8
)
# Benchmark before adopting. This model family may not benefit enough to justify
# the added complexity.
```

---

### 2.3 Real Metrics and Observability (No Cost)

**Per-step timing breakdown:**
The backend should time each pipeline stage and return it in the response.
This is genuinely interesting to show in the UI — users can see that preprocessing
takes 2 ms, the forward pass 35 ms, cleanup 8 ms, and ellipse fitting 1 ms.

Add to the `/live/infer` response:
```json
{
  "runtime_ms": 47,
  "step_times_ms": {
    "preprocess": 2,
    "forward_pass": 35,
    "sigmoid": 0,
    "threshold": 1,
    "cleanup": 8,
    "ellipse_fit": 1
  }
}
```

**Live metric comparison vs saved output:**
When live mode returns a result, compute the delta between live metrics and the
static manifest metrics for the same sample. Show this in the UI:

```
Live run  →  Dice: 0.991 | HC error: 0.03 mm
Saved run →  Dice: 0.991 | HC error: 0.03 mm   (matches ✓)
```

This is a strong demo moment: the live model produces the same result as the
pre-computed saved output, proving the pipeline is deterministic and real.

**MC Dropout uncertainty estimation:**
This is an interesting future feature, but it is not plug-and-play with the
current checkpoint. The current run config uses `dropout: 0.0`, so there may be
no active dropout to sample from at all. Also, blindly switching to
`model.train()` changes BatchNorm behavior, not just dropout.

If we want this feature, we should first decide one of:

- retrain a dropout-enabled checkpoint specifically for uncertainty estimation
- selectively enable dropout layers while keeping BatchNorm in eval mode
- choose a different uncertainty method

Experimental sketch only:

```python
def mc_dropout_inference(model, image, n_samples=10):
    model.train()
    probs = torch.stack([
        torch.sigmoid(model(image)) for _ in range(n_samples)
    ])
    mean_prob = probs.mean(0)
    uncertainty = probs.var(0)  # pixel-wise variance
    return mean_prob, uncertainty
```

The uncertainty map is a genuine additional output that most medical imaging demos
do not show. Pixels where the model is unsure (high variance) tend to be exactly
at the skull boundary — which is the most interesting region for the user to explore
with the threshold slider. But in this repo it should be treated as a research
extension, not an immediate milestone.

**Threshold sweep metric:**
Pre-compute or compute live: as threshold varies from 0.1 to 0.9 in steps of 0.05,
how does Dice score change? Plot this as a curve. The optimal threshold (where Dice
is maximized) is a real model evaluation insight, not just a tunable parameter.

Static-mode implementation note:
If this is added to the public static site, pre-compute the full curve during
artifact export and store it in the manifest or per-sample metadata. Do not make
the browser recompute Dice unless we are also comfortable publishing the target
mask artifacts needed for that computation.

---

### 2.4 Rate Limiting and Robustness (No Dependencies)

Simple in-memory rate limiting without Redis, using a sliding window:

```python
from collections import deque
from time import time
from fastapi import Request, HTTPException

class RateLimiter:
    def __init__(self, max_requests: int = 10, window_s: float = 60.0):
        self.max_requests = max_requests
        self.window_s = window_s
        self.requests: deque = deque()

    def check(self):
        now = time()
        while self.requests and now - self.requests[0] > self.window_s:
            self.requests.popleft()
        if len(self.requests) >= self.max_requests:
            raise HTTPException(429, "Rate limit exceeded. Try again in a minute.")
        self.requests.append(now)

limiter = RateLimiter(max_requests=30, window_s=60)

@app.post("/live/infer")
async def infer(request: InferRequest):
    limiter.check()
    ...
```

30 requests/minute is more than enough for a demo. This prevents a single visitor
from hammering the Colab GPU.

**Request logging (stdlib only):**
Log sample_id, threshold, step_times_ms, and result metrics to a file or stdout.
Useful post-demo to see what visitors explored.

---

## 3. Visualization Improvements from Industry Research

The following improvements are grounded in three landmark interactive ML
visualization projects: CNN Explainer (Georgia Tech / IEEE VIS 2020), GAN Lab
(Georgia Tech / IEEE VIS 2019), and Distill.pub. Each section identifies what
they do, why it works, and how to apply it specifically to this project.

---

### 3.1 From CNN Explainer — Multi-Level Abstraction and Animated Operations

**What CNN Explainer does:**
Presents the same CNN in three tightly linked levels of detail: (1) architecture
overview with heatmaps, (2) per-layer computation with animated sliding kernels,
(3) the dot-product formula for a single output pixel. Smooth transitions between
levels let users jump from "what does this layer do" to "what is the exact math."

**What to steal for this project:**

**Animated pipeline stage transitions:**
Currently the stepper jumps between stages. An animated transition showing the
transformation — e.g., the raw ultrasound dissolving into the probability heatmap,
or the raw mask morphing into the cleaned mask as connected-component cleanup runs
— is more educational than a static swap.

**Attention gate visualization:**
The Attention U-Net computes `coefficients = self.attention(skip_proj + gating_proj)`
inside each `AttentionGate.forward` — a `[B, 1, H, W]` tensor of sigmoid values
(0 = ignore, 1 = attend) before multiplying the skip features. This IS the
attention map. A forward hook captures it without any model changes:

```python
attention_maps = {}
def _hook(module, input, output):
    attention_maps['decoder4_gate'] = output.detach().cpu()
# Register on the Sigmoid → output is [0,1] attention coefficients
model.decoder4.gate.attention.register_forward_hook(_hook)
```

Run this during V2.S7.2 inference and return one attention PNG per decoder gate
alongside `prob.png`. Overlaid on the ultrasound, it shows exactly which skull
boundary region the model focused on — the strongest interpretability story this
project can tell. No model rebuild or retraining required.

**Level 3 detail on demand:**
Add a "How does thresholding work?" expandable panel that shows the math:
`mask[x,y] = prob[x,y] > t`. Then show the prob value of the pixel you last
hovered over in ThresholdViewer. This closes the loop between interaction and
understanding.

---

### 3.2 From GAN Lab — Live Hyperparameter Experimentation

**What GAN Lab does:**
Lets users change hyperparameters mid-training and watch the model adapt in
real time. The key insight: the interaction IS the explanation — users learn
by forming hypotheses and testing them, not by reading text.

**What to steal for this project:**

**Pre-run threshold control:**
Currently the threshold slider changes only the displayed mask after the fact.
A stronger design: the user sets the threshold before clicking "Run live", the
backend runs inference at that threshold, and they can see whether their chosen
threshold produced a better or worse result than the default 0.5.
Pair this with a real-time Dice score returned from the backend.

**Hypothesis testing mode:**
Show two panels side by side: "What happens if threshold = 0.3?" vs
"What happens if threshold = 0.7?" Both run live inference with different
thresholds and display the results simultaneously. The user can see the
over-segmentation vs under-segmentation tradeoff visually.

**Threshold sweep animation:**
A "Play" button that automatically increments the threshold from 0.1 to 0.9
in steps of 0.05 while the canvas repaints each frame. The mask grows and shrinks
in real time. No backend required — this is just re-processing the existing
`prob.png` pixel data in the ThresholdViewer canvas.
Overlay a Dice-vs-threshold curve (pre-computed from static manifest or returned
by backend) so users can see the score peak.

**Step-by-step execution with timing:**
Instead of returning the full result at once, show each pipeline step completing
with its actual timing. "Preprocessing... 2ms → Forward pass... 35ms → Cleanup... 8ms →
Ellipse fit... 1ms → Done." This is already supported by the `step_times_ms`
response field in Section 2.3. Just animate each step label as its time arrives.

---

### 3.3 From Distill.pub — Narrative + Inline Interaction

**What Distill.pub does:**
Interactive elements are embedded inline within the narrative text, not separated
into a "demo section." Reading about how attention works, you scroll past a live
interactive attention weight map. The article and the tool are the same thing.

**What to steal for this project:**

**Scrollytelling: Stage panels update with scroll position:**
The current design has a stepper you click through. An alternative (or addition)
for the pipeline section: as you scroll down through the explanation text for each
stage, the central image composite automatically updates to show that stage.
This is the IntersectionObserver scrollspy already in the app — extend it so the
stage panel advances as you read, not just as you click.

**Inline probability value callouts:**
While the user hovers over the ThresholdViewer canvas, show a callout near the
cursor: "p = 0.87 at this pixel. High confidence — this region is skull."
Below threshold 0.5, show: "p = 0.34 — model is uncertain here."
This turns a passive slider into a teaching moment about what probability means.

**"Why did this fail?" narrative for failure samples:**
For the two failure cases (793_HC, 032_HC), add an expandable failure analysis
section that explains in plain English: what went wrong geometrically, where
the mask deviated, and what the HC error looks like in context. This is text +
the existing MetricsPanel, but framed as a story rather than a data table.

---

### 3.4 Domain-Specific: Medical Imaging and Ultrasound Visualization

**Attention gate visualization (highest impact):**
Already described in Section 3.1. For an Attention U-Net specifically, this is
the canonical interpretability tool. A recruiter who sees the attention map
overlaid on an ultrasound — showing that the network learned to focus on the
skull boundary — immediately understands what the word "attention" means.

**Uncertainty map (MC Dropout) — BLOCKED:**
Confirmed blocked. `config.json` has `"dropout": 0.0` — the trained checkpoint
has no active dropout layers to sample from. Calling `model.train()` would only
change BatchNorm behavior. Do not implement until one of these decisions is made:
(a) retrain a new checkpoint with `dropout: 0.1`–`0.2`; or (b) use test-time
augmentation (flip/rotate N times, measure prediction variance) which requires
no retraining. See Section 6.1 for full detail.

**HC measurement ruler overlay:**
Draw the circumference measurement on the image as a visual ruler — a dashed
ellipse with a label showing the measurement in mm. Most implementations just
show the ellipse as a contour. Showing "191.4 mm" with a scalebar gives the
measurement physical intuition.

**Fetal growth context panel — BLOCKED:**
HC18 annotation CSVs contain only ellipse coordinates and pixel spacing. There
is no gestational age field in the dataset. This feature requires per-sample
gestational age, which this dataset does not provide. Do not implement unless
gestational age data is sourced externally. An alternative in-scope version:
show where the predicted HC sits relative to the range of the 6 curated samples
(min, median, max HC across the set), with a plain label like "lower third of
curated range" — this requires no external data.

**Side-by-side comparison mode:**
Add a split-panel mode: select two samples from the gallery and see both stepping
through the pipeline in sync. The most revealing comparison is a strong case next
to a failure case at the same pipeline stage — the user can see exactly where the
failure diverges from the correct prediction.

**Contour evolution animation:**
The cleaned mask is produced by taking the raw mask, removing small components,
and filling holes. Animate this process: show the raw mask → then each component
disappearing → then the final cleaned mask.

Implementation: pre-render each intermediate step as a static PNG during
artifact export and serve them alongside `pred.png`. The browser plays through
them as an animation. Do not attempt client-side morphological operations —
there are no native browser APIs for connected-component labeling. `raw_mask.png`
already exists in the sample directory from the V2.S2 export; intermediate
steps need to be added to the export script output.

---

## 4. Prioritized Improvement List

See **Section 6.6** for the authoritative, corrected priority table. This
section is intentionally kept as a forward reference to avoid having two
tables that can drift apart.

The canonical sequence is:

1. Path A (real images) — policy decision + one-line code fix + redeploy.
2. Threshold sweep Play button + inline probability callout — no backend, immediate.
3. Pre-compute threshold-Dice curve in export — adds real evaluation insight.
4. Live inference backend (V2.S7.2) including attention gate maps.
5. Optional static polish: HC ruler, failure narrative, contour evolution frames.
6. Blocked until explicit decision: MC Dropout (retrain), fetal growth chart
   (no gestational age in HC18).

---

## 6. Blind Spots and Cross-Document Gaps

This section documents issues found by cross-referencing the roadmap against the
actual codebase (`config.json`, `samples.ts`, `attention_unet.py`) and the
planning docs (`architecture.md`, `project-tasks.md`). Items are grouped by
severity.

---

### 6.1 Hard Blockers — These Features Cannot Be Built As Described

**MC Dropout uncertainty map is impossible without retraining.**

`outputs/runs/attention_unet_local_baseline/config.json` contains `"dropout": 0.0`.
The model was trained with zero dropout. There are no active dropout layers to
sample from during inference. Calling `model.train()` changes BatchNorm behavior
(it switches to per-batch statistics) but produces zero dropout stochasticity.

Section 2.3 calls this "experimental" — it should say: **blocked, requires an
explicit retraining decision first.** Before adding uncertainty estimation to the
roadmap, decide:
- Retrain a new checkpoint with `dropout: 0.1` or `0.2` (adds one config change
  and one training run).
- OR pick a non-dropout uncertainty method (test-time augmentation: run inference
  on flipped/rotated versions and measure prediction variance — this works even
  with `dropout: 0.0` and requires no retraining).

**Fetal growth context chart has no data source in this project.**

HC18 annotation CSVs contain only: `filename`, ellipse center/semi-axes/angle,
and pixel spacing. Gestational age is not included. A fetal growth reference
chart requires gestational age per sample, which this dataset does not provide.
Remove item 11 from the priority table, or re-scope it as:
- Show where the predicted HC falls relative to the 6-sample range in this
  curated set (does not require gestational age — just dataset-level context).
- Or label it explicitly as "requires external clinical reference table" and
  treat it as a separately approved feature.

---

### 6.2 Critical Implementation Gap — Path A Will Not Work As Described

**The manifest loading code in `frontend/src/data/samples.ts` uses a hostname
check, not a fetch-and-fallback.**

The roadmap says: "commit real images, update the manifest path, redeploy."
That is not sufficient.

Actual code:

```typescript
function preferredManifestPath(): string {
  const isLocalHost = hostname === "localhost" || hostname === "127.0.0.1";
  return isLocalHost ? DEFAULT_MANIFEST_PATH : PUBLIC_PREVIEW_MANIFEST_PATH;
}
```

On Vercel (non-localhost), the app unconditionally loads `/demo-samples/manifest.json`
(the SVG placeholder path) regardless of whether real images are present. Committing
real sample PNGs does not change this — the samples.ts hostname routing takes
precedence.

To make Path A work on Vercel, change `preferredManifestPath()` to always try
`/samples/manifest.json` first and fall back to `/demo-samples/manifest.json` on
a 404. There is already partial fallback logic: if the initial load fails for any
reason, it retries the other path. The fix is to make the default path
`DEFAULT_MANIFEST_PATH` regardless of hostname, and let the existing fallback
handle Vercel deployments where real images are absent:

```typescript
// Simplified: always try real samples first, fall back to preview on 404
function preferredManifestPath(): string {
  return DEFAULT_MANIFEST_PATH;  // /samples/manifest.json
}
// The existing fallback in loadManifest() already handles the 404 case.
```

This single-line change + committing real images is all that is needed for Path A.

---

### 6.3 Design Corrections — Features Are Feasible But Described Incorrectly

**Attention gate visualization does NOT require model changes.**

Section 3.1 says "we likely need a small model change." This is wrong. Inspecting
`AttentionGate.forward`:

```python
def forward(self, skip, gating):
    coefficients = self.attention(skip_proj + gating_proj)  # [B, 1, H, W], sigmoid 0–1
    return skip * coefficients
```

The `coefficients` tensor IS the attention map. It is computed inside `forward`
before the return. A `register_forward_hook` on the `self.attention` sequential
captures it at inference time without touching model weights or architecture:

```python
attention_maps = {}
def _hook(module, input, output):
    attention_maps['decoder4_gate'] = output.detach().cpu()

# Register on the attention sequential (last layer is Sigmoid → output is [0,1])
model.decoder4.gate.attention.register_forward_hook(_hook)
```

The hook captures a `[1, 1, H, W]` map for each decoder-level attention gate.
These can be exported as additional PNGs in V2.S7.1 or as base64 data in the
live `/infer` response, with no model rebuild or retraining required.

**Threshold sweep Dice curve requires the target mask to be in the browser.**

Section 3.2 says: "overlay a Dice-vs-threshold curve (pre-computed from static
manifest or returned by backend)." The pre-compute path is the right one.

Computing Dice client-side in the browser requires the target mask at runtime.
The target mask (`target.png`) is already in the curated bundle but computing
Dice from canvas pixel data in JavaScript is non-trivial and slow.

Correct implementation: during artifact export (`scripts/export_demo_artifacts.py`),
compute Dice at thresholds 0.1, 0.15, ..., 0.90 using `prob.png` vs `target.png`
and store the curve as a per-sample field in `metadata.json` and the manifest.
The browser reads this static data and renders it as an SVG path overlay. No
client-side Dice computation needed.

This requires a manifest schema update — see Section 6.5.

**Contour evolution animation requires JavaScript morphological operations.**

Section 3.4 says: "recompute client-side from existing `pred.png` mask data."
The contour evolution (raw mask → remove small components → fill holes → final
mask) requires connected-component labeling and binary fill, which have no
native browser APIs.

Options in order of feasibility:
1. Pre-render each step as separate PNGs during artifact export and serve them
   as static assets — simplest, no browser compute needed.
2. Use `opencv.js` (WebAssembly port, ~8 MB) — adds a large dependency.
3. Implement a minimal flood-fill in JavaScript — feasible but nontrivial.

Option 1 is recommended. Add `raw_mask.png` (already exists in the sample
directory from V2.S2 export) and intermediate-step PNGs to the curated bundle
if this feature is prioritized.

---

### 6.4 Colab Backend URL Rotation — Mitigation Strategy

The roadmap notes that ngrok URLs rotate with every session, requiring a Vercel
env var update plus redeploy. For a demo-only workflow this is acceptable; for
a persistent public feature it is not.

Three concrete mitigations, in order of effort:

1. **Notebook-hosted redirect** (zero extra infrastructure): Store the current
   backend URL in a GitHub Gist using the GitHub API from the Colab notebook.
   The frontend fetches the Gist content to resolve the backend URL at runtime.
   No Vercel redeploy needed — just run one cell in the notebook.

2. **ngrok paid static domain** (~$8/month): ngrok paid plans provide a persistent
   custom domain. The ngrok URL never rotates — the Vercel env var is set once.

3. **HF Spaces as the stable public backend, Colab as the fast dev backend**:
   Use Colab only for local demo sessions and interviews. For the public site,
   deploy to HF Spaces CPU Basic (always-on, cold start expected). This matches
   Combination 1 + 3 from the live-inference-plan.md.

---

### 6.5 Architecture.md and project-tasks.md Gaps

**architecture.md — file layout is stale.**
The file layout (Section 4) was written before the demo-samples/ fallback
path was implemented. Current actual layout:

```text
frontend/public/
  samples/             ← real curated public bundle
  demo-samples/
    manifest.json      ← fallback preview manifest
    public-preview/    ← SVG fallback assets
  experiments/
    summary.json
```

Section 9 also describes the fallback as "tries /samples/ first, falls back to
/demo-samples/" — but the actual `samples.ts` code does the reverse: non-localhost
defaults to `/demo-samples/` unconditionally. See Section 6.2 above.

**architecture.md — manifest schema is missing planned fields.**
If threshold-sweep curves (Section 3.2) are pre-computed during export, the
manifest schema needs a new optional field:

```typescript
thresholdCurve?: {
  thresholds: number[];           // [0.10, 0.15, ..., 0.90]
  dice: number[];                 // Dice at each threshold
  optimalThreshold: number;       // threshold that maximizes Dice
  optimalDice: number;
};
```

This field lives in the per-sample `metadata.json` and is merged into
`manifest.json` during export. It is optional (`?`) so old manifests remain valid.

**architecture.md — `frontend/src/utils/assets.ts` not in file layout.**
This helper (`getSampleAssets`) is agreed upon in `live-inference-plan.md` and
`project-tasks.md` but is absent from architecture.md Section 4.

**project-tasks.md — V2.S0 through V2.S6 are all done.**
The static MVP is complete and deployed. V2.S7 is in_progress (V2.S7.1 done,
V2.S7.2–S7.4 todo). The session-dependency concern about V2.S5 no longer
applies — all static-demo components (ContourEllipse, MetricsPanel,
ExperimentDashboard) are live on the deployed app.

**project-tasks.md — V2.S7 missing attention gate export.**
The attention gate visualization (priority item 4) requires V2.S7.1 to export
the attention coefficient maps alongside `prob.png`. The V2.S7.1 subtasks in
project-tasks.md don't mention this. Add: "register hooks on decoder attention
gates and return attention maps as additional inference outputs."

Important implementation note:
The current docs have drifted slightly ahead of the code. `project-tasks.md`
now says this attention-hook work is part of completed `V2.S7.1`, but the
current `src/inference/live.py` still returns only `ultrasound`, `target`,
`prob`, and `pred` assets plus scalar metrics. There is no shipped attention-map
capture path yet. Do not treat attention visualization as "already covered by
S7.1"; either:

- move it into `V2.S7.2` as part of the FastAPI payload work, or
- add a small follow-up sub-session (`V2.S7.1b`) and keep `V2.S7.1` narrowly
  defined as the core live inference path that already exists.

This keeps the task log honest and avoids future confusion during implementation.

**architecture.md — live response contract is still underspecified.**
The architecture file defines the static `Sample` contract well, but it does not
yet define the full live API contract. The roadmap now assumes live mode may
return:

- `sample` (Sample-compatible object),
- `assets` (URL or data-URL overrides),
- `runtime_ms`,
- optional `step_times_ms`,
- potentially attention maps in a future revision.

That deserves an explicit architecture section with concrete TypeScript/Pydantic
shapes such as:

```typescript
type SampleAssets = {
  ultrasound?: string;
  target?: string;
  prob?: string;
  pred?: string;
  attention?: Record<string, string>;
};

interface LiveInferResponse {
  mode: "live";
  runtime_ms: number;
  step_times_ms?: Record<string, number>;
  sample: Sample;
  assets: SampleAssets;
}
```

Without this, `architecture.md`, `project-tasks.md`, and the eventual FastAPI
schemas are likely to drift.

**Hosted curated-bundle spec is missing required target/spacing data.**
Section 2.1 currently says a hosted Colab/Drive bundle only needs:

- `best_model.pt`
- `config.json`
- six `ultrasound.png` files
- metadata

That is incomplete if we want the live backend to compute:

- Dice/IoU/HD95,
- target-vs-live metric deltas,
- target-mask visualizations,
- or regenerate target masks from annotations.

For a hosted curated bundle, we need one of these explicit contracts:

1. **Target-mask bundle**  
   Store `target.png` plus per-sample spacing/labels.

2. **Annotation bundle**  
   Store the original annotation parameters needed to regenerate the target mask
   plus spacing and any derived target HC metadata.

The roadmap should treat this as a real data-contract decision before hosted
live mode, not as a detail to infer later.

**Path A needs a canonical artifact source-of-truth rule.**
If public real artifacts are approved, there will be two near-identical trees:

- `outputs/demo_samples/` — generated source bundle
- `frontend/public/samples/` — runtime/public bundle

Right now the docs explain the copy step, but not the ownership rule. Add this
explicitly to avoid silent drift:

- `outputs/demo_samples/` remains the generated source of truth
- `frontend/public/samples/` is a copied publish/runtime mirror
- never hand-edit `frontend/public/samples/`
- when curated artifacts change, regenerate under `outputs/demo_samples/` and
  then sync-copy into `frontend/public/samples/`

This matters more once `frontend/public/samples/` becomes committed for Path A.

**Path A should keep the placeholder fallback, not delete it.**
Section 1 currently says the split between `samples/` and `demo-samples/` "can
be collapsed." That is optional, but not obviously desirable. Keeping
`demo-samples/` committed as a fallback still helps:

- fresh clones before local artifact generation,
- forks where users do not want to publish HC18-derived files,
- future policy rollback,
- visual QA when real artifacts are intentionally absent.

Recommended adjustment: for Path A, make `/samples/manifest.json` the preferred
path everywhere, but keep `/demo-samples/manifest.json` as a committed fallback
rather than deleting the preview bundle.

**architecture.md boundary text should distinguish local/static from hosted/live.**
Section 10 says "The demo should not require internet access." That is true for
the local saved-output MVP, but it is not true for:

- the public Vercel portfolio site,
- any Colab/ngrok or HF Spaces live backend,
- runtime Gist-based backend URL discovery if we adopt that mitigation.

The architecture should clarify that:

- local saved-output mode should run offline after artifacts are present
- public hosting and hosted live inference obviously require network access

That keeps the boundary meaningful without accidentally contradicting the live
deployment plan.

**project-tasks.md — side-by-side comparison mode needs a new optional session.**
Comparison mode requires changing `activeId: string` to `activeIds: [string, string]`
in App.tsx and refactoring all consumers. This is a nontrivial state model change.
It should not be added to V2.S4 or V2.S5 scope retroactively — treat it as a
post-V2.S6 optional session if prioritized.

---

### 6.6 Revised Priority Table

Incorporating the corrections from this section:

| Priority | Improvement | Path | Effort | Status |
|---|---|---|---|---|
| 1 | Fix `preferredManifestPath()` + commit real samples (Path A) | Static | 1–2 h | Implemented locally; commit/push + redeploy pending |
| 2 | Threshold sweep animation (Play button, no Dice curve) | Static | 2 h | No backend, no blockers |
| 3 | Inline probability callout on canvas hover | Static | 2 h | No blockers |
| 4 | Pre-compute threshold-Dice curve in export script | Static | 2–3 h | Requires V2.S2 revision |
| 5 | Define live API contract in architecture + schemas | Live | 1–2 h | Prevents FastAPI/TS drift before S7.2 |
| 6 | Attention gate visualization via forward hook | Live | 3–4 h | No model changes needed, but not yet implemented |
| 7 | Step-by-step timing animation | Live | 2 h | Needs `step_times_ms` in live response |
| 8 | Colab Pro T4 GPU backend | Live | 2–3 h setup | Needs curated hosted-bundle contract first |
| 9 | Contour evolution — pre-render intermediate PNGs | Static | 2–3 h | Export script change |
| 10 | HC ruler overlay on image | Static | 2 h | No blockers (V2.S5 done) |
| 11 | Side-by-side comparison mode | Static | 5–7 h | Requires App state refactor |
| 12 | Failure analysis narrative | Static | 1–2 h | No blockers (V2.S5 done) |
| 13 | MC Dropout uncertainty map | Live | — | **BLOCKED** — retrain needed |
| 14 | Fetal growth context chart | Static | — | **BLOCKED** — no gestational age in HC18 |

---

## 5. Sources and Research Basis

The visualization improvements in Section 3 draw from:

- Wang et al., "CNN Explainer: Learning Convolutional Neural Networks with Interactive
  Visualization," IEEE VIS 2020. arXiv:2004.15004
- Kahng et al., "GAN Lab: Understanding Complex Deep Generative Models using
  Interactive Visual Experimentation," IEEE VIS 2019.
- Distill.pub editorial philosophy: https://distill.pub/about/
- Hugging Face blog on interactive ML tools: https://huggingface.co/blog/Suzana/interactive-tools
- "A Survey on Explainable AI (XAI) Techniques for Visualizing Deep Learning Models
  in Medical Imaging," MDPI Journal of Imaging, 2024.
- ngrok + Colab FastAPI setup: https://ngrok.com/docs/using-ngrok-with/googleColab
- HC18 challenge page: https://hc18.grand-challenge.org/
- HC18 Zenodo dataset: https://zenodo.org/records/1322001
- HC18 Zenodo dataset v2 record: https://zenodo.org/records/1327317
- Zenodo license/reuse guidance: https://support.zenodo.org/help/en-gb/2-content/21-can-i-get-permission-to-use-a-specific-record
- HC18 paper / data-availability statement: https://doi.org/10.1371/journal.pone.0200412
