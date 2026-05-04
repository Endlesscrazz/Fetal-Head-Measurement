import { useEffect, useMemo, useState } from "react";

import type { Sample } from "../../types/sample";
import type { SampleAssets } from "../../utils/assets";
import { ProbThresholdLayer } from "./ProbThresholdLayer";

function thresholdInsight(thresh: number) {
  if (thresh < 0.3) return "Below 0.3 the mask leaks into noise and low-confidence tissue.";
  if (thresh < 0.6) return "Around 0.5 the model commits to its strongest beliefs and keeps the skull boundary coherent.";
  if (thresh < 0.85) return "Above 0.6 the low-confidence fringe falls away and only the interior survives.";
  return "At 0.85+ the mask collapses to the most certain core of the prediction.";
}

export function ThresholdSection({
  assets,
  sample,
}: {
  assets: SampleAssets;
  sample: Sample;
}) {
  const [thresh, setThresh] = useState(0.5);
  const [showProb, setShowProb] = useState(true);

  useEffect(() => {
    setThresh(0.5);
    setShowProb(true);
  }, [sample.id]);

  const coverageLabel = useMemo(() => {
    const optimal = sample.thresholdCurve?.optimalThreshold;
    if (typeof optimal === "number") {
      return `Best exported Dice at ${optimal.toFixed(2)}`;
    }
    return "Default operating point";
  }, [sample.thresholdCurve]);

  return (
    <div className="section-grid">
      <div className="stage">
        <img
          alt={`${sample.id} ultrasound`}
          className="layer fade-in stage__image"
          src={assets.ultrasound}
          style={{ filter: "brightness(0.78) contrast(1.05)" }}
        />
        <ProbThresholdLayer probSrc={assets.prob} sample={sample} showProb={showProb} thresh={thresh} />
        <div className="stage__top-left">
          <div className="status-pill">
            <span className="led led--cyan" />τ = {thresh.toFixed(2)}
          </div>
        </div>
        <div className="scale-ticks">
          <span className="swatch" />
          <span>10 mm</span>
        </div>
      </div>

      <div className="section-stack">
        <div>
          <div className="eyebrow">02 / Threshold ↦ Mask</div>
          <h2 className="serif section-title">The moment the model commits.</h2>
          <p className="section-copy">
            The CNN outputs a belief for every pixel. Drag tau to see which regions survive the
            decision boundary and which ones stay uncertain.
          </p>
        </div>

        <div className="panel">
          <input
            max={1}
            min={0}
            onChange={(event) => setThresh(Number.parseFloat(event.target.value))}
            step={0.01}
            type="range"
            value={thresh}
          />
          <div className="mono threshold-section__labels">
            <span>0.00 · noisy</span>
            <span className="threshold-section__active">τ = {thresh.toFixed(2)}</span>
            <span>1.00 · strict</span>
          </div>
        </div>

        <label className="threshold-section__toggle">
          <input
            checked={showProb}
            onChange={() => setShowProb((value) => !value)}
            type="checkbox"
          />
          <span>Show probability heat under threshold</span>
        </label>

        <div className="insight">
          <div className="mono insight__title">What you&apos;re seeing</div>
          <p>{thresholdInsight(thresh)}</p>
          <p className="insight__note">{coverageLabel}</p>
        </div>
      </div>
    </div>
  );
}
