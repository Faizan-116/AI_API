import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import ServiceCard from "../components/ServiceCard";
import ProjectCard from "../components/ProjectCard";
import SectionHeading from "../components/SectionHeading";
import { profile } from "../content";

export default function Home() {
  const [services, setServices] = useState([]);
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    api.getServices().then(setServices).catch(() => {});
    api.getProjects().then((p) => setProjects(p.slice(0, 3))).catch(() => {});
  }, []);

  return (
    <div>
      <section className="mx-auto max-w-6xl px-6 pt-16 pb-24 grid md:grid-cols-[1.4fr,1fr] gap-12 items-end">
        <div>
          <div className="citation-mark mb-4">Lecturer · Mentor · Freelance Academic Support</div>
          <h1 className="font-display text-4xl md:text-6xl leading-[1.05] text-ink">
            {profile.tagline}
          </h1>
          <p className="mt-6 max-w-prose text-ink-soft leading-relaxed">{profile.bio}</p>
          <div className="mt-8 flex flex-wrap gap-4">
            <Link
              to="/book"
              className="rounded-sm bg-moss px-6 py-3 font-mono text-sm text-paper hover:bg-moss-dark transition-colors"
            >
              Book a session
            </Link>
            <Link
              to="/services"
              className="rounded-sm border border-ink px-6 py-3 font-mono text-sm text-ink hover:bg-ink hover:text-paper transition-colors"
            >
              View services
            </Link>
          </div>
        </div>
        <div className="border border-line bg-white/40 p-6">
          <div className="citation-mark mb-3">At a glance</div>
          <dl className="space-y-3 font-mono text-sm">
            <div className="flex justify-between border-b border-line pb-2">
              <dt className="text-ink-soft">Institution</dt>
              <dd className="text-ink">{profile.university}</dd>
            </div>
            <div className="flex justify-between border-b border-line pb-2">
              <dt className="text-ink-soft">Experience</dt>
              <dd className="text-ink">{profile.yearsExperience} years</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-ink-soft">Based in</dt>
              <dd className="text-ink">{profile.location}</dd>
            </div>
          </dl>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-6 py-16 border-t border-line">
        <SectionHeading
          mark="1"
          title="How I can help"
          description="Support across the parts of a degree students find hardest — from a blank page to the viva."
        />
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {services.map((service) => (
            <ServiceCard key={service.id} service={service} />
          ))}
        </div>
      </section>

      {projects.length > 0 && (
        <section className="mx-auto max-w-6xl px-6 py-16 border-t border-line">
          <SectionHeading mark="2" title="Selected work" />
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((project) => (
              <ProjectCard key={project.id} project={project} />
            ))}
          </div>
          <Link
            to="/projects"
            className="inline-block mt-8 font-mono text-sm text-moss hover:text-moss-dark underline underline-offset-4"
          >
            See all projects
          </Link>
        </section>
      )}
    </div>
  );
}
