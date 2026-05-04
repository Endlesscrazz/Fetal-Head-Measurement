import { METRIC_COPY } from "../../data/metric-copy";

function metricColor(value: number, ok: number, good: number) {
  if (value >= good) return "var(--good)";
  if (value >= ok) return "var(--cyan)";
  return "var(--amber)";
}

export function ArcCard({
  metricKey,
  value,
}: {
  metricKey: "dice" | "iou";
  value: number;
}) {
  const meta = METRIC_COPY[metricKey];
  const thresholds: [number, number] = metricKey === "dice" ? [0.85, 0.95] : [0.7, 0.9];
  const color = metricColor(value, thresholds[0], thresholds[1]);
  const radius = 38;
  const circumference = 2 * Math.PI * radius;
  const total = circumference * 0.75;
  const dash = total * Math.max(0, Math.min(1, value));

  return (
    <article className="metric-card">
      <div className="mono metric-card__label">{meta.label}</div>
      <div className="arc-card__wrap">
        <svg aria-hidden="true" viewBox="-50 -50 100 72">
          <g transform="rotate(135)">
            <circle
              fill="none"
              r={radius}
              stroke="var(--bg-4)"
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
      <p>{meta.interpret(value)}</p>
      <small>{meta.description}</small>
    </article>
  );
}
