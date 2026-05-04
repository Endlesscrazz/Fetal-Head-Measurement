# V2 Frontend Design Handoff

Source: `/Users/shreyas/Downloads/fetal-head-claude-designs/design_handoff_fetal_hc_v2/`
Reviewed: 2026-05-04

This document is the implementation reference for porting the v2 redesign into the
existing Vite + React + TypeScript codebase. Read it alongside `architecture.md`
and `live-inference-plan.md` before writing any code.

The v1 handoff (`frontend-design-handoff.md`) is superseded by this document for all
UI work. Data contract decisions from v1 still apply unless overridden in Section 5.

---

## 1. What changed and why

The v2 redesign is not a theme update — it restructures the page and replaces or
removes several components. The motivations are:

| Area | v1 (current live) | v2 (this handoff) |
|---|---|---|
| Player position | Below the gallery; users had to scroll to the main interaction | **Hero IS the player** — above the fold, visible without scrolling |
| Stage transitions | Whole stage cards swap; layout jumps on transition | **Stable media stage** — single fixed-aspect frame, overlay layers fade in/out |
| Case switching | Auto-jumped to CNN stage; story started mid-pipeline | Pins to **stage 01 Input** on every case switch |
| Probability viz | Full-frame yellow/amber flood; visually noisy | **Iso-probability contour lines** at 0.30/0.50/0.75/0.92 + focus reticle |
| Case gallery | Separate full-width section with card grid | **Compact picker** (6 thumbnail buttons, 50px tall) inside the hero title row |
| Geometry layout | Morph slider appears/disappears → card height reflows | Slider in a **reserved slot** (visibility:hidden when unused) — no reflow |
| Geometry story | Raw numbers, no context | **Dual story**: this-sample panel + dataset stripe chart |
| Experiment dashboard | Full section with run cards, sparklines, ablation tables | **Removed.** Replaced by a 3-card `MethodSection` (architecture, training, geometry prior) |
| Live mode | No affordance anywhere in the UI | Transport rail has **mode prop + status pill + timing chip** — drop-in live ready |
| Tour mode | `TourBar` + `tourActive` state + tour copy | **Removed** |
| Section count | 6+ sections (Gallery, Pipeline, Threshold, Geometry, Metrics, Experiments) | **5 sections**: Play, Threshold, Geometry, Metrics, Method |

### What stays the same

- Dark lab-notebook palette, Instrument Serif + Inter + JetBrains Mono
- Cyan (`#6ee0ff`) primary, amber (`#ffb454`) secondary
- Six pipeline stages: Input → Target → CNN → Mask → Ellipse → HC
- Persistent "Educational demo · Not for clinical use" safety chip
- Sticky sub-nav with scrollspy
- Same overall product identity and technical tone

---

## 2. Source files

| Design file | Role |
|---|---|
| `README.md` | Authoritative prose spec — layout, interactions, design rationale, responsive |
| `styles.css` | v1 base tokens (unchanged) |
| `styles-v2.css` | v2 additions: `.stage`, `.transport`, `.caption`, `.geom-controls`, `.insight`, `.focus-reticle` |
| `data.js` | Sample data + STAGES + METRIC_COPY |
| `app-v2.jsx` | `AppV2`, `HeroPlayer`, `SubNav`, `ThresholdSection`, `MetricsSection`, `MethodSection`, `ArcCard`, `BarCard`, `CategoryBadge`, `CasePickerCompact`, `StageCaption`, `ProbThresholdLayer` |
| `components-v2/transport.jsx` | `Transport`, `MediaStage`, `Outline`, `ProbabilityViz`, `EllipseLayer` |
| `components-v2/geometry.jsx` | `GeometryV2`, `ContourPath` |
| `screenshots/` | Layout and overlay treatment truth (not pixel-precise — see README spec for values) |

**Do not drop these files into the production app.** They use Babel-in-browser and
inline styles. Port them to the existing Vite + TypeScript build, translating each
component to a `.tsx` file.

---

## 3. Component mapping

### Components to replace

| v1 production file | v2 replacement | Action |
|---|---|---|
| `components/nav/StickyNav.tsx` | `SubNav` (app-v2.jsx) | Replace — SubNav adds mode toggle |
| `components/nav/TourBar.tsx` | _(removed)_ | Delete — tour mode is gone |
| `components/hero/Hero.tsx` | `HeroPlayer` (app-v2.jsx) | Replace — hero now owns the player |
| `components/gallery/SampleGallery.tsx` | `CasePickerCompact` (app-v2.jsx) | Replace — compact picker inside hero |
| `components/pipeline/PipelineStepper.tsx` | `Transport` (transport.jsx) | Replace — transport rail |
| `components/pipeline/StageDetail.tsx` | `StageCaption` (app-v2.jsx) | Replace — lives inside HeroPlayer |
| `components/threshold/ThresholdViewer.tsx` | `ThresholdSection` + `ProbThresholdLayer` (app-v2.jsx) | Refactor — section wrapper changes; pixel logic is same |
| `components/geometry/ContourEllipse.tsx` | `GeometryV2` (geometry.jsx) | Replace — stable height, dataset stripe added |
| `components/metrics/MetricsPanel.tsx` | `MetricsSection` + `ArcCard` + `BarCard` (app-v2.jsx) | Replace — layout unchanged, 2×2 grid |
| `components/experiments/ExperimentDashboard.tsx` | `MethodSection` (app-v2.jsx) | Replace — full removal of run cards/sparklines |
| `components/shared/SafetyChip.tsx` | _(unchanged)_ | Keep exactly as-is |
| `components/shared/CategoryBadge.tsx` | `CategoryBadge` (app-v2.jsx) | Keep shape — v2 has updated variant map |

### New components to create

