# Final Report Outline

Target length: 6 pages maximum.

## Title

Automated Fetal Head Circumference Measurement from 2D Ultrasound Using
Attention U-Net and Ellipse-Based Geometry

## 1. Introduction

Head circumference is a standard fetal growth biomarker measured during
prenatal ultrasound. Manual measurement requires identifying the fetal skull
boundary and fitting an ellipse, which can be time-consuming and operator
dependent. This project studies a segmentation-first deep learning pipeline for
HC18 fetal ultrasound images: predict the fetal head mask, fit an ellipse to
the predicted mask, and compute head circumference in millimeters.

Key challenges to mention:

- ultrasound images have speckle noise, low contrast, and shadowing;
- the fetal skull boundary can be partial or ambiguous;
- segmentation quality must translate into accurate physical measurements;
- compute limits required a reduced local training setup.

## 2. Method

Pipeline:

```text
image -> segmentation model -> binary mask -> largest component -> ellipse fit -> HC in mm
```

Models:

- U-Net baseline;
- Attention U-Net improved model with additive attention gates on skip
  connections.

Training:

- PyTorch script-first pipeline;
- AdamW optimizer;
- BCE+Dice loss for the main runs;
- Dice-only loss ablation;
- training-only augmentation ablation with horizontal flip, intensity scaling,
  intensity shift, and mild Gaussian noise.

Post-processing:

- threshold model probabilities at 0.5;
- keep the largest connected component;
- fit an ellipse to the external contour;
- compute circumference from sampled ellipse points scaled by pixel spacing.

## 3. Experiments

Dataset:

- HC18 labeled training set;
- train/validation/internal-test split: 698 / 152 / 149 images;
- split id: `seed42_train698_val152_test149`;
- internal test split is held out from labeled training images and is not the
  official unlabeled HC18 challenge test set.

Reduced-resource setup:

- image size: 256x384;
- base channels: 16;
- epochs: 10;
- compute: MacBook MPS.

Metrics:

- Dice and IoU for segmentation overlap;
- HD95 in mm for boundary distance;
- signed HC error, MAE, and RMSE in mm for measurement accuracy.

Main model comparison:

Use `report/tables/main_test_results.csv`.

Suggested compact table columns:

- Experiment;
- Dice;
- IoU;
- HD95 mm;
- HC MAE mm;
- HC RMSE mm.

Main result:

Attention U-Net + BCE/Dice was best on internal test:

- Dice: 0.9669;
- IoU: 0.9373;
- HD95: 2.38 mm;
- HC MAE: 3.37 mm;
- HC RMSE: 4.68 mm.

Ablation discussion:

- Dice-only loss underperformed BCE+Dice on HC RMSE;
- the simple augmentation recipe did not improve internal-test HC error;
- direct contour-length measurement substantially overestimated HC;
- ellipse fitting reduced HC MAE from 16.73 mm for raw contour length to
  3.37 mm.

Figures to include:

- `report/figures/main_test_hc_mae.png`;
- `report/figures/main_test_dice.png`;
- `report/figures/postprocess_test_hc_mae.png`;
- one qualitative overlay panel from `outputs/figures/attention_unet_local_baseline/`.

## 4. Conclusions

Attention U-Net improved over the U-Net baseline for both segmentation and HC
measurement under the local reduced-resource setup. BCE+Dice was more reliable
than Dice-only loss, and the tested simple augmentation did not help. The
geometry stage was important: direct contour length gave large overestimates,
while ellipse fitting produced much lower HC error.

Future work:

- run larger 352x512/base32 configs on CHPC;
- tune augmentation strength and training duration;
- inspect high-error cases qualitatively;
- optionally build a lightweight demo for resume/project presentation.

## Required Citations To Add

- HC18 challenge/dataset source;
- U-Net paper;
- Attention U-Net paper;
- PyTorch;
- any public code if added later.
