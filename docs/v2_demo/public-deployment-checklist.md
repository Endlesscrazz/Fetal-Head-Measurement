# Public Deployment Checklist

Date: 2026-05-03

Purpose:
This is the shared runbook for getting the v2 React demo to a public URL
and keeping the public deployment state documented.

Current public production URL:
`https://fetal-head-measurement.vercel.app/`

Current status note:
The project now has a public production domain. Preview/deployment URLs may
still be protected, but they are no longer the main portfolio link.

Recommended path:
Use Vercel for the static frontend. The current public production deployment now
serves the curated real HC18-derived saved-output bundle from
`frontend/public/samples/`, while retaining `frontend/public/demo-samples/` as a
fallback preview bundle.

## 1. What Is Already Ready In The Repo

- `frontend/` builds successfully with `npm run build`
- `vercel.json` exists at the repo root
- `README.md` documents the public static real-artifact mode and local
  regeneration flow
- the app falls back to `/demo-samples/manifest.json` when
  `/samples/manifest.json` is absent
- `frontend/public/samples/` contains the committed curated public bundle

## 2. What I Need From You

These are the only things that require your account or approval:

1. Access to the GitHub repo from the Vercel account you want to use
2. A choice on deployment target:
   `Vercel preview from v2-demo` is recommended first
3. If you want a custom domain, the domain name and DNS access
4. The final deployed URL after Vercel creates it, if you complete the import
   flow in the browser

## 3. Current Deployment Mode

Current production mode:

- branch: `v2-demo`
- host: Vercel
- public content: curated real HC18-derived saved-output bundle
- fallback content: committed preview bundle under `frontend/public/demo-samples/`

Why this is the current recommended static setup:

- the live website shows the real end-to-end saved-output walkthrough
- raw HC18 data and checkpoints are still not published
- the preview bundle remains available if `samples/` is absent on another host

## 4. Shared Step-By-Step Checklist

### Step 1 - Push the latest branch state

Owner:
Codex

Status:
Ready now

Outcome:
`origin/v2-demo` contains the latest React demo, the curated public artifact
bundle, the fallback preview bundle, live inference core work, and deployment
docs.

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

- none required for the static public curated deployment

Branch recommendation:

- first deploy `v2-demo`

### Step 4 - Verify the public deploy

Owner:
Shared

Status:
Production domain is live

What to check:

1. The homepage loads
2. The active-case UI renders from the real curated `samples/manifest.json`
3. `ultrasound.png`, `target.png`, `pred.png`, and `prob.png` load from
   `/samples/<id>/...`
4. The safety disclaimer is visible

What I can do after you send the URL:

- verify the deployment behavior
- update `README.md`, `handoff.md`, and any v2 docs with the real public URL
- note any follow-up fixes if the deployed build differs from local

### Step 5 - Make the site publicly accessible

Owner:
You

Status:
Done

Why this step matters:

- the current `*-git-v2-demo-*.vercel.app` and random deployment URLs are still
  returning protected responses
- on Vercel Hobby, preview/deployment URLs can remain protected while the
  production domain is the public one

What to do in Vercel:

1. Open the project in Vercel
2. Go to `Settings` -> `Git`
3. Set `Production Branch` to `v2-demo` if you want this branch to power the
   public resume link
4. Trigger a new production deployment from `v2-demo`
5. Open the production domain shown in `Domains`

What I need back from you:

- the production-domain URL Vercel shows after that deploy
- confirmation that the page opens in a logged-out browser window

If you prefer not to make `v2-demo` the production branch:

- keep `main` as production
- later merge `v2-demo` into `main`
- then use the resulting production domain as the public link

### Step 6 - Optional custom domain

Owner:
You

Only needed if you want a polished branded URL now.

If yes, I need:

- the domain/subdomain you want to use
- confirmation that you can update DNS records

If no, we can keep the default `*.vercel.app` URL for now.

## 5. Deployment Protection Note

According to Vercel's Deployment Protection docs, preview/deployment URLs can
be protected while the production domain remains public on Hobby plans. If the
site still asks for Vercel access after a production deployment, check
`Settings` -> `Deployment Protection` and confirm you did not enable a stricter
scope such as `All Deployments`.

## 6. If You Prefer GitHub Pages Instead

This is possible, but it is not the recommended first path because the repo is
already set up for Vercel.

If you want GitHub Pages, I would still need from you:

- confirmation that Pages is your preferred host
- whether you want deployment from `main`, `v2-demo`, or a GitHub Actions build

Then I can add the workflow and base-path adjustments before we deploy.

## 7. What Happens After You Send Me The URL

I will:

1. update the docs with the real public URL
2. verify the deployed preview matches the intended public-safe behavior
3. note any remaining deployment polish work

## 8. Current State

Current status:
Static public deployment is complete and now uses the curated real artifact
bundle. Remaining work is optional presentation polish and then live inference.
