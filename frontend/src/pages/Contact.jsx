import { useState } from "react";
import { api } from "../api";
import SectionHeading from "../components/SectionHeading";
import { profile } from "../content";

export default function Contact() {
  const [form, setForm] = useState({ name: "", email: "", subject: "", message: "" });
  const [sent, setSent] = useState(false);
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await api.sendContactMessage(form);
      setSent(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="mx-auto max-w-2xl px-6 py-16">
      <SectionHeading mark="Contact" title="Get in touch" description={`Or email me directly at ${profile.email}.`} />

      {sent ? (
        <p className="text-ink">Thanks — I'll get back to you soon.</p>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <label className="block">
            <span className="citation-mark block mb-1">Name</span>
            <input
              required
              className="w-full border border-line bg-white/60 px-3 py-2"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
            />
          </label>
          <label className="block">
            <span className="citation-mark block mb-1">Email</span>
            <input
              required
              type="email"
              className="w-full border border-line bg-white/60 px-3 py-2"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
            />
          </label>
          <label className="block">
            <span className="citation-mark block mb-1">Subject</span>
            <input
              className="w-full border border-line bg-white/60 px-3 py-2"
              value={form.subject}
              onChange={(e) => setForm({ ...form, subject: e.target.value })}
            />
          </label>
          <label className="block">
            <span className="citation-mark block mb-1">Message</span>
            <textarea
              required
              rows={5}
              className="w-full border border-line bg-white/60 px-3 py-2"
              value={form.message}
              onChange={(e) => setForm({ ...form, message: e.target.value })}
            />
          </label>
          {error && <p className="text-red-700 font-mono text-sm">{error}</p>}
          <button
            type="submit"
            disabled={submitting}
            className="rounded-sm bg-moss px-6 py-3 font-mono text-sm text-paper hover:bg-moss-dark transition-colors disabled:opacity-50"
          >
            {submitting ? "Sending…" : "Send message"}
          </button>
        </form>
      )}
    </div>
  );
}
