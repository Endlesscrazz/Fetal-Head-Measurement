import { useMemo, useState } from "react";

import type { Sample } from "../../types/sample";
import type { SampleAssets } from "../../utils/assets";
import { ContourPath } from "./ContourPath";

type GeometryMode = "contour" | "ellipse" | "both" | "morph";

export function GeometryV2({
  assets,
  allSamples,
  sample,
}: {
  assets: SampleAssets;
  allSamples: Sample[];
  sample: Sample;
}) {
  const [mode, setMode] = useState<GeometryMode>("both");
  const [morph, setMorph] = useState(0.5);

  const contourOpacity = mode === "morph" ? 1 - morph : mode === "ellipse" ? 0 : 1;
  const ellipseOpacity = mode === "morph" ? morph : mode === "contour" ? 0 : 1;
  const contourErr = Math.abs(sample.contourHC - sample.metrics.targetHC);
  const ellipseErr = sample.metrics.hcErr;
  const ellipseBetter = ellipseErr < contourErr;
  const delta = Math.abs(contourErr - ellipseErr);

  const datasetSummary = useMemo(() => {
    const errs = allSamples.map((entry) => {
      const contour = Math.abs(entry.contourHC - entry.metrics.targetHC);
      const ellipse = entry.metrics.hcErr;
      return {
        contourErr: contour,
        ellipseBetter: contour > ellipse,
        ellipseErr: ellipse,
        id: entry.id,
      };
    });

    const total = errs.length || 1;
    return {
      ellipseWins: errs.filter((entry) => entry.ellipseBetter).length,
      errs,
      meanContour: errs.reduce((sum, entry) => sum + entry.contourErr, 0) / total,
      meanEllipse: errs.reduce((sum, entry) => sum + entry.ellipseErr, 0) / total,
      total,
    };
  }, [allSamples]);

  const degrees = (sample.predEllipse.rot * 180) / Math.PI;

  return (
    <div className="section-grid">
      <div className="stage">
        <img
          alt={`${sample.id} ultrasound`}
          className="layer fade-in stage__image"
          src={assets.ultrasound}
          style={{ filter: "brightness(0.78) contrast(1.05)" }}
        />
        <svg
          aria-hidden="true"
          className="layer fade-in"
          preserveAspectRatio="xMidYMid slice"
          viewBox={`0 0 ${sample.resolution.w} ${sample.resolution.h}`}
        >
          <ContourPath ellipse={sample.predEllipse} opacity={contourOpacity} />
          <ellipse
            cx={sample.predEllipse.cx}
            cy={sample.predEllipse.cy}
            fill="rgba(110,224,255,0.04)"
            opacity={ellipseOpacity}
            rx={sample.predEllipse.rx}
            ry={sample.predEllipse.ry}
            stroke="#6ee0ff"
            strokeWidth="1.6"
            style={{
              filter: "drop-shadow(0 0 4px rgba(110,224,255,0.7))",
              transition: "opacity 280ms ease",
            }}
            transform={`rotate(${degrees.toFixed(2)} ${sample.predEllipse.cx} ${sample.predEllipse.cy})`}
          />
        </svg>

        <div className="geometry-v2__legend">
          <div className="geometry-v2__legend-pill" style={{ opacity: contourOpacity > 0.05 ? 1 : 0.4 }}>
            <span className="geometry-v2__legend-dot geometry-v2__legend-dot--amber" />
            <span className="mono">Cleaned contour</span>
          </div>
          <div className="geometry-v2__legend-pill" style={{ opacity: ellipseOpacity > 0.05 ? 1 : 0.4 }}>
            <span className="geometry-v2__legend-dot geometry-v2__legend-dot--cyan" />
            <span className="mono">Fitted ellipse</span>
          </div>
        </div>

        <div className="scale-ticks">
          <span className="swatch" />
          <span>10 mm</span>
        </div>
      </div>

      <div className="section-stack">
        <div>
          <div className="eyebrow">03 / Geometry regularization</div>
          <h2 className="serif section-title">Why the mask becomes a measurement.</h2>
          <p className="section-copy">
            The mask is useful, but circumference is a geometric quantity. This view compares the
            contour-derived HC to the ellipse fit used for the final saved-output measurement.
          </p>
        </div>

        <div className="geom-controls panel">
          <div className="geom-controls__tabs">
            {[
              ["contour", "Contour"],
              ["ellipse", "Ellipse"],
              ["both", "Both"],
              ["morph", "Morph"],
            ].map(([value, label]) => (
              <button
                key={value}
                className={mode === value ? "active" : ""}
                onClick={() => setMode(value as GeometryMode)}
                type="button"
              >
                {label}
              </button>
            ))}
          </div>
          <div className={`slider-slot ${mode === "morph" ? "show" : ""}`}>
            <input
              max={1}
              min={0}
              onChange={(event) => setMorph(Number.parseFloat(event.target.value))}
              step={0.01}
              type="range"
              value={morph}
            />
            <div className="mono slider-slot__labels">
              <span>Contour</span>
              <span>{Math.round(morph * 100)}%</span>
              <span>Ellipse</span>
            </div>
          </div>
        </div>

        <div className="panel geometry-v2__sample-panel">
          <div className="mono geometry-v2__sample-title">This sample · {sample.id}</div>
          <div className="geometry-v2__sample-grid">
            <div>
              <div className="mono geometry-v2__metric-label">Contour HC</div>
              <div className="mono geometry-v2__metric-value geometry-v2__metric-value--amber">
                {sample.contourHC.toFixed(2)}
                <span>mm</span>
              </div>
              <div className="mono geometry-v2__metric-note">err {contourErr.toFixed(2)} mm</div>
            </div>
            <div>
              <div className="mono geometry-v2__metric-label">Ellipse HC</div>
              <div className="mono geometry-v2__metric-value geometry-v2__metric-value--cyan">
                {sample.metrics.predHC.toFixed(2)}
                <span>mm</span>
              </div>
              <div className="mono geometry-v2__metric-note">err {ellipseErr.toFixed(2)} mm</div>
            </div>
          </div>
          <div className="geometry-v2__target-row">
            <span>
              Target <span className="mono">{sample.metrics.targetHC.toFixed(2)} mm</span>
            </span>
            <span className={`mono ${ellipseBetter ? "geometry-v2__verdict--good" : "geometry-v2__verdict--amber"}`}>
              {ellipseBetter ? "✓ ellipse wins by" : "⚠ contour wins by"} {delta.toFixed(2)} mm
            </span>
          </div>
        </div>

        <div className={`insight ${ellipseBetter ? "" : "amber"}`}>
          <div className="mono insight__title">But across the full set</div>
          <p>
            On <strong>{datasetSummary.ellipseWins}/{datasetSummary.total}</strong> samples the
            ellipse fit beats the raw contour. Mean error: contour{" "}
            <strong className="geometry-v2__verdict--amber">{datasetSummary.meanContour.toFixed(2)} mm</strong>,
            ellipse <strong className="geometry-v2__verdict--cyan">{datasetSummary.meanEllipse.toFixed(2)} mm</strong>.
          </p>
          <div className="geometry-v2__stripe-chart">
            {datasetSummary.errs.map((entry) => (
              <div
                key={entry.id}
                className="geometry-v2__stripe-col"
                title={`${entry.id} · contour ${entry.contourErr.toFixed(2)} · ellipse ${entry.ellipseErr.toFixed(2)}`}
              >
                <div
                  className="geometry-v2__stripe-colour geometry-v2__stripe-colour--amber"
                  style={{ height: `${Math.min(100, (entry.contourErr / 7) * 100)}%` }}
                />
                <div
                  className="geometry-v2__stripe-colour geometry-v2__stripe-colour--cyan"
                  style={{ height: `${Math.min(100, (entry.ellipseErr / 7) * 100)}%` }}
                />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
