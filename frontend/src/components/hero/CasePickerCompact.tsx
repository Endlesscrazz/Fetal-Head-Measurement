import type { Sample } from "../../types/sample";
import { getSampleAssets } from "../../utils/assets";

export function CasePickerCompact({
  activeId,
  onPick,
  samples,
}: {
  activeId: string;
  onPick: (id: string) => void;
  samples: Sample[];
}) {
  return (
    <div className="case-picker">
      <div className="mono case-picker__label">Active case · click to switch</div>
      <div className="case-picker__grid">
        {samples.map((sample) => {
          const active = sample.id === activeId;
          const assets = getSampleAssets(sample);
          const dotClass =
            sample.cat === "strong"
              ? "case-picker__dot case-picker__dot--strong"
              : sample.cat === "typical"
                ? "case-picker__dot case-picker__dot--typical"
                : "case-picker__dot case-picker__dot--failure";

          return (
            <button
              key={sample.id}
              className={`case-picker__item ${active ? "is-active" : ""}`}
              onClick={() => onPick(sample.id)}
              title={`${sample.id} · ${sample.label}`}
              type="button"
            >
              <img alt="" src={assets.ultrasound} />
              <span className={dotClass} />
            </button>
          );
        })}
      </div>
    </div>
  );
}
