import { useEffect, useState } from "react";
import { api } from "../api";
import SectionHeading from "../components/SectionHeading";
import CourseCard from "../components/CourseCard";

export default function Courses() {
  const [courses, setCourses] = useState([]);

  useEffect(() => {
    api.getCourses().then(setCourses).catch(() => {});
  }, []);

  return (
    <div className="mx-auto max-w-6xl px-6 py-16">
      <SectionHeading
        mark="Courses"
        title="One-to-one courses"
        description="Structured, multi-week courses taught one-to-one and paced to you."
      />
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {courses.map((course) => (
          <CourseCard key={course.id} course={course} />
        ))}
      </div>
    </div>
  );
}
