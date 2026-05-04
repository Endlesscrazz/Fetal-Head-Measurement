import { useEffect, useMemo, useRef } from "react";

import type { Sample } from "../../types/sample";

const ISO_LEVELS = [
  { value: 0.3, rgba: [255, 180, 84, 110] as const, label: "0.30", swatch: "#ffb454" },
  { value: 0.5, rgba: [110, 224, 255, 200] as const, label: "0.50", swatch: "#6ee0ff" },
  { value: 0.75, rgba: [110, 224, 255, 230] as const, label: "0.75", swatch: "#aaeeff" },
  { value: 0.92, rgba: [255, 255, 255, 240] as const, label: "0.92", swatch: "#ffffff" },
];

export function ProbabilityViz({
  probSrc,
  sample,
  visible,
}: {
  probSrc: string;
  sample: Sample;
  visible: boolean;
}) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    let cancelled = false;
    const canvas = canvasRef.current;
    if (!canvas) return;

    const image = new Image();
    image.onload = () => {
      if (cancelled) return;

      const { w: width, h: height } = sample.resolution;
      const offscreen = document.createElement("canvas");
      offscreen.width = width;
      offscreen.height = height;
      const offscreenCtx = offscreen.getContext("2d", { willReadFrequently: true });
      const ctx = canvas.getContext("2d", { willReadFrequently: true });
      if (!offscreenCtx || !ctx) return;

      offscreenCtx.clearRect(0, 0, width, height);
      offscreenCtx.drawImage(image, 0, 0, width, height);
      const data = offscreenCtx.getImageData(0, 0, width, height);
      const output = ctx.createImageData(width, height);
      const idx = (x: number, y: number) => (y * width + x) * 4;

      for (const level of ISO_LEVELS) {
        const threshold = Math.floor(level.value * 255);
        for (let y = 1; y < height - 1; y += 1) {
          for (let x = 1; x < width - 1; x += 1) {
            const i = idx(x, y);
            const value = data.data[i];
            if (value < threshold) continue;

            const north = data.data[idx(x, y - 1)];
            const south = data.data[idx(x, y + 1)];
            const east = data.data[idx(x + 1, y)];
            const west = data.data[idx(x - 1, y)];

            if (north < threshold || south < threshold || east < threshold || west < threshold) {
              if (output.data[i + 3] < level.rgba[3]) {
                output.data[i] = level.rgba[0];
                output.data[i + 1] = level.rgba[1];
                output.data[i + 2] = level.rgba[2];
                output.data[i + 3] = level.rgba[3];
              }
            }
          }
        }
      }

      canvas.width = width;
      canvas.height = height;
      ctx.clearRect(0, 0, width, height);
      ctx.putImageData(output, 0, 0);
    };

    image.src = probSrc;
    return () => {
      cancelled = true;
    };
  }, [probSrc, sample.resolution]);

  const reticleStyle = useMemo(() => {
    const ellipse = sample.predEllipse;
    const { w, h } = sample.resolution;
    return {
      left: `${((ellipse.cx - ellipse.rx - 12) / w) * 100}%`,
      top: `${((ellipse.cy - ellipse.ry - 12) / h) * 100}%`,
      width: `${((ellipse.rx * 2 + 24) / w) * 100}%`,
      height: `${((ellipse.ry * 2 + 24) / h) * 100}%`,
    };
  }, [sample.predEllipse, sample.resolution]);

  return (
    <>
      <canvas
        ref={canvasRef}
        className={`layer probability-viz ${visible ? "fade-in" : "fade-out"}`}
      />
      <div className={`layer probability-viz__ui ${visible ? "fade-in" : "fade-out"}`}>
        <div className="focus-reticle" style={reticleStyle} />
        <div className="probability-viz__legend">
          <div className="mono probability-viz__legend-title">Iso-P levels</div>
          {ISO_LEVELS.map((level) => (
            <div className="probability-viz__legend-row" key={level.label}>
              <span style={{ background: level.swatch, boxShadow: `0 0 4px ${level.swatch}` }} />
              {level.label}
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
