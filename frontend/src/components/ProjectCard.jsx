export default function ProjectCard({ project }) {
  return (
    <a
      href={project.project_url || undefined}
      target={project.project_url ? "_blank" : undefined}
      rel="noreferrer"
      className="block border border-line bg-white/40 p-6 hover:border-moss transition-colors"
    >
      {project.category && (
        <div className="citation-mark mb-2">{project.category}</div>
      )}
      <h3 className="font-display text-xl text-ink">{project.title}</h3>
      <p className="mt-2 text-sm text-ink-soft leading-relaxed">{project.description}</p>
      {project.tech_stack && (
        <p className="mt-4 font-mono text-xs text-ink-soft">{project.tech_stack}</p>
      )}
    </a>
  );
}
