import { METRIC_COPY } from "../../data/metric-copy";

function metricColor(value: number, key: "hcErr" | "hd95_mm") {
  if (key === "hcErr") {
    if (value < 0.5) return "var(--good)";
    if (value < 3) return "var(--cyan)";
    return "var(--amber)";
  }

  if (value < 1) return "var(--good)";
  if (value < 6) return "var(--cyan)";
  return "var(--amber)";
}

export function BarCard({
  metricKey,
  max,
  unit,
  value,
}: {
  metricKey: "hcErr" | "hd95_mm";
  max: number;
  unit: string;
  value: number;
}) {
  const meta = METRIC_COPY[metricKey];
  const color = metricColor(value, metricKey);
  const pct = Math.max(0, Math.min(1, value / max));

  return (
    <article className="metric-card">
      <div className="mono metric-card__label">{meta.label}</div>
      <div className="bar-card__value mono">
        {value.toFixed(2)}
        <span>{unit}</span>
      </div>
      <div className="bar-card__rail">
        <div
          className="bar-card__fill"
          style={{ background: color, boxShadow: `0 0 6px ${color}`, width: `${pct * 100}%` }}
        />
      </div>
      <p>{meta.interpret(value)}</p>
      <small>{meta.description}</small>
    </article>
  );
}
