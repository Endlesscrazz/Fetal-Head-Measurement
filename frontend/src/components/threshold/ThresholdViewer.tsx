import { useEffect, useMemo, useRef, useState } from "react";

import { sampleAssetPath } from "../../data/samples";
import type { Sample } from "../../types/sample";

function CustomSlider({
  value,
  onChange,
  min = 0,
  max = 1,
  step = 0.01,
}: {
  value: number;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
  step?: number;
}) {
  const pct = ((value - min) / (max - min)) * 100;

  return (
    <div className="custom-slider">
      <div className="custom-slider__rail" />
      <div className="custom-slider__fill" style={{ width: `${pct}%` }} />
      <input
        max={max}
        min={min}
        onChange={(event) => onChange(Number.parseFloat(event.target.value))}
        step={step}
        type="range"
        value={value}
      />
      <div className="custom-slider__thumb" style={{ left: `calc(${pct}% - 9px)` }} />
      <div className="custom-slider__labels mono">
        <span>0.00 / noisy</span>
        <span>tau = {value.toFixed(2)}</span>
        <span>1.00 / strict</span>
      </div>
    </div>
  );
}

function ThresholdHistogram({
  thresh,
  sample,
}: {
  thresh: number;
  sample: Sample;
}) {
  const bins = useMemo(() => computeBins(sample.id), [sample.id]);
  const max = Math.max(...bins, 1);

  return (
    <div className="threshold-histogram">
      <div className="mono threshold-histogram__label">Pixel probability distribution</div>
      <div className="threshold-histogram__bins">
        {bins.map((bin, index) => {
          const probability = index / bins.length;
          const above = probability > thresh;
          return (
            <div
              className={above ? "active" : ""}
              key={`${sample.id}-${index}`}
              style={{ height: `${(bin / max) * 100}%` }}
            />
          );
        })}
        <span className="threshold-histogram__marker" style={{ left: `${thresh * 100}%` }} />
      </div>
    </div>
  );
}

const binCache: Record<string, number[]> = {};

function computeBins(sampleId: string) {
  if (binCache[sampleId]) return binCache[sampleId];

  const bins = new Array<number>(40).fill(0);
  let seed = 0;
  for (let index = 0; index < sampleId.length; index += 1) {
    seed = (seed * 31 + sampleId.charCodeAt(index)) | 0;
  }
  let state = Math.abs(seed) || 7;
  const rand = () => {
    state = (state * 9301 + 49297) % 233280;
    return state / 233280;
  };

  for (let index = 0; index < bins.length; index += 1) {
    const x = index / bins.length;
    const bg = Math.exp(-((x - 0.05) * (x - 0.05)) / 0.005) * 800;
    const fg = Math.exp(-((x - 0.85) * (x - 0.85)) / 0.01) * 220;
    const mid = Math.exp(-((x - 0.4) * (x - 0.4)) / 0.05) * 30;
    bins[index] = bg + fg + mid + rand() * 30;
  }

  binCache[sampleId] = bins;
  return bins;
}

