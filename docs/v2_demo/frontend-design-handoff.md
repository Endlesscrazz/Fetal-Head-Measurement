# V2 Frontend Design Handoff

Source: `/Users/shreyas/Downloads/design_handoff_fetal_hc_explorer/`
Reviewed: 2026-05-01

This document is the primary handoff reference for Codex implementing the v2 React
frontend. Read this alongside `architecture.md` and `project-tasks.md` before
writing any code.

---

## 1. What the design delivers

The design handoff is a high-fidelity React prototype of a single-page interactive
ML explainer. It is the authoritative source for colors, typography, spacing, layout,
component structure, and all interactions. The implementer's job is to port it to a
real Vite + React + TypeScript build, replace placeholder sample data with real v1
artifacts, and fix the places where the design diverged from our actual experiment
results.

The design is excellent and should be reproduced closely, subject to the
corrections listed in Section 4 and the repository frontend rules in
`AGENTS.md`. In particular, keep the visual intent but normalize any negative
letter-spacing values to `0`.

---

## 2. Tech stack decision

**Frontend:** Vite + React + TypeScript + CSS custom properties (from `styles.css`).
Do NOT use Tailwind — the design ships a complete token system in `styles.css` that
is already clean and should be ported directly, with the project-specific
corrections in this document. Adding Tailwind would conflict with it.

**Backend:** None for the MVP. The frontend is a fully static site — it reads from
pre-built JSON and PNG files under `public/samples/`. There is no API call, no
Python server, and no live inference in the default mode.

**Deployment target:** Vite build → `frontend/dist/`. Deploy to Vercel or GitHub Pages
for free. Single `vercel.json` or `gh-pages` action is sufficient.

**Live inference (V2.S7 / post-MVP):** A separate FastAPI backend can be added later.
The frontend architecture should be adapter-aware — but the static mode must work
without any backend running.

---

## 3. Files from the handoff

### Port to production (these are the source of truth)

| Handoff file | Production equivalent |
|---|---|
| `styles.css` | `frontend/src/styles.css` — port tokens/layout directly, with documented corrections |
| `components/nav.jsx` | `frontend/src/components/nav/StickyNav.tsx` |
| `components/gallery.jsx` | `frontend/src/components/gallery/SampleGallery.tsx` |
| `components/pipeline.jsx` | `frontend/src/components/pipeline/PipelineStepper.tsx` + `StageDetail.tsx` |
| `components/threshold.jsx` | `frontend/src/components/threshold/ThresholdViewer.tsx` |
| `components/insight.jsx` | `frontend/src/components/geometry/ContourEllipse.tsx` + `MetricsPanel.tsx` |
| `components/experiments.jsx` | `frontend/src/components/experiments/ExperimentDashboard.tsx` (with data corrections — see Section 4) |
| `app.jsx` | `frontend/src/App.tsx` + `frontend/src/components/hero/Hero.tsx` |
| `data.js` (`STAGES`, `METRIC_COPY`) | `frontend/src/data/stages.ts` + `frontend/src/data/metric-copy.ts` (port verbatim) |
| `data.js` (`SAMPLES`) | `frontend/src/data/samples.ts` — generated from `public/samples/manifest.json`, NOT hand-edited |

### Drop — design-time only

| Handoff file | Reason |
|---|---|
| `tweaks-panel.jsx` | Design-time feature, not needed in production |
| `design-canvas.jsx` | Design canvas component, not needed |
| `artboards/*.jsx` | Artboard layout views, not needed |
| `Design Canvas.html` | Design canvas entry point |
| `samples/*/` (the placeholder PNGs) | Replace with real v1 artifacts from `outputs/demo_samples/` |

---

## 4. Corrections required — where design diverges from our project

### 4.1 Sample IDs and metrics (CRITICAL)

The design uses these six sample IDs: `296_HC`, `142_HC`, `418_HC`, `073_HC`,
`511_HC`, `624_HC`.

After checking against `attention_unet_local_baseline` test evaluation:

| Design ID | In test split? | Notes |
|---|---|---|
| `296_HC` | ✅ yes | dice 0.9907, hcErr 0.03 mm — matches design label "Near-perfect" |
| `142_HC` | ✅ yes | dice 0.9677, hcErr 4.51 mm — design metrics are WRONG (placeholder) |
| `073_HC` | ✅ yes | dice 0.9696, hcErr 1.62 mm — design metrics are close but placeholder |
| `511_HC` | ✅ yes | dice 0.9762, hcErr 4.30 mm — design labels this "failure"; real performance is strong |
| `418_HC` | ❌ no | Not in test split — must replace |
| `624_HC` | ❌ no | Not in test split — must replace |

**Decision after Codex review:** do not force the production app to keep the
design prototype IDs. The handoff images are procedural placeholders, so the
visual layout can be ported while using the stronger already-curated real sample
set in `docs/v2_demo/curated-samples.json`:

