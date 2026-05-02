import { NAV_SECTIONS } from "./StickyNav";

const TOUR_COPY = [
  {
    title: "Pick a case",
    body: "Six real curated examples: strong, typical, and failure cases. The card you click drives every panel below.",
  },
  {
    title: "Inside the pipeline",
    body: "Step through the six stages: pixels, human target, model belief, binary mask, fitted geometry, and millimetres.",
  },
  {
    title: "The threshold",
    body: "The CNN outputs a probability per pixel. Drag the slider to feel the model commit from belief to a mask.",
  },
  {
    title: "Why geometry matters",
    body: "The next session expands this into the contour-vs-ellipse comparison that made the v1 post-processing story interesting.",
  },
  {
    title: "Numbers in context",
    body: "The metrics panel will translate overlap and millimetre error into phrases that are easy to explain in an interview.",
  },
  {
    title: "How we got here",
    body: "The research dashboard will summarize the real v1 runs and ablations behind this saved-output demo.",
  },
];

interface TourBarProps {
  step: number;
  total: number;
  onNext: () => void;
  onPrev: () => void;
  onExit: () => void;
}

export function TourBar({ step, total, onNext, onPrev, onExit }: TourBarProps) {
  const copy = TOUR_COPY[step] ?? TOUR_COPY[0];

  return (
    <div className="tour-bar">
      <div className="tour-bar__step">
        <span className="mono">{String(step + 1).padStart(2, "0")}</span>
      </div>
      <div>
        <div className="mono tour-bar__eyebrow">
          Step {step + 1} of {total} / {copy.title}
        </div>
        <div className="tour-bar__body">{copy.body}</div>
      </div>
      <div className="tour-bar__actions">
        <button disabled={step === 0} onClick={onPrev} type="button">
          Back
        </button>
        {step === NAV_SECTIONS.length - 1 ? (
          <button className="primary" onClick={onExit} type="button">
            Finish
          </button>
        ) : (
          <button className="primary" onClick={onNext} type="button">
            Next
          </button>
        )}
      </div>
    </div>
  );
}
