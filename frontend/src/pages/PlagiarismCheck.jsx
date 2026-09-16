import { useState } from "react";
import { api } from "../api";
import SectionHeading from "../components/SectionHeading";

export default function PlagiarismCheck() {
  const [form, setForm] = useState({ student_name: "", student_email: "" });
  const [file, setFile] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!file) return;
    setSubmitting(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append("student_name", form.student_name);
      formData.append("student_email", form.student_email);
      formData.append("file", file);
      const res = await api.submitPlagiarismCheck(formData);
      setResult(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="mx-auto max-w-2xl px-6 py-16">
      <SectionHeading
        mark="Check"
        title="Plagiarism & AI-writing check"
        description="Upload a document to be submitted through Turnitin. You'll receive a similarity and AI-writing report."
      />

      {result ? (
        <div className="border border-line bg-white/40 p-6">
          <p className="text-ink">
            Submitted &ldquo;{result.file_name}&rdquo;. Status: <strong>{result.status}</strong>.
          </p>
          <p className="mt-2 text-sm text-ink-soft">
            You'll be emailed the report once it's ready. Reference ID: {result.id}
          </p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
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
            <span className="citation-mark block mb-1">Document</span>
            <input
              required
              type="file"
              accept=".doc,.docx,.pdf,.txt"
              className="w-full border border-line bg-white/60 px-3 py-2"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
          </label>
          {error && (
            <p className="text-red-700 font-mono text-sm">
              {error}. (Turnitin API credentials may not be configured yet.)
            </p>
          )}
          <button
            type="submit"
            disabled={submitting}
            className="rounded-sm bg-moss px-6 py-3 font-mono text-sm text-paper hover:bg-moss-dark transition-colors disabled:opacity-50"
          >
            {submitting ? "Submitting…" : "Submit for checking"}
          </button>
        </form>
      )}
    </div>
  );
}
