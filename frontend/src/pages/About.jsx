import SectionHeading from "../components/SectionHeading";
import { profile, testimonials } from "../content";

export default function About() {
  return (
    <div className="mx-auto max-w-6xl px-6 py-16">
      <SectionHeading mark="Bio" title={profile.name} description={profile.title} />

      <div className="grid md:grid-cols-[1fr,1fr] gap-12">
        <p className="text-ink-soft leading-relaxed whitespace-pre-line">{profile.bio}</p>

        <div className="space-y-8">
          <div>
            <div className="citation-mark mb-2">Credentials</div>
            <ul className="space-y-1 text-sm text-ink">
              {profile.credentials.map((c, i) => (
                <li key={i} className="border-b border-line pb-1">{c}</li>
              ))}
            </ul>
          </div>
          <div>
            <div className="citation-mark mb-2">Subjects & skills</div>
            <div className="flex flex-wrap gap-2">
              {profile.skills.map((skill) => (
                <span key={skill} className="border border-line px-3 py-1 text-sm font-mono">
                  {skill}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {testimonials.length > 0 && (
        <div className="mt-16 pt-16 border-t border-line">
          <SectionHeading mark="3" title="What students say" />
          <div className="grid md:grid-cols-2 gap-6">
            {testimonials.map((t) => (
              <blockquote key={t.author} className="border border-line bg-white/40 p-6">
                <p className="text-ink italic">&ldquo;{t.quote}&rdquo;</p>
                <footer className="mt-3 font-mono text-xs text-ink-soft">{t.author}</footer>
              </blockquote>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