| Production path | Source in design | Notes |
|---|---|---|
| `components/stage/MediaStage.tsx` | `transport.jsx MediaStage` | The stable frame — central primitive |
| `components/stage/Outline.tsx` | `transport.jsx Outline` | Canvas-based mask-to-outline renderer |
| `components/stage/ProbabilityViz.tsx` | `transport.jsx ProbabilityViz` | Iso-contour canvas + focus reticle |
| `components/stage/EllipseLayer.tsx` | `transport.jsx EllipseLayer` | SVG ellipse + HC ribbon |
| `components/transport/Transport.tsx` | `transport.jsx Transport` | Transport rail (play/pause, tick rail, status) |
| `components/geometry/ContourPath.tsx` | `geometry.jsx ContourPath` | Wobbly SVG contour path |
| `components/method/MethodSection.tsx` | `app-v2.jsx MethodSection` | 3-card architecture/training/geometry narrative |

### Existing files that remain

- `frontend/src/data/samples.ts` — unchanged (manifest loading, sampleAssetPath)
- `frontend/src/types/sample.ts` — unchanged (Sample interface; see Section 5 for one addition)
- `frontend/src/utils/assets.ts` — unchanged (getSampleAssets helper)
- `frontend/src/data/stages.ts` — unchanged (STAGES array matches design data.js)
- `frontend/src/data/metric-copy.ts` — unchanged (METRIC_COPY matches design data.js)
- `frontend/public/samples/` and `frontend/public/demo-samples/` — unchanged

---

## 4. File structure (target)

```
frontend/src/
  components/
    nav/
      SubNav.tsx               ← replaces StickyNav + TourBar
    hero/
      HeroPlayer.tsx           ← header section: title + picker + MediaStage + StageCaption + Transport
      CasePickerCompact.tsx    ← 6-button thumbnail picker
      StageCaption.tsx         ← right column stable-height card
    stage/
      MediaStage.tsx           ← stable frame: img + overlay layers
      Outline.tsx              ← canvas: mask → edge outline
      ProbabilityViz.tsx       ← canvas: iso-contour + focus reticle
      EllipseLayer.tsx         ← SVG: ellipse + axes + HC ribbon
    transport/
      Transport.tsx            ← play rail: buttons + tick rail + status pill
    threshold/
      ThresholdSection.tsx     ← section wrapper + slider controls
      ProbThresholdLayer.tsx   ← canvas: live threshold re-render
    geometry/
      GeometryV2.tsx           ← section: modes, single-sample panel, dataset stripe
      ContourPath.tsx          ← SVG: wobbly contour path
    metrics/
      MetricsSection.tsx       ← 2×2 grid wrapper
      ArcCard.tsx              ← Dice / IoU gauge
      BarCard.tsx              ← HC error / HD95 bar
    method/
      MethodSection.tsx        ← 3-card architecture narrative
    shared/
      SafetyChip.tsx           ← unchanged
      CategoryBadge.tsx        ← updated variant map
  data/
    stages.ts                  ← unchanged
    metric-copy.ts             ← unchanged
    samples.ts                 ← unchanged
    live-api.ts                ← live mode API client (V2.S7.3)
  types/
    sample.ts                  ← unchanged
    live.ts                    ← live mode types (V2.S7.3)
  utils/
    assets.ts                  ← unchanged (getSampleAssets)
  App.tsx                      ← updated: new state model (Section 7), 5 sections
  styles.css                   ← port v2 additions from styles-v2.css
```

---

## 5. Corrections for production — where design diverges

### 5.1 Sample IDs (CRITICAL — same issue as v1 handoff)

The v2 `data.js` uses these IDs: `296_HC`, `142_HC`, `418_HC`, `073_HC`, `511_HC`, `624_HC`.

`418_HC` and `624_HC` are not in the internal test split. All metrics in `data.js`
are design placeholders. **Do not use them in production.**

Use the real curated samples from `frontend/public/samples/manifest.json`:

| Slot | Production ID | Category | Real Dice | Real HC Error |
|---|---|---|---|---|
| 1 | `296_HC` | strong | 0.9907 | 0.03 mm |
| 2 | `217_HC` | strong | ~0.988 | ~0.19 mm |
| 3 | `663_HC` | typical | ~0.965 | ~1.6 mm |
| 4 | `025_HC` | typical | ~0.961 | ~3.3 mm |
| 5 | `793_HC` | failure | ~0.874 | ~10 mm |
| 6 | `032_HC` | failure | ~0.831 | ~19.9 mm |

All metrics come from the manifest — never from `data.js` SAMPLES.

### 5.2 ExperimentDashboard is fully removed

The v2 design replaces the experiment dashboard (run cards, sparklines, ablation
tables) with `MethodSection` — three narrative cards about architecture, training,
and the geometry prior. There is no fifth section equivalent to the old dashboard.

Implication: `ExperimentDashboard.tsx` and `frontend/public/experiments/` are no
longer referenced in v2. Keep them in the repo (do not delete) in case a later
milestone restores experiment data, but do not wire them into v2.

### 5.3 `hd95` field name

The v2 `data.js` uses `hd95`. Production uses `hd95_mm` (from v1 CSVs).

The `MetricsSection` `BarCard` for HD95 should read `sample.metrics.hd95_mm`. The
`METRIC_COPY.hd95` label and interpret function are correct — just read the right key.

### 5.4 `ellipse` vs `predEllipse`

The v2 `data.js` has both `ellipse` (ground-truth) and `predEllipse` (prediction).
Production only has `predEllipse`. All v2 components fall back:

```typescript
const e = sample.predEllipse || (sample as any).ellipse;
```

Keep this fallback; it is already present in the design JSX (`sample.predEllipse || sample.ellipse`).

### 5.5 `thresholdCurve` (new optional field — V2.S9)

The v2 design does not include a threshold-Dice curve Play button — that is a V2.S9
enhancement. The `Sample` interface already has `thresholdCurve?` optional. If
present, `ThresholdSection` can use it for a Play animation; if absent, the slider
still works identically.

### 5.6 Asset path integration

