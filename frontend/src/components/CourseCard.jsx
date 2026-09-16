import { Link } from "react-router-dom";

export default function CourseCard({ course }) {
  return (
    <div className="border border-line bg-white/40 p-6 flex flex-col gap-4">
      <div>
        <div className="citation-mark mb-2">
          {course.is_one_to_one ? "One-to-one" : "Group"} · {course.duration_weeks} weeks · {course.level}
        </div>
        <h3 className="font-display text-xl text-ink">{course.title}</h3>
        <p className="mt-2 text-sm text-ink-soft leading-relaxed">{course.description}</p>
      </div>
      <div className="mt-auto flex items-center justify-between pt-4 border-t border-line">
        <span className="font-mono text-sm text-brass">£{course.price}</span>
        <Link
          to={`/book?course=${course.id}`}
          className="font-mono text-sm text-moss hover:text-moss-dark underline underline-offset-4"
        >
          Enroll
        </Link>
      </div>
    </div>
  );
}
