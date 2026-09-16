import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import SectionHeading from "../components/SectionHeading";
import ServiceCard from "../components/ServiceCard";

export default function Services() {
  const [services, setServices] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.getServices().then(setServices).catch((e) => setError(e.message));
  }, []);

  return (
    <div className="mx-auto max-w-6xl px-6 py-16">
      <SectionHeading
        mark="Services"
        title="Ways I can help"
        description="Every session is one-to-one. Pick a service below, or get in touch if you're not sure which one fits."
      />

      {error && <p className="text-red-700 font-mono text-sm mb-6">{error}</p>}

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {services.map((service) => (
          <ServiceCard key={service.id} service={service} />
        ))}
      </div>

      <div className="mt-16 pt-16 border-t border-line max-w-prose">
        <SectionHeading
          mark="Note"
          title="Plagiarism & AI-writing checks"
          description="Submit a document and I'll run it through Turnitin for a similarity and AI-writing report, with results shared back to you directly."
        />
        <Link
          to="/plagiarism-check"
          className="inline-block font-mono text-sm text-moss hover:text-moss-dark underline underline-offset-4"
        >
          Submit a document for checking
        </Link>
      </div>
    </div>
  );
}
