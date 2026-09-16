import { Link } from "react-router-dom";

const PRICE_LABEL = {
  hourly: "/ hr",
  fixed: "flat",
  package: "package",
};

export default function ServiceCard({ service }) {
  return (
    <div className="border border-line bg-white/40 p-6 flex flex-col gap-4">
      <div>
        <h3 className="font-display text-xl text-ink">{service.title}</h3>
        <p className="mt-2 text-sm text-ink-soft leading-relaxed">{service.short_description}</p>
      </div>
      <div className="mt-auto flex items-center justify-between pt-4 border-t border-line">
        <span className="font-mono text-sm text-brass">
          {service.price === 0 ? "Free" : `£${service.price} ${PRICE_LABEL[service.price_type]}`}
        </span>
        <Link
          to={`/book?service=${service.id}`}
          className="font-mono text-sm text-moss hover:text-moss-dark underline underline-offset-4"
        >
          Book this
        </Link>
      </div>
    </div>
  );
}
