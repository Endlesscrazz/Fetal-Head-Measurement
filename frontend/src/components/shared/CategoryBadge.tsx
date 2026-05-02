import type { SampleCategory } from "../../types/sample";

export const CAT_STYLE: Record<
  SampleCategory,
  { color: string; bg: string; dot: string; label: string }
> = {
  strong: {
    color: "var(--good)",
    bg: "rgba(123, 227, 139, 0.10)",
    dot: "var(--good)",
    label: "Strong",
  },
  typical: {
    color: "var(--cyan)",
    bg: "rgba(110, 224, 255, 0.10)",
    dot: "var(--cyan)",
    label: "Typical",
  },
  failure: {
    color: "var(--amber)",
    bg: "rgba(255, 180, 84, 0.10)",
    dot: "var(--amber)",
    label: "Failure",
  },
};

export function CategoryBadge({ cat, size = "md" }: { cat: SampleCategory; size?: "sm" | "md" }) {
  const style = CAT_STYLE[cat];
  const padY = size === "sm" ? 2 : 3;
  const padX = size === "sm" ? 6 : 8;
  const fontSize = size === "sm" ? 9.5 : 10.5;

  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 6,
        padding: `${padY}px ${padX}px`,
        color: style.color,
        fontFamily: "var(--mono)",
        fontSize,
        letterSpacing: 0,
        textTransform: "uppercase",
        background: style.bg,
        border: `1px solid ${style.color}33`,
        borderRadius: 999,
        whiteSpace: "nowrap",
      }}
    >
      <span
        style={{
          width: 5,
          height: 5,
          background: style.dot,
          borderRadius: 999,
          boxShadow: `0 0 8px ${style.dot}`,
        }}
      />
      {style.label}
    </span>
  );
}
