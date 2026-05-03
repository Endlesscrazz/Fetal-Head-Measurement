# Public Deployment Checklist

Date: 2026-05-03

Purpose:
This is the shared runbook for getting the v2 React demo to a public URL
without publishing the real HC18 sample bundle.

Current public preview URL:
`https://fetal-head-measurement-mgv1fgahc-shreyas-projects-843f684c.vercel.app/`

Recommended path:
Use Vercel for the static frontend. The current app already includes a safe
public fallback preview under `frontend/public/demo-samples/`, so we can deploy
the UI now without uploading the real medical-image artifacts.

## 1. What Is Already Ready In The Repo

- `frontend/` builds successfully with `npm run build`
- `vercel.json` exists at the repo root
- `README.md` documents the public-preview mode and local real-artifact mode
- the app falls back to `/demo-samples/manifest.json` when
  `/samples/manifest.json` is absent
- `frontend/public/samples/` is ignored, so the real HC18-derived bundle stays
  local

## 2. What I Need From You

These are the only things that require your account or approval:

1. Access to the GitHub repo from the Vercel account you want to use
2. A choice on deployment target:
   `Vercel preview from v2-demo` is recommended first
3. If you want a custom domain, the domain name and DNS access
4. The final deployed URL after Vercel creates it, if you complete the import
   flow in the browser

## 3. Recommended Deployment Mode

Use this first:

- branch: `v2-demo`
- host: Vercel
- public content: placeholder preview only
- real HC18 sample bundle: local only

Why this is the safest path:

- no medical-image bundle is committed
- no checkpoint is published
- the portfolio UI becomes reviewable immediately
- we can later decide whether `main` or `v2-demo` should become the production
  branch

## 4. Shared Step-By-Step Checklist

### Step 1 - Push the latest branch state

Owner:
Codex

Status:
Ready now

Outcome:
`origin/v2-demo` contains the latest React demo, public preview assets, live
inference core work, and deployment docs.

### Step 2 - Import the repo into Vercel

Owner:
You

What to do:

1. Open Vercel Dashboard
2. Click `Add New...` -> `Project`
3. Import `Endlesscrazz/Fetal-Head-Measurement`
4. If Vercel asks for repo access, approve it for this repository

What I need back from you:

- confirmation that the repo import succeeded
- the generated Vercel project URL or deployment URL

### Step 3 - Use these exact Vercel settings

Owner:
You

Project settings:

- Framework Preset: `Other`
- Root Directory: `.`
- Install Command: `npm --prefix frontend install`
- Build Command: `npm --prefix frontend run build`
- Output Directory: `frontend/dist`

Environment variables:

- none required for the static public-preview deployment

Branch recommendation:

- first deploy `v2-demo`

### Step 4 - Verify the first public deploy

Owner:
Shared

Status:
Initial Vercel preview URL exists

What to check:

1. The homepage loads
2. The sample gallery renders from the placeholder preview manifest
3. No request is made for local-only `frontend/public/samples/` assets
4. The safety disclaimer is visible

What I can do after you send the URL:

- verify the deployment behavior
- update `README.md`, `handoff.md`, and any v2 docs with the real public URL
- note any follow-up fixes if the deployed build differs from local

### Step 5 - Optional custom domain

Owner:
You

Only needed if you want a polished branded URL now.

If yes, I need:

- the domain/subdomain you want to use
- confirmation that you can update DNS records

If no, we can keep the default `*.vercel.app` URL for now.

## 5. If You Prefer GitHub Pages Instead

This is possible, but it is not the recommended first path because the repo is
already set up for Vercel.

If you want GitHub Pages, I would still need from you:

- confirmation that Pages is your preferred host
- whether you want deployment from `main`, `v2-demo`, or a GitHub Actions build

Then I can add the workflow and base-path adjustments before we deploy.

## 6. What Happens After You Send Me The URL

I will:

1. update the docs with the real public URL
2. verify the deployed preview matches the intended public-safe behavior
3. note any remaining deployment polish work

## 7. Current Blocking Item

Current blocker:
The repository code is ready, but the first public URL still depends on your
Vercel or GitHub Pages account connection in the browser.
