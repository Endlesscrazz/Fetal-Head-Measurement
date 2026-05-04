import { CategoryBadge } from "../shared/CategoryBadge";
import { CasePickerCompact } from "./CasePickerCompact";
import { StageCaption } from "./StageCaption";
import { MediaStage } from "../stage/MediaStage";
import { Transport } from "../transport/Transport";
import type { Sample } from "../../types/sample";
import type { SampleAssets } from "../../utils/assets";
import { STAGES } from "../../data/stages";

export function HeroPlayer({
  assets,
  mode,
  onNext,
  onPause,
  onPickCase,
  onPlay,
  onPrev,
  onReadMethod,
  onRestart,
  onSeek,
  playing,
  sample,
  samples,
  stageIdx,
}: {
  assets: SampleAssets;
  mode: "replay" | "live";
  onNext: () => void;
  onPause: () => void;
  onPickCase: (id: string) => void;
  onPlay: () => void;
  onPrev: () => void;
  onReadMethod: () => void;
  onRestart: () => void;
  onSeek: (index: number) => void;
  playing: boolean;
  sample: Sample;
  samples: Sample[];
  stageIdx: number;
}) {
  const stage = STAGES[stageIdx];
  return (
    <header className="hero-player">
      <div className="hero-player__shell">
        <div className="hero-player__media-row">
          <MediaStage assets={assets} sample={sample} stageIdx={stageIdx} />
          <div className="hero-player__aside">
            <StageCaption onPlayPipeline={onPlay} onReadMethod={onReadMethod} sample={sample} />
            <div className="hero-player__aside-footer">
              <CasePickerCompact activeId={sample.id} onPick={onPickCase} samples={samples} />
            </div>
          </div>
        </div>

        <div className="hero-player__transport">
          <Transport
            mode={mode === "replay" ? "replay" : "live"}
            onNext={onNext}
            onPause={onPause}
            onPlay={onPlay}
            onPrev={onPrev}
            onRestart={onRestart}
            onSeek={onSeek}
            playing={playing}
            stageIdx={stageIdx}
            timing={mode === "replay" ? { label: "Saved-output replay", value: "12 ms / stage" } : null}
            total={STAGES.length}
          />
        </div>

        <div className="hero-player__telemetry">
          <span className="mono">
            Stage <strong>{String(stageIdx + 1).padStart(2, "0")}</strong> / {String(STAGES.length).padStart(2, "0")}{" "}
            {stage.short}
          </span>
          <span className="mono">Case {sample.id}</span>
          <span className="mono">
            Confidence <strong>{Math.round(sample.confidence * 100)}%</strong>
          </span>
          <span className="mono">
            Dice <strong>{sample.metrics.dice.toFixed(4)}</strong>
          </span>
          <span className="mono">
            IoU <strong>{sample.metrics.iou.toFixed(4)}</strong>
          </span>
          <span className="mono">
            HC error <strong>{sample.metrics.hcErr.toFixed(2)} mm</strong>
          </span>
          <span className="mono">
            Pred HC <strong>{sample.metrics.predHC.toFixed(2)} mm</strong>
          </span>
        </div>
      </div>

      <div className="hero-player__meta">
        <div className="hero-player__brandmark">
          <svg aria-hidden="true" viewBox="0 0 24 24" width="20" height="20" fill="none">
            <ellipse cx="12" cy="12" rx="9" ry="6.5" stroke="var(--cyan)" strokeWidth="1.6" />
            <ellipse cx="12" cy="12" rx="5" ry="3.5" stroke="var(--cyan)" strokeWidth="1" opacity="0.5" />
            <circle cx="12" cy="12" r="1.4" fill="var(--cyan)" />
          </svg>
          <span className="serif">Cephal</span>
          <span className="mono hero-player__brandline">Pipeline Explorer · v0.5</span>
        </div>
        <div className="hero-player__active-meta">
          <CategoryBadge cat={sample.cat} size="sm" />
          <span className="mono">{sample.label}</span>
        </div>
      </div>
    </header>
  );
}
