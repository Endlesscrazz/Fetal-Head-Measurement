# Architecture — Automated Measurement of Fetal Head Circumference

## 1. Architecture goal
Design a simple, reproducible system that turns an HC18 ultrasound image into:
- a predicted fetal head segmentation,
- a fitted ellipse,
- a final head circumference measurement in millimeters,
- evaluation artifacts for the report.

The architecture should optimize for:
- reproducibility,
- low implementation risk,
- easy experimentation,
- clean separation between data, modeling, and evaluation.

---

## 2. High-level system view

```text
HC18 image + annotation metadata
        │
        ▼
Data ingestion + annotation parser
        │
        ▼
Ellipse-to-mask target generation
        │
        ▼
Preprocessing + augmentation
        │
        ▼
Segmentation model (U-Net / Attention U-Net / ResUNet)
        │
        ▼
Probability map
        │
        ▼
Thresholding + connected component cleanup
        │
        ▼
Contour extraction + ellipse fitting
        │
        ▼
Head circumference computation (pixels -> mm)
        │
        ├──► quantitative metrics
        └──► qualitative overlays / report figures
```

---

## 3. Major modules

## 3.1 Data module
Responsible for reading HC18 images, labels, and metadata.

### Responsibilities
- load raw ultrasound images,
- parse annotation files,
- extract pixel spacing,
- build train/val/test splits,
- cache processed labels if needed.

### Inputs
- image files,
- annotation CSV / metadata files,
- split configuration.

### Outputs
- tensors for image,
- target mask,
- ellipse parameters,
- pixel spacing,
- sample id.

### Design note
The dataset stores ellipse-style supervision rather than dense manual skull masks in the original challenge framing, so this module must generate training masks deterministically from the ellipse annotations. citeturn524901search4

---

## 3.2 Target-generation module
Converts annotation parameters into training targets.

### Supported target types
1. **Filled ellipse mask**
2. **Boundary band mask**
3. **Multi-target variant** (optional)
   - channel 1: filled ellipse
   - channel 2: contour band

### Why this module matters
This is the key modeling decision for the project because the training target is not a native segmentation mask from a human contour trace. By isolating it into a standalone module, you can compare supervision styles without touching the rest of the pipeline.

---

## 3.3 Preprocessing module
Standardizes raw images before training.

### Steps
- read grayscale image,
- normalize intensities per image,
- resize to configured resolution,
- transform ellipse/mask consistently,
- optionally apply contrast enhancement.

### Guardrails
- preserve geometry carefully,
- any resize must be mirrored in label generation,
- pixel spacing must be updated if image dimensions are rescaled.

---

## 3.4 Augmentation module
Applied during training only.

### Recommended transforms
- horizontal flip,
- small rotations,
- small scaling / shifts,
- mild brightness / contrast change,
- low-level additive noise.

### Constraint
Augmentations must remain anatomically plausible. Heavy warping is discouraged because the final task is geometric measurement, not just segmentation.

---

## 3.5 Model module
Contains trainable segmentation architectures.

### Baseline architecture
**U-Net**
- encoder-decoder CNN
- skip connections
- 1-channel grayscale input
- 1-channel sigmoid output

### Improved architecture
**Attention U-Net** or **ResUNet**
- identical input/output contract,
- better robustness on low-contrast structures.

### Interface contract
Each model must implement:
- `forward(image) -> logits`
- input shape `[B, 1, H, W]`
- output shape `[B, 1, H, W]`

### Why segmentation is the architectural center
A segmentation-first pipeline is the best fit for the assignment because the project description explicitly says the system should first segment the fetus head and then compute head circumference.

---

## 3.6 Training module
Coordinates optimization and checkpointing.

### Responsibilities
- batching,
- loss computation,
- backpropagation,
- metric tracking,
- checkpoint save/load,
- early stopping.

### Training loop outputs
- train loss per epoch,
- val loss per epoch,
- val Dice / IoU / HD,
- checkpoint for best model.

### Recommended trainer features
- seed control,
- mixed precision optional,
- learning rate scheduler,
- gradient clipping optional,
- CSV / JSON logging.

---

## 3.7 Inference module
Turns a trained checkpoint into final measurement outputs.

### Steps
1. load image,
2. preprocess,
3. run model,
4. threshold probability map,
5. remove small noisy components,
6. fit ellipse to final contour,
7. compute HC in pixels and mm,
8. save overlay image and structured prediction record.

### Output artifact schema
```json
{
  "sample_id": "...",
  "pixel_spacing_mm": [sx, sy],
  "pred_mask_path": "...",
  "ellipse": {
    "cx": 0.0,
    "cy": 0.0,
    "a": 0.0,
    "b": 0.0,
    "theta": 0.0
  },
  "hc_pixels": 0.0,
  "hc_mm": 0.0
}
```

---

## 3.8 Post-processing / geometry module
This module is separate from neural inference on purpose.

### Responsibilities
- contour extraction,
- ellipse fitting,
- circumference calculation,
- geometric cleanup.

### Why split it out
It lets you answer report questions like:
- Is raw-mask HC worse than ellipse-fitted HC?
- How much does geometric smoothing reduce measurement error?

