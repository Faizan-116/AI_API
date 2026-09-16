import { NavLink } from "react-router-dom";
import { profile } from "../content";

const links = [
  { to: "/", label: "Home" },
  { to: "/about", label: "About" },
  { to: "/services", label: "Services" },
  { to: "/projects", label: "Projects" },
  { to: "/courses", label: "Courses" },
  { to: "/contact", label: "Contact" },
];

export default function Navbar() {
  return (
    <header className="border-b border-line bg-paper/95 backdrop-blur sticky top-0 z-40">
      <div className="mx-auto max-w-6xl px-6 flex items-center justify-between h-16">
        <NavLink to="/" className="font-display text-lg text-ink">
          {profile.name}
        </NavLink>
        <nav className="hidden md:flex items-center gap-8 font-mono text-sm">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `pb-1 border-b-2 transition-colors ${
                  isActive ? "border-moss text-ink" : "border-transparent text-ink-soft hover:text-ink"
                }`
              }
              end={link.to === "/"}
            >
              {link.label}
            </NavLink>
          ))}
        </nav>
        <NavLink
          to="/book"
          className="hidden md:inline-block rounded-sm bg-moss px-4 py-2 font-mono text-sm text-paper hover:bg-moss-dark transition-colors"
        >
          Book a session
        </NavLink>
      </div>
      <nav className="md:hidden flex overflow-x-auto gap-6 px-6 pb-3 font-mono text-xs">
        {[...links, { to: "/book", label: "Book" }].map((link) => (
          <NavLink key={link.to} to={link.to} className="text-ink-soft whitespace-nowrap">
            {link.label}
          </NavLink>
        ))}
      </nav>
    </header>
  );
}
