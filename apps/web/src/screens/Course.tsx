import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { Archive, ArchiveRestore, ChevronRight, CircleAlert, CircleCheck, LoaderCircle, RefreshCw, Trash2 } from "lucide-react";
import { del, patch, post } from "../api/client";
import { useApi } from "../api/useApi";
import type { CourseDetail, LessonSummary } from "../api/types";
import { Glass } from "../components/Glass";
import { CourseIcon } from "../components/icons";
import { Loading, PageHead } from "../components/PageHead";
import { Ring } from "../components/Ring";
import { cap } from "./Library";

const busy = (c: CourseDetail) => c.status === "planning" || c.sections.some((s) => s.lessons.some((l) => l.status === "writing"));

export function Course() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: course, error, reload } = useApi<CourseDetail>(`/api/courses/${id}`, { poll: busy });
  const [working, setWorking] = useState(false);

  if (error && !course) return <><PageHead back="/library" backLabel="Library" title="Course" /><div className="error-banner" role="alert">{error}</div></>;
  if (!course) return <Loading />;

  async function act(fn: () => Promise<unknown>) {
    setWorking(true);
    try {
      await fn();
      reload();
    } finally {
      setWorking(false);
    }
  }
  async function remove() {
    if (!window.confirm(`Delete "${course!.title}"? Your history and awards stay.`)) return;
    await del(`/api/courses/${course!.id}`);
    navigate("/library");
  }

  const failed = course.sections.flatMap((s) => s.lessons).filter((l) => l.status === "error").length;
  let number = 0;

  return (
    <>
      <PageHead back="/library" backLabel="Library" eyebrow={`${cap(course.level)} · ${course.progress.lessons || "…"} lessons`} title={course.title} />
      <Glass className="course-hero">
        <CourseIcon icon={course.icon} id={course.id} size={64} />
        <div className="course-hero__text">
          <p>{course.summary || `Planning a course on "${course.topic}"…`}</p>
          {course.notes && <p className="muted">Your notes: {course.notes}</p>}
        </div>
        {course.status === "ready" && (
          <Ring value={course.progress.percent / 100} size={84} label={`${course.progress.percent}% complete`} color={course.completed_at ? "var(--good)" : "var(--accent)"}>
            <span className="ring__big">{course.progress.percent}%</span>
          </Ring>
        )}
      </Glass>

      {course.status === "planning" && (
        <Glass className="writing" aria-live="polite">
          <LoaderCircle className="spin" aria-hidden="true" />
          <div><p className="stat-card__title">Planning your course…</p><p className="muted">Working out the sections and lessons. This takes about a minute.</p></div>
        </Glass>
      )}
      {course.status === "error" && (
        <div className="error-banner row" role="alert">
          <span style={{ flex: 1 }}>{course.error}</span>
          <button type="button" className="button button--small chip--button" onClick={() => act(() => post(`/api/courses/${course.id}/retry`))} disabled={working}><RefreshCw size={15} aria-hidden="true" /> Retry</button>
        </div>
      )}
      {failed > 0 && course.status === "ready" && (
        <div className="warning-banner row" role="status">
          <span style={{ flex: 1 }}>{failed} lesson{failed === 1 ? "" : "s"} couldn't be written.</span>
          <button type="button" className="button button--small chip--button" onClick={() => act(() => post(`/api/courses/${course.id}/retry`))} disabled={working}><RefreshCw size={15} aria-hidden="true" /> Retry</button>
        </div>
      )}

      {course.sections.map((section, s) => (
        <section key={s} className="course-section">
          <h2 className="section-title">Section {s + 1} · {section.title}</h2>
          {section.summary && <p className="muted course-section__summary">{section.summary}</p>}
          <Glass className="lesson-list">
            {section.lessons.map((lesson) => {
              number += 1;
              return <LessonRow key={lesson.id} lesson={lesson} number={number} next={course.next_lesson?.id === lesson.id} />;
            })}
          </Glass>
        </section>
      ))}

      <div className="row course-actions">
        <button type="button" className="chip chip--button" onClick={() => act(() => patch(`/api/courses/${course.id}`, { archived: !course.archived }))} disabled={working}>
          {course.archived ? <><ArchiveRestore size={15} aria-hidden="true" /> Unarchive</> : <><Archive size={15} aria-hidden="true" /> Archive</>}
        </button>
        <button type="button" className="chip chip--button chip--danger" onClick={remove}><Trash2 size={15} aria-hidden="true" /> Delete</button>
      </div>
    </>
  );
}

function LessonRow({ lesson, number, next }: { lesson: LessonSummary; number: number; next: boolean }) {
  const passed = !!lesson.passed_at;
  return (
    <Link to={`/lesson/${lesson.id}`} className={`lesson-row ${next ? "lesson-row--next" : ""}`}>
      <span className={`lesson-row__num ${passed ? "lesson-row__num--done" : ""}`} aria-hidden="true">
        {passed ? <CircleCheck size={18} /> : number}
      </span>
      <span className="lesson-row__text">
        <span className="lesson-row__title">{lesson.title}</span>
        <span className="lesson-row__summary">{lesson.summary}</span>
      </span>
      <span className="lesson-row__status">
        {lesson.status === "writing" && <><LoaderCircle className="spin" size={14} aria-hidden="true" /> Writing</>}
        {lesson.status === "error" && <CircleAlert size={16} className="tone-critical" aria-label="Couldn't be written" />}
        {lesson.best_score !== null && <span className={passed ? "tone-good" : "tone-warning"}>{Math.round(lesson.best_score * 100)}%</span>}
        {next && !passed && <span className="chip chip--tiny">Up next</span>}
      </span>
      <ChevronRight size={18} className="lesson-row__go" aria-hidden="true" />
    </Link>
  );
}
