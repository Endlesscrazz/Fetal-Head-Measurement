import { STAGES } from "../../data/stages";
import type { Sample } from "../../types/sample";

function stageFacts(sample: Sample) {
  return {
    input: [
      ["Source", `${sample.id}.png`],
      ["Channels", "1 (gray)"],
    ],
    target: [
      ["Origin", "Radiologist"],
      ["Role", "Ground truth"],
    ],
    prob: [
      ["Mean conf.", `${Math.round(sample.confidence * 100)}%`],
      ["Output", "P(skull) per pixel"],
    ],
    mask: [
      ["Threshold", "0.50"],
      ["Cleanup", "Fill / largest CC"],
    ],
    ellipse: [
      ["Method", "Least-squares"],
      ["Reject", "Non-elliptical drift"],
    ],
    hc: [
      ["Predicted HC", `${sample.metrics.predHC.toFixed(2)} mm`],
      ["Final error", `${sample.metrics.hcErr.toFixed(2)} mm`],
    ],
  } as const;
}

export function StageCaption({ sample, stageIdx }: { sample: Sample; stageIdx: number }) {
  const stage = STAGES[stageIdx];
  const facts = stageFacts(sample)[stage.id as keyof ReturnType<typeof stageFacts>] ?? stageFacts(sample).input;

  return (
    <aside className="caption">
      <div>
        <div className="mono caption__eyebrow">
          Stage {String(stageIdx + 1).padStart(2, "0")} of {String(STAGES.length).padStart(2, "0")}
        </div>
        <h2 className="serif caption__title">{stage.title}</h2>
      </div>

      <div className="caption__blurb-slot">
        <p>{stage.blurb}</p>
        <p className="caption__detail">{stage.detail}</p>
      </div>

      <div className="caption__facts">
        {facts.map(([label, value]) => (
          <div className="caption__fact" key={label}>
            <div className="mono caption__fact-label">{label}</div>
            <div className="mono caption__fact-value">{value}</div>
          </div>
        ))}
      </div>
    </aside>
  );
}
