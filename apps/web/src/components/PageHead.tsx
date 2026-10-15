import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import { ChevronLeft } from "lucide-react";

export function PageHead({ eyebrow, title, back, backLabel = "Back", actions }: { eyebrow?: string; title: string; back?: string; backLabel?: string; actions?: ReactNode }) {
  return (
    <header className="page-head">
      <div style={{ minWidth: 0 }}>
        {back && (
          <Link to={back} className="back-link">
            <ChevronLeft size={18} aria-hidden="true" /> {backLabel}
          </Link>
        )}
        {eyebrow && <p className="page-head__eyebrow">{eyebrow}</p>}
        <h1 className="page-head__title">{title}</h1>
      </div>
      {actions && <div className="row">{actions}</div>}
    </header>
  );
}

export function Loading({ label = "Loading" }: { label?: string }) {
  return (
    <div className="screen-fallback" aria-busy="true" aria-label={label}>
      <div className="skeleton" style={{ height: 34, width: "45%" }} />
      <div className="skeleton" style={{ height: 120 }} />
      <div className="skeleton" style={{ height: 80 }} />
    </div>
  );
}