- `296_HC` — strong headline success
- `217_HC` — second strong success
- `663_HC` — typical/median-like error
- `025_HC` — cleanup and ellipse teaching case
- `793_HC` — high-error case
- `032_HC` — failure case

This set covers the design's desired story more honestly than the placeholder
IDs, because `511_HC` is not actually a failure in the real run and `418_HC` /
`624_HC` are not available in the internal test split.

**All `data.js` SAMPLES metrics are placeholder.** Replace every number with real
values from v1 prediction/evaluation CSVs through the generated manifest. The
`id`, `label`, `cat`, `split`, and `summary` fields should come from the curated
sample JSON and real metrics, not from the prototype `data.js`.

### 4.2 Experiment dashboard — replace U-Net++ with real ablations (CRITICAL)

The design's `ExperimentDashboard` shows three architectures:
- U-Net (baseline)
- Attention U-Net (best)
- U-Net++ (third)

**We never trained U-Net++.** Replace with our actual runs:

| Design slot | Real run ID | Real label |
|---|---|---|
| U-Net | `unet_local_baseline` | U-Net |
| Attention U-Net | `attention_unet_local_baseline` | Attention U-Net (best) |
| U-Net++ | `attention_unet_aug` | Attn U-Net + Aug |

The training sparklines in the design are synthetically generated. Replace with real
epoch-by-epoch Dice values from `outputs/runs/<run_id>/metrics.csv` (columns:
`epoch, train_loss, val_loss, val_dice`). Plot `val_dice` as the sparkline.

The augmentation ablation table in the design uses synthetic values. Replace with
real data from `outputs/tables/local_ablation_summary.csv` or
`outputs/tables/attention_unet_local_baseline_test_postprocess_ablation.csv`.

Add a visible disclaimer: "Local training: 10 epochs, 256×384, base channels 16."

### 4.3 `prob.png` is missing from v1 outputs (CRITICAL)

The `ThresholdViewer` component reads pixel data directly from `prob.png` — a
grayscale PNG where pixel brightness = model confidence (0 = background, 255 = skull).
**This file does not exist in any v1 prediction output.** v1 only saved binary masks.

V2.S2 (export script) must generate `prob.png` for each selected sample by:
1. Loading the `attention_unet_local_baseline` checkpoint
2. Running a forward pass on the sample image with sigmoid (no thresholding)
3. Saving the sigmoid output as a uint8 grayscale PNG (`prob * 255`)
4. Resizing to the display resolution used in the frontend (confirm with V2.S1)

This means V2.S2 **requires the checkpoint to be present locally**. The checkpoint
exists at `outputs/runs/attention_unet_local_baseline/best_model.pt`.

### 4.4 `contourHC` must be computed (CRITICAL)

The design's `ContourEllipse` component uses `sample.contourHC` — the HC measurement
from the raw mask contour (before ellipse fitting). This does not exist in any v1
output file.

V2.S2 must compute it for each sample:
- Load the cleaned mask
- Extract the largest contour
- Compute its perimeter in pixels, then convert to mm using per-sample pixel spacing
- Store as `contourHC` in `manifest.json`

Use existing functions in `src/utils/geometry.py`.

### 4.5 `confidence` field must be computed

The design has `sample.confidence` (e.g. `0.97`) — the mean probability value across
all pixels where the predicted mask is 1. This is "how confident the model is inside
its own prediction."

V2.S2 must compute: `mean(prob_map[cleaned_mask == 1])` and store as `confidence`
in `manifest.json`. This requires `prob.png` (see 4.3).

### 4.6 `predEllipse` vs `ellipse` — only one exists in v1

The design has both:
- `ellipse` — ground truth ellipse from the radiologist annotation
- `predEllipse` — model prediction ellipse

v1 only saves `predEllipse` parameters (in `predictions.csv` columns:
`ellipse_center_x, ellipse_center_y, ellipse_semi_axis_a, ellipse_semi_axis_b,
ellipse_angle_deg`).

For the MVP, use `predEllipse` for both slots, or compute the ground-truth ellipse
from the annotation CSV using `src/data/masks.py`. The `ContourEllipse` component
only uses `predEllipse`, so this primarily affects the `StageCallout` for the target
stage. If ground-truth ellipse is not available, omit it gracefully.

### 4.7 Image display resolution

The design hardcodes `480 × 360` and `0.184 mm/px` in `StageImage`. Our v1 images
are resized to `256 × 384` and pixel spacing varies per sample (stored in
`predictions.csv` as `spacing_x_mm`, `spacing_y_mm`).

- The `StageImage` caption should read actual resolution from `manifest.json`
- The `StageCallout` for stage 1 (input) should show actual spacing from metadata

### 4.8 `hd95` field name inconsistency

