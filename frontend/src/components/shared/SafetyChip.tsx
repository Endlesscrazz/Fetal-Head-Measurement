export function SafetyChip({ text }: { text: string }) {
  return (
    <div className="safety-chip">
      <span className="safety-dot" />
      <span>{text}</span>
    </div>
  );
}
