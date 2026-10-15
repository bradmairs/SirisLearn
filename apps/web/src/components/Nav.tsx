import { useEffect } from "react";
import { NavLink, useLocation } from "react-router-dom";
import { Award, History, House, Library, LogOut, Settings, X } from "lucide-react";
import { APP_VERSION } from "../version";
import { Glass } from "./Glass";
import { Logo } from "./Logo";

/** Every screen. `dock: false` keeps one off the phone tab bar. */
export const NAV: { to: string; label: string; Icon: typeof House; end: boolean; dock?: boolean }[] = [
  { to: "/", label: "Today", Icon: House, end: true },
  { to: "/library", label: "Library", Icon: Library, end: false },
  { to: "/history", label: "History", Icon: History, end: false },
  { to: "/awards", label: "Awards", Icon: Award, end: false },
  { to: "/settings", label: "Settings", Icon: Settings, end: false, dock: false },
];

/** Phone tab bar. Wide screens use the sidebar instead (hidden in CSS). */
export function Dock() {
  return (
    <Glass as="nav" shape="pill" className="dock" aria-label="Main">
      {NAV.filter((n) => n.dock !== false).map(({ to, label, Icon, end }) => (
        <NavLink key={to} to={to} end={end} className="dock__item">
          <Icon size={22} strokeWidth={2} aria-hidden="true" />
          <span>{label}</span>
        </NavLink>
      ))}
    </Glass>
  );
}

/** The side menu: always visible on wide screens, a drawer on phones. */
export function Sidebar({ user, open, onClose, onSignOut }: { user: string; open: boolean; onClose: () => void; onSignOut: () => void }) {
  const location = useLocation();
  useEffect(() => {
    onClose();
  }, [location.pathname, onClose]);
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  return (
    <>
      <div className={`sidebar-scrim ${open ? "sidebar-scrim--open" : ""}`} onClick={onClose} aria-hidden="true" />
      <Glass as="aside" variant="strong" shape="xl" className={`sidebar ${open ? "sidebar--open" : ""}`} aria-label="Menu">
        <div className="sidebar__brand">
          <Logo size={38} />
          <button type="button" className="icon-link sidebar__close" onClick={onClose} aria-label="Close menu">
            <X size={18} aria-hidden="true" />
          </button>
        </div>
        <nav className="sidebar__nav" aria-label="Screens">
          {NAV.map(({ to, label, Icon, end }) => (
            <NavLink key={to} to={to} end={end} className="sidebar__link">
              <Icon size={19} aria-hidden="true" />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>
        <div className="sidebar__foot">
          <span className="sidebar__user">
            {user.charAt(0).toUpperCase() + user.slice(1)}
            <span className="sidebar__version">SirisLearn {APP_VERSION}</span>
          </span>
          <button type="button" className="icon-link" onClick={onSignOut} aria-label="Sign out" title="Sign out">
            <LogOut size={17} aria-hidden="true" />
          </button>
        </div>
      </Glass>
    </>
  );
}
