import { useState } from "react";
import { Link } from "react-router-dom";
import { CircleAlert, CircleCheck, LoaderCircle, Plus } from "lucide-react";
import { useApi } from "../api/useApi";
import type { CourseCard } from "../api/types";
import { Glass } from "../components/Glass";
import { CourseIcon } from "../components/icons";
import { NewCourse } from "../components/NewCourse";
import { Loading, PageHead } from "../components/PageHead";
import { Sheet } from "../components/Sheet";

const FILTERS = [
  { id: "active", label: "In progress", test: (c: CourseCard) => !c.archived && !c.completed_at },
  { id: "done", label: "Completed", test: (c: CourseCard) => !!c.completed_at && !c.archived },
  { id: "archived", label: "Archived", test: (c: CourseCard) => c.archived },
  { id: "all", label: "All", test: () => true },
] as const;

export function Library() {
  const { data, error } = useApi<CourseCard[]>("/api/courses", { poll: (cs) => cs.some((c) => c.status === "planning") });
  const [filter, setFilter] = useState<(typeof FILTERS)[number]["id"]>("active");
  const [creating, setCreating] = useState(false);
  const chosen = FILTERS.find((f) => f.id === filter)!;
  const shown = (data ?? []).filter(chosen.test);

  return (
    <>
      <PageHead eyebrow={data ? `${data.length} course${data.length === 1 ? "" : "s"}` : undefined} title="Library" actions={
        <Glass as="button" variant="tint" shape="pill" interactive className="button button--small" onClick={() => setCreating(true)}>
          <Plus aria-hidden="true" /> New course
        </Glass>
      } />
      <div className="chip-row" role="tablist" aria-label="Show">
        {FILTERS.map((f) => (
          <button key={f.id} type="button" role="tab" aria-selected={filter === f.id} className={`chip chip--button ${filter === f.id ? "chip--active" : ""}`} onClick={() => setFilter(f.id)}>
            {f.label} <span className="chip__count">{(data ?? []).filter(f.test).length}</span>
          </button>
        ))}
      </div>
      {error && <div className="error-banner" role="alert">{error}</div>}
      {!data ? <Loading /> : shown.length === 0 ? (
        <Glass className="empty"><p className="muted">{filter === "active" ? "Nothing in progress. Start a course on anything you're curious about." : "Nothing here yet."}</p></Glass>
      ) : (
        <div className="course-grid">{shown.map((c) => <CourseTile key={c.id} course={c} />)}</div>
      )}
      {creating && (
        <Sheet label="New course" onClose={() => setCreating(false)}>
          <h2 className="sheet__title">New course</h2>
          <NewCourse />
        </Sheet>
      )}
    </>
  );
}

export function CourseTile({ course }: { course: CourseCard }) {
  const p = course.progress;
  return (
    <Glass as={Link} to={`/course/${course.id}`} interactive className="course-tile">
      <div className="course-tile__head">
        <CourseIcon icon={course.icon} id={course.id} size={44} />
        <span className="course-tile__state">
          {course.status === "planning" && <><LoaderCircle className="spin" size={15} aria-hidden="true" /> Planning…</>}
          {course.status === "error" && <><CircleAlert size={15} className="tone-critical" aria-hidden="true" /> Needs a retry</>}
          {course.completed_at && <><CircleCheck size={15} className="tone-good" aria-hidden="true" /> Completed</>}
        </span>
      </div>
      <span className="course-tile__title">{course.title}</span>
      <span className="course-tile__meta">{cap(course.level)} · {p.lessons ? `${p.lessons} lessons` : cap(course.length)}</span>
      {course.status === "ready" && (
        <>
          <div className="bar bar--thin" aria-label={`${p.percent}% complete`}><span style={{ width: `${p.percent}%` }} /></div>
          <span className="muted course-tile__next">{course.completed_at ? `All ${p.lessons} lessons passed` : course.next_lesson ? `Next: ${course.next_lesson.title}` : ""}</span>
        </>
      )}
    </Glass>
  );
}

export function cap(s: string): string {
  return s.charAt(0).toUpperCase() + s.slice(1);
}
