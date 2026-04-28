# Submission Checklist

## Course PDF Report

- [x] Maximum 6 pages. Current generated PDF is 4 pages.
- [ ] Introduction explains why fetal HC measurement matters.
- [ ] Method describes U-Net, Attention U-Net, BCE+Dice, ablations, and
  ellipse-based HC measurement.
- [ ] Experiments section discloses local reduced-resource setup:
  - split id `seed42_train698_val152_test149`;
  - train/val/internal-test counts 698 / 152 / 149;
  - image size 256x384;
  - base channels 16;
  - 10 epochs;
  - MacBook MPS compute.
- [ ] Results include segmentation metrics and HC measurement metrics.
- [ ] Results use internal-test rows for final comparison.
- [ ] Post-processing ablation explains why ellipse fitting is used.
- [ ] Conclusion includes lessons learned and future CHPC/full-scale reruns.
- [ ] Citations include HC18, U-Net, Attention U-Net, PyTorch, and any reused
  public code.
- [x] Initial PDF generated at `report/final-report.pdf` for review.

## Code ZIP

See `docs/submission-packaging.md` for the detailed packaging guide.

- [ ] Include `Myproject.sh`.
- [ ] Include `README.md`.
- [ ] Include `requirements.txt`.
- [ ] Include `configs/`.
- [ ] Include `src/`.
- [ ] Include `scripts/`.
- [ ] Include `tests/`.
- [ ] Include `report/`.
- [ ] Include `data/splits/`.
- [ ] Do not include raw HC18 data unless course policy explicitly allows it.

## Saved Artifacts For Fast Verification

Include these if the grader should run `bash Myproject.sh` in fast report-only
mode:

- [ ] `outputs/runs/unet_local_baseline/config.json`
- [ ] `outputs/runs/unet_local_baseline/evaluation/`
- [ ] `outputs/runs/attention_unet_local_baseline/config.json`
- [ ] `outputs/runs/attention_unet_local_baseline/evaluation/`
- [ ] `outputs/runs/attention_unet_local_baseline/predictions/`
- [ ] `outputs/runs/attention_unet_dice_loss/config.json`
- [ ] `outputs/runs/attention_unet_dice_loss/evaluation/`
- [ ] `outputs/runs/attention_unet_aug/config.json`
- [ ] `outputs/runs/attention_unet_aug/evaluation/`
- [ ] `outputs/tables/`

Model checkpoints are not required for report-only verification, but include
`best_model.pt` files if future inference from checkpoints should be possible.

## Verification Commands

Fast verification from saved artifacts:

```bash
bash Myproject.sh
```

Full local rerun from raw data:

```bash
bash Myproject.sh --full-local
```

Quick code checks:

```bash
.venv/bin/python -m pytest tests
bash -n Myproject.sh
```

## Final Local Numbers To Match

Best local internal-test model:

- Run id: `attention_unet_local_baseline`
- Dice: 0.9669
- IoU: 0.9373
- HD95: 2.38 mm
- HC MAE: 3.37 mm
- HC RMSE: 4.68 mm
