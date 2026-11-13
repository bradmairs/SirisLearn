import { useState, type FormEvent } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { ArrowDown, ArrowRight, ArrowUp, BadgeCheck, CalendarClock, CircleCheck, Plus, Route, Trash2, X } from "lucide-react";
import { del, patch, post } from "../api/client";
import { useApi } from "../api/useApi";
import type { CourseCard, LearningPath, PathStatus } from "../api/types";
import { Glass } from "../components/Glass";
import { CourseIcon } from "../components/icons";
import { Loading, PageHead } from "../components/PageHead";
import { Ring } from "../components/Ring";

const STATUS: Record<PathStatus, { label: string; tone: string }> = {
  done: { label: "Done", tone: "good" },
  on_track: { label: "On track", tone: "good" },
  behind: { label: "Behind", tone: "warning" },
  overdue: { label: "Past target", tone: "critical" },
  no_date: { label: "No target date", tone: "" },
};

function dateLabel(day: string): string {
  return new Date(`${day}T00:00:00`).toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" });
}

export function pace(p: LearningPath): string {
  if (p.done) return "Every course and exam passed.";
  if (!p.target_date) return `${p.done_units} of ${p.units} steps done.`;
  if (p.status === "overdue") return `Target was ${dateLabel(p.target_date)} · ${p.units - p.done_units} steps left.`;
  return `${p.days_left} days to ${dateLabel(p.target_date)} · about ${p.per_week} step${p.per_week === 1 ? "" : "s"} a week`
    + (p.status === "behind" ? ` (you'd be at ${p.expected_percent}% on a steady pace)` : "");
}

/** Learning paths: /paths */
export function Paths() {
  const { data, error, reload } = useApi<LearningPath[]>("/api/paths");
  const [creating, setCreating] = useState(false);
  return (
    <>
      <PageHead eyebrow="Goals" title="Learning paths" actions={!creating && (
        <Glass as="button" type="button" shape="pill" interactive className="button button--small" onClick={() => setCreating(true)}><Plus aria-hidden="true" /> New path</Glass>
      )} />
      <p className="muted">A path chains courses towards a goal, with a target date if you want one. A path is done when every lesson and final exam in it is passed.</p>
      {error && <div className="error-banner" role="alert">{error}</div>}
      {creating && <PathForm onDone={() => { setCreating(false); reload(); }} />}
      {!data ? <Loading /> : data.length === 0 && !creating ? (
        <Glass className="empty"><Route aria-hidden="true" /><p>No paths yet. Make one from courses in your library.</p></Glass>
      ) : (
        <div className="stack">{data.map((p) => <PathCard key={p.id} path={p} />)}</div>
      )}
    </>
  );
}

export function PathCard({ path, compact = false }: { path: LearningPath; compact?: boolean }) {
  const status = STATUS[path.status];
  return (
    <Glass as={Link} to={`/path/${path.id}`} interactive className="path-card">
      <Ring value={path.percent / 100} size={compact ? 64 : 76} label={`${path.percent}% done`} color={path.status === "behind" || path.status === "overdue" ? "var(--warning)" : path.done ? "var(--good)" : "var(--accent)"}>
        <span className="ring__big">{path.percent}%</span>
      </Ring>
      <div className="path-card__text">
        <span className="continue__eyebrow">{compact ? "Learning path" : `${path.courses.length} course${path.courses.length === 1 ? "" : "s"}`}{status.label && <span className={`tone-${status.tone}`}> · {status.label}</span>}</span>
        <span className="continue__title">{path.title}</span>
        <span className="muted">{pace(path)}</span>
        {path.next && <span className="path-card__next">Next: {path.next.title}</span>}
      </div>
      <ArrowRight className="continue__go" aria-hidden="true" />
    </Glass>
  );
}

