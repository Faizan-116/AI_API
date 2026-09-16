export default function SectionHeading({ mark, title, description }) {
  return (
    <div className="mb-10 max-w-prose">
      {mark && <div className="citation-mark mb-2">[{mark}]</div>}
      <h2 className="font-display text-3xl md:text-4xl text-ink">{title}</h2>
      {description && <p className="mt-3 text-ink-soft leading-relaxed">{description}</p>}
    </div>
  );
}
