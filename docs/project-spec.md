# Project Spec — Automated Measurement of Fetal Head Circumference (HC18)

## 1. Project summary
Build a reproducible deep-learning pipeline in **PyTorch** that estimates fetal head circumference from **2D ultrasound images** using the HC18 challenge dataset. The system will:

1. ingest HC18 images and ellipse annotations,
2. convert ellipse annotations into training targets,
3. train one or more **non-trivial segmentation networks**,
4. convert predicted masks into ellipse parameters,
5. compute head circumference in **mm**, and
6. evaluate segmentation and measurement accuracy with clear ablations.

This scope satisfies the course requirement that the project use a deep neural network with more than one hidden layer, and it keeps the implementation realistic for an individual or 2-person team.

---

## 2. Why this is a good project for the class
This problem is clinically meaningful because head circumference is a standard fetal growth measurement, but manual measurement is operator-dependent and ultrasound images are noisy, low-contrast, and artifact-heavy. The HC18 benchmark contains **1,334** fetal ultrasound images, with **999 training** and **335 test** images, all at **800×540** resolution and with variable pixel size, which makes both segmentation and metric conversion non-trivial. The original challenge and follow-up literature evaluate both geometric overlap and measurement error, commonly using **Dice**, **Hausdorff distance**, **difference / absolute difference in HC**, and related analysis. The dataset annotations are ellipse-based rather than precise skull-boundary masks, so the project must explicitly decide how to convert ellipse labels into training supervision. citeturn708442search0turn984769view0turn440750view1turn524901search4

---

## 3. Recommended scope decision

### Recommended core scope
Implement a **segmentation-first pipeline**:
- **Baseline model:** U-Net
- **Primary improved model:** Attention U-Net or ResUNet
- **Optional stretch model:** U-Net++ or lightweight SegFormer
- **Post-processing:** largest connected component + contour extraction + ellipse fitting
- **Final HC computation:** ellipse-perimeter approximation in mm using pixel spacing metadata

### Why this is the right scope
This is the safest path because:
- it directly matches the assignment statement: segment first, then compute HC;
- it uses standard deep learning components that are easy to justify in the report;
- it allows multiple experiments on loss functions, augmentation, and architecture;
- it avoids over-scoping into detection, multimodal learning, or semi-supervised pipelines.

### What is explicitly out of scope
Do **not** include these unless the base pipeline is already solid:
- transformer-heavy architectures as the main story,
- semi-supervised training,
- GAN-based synthesis,
- real-time clinical deployment,
- trimester classification as a separate task,
- federated learning,
- interactive UI or web app.

---

## 4. Problem formulation

### Input
A 2D fetal ultrasound image plus metadata such as pixel spacing.

### Supervision
Ellipse annotation describing the fetal head contour. Because HC18 does not provide exact skull masks for training in the original challenge format, training targets should be generated as one of the following:
1. **filled ellipse mask**,
2. **ellipse boundary band mask**,
3. both, for comparison. citeturn524901search4

### Output
- predicted head mask,
- fitted ellipse parameters,
- predicted HC in pixels and mm.

### Primary task
Binary segmentation of fetal head region / contour.

### Derived task
Geometric measurement of head circumference from the predicted segmentation.

---

## 5. Research questions
The report should answer questions like these:

1. How well does a plain U-Net perform on HC18?
2. Does attention / residual design improve robustness on noisy ultrasound boundaries?
3. Which target representation works better: filled ellipse mask or boundary band mask?
4. Which loss is best: BCE+Dice, Dice only, or Focal/Tversky-style loss?
5. How much do ultrasound-specific augmentations help?
6. Does post-processing with ellipse fitting materially reduce HC error compared to reading directly from raw masks?

---

## 6. Success criteria

### Minimum viable project
The project is successful if it includes:
- one working segmentation model,
- one reproducible train/val split,
- inference pipeline from image -> mask -> ellipse -> HC,
- quantitative evaluation,
- at least 2–3 meaningful experiments.

### Strong project
A strong submission includes:
- a solid U-Net baseline,
- at least one better architecture,
- a loss/augmentation ablation,
- error analysis by image difficulty or trimester proxy,
- reproducible scripts and clean report figures.

### Stretch success
If time remains:
- ensemble 2 models,
- compare mask-based circumference vs ellipse-fitted circumference,
- add uncertainty estimates with test-time augmentation.

---

## 7. Dataset plan

### Dataset
Use the **HC18** dataset.

### Important dataset facts to account for
- 1,334 total images
- 999 training / 335 test images
- image size 800×540
- variable pixel size roughly 0.052–0.326 mm
- images span all trimesters, with first trimester being harder in prior work due to weaker skull visibility. citeturn708442search0turn984769view0turn440750view3

### Split strategy
Because report writing needs labeled evaluation, use one of these:

#### Option A — safest for coursework
Split the labeled training set into:
- train: 70%
- val: 15%
- internal test: 15%

If metadata supports it, avoid leakage by grouping images from the same exam/patient into the same split, similar to how the original paper kept examinations together. citeturn440750view3

#### Option B — if official held-out labels are available to you
Use the official train/test split and create a validation split from training only.

### Annotation conversion
Convert ellipse parameters to a binary mask at image resolution. Also generate:
- contour points,
- ellipse center / axes / rotation,
- pixel-to-mm conversion factors.

---

## 8. Model plan

### Model 1 — Baseline
**U-Net**
- encoder-decoder CNN
- binary segmentation output
- simple, strong, easy to explain

