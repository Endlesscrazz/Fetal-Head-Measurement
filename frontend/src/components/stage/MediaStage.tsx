import { STAGES } from "../../data/stages";
import type { Sample } from "../../types/sample";
import type { SampleAssets } from "../../utils/assets";
import { EllipseLayer } from "./EllipseLayer";
import { Outline } from "./Outline";
import { ProbabilityViz } from "./ProbabilityViz";

export function MediaStage({
  assets,
  sample,
  stageIdx,
}: {
  assets: SampleAssets;
  sample: Sample;
  stageIdx: number;
}) {
  const stage = STAGES[stageIdx];
  const showTarget = stage.id === "target";
  const showProb = stage.id === "prob";
  const showMask = stage.id === "mask";
  const showEllipse = stage.id === "ellipse" || stage.id === "hc";
  const showHC = stage.id === "hc";

  return (
    <div className="stage" data-stage={stage.id}>
      <img
        alt={`${sample.id} ultrasound`}
        className="layer fade-in stage__image"
        src={assets.ultrasound}
        style={{
          filter: stage.id === "input" ? "none" : "brightness(0.78) contrast(1.05)",
        }}
      />

      <Outline
        height={sample.resolution.h}
        src={assets.target}
        stroke="#6ee0ff"
        visible={showTarget}
        width={sample.resolution.w}
      />
      <ProbabilityViz probSrc={assets.prob} sample={sample} visible={showProb} />
      <Outline
        fill="rgba(110,224,255,0.10)"
        height={sample.resolution.h}
        src={assets.pred}
        stroke="#6ee0ff"
        visible={showMask}
        width={sample.resolution.w}
      />
      <EllipseLayer
        ellipse={sample.predEllipse}
        hcMm={sample.metrics.predHC}
        height={sample.resolution.h}
        showHC={showHC}
        visible={showEllipse}
        width={sample.resolution.w}
      />

      <div className="stage__top-left">
        <div className="status-pill stage__chip">
          <span style={{ color: "var(--cyan)", fontWeight: 600 }}>
            {String(stageIdx + 1).padStart(2, "0")}
          </span>
          <span>{stage.title}</span>
        </div>
      </div>

      <div className="stage__top-right">
        <div className="status-pill stage__chip">{sample.id}</div>
      </div>

      <div className="scale-ticks">
        <span className="swatch" />
        <span>10 mm</span>
      </div>
    </div>
  );
}
