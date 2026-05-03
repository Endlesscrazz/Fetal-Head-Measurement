import { useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";

import { ExperimentDashboard } from "./components/experiments/ExperimentDashboard";
import { SampleGallery, type GalleryFilter } from "./components/gallery/SampleGallery";
import { ContourEllipse } from "./components/geometry/ContourEllipse";
import { Hero } from "./components/hero/Hero";
import { MetricsPanel } from "./components/metrics/MetricsPanel";
import { NAV_SECTIONS, StickyNav, type NavSectionId } from "./components/nav/StickyNav";
import { TourBar } from "./components/nav/TourBar";
import { PipelineStepper } from "./components/pipeline/PipelineStepper";
import { StageDetail } from "./components/pipeline/StageDetail";
import { SafetyChip } from "./components/shared/SafetyChip";
import { ThresholdViewer } from "./components/threshold/ThresholdViewer";
import { loadManifest } from "./data/samples";
import type { Manifest, Sample } from "./types/sample";

function formatMm(value: number): string {
  return `${value.toFixed(2)} mm`;
}

function Section({
  id,
  children,
  className,
}: {
  id: NavSectionId;
  children: ReactNode;
  className?: string;
}) {
  return (
    <section className={`page-section ${className ?? ""}`} id={id}>
      {children}
    </section>
  );
}

function Vital({ label, value, accent }: { label: string; value: string; accent?: boolean }) {
  return (
    <div className="active-strip__vital">
      <div className="mono">{label}</div>
      <strong className="mono" style={{ color: accent ? "var(--cyan)" : "var(--fg-0)" }}>
        {value}
      </strong>
    </div>
  );
}

function ActiveSampleStrip({ sample }: { sample: Sample }) {
  return (
    <div className="active-strip">
      <div>
        <div className="mono active-strip__eyebrow">
          {sample.id} / split {sample.split}
        </div>
        <div className="serif active-strip__title">{sample.label}</div>
      </div>
      <div className="active-strip__metrics">
        <Vital label="Pred HC" value={formatMm(sample.metrics.predHC)} />
        <Vital label="Target HC" value={formatMm(sample.metrics.targetHC)} />
        <Vital label="HC error" value={formatMm(sample.metrics.hcErr)} accent />
        <Vital label="Dice" value={sample.metrics.dice.toFixed(4)} />
      </div>
    </div>
  );
}

function App() {
  const [manifest, setManifest] = useState<Manifest | null>(null);
  const [activeId, setActiveId] = useState<string>("");
  const [filter, setFilter] = useState<GalleryFilter>("all");
  const [stageIdx, setStageIdx] = useState(0);
  const [activeSection, setActiveSection] = useState<NavSectionId>("cases");
  const [tourActive, setTourActive] = useState(false);
  const [tourStep, setTourStep] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const loadingManifestPath =
    typeof window !== "undefined" &&
    window.location.hostname !== "localhost" &&
    window.location.hostname !== "127.0.0.1"
      ? "/demo-samples/manifest.json"
      : "/samples/manifest.json";

  useEffect(() => {
    let cancelled = false;

    loadManifest()
      .then((nextManifest) => {
        if (cancelled) return;
        setManifest(nextManifest);
        setActiveId(nextManifest.samples[0]?.id ?? "");
      })
      .catch((nextError: unknown) => {
        if (cancelled) return;
        setError(nextError instanceof Error ? nextError.message : String(nextError));
      });

    return () => {
      cancelled = true;
    };
  }, []);

  const activeSample = useMemo<Sample | undefined>(
    () => manifest?.samples.find((sample) => sample.id === activeId),
    [activeId, manifest],
  );

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        const first = visible[0]?.target.id;
        if (first && NAV_SECTIONS.some((section) => section.id === first)) {
          setActiveSection(first as NavSectionId);
        }
      },
      { rootMargin: "-20% 0px -60% 0px", threshold: 0 },
    );

    NAV_SECTIONS.forEach((section) => {
      const element = document.getElementById(section.id);
      if (element) observer.observe(element);
    });

    return () => observer.disconnect();
  }, [manifest]);

  useEffect(() => {
    if (!activeId) return;
    setStageIdx(0);
    let index = 0;
    const timer = window.setInterval(() => {
      index += 1;
      if (index >= 3) {
        window.clearInterval(timer);
        return;
      }
      setStageIdx(index);
    }, 220);

    return () => window.clearInterval(timer);
  }, [activeId]);

  const jumpTo = (id: NavSectionId) => {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const startTour = () => {
    setTourActive(true);
    setTourStep(0);
    window.setTimeout(() => jumpTo(NAV_SECTIONS[0].id), 50);
  };

  const exitTour = () => setTourActive(false);

  const nextTourStep = () => {
    const next = Math.min(tourStep + 1, NAV_SECTIONS.length - 1);
    setTourStep(next);
    jumpTo(NAV_SECTIONS[next].id);
  };

  const prevTourStep = () => {
    const next = Math.max(tourStep - 1, 0);
    setTourStep(next);
    jumpTo(NAV_SECTIONS[next].id);
  };

  return (
    <main className="app-bg app-shell">
      <StickyNav
        active={activeSection}
        onJump={jumpTo}
        onTourToggle={() => (tourActive ? exitTour() : startTour())}
        tourActive={tourActive}
      />

      <div className="shell">
        {error && (
          <section className="card load-state load-state--error">
            <div className="eyebrow">Manifest error</div>
            <p>{error}</p>
          </section>
        )}

        {!manifest && !error && (
          <section className="card load-state">
            <div className="eyebrow">Loading</div>
            <p>Loading {loadingManifestPath}...</p>
          </section>
        )}

        {manifest && activeSample && (
          <>
            <Hero activeSample={activeSample} onStartTour={startTour} sampleCount={manifest.samples.length} />

            <Section id="cases">
              <SampleGallery
                activeId={activeId}
                filter={filter}
                onFilterChange={setFilter}
                onPick={setActiveId}
                samples={manifest.samples}
              />
            </Section>

            <div className="active-strip-wrap">
              <ActiveSampleStrip sample={activeSample} />
            </div>

            <Section id="pipeline">
              <PipelineStepper activeIdx={stageIdx} onPick={setStageIdx} sample={activeSample} />
              <div className="pipeline-detail-wrap">
                <StageDetail sample={activeSample} stageIdx={stageIdx} />
              </div>
            </Section>

            <Section id="threshold">
              <div className="card threshold-card">
                <ThresholdViewer sample={activeSample} />
              </div>
            </Section>

            <Section id="geometry">
              <ContourEllipse sample={activeSample} />
            </Section>

            <Section id="metrics">
              <MetricsPanel sample={activeSample} />
            </Section>

            <Section className="research-section" id="research">
              <ExperimentDashboard />
            </Section>

            <footer className="footer-strip">
              <span className="mono">HC18 dataset / {manifest.created_from_run_id} / saved-output mode</span>
              <span className="mono">Built for explanation, not diagnosis.</span>
            </footer>
          </>
        )}
      </div>

      {tourActive && (
        <TourBar
          onExit={exitTour}
          onNext={nextTourStep}
          onPrev={prevTourStep}
          step={tourStep}
          total={NAV_SECTIONS.length}
        />
      )}

      <SafetyChip text={manifest?.safety_text ?? "Educational demo only. Not for clinical use."} />
    </main>
  );
}

export default App;
