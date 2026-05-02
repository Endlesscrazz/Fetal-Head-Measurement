import { CategoryBadge } from "../shared/CategoryBadge";
import { sampleAssetPath } from "../../data/samples";
import type { Sample, SampleCategory } from "../../types/sample";

export type GalleryFilter = "all" | SampleCategory;

function SampleCard({ sample, active, onClick }: { sample: Sample; active: boolean; onClick: () => void }) {
  const errorColor =
    sample.metrics.hcErr < 0.5 ? "var(--good)" : sample.metrics.hcErr < 3 ? "var(--cyan)" : "var(--amber)";

  return (
    <button className={`sample-card ${active ? "active" : ""}`} onClick={onClick} type="button">
      <div className="sample-card__thumb">
        <img alt={`${sample.id} ultrasound`} src={sampleAssetPath(sample.id, "ultrasound")} />
        <div
          className="sample-card__mask"
          style={{ backgroundImage: `url(${sampleAssetPath(sample.id, "pred")})` }}
        />
        <div className="sample-card__badge">
          <CategoryBadge cat={sample.cat} size="sm" />
        </div>
        {active && <div className="sample-card__active-dot" />}
      </div>
      <div>
        <div className="mono sample-card__id">
          {sample.id} / {sample.split.toUpperCase()}
        </div>
        <div className="sample-card__label">{sample.label}</div>
      </div>
      <div className="sample-card__metric">
        <span className="mono">HC error</span>
        <strong className="mono" style={{ color: errorColor }}>
          {sample.metrics.hcErr.toFixed(2)}
          <span> mm</span>
        </strong>
      </div>
    </button>
  );
}

export function SampleGallery({
  samples,
  activeId,
  filter,
  onPick,
  onFilterChange,
}: {
  samples: Sample[];
  activeId: string;
  filter: GalleryFilter;
  onPick: (id: string) => void;
  onFilterChange: (filter: GalleryFilter) => void;
}) {
  const filtered = filter === "all" ? samples : samples.filter((sample) => sample.cat === filter);
  const filters: GalleryFilter[] = ["all", "strong", "typical", "failure"];

  return (
    <div className="gallery">
      <div className="section-heading">
        <div>
          <div className="eyebrow">01 / Pick a case</div>
          <h2 className="serif">Six curated examples: successes, typical cases, and failures.</h2>
        </div>
        <div className="gallery__filters" role="tablist" aria-label="Sample filters">
          {filters.map((nextFilter) => (
            <button
              className={filter === nextFilter ? "active" : ""}
              key={nextFilter}
              onClick={() => onFilterChange(nextFilter)}
              type="button"
            >
              {nextFilter === "all" ? `All ${samples.length}` : nextFilter}
            </button>
          ))}
        </div>
      </div>
      <div className="gallery__cards">
        {filtered.map((sample) => (
          <SampleCard
            active={sample.id === activeId}
            key={sample.id}
            onClick={() => onPick(sample.id)}
            sample={sample}
          />
        ))}
      </div>
    </div>
  );
}
