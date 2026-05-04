# Handoff

This file preserves current v2 demo session context for Codex agents. The
archived v1 history is under `docs/v1/handoff.md`.

Newest entry stays at the top.

## Current Status

- V1 course pipeline is complete and frozen except for bug fixes or explicit
  packaging/report updates.
- V1 governance and history live under `docs/v1/`.
- V2 demo work is on branch `v2-demo`.
- Root `AGENTS.md` is the active v2 operating contract.
- V2 planning docs live under `docs/v2_demo/`.
- V2 session-level task plan lives at `docs/v2_demo/project-tasks.md`.
- The v2 MVP direction is now a saved-output Vite + React + TypeScript pipeline
  explorer ported from the Claude Design handoff, with live checkpoint inference
  as a later backend/adapter-backed milestone.
- The previous Streamlit prototype under `demo/` is superseded for the
  portfolio MVP but remains available as local reference code.
- Existing v1 prediction artifacts already include per-sample raw masks,
  cleaned masks, overlays, prediction CSVs, and evaluation CSVs under
  `outputs/runs/<run_id>/predictions/` and `outputs/runs/<run_id>/evaluation/`.
- The React app now lives under `frontend/`, with `outputs/demo_samples/` as the
  generated source bundle and `frontend/public/samples/` as the committed public
  runtime mirror for the curated Path A deployment.
- V2.S5 is implemented: the React app now has the full saved-output explorer
  with geometry comparison, selected-case metrics, real run cards/sparklines,
  model ablation, and post-processing ablation sections.
- V2.S6 static deployment and portfolio polish are complete for the current
  milestone: the public production URL is live at
  `https://fetal-head-measurement.vercel.app/`, and the root README now leads
  with the v2 portfolio demo rather than the archived course framing.
- Path A is now implemented locally: the frontend prefers
  `/samples/manifest.json` on every host, the public curated HC18-derived bundle
  is approved for static deployment, and `frontend/public/demo-samples/`
  remains as a committed fallback preview bundle.
- `docs/v2_demo/public-deployment-checklist.md` now captures the exact shared
  deployment state for the real curated static bundle plus the fallback preview
  path.
- Live inference planning now lives at
  `docs/v2_demo/live-inference-plan.md`; Claude Code review has been integrated
  into the roadmap/task docs before V2.S7 implementation.
- V2.S7.1 is implemented: `src/inference/live.py` provides the reusable
  curated-sample live inference core, with in-memory assets and frontend
  `Sample`-compatible output. FastAPI and React live mode remain next.
- `docs/v2_demo/production-and-visualization-roadmap.md` has been revised to
  reflect stronger HC18 licensing evidence from Zenodo/HC18 sources: public
  curated artifacts now look feasible with attribution, while checkpoint
  publication remains a separate decision.
- After a second cross-review of the updated roadmap, architecture, and
  session plan, the roadmap now also records remaining cross-document blind
  spots: live API contract drift risk, hosted curated-bundle requirements,
  Path A source-of-truth rules, placeholder fallback retention, and the
  mismatch between the documented `V2.S7.1` attention-hook scope and the
  current `src/inference/live.py` implementation.

## Latest Session

Date: 2026-05-03

Task id:
V2 Path A public static deployment

Branch:
`v2-demo`

Goal:
Implement Path A so the public static site uses the real curated HC18-derived
saved-output bundle instead of placeholder-first routing, and update the repo
docs so they all tell the same story before live inference work begins.

Files changed:

- `.gitignore`
- `README.md`
- `frontend/src/data/samples.ts`
- `frontend/src/App.tsx`
- `docs/v2_demo/DECISIONS.md`
- `docs/v2_demo/architecture.md`
- `docs/v2_demo/project-spec.md`
- `docs/v2_demo/project-tasks.md`
- `docs/v2_demo/public-deployment-checklist.md`
- `docs/v2_demo/roadmap.md`
- root `project-tasks.md`
- `handoff.md`

Commands run:

- `git status --short --branch`
- `sed -n '1,240p' .gitignore`
- `sed -n '1,220p' frontend/src/data/samples.ts`
- `find frontend/public -maxdepth 3 -type f | sort`
- `find outputs/demo_samples -maxdepth 3 -type f | sort | sed -n '1,120p'`
- `sed -n '1,280p' frontend/src/App.tsx`
- `rg -n "placeholder|demo-samples|public preview|preview bundle|local real|samples/|artifact policy|Vercel" README.md docs/v2_demo/*.md project-tasks.md handoff.md`
- `npm run build` (in `frontend/`)
- `git diff --check`

Verification result:

- Frontend production build passed.
- The loader now prefers `/samples/manifest.json` on every host and still
  falls back to `/demo-samples/manifest.json` if the curated bundle is absent.
- The real curated bundle under `frontend/public/samples/` is now visible to
  git after the ignore-rule change.
- `git diff --check` passed.

Decisions made:

- Approve Path A for the static public site: publish the curated derivative
  bundle, but keep raw HC18 files and checkpoints private.
- Keep `frontend/public/demo-samples/` as a committed fallback preview bundle.
- Treat `outputs/demo_samples/` as the generated source of truth and
  `frontend/public/samples/` as the public/runtime mirror.

Open issues:

- The real curated sample files under `frontend/public/samples/` are now
  untracked and need to be committed/pushed before Vercel can serve them.
- Live inference planning is ready to resume at `V2.S7.2 - FastAPI Demo Server`
  after the Path A branch state is committed.

Next exact task:

- Commit/push the Path A branch state including `frontend/public/samples/`, then
  let Vercel redeploy and verify the live site is serving the real curated
  bundle before starting `V2.S7.2`.

## Previous Session

Date: 2026-05-03

Task id:
V2 roadmap cross-document blind-spot review

Branch:
`v2-demo`

Goal:
Review the user-updated production roadmap against the updated architecture and
session-task docs, identify remaining blind spots, and record those findings
back into the roadmap for another Claude Code review.

Files changed:

- `docs/v2_demo/production-and-visualization-roadmap.md`
- `handoff.md`

Commands run:

- `sed -n '1,260p' docs/v2_demo/production-and-visualization-roadmap.md`
- `sed -n '1,260p' docs/v2_demo/architecture.md`
- `sed -n '1,320p' docs/v2_demo/project-tasks.md`
- `rg -n "samples.ts|preferredManifestPath|demo-samples|thresholdCurve|public artifacts|Colab|ngrok|S7\\.2|S7\\.3|S7\\.4|public checkpoint|assetOverrides|Vercel" docs/v2_demo/architecture.md docs/v2_demo/project-tasks.md docs/v2_demo/production-and-visualization-roadmap.md`
- `sed -n '260,520p' docs/v2_demo/architecture.md`
- `sed -n '558,760p' docs/v2_demo/project-tasks.md`
- `sed -n '620,920p' docs/v2_demo/production-and-visualization-roadmap.md`
- `sed -n '1,240p' frontend/src/data/samples.ts`
- `sed -n '1,260p' src/models/attention_unet.py`
- `sed -n '1,520p' src/inference/live.py`
- `git diff --check`

Verification result:

- Confirmed the roadmap's `preferredManifestPath()` discussion matches the
  actual `frontend/src/data/samples.ts` code.
- Confirmed `AttentionGate.attention` can be hooked without changing model
  weights, but also confirmed `src/inference/live.py` does not currently export
  attention maps despite the updated task plan implying that work is done.
- `git diff --check` passed.

Decisions made:

- Keep the new findings in the roadmap rather than silently editing
  `architecture.md` or `project-tasks.md` mid-review.
- Treat the live API contract, hosted curated-bundle contract, and Path A
  source-of-truth rule as explicit planning gaps to resolve before more
  implementation.

Open issues:

- `docs/v2_demo/architecture.md` and `docs/v2_demo/project-tasks.md` still
  contain user-authored edits that should be reviewed alongside the updated
  roadmap before we change implementation scope.
- The `V2.S7.1` done state in `project-tasks.md` is currently broader than the
  code that actually exists.

Next exact task:

- User reviews the updated
  `docs/v2_demo/production-and-visualization-roadmap.md` with Claude Code, then
  decides whether to refine the planning docs further or start the next
  approved implementation task.

## Previous Session

Date: 2026-05-03

Task id:
V2 roadmap licensing/policy clarification

Branch:
`v2-demo`

Goal:
Update the production/visualization roadmap so the user can re-review it with
Claude Code after the HC18 licensing/source check.