### Model 2 — Improved
**Attention U-Net** or **ResUNet**
- better focus on relevant regions,
- often more stable on noisy medical boundaries.

### Optional Model 3 — Stretch
**U-Net++** or lightweight **SegFormer**
- only if baseline experiments are already complete.

### Recommended loss functions to try
1. BCE + Dice loss
2. Dice loss
3. Focal + Dice or Tversky-style loss for boundary imbalance

### Regularization / training ideas to try
- early stopping
- weight decay
- dropout only if empirically useful
- cosine schedule or ReduceLROnPlateau
- mixed precision if GPU allows

---

## 9. Preprocessing and augmentation plan

### Preprocessing
- preserve aspect ratio if possible,
- resize to a manageable shape such as 512×352 or 640×432,
- normalize image intensities per image,
- optional contrast enhancement such as CLAHE only as an experiment.

### Augmentation
Start simple and clinically plausible:
- horizontal flip
- mild rotation
- translation / scaling
- brightness / contrast jitter
- Gaussian noise
- elastic deformation only if it does not destroy anatomy realism

Do not use aggressive augmentations that create anatomically implausible fetal head shapes.

---

## 10. Post-processing plan
After model prediction:
1. threshold probability map,
2. keep largest connected component,
3. optionally smooth contour,
4. fit ellipse to contour points,
5. compute circumference in pixels,
6. convert to mm using pixel spacing.

### Circumference formula
Use an ellipse-perimeter approximation such as Ramanujan’s formula for semi-axes `a` and `b`:

`HC ≈ π [ 3(a+b) - sqrt((3a+b)(a+3b)) ]`

This makes the measurement stage easy to explain and reproducible.

---

## 11. Evaluation plan

### Segmentation metrics
- Dice similarity coefficient
- IoU
- Hausdorff distance or HD95

### Measurement metrics
- signed HC difference (mm)
- absolute HC difference (mm)
- MAE / RMSE for HC

### Analysis views for the report
- train vs val curves,
- table of model/loss/augmentation comparisons,
- qualitative overlays,
- failure cases,
- boundary-quality vs measurement-error discussion.

These choices align well with the original HC18 evaluation style, which reported DF, ADF, HD, and DSC. citeturn440750view1turn440750view4

---

## 12. Experiment matrix

### Phase 1 — establish baseline
- U-Net + BCE/Dice
- no fancy preprocessing
- standard augmentation

### Phase 2 — improve architecture
- Attention U-Net or ResUNet
- same preprocessing for fair comparison

### Phase 3 — improve supervision / losses
- filled mask vs boundary-band mask
- Dice vs BCE+Dice vs Focal+Dice

### Phase 4 — improve inference
- with vs without connected-component cleanup
- raw contour vs ellipse-fitted HC

Ablation count target: **5–8 total runs**, not 20+.

---

## 13. Deliverables

### Code deliverables
- `Myproject.sh` **or** `Myproject.ipynb`
- training script
- evaluation script
- inference script
- config file(s)
- saved best checkpoints
- figure-generation notebook/script

### Report deliverables
A PDF of at most **6 pages** with:
1. introduction,
2. method,
3. experiments,
4. conclusions.

### Reproducibility deliverables
- exact package versions,
- random seed handling,
- README with commands,
- clear directory structure.

---

## 14. Proposed repo structure
```text
fetal-hc-project/
├── data/
│   ├── raw/
│   ├── processed/
│   └── splits/
├── notebooks/
├── src/
│   ├── data/
│   ├── models/
│   ├── training/
│   ├── evaluation/
│   ├── inference/
│   └── utils/
├── outputs/
│   ├── checkpoints/
│   ├── predictions/
│   ├── figures/
│   └── tables/
├── configs/
├── tests/
├── Myproject.sh
├── README.md
└── report/
```

---

## 15. Timeline

### Week 1
- download / inspect HC18
- parse annotations
- create masks
- build dataloader
- run sanity visualizations

### Week 2
- implement U-Net baseline
- train first model
- evaluate segmentation and HC pipeline end-to-end

### Week 3
- add improved model
- run loss / augmentation ablations
- save qualitative figures

### Week 4
- finalize best model
- run clean experiments
- write report
- package reproducible code

---

## 16. Risks and mitigation

### Risk 1: labels are ellipse-only, not true masks
**Mitigation:** make this part of the method; train on generated ellipse masks and acknowledge the supervision limitation.

### Risk 2: measurement looks good but segmentation is visually rough
**Mitigation:** evaluate both segmentation and HC error; use ellipse fitting as the canonical measurement output.

### Risk 3: over-scoping architectures
**Mitigation:** lock baseline + one improved model before trying anything else.

### Risk 4: data leakage
**Mitigation:** split by exam/patient when metadata permits; document split methodology clearly.

### Risk 5: limited compute
**Mitigation:** resize inputs, use mixed precision, cap epochs, and prioritize clean ablations over many architectures.

---

## 17. Final recommendation
If you are building this with Codex, the best project story is:

> "We implemented an end-to-end PyTorch pipeline for fetal head circumference estimation on HC18. We trained deep segmentation models using ellipse-derived supervision, converted predictions into geometric ellipse fits, and evaluated both overlap and clinically meaningful measurement error."

That is well-scoped, defensible, and strong enough for the assignment.

---

## 18. References to ground the scope
- HC18 Grand Challenge dataset description.
- van den Heuvel et al., 2018, *Automated measurement of fetal head circumference using 2D ultrasound images*.
- Cabezas et al., 2024, dataset note explaining HC18 annotations are ellipse-based rather than precise skull masks.
