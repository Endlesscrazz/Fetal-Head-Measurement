import { useEffect, useMemo, useState } from "react";

interface ExperimentPoint {
  epoch: number;
  train_loss: number;
  val_loss: number;
  val_dice: number;
}

interface ExperimentRun {
  id: string;
  name: string;
  tag: string;
  split: string;
  epochs: number;
  imageSize: string;
  baseChannels: number;
  curve: ExperimentPoint[];
  summary: {
    n_samples: number;
    mean_dice: number;
    mean_iou: number;
    mean_hd95_mm: number;
    mae_hc_mm: number;
    rmse_hc_mm: number;
  };
}

interface AblationRow {
  run_id: string;
  label: string;
  mean_dice: number;
  mae_hc_mm: number;
  mean_hd95_mm: number;
}

interface PostprocessRow {
  variant: string;
  label: string;
  mae_hc_mm: number;
  rmse_hc_mm: number;
  n_samples: number;
}

interface ExperimentSummary {
  training_note: string;
  runs: ExperimentRun[];
  ablation: AblationRow[];
  postprocess: PostprocessRow[];
}

function formatRunLabel(label: string) {
  return label
    .replace("attention unet", "Attention U-Net")
    .replace("unet", "U-Net")
    .replace("bce dice", "BCE + Dice")
    .replace("+aug", "+ Aug");
}

function Sparkline({ color, points }: { color: string; points: number[] }) {
  const width = 280;
  const height = 60;
  const max = Math.max(...points);
  const min = Math.min(...points);
  const span = max - min || 1;
  const path = points
    .map((point, index) => {
      const x = points.length === 1 ? 0 : (index / (points.length - 1)) * width;
      const y = height - ((point - min) / span) * (height - 8) - 4;
      return `${index === 0 ? "M" : "L"} ${x.toFixed(1)} ${y.toFixed(1)}`;
    })
    .join(" ");

  return (
    <svg className="sparkline" preserveAspectRatio="none" viewBox={`0 0 ${width} ${height}`} aria-hidden="true">
      <path d={`${path} L ${width} ${height} L 0 ${height} Z`} fill={color} fillOpacity="0.08" />
      <path d={path} fill="none" stroke={color} strokeWidth="1.5" />
    </svg>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="experiment-stat">
      <div className="mono">{label}</div>
      <strong className="mono">{value}</strong>
    </div>
  );
}

function RunCard({
  active,
  onPick,
  run,
}: {
  active: boolean;
  onPick: () => void;
  run: ExperimentRun;
}) {
  const color = active ? "var(--cyan)" : "var(--fg-3)";
  const finalValDice = run.curve.at(-1)?.val_dice ?? run.summary.mean_dice;

  return (
    <button className={`experiment-card card ${active ? "active" : ""}`} onClick={onPick} type="button">
      <div className="experiment-card__top">
        <span className="serif">{run.name}</span>
        <span className={`mono experiment-tag experiment-tag--${run.tag}`}>{run.tag}</span>
      </div>
      <Sparkline color={color} points={run.curve.map((point) => point.val_dice)} />
      <div className="experiment-card__stats">
        <Stat label="Test Dice" value={run.summary.mean_dice.toFixed(3)} />
        <Stat label="HC MAE" value={`${run.summary.mae_hc_mm.toFixed(2)}mm`} />
        <Stat label="Val Dice" value={finalValDice.toFixed(3)} />
      </div>
    </button>
  );
}

function TrainingCurve({ run }: { run: ExperimentRun }) {
  const lossMax = Math.max(...run.curve.flatMap((point) => [point.train_loss, point.val_loss]));
  const diceMin = Math.min(...run.curve.map((point) => point.val_dice));
  const diceMax = Math.max(...run.curve.map((point) => point.val_dice));

  return (
    <div className="training-curve card">
      <div className="training-curve__header">
        <div>
          <div className="eyebrow">Selected run</div>
          <h3 className="serif">{run.name}</h3>
        </div>
        <span className="mono">{run.epochs} epochs / {run.split}</span>
      </div>
      <div className="training-curve__rows">
        {run.curve.map((point) => {
          const lossPct = Math.max(3, (point.val_loss / lossMax) * 100);
          const dicePct = Math.max(3, ((point.val_dice - diceMin) / (diceMax - diceMin || 1)) * 100);
          return (
            <div className="training-epoch" key={point.epoch}>
              <span className="mono">E{point.epoch}</span>
              <div className="training-bars">
                <i className="training-bars__loss" style={{ width: `${lossPct}%` }} />
                <i className="training-bars__dice" style={{ width: `${dicePct}%` }} />
              </div>
              <strong className="mono">{point.val_dice.toFixed(3)}</strong>
            </div>
          );
        })}
      </div>
      <div className="training-curve__legend">
        <span><i className="loss" /> val loss</span>
        <span><i className="dice" /> val Dice</span>
      </div>
    </div>
  );
}

