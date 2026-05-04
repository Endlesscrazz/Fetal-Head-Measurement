import type { Sample } from "../../types/sample";
import { ArcCard } from "./ArcCard";
import { BarCard } from "./BarCard";

export function MetricsSection({ sample }: { sample: Sample }) {
  return (
    <section className="metrics-section">
      <div className="section-heading">
        <div>
          <div className="eyebrow">04 / Metrics in human terms</div>
          <h2 className="serif section-title">What these numbers actually mean.</h2>
        </div>
      </div>

      <div className="metrics-grid">
        <ArcCard metricKey="dice" value={sample.metrics.dice} />
        <ArcCard metricKey="iou" value={sample.metrics.iou} />
        <BarCard max={10} metricKey="hcErr" unit="mm" value={sample.metrics.hcErr} />
        <BarCard max={10} metricKey="hd95_mm" unit="mm" value={sample.metrics.hd95_mm} />
      </div>
    </section>
  );
}
