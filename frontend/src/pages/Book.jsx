import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { api } from "../api";
import SectionHeading from "../components/SectionHeading";

function formatSlot(slot) {
  const start = new Date(slot.start);
  return start.toLocaleString(undefined, {
    weekday: "short",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

export default function Book() {
  const [searchParams] = useSearchParams();
  const preselectedServiceId = searchParams.get("service");
  const preselectedCourseId = searchParams.get("course");

  const [services, setServices] = useState([]);
  const [courses, setCourses] = useState([]);
  const [serviceId, setServiceId] = useState(preselectedServiceId || "");
  const [courseId, setCourseId] = useState(preselectedCourseId || "");

  const [slots, setSlots] = useState([]);
  const [slotsError, setSlotsError] = useState(null);
  const [loadingSlots, setLoadingSlots] = useState(false);
  const [selectedSlot, setSelectedSlot] = useState(null);

  const [form, setForm] = useState({ student_name: "", student_email: "", notes: "" });
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [submitError, setSubmitError] = useState(null);

  useEffect(() => {
    api.getServices().then(setServices).catch(() => {});
    api.getCourses().then(setCourses).catch(() => {});
  }, []);

  const selected = useMemo(() => {
    if (serviceId) return services.find((s) => String(s.id) === String(serviceId));
    if (courseId) return courses.find((c) => String(c.id) === String(courseId));
    return null;
  }, [serviceId, courseId, services, courses]);

  const durationMinutes = selected?.duration_minutes || 60;

  useEffect(() => {
    if (!selected) return;
    setLoadingSlots(true);
    setSlotsError(null);
    setSelectedSlot(null);
    api
      .getAvailability(durationMinutes)
      .then(setSlots)
      .catch((e) => setSlotsError(e.message))
      .finally(() => setLoadingSlots(false));
  }, [selected, durationMinutes]);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!selectedSlot) return;
    setSubmitting(true);
    setSubmitError(null);
    try {
      const booking = await api.createBooking({
        ...form,
        service_id: serviceId ? Number(serviceId) : null,
        course_id: courseId ? Number(courseId) : null,
        start_time: selectedSlot.start,
        end_time: selectedSlot.end,
      });
      setResult(booking);
    } catch (err) {
      setSubmitError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  if (result) {
    return (
      <div className="mx-auto max-w-2xl px-6 py-24 text-center">
        <SectionHeading mark="Booked" title="Session requested" />
        <p className="text-ink-soft">
          Thanks, {result.student_name}. Your session is{" "}
          {result.status === "confirmed" ? "confirmed" : "pending confirmation"}.
          {result.meet_link && (
            <>
              {" "}
              Join link:{" "}
              <a className="text-moss underline" href={result.meet_link}>
                {result.meet_link}
              </a>
            </>
          )}
        </p>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl px-6 py-16">
      <SectionHeading mark="Book" title="Book a session" description="Pick a service or course, then a time." />

      <div className="grid sm:grid-cols-2 gap-4 mb-8">
        <label className="block">
          <span className="citation-mark block mb-1">Service</span>
          <select
            className="w-full border border-line bg-white/60 px-3 py-2 font-mono text-sm"
            value={serviceId}
            onChange={(e) => {
              setServiceId(e.target.value);
              setCourseId("");
            }}
          >
            <option value="">— choose a service —</option>
            {services.map((s) => (
              <option key={s.id} value={s.id}>
                {s.title}
              </option>
            ))}
          </select>
        </label>
        <label className="block">
          <span className="citation-mark block mb-1">Course</span>
          <select
            className="w-full border border-line bg-white/60 px-3 py-2 font-mono text-sm"
            value={courseId}
            onChange={(e) => {
              setCourseId(e.target.value);
              setServiceId("");
            }}
          >
            <option value="">— choose a course —</option>
            {courses.map((c) => (
              <option key={c.id} value={c.id}>
                {c.title}
              </option>
            ))}
          </select>
        </label>
      </div>

      {selected && (
        <div className="mb-8">
          <div className="citation-mark mb-2">Available times ({durationMinutes} min)</div>
          {loadingSlots && <p className="text-sm text-ink-soft">Loading availability…</p>}
          {slotsError && (
            <p className="text-sm text-red-700 font-mono">
              {slotsError}. (Google Calendar may not be connected yet — see backend/README.)
            </p>
          )}
          {!loadingSlots && !slotsError && slots.length === 0 && (
            <p className="text-sm text-ink-soft">No slots available in the next two weeks.</p>
          )}
          <div className="flex flex-wrap gap-2">
            {slots.slice(0, 24).map((slot) => (
              <button
                type="button"
                key={slot.start}
                onClick={() => setSelectedSlot(slot)}
                className={`border px-3 py-2 font-mono text-xs ${
                  selectedSlot?.start === slot.start
                    ? "border-moss bg-moss text-paper"
                    : "border-line hover:border-moss"
                }`}
              >
                {formatSlot(slot)}
              </button>
            ))}
          </div>
        </div>
      )}

      {selected && selectedSlot && (
        <form onSubmit={handleSubmit} className="space-y-4 border-t border-line pt-8">
          <label className="block">
            <span className="citation-mark block mb-1">Your name</span>
            <input
              required
              className="w-full border border-line bg-white/60 px-3 py-2"
              value={form.student_name}
              onChange={(e) => setForm({ ...form, student_name: e.target.value })}
            />
          </label>
          <label className="block">
            <span className="citation-mark block mb-1">Your email</span>
            <input
              required
              type="email"
              className="w-full border border-line bg-white/60 px-3 py-2"
              value={form.student_email}
              onChange={(e) => setForm({ ...form, student_email: e.target.value })}
            />
          </label>
          <label className="block">
            <span className="citation-mark block mb-1">What would you like to cover?</span>
            <textarea
              rows={4}
              className="w-full border border-line bg-white/60 px-3 py-2"
              value={form.notes}
              onChange={(e) => setForm({ ...form, notes: e.target.value })}
            />
          </label>
          {submitError && <p className="text-red-700 font-mono text-sm">{submitError}</p>}
          <button
            type="submit"
            disabled={submitting}
            className="rounded-sm bg-moss px-6 py-3 font-mono text-sm text-paper hover:bg-moss-dark transition-colors disabled:opacity-50"
          >
            {submitting ? "Booking…" : "Confirm booking"}
          </button>
        </form>
      )}
    </div>
  );
}