export function ThresholdViewer({ sample }: { sample: Sample }) {
  const [thresh, setThresh] = useState(0.5);
  const [showProb, setShowProb] = useState(false);
  const [decodeTick, setDecodeTick] = useState(0);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const probDataRef = useRef<ImageData | null>(null);
  const ultrasoundRef = useRef<HTMLImageElement | null>(null);
  const width = sample.resolution.w;
  const height = sample.resolution.h;

  useEffect(() => {
    let cancelled = false;
    probDataRef.current = null;
    ultrasoundRef.current = null;

    const probImg = new Image();
    probImg.onload = () => {
      if (cancelled) return;
      const canvas = document.createElement("canvas");
      canvas.width = width;
      canvas.height = height;
      const ctx = canvas.getContext("2d");
      if (!ctx) return;
      ctx.drawImage(probImg, 0, 0, width, height);
      probDataRef.current = ctx.getImageData(0, 0, width, height);
      setDecodeTick((tick) => tick + 1);
    };
    probImg.src = sampleAssetPath(sample.id, "prob");

    const ultrasound = new Image();
    ultrasound.onload = () => {
      if (cancelled) return;
      ultrasoundRef.current = ultrasound;
      setDecodeTick((tick) => tick + 1);
    };
    ultrasound.src = sampleAssetPath(sample.id, "ultrasound");

    return () => {
      cancelled = true;
    };
  }, [height, sample.id, width]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const probData = probDataRef.current;
    const ultrasound = ultrasoundRef.current;
    if (!canvas || !probData || !ultrasound) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.drawImage(ultrasound, 0, 0, width, height);
    const layer = ctx.getImageData(0, 0, width, height);
    const probPixels = probData.data;
    const out = layer.data;
    const edge = 0.04;

    for (let index = 0; index < probPixels.length; index += 4) {
      const probability = probPixels[index] / 255;
      if (showProb) {
        const alpha = probability * 0.55;
        out[index] = Math.min(255, out[index] + 110 * alpha);
        out[index + 1] = Math.min(255, out[index + 1] + 224 * alpha);
        out[index + 2] = Math.min(255, out[index + 2] + 255 * alpha);
      } else {
        const alpha =
          probability > thresh + edge
            ? 0.55
            : probability > thresh - edge
              ? 0.55 * ((probability - (thresh - edge)) / (2 * edge))
              : 0;
        if (alpha > 0) {
          out[index] = Math.min(255, out[index] + 110 * alpha);
          out[index + 1] = Math.min(255, out[index + 1] + 224 * alpha);
          out[index + 2] = Math.min(255, out[index + 2] + 255 * alpha);
        }
      }
    }

    ctx.putImageData(layer, 0, 0);
  }, [decodeTick, height, showProb, thresh, width]);

  const stats = useMemo(() => {
    const data = probDataRef.current?.data;
    if (!data) return { coverage: 0, pixels: 0 };
    let count = 0;
    for (let index = 0; index < data.length; index += 4) {
      if (data[index] / 255 > thresh) count += 1;
    }
    return { coverage: count / (width * height), pixels: count };
  }, [decodeTick, height, sample.id, thresh, width]);

  const insight =
    thresh < 0.25
      ? "A low threshold trusts almost every pixel. The mask leaks into noisy tissue."
      : thresh < 0.55
        ? "Around 0.5 the model commits to its strongest beliefs: the default operating point."
        : thresh < 0.8
          ? "Higher thresholds keep only the very confident pixels, so the skull shrinks inward."
          : "A near-1.0 threshold rejects almost everything; only peak-confidence pixels survive.";

  return (
    <div className="threshold-viewer">
      <div>
        <div className="threshold-canvas" style={{ aspectRatio: `${width} / ${height}` }}>
          <canvas ref={canvasRef} width={width} height={height} />
          <div className="threshold-canvas__badge mono">
            {showProb ? "Probability map" : `Threshold = ${thresh.toFixed(2)}`}
          </div>
        </div>
        <ThresholdHistogram sample={sample} thresh={thresh} />
      </div>

      <div className="threshold-viewer__controls">
        <div>
          <div className="eyebrow">03 / Threshold to mask</div>
          <h3 className="serif">Drag to watch the model commit.</h3>
        </div>
        <p>
          The CNN does not output a mask. It outputs a belief for every pixel, and the threshold
          turns that belief into a binary decision.
        </p>
        <CustomSlider value={thresh} onChange={setThresh} />
        <div className="threshold-stats">
          <div>
            <div className="mono">Coverage</div>
            <strong className="mono">{(stats.coverage * 100).toFixed(1)}%</strong>
          </div>
          <div>
            <div className="mono">Pixels above tau</div>
            <strong className="mono">{stats.pixels.toLocaleString()}</strong>
          </div>
        </div>
        <div className="threshold-actions">
          <button className={showProb ? "active" : ""} onClick={() => setShowProb((value) => !value)} type="button">
            {showProb ? "Showing P(skull)" : "Show P(skull) heat"}
          </button>
          <button onClick={() => setThresh(0.5)} type="button">
            Reset 0.50
          </button>
        </div>
        <div className="threshold-insight">
          <div className="mono">What you are seeing</div>
          {insight}
        </div>
      </div>
    </div>
  );
}