The design reads images as `samples/${sampleId}/ultrasound.png`. In production,
all image paths must go through `getSampleAssets(sample, overrides?)` from
`frontend/src/utils/assets.ts`. This is the integration point for live mode — when
live assets arrive, pass them as `overrides` to every image-consuming component.

Replace all direct string interpolations with `getSampleAssets(sample, assetOverrides)`.

---

## 6. Detailed component specs

### 6.1 `SubNav.tsx`

Replace `StickyNav.tsx`. Remove `TourBar` and all tour state.

```
Position: sticky top 0, z-index 40
Background: rgba(7,9,15,0.78) + backdrop-filter blur(14px)
Border-bottom: 1px solid var(--line)
Outward bleed: marginLeft/Right -36px, paddingLeft/Right 36px (so blur reaches viewport edge)
Height: ~42px content + 20px vertical padding = ~62px total
```

Three clusters:

**Left — brand:**
- Small SVG ellipse glyph (see app-v2.jsx)
- `"HC EXPLORER"` mono 10.5px, `--fg-2`, letter-spacing `0.14em`, uppercase

**Center — section pills:**
- Five sections: `01 PLAY`, `02 THRESHOLD`, `03 GEOMETRY`, `04 METRICS`, `05 METHOD`
- Container: `display:flex; gap:2px; padding:3px; background:var(--bg-2); border:1px solid var(--line); border-radius:999px`
- Each pill: `padding:6px 12px; font-family:var(--mono); font-size:10.5px; letter-spacing:0.1em; uppercase`
- Active: `background:var(--bg-4); color:var(--fg-0);` — number turns `var(--cyan)`
- Inactive: `background:transparent; color:var(--fg-2);`

**Right — mode toggle (live mode hook):**
- Same `.status-pill` style as transport
- Click toggles `mode` between `'replay'` and `'live'`
- `'replay'` → green LED + `"Saved · v1"`
- `'live'` → cyan LED + `"Live · preview"` (preview note until backend is wired)

Scrollspy: `IntersectionObserver rootMargin:'-20% 0px -60% 0px'`. On each section's
entry, set `activeSection` to that section's id.

### 6.2 `HeroPlayer.tsx`

The hero section is the most important component. It contains the player and must be
visible without scrolling on 1440×900 desktop.

Internal layout:
```
HeroPlayer
  ├── Title row (flex, space-between)
  │   ├── Left: eyebrow + H1 + subtitle
  │   └── Right: CasePickerCompact
  └── Media row (grid, 1.55fr : 1fr, gap 22px)
      ├── Left: MediaStage
      └── Right: StageCaption
  └── Transport (marginTop 14px)
```

**Title row:**
- Eyebrow: ellipse SVG glyph + `"Fetal HC · Pipeline Explorer · v0.5"` mono 11px `--fg-3` uppercase letter-spacing `0.14em`
- H1: `Instrument Serif`, `46px`, `lineHeight:1.06`, `letterSpacing:'-0.02em'`
  - Three lines: `"From a noisy ultrasound / to a number in millimetres, / step by step."`
  - Third line `"step by step."` in `var(--cyan)`
- Subtitle: `14.5px`, `--fg-1`, `maxWidth:560px`, `lineHeight:1.55`
  - Copy: `"Press play to watch a CNN measure the head circumference of a fetus — six visible stages, no black boxes. Pick any case to drive the pipeline."`

**Case switch effect (critical):**
```typescript
useEffect(() => {
  setStageIdx(0);
  setPlaying(false);
}, [activeId]);
```
This is the v1 bug fix. The sample switch must reset to stage 0 (Input), never auto-jump.

**Auto-advance:**
```typescript
useEffect(() => {
  if (!playing) return;
  const t = setInterval(() => {
    setStageIdx(i => {
      if (i >= STAGES.length - 1) { setPlaying(false); return i; }
      return i + 1;
    });
  }, 1300);
  return () => clearInterval(t);
}, [playing]);
```

### 6.3 `CasePickerCompact.tsx`

Six thumbnail buttons replacing the full gallery section.

```
Container: display:flex; flex-direction:column; gap:6px; minWidth:280px
Caption above: "Active case · click to switch" mono 10px --fg-3 uppercase letter-spacing 0.14em
Grid: display:grid; grid-template-columns:repeat(6,1fr); gap:4px; padding:4px;
      background:var(--bg-1); border:1px solid var(--line); border-radius:10px
```

Each button (50px tall):
- `borderRadius:6px; overflow:hidden; position:relative; cursor:pointer`
- Active: `border:1px solid var(--cyan); boxShadow:0 0 0 1px rgba(110,224,255,0.4)`
- Inactive: `opacity:0.62; filter:saturate(0.7)`
- Image: `objectFit:cover; width:100%; height:100%`
- Category dot: `position:absolute; left:4px; bottom:3px; width:5px; height:5px; borderRadius:999px`
  - Strong → `var(--good)` | Typical → `var(--cyan)` | Failure → `var(--bad)`

No label text inside the button — category and id shown in tooltip (`title` attr).

### 6.4 `MediaStage.tsx`

The central stable frame. **This must not change height or aspect ratio when stages change.**

```css
.stage {
  position: relative;
  aspect-ratio: 4/3;   /* shifts to 1/1 below 920px */
  background: #000;
  border: 1px solid var(--line);
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 1px 0 rgba(255,255,255,0.04) inset,
              0 12px 40px -16px rgba(0,0,0,0.7);
}
```

Every child is a layer:
```css
.layer {
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  transition: opacity 480ms cubic-bezier(.4,.2,.2,1);
}
.layer.fade-in  { opacity: 1; }
.layer.fade-out { opacity: 0; }
```

**Layer stack per stage (show/hide by opacity — never unmount):**