### Default geometry approach
- extract outer contour,
- fit least-squares ellipse,
- compute circumference with Ramanujan approximation.

This matches the general structure used in prior HC18 pipelines: segmentation or skull localization followed by ellipse fitting for measurement. citeturn440750view4turn561040search12

---

## 3.9 Evaluation module
Evaluates both vision quality and clinical measurement quality.

### Segmentation metrics
- Dice
- IoU
- Hausdorff distance / HD95

### Measurement metrics
- signed difference (DF)
- absolute difference (ADF)
- MAE / RMSE

### Evaluation outputs
- experiment summary table,
- per-sample metrics CSV,
- error histogram,
- top-k best and worst examples,
- overlay panel for report.

The original HC18 evaluation style compared methods with DF, ADF, HD, and DSC, so this module should expose those whenever possible. citeturn440750view1

---

## 3.10 Reporting module
Produces report-ready artifacts.

### Responsibilities
- generate tables,
- generate loss curves,
- generate qualitative figure panels,
- save model comparison summaries.

### Suggested outputs
- `results_summary.csv`
- `ablation_table.csv`
- `loss_curve.png`
- `qualitative_grid_best.png`
- `qualitative_grid_failures.png`

---

## 4. Data flow details

## 4.1 Training flow
```text
raw image
  -> parse annotation
  -> generate target mask
  -> preprocess / augment
  -> model forward
  -> loss
  -> optimizer step
  -> validation metrics
  -> checkpoint
```

## 4.2 Evaluation flow
```text
checkpoint + val/test image
  -> preprocess
  -> predicted mask
  -> cleanup
  -> ellipse fit
  -> HC computation
  -> compare to annotation-derived target
  -> save metrics + overlays
```

## 4.3 Report flow
```text
metrics CSVs + saved figures
  -> aggregate statistics
  -> tables
  -> plots
  -> final PDF report inputs
```

---

## 5. Storage design

### Raw data
`data/raw/`
- untouched source files,
- never overwritten.

### Processed data
`data/processed/`
- cached masks,
- resized previews,
- cleaned metadata files.

### Outputs
`outputs/`
- checkpoints,
- predictions,
- figures,
- tables,
- logs.

### Principle
Keep raw, processed, and experiment outputs separate so reruns are reproducible.

---

## 6. Configuration design
Use YAML config files for experiment control.

### Example config sections
- dataset paths
- split seed
- image size
- model name
- loss name
- optimizer params
- scheduler params
- augmentation flags
- inference threshold

### Why config-driven design
It lets Codex add new experiments without editing core training code.

---

## 7. Suggested tech stack
- **PyTorch**
- `torchvision`
- `opencv-python`
- `numpy`
- `pandas`
- `scikit-image`
- `matplotlib`
- `PyYAML`
- optional: `albumentations`

This keeps the stack familiar, light, and easy to package.

---

## 8. Reproducibility requirements
- fixed random seeds,
- explicit config file per run,
- model checkpoint naming with run id,
- save commit hash or experiment tag,
- store per-run metrics in CSV/JSON.

### Minimal reproducibility contract
A grader should be able to run:
```bash
bash Myproject.sh
```
or open:
```text
Myproject.ipynb
```
and regenerate the core reported results with reasonable setup effort.

---

## 9. Failure modes the architecture must handle

### 9.1 Weak skull boundary
Common in first-trimester or low-contrast images.

### 9.2 Spurious bright structures
Ultrasound artifacts may create false boundaries.

### 9.3 Fragmented masks
Model predicts multiple small connected regions.

### 9.4 Good Dice, bad circumference
Boundary roughness may not look severe in overlap metrics but can hurt geometric fitting.

### 9.5 Resize / spacing mismatch
The model may segment correctly in resized pixel space but HC conversion becomes wrong if spacing is not updated properly.

Architecture must therefore separate:
- segmentation quality,
- geometry quality,
- physical-unit conversion.

---

## 10. Architecture decisions and rationale

### Decision 1
**Use segmentation as the primary deep learning task.**
Reason: directly matches the assignment and simplifies analysis.

### Decision 2
**Generate masks from ellipse annotations.**
Reason: HC18 labels are ellipse-based in the original dataset framing. citeturn524901search4

### Decision 3
**Keep ellipse fitting outside the network.**
Reason: easier debugging, better interpretability, easier ablation.

### Decision 4
**Build a config-driven experiment system.**
Reason: makes Codex productive and avoids hard-coded experiments.

### Decision 5
**Limit architecture count.**
Reason: the report rewards analysis more than novelty.

---

## 11. Recommended directory-level ownership
```text
src/data/         -> parsing, masks, splits
src/models/       -> U-Net, Attention U-Net, ResUNet
src/training/     -> trainer, losses, schedulers
src/inference/    -> prediction pipeline
src/evaluation/   -> metrics, error analysis
src/utils/        -> config, logging, geometry helpers
```

---

## 12. Definition of done
The architecture is complete when:
- data loads reproducibly,
- at least one model trains end-to-end,
- inference outputs ellipse + HC in mm,
- evaluation generates both overlap and HC metrics,
- report-ready figures and tables are created automatically.
