import { Link, useParams } from "react-router-dom";
import { ChevronLeft, Printer } from "lucide-react";
import { useApi } from "../api/useApi";
import type { Certificate as CertificateData } from "../api/types";
import { LogoMark } from "../components/Logo";
import { Loading } from "../components/PageHead";
import { cap } from "./Library";

/** A printable certificate for a course whose final exam you passed. */
export function Certificate() {
  const { id } = useParams();
  const { data, error } = useApi<CertificateData>(`/api/courses/${id}/certificate`);
  if (error) return <div className="stack"><div className="error-banner" role="alert">{error}</div><Link to={`/course/${id}`} className="back-link">Back to the course</Link></div>;
  if (!data) return <Loading />;
  const issued = new Date(data.issued).toLocaleDateString(undefined, { day: "numeric", month: "long", year: "numeric" });
  return (
    <div className="certificate-page">
      <div className="row certificate__tools">
        <Link to={`/course/${id}`} className="back-link"><ChevronLeft size={18} aria-hidden="true" /> Course</Link>
        <span className="spacer" />
        <button type="button" className="chip chip--button" onClick={() => window.print()}><Printer size={14} aria-hidden="true" /> Print or save as PDF</button>
      </div>
      <article className="certificate" aria-label="Certificate of completion">
        <div className="certificate__brand"><LogoMark size={44} /><span>SIRIS<b>LEARN</b></span></div>
        <p className="certificate__eyebrow">Certificate of completion</p>
        <p className="certificate__lead">This certifies that</p>
        <h1 className="certificate__name">{data.name}</h1>
        <p className="certificate__lead">has completed the {data.level} course</p>
        <h2 className="certificate__course">{data.course}</h2>
        <p className="certificate__summary">{data.summary}</p>
        <ul className="certificate__facts">
          <li><b>{data.lessons}</b> lessons</li>
          <li>{data.minutes >= 60 ? <><b>{Math.round(data.minutes / 6) / 10}</b> hours of study</> : <><b>{data.minutes}</b> minutes of study</>}</li>
          <li><b>{Math.round((data.score ?? 0) * 100)}%</b> on the final exam</li>
        </ul>
        <p className="certificate__sections">{data.sections.join(" · ")}</p>
        <footer className="certificate__foot">
          <span>Issued {issued}</span>
          <span>{cap(data.level)} level</span>
          <span>Ref. {data.reference}</span>
        </footer>
      </article>
    </div>
  );
}
