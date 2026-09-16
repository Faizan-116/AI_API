import { profile } from "../content";

export default function Footer() {
  return (
    <footer className="border-t border-line mt-24">
      <div className="mx-auto max-w-6xl px-6 py-10 flex flex-col md:flex-row justify-between gap-4 text-sm text-ink-soft font-mono">
        <span>© {new Date().getFullYear()} {profile.name}</span>
        <span>{profile.email} · {profile.location}</span>
      </div>
    </footer>
  );
}
