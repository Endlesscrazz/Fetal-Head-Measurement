import type { Ellipse } from "../../types/sample";

export function EllipseLayer({
  ellipse,
  height,
  hcMm,
  showHC,
  visible,
  width,
}: {
  ellipse: Ellipse;
  height: number;
  hcMm: number;
  showHC: boolean;
  visible: boolean;
  width: number;
}) {
  const degrees = (ellipse.rot * 180) / Math.PI;
  const ribbonX = Math.min(width - 112, ellipse.cx + ellipse.rx + 14);
  const ribbonY = Math.max(24, ellipse.cy - ellipse.ry - 10);

  return (
    <svg
      aria-hidden="true"
      className={`layer ${visible ? "fade-in" : "fade-out"}`}
      preserveAspectRatio="xMidYMid slice"
      viewBox={`0 0 ${width} ${height}`}
    >
      <ellipse
        cx={ellipse.cx}
        cy={ellipse.cy}
        fill="rgba(110,224,255,0.04)"
        rx={ellipse.rx}
        ry={ellipse.ry}
        stroke="#6ee0ff"
        strokeWidth="1.6"
        style={{ filter: "drop-shadow(0 0 4px rgba(110,224,255,0.8))" }}
        transform={`rotate(${degrees.toFixed(2)} ${ellipse.cx} ${ellipse.cy})`}
      />

      <g transform={`rotate(${degrees.toFixed(2)} ${ellipse.cx} ${ellipse.cy})`}>
        <line
          opacity="0.6"
          stroke="#6ee0ff"
          strokeDasharray="3 3"
          strokeWidth="0.8"
          x1={ellipse.cx - ellipse.rx}
          x2={ellipse.cx + ellipse.rx}
          y1={ellipse.cy}
          y2={ellipse.cy}
        />
        <line
          opacity="0.6"
          stroke="#6ee0ff"
          strokeDasharray="3 3"
          strokeWidth="0.8"
          x1={ellipse.cx}
          x2={ellipse.cx}
          y1={ellipse.cy - ellipse.ry}
          y2={ellipse.cy + ellipse.ry}
        />
      </g>

      {showHC && (
        <>
          <ellipse
            cx={ellipse.cx}
            cy={ellipse.cy}
            fill="none"
            opacity="0.7"
            rx={ellipse.rx + 6}
            ry={ellipse.ry + 6}
            stroke="#6ee0ff"
            strokeDasharray="2 4"
            strokeWidth="0.8"
            transform={`rotate(${degrees.toFixed(2)} ${ellipse.cx} ${ellipse.cy})`}
          >
            <animate
              attributeName="stroke-dashoffset"
              dur="2s"
              from="0"
              repeatCount="indefinite"
              to="-12"
            />
          </ellipse>
          <g transform={`translate(${ribbonX} ${ribbonY})`}>
            <rect
              fill="rgba(7,9,15,0.82)"
              height="22"
              rx="11"
              stroke="rgba(110,224,255,0.3)"
              width="92"
              x="0"
              y="0"
            />
            <text
              fill="#6ee0ff"
              fontFamily="var(--mono)"
              fontSize="11"
              letterSpacing="0.08em"
              x="46"
              y="14.5"
              textAnchor="middle"
            >
              {hcMm.toFixed(2)} mm
            </text>
          </g>
        </>
      )}
    </svg>
  );
}
