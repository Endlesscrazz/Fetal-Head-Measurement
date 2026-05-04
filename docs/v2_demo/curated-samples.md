# V2 Curated Demo Samples

Date: 2026-05-01

Source run:
`attention_unet_local_baseline`

Source split:
internal `test`

Source files:

- `outputs/runs/attention_unet_local_baseline/evaluation/test/per_sample_metrics.csv`
- `outputs/runs/attention_unet_local_baseline/evaluation/test/postprocess_ablation_per_sample.csv`
- `outputs/runs/attention_unet_local_baseline/predictions/test/predictions.csv`

Purpose:
This set gives the saved-output React demo enough variety to teach the
pipeline, not just show the best-looking outputs. It includes strong examples,
a typical case, a cleanup/ellipse comparison case, and clear failure/high-error
cases.

The machine-readable companion file is `docs/v2_demo/curated-samples.json`.
Exporter code should read the JSON, not this Markdown file.

## Selected Samples

| Sample | Category | Dice | HC Error mm | Why include it |
|---|---:|---:|---:|---|
| `296_HC` | strong | 0.9907 | 0.03 | Best headline example: excellent mask overlap and near-perfect HC measurement. |
| `217_HC` | strong | 0.9869 | 0.13 | Second strong example with a different HC size, useful for showing consistency. |
| `663_HC` | typical | 0.9815 | 2.33 | Median-like HC error, good for explaining normal model behavior without cherry-picking. |
| `089_HC` | typical | 0.9743 | 0.28 | Cleaner geometry teaching case: cleanup narrows the contour, then ellipse fitting clearly beats the cleaned contour on final HC. |
| `793_HC` | failure | 0.9297 | 19.92 | Large-head high-error case with high HD95; useful for honest error analysis. |
| `032_HC` | failure | 0.8316 | 11.84 | Low-Dice small-HC failure case; good for discussing limits on weaker segmentation. |

## Category Rationale

- **strong**: samples with high Dice and very low absolute HC error. These show
  the intended success path from image to measurement.
- **typical**: samples near ordinary model behavior, including the
  cleanup/ellipse teaching case. For `089_HC`, raw contour HC error is
  51.31 mm, cleaned contour HC error is 3.83 mm, and cleaned ellipse HC error is
  0.28 mm.
- **failure**: cases where the final HC measurement or segmentation quality is
  substantially weaker despite a completed prediction pipeline.

## Export Notes

For each selected sample, the v1 run already has:

- prediction row in `predictions.csv`,
- raw mask under `predictions/test/masks/`,
- cleaned mask under `predictions/test/masks/`,
- ellipse overlay under `predictions/test/overlays/`,
- evaluation row in `per_sample_metrics.csv`.

`V2.S2` must still export the original image, annotation-derived target mask,
cleaned prediction mask, and checkpoint-derived probability map from local
artifacts. It must store contour measurement as `contourHC` in the React
manifest.