Files changed:

- `docs/v2_demo/production-and-visualization-roadmap.md`
- `handoff.md`

Commands run:

- `sed -n '1,220p' AGENTS.md`
- `sed -n '1,260p' project-tasks.md`
- `sed -n '1,260p' handoff.md`
- `sed -n '1,260p' docs/v2_demo/DECISIONS.md`
- `rg --files docs/v2_demo`
- `sed -n '1,320p' docs/v2_demo/project-tasks.md`
- `sed -n '1,320p' docs/v2_demo/project-spec.md`
- `sed -n '1,760p' docs/v2_demo/production-and-visualization-roadmap.md`
- `git diff --check`

Verification result:

- `production-and-visualization-roadmap.md` now separates artifact-publication
  policy from checkpoint-publication policy.
- The roadmap now reflects the stronger CC BY 4.0 evidence from the HC18 Zenodo
  record and Zenodo reuse guidance.
- `git diff --check` passed.

Decisions made:

- Do not record a repo-wide policy flip yet; this session only updates the plan
  and evidence framing.
- Treat public curated artifacts as likely feasible with attribution, while
  keeping public checkpoint publication as a separate decision gate.

Open issues:

- The user still needs to decide whether to approve Path A and publish the real
  curated artifact bundle on the public site.
- If Path A is approved, follow-up docs will need explicit attribution and scope
  notes.

Next exact task:

- User reviews `docs/v2_demo/production-and-visualization-roadmap.md` with
  Claude Code, then decides whether to approve Path A or continue with local-only
  real artifacts.

## Previous Session

Date: 2026-05-03

Task id:
V2 README and static deployment polish close-out

Branch:
`v2-demo`

Goal:
Finish the short static-polish pass by rewriting the root README around the v2
portfolio demo and updating the v2 planning docs to mark the static deployment
milestone complete.

Files changed:

- `README.md`
- `docs/v2_demo/project-spec.md`
- `docs/v2_demo/public-deployment-checklist.md`
- `docs/v2_demo/roadmap.md`
- `docs/v2_demo/project-tasks.md`
- root `project-tasks.md`
- `handoff.md`

Commands run:

- `sed -n '1,260p' README.md`
- `sed -n '1,260p' docs/v2_demo/project-spec.md`
- `sed -n '1,260p' docs/v2_demo/roadmap.md`
- `sed -n '1,260p' docs/v2_demo/project-tasks.md`
- `rg -n "V2\\.S6|V2\\.P5|portfolio|README" docs/v2_demo/project-tasks.md docs/v2_demo/roadmap.md project-tasks.md handoff.md`
- `cd frontend && npm run build`
- `git diff --check`

Verification result:

- Root README now presents the repository as a v2 portfolio/demo project.
- The frontend still builds successfully after doc/readme polish.
- `git diff --check` passed.
- `V2.P5` and `V2.S6` docs now reflect the current completed static milestone.

Decisions made:

- Treat the v1 training/report material as archived background context in
  `docs/v1/`, not as the primary README story.
- Mark the static deployment/readme milestone complete and keep screenshots/GIFs
  as optional future presentation assets.

Open issues:

- Optional screenshots/GIFs could still improve the public repo page later.
- The next real implementation step is still `V2.S7.2 - FastAPI Demo Server`.

Next exact task:

- Push the README/doc polish commit, then begin `V2.S7.2 - FastAPI Demo Server`
  unless the user asks for another portfolio-only pass.

## Previous Session

Date: 2026-05-03

Task id:
Static production deployment confirmation

Branch:
`v2-demo`

Goal:
Confirm that the Vercel production domain is publicly accessible and update the
v2 docs so static deployment status matches reality.

Files changed:

- `README.md`
- `docs/v2_demo/public-deployment-checklist.md`
- `docs/v2_demo/roadmap.md`
- `docs/v2_demo/project-tasks.md`
- root `project-tasks.md`
- `handoff.md`

Commands run:

- `curl -I https://fetal-head-measurement.vercel.app/`
- `curl -I https://fetal-head-measurement.vercel.app/favicon.svg`
- `git status --short --branch`
- `sed -n '1,260p' docs/v2_demo/public-deployment-checklist.md`

Verification result:

- The production domain `https://fetal-head-measurement.vercel.app/` returned
  `HTTP/2 200`.
- The deployed favicon returned `HTTP/2 200`.
- This confirms the static public deployment is now live and publicly reachable.

Decisions made:

- Treat the production domain as the real portfolio/public link, not the
  protected preview URLs.
- Move `V2.P5` / `V2.S6` from blocked to in-progress because deployment is no
  longer blocked; only polish remains.

Open issues:

- README/media polish for the public site is still optional follow-up work.
- The committed deployment checklist update should be pushed so the repo reflects
  the live production state.

Next exact task:

- Push the production-domain doc updates, then either finish any optional S6
  polish or move to `V2.S7.2 - FastAPI Demo Server`.

## Previous Session

Date: 2026-05-03

Task id:
Vercel preview manifest fallback and canvas warning cleanup

Branch:
`v2-demo`

Goal:
Remove the expected-but-misleading production `/samples/manifest.json` 404 from
the public Vercel preview and quiet the Canvas 2D readback warning in the
threshold viewer.

Files changed:

- `frontend/src/data/samples.ts`
- `frontend/src/components/threshold/ThresholdViewer.tsx`
- `frontend/src/App.tsx`
- `handoff.md`

Commands run:

- `sed -n '1,240p' frontend/src/data/samples.ts`
- `sed -n '1,320p' frontend/src/components/threshold/ThresholdViewer.tsx`
- `sed -n '1,240p' frontend/src/App.tsx`
- `rg -n "getImageData|/samples/manifest.json|/demo-samples/manifest.json" frontend -g '*.*'`
- `cd frontend && npm run build`
- `git diff --check`

Verification result:

- Frontend production build passed.
- `git diff --check` passed.
- Confirmed the loader now prefers `/demo-samples/manifest.json` on deployed
  non-local hosts, while localhost still prefers `/samples/manifest.json`.
- Confirmed canvas contexts used for repeated `getImageData` calls now request
  `{ willReadFrequently: true }`.

Decisions made:

- Keep the dual-manifest fallback, but reverse the preference by hostname so
  deployed previews stop generating a harmless 404 before loading the real
  public-preview content.
- Treat the `checkSupportDomain` message as external to the app bundle unless a
  concrete repo-owned source is identified.

Open issues:

- The Vercel preview must redeploy from the latest branch commit before the
  browser console reflects these fixes.
- Deployment protection/public-access policy still needs a final decision.

Next exact task:

- Push the preview cleanup commit and verify the redeployed Vercel console no
  longer shows the manifest-path 404 or the canvas readback warning.

## Previous Session

Date: 2026-05-03

Task id:
Vercel preview URL review and favicon follow-up

Branch:
`v2-demo`

Goal:
Record the first public Vercel preview URL, explain the reported browser
resource errors, and remove the missing favicon request from the deployed app.

Files changed:

- `frontend/index.html`
- `frontend/public/favicon.svg`
- `README.md`
- `docs/v2_demo/public-deployment-checklist.md`
- `handoff.md`

Commands run:

- `curl -I https://fetal-head-measurement-mgv1fgahc-shreyas-projects-843f684c.vercel.app/`
- `curl -I https://fetal-head-measurement-mgv1fgahc-shreyas-projects-843f684c.vercel.app/favicon.ico`
- `sed -n '1,200p' frontend/index.html`
- `find frontend/public -maxdepth 2 -type f | sort`

Verification result:

- Confirmed the deployed page currently returns Vercel auth-protected responses
  to unauthenticated `curl`, which means browser-only Vercel access policy is
  in effect.
- Confirmed the app had no favicon declared, so `/favicon.ico` 404s were
  expected from the browser.
- Added a linked SVG favicon so the next deployment should stop the missing
  favicon request in normal browser loads.

Decisions made:

- Record the current Vercel preview URL in repo docs now that it exists.
- Treat the `favicon.ico` error as an app polish issue and the
  `2filler...checkSupportDomain` console message as external/non-app unless it
  reproduces from the app bundle itself.

Open issues:

- The favicon fix still needs a fresh Vercel deployment to appear publicly.
- The deployed site appears to be behind Vercel authentication for non-browser
  requests; decide whether to keep that or make the preview fully public.

Next exact task:

- Redeploy the updated branch to Vercel, then verify the favicon request is gone
  and decide whether Vercel deployment protection should remain enabled.

## Previous Session

Date: 2026-05-03

Task id:
Push current progress and add public deployment runbook

Branch:
`v2-demo`

Goal:
Push the current safe v2 progress to GitHub and document the exact shared steps
required to get the first public deployment URL.

Files changed:

- `docs/v2_demo/public-deployment-checklist.md`
- `handoff.md`

Commands run:

- `git status --short --branch`
- `git remote -v`
- `rg -n ... .gitignore`
- `find frontend/public -maxdepth 3 -type f | sort`
- `find frontend/src/components/experiments frontend/src/components/geometry frontend/src/components/metrics -maxdepth 2 -type f | sort`
- `find docs/v2_demo -maxdepth 1 -type f | sort`

Verification result:

- Confirmed the repo points to `origin https://github.com/Endlesscrazz/Fetal-Head-Measurement.git`
- Confirmed `frontend/public/samples/` remains gitignored while safe public
  preview assets under `frontend/public/demo-samples/` are available to commit
- Wrote a shared deployment checklist that records the exact Vercel settings and
  the account-linked steps only the user can complete

Decisions made:

- Keep the first public deployment runbook Vercel-first because the repo already
  contains `vercel.json` and a static public-preview fallback
- Continue treating the real HC18-derived sample bundle as local-only until the
  user explicitly approves a different artifact policy

Open issues:

- The actual public URL still depends on the user's Vercel or GitHub Pages
  account flow
- This session should end with a GitHub push of the current safe repo state

Next exact task:

- Push the current branch snapshot to GitHub, then wait for the user's Vercel
  import URL or deployment choice

## Previous Session

Date: 2026-05-03

Task id:
`V2.S7.1` - Live Inference Core

Branch:
`v2-demo`

Goal:
Extract the single-sample checkpoint inference transform into reusable Python
code that can support the future FastAPI live demo without disturbing static
saved-output replay.

Files changed:

- `src/inference/live.py`
- `scripts/export_demo_artifacts.py`
- `tests/test_live_inference_contract.py`
- `docs/v2_demo/DECISIONS.md`
- `docs/v2_demo/project-tasks.md`
- `docs/v2_demo/roadmap.md`
- root `project-tasks.md`
- `handoff.md`

Commands run:

- `sed -n ... AGENTS.md project-tasks.md handoff.md docs/v2_demo/* docs/v1/*`
- `sed -n ... scripts/export_demo_artifacts.py src/inference/predict.py src/utils/geometry.py src/data/dataset.py`
- `rg -n ... src tests docs/v2_demo`
- `.venv/bin/python -m pytest tests/test_live_inference_contract.py`
- `.venv/bin/python scripts/export_demo_artifacts.py --run-id attention_unet_local_baseline --split test --sample-id 296_HC --sample-id 793_HC --output-dir outputs/demo_samples_live_check`
- `.venv/bin/python -m pytest tests/test_demo_manifest.py tests/test_live_inference_contract.py`
- `.venv/bin/python -m py_compile src/inference/live.py scripts/export_demo_artifacts.py tests/test_live_inference_contract.py`
- `.venv/bin/python -m pytest`
- `cd frontend && npm run build`
- `git diff --check`

Verification result:

- `tests/test_live_inference_contract.py` passed, including a synthetic contract
  test and a local curated `296_HC` checkpoint smoke test when artifacts are
  present.
- `tests/test_demo_manifest.py` plus live inference contract tests passed
  together: 5 passed.
- Exporter smoke with one strong and one failure sample passed and produced a
  schema-version-2 bundle under ignored `outputs/demo_samples_live_check/`.
- Python compile checks passed for the changed Python files.
- Full Python test suite passed: 29 passed.
- Frontend production build passed with no TypeScript errors.
- `git diff --check` passed.

Decisions made:

- The live core returns a frontend `Sample`-compatible dict plus in-memory asset
  arrays. The future API layer will map assets to file URLs or data URLs.
- Keep static saved-output replay unchanged. The exporter now reuses shared live
  helpers for dataset loading, curated sample handling, image normalization, and
  probability-map conversion while continuing to copy the saved cleaned masks and
  real evaluation metrics.

Open issues:

- `V2.S7.2` still needs `demo_live/` FastAPI endpoints, startup model loading,
  CORS, request validation, and result caching.
- React live mode and asset override helpers are not implemented yet.
- Public deployment from `V2.S6` remains blocked on external account connection.

Next exact task:

- Start `V2.S7.2 - FastAPI Demo Server`, unless the user wants to pause for a
  commit or resolve the public deployment blocker first.

## Previous Session

Date: 2026-05-03

Task id:
`V2.S6` - Build, Deploy, And Portfolio Polish

Branch:
`v2-demo`

Goal:
Prepare the React demo for portfolio use, local reviewer startup, and public
static hosting without committing or deploying the real HC18 sample image bundle.

Files changed:

- `README.md`
- `start_demo.sh`
- `vercel.json`
- `frontend/src/types/sample.ts`
- `frontend/src/data/samples.ts`
- `frontend/src/components/hero/Hero.tsx`
- `frontend/src/components/gallery/SampleGallery.tsx`
- `frontend/src/components/pipeline/StageDetail.tsx`
- `frontend/src/components/threshold/ThresholdViewer.tsx`
- `frontend/src/components/geometry/ContourEllipse.tsx`
- `frontend/public/demo-samples/manifest.json`
- `frontend/public/demo-samples/public-preview/*.svg`
- `docs/v2_demo/DECISIONS.md`
- `docs/v2_demo/architecture.md`
- `docs/v2_demo/project-tasks.md`
- `docs/v2_demo/roadmap.md`
- root `project-tasks.md`
- `handoff.md`

Commands run:

- `sed -n ... AGENTS.md project-tasks.md handoff.md docs/v2_demo/* docs/v1/* README.md frontend/src/*`
- `git remote -v`
- `mkdir -p frontend/public/demo-samples/public-preview`
- `chmod +x start_demo.sh`
- `cd frontend && npm run build`
- `bash -n start_demo.sh`
- `node -e ...` to validate `frontend/public/demo-samples/manifest.json`
- `node -e ...` to validate `vercel.json`
- `curl -I http://127.0.0.1:5173/demo-samples/manifest.json`
- `curl -I http://127.0.0.1:5173/demo-samples/public-preview/prob.svg`
- `git status --short --ignored frontend/public`
- `git diff --check`

Verification result:

- `npm run build` passed with no TypeScript errors.
- `start_demo.sh` passed shell syntax validation and is executable.
- Public preview manifest validates with schema version 2 and three preview
  samples.
- Existing Vite dev server returned `200 OK` for the preview manifest and SVG
  probability asset.
- `git diff --check` passed.
- `frontend/public/samples/` remains ignored; it should not be committed.

Decisions made:

- Public static hosting will use non-medical placeholder preview assets by
  default when `/samples/manifest.json` is absent.
- Real HC18-derived demo artifacts remain local under ignored
  `frontend/public/samples/`, populated by `./start_demo.sh`.
- Use Vercel config for the static frontend, with public URL entry deferred
  until the user's deployment account is connected.

Open issues:

- No public URL was created in this session because Vercel/GitHub Pages setup
  requires external account connection and likely a commit/push.
- README has deployment instructions but no final live URL yet.
- Full browser visual regression testing is still manual; no Playwright suite exists.

Next exact task:

- Connect the branch to Vercel or GitHub Pages and record the public URL, or
  explicitly move to `V2.S7.1 - Live Inference Core` while deployment remains
  blocked.

## Previous Session

Date: 2026-05-02

Task id:
`V2.S5` - Geometry Panel, Metrics, And Experiment Dashboard

Branch:
`v2-demo`

Goal:
Complete the remaining React saved-output sections using real v1 data:
contour-vs-ellipse geometry, per-sample metrics, and the experiment dashboard.

Files changed:

- `frontend/src/App.tsx`
- `frontend/src/styles.css`
- `frontend/src/components/geometry/ContourEllipse.tsx`
- `frontend/src/components/metrics/MetricsPanel.tsx`
- `frontend/src/components/experiments/ExperimentDashboard.tsx`
- `frontend/src/components/threshold/ThresholdViewer.tsx`
- `frontend/public/experiments/summary.json`
- `docs/v2_demo/project-tasks.md`
- `docs/v2_demo/roadmap.md`
- root `project-tasks.md`
- `handoff.md`

