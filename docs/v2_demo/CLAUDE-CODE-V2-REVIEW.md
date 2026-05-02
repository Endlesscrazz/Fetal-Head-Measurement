# V2 Demo Plan Review

Superseded context:
This review captured the pre-Claude-Design Streamlit plan. It remains useful for
the saved-output-first reasoning, artifact-export gap, safety disclaimer, and
contour-vs-ellipse emphasis. The current MVP framework is Vite + React +
TypeScript, with details in `frontend-design-handoff.md`, `architecture.md`, and
`project-tasks.md`.

Reviewed: 2026-04-28
Reviewer: Claude Code (claude-sonnet-4-6)
Files reviewed: project-spec.md, architecture.md, roadmap.md, DECISIONS.md, AGENTS.md
Also inspected: outputs/ tree, src/ tree

---

## Overall assessment

The plan is solid. The saved-output-first strategy is the right call for a portfolio
demo. The mission, audience, and MVP criteria are well-defined. The DECISIONS.md is
unusually thorough — the rationale entries are exactly what you want when picking this
back up after a break.

The main issues are concrete gaps between what the plan says will exist and what
actually exists in outputs/ right now, plus a few underspecified components that
will cause friction when you start implementing P3.

---

## What is strong

- **Saved-output-first** — correct call. Avoids checkpoint distribution,
  preprocessing, and GPU-availability issues for a portfolio demo.
- **Audience definition** — primary vs secondary audience in project-spec.md is
  clear and drives the right UI decisions (visual over textual).
- **Adapter abstraction** — separating saved-output and live-inference modes so
  the UI is stable is the correct architecture for this scope.
- **Safety disclaimer is a first-class requirement**, not an afterthought.
- **DECISIONS.md format** — decision + rationale + alternatives + impact is exactly
  right and will save you time resuming across sessions.

---

## Gaps and issues

### 1. The per-sample artifacts do not exist yet — P2 is blocking P3

This is the most significant gap. The roadmap treats P2 (artifact curation) as a
logistics task ("choose samples, write manifest"). But looking at outputs/:

```
outputs/figures/                  ← multi-panel composite PNGs per run (histograms, failure grids)
outputs/tables/                   ← CSVs with aggregate metrics per run
outputs/figures/data_overlays/    ← 10 GT annotation overlays (not prediction outputs)
outputs/runs/*/best_model.pt      ← checkpoints
```

What the Streamlit app actually needs for each sample is:
- the original grayscale ultrasound image
- the target mask (derived from annotation)
- the raw prediction mask or probability map
- the cleaned (post-processed) mask
- the ellipse overlay image
- the per-sample HC prediction in mm

None of these per-sample stage artifacts exist in outputs/ as individual files. The
qualitative failure figures that exist are multi-panel composites saved as a single
PNG — not usable as individual sample views.

**Action required before P3 can start:** Write a small artifact-export script
(`scripts/export_demo_artifacts.py`) that:
1. loads a checkpoint,
2. runs inference on a small fixed set of sample IDs,
3. saves each pipeline stage (raw mask, cleaned mask, ellipse overlay, HC value) to
   `outputs/demo_samples/<sample_id>/`,
4. writes the manifest JSON.

This is effectively a P2.5 that the roadmap does not currently contain. Add it.

### 2. Manifest schema is not defined

P2 says "a demo sample manifest" but neither architecture.md nor roadmap.md defines
what the manifest looks like. When P3 starts, whoever writes the sample selector will
invent a schema, and it may not match what the artifact export script produced.

Define the manifest schema now, even if it changes. A minimal example:

```json
{
  "samples": [
    {
      "id": "199",
      "label": "Strong prediction",
      "split": "test",
      "image_path": "outputs/demo_samples/199/image.png",
      "target_mask_path": "outputs/demo_samples/199/target_mask.png",
      "raw_mask_path": "outputs/demo_samples/199/raw_mask.png",
      "cleaned_mask_path": "outputs/demo_samples/199/cleaned_mask.png",
      "ellipse_overlay_path": "outputs/demo_samples/199/ellipse_overlay.png",
      "hc_pred_mm": 183.4,
      "hc_gt_mm": 180.1,
      "dice": 0.94
    }
  ]
}
```