The design uses `hd95` in sample metrics. v1 CSVs use `hd95_mm`. Use `hd95_mm` in
`manifest.json` and alias to `hd95` in the TypeScript type if needed.

### 4.9 Category key: `'failure'` not `'edge'`

The design uses `cat: 'edge'` for edge cases. Our review docs and `architecture.md`
use `'failure'`. Standardize on `'failure'` everywhere (manifest, TypeScript type,
filter tabs). Update the gallery filter tab label from "Edge case" to "Failure" or
"Edge / Failure" — both are honest.

---

## 5. Frontend file structure

```
frontend/
  src/
    components/
      nav/
        StickyNav.tsx       ← from components/nav.jsx
        TourBar.tsx         ← from components/nav.jsx (TourBar section)
      hero/
        Hero.tsx            ← from app.jsx Hero function
      gallery/
        SampleGallery.tsx   ← from components/gallery.jsx
      pipeline/
        PipelineStepper.tsx ← from components/pipeline.jsx PipelineStepper
        StageDetail.tsx     ← from components/pipeline.jsx StageDetail + StageImage
      threshold/
        ThresholdViewer.tsx ← from components/threshold.jsx (keep canvas logic exact)
      geometry/
        ContourEllipse.tsx  ← from components/insight.jsx ContourEllipse
        MetricsPanel.tsx    ← from components/insight.jsx MetricsPanel
      experiments/
        ExperimentDashboard.tsx ← from components/experiments.jsx (with corrections)
      shared/
        SafetyChip.tsx      ← from app.jsx SafetyChip (non-negotiable, always visible)
        CategoryBadge.tsx   ← from gallery.jsx CategoryBadge
    data/
      stages.ts             ← STAGES array, port verbatim from data.js
      metric-copy.ts        ← METRIC_COPY object, port verbatim from data.js
      samples.ts            ← loads and exports SAMPLES from manifest.json at build time
                               OR fetches /samples/manifest.json at runtime
    types/
      sample.ts             ← Sample + Manifest TypeScript interfaces (Section 6)
    styles.css              ← port from styles.css verbatim (all CSS custom properties)
    App.tsx                 ← from app.jsx App function (minus tweaks panel)
    main.tsx
  public/
    samples/
      manifest.json         ← generated by V2.S2 export script
      <sample_id>/
        ultrasound.png
        target.png          ← annotation-derived mask
        pred.png            ← cleaned binary prediction
        prob.png            ← RAW probability map (uint8 grayscale) ← required for ThresholdViewer
  index.html
  vite.config.ts
  package.json
  tsconfig.json
```

---

## 6. TypeScript data types

The production equivalent of `SAMPLES` in `data.js`. Use this as the authoritative
interface — it maps directly to the manifest schema in `architecture.md`.

```typescript
export interface SampleMetrics {
  dice: number;       // 0..1
  iou: number;        // 0..1
  hd95_mm: number;    // mm (alias hd95 in component props if needed)
  hcErr: number;      // mm, abs_hc_error_mm from v1
  predHC: number;     // mm, pred_hc_mm from v1
  targetHC: number;   // mm, target_hc_mm from v1
}

export interface Ellipse {
  cx: number;         // center x in image pixels (at export resolution)
  cy: number;         // center y
  rx: number;         // semi-axis a
  ry: number;         // semi-axis b
  rot: number;        // angle in radians
}

export interface Sample {
  id: string;                          // e.g. "296_HC"
  label: string;                       // human title e.g. "Near-perfect HC"
  cat: 'strong' | 'typical' | 'failure';
  split: string;                       // "test"
  summary: string;                     // 1-line description for gallery card
  metrics: SampleMetrics;
  predEllipse: Ellipse;
  contourHC: number;                   // mm, computed by export script
  confidence: number;                  // 0..1, mean prob inside predicted mask
  spacingXMm: number;                  // mm per pixel (x)
  spacingYMm: number;                  // mm per pixel (y)
  resolution: { w: number; h: number }; // image dimensions at export resolution
  notes?: string;
}

export interface Manifest {
  schema_version: number;
  created_from_run_id: string;
  safety_text: string;
  samples: Sample[];
}
```

The `paths` fields from the design's data.js (`paths.ultrasound`, `paths.prob`, etc.)
should NOT be in the manifest — derive them as `public/samples/${id}/<file>.png`
at runtime in the frontend using the sample `id`. This keeps the manifest clean.

---

## 7. Interaction preservation checklist

These interactions must be preserved exactly. Each was validated in the design
prototype as core to the educational value.

