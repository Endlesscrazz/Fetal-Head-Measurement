import { useEffect, useRef } from "react";

import type { Sample } from "../../types/sample";

export function ProbThresholdLayer({
  probSrc,
  sample,
  showProb,
  thresh,
}: {
  probSrc: string;
  sample: Sample;
  showProb: boolean;
  thresh: number;
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
      const source = offscreenCtx.getImageData(0, 0, width, height);
      const output = ctx.createImageData(width, height);
      const threshold = thresh * 255;

      for (let index = 0; index < source.data.length; index += 4) {
        const value = source.data[index];
        if (value >= threshold) {
          output.data[index] = 110;
          output.data[index + 1] = 224;
          output.data[index + 2] = 255;
          output.data[index + 3] = Math.min(180, 80 + Math.max(0, value - threshold));
        } else if (showProb && value > 30) {
          output.data[index] = 255;
          output.data[index + 1] = 180;
          output.data[index + 2] = 84;
          output.data[index + 3] = Math.round((value / 255) * 60);
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
  }, [probSrc, sample.resolution, showProb, thresh]);

  return <canvas ref={canvasRef} className="layer threshold-layer fade-in" />;
}