| Stage | Base brightness | Overlay layers shown |
|---|---|---|
| `input` | `none` (full) | base only |
| `target` | `brightness(0.78) contrast(1.05)` | `Outline(target.png)` |
| `prob` | `brightness(0.78) contrast(1.05)` | `ProbabilityViz` |
| `mask` | `brightness(0.78) contrast(1.05)` | `Outline(pred.png)` |
| `ellipse` | `brightness(0.78) contrast(1.05)` | `EllipseLayer` |
| `hc` | `brightness(0.78) contrast(1.05)` | `EllipseLayer` + HC ribbon |

**Persistent badges (always in DOM, always visible):**
- Top-left: glass pill with stage number + stage title. Background `rgba(7,9,15,0.78)` + `backdrop-filter:blur(8px)`.
- Top-right: glass pill with `sample.id`.
- Bottom-left: scale legend — `.scale-ticks` class (28px cyan swatch + `"10 mm"` label).

**Asset wiring:** do not hardcode paths. Receive `assets: SampleAssets` prop derived
from `getSampleAssets(sample, assetOverrides)` in the parent. Pass `assets.ultrasound`,
`assets.target`, `assets.pred`, `assets.prob` down to child overlay components.

### 6.5 `Outline.tsx`

Canvas-based mask-to-outline renderer. Re-renders when `visible` or `src` changes.

Algorithm (from transport.jsx):
1. Load `src` PNG into an offscreen canvas.
2. `getImageData` to read pixel values.
3. For each pixel where `v >= 128`: if any 4-connected neighbor is `< 128`, it is an edge pixel — write to output at full alpha.
4. Optional fill: if `fill !== 'transparent'`, flood-fill inside the mask shape using `globalCompositeOperation: 'source-in'`.
5. Apply stroke color + shadow via `ctx.shadowColor = stroke; ctx.shadowBlur = glow;`.
6. Composite with `mix-blend-mode: normal` (overlaid on darkened base).

Props: `visible: boolean; src: string; stroke: string; fill?: string; width?: number; glow?: number`.

For target mask: `stroke="#6ee0ff"`, `fill` omitted (outline only).
For pred mask: `stroke="#6ee0ff"`, `fill="rgba(110,224,255,0.10)"`.

**Render as:**
```tsx
<canvas className={`layer ${visible ? 'fade-in' : 'fade-out'}`}
        style={{ pointerEvents: 'none', objectFit: 'fill' }} />
```

### 6.6 `ProbabilityViz.tsx`

Iso-probability contour canvas. Replaces the v1 full-frame yellow wash.

**Algorithm (from transport.jsx ProbabilityViz):**
1. Load `prob.png` into canvas.
2. For each of four iso-levels `[0.30, 0.50, 0.75, 0.92]`:
   - Threshold at `L = Math.floor(level * 255)`.
   - For each pixel where `v >= L` but any 4-connected neighbor `< L` → it is a boundary pixel.
   - Write that pixel to the output at the level's RGBA color.
   - Do not overwrite a higher-alpha level (check `out.data[i+3] < a`).
3. Put image data; composite with `mix-blend-mode: screen`.

**Iso-level colors:**
| Level | RGBA |
|---|---|
| 0.30 | `rgba(255,180,84,110)` — amber soft |
| 0.50 | `rgba(110,224,255,200)` — cyan |
| 0.75 | `rgba(110,224,255,230)` — cyan bright |
| 0.92 | `rgba(255,255,255,240)` — white |

**Focus reticle:**
A `div.focus-reticle` anchored to `predEllipse` bounding box + 12px padding on each side.
Position is percentage of the stage frame:
```
left: ((ellipse.cx - ellipse.rx - 12) / VW) * 100 + '%'
top:  ((ellipse.cy - ellipse.ry - 12) / VH) * 100 + '%'
width: ((ellipse.rx * 2 + 24) / VW) * 100 + '%'
height: ((ellipse.ry * 2 + 24) / VH) * 100 + '%'
```
where `VW = 480, VH = 360` match the design coordinate space.

The focus reticle uses `::before`/`::after` pseudo-elements for cross-hair lines (see `.focus-reticle` in `styles-v2.css`).

**Iso-level legend:** pinned bottom-right inside the stage, shows four colored rows with level values.

**Important:** this component is CORS-sensitive. Images in `public/samples/` served by Vite
dev server are same-origin — `getImageData` works. In production on Vercel, verify no
restrictive headers are added. The same constraint applies to all canvas-based overlays.

### 6.7 `EllipseLayer.tsx`

SVG ellipse rendered at a fixed `viewBox="0 0 480 360"` with `preserveAspectRatio="xMidYMid slice"`.
This keeps ellipse coordinates consistent regardless of the displayed image resolution.

**Layers inside the SVG:**
1. Soft SVG ellipse: `stroke="#6ee0ff"`, `strokeWidth="1.6"`, `fill="rgba(110,224,255,0.04)"`, `filter: drop-shadow(0 0 4px ...)`
2. Major/minor axis dashes: two `<line>` elements inside a `<g transform="rotate(...)">`, `strokeDasharray="3 3"`, `opacity="0.6"`
3. HC ribbon (visible only when `showHC === true`):
   - Outer dashed ellipse: `rx + 6, ry + 6`, `strokeDasharray="2 4"`, `opacity="0.7"`, with `<animate attributeName="stroke-dashoffset" from="0" to="-12" dur="2s" repeatCount="indefinite" />`
   - Callout pill: `<rect>` + `<text>` at `cx + rx + 14`, showing `"191.44 mm"` in `JetBrains Mono 11px` cyan

**Coordinate space:** design `data.js` ellipses use 480×360 space. Production `predEllipse`
values come from `predictions.csv` and are in image pixel coordinates (256×384). These
are stored in the manifest as pixel coordinates at export resolution. The SVG viewBox
must match the coordinate space of the ellipse values — use `viewBox="0 0 384 256"`
(width × height from `sample.resolution`) for production, not the design's `480 360`.

### 6.8 `Transport.tsx`

Three-column grid rail: `auto 1fr auto`, height 64px.

