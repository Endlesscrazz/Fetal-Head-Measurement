import { STAGES } from "../../data/stages";

export function Transport({
  mode,
  onNext,
  onPause,
  onPlay,
  onPrev,
  onRestart,
  onSeek,
  playing,
  stageIdx,
  timing,
  total,
}: {
  mode: "replay" | "live" | "computing";
  onNext: () => void;
  onPause: () => void;
  onPlay: () => void;
  onPrev: () => void;
  onRestart: () => void;
  onSeek: (index: number) => void;
  playing: boolean;
  stageIdx: number;
  timing?: { label: string; value: string } | null;
  total: number;
}) {
  const stage = STAGES[stageIdx];
  const pct = total > 1 ? (stageIdx / (total - 1)) * 100 : 0;

  return (
    <div className="transport" role="group" aria-label="Pipeline transport">
      <div className="transport__controls">
        <button className="transport-btn ghost" aria-label="Restart" onClick={onRestart} type="button">
          <svg fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24" width="14" height="14">
            <path d="M3 12a9 9 0 1 0 3-6.7L3 8" />
            <path d="M3 4v4h4" />
          </svg>
        </button>
        <button
          aria-label="Previous stage"
          className="transport-btn ghost"
          disabled={stageIdx === 0}
          onClick={onPrev}
          type="button"
        >
          <svg fill="currentColor" viewBox="0 0 24 24" width="12" height="12">
            <path d="M19 5v14L7 12z M5 5h2v14H5z" />
          </svg>
        </button>
        <button
          aria-label={playing ? "Pause" : "Play"}
          className="transport-btn primary"
          onClick={playing ? onPause : onPlay}
          type="button"
        >
          {playing ? (
            <svg fill="currentColor" viewBox="0 0 24 24" width="14" height="14">
              <rect x="6" y="5" width="4" height="14" />
              <rect x="14" y="5" width="4" height="14" />
            </svg>
          ) : (
            <svg fill="currentColor" viewBox="0 0 24 24" width="14" height="14">
              <path d="M7 5l12 7-12 7z" />
            </svg>
          )}
        </button>
        <button
          aria-label="Next stage"
          className="transport-btn ghost"
          disabled={stageIdx === total - 1}
          onClick={onNext}
          type="button"
        >
          <svg fill="currentColor" viewBox="0 0 24 24" width="12" height="12">
            <path d="M5 5l12 7-12 7z M17 5h2v14h-2z" />
          </svg>
        </button>
      </div>

      <div className="tickrail">
        <div className="tickrail__track">
          <div className="tickrail__fill" style={{ width: `${pct}%` }} />
        </div>
        <div className="tickrail__stops">
          {STAGES.map((entry, index) => {
            const passed = index < stageIdx;
            const active = index === stageIdx;
            return (
              <button
                key={entry.id}
                className={`tickrail__stop ${passed ? "passed" : ""} ${active ? "active" : ""}`}
                onClick={() => onSeek(index)}
                type="button"
              >
                <span className="dot" />
                <span>{entry.short}</span>
              </button>
            );
          })}
        </div>
      </div>

      <div className="transport__right-cluster">
        <div className={`status-pill status-pill--mode status-pill--${mode}`}>
          <span className="led" />
          {mode === "replay" ? "Saved · v1" : mode === "computing" ? "Computing" : "Live"}
        </div>
        {timing && (
          <div className="status-pill" title={timing.label}>
            {timing.value}
          </div>
        )}
        <span className="mono transport__counter">
          {String(stageIdx + 1).padStart(2, "0")} / {String(total).padStart(2, "0")} · {stage.short}
        </span>
      </div>
    </div>
  );
}
