import { useEffect, useMemo, useState } from "react";

import { sampleAssetPath } from "../../data/samples";
import type { Sample } from "../../types/sample";
import { getMaskOutlineDataUrl } from "../../utils/maskOutline";

type GeometryView = "contour" | "ellipse" | "both" | "morph";

function formatMm(value: number | null | undefined) {
  return typeof value === "number" && Number.isFinite(value) ? `${value.toFixed(2)} mm` : "-";
}

function LegendDot({ active, color, label }: { active: boolean; color: string; label: string }) {
  return (
    <div className="legend-dot" style={{ opacity: active ? 1 : 0.4 }}>
      <span style={{ background: color, boxShadow: `0 0 6px ${color}` }} />
      <span className="mono">{label}</span>
    </div>
  );
}

function HCRow({ color, label, value }: { color: string; label: string; value: number | null | undefined }) {
  return (
    <div className="hc-row">
      <div className="mono hc-row__label">{label}</div>
      <div className="mono hc-row__value" style={{ color }}>
        {formatMm(value)}
      </div>
    </div>
  );
}

export function ContourEllipse({ sample }: { sample: Sample }) {
  const [view, setView] = useState<GeometryView>("both");
  const [morph, setMorph] = useState(0.5);
  const [contourOutlineSrc, setContourOutlineSrc] = useState<string | null>(null);
  const width = sample.resolution.w;
  const height = sample.resolution.h;
  const ellipse = sample.predEllipse;
  const ellipseDegrees = (ellipse.rot * 180) / Math.PI;
  const predictedMaskSrc = useMemo(() => sampleAssetPath(sample, "pred"), [sample]);
  const contourOpacity = view === "ellipse" ? 0 : view === "morph" ? 1 - morph : 0.72;
  const ellipseOpacity = view === "contour" ? 0 : view === "morph" ? morph : 1;
  const contourDiff =
    typeof sample.contourHC === "number" && Number.isFinite(sample.contourHC)
      ? sample.contourHC - sample.metrics.predHC
      : null;

  useEffect(() => {
    let cancelled = false;
    setContourOutlineSrc(null);

    getMaskOutlineDataUrl(predictedMaskSrc)
      .then((nextSrc) => {
        if (!cancelled) {
          setContourOutlineSrc(nextSrc);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setContourOutlineSrc(null);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [predictedMaskSrc]);

  return (
    <div className="geometry-grid">
      <div className="geometry-image" style={{ aspectRatio: `${width} / ${height}` }}>
        <img
          alt={`${sample.id} ultrasound`}
          className="geometry-image__base"
          src={sampleAssetPath(sample, "ultrasound")}
        />
        <img
          alt={`${sample.id} contour outline`}
          className="geometry-image__contour"
          src={contourOutlineSrc ?? predictedMaskSrc}
          style={{ opacity: contourOpacity }}
        />
        <svg className="geometry-image__svg" viewBox={`0 0 ${width} ${height}`} aria-hidden="true">
          <ellipse
            cx={ellipse.cx}
            cy={ellipse.cy}
            fill="rgba(110,224,255,0.04)"
            opacity={ellipseOpacity}
            rx={ellipse.rx}
            ry={ellipse.ry}
            stroke="var(--cyan)"
            strokeWidth="1.5"
            style={{ filter: "drop-shadow(0 0 4px rgba(110,224,255,0.75))" }}
            transform={`rotate(${ellipseDegrees.toFixed(2)} ${ellipse.cx} ${ellipse.cy})`}
          />
        </svg>
        <div className="geometry-image__legend">
          <LegendDot active={view !== "ellipse"} color="var(--amber)" label="Cleaned contour" />
          <LegendDot active={view !== "contour"} color="var(--cyan)" label="Fitted ellipse" />
        </div>
      </div>

      <div className="geometry-panel">
        <div>
          <div className="eyebrow">04 / Ellipse regularization</div>
          <h2 className="serif">Why the mask becomes a measurement.</h2>
        </div>
        <p>
          The predicted mask is useful, but head circumference is a geometric quantity. This panel
          compares the contour-derived HC with the ellipse fit used by the final v1 measurement.
        </p>
        <p className="geometry-panel__note">
          Amber shows the cleaned contour boundary. Cyan shows the fitted ellipse used for the final
          saved-output measurement.
        </p>

        <div className="segmented-control" aria-label="Geometry view">
          {[
            ["contour", "Contour"],
            ["ellipse", "Ellipse"],
            ["both", "Both"],
            ["morph", "Morph"],
          ].map(([key, label]) => (
            <button
              className={view === key ? "active" : ""}
              key={key}
              onClick={() => setView(key as GeometryView)}
              type="button"
            >
              {label}
            </button>
          ))}
        </div>

        {view === "morph" && (
          <div className="geometry-morph">
            <input
              aria-label="Morph contour to ellipse"
              max={1}
              min={0}
              onChange={(event) => setMorph(Number.parseFloat(event.target.value))}
              step={0.01}
              type="range"
              value={morph}
            />
            <div className="mono">
              <span>Contour</span>
              <span>Ellipse</span>
            </div>
          </div>
        )}

        <div className="hc-comparison">
          <div className="mono hc-comparison__title">HC measurement comparison</div>
          <div className="hc-comparison__rows">
            <HCRow color="var(--amber)" label="Contour HC" value={sample.contourHC} />
            <HCRow color="var(--cyan)" label="Ellipse HC" value={sample.metrics.predHC} />
          </div>
          <div className="hc-comparison__delta">
            <span>Delta between methods</span>
            <strong className="mono">{contourDiff === null ? "-" : `${contourDiff.toFixed(2)} mm`}</strong>
          </div>
          <div className="hc-comparison__target">
            Target HC <span className="mono">{formatMm(sample.metrics.targetHC)}</span> / final error{" "}
            <span className="mono">{formatMm(sample.metrics.hcErr)}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
