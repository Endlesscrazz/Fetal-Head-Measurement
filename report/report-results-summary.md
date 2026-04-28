# Local V1 Report Results Summary

These artifacts summarize the local reduced-resource v1 experiments for the
HC18 fetal head circumference project.

## Local Setup

- Split id: `seed42_train698_val152_test149`
- Train/val/internal-test counts: 698 / 152 / 149
- Image size: `256x384`
- Base channels: `16`
- Epochs per reported local run: `10`
- Compute: MacBook MPS
- Final HC measurement method: cleaned largest component + ellipse fitting

The local setup uses the full labeled HC18 training split partition but reduced
image resolution and model width. This should be disclosed in the course report.

## Best Local Model

Best internal-test model by HC MAE:

- Experiment: Attention U-Net + BCE/Dice
- Run id: `attention_unet_local_baseline`
- Dice: 0.9669
- IoU: 0.9373
- HD95: 2.38 mm
- HC MAE: 3.37 mm
- HC RMSE: 4.68 mm

## Report Tables

- `report/tables/main_test_results.csv`
- `report/tables/attention_unet_ablation_test_results.csv`
- `report/tables/postprocess_test_results.csv`

## Report Figures

- `report/figures/main_test_hc_mae.png`
- `report/figures/main_test_dice.png`
- `report/figures/postprocess_test_hc_mae.png`

## Suggested Interpretation

Attention U-Net with BCE+Dice gave the best local v1 result. Dice-only loss and
the simple augmentation recipe did not improve internal-test HC error. Direct
contour-length measurement substantially overestimated HC, while ellipse fitting
reduced HC error and supports the segmentation-to-geometry design.