/** One path: /path/:id */
export function PathDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: path, error, reload } = useApi<LearningPath>(`/api/paths/${id}`);
  const [editing, setEditing] = useState(false);
  if (error && !path) return <><PageHead back="/paths" backLabel="Paths" title="Path" /><div className="error-banner" role="alert">{error}</div></>;
  if (!path) return <Loading />;

  async function remove() {
    if (!window.confirm(`Delete the path "${path!.title}"? The courses stay in your library.`)) return;
    await del(`/api/paths/${path!.id}`);
    navigate("/paths");
  }

  const status = STATUS[path.status];
  return (
    <>
      <PageHead back="/paths" backLabel="Paths" eyebrow="Learning path" title={path.title} />
      <Glass className="course-hero">
        <Ring value={path.percent / 100} size={92} label={`${path.percent}% done`} color={path.done ? "var(--good)" : path.status === "behind" || path.status === "overdue" ? "var(--warning)" : "var(--accent)"}>
          <span className="ring__big">{path.percent}%</span>
        </Ring>
        <div className="course-hero__text">
          {path.description && <p>{path.description}</p>}
          <p className="muted"><CalendarClock size={14} aria-hidden="true" /> {pace(path)}</p>
          {status.label && path.target_date && <span className={`chip tone-${status.tone}`}>{status.label}</span>}
        </div>
      </Glass>
      {path.next && (
        <Glass as={Link} to={path.next.url} interactive className="continue">
          <span className="review-card__icon" aria-hidden="true">{path.next.kind === "exam" ? <BadgeCheck /> : <Route />}</span>
          <div className="continue__text">
            <span className="continue__eyebrow">Next step · {path.next.course_title}</span>
            <span className="continue__title">{path.next.title}</span>
          </div>
          <ArrowRight className="continue__go" aria-hidden="true" />
        </Glass>
      )}
      <h2 className="section-title">Courses</h2>
      <ol className="stack path-steps">
        {path.courses.map((c, i) => (
          <li key={c.id}>
            <Glass as={Link} to={`/course/${c.id}`} interactive className="path-step">
              <span className="path-step__number">{c.done ? <CircleCheck className="tone-good" aria-label="Done" /> : i + 1}</span>
              <CourseIcon icon={c.icon} id={c.id} size={44} />
              <div className="path-step__text">
                <span className="weak__title">{c.title}</span>
                <span className="muted">{c.passed} of {c.lessons} lessons · {c.exam_passed ? "exam passed" : "exam to go"}</span>
                <div className="bar bar--thin"><span style={{ width: `${c.lessons ? ((c.passed + (c.exam_passed ? 1 : 0)) / (c.lessons + 1)) * 100 : 0}%` }} /></div>
              </div>
            </Glass>
          </li>
        ))}
      </ol>
      {editing ? <PathForm path={path} onDone={() => { setEditing(false); reload(); }} /> : (
        <div className="row path-actions">
          <button type="button" className="chip chip--button" onClick={() => setEditing(true)}>Edit path</button>
          <button type="button" className="chip chip--button tone-critical" onClick={remove}><Trash2 size={14} aria-hidden="true" /> Delete path</button>
        </div>
      )}
    </>
  );
}

function PathForm({ path, onDone }: { path?: LearningPath; onDone: () => void }) {
  const courses = useApi<CourseCard[]>("/api/courses");
  const [title, setTitle] = useState(path?.title ?? "");
  const [description, setDescription] = useState(path?.description ?? "");
  const [target, setTarget] = useState(path?.target_date ?? "");
  const [picked, setPicked] = useState<string[]>(path?.courses.map((c) => c.id) ?? []);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const available = (courses.data ?? []).filter((c) => c.status === "ready" && !c.archived && !picked.includes(c.id));
  const byId = Object.fromEntries((courses.data ?? []).map((c) => [c.id, c]));

  function move(i: number, by: number) {
    const next = [...picked];
    [next[i], next[i + by]] = [next[i + by], next[i]];
    setPicked(next);
  }

  async function save(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    const body = { title, description, course_ids: picked, target_date: target || null };
    try {
      await (path ? patch(`/api/paths/${path.id}`, body) : post("/api/paths", body));
      onDone();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Couldn't save the path.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <Glass as="form" className="path-form stack" onSubmit={save}>
      <label className="field-label">Name<input className="field" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="AI leader" required minLength={2} maxLength={120} /></label>
      <label className="field-label">What it's for (optional)<input className="field" value={description} onChange={(e) => setDescription(e.target.value)} maxLength={500} /></label>
      <label className="field-label">Target date (optional)<input className="field" type="date" value={target} onChange={(e) => setTarget(e.target.value)} /></label>
      <div>
        <p className="field-label">Courses, in order</p>
        {picked.length === 0 && <p className="muted">Add courses from your library below.</p>}
        <ol className="path-pick">
          {picked.map((cid, i) => (
            <li key={cid}>
              <span>{byId[cid]?.title ?? "…"}</span>
              <button type="button" className="icon-link" onClick={() => move(i, -1)} disabled={i === 0} aria-label="Move up"><ArrowUp size={16} /></button>
              <button type="button" className="icon-link" onClick={() => move(i, 1)} disabled={i === picked.length - 1} aria-label="Move down"><ArrowDown size={16} /></button>
              <button type="button" className="icon-link" onClick={() => setPicked(picked.filter((x) => x !== cid))} aria-label="Remove"><X size={16} /></button>
            </li>
          ))}
        </ol>
        {available.length > 0 && (
          <select className="field" value="" onChange={(e) => e.target.value && setPicked([...picked, e.target.value])} aria-label="Add a course">
            <option value="">Add a course…</option>
            {available.map((c) => <option key={c.id} value={c.id}>{c.title}</option>)}
          </select>
        )}
      </div>
      {error && <div className="error-banner" role="alert">{error}</div>}
      <div className="row">
        <Glass as="button" type="submit" variant="tint" shape="pill" interactive className="button" disabled={busy || picked.length === 0 || title.trim().length < 2}>{path ? "Save" : "Create path"}</Glass>
        <button type="button" className="chip chip--button" onClick={onDone}>Cancel</button>
      </div>
    </Glass>
  );
}