```css
.transport {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 18px;
  height: 64px;
  padding: 0 16px;
  background: linear-gradient(180deg, rgba(17,23,38,0.92), rgba(12,17,27,0.88));
  border: 1px solid var(--line);
  border-radius: 14px;
  backdrop-filter: blur(10px);
}
```

**Left cluster — player controls:**
- `[restart]` ghost button (40×40 circle, restart icon SVG)
- `[prev]` ghost button (disabled + `opacity:0.35` at stage 0)
- **`[play/pause]` primary** — `background:var(--cyan); color:#07090f; boxShadow:0 0 16px -2px rgba(110,224,255,0.5)`
- `[next]` ghost button (disabled at last stage)

Button styles (`.transport-btn`):
```css
width: 40px; height: 40px;
background: var(--bg-3); border: 1px solid var(--line-2);
border-radius: 999px; cursor: pointer;
transition: background 150ms, border-color 150ms, transform 100ms;
/* hover */ background: var(--bg-4); border-color: var(--cyan); color: var(--cyan);
/* active */ transform: scale(0.96);
```

**Center — tick rail:**
- Track: `height:4px; background:var(--bg-4); border-radius:999px; overflow:hidden`
- Fill: `linear-gradient(90deg, var(--cyan-dim), var(--cyan))`, width = `(stageIdx / (total-1)) * 100%`, `transition:width 380ms`
- Six stop buttons sit above the track:
  - Default dot: `12×12px; background:var(--bg-1); border:1.5px solid var(--line-2)`
  - Passed: `background:var(--cyan-dim)`
  - Active: `background:var(--cyan); box-shadow:0 0 0 4px rgba(110,224,255,0.18), 0 0 12px rgba(110,224,255,0.6)`
  - Label below dot: stage short name, `9.5px` mono uppercase

**Right cluster — status/timing (live mode hook):**
```typescript
interface TransportProps {
  mode: 'replay' | 'live' | 'computing';
  timing?: { label: string; value: string } | null;
  // ... player callbacks
}
```

| Mode | Status pill | LED color | LED animation |
|---|---|---|---|
| `replay` | `"Saved · v1"` | `var(--good)` | static |
| `live` | `"Live"` | `var(--cyan)` | `pulse-ring 2s infinite` |
| `computing` | `"Computing"` | `var(--amber)` | `pulse-ring 1.4s infinite` |

Timing pill: `"12 ms / stage"` in replay mode. In live mode, receives actual per-stage ms.
Counter: mono `10.5px` `--fg-3`, format `"03 / 06 · CNN"`.

**Responsive:** at `< 920px`, `.right-cluster { display: none }` and grid collapses to `auto 1fr`.

### 6.9 `StageCaption.tsx`

Right column of the hero grid. **Fixed minimum height — content swaps, slot never grows.**

```css
.caption {
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 12px;
  min-height: 320px;   /* critical — never let this collapse */
  padding: 22px;
  background: var(--bg-2);
  border: 1px solid var(--line);
  border-radius: 14px;
}
```

Three rows:

1. **Header row:** Mono eyebrow `"STAGE 03 OF 06"` (10.5px, `--fg-3`, uppercase, letter-spacing `0.14em`) + H2 in Instrument Serif (26px, lineHeight 1.2).

2. **Blurb slot:** `minHeight: 96px` — prevents reflow when blurb lengths differ.
   - Primary paragraph: `14px`, `--fg-1`, `lineHeight:1.55` — `stage.blurb`
   - Follow-up: `12.5px`, `--fg-2`, `lineHeight:1.55` — `stage.detail`

3. **Fact tiles:** `display:flex; gap:10px`. Two tiles per stage.
   - Each: `flex:1; padding:12px 14px; background:var(--bg-1); border:1px solid var(--line); border-radius:10px`
   - Inside: mono uppercase label (9.5px `--fg-3`) + mono value (14px `--fg-0`)
   - Per-stage fact values (exact copy from app-v2.jsx `factsByStage`):

| Stage | Fact 1 | Fact 2 |
|---|---|---|
| input | `Source: <id>.png` | `Channels: 1 (gray)` |
| target | `Origin: Radiologist` | `Role: Ground truth` |
| prob | `Mean conf.: <confidence>%` | `Output: P(skull) per pixel` |
| mask | `Threshold: 0.50` | `Cleanup: Fill / largest CC` |
| ellipse | `Method: Least-squares` | `Reject: Non-elliptical drift` |
| hc | `Predicted HC: <predHC> mm` | `Final error: <hcErr> mm` |

### 6.10 `ThresholdSection.tsx` + `ProbThresholdLayer.tsx`

Same two-column layout as hero: `minmax(0, 1.4fr) minmax(0, 1fr)`, gap `26px`.

Left: a `.stage` frame (same CSS as MediaStage, `aspectRatio: '4/3'`).
- Base ultrasound: darkened `brightness(0.78) contrast(1.05)`
- `ProbThresholdLayer` canvas on top (screen blend mode)
- Top-left status pill: `τ = 0.50` in cyan LED pill

