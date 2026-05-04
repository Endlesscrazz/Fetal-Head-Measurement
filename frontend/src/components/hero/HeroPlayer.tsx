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
  onRestart: () => void;
  onSeek: (index: number) => void;
  playing: boolean;
  sample: Sample;
  samples: Sample[];
  stageIdx: number;
}) {
  return (
    <header className="hero-player">
      <div className="hero-player__title-row">
        <div className="hero-player__copy">
          <div className="hero-player__eyebrow">
            <svg aria-hidden="true" viewBox="0 0 24 24" width="20" height="20" fill="none">
              <ellipse cx="12" cy="12" rx="9" ry="6.5" stroke="var(--cyan)" strokeWidth="1.6" />
              <ellipse cx="12" cy="12" rx="5" ry="3.5" stroke="var(--cyan)" strokeWidth="1" opacity="0.5" />
              <circle cx="12" cy="12" r="1.4" fill="var(--cyan)" />
            </svg>
            <span className="mono">Fetal HC · Pipeline Explorer · v0.5</span>
          </div>
          <h1 className="serif">
            From a noisy ultrasound
            <br />
            to a number in millimetres,
            <br />
            <span>step by step.</span>
          </h1>
          <p>
            Press play to watch a CNN measure the head circumference of a fetus — six visible
            stages, no black boxes. Pick any case to drive the pipeline.
          </p>
          <div className="hero-player__active-meta">
            <CategoryBadge cat={sample.cat} size="sm" />
            <span className="mono">{sample.id}</span>
            <span>{sample.label}</span>
          </div>
        </div>

        <CasePickerCompact activeId={sample.id} onPick={onPickCase} samples={samples} />
      </div>

      <div className="hero-player__media-row">
        <MediaStage assets={assets} sample={sample} stageIdx={stageIdx} />
        <StageCaption sample={sample} stageIdx={stageIdx} />
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
    </header>
  );
}