Commands run:

- `sed -n ... AGENTS.md project-tasks.md handoff.md docs/v2_demo/* docs/v1/* frontend/src/*`
- `sed -n ... /Users/shreyas/Downloads/design_handoff_fetal_hc_explorer/components/insight.jsx`
- `sed -n ... /Users/shreyas/Downloads/design_handoff_fetal_hc_explorer/components/experiments.jsx`
- `find outputs/runs -maxdepth 3 -name metrics.csv -o -name aggregate_metrics.csv`
- `sed -n ... outputs/runs/*/metrics.csv outputs/runs/*/evaluation/test/aggregate_metrics.csv outputs/tables/local_ablation_summary.csv outputs/tables/local_postprocess_ablation_summary.csv`
- `mkdir -p frontend/public/experiments`
- `node -e ...` to generate `frontend/public/experiments/summary.json` from real v1 CSVs
- `cd frontend && npm run build`
- `rg -n "makeCurve|synthetic|ComingNextPanel|Geometry controls are next|Human-readable metrics arrive|Experiment dashboard comes next|U-Net\\+\\+|unet_pp|m\\.hd95\\b|hd95\\b" frontend/src frontend/public/experiments docs/v2_demo/project-tasks.md`
- `curl -I http://127.0.0.1:5173/`
- `curl -I http://127.0.0.1:5173/experiments/summary.json`
- `node -e ...` to validate `summary.json` has three runs, ten epochs per run,
  and ablation/post-processing rows
- `git diff --check`
- `git status --short --branch`

Verification result:

- `npm run build` passed with no TypeScript errors.
- Existing Vite dev server returned `200 OK` for `/` and
  `/experiments/summary.json`.
- Experiment dashboard data comes from real `metrics.csv`, aggregate metrics,
  `local_ablation_summary.csv`, and `local_postprocess_ablation_summary.csv`.
- Removed the design's synthetic experiment curves and replaced the threshold
  histogram with bins computed from real `prob.png` pixel data.

Decisions made:

- Use the real cleaned prediction mask asset as the contour visual layer instead
  of inventing a fake contour path.
- Commit only static experiment metrics JSON; medical image samples remain in
  ignored `frontend/public/samples/`.

Open issues:

- Full browser interaction testing is still manual; no Playwright suite exists.
- `V2.S6` still needs README polish, deployment configuration, and portfolio
  artifact distribution decisions.
- Public sample artifact distribution remains undecided.

Next exact task:

- Start `V2.S6 - Build, Deploy, And Portfolio Polish`.

## Previous Session

Date: 2026-05-02

Task id:
Live inference plan review integration for `V2.S7`

Branch:
`v2-demo`

Goal:
Analyze the Claude-reviewed live inference plan, confirm it fits the current
React/static setup, and reconcile the roadmap, task plan, architecture, and
decision docs before implementation continues.

Files changed:

- `docs/v2_demo/live-inference-plan.md`
- `docs/v2_demo/project-tasks.md`
- `docs/v2_demo/roadmap.md`
- `docs/v2_demo/architecture.md`
- `docs/v2_demo/project-spec.md`
- `docs/v2_demo/DECISIONS.md`
- root `project-tasks.md`
- `handoff.md`

Commands run:

- `sed -n ... docs/v2_demo/live-inference-plan.md docs/v2_demo/project-tasks.md docs/v2_demo/roadmap.md docs/v2_demo/architecture.md docs/v2_demo/DECISIONS.md handoff.md project-tasks.md`
- `rg -n "V2\\.P4|Live inference|live inference|V2\\.S7|backend|FastAPI|upload|uploaded|curated" docs/v2_demo/live-inference-plan.md docs/v2_demo/project-tasks.md docs/v2_demo/roadmap.md docs/v2_demo/architecture.md docs/v2_demo/project-spec.md project-tasks.md`
- `rg -n "backend/main|backend/inference|backend/requirements|POST /predict|uploaded or selected|run model prediction on selected or uploaded|single session|Optional Live Inference FastAPI Backend|live-adapter" docs/v2_demo project-tasks.md handoff.md`
- `rg -n "live-inference-plan|V2\\.S7\\.1|V2\\.S7\\.2|V2\\.S7\\.3|V2\\.S7\\.4|curated-sample|demo_live|assetOverrides|SampleAssets|arbitrary public" docs/v2_demo/project-tasks.md docs/v2_demo/roadmap.md docs/v2_demo/architecture.md docs/v2_demo/project-spec.md docs/v2_demo/DECISIONS.md project-tasks.md handoff.md`
- `git diff --check`
- `git status --short --branch`

Verification result:

- Confirmed the live inference plan is compatible with the current app if it
  remains optional, curated-sample-first, and feeds the same React `Sample`
  contract with asset overrides.
- Updated V2.S7 from a broad single backend/upload task into four sub-sessions:
  live inference core, FastAPI demo server, React live mode, and deployment
  packaging.
- Recorded that public upload, checkpoint publishing, and curated medical-image
  hosting remain out of scope until explicitly approved.
- `git diff --check` passed.

Decisions made:

- Use `demo_live/` for the FastAPI companion server.
- Keep static saved-output replay as the default public portfolio path.
- Prefer local live mode plus demo video first; use Hugging Face Spaces only if
  publishing artifacts/checkpoints is later approved.

Open issues:

- Public distribution of checkpoint and curated medical-image artifacts is still
  undecided.
- The hosted curated-bundle input source is planned but not implemented.
- `V2.S5` remains the next implementation session before live inference work.

Next exact task:

- Continue with `V2.S5 - Geometry Panel, Metrics, And Experiment Dashboard`
  unless the user explicitly reprioritizes live inference.

## Previous Session

Date: 2026-05-02

Task id:
Live inference planning for `V2.S7`

Branch:
`v2-demo`

Goal:
Write a reviewable live inference plan covering reuse, integration with the
current React/static setup, API shape, deployment options, and free-tier hosting
tradeoffs.

Files changed:

- `docs/v2_demo/live-inference-plan.md`
- `handoff.md`

Commands run:

- `sed -n ... AGENTS.md project-tasks.md handoff.md docs/v2_demo/* docs/v1/*`
- `rg --files docs/v2_demo docs/v1`
- `rg -n "def main|predict|load_checkpoint|build_model|sigmoid|clean|ellipse|mask_contour|fit" src scripts/export_demo_artifacts.py src/inference src/utils src/data tests`
- `sed -n ... scripts/export_demo_artifacts.py src/inference/predict.py src/utils/geometry.py`
- Web review of official hosting docs for Vercel, GitHub Pages, and Hugging
  Face Spaces.

Verification result:

- Confirmed v1 code already exposes reusable model loading, dataset loading,
  probability inference, thresholding, geometry cleanup, ellipse fitting, and
  contour HC utilities.
- Confirmed current frontend can keep the existing `Sample` contract and add
  live asset overrides rather than replacing the saved-output path.
- Confirmed static hosting is suitable for Vercel/GitHub Pages, while Hugging
  Face Spaces is the best candidate for hosted live ML inference.

Decisions made:

- Keep live inference optional and post-MVP; static saved-output mode remains
  the reliable default.
- Plan curated-sample live inference before any arbitrary upload workflow.
- Prefer local live backend first, then decide whether to publish a Hugging Face
  Space after artifact/checkpoint distribution review.

Open issues:

- Claude Code still needs to review `docs/v2_demo/live-inference-plan.md`.
- Public distribution of checkpoint and curated medical-image artifacts is still
  undecided.
- `V2.S5` remains the next implementation session before live inference work.

Next exact task:

- Have Claude Code review `docs/v2_demo/live-inference-plan.md`, then continue
  with `V2.S5 - Geometry Panel, Metrics, And Experiment Dashboard` unless the
  user explicitly reprioritizes live inference.

## Previous Session

Date: 2026-05-02

Task id:
`V2.S4` - React Pipeline Explorer (Core UI)

Branch:
`v2-demo`

Goal:
Port the core Claude Design React UI to the Vite TypeScript app and wire it to
the real schema-v2 sample manifest and generated PNG assets.

Files changed:

- `frontend/src/App.tsx`
- `frontend/src/styles.css`
- `frontend/src/components/nav/StickyNav.tsx`
- `frontend/src/components/nav/TourBar.tsx`
- `frontend/src/components/hero/Hero.tsx`
- `frontend/src/components/gallery/SampleGallery.tsx`
- `frontend/src/components/pipeline/PipelineStepper.tsx`
- `frontend/src/components/pipeline/StageDetail.tsx`
- `frontend/src/components/threshold/ThresholdViewer.tsx`
- `frontend/src/components/shared/SafetyChip.tsx`
- `frontend/src/components/shared/CategoryBadge.tsx`
- `docs/v2_demo/project-tasks.md`
- `handoff.md`

Commands run:

- `git status --short --branch`
- `rg --files docs/v2_demo docs/v1 frontend/src /Users/shreyas/Downloads/design_handoff_fetal_hc_explorer`
- `sed -n ... AGENTS.md project-tasks.md handoff.md docs/v2_demo/* docs/v1/*`
- `sed -n ... /Users/shreyas/Downloads/design_handoff_fetal_hc_explorer/{app.jsx,components/nav.jsx,components/gallery.jsx,components/pipeline.jsx,components/threshold.jsx,data.js,styles.css}`
- `mkdir -p frontend/src/components/nav frontend/src/components/hero frontend/src/components/gallery frontend/src/components/pipeline frontend/src/components/threshold frontend/src/components/shared`
- `cd frontend && npm run build`
- `ps -axo pid,command`
- `curl -I http://127.0.0.1:5173/`
- `curl -I http://127.0.0.1:5173/samples/manifest.json`
- `curl -I http://127.0.0.1:5173/samples/296_HC/prob.png`
- `rg -n "letter-spacing" frontend/src`
- `rg -n "V2\\.S4|SafetyChip|ThresholdViewer|SampleGallery|PipelineStepper|StageDetail|StickyNav|TourBar" frontend/src docs/v2_demo/project-tasks.md handoff.md`
- `find frontend/src/components -maxdepth 3 -type f`
- `git diff --check`

Verification result:

- `npm run build` passed with no TypeScript errors.
- Existing Vite dev server is reachable at `http://127.0.0.1:5173/`.
- `curl -I` confirmed the app root, `/samples/manifest.json`, and
  `/samples/296_HC/prob.png` are served.
- The threshold canvas reads same-origin `prob.png` and `ultrasound.png` paths
  through the same manifest-driven sample id convention as the design.
- CSS letter spacing declarations are all normalized to `0`.
- `git diff --check` passed.

Decisions made:

- Keep V2.S4 scoped to the core explorer UI only. Geometry controls, metrics
  gauges, and the real experiment dashboard remain in `V2.S5`, with placeholder
  section anchors so sticky nav and tour flow are already in place.
- Use each sample's exported `resolution`, `spacingXMm`, and `spacingYMm`
  rather than the design prototype's hardcoded 480x360 / 0.184 mm-pixel labels.
- Keep the safety chip visible with the manifest text:
  "Educational demo only. Not for clinical use."

Open issues:

- Full visual/browser interaction testing was limited to local serving checks
  and TypeScript build; no Playwright suite exists yet.
- The current server process at port 5173 was already running from the previous
  frontend session and is still serving the app.
- V2.S5 still needs the contour-vs-ellipse panel, metric gauges, and real
  experiment dashboard.
- Public artifact distribution remains undecided for portfolio polish.

Next exact task:

- Start `V2.S5 - Geometry Panel, Metrics, And Experiment Dashboard`: port the
  remaining sections and replace design placeholders with real v1 metrics,
  contour/ellipse values, sparklines, and ablation tables.

## Previous Session

Date: 2026-05-01

Task id:
`V2.S3` - React App Scaffold And Data Layer

Branch:
`v2-demo`

Goal:
Create the Vite + React + TypeScript frontend shell, port the design/data
contract into typed frontend modules, copy the saved-output sample bundle into
the app's public directory, and verify local dev/build flow.

Files changed:

- `.gitignore`
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/index.html`
- `frontend/tsconfig.json`
- `frontend/tsconfig.app.json`
- `frontend/tsconfig.node.json`
- `frontend/vite.config.ts`
- `frontend/src/main.tsx`
- `frontend/src/App.tsx`
- `frontend/src/styles.css`
- `frontend/src/types/sample.ts`
- `frontend/src/data/samples.ts`
- `frontend/src/data/stages.ts`
- `frontend/src/data/metric-copy.ts`
- `docs/v2_demo/project-tasks.md`
- `handoff.md`

Generated local artifacts:

- `frontend/public/samples/manifest.json`
- `frontend/public/samples/<sample_id>/ultrasound.png`
- `frontend/public/samples/<sample_id>/target.png`
- `frontend/public/samples/<sample_id>/pred.png`
- `frontend/public/samples/<sample_id>/prob.png`
- `frontend/public/samples/<sample_id>/metadata.json`
- `frontend/dist/`
- `frontend/node_modules/`

Commands run:

- `node --version`
- `npm --version`
- `mkdir -p frontend/src/data frontend/src/types frontend/public/samples`
- `cp -R outputs/demo_samples/. frontend/public/samples/`
- `cd frontend && npm install`
- `cd frontend && npm run build`
- `cd frontend && npm run dev -- --host 127.0.0.1 --port 5173`
- `curl -L http://127.0.0.1:5173/samples/manifest.json`
- `curl -L http://127.0.0.1:5173/`
- `curl -I http://127.0.0.1:5173/`
- `curl -I http://127.0.0.1:5173/samples/manifest.json`
- `find frontend/public/samples -maxdepth 2 -type f | sort | head -30`
- `test -f frontend/public/samples/manifest.json && test -f frontend/public/samples/296_HC/prob.png`
- `git status --short --ignored frontend`
- `git diff --check`

Verification result:

- `npm install` completed successfully with no reported vulnerabilities.
- `npm run build` completed successfully with no TypeScript errors.
- The Vite dev server is running at `http://127.0.0.1:5173/`.
- `curl -I` confirmed the app root and `/samples/manifest.json` are served
  from the unrestricted local shell. Sandboxed curl could not connect to the
  long-running Vite process even though the server was active.
- The fetched manifest is schema version 2 and includes the six curated samples.
- `frontend/public/samples/296_HC/prob.png` exists, confirming the copied
  bundle has the React-required image set.
- `frontend/public/samples/`, `frontend/dist/`, and `frontend/node_modules/`
  are gitignored.
- `git diff --check` passed.

Decisions made:

- Scaffolded Vite files manually instead of using the generator so the resulting
  files stayed deterministic in the existing dirty worktree.
- Kept the V2.S3 app as a typed shell/data proof only; full design components
  remain scoped to `V2.S4`.
- Normalized imported design letter spacing to `0` for frontend rule
  compliance.

Open issues:

- The full core explorer UI is not implemented yet.
- Local ignored sample folders still include older Streamlit-named artifacts
  alongside the required React files; this is harmless for the frontend but can
  be cleaned in a later exporter housekeeping pass.
- Public artifact distribution remains undecided for portfolio polish.

Next exact task:

- Start `V2.S4 - React Pipeline Explorer (Core UI)`: port the core explorer
  layout, stage selector, image panels, metric tiles, and safety copy using the
  typed sample data.

## Previous Session

Date: 2026-05-01

Task id:
`V2.S2` - React Demo Artifact Export And Manifest Validation

Branch:
`v2-demo`

Goal:
Revise the saved-output demo exporter from the old Streamlit bundle contract to
the React/Vite design contract, including checkpoint-generated `prob.png` and
schema version 2 manifest fields.

Files changed:

- `scripts/export_demo_artifacts.py`
- `scripts/validate_demo_manifest.py`
- `tests/test_demo_manifest.py`
- `docs/v2_demo/project-tasks.md`
- `docs/v2_demo/roadmap.md`
- `project-tasks.md`
- `handoff.md`

Generated local artifacts:

- `outputs/demo_samples/manifest.json`
- `outputs/demo_samples/<sample_id>/ultrasound.png`
- `outputs/demo_samples/<sample_id>/target.png`
- `outputs/demo_samples/<sample_id>/pred.png`
- `outputs/demo_samples/<sample_id>/prob.png`
- `outputs/demo_samples/<sample_id>/metadata.json`

Commands run:

