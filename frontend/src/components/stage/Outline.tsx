import { useEffect, useRef } from "react";

function parseColor(value: string): [number, number, number, number] {
  if (value.startsWith("#")) {
    const hex = value.slice(1);
    const normalized = hex.length === 3 ? hex.split("").map((c) => c + c).join("") : hex;
    return [
      Number.parseInt(normalized.slice(0, 2), 16),
      Number.parseInt(normalized.slice(2, 4), 16),
      Number.parseInt(normalized.slice(4, 6), 16),
      255,
    ];
  }

  const rgba = value.match(/rgba?\(([^)]+)\)/i);
  if (!rgba) return [255, 255, 255, 255];
  const parts = rgba[1].split(",").map((part) => part.trim());
  const [r, g, b] = parts.slice(0, 3).map((part) => Number.parseFloat(part));
  const alpha = parts[3] === undefined ? 1 : Number.parseFloat(parts[3]);
  return [r, g, b, Math.round(alpha * 255)];
}

export function Outline({
  fill,
  height,
  src,
  stroke,
  visible,
  width,
}: {
  fill?: string;
  height: number;
  src: string;
  stroke: string;
  visible: boolean;
  width: number;
}) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    let cancelled = false;
    const canvas = canvasRef.current;
    if (!canvas) return;

    const image = new Image();
    image.onload = () => {
      if (cancelled) return;

      const offscreen = document.createElement("canvas");
      offscreen.width = width;
      offscreen.height = height;
      const offscreenCtx = offscreen.getContext("2d", { willReadFrequently: true });
      const ctx = canvas.getContext("2d", { willReadFrequently: true });
      if (!offscreenCtx || !ctx) return;

      offscreenCtx.clearRect(0, 0, width, height);
      offscreenCtx.drawImage(image, 0, 0, width, height);
      const source = offscreenCtx.getImageData(0, 0, width, height);
      const outline = ctx.createImageData(width, height);
      const strokeRgba = parseColor(stroke);
      const fillRgba = fill ? parseColor(fill) : null;
      const idx = (x: number, y: number) => (y * width + x) * 4;

      for (let y = 0; y < height; y += 1) {
        for (let x = 0; x < width; x += 1) {
          const i = idx(x, y);
          const value = source.data[i];
          if (value < 128) continue;

          if (fillRgba) {
            outline.data[i] = fillRgba[0];
            outline.data[i + 1] = fillRgba[1];
            outline.data[i + 2] = fillRgba[2];
            outline.data[i + 3] = fillRgba[3];
          }

          const north = y > 0 ? source.data[idx(x, y - 1)] : 0;
          const south = y < height - 1 ? source.data[idx(x, y + 1)] : 0;
          const east = x < width - 1 ? source.data[idx(x + 1, y)] : 0;
          const west = x > 0 ? source.data[idx(x - 1, y)] : 0;

          if (north < 128 || south < 128 || east < 128 || west < 128) {
            outline.data[i] = strokeRgba[0];
            outline.data[i + 1] = strokeRgba[1];
            outline.data[i + 2] = strokeRgba[2];
            outline.data[i + 3] = strokeRgba[3];
          }
        }
      }

      canvas.width = width;
      canvas.height = height;
      ctx.clearRect(0, 0, width, height);
      ctx.putImageData(outline, 0, 0);
    };

    image.src = src;

    return () => {
      cancelled = true;
    };
  }, [fill, height, src, stroke, width]);

  return <canvas ref={canvasRef} className={`layer ${visible ? "fade-in" : "fade-out"}`} />;
}
