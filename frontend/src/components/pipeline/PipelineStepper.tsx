import { STAGES } from "../../data/stages";

export function PipelineStepper({
  activeIdx,
  isPlaying,
  onPick,
  onRestart,
  onTogglePlay,
}: {
  activeIdx: number;
  isPlaying: boolean;
  onPick: (index: number) => void;
  onRestart: () => void;
  onTogglePlay: () => void;
}) {
  const activeStage = STAGES[activeIdx];
  const atEnd = activeIdx === STAGES.length - 1;
  const progress = (activeIdx / (STAGES.length - 1)) * 100;

  return (
    <div className="pipeline-stepper">
      <div className="eyebrow">02 / Inside the pipeline</div>
      <h2 className="serif">How the model goes from pixels to millimetres.</h2>
      <div className="pipeline-player">
        <button className={`pipeline-player__button ${isPlaying ? "active" : ""}`} onClick={onTogglePlay} type="button">
          {isPlaying ? "Pause walkthrough" : atEnd ? "Replay walkthrough" : "Play walkthrough"}
        </button>
        <div className="pipeline-player__scrub">
          <div className="pipeline-player__meta">
            <span className="mono">Stage {String(activeIdx + 1).padStart(2, "0")} of 06</span>
            <strong>{activeStage.title}</strong>
          </div>
          <input
            aria-label="Scrub pipeline stage"
            max={STAGES.length - 1}
            min={0}
            onChange={(event) => onPick(Number.parseInt(event.target.value, 10))}
            step={1}
            type="range"
            value={activeIdx}
          />
          <div className="pipeline-player__labels mono">
            {STAGES.map((stage) => (
              <span key={stage.id}>{stage.short}</span>
            ))}
          </div>
        </div>
        <button className="pipeline-player__ghost" onClick={onRestart} type="button">
          Restart
        </button>
      </div>

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