- `test -d data/raw/HC18/training_set && test -f outputs/runs/attention_unet_local_baseline/best_model.pt`
- `.venv/bin/python -m compileall scripts/export_demo_artifacts.py scripts/validate_demo_manifest.py`
- `.venv/bin/python -m pytest tests/test_demo_manifest.py`
- `.venv/bin/python scripts/export_demo_artifacts.py --run-id attention_unet_local_baseline --split test`
- `.venv/bin/python scripts/validate_demo_manifest.py --manifest outputs/demo_samples/manifest.json`
- `rg -n "Educational demo only. Not for clinical use.|contourHC|confidence|predEllipse|schema_version" outputs/demo_samples/manifest.json`
- `.venv/bin/python - <<'PY' ...` image-shape/probability smoke check
- `rg -n "data/raw|best_model|\\.pt|\\.ckpt" outputs/demo_samples || true`
- `.venv/bin/python -m pytest tests/test_demo_manifest.py tests/test_demo_saved_output.py`
- `git diff --check`

Verification result:

- Prerequisites were present locally: raw HC18 training data and
  `attention_unet_local_baseline/best_model.pt`.
- Exported six curated samples: `296_HC`, `217_HC`, `663_HC`, `025_HC`,
  `793_HC`, and `032_HC`.
- Manifest validation passed with `schema_version: 2`.
- Every exported React artifact has shape 256x384:
  `ultrasound.png`, `target.png`, `pred.png`, and `prob.png`.
- Manifest includes `predEllipse`, `contourHC`, `confidence`, spacing,
  resolution, real metrics, and safety text.
- Focused tests passed: 5 tests.
- `outputs/demo_samples/` contains no raw-data paths or checkpoint references.
- `outputs/demo_samples/` remains ignored by git.
- `git diff --check` passed.

Decisions made:

- Use CPU checkpoint inference inside the exporter for `prob.png` generation so
  export does not depend on sandbox-visible MPS.
- Keep paths out of the React manifest and derive frontend image paths from
  `/samples/<id>/<file>.png`.
- Leave old ignored Streamlit-named files in `outputs/demo_samples/` if already
  present; the schema-v2 validator only requires the React artifact set.

Open issues:

- No `frontend/` project exists yet.
- `frontend/public/samples/` still needs to be created and gitignored in
  `V2.S3`.
- Public artifact distribution is still undecided for portfolio polish.

Next exact task:

- Start `V2.S3 - React App Scaffold And Data Layer`: scaffold the Vite React
  TypeScript app, port design tokens, define the TypeScript `Sample` contract,
  copy `outputs/demo_samples/` into `frontend/public/samples/`, and verify
  `npm run dev` plus `npm run build`.

## Previous Session

Date: 2026-05-01

Task id:
`V2.S2` / planning reconciliation - Claude Design React pivot

Branch:
`v2-demo`

Goal:
Analyze the Claude Design handoff at
`/Users/shreyas/Downloads/design_handoff_fetal_hc_explorer/`, reconcile it with
the existing v2 plan, and update Markdown contracts before implementation
continues.

Files changed:

- `AGENTS.md`
- `project-tasks.md`
- `docs/v2_demo/DECISIONS.md`
- `docs/v2_demo/architecture.md`
- `docs/v2_demo/project-spec.md`
- `docs/v2_demo/roadmap.md`
- `docs/v2_demo/project-tasks.md`
- `docs/v2_demo/frontend-design-handoff.md`
- `docs/v2_demo/CLAUDE-CODE-V2-REVIEW.md`
- `docs/v2_demo/curated-samples.md`
- `docs/v2_demo/curated-samples.json`
- `handoff.md`

Commands run:

- `find /Users/shreyas/Downloads/design_handoff_fetal_hc_explorer -maxdepth 3 -type f | sort`
- `sed -n ...` reads across root governance, v2 docs, v1 docs, and the design
  handoff files
- `rg -n "Streamlit|React|Vite|prob.png|..." AGENTS.md project-tasks.md handoff.md docs/v2_demo`
- `rg -n "142_HC|073_HC|511_HC|..."`
  `outputs/runs/attention_unet_local_baseline/evaluation/test/per_sample_metrics.csv`
- `.venv/bin/python -m json.tool docs/v2_demo/curated-samples.json`
- `git diff --check`

Verification result:

- Confirmed the design handoff is a high-fidelity React prototype, not
  production code.
- Confirmed the design sample metrics and some sample IDs are placeholders.
- Confirmed the current curated sample set already provides a stronger real
  success/typical/failure story than the design IDs.
- `docs/v2_demo/curated-samples.json` remains valid JSON after category
  normalization.
- `git diff --check` passed.

Decisions made:

- Current MVP framework is Vite + React + TypeScript, not Streamlit.
- Existing Streamlit work is superseded reference code.
- Keep the current curated samples: `296_HC`, `217_HC`, `663_HC`, `025_HC`,
  `793_HC`, and `032_HC`.
- Normalize frontend categories to `strong`, `typical`, and `failure`; preserve
  cleanup/error nuance in labels and tags.
- Resume implementation at the React artifact-contract revision: export
  `ultrasound.png`, `target.png`, `pred.png`, and `prob.png`; produce manifest
  schema version 2.

Open issues:

- `scripts/export_demo_artifacts.py` and `scripts/validate_demo_manifest.py`
  still need to be revised to the React schema.
- No `frontend/` project exists yet.
- Generated medical-image artifacts remain local/ignored unless the user
  approves a distribution policy.

Next exact task:

- Implement `V2.S2 - Export Demo Artifacts And Validate Manifest` for the React
  contract, including checkpoint-generated `prob.png` and manifest schema
  version 2.

## Previous Session

Date: 2026-05-01

Task id:
`V2.S4` - Streamlit Import-Path Hotfix

Branch:
`v2-demo`

Goal:
Fix the local Streamlit launch error where `demo/app.py` could not import the
`demo.adapters` package when executed as a script by Streamlit.

Files changed:

- `demo/app.py`
- `handoff.md`

Commands run:

- `.venv/bin/python -m compileall demo/app.py`
- `.venv/bin/python - <<'PY' ...` Streamlit `AppTest` smoke check
- `.venv/bin/python -m pytest tests/test_demo_manifest.py tests/test_demo_saved_output.py`
- `curl -L http://localhost:8501/_stcore/health`
- `git diff --check`

Verification result:

- App entrypoint compiles.
- Streamlit `AppTest` renders without app exceptions.
- Focused demo tests still pass: 5 tests.
- Existing local Streamlit server health endpoint returns `ok`.
- `git diff --check` passed.

Decisions made:

- Add the repository root to `sys.path` at the app entrypoint before importing
  the local `demo` package so `streamlit run demo/app.py` works from localhost.

Open issues:

- `V2.S5` still needs to add the experiment dashboard and measurement story.

Next exact task:

- Refresh the local Streamlit page and then start `V2.S5 - Experiment Dashboard
  And Measurement Story` once the app launch is confirmed.

## Previous Session

Date: 2026-05-01

Task id:
`V2.S4` - Streamlit Pipeline Explorer

Branch:
`v2-demo`

Goal:
Build the first saved-output Streamlit app screen with sample selection, visible
safety language, core pipeline stage images, and concise metrics.

Files changed:

- `requirements-demo.txt`
- `demo/app.py`
- `demo/components/__init__.py`
- `demo/components/sample_selector.py`
- `demo/components/pipeline_views.py`
- `docs/v2_demo/project-tasks.md`
- `handoff.md`

Commands run:

- `sed -n '276,333p' docs/v2_demo/project-tasks.md`
- `.venv/bin/python -c "import streamlit; print(streamlit.__version__)"` before install
- `.venv/bin/python -m compileall demo`
- `.venv/bin/python -m pytest tests/test_demo_manifest.py tests/test_demo_saved_output.py`
- `UV_CACHE_DIR=.uv-cache uv pip install -r requirements-demo.txt` (failed because uv targeted an unrelated active environment and network was sandboxed)
- `.venv/bin/python -m pip install -r requirements-demo.txt` (failed because `.venv` has no pip module)
- `VIRTUAL_ENV= UV_CACHE_DIR=.uv-cache uv pip install --python .venv/bin/python -r requirements-demo.txt`
- `.venv/bin/streamlit --version`
- `.venv/bin/streamlit run demo/app.py --server.port 8501 --server.headless true`
- `curl -L http://localhost:8501`
- `.venv/bin/python - <<'PY' ...` saved-output loader smoke check
- `.venv/bin/python - <<'PY' ...` Streamlit `AppTest` smoke check
- `curl -L http://localhost:8501/_stcore/health`

Verification result:

- Streamlit 1.57.0 installed in project `.venv`.
- `compileall demo` passed.
- Focused demo tests passed: 5 tests.
- Streamlit app started successfully at `http://localhost:8501`.
- Health endpoint returned `ok`.
- Streamlit `AppTest` smoke check confirmed the title, safety warning, and two
  selectboxes render without app exceptions.
- Saved-output loader confirmed all six samples load with expected 256x384 image
  and mask arrays.
- Marked `V2.S4` as done.

Decisions made:

- Keep the first app screen focused on the actual pipeline explorer.
- Add demo dependencies in `requirements-demo.txt`, separate from v1
  `requirements.txt`.
- Use the generated saved-output bundle as the only app data source for this
  milestone.

Open issues:

- `V2.S5` still needs to add the experiment dashboard and fuller measurement
  story.
- `outputs/demo_samples/` remains generated and ignored.
- `context-bridge-log.md` and `context-bridge-state.db` are untracked and were
  not changed.

Next exact task:

- Start `V2.S5 - Experiment Dashboard And Measurement Story`: add result-table
  loading, training/validation loss curves, post-processing comparison, and a
  clearer contour-vs-ellipse panel while keeping saved-output mode raw-data-free.

## Previous Session

Date: 2026-05-01

Task id:
`V2.S3` - Saved-Output Data Layer

Branch:
`v2-demo`

Goal:
Build the app-facing saved-output adapter and `DemoSample` contract without
Streamlit-specific code.

Files changed:

- `demo/__init__.py`
- `demo/adapters/__init__.py`
- `demo/adapters/saved_output.py`
- `demo/types.py`
- `tests/test_demo_saved_output.py`
- `docs/v2_demo/project-tasks.md`
- `handoff.md`

Commands run:

- `sed -n '223,276p' docs/v2_demo/project-tasks.md`
- `sed -n '1,220p' outputs/demo_samples/manifest.json`
- `sed -n '1,220p' outputs/demo_samples/025_HC/metadata.json`
- `.venv/bin/python -m pytest tests/test_demo_saved_output.py`
- `.venv/bin/python -m compileall demo`
- `.venv/bin/python -c "from demo.adapters.saved_output import load_manifest; print('import ok')"`
- `.venv/bin/python -c "from demo.adapters.saved_output import load_manifest; print(load_manifest('outputs/demo_samples/manifest.json').safety_text)"`
- `.venv/bin/python - <<'PY' ...` to load the real manifest and `025_HC`
- `rg -n "streamlit|torch" demo tests/test_demo_saved_output.py`
- `.venv/bin/python -m pytest tests/test_demo_manifest.py tests/test_demo_saved_output.py`

Verification result:

- `tests/test_demo_saved_output.py` passed: 3 tests.
- Combined demo tests passed: 5 tests.
- `compileall demo` passed.
- Import smoke check printed `import ok`.
- Artifact-bundle smoke check printed the required safety text.
- Real manifest loads six sample ids.
- Real sample `025_HC` loads with image/mask shape 256x384, overlay shape
  256x384x3, category `cleanup_ellipse`, and non-null `contour_hc_mm`.
- `rg -n "streamlit|torch" demo tests/test_demo_saved_output.py` found no
  matches, confirming the saved-output layer does not import Streamlit or
  PyTorch.
- Marked `V2.S3` as done.

Decisions made:

- Load masks as binary `uint8` arrays with values 0/1.
- Load ellipse overlays as RGB `uint8` arrays for future Streamlit rendering.
- Keep `DemoManifest` separate from `DemoSample` so UI code can list samples
  without loading every image.

Open issues:

- Streamlit UI is not implemented yet.
- `outputs/demo_samples/` remains a generated ignored local artifact bundle.
- `context-bridge-log.md` and `context-bridge-state.db` are untracked and were
  not changed.

Next exact task:

- Start `V2.S4 - Streamlit Pipeline Explorer`: add `requirements-demo.txt`,
  `demo/app.py`, `demo/components/sample_selector.py`, and
  `demo/components/pipeline_views.py`; render sample selection and the original,
  target, raw prediction, cleaned mask, and ellipse overlay views with visible
  safety language.

## Previous Session

Date: 2026-05-01

Task id:
`V2.S2` - Export Demo Artifacts And Validate Manifest

Branch:
`v2-demo`

Goal:
Create a raw-data-free saved-output artifact bundle for the Streamlit MVP and
validate the manifest.

Files changed:

- `scripts/export_demo_artifacts.py`
- `scripts/validate_demo_manifest.py`
- `tests/test_demo_manifest.py`
- `outputs/demo_samples/manifest.json` (generated and ignored)
- `outputs/demo_samples/<sample_id>/...` (generated and ignored)
- `docs/v2_demo/project-tasks.md`
- `docs/v2_demo/roadmap.md`
- `project-tasks.md`
- `handoff.md`

Commands run:

- `test -d data/raw/HC18/training_set`
- `.venv/bin/python -m pytest tests/test_demo_manifest.py`
- `.venv/bin/python -m compileall scripts/export_demo_artifacts.py scripts/validate_demo_manifest.py`
- `.venv/bin/python -m json.tool docs/v2_demo/curated-samples.json`
- `.venv/bin/python scripts/export_demo_artifacts.py --run-id attention_unet_local_baseline --split test`
- `.venv/bin/python scripts/validate_demo_manifest.py --manifest outputs/demo_samples/manifest.json`
- `rg -n "Educational demo only. Not for clinical use." outputs/demo_samples/manifest.json`
- `rg -n "contour_hc_mm" outputs/demo_samples/*/metadata.json`
- `find outputs/demo_samples -maxdepth 2 -type f | sort`
- `rg -n "data/raw|best_model|\\.pt|\\.ckpt" outputs/demo_samples || true`
- `.venv/bin/python - <<'PY' ...` to confirm exported image/mask/overlay shapes
- `git status --short --ignored outputs/demo_samples data/raw .venv .uv-cache`

Verification result:

- Manifest validation passed.
- `tests/test_demo_manifest.py` passed: 2 tests.
- Exported six curated samples: `296_HC`, `217_HC`, `663_HC`, `025_HC`,
  `793_HC`, and `032_HC`.
- Each sample has `image.png`, `target_mask.png`, `raw_mask.png`,
  `cleaned_mask.png`, `ellipse_overlay.png`, and `metadata.json`.
- Each exported image/mask is aligned at 256x384; overlays are 256x384x3.
- Each metadata file includes non-null `contour_hc_mm`.
- `outputs/demo_samples/` contains no `data/raw`, checkpoint, `.pt`, or `.ckpt`
  references.
- `outputs/demo_samples/` remains ignored by git, as intended.
- Marked `V2.S2` and roadmap/root `V2.P2.5` as done.

Decisions made:

- Exported model-space/preprocessed grayscale images at 256x384 so image,
  target mask, prediction masks, and overlays align in the saved-output app.
- Kept generated demo medical-image assets under ignored `outputs/demo_samples/`.

Open issues:

- `outputs/demo_samples/` is generated locally and ignored; future portfolio
  polish still needs to choose the public artifact distribution strategy.
- Streamlit data loading is not implemented yet.
- `context-bridge-log.md` and `context-bridge-state.db` are untracked and were
  not changed.

Next exact task:

- Start `V2.S3 - Saved-Output Data Layer`: add `demo/types.py`,
  `demo/adapters/saved_output.py`, and tests that load
  `outputs/demo_samples/manifest.json` into the `DemoSample` contract without
  importing Streamlit or PyTorch.

## Previous Session

Date: 2026-05-01

Task id:
`V2.S1` - Curate Demo Sample Set

Branch:
`v2-demo`

Goal:
Choose the saved-output demo sample set and write both human-readable rationale
and machine-readable exporter input.

Files changed:

- `docs/v2_demo/curated-samples.md`
- `docs/v2_demo/curated-samples.json`
- `docs/v2_demo/project-tasks.md`
- `docs/v2_demo/roadmap.md`
- `project-tasks.md`
- `handoff.md`

Commands run:

- `sed -n '75,138p' docs/v2_demo/project-tasks.md`
- `sed -n '1,260p' docs/v2_demo/architecture.md`
- `head -5 outputs/runs/attention_unet_local_baseline/evaluation/test/per_sample_metrics.csv`
- `head -5 outputs/runs/attention_unet_local_baseline/predictions/test/predictions.csv`
- `.venv/bin/python - <<'PY' ...` to rank best, median, high-error, and low-Dice candidates
- `.venv/bin/python - <<'PY' ...` to inspect post-processing variants for candidate samples
- `.venv/bin/python -m json.tool docs/v2_demo/curated-samples.json`
- `rg -n "strong|typical|high-error|cleanup|ellipse|failure" docs/v2_demo/curated-samples.md`
- `.venv/bin/python - <<'PY' ...` to verify selected prediction rows, raw masks, cleaned masks, and overlays
- `test -f docs/v2_demo/curated-samples.md && test -f docs/v2_demo/curated-samples.json`

