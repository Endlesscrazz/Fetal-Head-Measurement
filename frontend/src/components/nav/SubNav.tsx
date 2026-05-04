export type NavSectionId = "play" | "threshold" | "geometry" | "metrics" | "method";

const SECTIONS: { id: NavSectionId; label: string; n: string }[] = [
  { id: "play", label: "Play", n: "01" },
  { id: "threshold", label: "Threshold", n: "02" },
  { id: "geometry", label: "Geometry", n: "03" },
  { id: "metrics", label: "Metrics", n: "04" },
  { id: "method", label: "Method", n: "05" },
];

export function SubNav({
  active,
  mode,
  onJump,
  onModeToggle,
}: {
  active: NavSectionId;
  mode: "replay" | "live";
  onJump: (id: NavSectionId) => void;
  onModeToggle: () => void;
}) {
  return (
    <div className="subnav">
      <div className="subnav__inner">
        <div className="subnav__brand">
          <svg aria-hidden="true" viewBox="0 0 24 24" width="16" height="16" fill="none">
            <ellipse cx="12" cy="12" rx="9" ry="6.5" stroke="var(--cyan)" strokeWidth="1.6" />
            <circle cx="12" cy="12" r="1.4" fill="var(--cyan)" />
          </svg>
          <span className="mono">HC Explorer</span>
        </div>

        <nav className="subnav__pills" aria-label="Sections">
          {SECTIONS.map((section) => {
            const activeSection = active === section.id;
            return (
              <button
                key={section.id}
                className={activeSection ? "active" : undefined}
                onClick={() => onJump(section.id)}
                type="button"
              >
                <span>{section.n}</span>
                {section.label}
              </button>
            );
          })}
        </nav>

        <button className="status-pill status-pill--toggle" onClick={onModeToggle} type="button">
          <span className={`led ${mode === "live" ? "led--cyan" : "led--good"}`} />
          {mode === "live" ? "Live · preview" : "Saved · v1"}
        </button>
      </div>
    </div>
  );
}
