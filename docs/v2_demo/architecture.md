# V2 Demo Architecture

## 1. Goal

V2 adds a portfolio-ready web demo on top of the v1 PyTorch pipeline. The demo
is an ML pipeline explorer, not a replacement for the v1 training and
evaluation scripts.

The first milestone uses saved v1 artifacts so the app is fast, reliable, and
easy to review. A later milestone can add live checkpoint inference through the
same app-facing interface.

## 2. High-level flow

```text
Curated sample manifest
        |
        v
Saved v1 artifacts
  image, target mask, prediction records, masks, overlays, metrics
        |
        v
Streamlit UI
        |
        +--> Data and target-mask view
        +--> CNN prediction/probability view
        +--> Threshold and cleanup view
        +--> Ellipse and HC measurement view
        +--> Experiment dashboard
```

Future live inference adds:

```text
Uploaded or selected image
        |
        v
Checkpoint inference adapter
        |
        v
Same demo-stage objects used by saved-output mode
```

## 3. App modes

### Saved-output mode

Saved-output mode is the v2 MVP.

Responsibilities:

- load a small manifest of curated samples,
- read existing prediction CSVs and saved masks/overlays,
- display each pipeline stage without loading a model checkpoint,
- compute lightweight interactive geometry variants when needed,
- show v1 result tables and figures.

This mode should run without raw HC18 data if the curated artifacts are present.

### Live-inference mode

Live-inference mode is a later extension.

Responsibilities:

- load a PyTorch checkpoint,
- preprocess selected or uploaded images,
- run model inference,
- produce the same stage objects as saved-output mode,
- use the existing deterministic geometry utilities.

This mode may require a checkpoint and the original HC18 image or a user-provided
image. It must keep the safety disclaimer visible.

## 4. Core components

### Sample selector

The selector reads a curated manifest. Each sample should identify:

- sample id,
- split,
- source image path or demo image path,
- target mask path when available,
- raw mask path,
- cleaned mask path,
- overlay path,
- prediction row or metrics row.

The first implementation should use a small fixed set of examples, including at
least one strong prediction and one failure or high-error case.

### Target-mask visualization

This view explains how HC18 annotation images become model targets. It should
show the original ultrasound, annotation-derived filled mask, and optional
boundary-style mask when available.

### CNN prediction visualization

Saved-output mode can show saved raw masks and overlays. If probability maps are
not yet saved, the app should label this as the thresholded prediction output
rather than pretending to show probabilities.

Live-inference mode can add probability heatmaps directly from model logits.

### Geometry visualization

This view uses existing geometry utilities where possible:

- thresholded mask,
- largest connected component cleanup,
- contour measurement,
- ellipse fit,
- HC in millimeters.

It should make the contour-vs-ellipse tradeoff visible because this was one of
the strongest v1 findings.

### Experiment dashboard

The dashboard reads v1 report tables and figures, especially:

- main test results,
- Attention U-Net ablations,
- post-processing ablation,
- HC MAE figures.

The dashboard should emphasize that v1 used a local reduced-resource setup.

## 5. Boundaries

- The demo must not mutate raw data or split files.
- The demo must not train models.
- The demo must not silently regenerate v1 experiments.
- The demo should not require internet access.
- The demo is educational and not for clinical use.