Verification result:

- Curated six samples from `attention_unet_local_baseline` internal test:
  `296_HC`, `217_HC`, `663_HC`, `025_HC`, `793_HC`, and `032_HC`.
- JSON is valid.
- Markdown rationale includes strong, typical, cleanup/ellipse, high-error, and
  failure categories.
- Each selected sample has a prediction row, metrics row, raw mask, cleaned
  mask, and overlay path present under the v1 output tree.
- Marked `V2.S1` and roadmap/root `V2.P2` as done.

Decisions made:

- Use six curated samples rather than the minimum five to cover both a large-HC
  high-error case and a low-Dice small-HC failure case.
- Keep `docs/v2_demo/curated-samples.md` human-readable and
  `docs/v2_demo/curated-samples.json` machine-readable.

Open issues:

- `V2.S2` still needs to export original images, target masks, copied masks,
  overlays, per-sample metadata, and `outputs/demo_samples/manifest.json`.
- `V2.S2` must compute `contour_hc_mm` from cleaned masks.
- `V2.S2` requires local `data/raw/HC18/training_set/` for export only.
- `outputs/demo_samples/` has not been generated yet.
- `context-bridge-log.md` and `context-bridge-state.db` are untracked and were
  not changed.

Next exact task:

- Start `V2.S2 - Export Demo Artifacts And Validate Manifest`: implement
  `scripts/export_demo_artifacts.py` and `scripts/validate_demo_manifest.py`,
  export the six curated samples, compute `contour_hc_mm`, and validate
  `outputs/demo_samples/manifest.json`.

## Previous Session

Date: 2026-05-01

Task id:
V2 Round 2 plan review incorporation

Branch:
`v2-demo`

Goal:
Analyze the updated Claude Code review and tighten v2 planning docs before
implementation starts.

Files changed:

- `docs/v2_demo/project-tasks.md`
- `docs/v2_demo/architecture.md`
- `docs/v2_demo/project-spec.md`
- `docs/v2_demo/roadmap.md`
- `docs/v2_demo/DECISIONS.md`
- `project-tasks.md`
- `handoff.md`

Commands run:

- `git status --short --branch`
- `sed -n ... AGENTS.md project-tasks.md handoff.md docs/v2_demo/* docs/v1/*`
- `rg -n "contour|circumference|ellipse|clean" src/utils/geometry.py src/evaluation src/inference scripts/postprocess_ablation.py`
- `sed -n '1,260p' src/utils/geometry.py`
- `head -5 outputs/runs/attention_unet_local_baseline/predictions/test/predictions.csv`
- `head -5 outputs/runs/attention_unet_local_baseline/evaluation/test/per_sample_metrics.csv`

Verification result:

- Confirmed v1 prediction/evaluation CSVs do not contain `contour_hc_mm`.
- Confirmed `src/utils/geometry.py` exposes `mask_contour_length_mm`.
- Updated v2 session tasks so V2.S2 computes contour HC from cleaned masks.
- Documented that V2.S2 requires local `data/raw/HC18/training_set/` for export
  only; saved-output app runtime remains raw-data-free.
- Replaced Markdown parsing with machine-readable
  `docs/v2_demo/curated-samples.json`.

Decisions made:

- `curated-samples.md` is human rationale only.
- `curated-samples.json` is the exporter input, with repeated `--sample-id`
  arguments allowed for one-off tests.
- `contour_hc_mm` should be computed during artifact export and stored in
  per-sample metadata, not recomputed in the Streamlit UI.

Open issues:

- `docs/v2_demo/curated-samples.md` and `docs/v2_demo/curated-samples.json` do
  not exist yet.
- No implementation has started yet.
- `outputs/demo_samples/` has not been generated yet.
- `context-bridge-log.md` and `context-bridge-state.db` are untracked and were
  not changed.

Next exact task:

- Start `V2.S1 - Curate Demo Sample Set`: inspect internal-test metrics, choose
  at least five samples, and write both `docs/v2_demo/curated-samples.md` and
  `docs/v2_demo/curated-samples.json`.

## Previous Session

Date: 2026-05-01

Task id:
V2 session task planning

Branch:
`v2-demo`

Goal:
Divide the v2 roadmap into implementation sessions with outcomes, subtasks,
expected files, verification, and done criteria before starting code work.

Files changed:

- `docs/v2_demo/project-tasks.md`
- `docs/v2_demo/roadmap.md`
- `project-tasks.md`
- `handoff.md`

Commands run:

- `sed -n ... AGENTS.md project-tasks.md handoff.md docs/v2_demo/*`
- `test -f docs/v2_demo/project-tasks.md`
- `rg -n "V2.S1|V2.S2|V2.S6|V2.S7|V2.S8" docs/v2_demo/project-tasks.md`
- `git diff --check`

Verification result:

- Added `docs/v2_demo/project-tasks.md` with sessions `V2.S0` through `V2.S8`.
- Confirmed the critical path is `V2.S1` through `V2.S6` for the saved-output
  MVP and portfolio polish.
- Confirmed post-MVP live inference and challenge export are separated as
  optional sessions.

Decisions made:

- Use `docs/v2_demo/project-tasks.md` as the detailed v2 execution queue.
- Keep root `project-tasks.md` as the repository-wide index.

Open issues:

- No implementation has started yet.
- Next session still needs to curate samples before artifact export.

Next exact task:

- Start `V2.S1 - Curate Demo Sample Set`: inspect internal-test metrics,
  choose at least five samples, and write `docs/v2_demo/curated-samples.md`.

## Previous Session

Date: 2026-05-01

Task id:
V2 plan review and documentation hardening

Branch:
`v2-demo`

Goal:
Review the v2 demo plan and Claude Code review, identify implementation
blockers, and update planning docs so the next implementation task has a clear
artifact/export/UI contract.

Files changed:

- `README.md`
- `project-tasks.md`
- `handoff.md`
- `docs/v2_demo/architecture.md`
- `docs/v2_demo/project-spec.md`
- `docs/v2_demo/roadmap.md`
- `docs/v2_demo/DECISIONS.md`
- `report/submission-checklist.md`

Commands run:

- `rg --files`
- `git status --short --branch`
- `sed -n ... AGENTS.md project-tasks.md docs/v2_demo/* docs/v1/* README.md`
- `find outputs -maxdepth ...`
- `head -5 outputs/runs/attention_unet_local_baseline/evaluation/test/per_sample_metrics.csv`
- `head -5 outputs/runs/attention_unet_local_baseline/predictions/test/predictions.csv`

Verification result:

- Confirmed v2 docs exist and Claude review has been incorporated.
- Confirmed root `handoff.md` was missing in the working tree and recreated as
  the active v2 handoff.
- Confirmed existing v1 artifacts are useful but not sufficient for raw-data-free
  demo runtime because image and target-mask exports still need to be bundled.

Decisions made:

- Use `demo/app.py` as the Streamlit entrypoint.
- Use `demo/components/` for reusable panels and `demo/adapters/` for sample
  loading/inference adapters.
- Use `outputs/demo_samples/manifest.json` as the saved-output app input.
- Add `V2.P2.5` before Streamlit work to export and validate the demo bundle.
- Keep generated demo medical-image artifacts local until the user explicitly
  approves a public distribution policy.

Open issues:

- `scripts/export_demo_artifacts.py` and `scripts/validate_demo_manifest.py` do
  not exist yet.
- `outputs/demo_samples/` has not been generated yet.
- Demo dependencies are not defined yet; use `requirements-demo.txt` during
  `V2.P3`.
- Public demo artifact distribution still needs a final choice during portfolio
  polish.
- `context-bridge-log.md` and `context-bridge-state.db` are untracked and were
  not changed.

Next exact task:

- Implement `V2.P2.5`: create `scripts/export_demo_artifacts.py` and
  `scripts/validate_demo_manifest.py`, export at least five curated samples from
  `attention_unet_local_baseline` internal-test outputs, and validate
  `outputs/demo_samples/manifest.json`.