| Interaction | Implementation notes |
|---|---|
| Click case card → pipeline auto-advances 0→2 | `useEffect` on `activeId`, `setInterval` 3 steps × 220 ms — keep exact timing |
| Drag threshold slider → canvas re-thresholds live | Canvas `getImageData` on `prob.png`, soft-edge blend — keep exact pixel logic from `ThresholdViewer` |
| Probability heatmap toggle | `showProb` state, same canvas draw path |
| Contour/Ellipse/Both/Morph toggle | SVG opacity transitions, morph slider — keep exact |
| Scrollspy nav | `IntersectionObserver`, `rootMargin: '-20% 0px -60% 0px'` — keep exact |
| Smooth scroll on nav click | `scrollIntoView({ behavior: 'smooth' })` |
| Guided tour mode | `tourActive` + `TourBar` — keep; tour copy in `TOUR_COPY` array should reference real section content |
| Threshold histogram | Show synthetic bins for MVP — replace with real prob.png histogram later |
| Pipeline stage animated swap | `fade-in` CSS class on stage detail card key change |

---

## 8. Additions not in the design

These are features required by the project spec that are absent from the design and
must be added during implementation.

### 8.1 Real training loss curves in ExperimentDashboard

The design shows Dice sparklines from synthetic data. Replace with real training
curves from `outputs/runs/*/metrics.csv` (`epoch, train_loss, val_loss, val_dice`).
Show `val_dice` as the sparkline (consistent with design aesthetic). Optionally show
`train_loss` and `val_loss` in a separate small chart when a run card is active.

Load these at build time (Vite import of JSON/CSV) or serve as static files from
`public/experiments/`.

### 8.2 Post-processing ablation table

The design's augmentation ablation table should be replaced or supplemented with
the post-processing ablation (raw mask vs cleanup + ellipse). This was the strongest
v1 finding. Use data from:
`outputs/tables/local_postprocess_ablation_summary.csv`

Show it as a second tab or a second table below the augmentation ablation.

---

## 9. Implementation gotchas from the design README

These are the implementer warnings from the design handoff README — all still apply:

1. **Canvas CORS** — `ThresholdViewer` uses `getImageData` on `prob.png`. The image
   must be same-origin. In Vite dev mode, assets in `public/` are served same-origin.
   In production, verify the hosting setup does not set restrictive CORS headers.
2. **`scroll-margin-top: 80px`** on every section — prevents anchor jumps from sliding
   under the sticky nav. Do not remove.
3. **`white-space: nowrap`** on hero stat labels and values — prevents wrapping at
   narrow widths. Do not remove.
4. **SafetyChip** — fixed bottom-right, `z-index: 50`, always visible. This is
   non-negotiable. Do not make it conditional or responsive-hidden.
5. **Pipeline auto-advance `useEffect`** — tied to `activeId` change. Clears its own
   interval. Make sure the cleanup return is present to avoid state updates on
   unmounted components.
6. **Background radial gradient** — `app-bg` class in styles.css. Do not skip — it
   gives the page its depth.

---

## 10. V2.S2 export script additions required by this design

The following additions to `scripts/export_demo_artifacts.py` are mandatory for the
frontend to function:

| New output | How to generate | Used by |
|---|---|---|
| `<id>/prob.png` | Forward pass → sigmoid → uint8 grayscale PNG. Requires `best_model.pt` | ThresholdViewer canvas |
| `manifest.json` `.confidence` | `mean(prob[cleaned_mask == 1])` per sample | StageCallout, hero card |
| `manifest.json` `.contourHC` | Contour perimeter × spacing, from `src/utils/geometry.py` | ContourEllipse panel |
| `manifest.json` `.predEllipse` | Parse from `predictions.csv` ellipse columns, convert angle to radians | StageImage SVG, ContourEllipse SVG |
| `manifest.json` `.spacingXMm`, `.spacingYMm` | From `predictions.csv` `spacing_x_mm`, `spacing_y_mm` | StageCallout pixel-size readout |
| `manifest.json` `.resolution` | Width × height of exported images | StageImage caption |
| Real sample metrics | From `evaluation/test/per_sample_metrics.csv` and `predictions/test/predictions.csv` | All metric displays |

The manifest schema in `architecture.md` must be updated to include the new fields
`confidence`, `contourHC`, `predEllipse`, `spacingXMm`, `spacingYMm`, `resolution`.

---

## 11. One-command start

After V2.S2 (export) has been run:

```bash
# First time
cd frontend
npm install
cp -r ../outputs/demo_samples/* public/samples/

# Start dev server
npm run dev
# → http://localhost:5173

# Build for deployment
npm run build
# → frontend/dist/ (deploy to Vercel or GitHub Pages)
```

The `start_demo.sh` script added in V2.S6 should wrap these commands.

---

## 12. Files to not commit

- `frontend/node_modules/`
- `frontend/dist/` (build output — let Vercel build it)
- `frontend/public/samples/` — medical image artifacts stay local by default
  (see `architecture.md` section 9 for distribution policy)

Add all of these to `.gitignore` in V2.S3.