Add this to architecture.md or as a separate `manifest-schema.md`.

### 3. Demo directory structure is not defined

AGENTS.md says "add demo-specific code under a clearly named demo/app area in a
future implementation task" but no document says what that area is. When P3 starts,
someone has to decide:

- `demo/app.py` + `demo/components/`?
- `app/main.py`?
- a top-level `streamlit_app.py`?

This matters because it affects imports from `src/` and the run command
(`streamlit run demo/app.py`). Decide now and add one line to architecture.md.

Recommendation: `demo/app.py` with `demo/components/` for reusable panels.
Run command: `streamlit run demo/app.py`.

### 4. Streamlit is not in requirements.txt

requirements.txt covers v1 training dependencies. When P3 starts, streamlit + any
demo-only deps (e.g. plotly if used for interactive ellipse vis) need to land
somewhere. Options:

- Add a `requirements-demo.txt` (keeps v1 env clean, separates concerns).
- Add a `[demo]` extras section if you move to pyproject.toml.

The plan does not mention this at all. P3 done criteria should include
"demo dependencies documented and installable."

### 5. The contour-vs-ellipse comparison is undersold

Both project-spec.md and architecture.md mark this "where feasible." Based on your
v1 work, the contour-vs-ellipse tradeoff was one of the most interesting findings
— ellipse regularization corrects for mask noise in ways that direct contour
measurement cannot. This is exactly the kind of thing an ML interviewer or recruiter
will ask about.

The app should always show this comparison if the ellipse fit succeeds. Demote the
"where feasible" hedge — it should be a core feature, not a stretch. The existing
geometry utilities in `src/utils/geometry.py` already support both paths.

### 6. Training curves are missing from the experiment dashboard plan

The architecture says the dashboard will show "result tables and figures" including
ablations and HC MAE figures. But `outputs/runs/*/metrics.csv` contains epoch-by-epoch
training and validation loss. A loss-curve plot (train loss vs val loss per epoch for
each run) is one of the most readable ways to explain the training story to a
non-specialist audience. It also differentiates your demo from a static results table.

Add "training loss curve per run" to the experiment dashboard component description
in architecture.md.

### 7. P4 adapter interface has no contract

The plan says the live-inference adapter produces "the same stage objects as saved-
output mode" but never defines what those objects are. For the architecture to hold,
you need a minimal data contract — something like:

```python
@dataclass
class DemoSample:
    id: str
    image: np.ndarray        # HxW uint8
    target_mask: np.ndarray  # HxW binary
    raw_mask: np.ndarray     # HxW binary
    cleaned_mask: np.ndarray # HxW binary
    ellipse_params: dict     # center, axes, angle
    hc_pred_mm: float
    hc_gt_mm: float | None
```

Both the saved-output loader and the live-inference adapter return a `DemoSample`.
The UI only talks to `DemoSample`. Define this in architecture.md now, even if the
fields change. It is the single most important design decision for making P4 a drop-in
addition rather than a rewrite.

### 8. No plan for demo artifact distribution on GitHub

The plan correctly says "do not commit raw data or checkpoints." But if a recruiter
or interviewer clones the repo, they cannot run the demo because the curated sample
artifacts will not exist. The plan does not address this.

Options to consider:
- **Git LFS** for the curated artifacts (a few MBs of PNGs + JSONs) — simplest.
- **GitHub Release asset** — upload a `demo-artifacts-v1.zip` as a release attachment,
  add a `scripts/download_demo_artifacts.sh` that fetches and extracts it.
- **Embed a tiny hardcoded set** — 3-5 samples small enough to commit as PNGs (~50KB
  each grayscale) without LFS.

The README polish (P5) will be incomplete without a decision here, because the run
instructions depend on whether the user needs to download artifacts separately.
Make this decision before starting P3 so the artifact paths are stable.

### 9. P5 (portfolio polish) needs one concrete addition: a single-command start

