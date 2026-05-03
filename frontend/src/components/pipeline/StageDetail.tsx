import { STAGES } from "../../data/stages";
import { sampleAssetPath } from "../../data/samples";
import type { Sample } from "../../types/sample";

function formatMm(value: number) {
  return `${value.toFixed(2)} mm`;
}

function StageImage({ sample, stageId }: { sample: Sample; stageId: string }) {
  const width = sample.resolution.w;
  const height = sample.resolution.h;
  const ellipse = sample.predEllipse;
  const ellipseDegrees = (ellipse.rot * 180) / Math.PI;

  return (
    <div className="stage-image" style={{ aspectRatio: `${width} / ${height}` }}>
      <img
        alt={`${sample.id} ultrasound`}
        className="stage-image__base"
        src={sampleAssetPath(sample, "ultrasound")}
        style={{ opacity: stageId === "target" ? 0.35 : stageId === "input" ? 1 : 0.62 }}
      />
      <img
        alt={`${sample.id} target mask`}
        className="stage-image__overlay stage-image__overlay--cyan"
        src={sampleAssetPath(sample, "target")}
        style={{ opacity: stageId === "target" ? 0.86 : 0 }}
      />
      <img
        alt={`${sample.id} probability map`}
        className="stage-image__overlay stage-image__overlay--amber"
        src={sampleAssetPath(sample, "prob")}
        style={{ opacity: stageId === "prob" ? 0.86 : 0 }}
      />
      <img
        alt={`${sample.id} predicted mask`}
        className="stage-image__overlay stage-image__overlay--cyan"
        src={sampleAssetPath(sample, "pred")}
        style={{ opacity: stageId === "mask" || stageId === "ellipse" || stageId === "hc" ? 0.58 : 0 }}
      />

      {(stageId === "ellipse" || stageId === "hc") && (
        <svg className="stage-image__svg" viewBox={`0 0 ${width} ${height}`} aria-hidden="true">
          <ellipse
            cx={ellipse.cx}
            cy={ellipse.cy}
            fill="none"
            rx={ellipse.rx}
            ry={ellipse.ry}
            stroke="var(--cyan)"
            strokeWidth="1.5"
            style={{ filter: "drop-shadow(0 0 4px var(--cyan))" }}
            transform={`rotate(${ellipseDegrees.toFixed(2)} ${ellipse.cx} ${ellipse.cy})`}
          />
          {stageId === "hc" && (
            <ellipse
              cx={ellipse.cx}
              cy={ellipse.cy}
              fill="none"
              opacity="0.5"
              rx={ellipse.rx + 8}
              ry={ellipse.ry + 8}
              stroke="var(--cyan)"
              strokeDasharray="3 4"
              strokeWidth="0.6"
              transform={`rotate(${ellipseDegrees.toFixed(2)} ${ellipse.cx} ${ellipse.cy})`}
            />
          )}
        </svg>
      )}

      <div className="stage-image__label">
        <span className="mono">{STAGES.find((stage) => stage.id === stageId)?.short ?? stageId}</span>
      </div>
      <div className="stage-image__resolution">
        <span className="mono">
          {width} x {height} / {sample.spacingXMm.toFixed(3)} x {sample.spacingYMm.toFixed(3)} mm/px
        </span>
      </div>
    </div>
  );
}

function Stat({
  label,
  value,
  hint,
}: {
  label: string;
  value: string;
  hint?: string;
}) {
  return (
    <div className="stage-stat">
      <div className="mono stage-stat__label">{label}</div>
      <div className="mono stage-stat__value">{value}</div>
      {hint && <div className="stage-stat__hint">{hint}</div>}
    </div>
  );
}

function StageCallout({ sample, stageId }: { sample: Sample; stageId: string }) {
  const metrics = sample.metrics;

  switch (stageId) {
    case "input":
      return (
        <div className="stage-callout">
          <Stat label="Resolution" value={`${sample.resolution.w} x ${sample.resolution.h}`} hint="Single-channel grayscale" />
          <Stat
            label="Pixel size"
            value={`${sample.spacingXMm.toFixed(3)} / ${sample.spacingYMm.toFixed(3)} mm`}
            hint="Horizontal and vertical spacing"
          />
        </div>
      );
    case "target":
      return (
        <div className="stage-callout">
          <Stat
            label="Target source"
            value={sample.previewOnly ? "Preview mask" : "HC18 annotation"}
            hint={sample.previewOnly ? "Non-medical placeholder art" : "Converted to a binary mask"}
          />
          <Stat label="Target HC" value={formatMm(metrics.targetHC)} hint="Reference circumference" />
        </div>
      );
    case "prob":
      return (
        <div className="stage-callout">
          <Stat label="Mean confidence" value={`${(sample.confidence * 100).toFixed(0)}%`} hint="Inside predicted mask" />
          <Stat
            label="Architecture"
            value={sample.previewOnly ? "Preview mode" : "Attention U-Net"}
            hint={sample.previewOnly ? "Local run shows real model output" : "Saved local checkpoint output"}
          />
        </div>
      );
    case "mask":
      return (
        <div className="stage-callout">
          <Stat label="Threshold" value="0.50" hint="Default operating point" />
          <Stat label="Cleanup" value="Largest CC" hint="Keep the main predicted head region" />
        </div>
      );
    case "ellipse":
      return (
        <div className="stage-callout">
          <Stat label="Method" value="Least squares" hint="Ellipse fit to predicted mask contour" />
          <Stat
            label="rx / ry"
            value={`${sample.predEllipse.rx.toFixed(0)} / ${sample.predEllipse.ry.toFixed(0)} px`}
            hint="Semi-axes of fitted ellipse"
          />
        </div>
      );
    case "hc":
      return (
        <div className="stage-callout">
          <Stat label="Predicted HC" value={formatMm(metrics.predHC)} hint="Ellipse perimeter in millimetres" />
          <Stat
            label="Error"
            value={formatMm(metrics.hcErr)}
            hint={metrics.hcErr < 0.5 ? "Below pencil-tip width" : metrics.hcErr < 3 ? "About a grain of rice" : "Visible error"}
          />
        </div>
      );
    default:
      return null;
  }
}

export function StageDetail({ sample, stageIdx }: { sample: Sample; stageIdx: number }) {
  const stage = STAGES[stageIdx];

  return (
    <div className="stage-detail card fade-in" key={`${sample.id}-${stage.id}`}>
      <StageImage sample={sample} stageId={stage.id} />
      <div className="stage-detail__copy">
        <div>
          <div className="eyebrow">Stage {String(stageIdx + 1).padStart(2, "0")} of 06</div>
          <h3 className="serif">{stage.title}</h3>
        </div>
        <p className="stage-detail__blurb">{stage.blurb}</p>
        <p className="stage-detail__detail">{stage.detail}</p>
        <StageCallout sample={sample} stageId={stage.id} />
      </div>
    </div>
  );
}