function AblationTable({ rows }: { rows: AblationRow[] }) {
  const minDice = 0.9;
  const bestDice = Math.max(...rows.map((row) => row.mean_dice));

  return (
    <div className="ablation-card card">
      <div className="mono ablation-card__title">Model and augmentation ablation / internal test split</div>
      <div className="ablation-list">
        {rows.map((row) => {
          const width = Math.max(4, ((row.mean_dice - minDice) / (bestDice - minDice || 1)) * 100);
          const active = row.mean_dice === bestDice;
          return (
            <div className="ablation-row" key={row.run_id}>
              <span>{formatRunLabel(row.label)}</span>
              <div>
                <i className={active ? "active" : ""} style={{ width: `${width}%` }} />
              </div>
              <strong className="mono">
                {row.mean_dice.toFixed(3)} <span>/ {row.mae_hc_mm.toFixed(2)}mm</span>
              </strong>
            </div>
          );
        })}
      </div>
      <p>Bars show Dice above a 0.90 floor. HC MAE is shown beside each run.</p>
    </div>
  );
}

function PostprocessTable({ rows }: { rows: PostprocessRow[] }) {
  const worst = Math.max(...rows.map((row) => row.mae_hc_mm));

  return (
    <div className="ablation-card card">
      <div className="mono ablation-card__title">Post-processing ablation / Attention U-Net</div>
      <div className="ablation-list">
        {rows.map((row) => {
          const width = Math.max(4, (row.mae_hc_mm / worst) * 100);
          const active = row.variant === "cleaned_ellipse" || row.variant === "raw_largest_contour_ellipse";
          return (
            <div className="ablation-row" key={row.variant}>
              <span>{row.label}</span>
              <div>
                <i className={active ? "active" : ""} style={{ width: `${width}%` }} />
              </div>
              <strong className="mono">
                {row.mae_hc_mm.toFixed(2)}mm <span>/ RMSE {row.rmse_hc_mm.toFixed(2)}</span>
              </strong>
            </div>
          );
        })}
      </div>
      <p>Lower is better here. Ellipse fitting sharply reduces HC error compared with contour perimeter.</p>
    </div>
  );
}

export function ExperimentDashboard() {
  const [summary, setSummary] = useState<ExperimentSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [activeId, setActiveId] = useState("attention_unet_local_baseline");

  useEffect(() => {
    let cancelled = false;
    fetch("/experiments/summary.json")
      .then((response) => {
        if (!response.ok) throw new Error(`Failed to load experiments: ${response.status}`);
        return response.json() as Promise<ExperimentSummary>;
      })
      .then((nextSummary) => {
        if (cancelled) return;
        setSummary(nextSummary);
        setActiveId(nextSummary.runs.find((run) => run.tag === "best")?.id ?? nextSummary.runs[0]?.id ?? "");
      })
      .catch((nextError: unknown) => {
        if (cancelled) return;
        setError(nextError instanceof Error ? nextError.message : String(nextError));
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const activeRun = useMemo(
    () => summary?.runs.find((run) => run.id === activeId) ?? summary?.runs[0],
    [activeId, summary],
  );

  if (error) {
    return (
      <div className="card load-state load-state--error">
        <div className="eyebrow">Experiment data error</div>
        <p>{error}</p>
      </div>
    );
  }

  if (!summary || !activeRun) {
    return (
      <div className="card load-state">
        <div className="eyebrow">Loading</div>
        <p>Loading /experiments/summary.json...</p>
      </div>
    );
  }

  return (
    <div className="experiment-dashboard">
      <div className="section-heading">
        <div>
          <div className="eyebrow">06 / Research dashboard</div>
          <h2 className="serif">The experiment story behind the demo.</h2>
        </div>
        <p>{summary.training_note}</p>
      </div>

      <div className="experiment-cards">
        {summary.runs.map((run) => (
          <RunCard active={activeRun.id === run.id} key={run.id} onPick={() => setActiveId(run.id)} run={run} />
        ))}
      </div>

      <TrainingCurve run={activeRun} />

      <div className="experiment-tables">
        <AblationTable rows={summary.ablation} />
        <PostprocessTable rows={summary.postprocess} />
      </div>
    </div>
  );
}
