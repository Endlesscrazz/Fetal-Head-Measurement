import { STAGES } from "../../data/stages";
import type { Sample } from "../../types/sample";

export function PipelineStepper({
  activeIdx,
  onPick,
}: {
  activeIdx: number;
  onPick: (index: number) => void;
  sample: Sample;
}) {
  const progress = (activeIdx / (STAGES.length - 1)) * 100;

  return (
    <div className="pipeline-stepper">
      <div className="eyebrow">02 / Inside the pipeline</div>
      <h2 className="serif">How the model goes from pixels to millimetres.</h2>

      <div className="pipeline-stepper__track">
        <div className="pipeline-stepper__line" />
        <div className="pipeline-stepper__progress" style={{ width: `${progress}%` }} />
        {STAGES.map((stage, index) => {
          const active = index === activeIdx;
          const past = index < activeIdx;
          return (
            <button
              className={`${active ? "active" : ""} ${past ? "past" : ""}`}
              key={stage.id}
              onClick={() => onPick(index)}
              type="button"
            >
              <span className="mono pipeline-stepper__node">{String(index + 1).padStart(2, "0")}</span>
              <span className="pipeline-stepper__short">{stage.short}</span>
              <span className="mono pipeline-stepper__kind">
                {stage.id === "input"
                  ? "pixels"
                  : stage.id === "target"
                    ? "human"
                    : stage.id === "prob"
                      ? "p(skull)"
                      : stage.id === "mask"
                        ? "binary"
                        : stage.id === "ellipse"
                          ? "fit"
                          : "mm"}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
