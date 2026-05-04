import { useMemo } from "react";

import type { Ellipse } from "../../types/sample";

export function ContourPath({ ellipse, opacity }: { ellipse: Ellipse; opacity: number }) {
  const path = useMemo(() => {
    const points: [number, number][] = [];
    let seed = 21;
    const rand = () => {
      seed = (seed * 9301 + 49297) % 233280;
      return seed / 233280;
    };

    for (let index = 0; index < 90; index += 1) {
      const angle = (index / 90) * Math.PI * 2;
      const rx = ellipse.rx + (rand() - 0.5) * 4.5;
      const ry = ellipse.ry + (rand() - 0.5) * 3.8;
      const lx = Math.cos(angle) * rx;
      const ly = Math.sin(angle) * ry;
      const cos = Math.cos(ellipse.rot);
      const sin = Math.sin(ellipse.rot);
      points.push([ellipse.cx + lx * cos - ly * sin, ellipse.cy + lx * sin + ly * cos]);
    }

    return points.map((point, index) => `${index === 0 ? "M" : "L"} ${point[0].toFixed(1)} ${point[1].toFixed(1)}`).join(" ") + " Z";
  }, [ellipse]);

  return (
    <path
      d={path}
      fill="rgba(255,180,84,0.04)"
      opacity={opacity}
      stroke="#ffb454"
      strokeWidth="1.6"
      style={{
        filter: "drop-shadow(0 0 3px rgba(255,180,84,0.6))",
        transition: "opacity 280ms ease",
      }}
    />
  );
}
