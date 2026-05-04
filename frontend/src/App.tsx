import { useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";

import { GeometryV2 } from "./components/geometry/GeometryV2";
import { HeroPlayer } from "./components/hero/HeroPlayer";
import { MethodSection } from "./components/method/MethodSection";
import { MetricsSection } from "./components/metrics/MetricsSection";
import { NavSectionId, SubNav } from "./components/nav/SubNav";
import { SafetyChip } from "./components/shared/SafetyChip";
import { ThresholdSection } from "./components/threshold/ThresholdSection";
import { loadManifest, preferredManifestPath } from "./data/samples";
import { STAGES } from "./data/stages";
import type { Manifest } from "./types/sample";
import { getSampleAssets } from "./utils/assets";

function Section({
  children,
  id,
}: {
  children: ReactNode;
  id: NavSectionId;
}) {
  return (
    <section className="page-section" id={id}>
      {children}
    </section>
  );
}

function App() {
  const [manifest, setManifest] = useState<Manifest | null>(null);
  const [activeId, setActiveId] = useState("");
  const [stageIdx, setStageIdx] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [mode, setMode] = useState<"replay" | "live">("replay");
  const [activeSection, setActiveSection] = useState<NavSectionId>("play");
  const [error, setError] = useState<string | null>(null);

  const loadingManifestPath = preferredManifestPath();

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

  const activeSample = useMemo(
    () => manifest?.samples.find((sample) => sample.id === activeId) ?? manifest?.samples[0],
    [activeId, manifest],
  );

  const assets = useMemo(
    () => (activeSample ? getSampleAssets(activeSample) : null),
    [activeSample],
  );

  useEffect(() => {
    if (!activeId) return;
    setStageIdx(0);
    setPlaying(false);
  }, [activeId]);

  useEffect(() => {
    if (!playing) return;
    const timer = window.setInterval(() => {
      setStageIdx((current) => {
        if (current >= STAGES.length - 1) {
          setPlaying(false);
          return current;
        }
        return current + 1;
      });
    }, 1300);

    return () => window.clearInterval(timer);
  }, [playing]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        const nextSection = visible[0]?.target.id as NavSectionId | undefined;
        if (nextSection) setActiveSection(nextSection);
      },
      { rootMargin: "-20% 0px -60% 0px", threshold: 0 },
    );

    (["play", "threshold", "geometry", "metrics", "method"] as NavSectionId[]).forEach((id) => {
      const element = document.getElementById(id);
      if (element) observer.observe(element);
    });

    return () => observer.disconnect();
  }, [manifest]);

  const jumpTo = (id: NavSectionId) => {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  if (error) {
    return (
      <main className="app-bg app-shell">
        <div className="shell">
          <section className="load-state">
            <div className="eyebrow">Manifest error</div>
            <p>{error}</p>
          </section>
        </div>
      </main>
    );
  }

  if (!manifest || !activeSample || !assets) {
    return (
      <main className="app-bg app-shell">
        <div className="shell">
          <section className="load-state">
            <div className="eyebrow">Loading</div>
            <p>Loading {loadingManifestPath}...</p>
          </section>
        </div>
      </main>
    );
  }

  return (
    <main className="app-bg app-shell">
      <SubNav
        active={activeSection}
        mode={mode}
        onJump={jumpTo}
        onModeToggle={() => setMode((current) => (current === "replay" ? "live" : "replay"))}
      />

      <div className="shell">
        <Section id="play">
          <HeroPlayer
            assets={assets}
            mode={mode}
            onNext={() => setStageIdx((current) => Math.min(STAGES.length - 1, current + 1))}
            onPause={() => setPlaying(false)}
            onPickCase={setActiveId}
            onPlay={() => {
              if (stageIdx >= STAGES.length - 1) setStageIdx(0);
              setPlaying(true);
            }}
            onPrev={() => setStageIdx((current) => Math.max(0, current - 1))}
            onRestart={() => {
              setPlaying(false);
              setStageIdx(0);
            }}
            onSeek={(index) => setStageIdx(index)}
            playing={playing}
            sample={activeSample}
            samples={manifest.samples}
            stageIdx={stageIdx}
          />
        </Section>

        <Section id="threshold">
          <ThresholdSection assets={assets} sample={activeSample} />
        </Section>

        <Section id="geometry">
          <GeometryV2 allSamples={manifest.samples} assets={assets} sample={activeSample} />
        </Section>

        <Section id="metrics">
          <MetricsSection sample={activeSample} />
        </Section>

        <Section id="method">
          <MethodSection />
        </Section>
      </div>

      <SafetyChip text={manifest.safety_text} />
    </main>
  );
}

export default App;