Recruiters and interviewers should be able to clone and run in under 60 seconds. The
P5 done criteria should explicitly require a one-command start:

```bash
# Option A: make
make demo

# Option B: shell script
./start_demo.sh

# Option C: just document the two commands
pip install -r requirements-demo.txt && streamlit run demo/app.py
```

Add this to P5 verification criteria.

### 10. No timeline or priority among P2–P6

Given your June 9 OPT deadline, P2+P3 is the critical path — that is the portfolio
artifact. P4 (live inference) adds polish but P5 (README + screenshots + GIF) is what
actually makes it recruiter-visible. P6 (challenge CSV) is a nice-to-have.

Rough effort estimates to help prioritize:

| Phase | Effort | Value |
|---|---|---|
| P2 (artifact export + manifest) | 3–5 hours | Required |
| P3 (Streamlit app) | 8–12 hours | Required |
| P4 (live inference) | 6–10 hours | High (interview depth) |
| P5 (polish + GIF) | 3–4 hours | High (LinkedIn visibility) |
| P6 (challenge CSV) | 4–6 hours | Low unless targeting leaderboard) |

Add rough effort estimates to the roadmap so you can sequence realistically against
your deadline.

---

## Small issues

- `handoff.md` is referenced in AGENTS.md as a required read but it does not appear
  in the outputs of `git status`. Confirm it exists or remove the reference.
- The roadmap verification for P2 says "manifest validates paths" but does not specify
  what tool runs the validation. Add a concrete command
  (`python scripts/validate_manifest.py`).
- architecture.md section 4 says the geometry view should "make the contour-vs-ellipse
  tradeoff visible because this was one of the strongest v1 findings" — good — but
  section 4 (CNN prediction) says "label this as the thresholded prediction output
  rather than pretending to show probabilities." If the checkpoints are already
  committed under `outputs/runs/`, you can extract probabilities at demo time in P4.
  Flag this in DECISIONS.md so you don't forget.

---

## Suggested additions to the roadmap

```
## V2.P2.5 - Demo artifact export script

Status: todo

Goal:
Write a script that runs inference on a small fixed sample set and saves each
pipeline stage as individual files for the saved-output demo.

Expected files:
- scripts/export_demo_artifacts.py
- outputs/demo_samples/<id>/{image,target_mask,raw_mask,cleaned_mask,ellipse_overlay}.png
- outputs/demo_samples/<id>/metadata.json  (hc_pred_mm, hc_gt_mm, dice, ellipse_params)
- outputs/demo_samples/manifest.json

Verification:
- script runs to completion with at least 5 samples (mix of good and failure cases)
- manifest.json validates against the schema in architecture.md
- no raw training data is required to run the Streamlit app after this step

Done criteria:
- saved-output demo has a stable, checkpoint-independent artifact set
```

---

## Summary

The plan is well-structured and the decisions are sound. The three things to fix
before writing any Streamlit code:

1. **Add P2.5** (artifact export script) — the per-sample stage files do not exist yet.
2. **Define the manifest schema** in architecture.md.
3. **Define the DemoSample dataclass contract** in architecture.md — this is the
   foundation the adapter pattern depends on.

Everything else above is improvement, not blockers.

---

# Round 2 Review

Reviewed: 2026-05-01
Files reviewed: architecture.md (updated), roadmap.md (updated), project-spec.md (updated),
  docs/v2_demo/project-tasks.md (new), root project-tasks.md (updated)
Also inspected: outputs/runs/attention_unet_local_baseline/ full tree, predictions.csv schema,
  per_sample_metrics.csv schema, .gitignore

---

## What was addressed from Round 1

All ten Round 1 items are resolved:

- P2.5 artifact export phase added ✅
- Manifest JSON schema defined in architecture.md ✅
- `DemoSample` dataclass contract defined in architecture.md ✅
- Demo directory layout (`demo/app.py`, `demo/components/`, `demo/adapters/`) defined ✅
- `requirements-demo.txt` called out in P3 and V2.S4 ✅
- Contour-vs-ellipse elevated to core feature, "where feasible" hedge removed ✅
- Training loss curves added to experiment dashboard spec ✅
- Distribution policy documented in architecture.md section 9 ✅
- Effort estimates added to all roadmap phases ✅
- One-command start added to P5 verification and V2.S6 subtasks ✅

