# AGENTS.md - Codex Operating Contract for Fetal HC18

This file is the source of truth for Codex agents working on this project.
The project goal is to complete a reproducible course submission for automatic
fetal head circumference estimation from 2D ultrasound images using HC18.

## 1. V1 mission

Build a script-first PyTorch pipeline that:

1. loads HC18 ultrasound images and annotations,
2. generates deterministic ellipse-derived segmentation targets,
3. trains a U-Net baseline,
4. trains Attention U-Net as the main improved model,
5. converts predicted masks into ellipse fits,
6. reports fetal head circumference in millimeters,
7. generates quantitative metrics, tables, figures, and course-ready outputs.

The v1 project thesis:

> Use deep segmentation on HC18, convert predictions to ellipse-based geometry,
> and measure fetal head circumference accurately enough to analyze what modeling
> choices matter most.

## 2. Required files to read at session start

Every Codex session must read these files before making changes:

1. `AGENTS.md`
2. `project-tasks.md`
3. `handoff.md`
4. `DECISIONS.md`
5. Relevant files under `docs/`

If a task conflicts with these instructions, the newest explicit user request
wins, but the conflict must be recorded in `handoff.md` and, if non-trivial, in
`DECISIONS.md`.

## 3. Scope locks

V1 is intentionally narrow.

- Use PyTorch.
- Use scripts and config files as the primary workflow.
- Use `Myproject.sh` as the final course runner unless the user explicitly
  changes the deliverable.
- Do not create notebooks as the primary implementation path.
- Do not build a web demo in v1.
- Implement U-Net before any improved model.
- Use Attention U-Net as the main improved model.
- Treat ResUNet as fallback or stretch only.
- Avoid transformer-heavy models, semi-supervised pipelines, deployment work,
  web APIs, and broad hyperparameter sweeps until v1 is complete.

## 4. Compute policy

- Local MacBook M1 Air: development, unit tests, data inspection, and tiny
  subset smoke runs.
- University CHPC Slurm GPU nodes: full training, final ablations, and reported
  results.
- Google Colab is not part of the v1 execution plan.

All training code must work from scripts and configs so the same commands can
run locally and on CHPC.

## 4.1 Environment policy

- Use `uv` for the project environment.
- The local environment path is `.venv/`.
- Use a project-local cache when needed: `UV_CACHE_DIR=.uv-cache uv ...`.
- Run project commands through `.venv/bin/python` unless a future task adds uv
  project metadata for `uv run`.
- Do not install packages into system Python for this project.

## 5. Agent discipline

Agents must implement exactly one approved session/task from `project-tasks.md`
at a time unless the user explicitly expands scope. The phase/session roadmap in
`project-tasks.md` controls implementation order.

Before editing, agents must state:

- the task id,
- the phase/session id when available,
- the expected files to change,
- the intended verification command or check.

Agents must not:

- make unrelated refactors,
- change task scope silently,
- add new dependencies without recording the decision,
- hard-code local-only paths,
- mix split generation into training code,
- change tensor contracts between models,
- couple model code to dataset parsing,
- compare experiments trained on different splits unless clearly labeled.

## 6. Build order

Follow this order unless the user explicitly changes it:

1. create repo structure and environment files,
2. inspect HC18 dataset format,
3. parse annotations and pixel spacing,
4. generate deterministic masks,
5. create visual overlay checks,
6. create train/val/internal-test splits,
7. implement U-Net,
8. implement training loop,
9. train first baseline run,
10. implement inference geometry,
11. evaluate segmentation and HC error,
12. implement Attention U-Net,
13. rerun on the same split,
14. run focused ablations,
15. generate report tables and figures,
16. package `README.md`, `Myproject.sh`, and final outputs.

## 7. Required handoff

After meaningful work, update `handoff.md` with:

- date,
- session goal,
- task id,
- files changed,
- commands run,
- verification result,
- decisions made,
- open issues,
- next exact task.

Keep `handoff.md` concise but specific enough that the next Codex session can
continue without guessing.

## 8. Decision log requirements

Update `DECISIONS.md` whenever a non-trivial decision is made about:

- architecture,
- data parsing or target generation,
- training policy,
- evaluation metrics,
- compute environment,
- dependencies,
- reproducibility,
- report scope.

Each decision entry must include:

- date,
- decision,
- rationale,
- alternatives considered,
- impact on future work.

Use append-only entries unless correcting an explicit error.

## 9. Experiment rules

Every real experiment must have:

- config,
- seed,
- split id,
- run id,
- checkpoint,
- metrics file,
- short description.

Recommended v1 experiment story:

1. U-Net + filled ellipse mask + BCE/Dice,
2. U-Net + alternate loss,
3. U-Net + stronger augmentation,
4. Attention U-Net + same split/config family,
5. post-processing ablation: raw mask vs cleanup + ellipse fit.

Do not run many architectures at the expense of completing the report.

## 10. Data and geometry guardrails

- Never resize images without updating annotation geometry or regenerating masks
  in the resized coordinate system.
- Keep raw data under `data/raw/` untouched.
- Keep split files under `data/splits/` and do not regenerate silently.
- Dataloader outputs must include image, mask, spacing, sample id, and annotation
  metadata when available.
- Geometry code must be deterministic and separate from neural inference.
- Ellipse fitting failure cases must be handled explicitly.

## 11. Completion definition

V1 is complete when:

- dataset loading works,
- generated masks are visually verified,
- one U-Net baseline trains successfully,
- Attention U-Net trains on the same split,
- inference returns HC in mm,
- evaluation includes segmentation and HC metrics,
- report-ready tables and figures exist,
- `Myproject.sh` reproduces the main pipeline,
- `README.md` explains exactly how to run locally and on CHPC.
