const outlineCache = new Map<string, Promise<string>>();

function buildOutline(src: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.onload = () => {
      const width = image.naturalWidth || image.width;
      const height = image.naturalHeight || image.height;
      const canvas = document.createElement("canvas");
      canvas.width = width;
      canvas.height = height;
      const context = canvas.getContext("2d", { willReadFrequently: true });
      if (!context) {
        reject(new Error("Could not create contour outline canvas context"));
        return;
      }

      context.drawImage(image, 0, 0, width, height);
      const source = context.getImageData(0, 0, width, height);
      const output = context.createImageData(width, height);

      const amber = { r: 255, g: 207, b: 110 };
      const indexFor = (x: number, y: number) => (y * width + x) * 4;
      const isOn = (x: number, y: number) => {
        if (x < 0 || x >= width || y < 0 || y >= height) return false;
        const index = indexFor(x, y);
        return source.data[index + 3] > 8 && source.data[index] > 8;
      };

      for (let y = 0; y < height; y += 1) {
        for (let x = 0; x < width; x += 1) {
          if (!isOn(x, y)) continue;

          const boundary =
            !isOn(x - 1, y) ||
            !isOn(x + 1, y) ||
            !isOn(x, y - 1) ||
            !isOn(x, y + 1) ||
            !isOn(x - 1, y - 1) ||
            !isOn(x + 1, y - 1) ||
            !isOn(x - 1, y + 1) ||
            !isOn(x + 1, y + 1);

          if (!boundary) continue;

          for (let dy = -1; dy <= 1; dy += 1) {
            for (let dx = -1; dx <= 1; dx += 1) {
              const nx = x + dx;
              const ny = y + dy;
              if (nx < 0 || nx >= width || ny < 0 || ny >= height) continue;
              const index = indexFor(nx, ny);
              const isCenter = dx === 0 && dy === 0;
              output.data[index] = amber.r;
              output.data[index + 1] = amber.g;
              output.data[index + 2] = amber.b;
              output.data[index + 3] = Math.max(output.data[index + 3], isCenter ? 255 : 112);
            }
          }
        }
      }

      context.clearRect(0, 0, width, height);
      context.putImageData(output, 0, 0);
      resolve(canvas.toDataURL("image/png"));
    };
    image.onerror = () => reject(new Error(`Could not load mask outline source: ${src}`));
    image.src = src;
  });
}

export function getMaskOutlineDataUrl(src: string): Promise<string> {
  const cached = outlineCache.get(src);
  if (cached) {
    return cached;
  }
  const promise = buildOutline(src);
  outlineCache.set(src, promise);
  return promise;
}