**`ProbThresholdLayer` canvas logic (from app-v2.jsx — identical to v1's ThresholdViewer):**
```
Load prob.png → getImageData → per-pixel:
  if v >= T (= thresh * 255):
    → cyan (110, 224, 255), alpha min(180, 80 + (v - T))   [committed mask]
  else if showProb && v > 30:
    → amber (255, 180, 84), alpha = (v/255) * 60            [sub-threshold heat]
Put image data; mixBlendMode: screen
```

This is the same algorithm as v1 `ThresholdViewer` — only the section wrapper changes.

Right column (top → bottom):
1. Eyebrow `"02 / Threshold ↦ Mask"`, H2 `"The moment the model commits."` (28px serif), paragraph
2. Slider card (`padding:14px 16px; bg:var(--bg-1); border:var(--line); border-radius:10px`):
   - Range input full-width `accentColor:var(--cyan)`
   - Three-up legend: `"0.00 · noisy"` — `"τ = 0.50"` (cyan) — `"1.00 · strict"`, mono 10px uppercase
3. Toggle: checkbox + `"Show probability heat under threshold"` (12px `--fg-2`)
4. Insight callout (`.insight`): heading `"What you're seeing"` (mono 10px cyan uppercase) + dynamic paragraph by threshold band:
   - `< 0.3` → `"Below 0.3 the mask leaks into noise..."`
   - `0.3 – 0.6` → `"Around 0.5 the model commits to its strongest beliefs..."`
   - `0.6 – 0.85` → `"Above 0.6 only the high-confidence core survives..."`
   - `≥ 0.85` → `"At 0.85+ the mask collapses to the most certain interior..."`

**Asset wiring:** `ProbThresholdLayer` must read `prob` from `getSampleAssets(sample, assetOverrides).prob`
rather than a hardcoded path, so live mode can supply a different URL.

### 6.11 `GeometryV2.tsx` + `ContourPath.tsx`

Same two-column layout, `alignItems:'start'`.

Left: `.stage` frame with SVG overlay (two paths: contour + ellipse). Opacity of each
is driven by mode state — transitions via `transition: opacity 280ms ease`.

```
Mode     → Contour opacity  Ellipse opacity
contour  → 1                0
ellipse  → 0                1
both     → 1                1
morph    → 1 - morph        morph
```

Top-left: two glass legend pills ("Cleaned contour" amber, "Fitted ellipse" cyan).
Each fades to `opacity:0.4` when its layer is at opacity 0.

`ContourPath` renders the raw (wobbly) contour as an SVG `<path>` with 90 points:
- Deterministic noise seeded LCG (seed 21, same each render for same ellipse)
- Formula: `rx + (rand() - 0.5) * 4.5`, `ry + (rand() - 0.5) * 3.8`
- Stroke `#ffb454`, `strokeWidth:1.6`, `filter: drop-shadow(0 0 3px rgba(255,180,84,0.6))`

Right column (top → bottom):

1. Eyebrow `"04 / Geometry regularization"`, H2 `"Why the mask becomes a measurement."` (28px), paragraph

2. **Mode tabs + reserved slider slot** (`.geom-controls`):
   - Grid: `grid-template-rows: auto 56px` — the 56px row is always present for the slider
   - Tab row: 4 tabs (`Contour`, `Ellipse`, `Both`, `Morph`), `gridTemplateColumns: repeat(4,1fr)`
   - **Slider slot:** `visibility: hidden` when mode ≠ morph; `visibility: visible` when morph.
     **NEVER use `display:none` on the slider slot — use `visibility` only.** `display:none`
     collapses the reserved row and causes layout reflow.

3. **"This sample" panel** (`padding:16px; bg:var(--bg-1); border:var(--line); border-radius:10px`):
   - Mono header: `"This sample · <sample.id>"` (9.5px `--fg-3` uppercase)
   - 2-column grid: `Contour HC` (amber, 22px mono, `err X.XX mm`) and `Ellipse HC` (cyan, 22px mono, `err X.XX mm`)
   - Bottom dashed border: `Target <targetHC> mm` left + verdict right
   - Verdict: `"✓ ellipse wins by X.XX mm"` in `var(--good)` or `"⚠ contour wins by X.XX mm"` in `#ffb454`

4. **"But across the full set" insight** (`.insight` or `.insight.amber` when contour wins current sample):
   - Heading + paragraph with real computed values from all loaded samples
   - Per-sample stripe chart: `display:flex; gap:4px; height:22px; marginTop:10px`
   - Each column: two stacked bars — amber = `contourErr/7*100%` height, cyan = `ellipseErr/7*100%` height
   - Tooltip on hover: `title="${sample.id} · contour ${contourErr.toFixed(2)} · ellipse ${ellipseErr.toFixed(2)}"`

**Dataset summary computation (from geometry.jsx — runs over `allSamples`):**
```typescript
const datasetSummary = useMemo(() => {
  const errs = allSamples.map(s => ({
    id: s.id,
    contourErr: Math.abs(s.contourHC - s.metrics.targetHC),
    ellipseErr: s.metrics.hcErr,
    ellipseBetter: Math.abs(s.contourHC - s.metrics.targetHC) > s.metrics.hcErr,
  }));
  return {
    errs,
    ellipseWins: errs.filter(e => e.ellipseBetter).length,
    total: errs.length,
    meanContour: errs.reduce((a, b) => a + b.contourErr, 0) / errs.length,
    meanEllipse: errs.reduce((a, b) => a + b.ellipseErr, 0) / errs.length,
  };
}, [allSamples]);
```

### 6.12 `MetricsSection.tsx`, `ArcCard.tsx`, `BarCard.tsx`

Title row: eyebrow `"04 / Metrics in human terms"`, H2 `"What these numbers actually mean."`.

2×2 card grid: `gridTemplateColumns: repeat(2,1fr)`, gap `14px`.

**`ArcCard`** (Dice, IoU): three-quarter-circle SVG gauge.
- SVG `viewBox="-50 -50 100 70"`, `width:120px height:84px`
- Two strokes: bg track `var(--bg-4)` and value arc `color`, both `strokeWidth:6 strokeLinecap:round`
- Angles: `C = 2π × r × 0.75` (total dash), `dash = C × value × 0.75` (filled dash)
- Color thresholds for Dice `[0.85, 0.95]` → amber/cyan/green; IoU `[0.7, 0.9]`
- Value display: mono 26px; hint: 12.5px; description: 11px `--fg-3`

**`BarCard`** (HC error, HD95): large mono number + progress bar.
- Value: mono `30px` + unit `"mm"` at 13px `--fg-3`
- Bar: `height:6px; background:var(--bg-4); border-radius:999px; overflow:hidden`
- Fill: width = `min(1, value/max) * 100%`; color with glow
- Color: HC error `< 0.5mm` green, `< 3mm` cyan, `≥ 3mm` amber; HD95 same scale `max=10mm`

`min-height: 220px` on each card is mandatory to keep the 2×2 grid even.

Read `sample.metrics.hd95_mm` (not `.hd95`) for the HD95 card.

### 6.13 `MethodSection.tsx`

Three cards in `gridTemplateColumns: repeat(3,1fr)`, gap `14px`.

Each card: `padding:18px; background:var(--bg-2); border:1px solid var(--line); border-radius:12px`.

Card content (verbatim from app-v2.jsx MethodSection):

| Eyebrow | Headline | Body |
|---|---|---|
| `Architecture` | `Attention U-Net` | `"Local features + attention gates over 4 scales. Reduced parameter budget vs full U-Net++."` |
| `Training` | `HC18 · 999 images` | `"Augmentations: rotation, intensity jitter, elastic deform. Held-out test split."` |
| `Why ellipse fit` | `Geometric prior` | `"Real fetal skulls are ellipsoidal. Fitting projects predictions onto the right shape family."` |

Typography: eyebrow mono 10px `--fg-3` uppercase; headline Instrument Serif 22px; body 12.5px `--fg-2`.

Note: the v1 disclaimer `"Local training: 10 epochs, 256×384, base channels 16."` should be
added somewhere in this section — either as a fourth card or below the grid — since this
context matters for interpreting the metrics.

---

## 7. App state model

```typescript
// Top-level in App.tsx
const [activeId, setActiveId] = useState<string>(samples[0].id);
const [stageIdx, setStageIdx] = useState<number>(0);
const [playing, setPlaying] = useState<boolean>(false);
const [mode, setMode] = useState<'replay' | 'live'>('replay');
const [activeSection, setActiveSection] = useState<string>('play');

// Derived
const sample = samples.find(s => s.id === activeId) ?? samples[0];

// Optional: live mode state (V2.S7.3 — add only then)
const [liveRun, setLiveRun] = useState<LiveRunResult | null>(null);
const [liveStatus, setLiveStatus] = useState<LiveStatus>('idle');

// Active assets (static or live override)
const assetOverrides = mode === 'live' && liveRun?.assets ? liveRun.assets : undefined;

// Transport mode value for display
const transportMode: 'replay' | 'live' | 'computing' =
  mode === 'replay' ? 'replay' :
  liveStatus === 'running' ? 'computing' :
  liveStatus === 'done' ? 'live' :
  'replay';
```

Five effects:

```typescript
// 1. Pin to stage 0 on case switch (the v1 bug fix)
useEffect(() => { setStageIdx(0); setPlaying(false); }, [activeId]);

// 2. Auto-advance when playing
useEffect(() => {
  if (!playing) return;
  const t = setInterval(() => {
    setStageIdx(i => {
      if (i >= STAGES.length - 1) { setPlaying(false); return i; }
      return i + 1;
    });
  }, 1300);
  return () => clearInterval(t);
}, [playing]);

// 3. Scrollspy
useEffect(() => {
  const obs = new IntersectionObserver(entries => {
    const visible = entries.filter(e => e.isIntersecting)
      .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
    if (visible[0]) setActiveSection(visible[0].target.id);
  }, { rootMargin: '-20% 0px -60% 0px', threshold: 0 });
  ['play','threshold','geometry','metrics','method'].forEach(id => {
    const el = document.getElementById(id);
    if (el) obs.observe(el);
  });
  return () => obs.disconnect();
}, []);
```

---

## 8. Design tokens (complete)

Port both `styles.css` (v1 base, unchanged) and the additions from `styles-v2.css`.

### Color

```css
/* Background scale */
--bg-0: #07090f
--bg-1: #0c111b
--bg-2: #11172a   /* cards, panels */
--bg-3: #1a2238
--bg-4: #25304a

/* Foreground scale */
--fg-0: #f1f5fb   /* primary text */
--fg-1: #c2cbdc
--fg-2: #8a93a8
--fg-3: #5a6378   /* dim labels */

/* Borders */
--line:   rgba(255,255,255,0.06)
--line-2: rgba(255,255,255,0.10)

/* Accent */
--cyan:     #6ee0ff
--cyan-dim: rgba(110,224,255,0.55)
--amber:    #ffb454
--good:     #7be38b
--bad:      #ff7065

/* Stage-specific */
--stage-bg:   #08101a
--stage-line: rgba(110,224,255,0.18)

/* Easing */
--overlay-fade: cubic-bezier(.4,.2,.2,1)
--transport-h: 64px
```

### Typography

| Family | Use |
|---|---|
| `Instrument Serif` | H1 (46px), H2 sections (28px), H2 caption (26px), method headlines (22px) |
| `Inter` | Body, paragraphs (14.5 / 14 / 13.5 / 13 / 12.5 / 12) |
| `JetBrains Mono` | Status pills, labels, numbers, counters, eyebrows |

Letter-spacing on mono uppercase: `0.10em` to `0.14em`. Always uppercase for mono captions.
`letterSpacing: '-0.02em'` on H1 only.

### Motion

| Effect | Timing |
|---|---|
| Overlay layer fade | `480ms cubic-bezier(.4,.2,.2,1)` |
| Geometry layer fade | `280ms ease` |
| Tick rail fill | `380ms` |
| Transport button hover | `150ms` color, `100ms` scale |
| Auto-advance | `1300ms` per stage |
| Live LED pulse | `2s infinite` |
| Computing LED pulse | `1.4s infinite` |

### CSS classes to port from `styles-v2.css`

All new classes from `styles-v2.css` must be ported into `frontend/src/styles.css`:
- `.stage`, `.stage > .layer`, `.layer.fade-in`, `.layer.fade-out`
- `.stage .scale-ticks`
- `.focus-reticle`, `.focus-reticle::before`, `.focus-reticle::after`
- `.transport`, `.transport-btn`, `.transport-btn.primary`, `.transport-btn.ghost`
- `.tickrail`, `.tickrail .track`, `.tickrail .fill`, `.tickrail .stops`, `.tickrail .stop`, `.tickrail .stop.dot`
- `.status-pill`, `.status-pill .led`, `.status-pill.live`, `.status-pill.computing`
- `.caption`, `.caption .blurb-slot`, `.caption .stage-fact`
- `.geom-controls`, `.geom-controls .slider-slot`, `.geom-controls .slider-slot.show`
- `.insight`, `.insight.amber`
- `@media (max-width: 920px)` responsive overrides

---

## 9. Interaction preservation checklist

These interactions must be preserved exactly:

| Interaction | Source | Critical detail |
|---|---|---|
| Play/Pause toggle | Transport primary button | `setPlaying(b => !b)` |
| Auto-advance at 1300ms | `useEffect` on `playing` | Clear interval on cleanup; stop at last stage |
| Seek on tick rail click | Transport stop button | `setStageIdx(i)` directly |
| Prev/Next buttons | Transport ghost buttons | Clamped to `[0, STAGES.length - 1]` |
| Case switch → reset to stage 0 | `useEffect` on `activeId` | **Must also set `playing=false`** |
| Overlay fade (all layers always mounted) | `.fade-in / .fade-out` CSS | Never unmount overlays — only toggle class |
| Threshold canvas re-render | `useEffect` on `thresh + showProb` | Canvas draws on every value change |
| Morph slider → no reflow | `visibility:hidden` not `display:none` | `.slider-slot` always occupies 56px |
| Geometry mode tabs | Local `mode` state in GeometryV2 | Each tab click changes opacity — no component swap |
| Scrollspy nav | IntersectionObserver | `rootMargin:'-20% 0px -60% 0px'` exactly |
| Smooth scroll on nav click | `element.scrollIntoView({ behavior:'smooth', block:'start' })` | `scroll-margin-top: 72px` on each section |
| CORS on canvas reads | Vite dev: same-origin OK; Vercel: verify | All canvas-based overlays use `getImageData` |
| SafetyChip always visible | `position:fixed; right:16; bottom:16; zIndex:50` | Must not be conditionally hidden |
| `prefers-reduced-motion` | Pause `pulse-ring` + ellipse dash animation | Gate via CSS media query |

---

## 10. Live mode wiring (Transport ready, backend wiring in V2.S7.3)

The Transport and SubNav are designed so live inference requires no UI redesign.
The connection points are:

1. `SubNav` `mode` toggle → sets `mode` state in `App.tsx`
2. `App.tsx` maps `liveStatus` → `transportMode` (see Section 7)
3. `Transport` receives `mode` + `timing` props — rendering already handles all states
4. `assetOverrides` from `liveRun?.assets` flows into every image-consuming component via `getSampleAssets`
5. `StageCaption` fact tiles can pull live `step_times_ms` from `LiveInferResponse` (V2.S7.3 addition)

**Do not wire this logic until V2.S7.3.** In V2.S4/S5 work (porting the v2 design),
stub `mode='replay'` and `liveRun=null` — the Transport and SubNav still render correctly.

---

## 11. Implementation order

Follow this order — each step depends on the primitive below it:

1. **CSS tokens** — port `styles.css` + `styles-v2.css` into `frontend/src/styles.css`. Verify fonts load and custom properties resolve.
2. **`MediaStage` + `Outline` + `EllipseLayer`** — get the stable frame with all six stages working with static images. This is the foundation everything else builds on. Do not advance until all six stage overlays are correct.
3. **`ProbabilityViz`** — the iso-contour canvas. Validate against real `prob.png` files.
4. **`Transport`** — wire to local state first (no live mode). Confirm play/pause/seek/prev/next all work.
5. **`StageCaption`** — stable-height right column with fact tiles. Test across all six stages.
6. **`CasePickerCompact`** — 6 thumbnail buttons. Confirm case switch pins to stage 0.
7. **`HeroPlayer`** — assemble title row + compact picker + media stage + caption + transport.
8. **`SubNav`** with scrollspy — five section pills. Add mode toggle stub.
9. **`ThresholdSection` + `ProbThresholdLayer`** — canvas logic is same as v1; just the section wrapper changes.
10. **`GeometryV2` + `ContourPath`** — verify reserved-slot height does not reflow on mode switch.
11. **`MetricsSection` + `ArcCard` + `BarCard`** — pure layout, no interaction risk.
12. **`MethodSection`** — static, no interaction.
13. **`App.tsx` wiring** — 5 sections, state model, remove tour/gallery/experiments dependencies.
14. **Safety chip, responsive collapse, reduced-motion guards.**

---

## 12. Files to remove or demote

| Existing file | Action | Reason |
|---|---|---|
| `components/nav/TourBar.tsx` | Remove (or keep un-wired) | Tour mode removed in v2 |
| `components/hero/Hero.tsx` | Replace with `HeroPlayer` | Old hero is a title block; v2 hero owns the player |
| `components/gallery/SampleGallery.tsx` | Remove (or keep un-wired) | Replaced by `CasePickerCompact` inside hero |
| `components/pipeline/PipelineStepper.tsx` | Replace with `Transport` | Tick rail has different behavior and live slot |
| `components/pipeline/StageDetail.tsx` | Replace with `StageCaption` | Stable-height card, inside hero now |
| `components/experiments/ExperimentDashboard.tsx` | Keep un-wired | Removed from v2 but may return in V2.S9 |

Do not delete `ExperimentDashboard.tsx` — it holds the real experiment data logic and may
be restored in a later milestone.

---

## 13. What the design explicitly does NOT do

- Add full-image color floods (outlines and contours only on the ultrasound)
- Add decorative gradients (only functional: tick rail fill, insight callout gradient)
- Remove the six-stage pipeline story
- Replace the v1 palette or typography
- Become a clinical tool (safety chip is always visible)
- Support arbitrary image upload (curated samples only, same policy as V2.S7 scope)
