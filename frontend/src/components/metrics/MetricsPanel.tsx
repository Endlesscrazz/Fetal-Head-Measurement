import { METRIC_COPY } from "../../data/metric-copy";
import type { Sample } from "../../types/sample";

function metricColor(value: number, good: number, ok: number, higherIsBetter = true) {
  if (higherIsBetter) {
    if (value >= good) return "var(--good)";
    if (value >= ok) return "var(--cyan)";
    return "var(--amber)";
  }
  if (value <= good) return "var(--good)";
  if (value <= ok) return "var(--cyan)";
  return "var(--amber)";
}

function ArcMetric({
  description,
  hint,
  label,
  thresholds,
  value,
}: {
  description: string;
  hint: string;
  label: string;
  thresholds: [number, number];
  value: number;
}) {
  const radius = 38;
  const circumference = 2 * Math.PI * radius;
  const total = circumference * 0.75;
  const dash = total * Math.max(0, Math.min(1, value));
  const color = metricColor(value, thresholds[1], thresholds[0]);

  return (
    <div className="metric-card card">
      <div className="mono metric-card__label">{label}</div>
      <div className="arc-metric">
        <svg viewBox="-50 -50 100 72" aria-hidden="true">
          <g transform="rotate(135)">
            <circle
              fill="none"
              r={radius}
              stroke="var(--line-2)"
              strokeDasharray={`${total} ${circumference}`}
              strokeLinecap="round"
              strokeWidth="6"
            />
            <circle
              fill="none"
              r={radius}
              stroke={color}
              strokeDasharray={`${dash} ${circumference}`}
              strokeLinecap="round"
              strokeWidth="6"
              style={{ filter: `drop-shadow(0 0 4px ${color})` }}
            />
          </g>
        </svg>
        <div>
          <strong className="mono">{value.toFixed(4)}</strong>
          <span className="mono">0 to 1</span>
        </div>
      </div>
      <p>{hint}</p>
      <small>{description}</small>
    </div>
  );
}

function ScaleMetric({
  description,
  hint,
  label,
  max = 10,
  unit,
  value,
}: {
  description: string;
  hint: string;
  label: string;
  max?: number;
  unit: string;
  value: number;
}) {
  const pct = Math.max(0, Math.min(1, value / max));
  const color = metricColor(value, label === "HC error" ? 0.5 : 1, label === "HC error" ? 3 : 6, false);

  return (
    <div className="metric-card card">
      <div className="mono metric-card__label">{label}</div>
      <div className="scale-metric__value mono">
        {value.toFixed(2)}
        <span>{unit}</span>
      </div>
      <div className="scale-metric__rail">
        <div style={{ background: color, boxShadow: `0 0 6px ${color}`, width: `${pct * 100}%` }} />
      </div>
      <p>{hint}</p>
      <small>{description}</small>
    </div>
  );
}

function MeasurementSummary({ sample }: { sample: Sample }) {
  return (
    <div className="metrics-summary card">
      <div>
        <div className="eyebrow">Final measurement</div>
        <h3 className="serif">{sample.metrics.predHC.toFixed(2)} mm</h3>
      </div>
      <div className="metrics-summary__grid">
        <div>
          <span className="mono">Target</span>
          <strong className="mono">{sample.metrics.targetHC.toFixed(2)} mm</strong>
        </div>
        <div>
          <span className="mono">Error</span>
          <strong className="mono">{sample.metrics.hcErr.toFixed(2)} mm</strong>
        </div>
        <div>
          <span className="mono">Confidence</span>
          <strong className="mono">{(sample.confidence * 100).toFixed(1)}%</strong>
        </div>
      </div>
    </div>
  );
}

export function MetricsPanel({ sample }: { sample: Sample }) {
  const m = sample.metrics;

  return (
    <div className="metrics-section">
      <div className="section-heading">
        <div>
          <div className="eyebrow">05 / Evaluation metrics</div>
          <h2 className="serif">Quality checks for the selected case.</h2>
        </div>
        <p>Overlap metrics judge the mask. HC error judges the measurement.</p>
      </div>

      <div className="metrics-grid">
        <ArcMetric
          description={METRIC_COPY.dice.description}
          hint={METRIC_COPY.dice.interpret(m.dice)}
          label={METRIC_COPY.dice.label}
          thresholds={[0.85, 0.95]}
          value={m.dice}
        />
        <ArcMetric
          description={METRIC_COPY.iou.description}
          hint={METRIC_COPY.iou.interpret(m.iou)}
          label={METRIC_COPY.iou.label}
          thresholds={[0.7, 0.9]}
          value={m.iou}
        />
        <ScaleMetric
          description={METRIC_COPY.hcErr.description}
          hint={METRIC_COPY.hcErr.interpret(m.hcErr)}
          label={METRIC_COPY.hcErr.label}
          max={12}
          unit="mm"
          value={m.hcErr}
        />
        <ScaleMetric
          description={METRIC_COPY.hd95_mm.description}
          hint={METRIC_COPY.hd95_mm.interpret(m.hd95_mm)}
          label={METRIC_COPY.hd95_mm.label}
          max={10}
          unit="mm"
          value={m.hd95_mm}
        />
      </div>

      <MeasurementSummary sample={sample} />
    </div>
  );
}
