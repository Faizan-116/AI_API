import { useEffect, useState } from "react";
import { api } from "../api";
import SectionHeading from "../components/SectionHeading";
import ProjectCard from "../components/ProjectCard";

export default function Projects() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    api.getProjects().then(setProjects).catch(() => {});
  }, []);

  return (
    <div className="mx-auto max-w-6xl px-6 py-16">
      <SectionHeading mark="Projects" title="Selected work" />
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {projects.map((project) => (
          <ProjectCard key={project.id} project={project} />
        ))}
      </div>
    </div>
  );
}
