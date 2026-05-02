export const NAV_SECTIONS = [
  { id: "cases", label: "Cases", n: "01" },
  { id: "pipeline", label: "Pipeline", n: "02" },
  { id: "threshold", label: "Threshold", n: "03" },
  { id: "geometry", label: "Geometry", n: "04" },
  { id: "metrics", label: "Metrics", n: "05" },
  { id: "research", label: "Research", n: "06" },
] as const;

export type NavSectionId = (typeof NAV_SECTIONS)[number]["id"];

interface StickyNavProps {
  active: string;
  tourActive: boolean;
  onJump: (id: NavSectionId) => void;
  onTourToggle: () => void;
}

export function StickyNav({ active, tourActive, onJump, onTourToggle }: StickyNavProps) {
  return (
    <div className="sticky-nav">
      <div className="sticky-nav__inner">
        <div className="sticky-nav__brand">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <ellipse cx="12" cy="12" rx="9" ry="6.5" stroke="var(--cyan)" strokeWidth="1.6" />
            <circle cx="12" cy="12" r="1.4" fill="var(--cyan)" />
          </svg>
          <span className="mono">HC Explorer</span>
        </div>

        <nav className="sticky-nav__pills" aria-label="Page sections">
          {NAV_SECTIONS.map((section) => (
            <button
              className={active === section.id ? "active" : ""}
              key={section.id}
              onClick={() => onJump(section.id)}
              type="button"
            >
              <span>{section.n}</span>
              {section.label}
            </button>
          ))}
        </nav>

        <button
          className={`tour-toggle ${tourActive ? "active" : ""}`}
          onClick={onTourToggle}
          type="button"
        >
          {tourActive ? "Exit tour" : "Take the tour"}
        </button>
      </div>
    </div>
  );
}