The new `docs/v2_demo/project-tasks.md` session plan is a strong addition.

---

## What is strong in the session plan

- **Session split S3/S4** — separating the data adapter (S3) from the Streamlit UI (S4)
  is the right call. It means the adapter can be tested without launching a browser, and
  UI sessions won't be blocked on data loading bugs.
- **Allowed implementation files** per session — scope-locking each session to specific
  files prevents agents from expanding scope unilaterally. This is the right constraint.
- **MVP Exit Checklist** at the end of project-tasks.md — one clear gate for "done" is
  exactly what this kind of portfolio project needs.
- **V2.S1 references actual artifact paths** for verification — referencing
  `outputs/runs/attention_unet_local_baseline/evaluation/test/per_sample_metrics.csv` is
  concrete and correct (these paths were confirmed to exist in the v1 outputs).

---

## Remaining gaps

### 1. `contour_hc_mm` is not in any v1 output — V2.S2 must compute it

The `DemoSample` dataclass and the `metadata.json` schema both include `contour_hc_mm`.
But after inspecting the actual v1 outputs:

- `predictions/test/predictions.csv` — has `hc_mm` (ellipse-based) and ellipse params, but no `contour_hc_mm`
- `evaluation/test/per_sample_metrics.csv` — has `pred_hc_mm`, `target_hc_mm`, but no `contour_hc_mm`

The contour-vs-ellipse comparison was identified as a post-processing ablation result
(stored in `outputs/tables/local_postprocess_ablation_summary.csv`), but the per-sample
contour HC value is not in the saved per-sample files.

**V2.S2 subtask list needs an explicit step:**

> Compute contour HC for each selected sample by loading the saved cleaned mask and
> calling the contour path in `src/utils/geometry.py`. Store the result in
> `metadata.json` as `contour_hc_mm`.

Without this, the contour-vs-ellipse panel in V2.S5 will always show `null` for
contour HC, and the feature that was elevated to core will be invisible.

### 2. V2.S2 implicit raw data dependency is undocumented

The exporter needs `data/raw/HC18/training_set/` present locally for two tasks:

1. **Copying the original image** — `predictions.csv` stores images as
   `data/raw/HC18/training_set/<sample_id>.png` (not in the demo bundle yet)
2. **Generating the target mask** — requires reading the HC18 annotation CSV and
   pixel spacing from the raw dataset

V2.S2 verification currently only shows:
```bash
.venv/bin/python scripts/export_demo_artifacts.py --run-id attention_unet_local_baseline --split test
```

This will silently fail or raise a confusing error if `data/raw/HC18/` is absent.

Add a prerequisite check to V2.S2 done criteria and verification:
```bash
test -d data/raw/HC18/training_set
```
And document it clearly: "V2.S2 requires `data/raw/HC18/` to be present locally.
After export, the demo runs without it."

### 3. The exporter should not parse `curated-samples.md`

V2.S2 subtask says: "Implement an exporter that reads curated samples from
`docs/v2_demo/curated-samples.md` or an explicit `--sample-id` list."

Parsing a Markdown file in a Python script is fragile and will break if the
document formatting changes. The `curated-samples.md` file (produced by V2.S1) is
documentation — not machine input.

Two clean options:
- **Option A:** `--sample-id` list only. V2.S1 produces the Markdown rationale;
  V2.S2 receives sample IDs explicitly at call time. Simple and robust.
- **Option B:** V2.S1 produces both `curated-samples.md` (human-readable) and
  `docs/v2_demo/curated-samples.json` (machine-readable), and the exporter reads the JSON.

Option A is simpler. Option B is better if multiple sessions need to reference the
same sample list. Either way, remove the Markdown parsing path.

### 4. `contour_hc_mm` is missing from the MVP Exit Checklist

