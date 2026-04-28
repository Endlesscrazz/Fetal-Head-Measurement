# Report Assets Index

Use this file to assemble the final PDF report and course ZIP.

## Core Summary

- `report/report-results-summary.md`
- `report/final-report-outline.md`
- `report/final-report-draft.md`
- `report/final-report.md`
- `report/final-report.pdf`
- `report/submission-checklist.md`

## Tables

- `report/tables/main_test_results.csv`
- `report/tables/main_test_results.md`
- `report/tables/attention_unet_ablation_test_results.csv`
- `report/tables/attention_unet_ablation_test_results.md`
- `report/tables/postprocess_test_results.csv`
- `report/tables/postprocess_test_results.md`

Recommended table for the main report:

- `report/tables/main_test_results.md`

Recommended table for the post-processing ablation:

- `report/tables/postprocess_test_results.md`

## Figures

- `report/figures/main_test_hc_mae.png`
- `report/figures/main_test_dice.png`
- `report/figures/postprocess_test_hc_mae.png`

Optional qualitative figures:

- `outputs/figures/attention_unet_local_baseline/test_qualitative_failures.png`
- `outputs/figures/attention_unet_local_baseline/val_qualitative_failures.png`
- `outputs/figures/data_overlays/`

## Reproducibility Inputs

Fast report-only runner requires:

- `outputs/runs/*/config.json`
- `outputs/runs/*/evaluation/*/aggregate_metrics.csv`
- `outputs/runs/attention_unet_local_baseline/predictions/*/predictions.csv`
- `outputs/runs/attention_unet_local_baseline/predictions/*/masks/`
- `outputs/tables/`

Full local rerun requires:

- raw HC18 data under `data/raw/HC18/`;
- configs under `configs/`;
- source code under `src/`;
- `Myproject.sh`.

Checkpoints are useful for future inference but are not required for
`bash Myproject.sh` in default report-only mode.
