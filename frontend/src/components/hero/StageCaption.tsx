import type { Sample } from "../../types/sample";

export function StageCaption({
  onPlayPipeline,
  onReadMethod,
  sample,
}: {
  onPlayPipeline: () => void;
  onReadMethod: () => void;
  sample: Sample;
}) {
  return (
    <aside className="caption caption--hero">
      <div>
        <div className="mono caption__eyebrow caption__eyebrow--hero">
          <span className="caption__eyebrow-dot" />
          From ultrasound to millimetres
        </div>
        <h2 className="serif caption__title caption__title--hero">
          A working CNN, explained <span>one stage at a time.</span>
        </h2>
      </div>

      <div className="caption__blurb-slot caption__blurb-slot--hero">
        <p>
          Six visible stages. No black boxes. Press play and watch the network measure a fetal head
          circumference from a noisy 2D ultrasound.
        </p>
        <p className="caption__detail">
          Active case <span className="mono">{sample.id}</span> · {Math.round(sample.confidence * 100)}%
          confidence · Dice {sample.metrics.dice.toFixed(4)}
        </p>
      </div>

      <div className="caption__actions">
        <button className="hero-action hero-action--primary" onClick={onPlayPipeline} type="button">
          <span className="hero-action__icon" aria-hidden="true">
            ▶
          </span>
          Play pipeline
        </button>
        <button className="hero-action hero-action--ghost" onClick={onReadMethod} type="button">
          Read method
        </button>
      </div>
    </aside>
  );
}
