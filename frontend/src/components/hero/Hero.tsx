import { CategoryBadge } from "../shared/CategoryBadge";
import type { Sample } from "../../types/sample";

function MiniMetric({ label, value, accent }: { label: string; value: string; accent?: boolean }) {
  return (
    <div className="mini-metric">
      <div className="mono mini-metric__label">{label}</div>
      <div className="mono mini-metric__value" style={{ color: accent ? "var(--cyan)" : "var(--fg-0)" }}>
        {value}
      </div>
    </div>
  );
}

function Stat({ k, v }: { k: string; v: string }) {
  return (
    <div className="hero-stat">
      <div className="mono hero-stat__label">{k}</div>
      <div className="mono hero-stat__value">{v}</div>
    </div>
  );
}

function Logo() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <ellipse cx="12" cy="12" rx="9" ry="6.5" stroke="var(--cyan)" strokeWidth="1.6" />
      <ellipse cx="12" cy="12" rx="5" ry="3.5" stroke="var(--cyan)" strokeWidth="1" opacity="0.5" />
      <circle cx="12" cy="12" r="1.4" fill="var(--cyan)" />
    </svg>
  );
}

export function Hero({
  activeSample,
  sampleCount,
  onStartTour,
}: {
  activeSample: Sample;
  sampleCount: number;
  onStartTour: () => void;
}) {
  const previewOnly = activeSample.previewOnly === true;

  return (
    <header className="hero">
      <div className="hero__copy">
        <div className="hero__brand">
          <Logo />
          <span className="mono">Fetal HC / Pipeline Explorer / v2</span>
        </div>
        <h1 className="serif">
          See how a CNN measures the circumference of a fetal head, stage by stage.
        </h1>
        <p>
          {previewOnly
            ? "Public preview mode uses non-medical placeholder art. Run locally with exported HC18 artifacts to see the real saved model outputs."
            : "From a noisy ultrasound to a single number in millimetres: six visible steps, real saved model outputs, and no retraining during the demo."}
        </p>
        <div className="hero__actions">
          <button className="hero__primary" onClick={onStartTour} type="button">
            Take the 6-step tour
          </button>
          <button
            className="hero__secondary"
            onClick={() => document.getElementById("cases")?.scrollIntoView({ behavior: "smooth" })}
            type="button"
          >
            Explore freely
          </button>
        </div>
        <div className="hero__stats">
          <Stat k="Curated samples" v={String(sampleCount)} />
          <Stat k="Pipeline stages" v="6" />
          <Stat k="Architecture" v="Attention U-Net" />
          <Stat k="Mode" v={previewOnly ? "Public preview" : "Static replay"} />
        </div>
      </div>

      <div className="hero-card card">
        <div className="hero-card__glow" />
        <div className="hero-card__title">
          <div>
            <div className="mono hero-card__eyebrow">Active case / {activeSample.id}</div>
            <div className="serif hero-card__name">{activeSample.label}</div>
          </div>
          <CategoryBadge cat={activeSample.cat} />
        </div>
        <p>{activeSample.summary}</p>
        <div className="hero-card__metrics">
          <MiniMetric label="Pred HC" value={`${activeSample.metrics.predHC.toFixed(2)} mm`} />
          <MiniMetric label="Target" value={`${activeSample.metrics.targetHC.toFixed(2)} mm`} />
          <MiniMetric label="Error" value={`${activeSample.metrics.hcErr.toFixed(2)} mm`} accent />
        </div>
      </div>
    </header>
  );
}