The checklist requires: image, target mask, raw prediction, cleaned mask, ellipse
overlay, HC measurement, safety disclaimer, experiment results, and loss curves.

But "app shows contour-vs-ellipse comparison when both values are available" is
not in the checklist — despite being elevated to a core feature in architecture.md,
project-spec.md, and V2.S5.

Add it. Otherwise the MVP gate can be declared done with a silently null contour
panel.

### 5. V2.S6 re-opens the artifact distribution decision

V2.S6 lists "Decide how reviewers get demo artifacts" as a subtask. But
architecture.md section 9 already defines the decision as three explicit options
(GitHub Release zip, screenshots/GIF, local-generation command). The choice between
them is deliberately deferred until after the MVP works.

The V2.S6 subtask is fine conceptually, but the wording makes it sound like an open
question. Change it to: "Choose and execute the artifact distribution strategy from
`docs/v2_demo/architecture.md` section 9." This avoids re-litigating the decision
in the session.

### 6. V2.S3 smoke test will fail in a fresh environment

The V2.S3 verification includes this smoke test:
```bash
.venv/bin/python -c "from demo.adapters.saved_output import load_manifest; print(load_manifest('outputs/demo_samples/manifest.json').safety_text)"
```

This will fail in any environment where V2.S2 hasn't run yet (fresh clone, CI,
another machine). The import test is useful; the manifest load test should be
separated into a test that's marked as requiring a local artifact bundle.

Suggest splitting the V2.S3 verification into:
```bash
# Always works after S3 implementation:
.venv/bin/python -c "from demo.adapters.saved_output import load_manifest; print('import ok')"

# Only works after V2.S2 export:
.venv/bin/python -c "from demo.adapters.saved_output import load_manifest; print(load_manifest('outputs/demo_samples/manifest.json').safety_text)"
```
And mark the second as "requires artifact bundle from V2.S2."

---

## Small issues

**`.gitignore` already covers `outputs/demo_samples/`** — The pattern `outputs/*`
in `.gitignore` will silently ignore the generated demo bundle. This is the right
default. But it means if you later choose the "commit screenshots to README" path,
you'll need to explicitly whitelist those files (e.g. `!docs/screenshots/*.png`).
Worth knowing before V2.S6.

**V2.S1 `Allowed implementation files` field is absent** — Every other session has
an explicit "Allowed implementation files" section. V2.S1 says "Documentation only"
in the subtask intro, which is correct, but the field is missing from the session
header. Add `Allowed implementation files: docs/v2_demo/curated-samples.md,
root handoff.md` to match the pattern.

**`demo/README.md` vs `docs/v2_demo/README-demo.md`** — Architecture.md section 4
shows `demo/README.md` as an optional file; V2.S6 mentions `docs/v2_demo/README-demo.md
or equivalent`. Two locations, no decision. The root README with a V2 demo section
(already planned in V2.S6) is sufficient. Remove the `demo/README.md` entry from
the architecture layout to avoid the ambiguity.

**No target dates for critical-path sessions** — Given the June 9 OPT deadline, the
plan is feasible (S1–S6 total: 17–26 hours, roughly 3–4 focused sessions). But
there are no target dates on any session. Adding a target week per session would make
it easy to check at a glance whether the demo will be ready before the deadline.
Suggested allocation:
  - S1 + S2: week of May 5
  - S3 + S4: week of May 12
  - S5 + S6: week of May 19
That leaves three weeks of buffer before June 9.

---

## Summary

The plan has improved substantially. The architecture is solid, the session
granularity is right, and the critical path is well-defined.

Three things to fix before running V2.S2:

1. **Add `contour_hc_mm` computation to V2.S2 subtasks** — it doesn't exist in any
   v1 saved output; the exporter must compute it from the cleaned mask.
2. **Document the raw data prerequisite in V2.S2** — the exporter silently needs
   `data/raw/HC18/` present; make that explicit.
3. **Remove the Markdown-parsing path from the exporter** — use `--sample-id` args
   or a companion JSON file instead.

Everything else is polish.
