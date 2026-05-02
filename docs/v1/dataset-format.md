# HC18 Dataset Format Notes

Last inspected: 2026-04-25

## Local Inspection Result

Downloaded archive:

```text
/Users/shreyas/Downloads/1327317.zip
```

Project raw-data root:

```text
data/raw/HC18/
```

Observed local layout after extraction:

```text
data/raw/HC18/
├── training_set/
│   ├── 000_HC.png
│   ├── 000_HC_Annotation.png
│   └── ...
├── test_set/
│   ├── 000_HC.png
│   └── ...
├── training_set.zip
├── test_set.zip
├── training_set_pixel_size_and_HC.csv
└── test_set_pixel_size.csv
```

Observed counts:

- training ultrasound images: 999
- training annotation images: 999
- test ultrasound images: 335
- training CSV shape: `(999, 3)`
- test CSV shape: `(335, 2)`
- sample image shape: `(540, 800)`
- sample annotation shape: `(540, 800)`

## Observed CSV Columns

`training_set_pixel_size_and_HC.csv`:

```text
filename, pixel size(mm), head circumference (mm)
```

`test_set_pixel_size.csv`:

```text
filename, pixel size(mm)
```

The training CSV provides labeled HC values for report evaluation. The official
test CSV does not include HC labels, so v1 uses an internal train/val/test split
from the labeled training set.

## Supported Target Sources

1. Paired annotation images next to the ultrasound image, such as
   `000_HC_Annotation.png`.
2. Explicit ellipse columns in metadata, if a future dataset variant provides
   them.

Observed HC18 annotation images encode ellipse contours. The dataset code
converts them into:

- filled masks when `target_type: filled`;
- boundary-band masks when `target_type: boundary`.

## Geometry Assumptions

- Images are read as grayscale.
- Model tensors use `[1, H, W]`.
- Pixel spacing is tracked as `(sx_mm, sy_mm)`, where `sx_mm` is horizontal
  millimeters per pixel and `sy_mm` is vertical millimeters per pixel.
- If an image is resized from `(H, W)` to `(H2, W2)`, spacing is updated as:
  - `sx2 = sx * W / W2`
  - `sy2 = sy * H / H2`
- Masks are resized with nearest-neighbor interpolation only.

## Verification

- `discover_hc18_records("data/raw/HC18", subset="training")` finds 999 labeled
  records.
- `.venv/bin/python -m src.data.make_splits --config configs/data.yaml`
  generated train 698, val 152, test 149.
- `.venv/bin/python scripts/visualize_samples.py --config configs/data.yaml --n 10`
  generated 10 overlay figures under `outputs/figures/data_overlays/`.
