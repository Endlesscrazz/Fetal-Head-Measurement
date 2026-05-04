export function MethodSection() {
  const cards = [
    {
      body: "Local features plus attention gates across four scales. Lightweight enough for a portfolio demo, faithful enough to the real pipeline.",
      eyebrow: "Architecture",
      title: "Attention U-Net",
    },
    {
      body: "HC18-derived curated examples, augmentation-heavy local training, and a held-out internal test split behind the exported bundle.",
      eyebrow: "Training",
      title: "HC18 · saved outputs",
    },
    {
      body: "Real fetal skulls are close to ellipsoidal. The ellipse fit projects noisy masks onto the right measurement family.",
      eyebrow: "Why ellipse fit",
      title: "Geometric prior",
    },
  ];

  return (
    <section className="method-section">
      <div className="section-heading">
        <div>
          <div className="eyebrow">05 / Method notes</div>
          <h2 className="serif section-title">How the model and geometry work together.</h2>
        </div>
      </div>

      <div className="method-grid">
        {cards.map((card) => (
          <article className="method-card" key={card.eyebrow}>
            <div className="mono method-card__eyebrow">{card.eyebrow}</div>
            <h3 className="serif method-card__title">{card.title}</h3>
            <p>{card.body}</p>
          </article>
        ))}
      </div>

      <div className="method-note">
        <span className="mono">Training note</span>
        <p>Local training checkpoint: 10 epochs, 256 × 384 resolution, base channels 16.</p>
      </div>
    </section>
  );
}
