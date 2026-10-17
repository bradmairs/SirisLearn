import { useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { BadgeCheck, CircleAlert, CircleCheck, LayoutGrid, LoaderCircle, Map as MapIcon, Plus } from "lucide-react";
import { useApi } from "../api/useApi";
import type { CourseCard } from "../api/types";
import { Glass } from "../components/Glass";
import { AREAS, CourseIcon } from "../components/icons";
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
  const [params, setParams] = useSearchParams();
  const area = params.get("area");
  const view = params.get("view") === "map" ? "map" : "grid";
  const chosen = FILTERS.find((f) => f.id === filter)!;
  const shown = (data ?? []).filter(chosen.test).filter((c) => !area || c.area === area);
  const areas = [...new Set((data ?? []).map((c) => c.area).filter(Boolean))].sort();
  const set = (key: string, value: string | null) => {
    const next = new URLSearchParams(params);
    if (value) next.set(key, value);
    else next.delete(key);
    setParams(next, { replace: true });
  };

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
      {areas.length > 1 && (
        <div className="chip-row" aria-label="Area">
          <button type="button" className={`chip chip--button ${!area ? "chip--active" : ""}`} onClick={() => set("area", null)}>All areas</button>
          {areas.map((a) => (
            <button key={a} type="button" className={`chip chip--button ${area === a ? "chip--active" : ""}`} onClick={() => set("area", area === a ? null : a)}>{AREAS[a] ?? a}</button>
          ))}
          <span className="spacer" />
          <button type="button" className="chip chip--button" onClick={() => set("view", view === "map" ? null : "map")} aria-pressed={view === "map"}>
            {view === "map" ? <><LayoutGrid size={14} aria-hidden="true" /> Grid</> : <><MapIcon size={14} aria-hidden="true" /> Map</>}
          </button>
        </div>
      )}
      {error && <div className="error-banner" role="alert">{error}</div>}
      {!data ? <Loading /> : shown.length === 0 ? (
        <Glass className="empty"><p className="muted">{filter === "active" ? "Nothing in progress. Start a course on anything you're curious about." : "Nothing here yet."}</p></Glass>
      ) : (
        view === "map" ? <CourseMap courses={shown} /> : <div className="course-grid">{shown.map((c) => <CourseTile key={c.id} course={c} />)}</div>
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
          {course.exam_passed_at ? <><BadgeCheck size={15} className="tone-good" aria-hidden="true" /> Certified</> :
            course.completed_at && <><CircleCheck size={15} className="tone-good" aria-hidden="true" /> Completed</>}
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

/** Courses grouped by area, in level order, so you can see how they fit together. */
function CourseMap({ courses }: { courses: CourseCard[] }) {
  const order = { beginner: 0, intermediate: 1, advanced: 2 } as const;
  const groups = new Map<string, CourseCard[]>();
  for (const c of courses) groups.set(c.area || "other", [...(groups.get(c.area || "other") ?? []), c]);
  return (
    <div className="course-map">
      {[...groups.entries()].sort().map(([area, list]) => (
        <Glass key={area} className="course-map__area">
          <h2 className="section-title">{AREAS[area] ?? area}</h2>
          <ol className="course-map__list">
            {list.sort((a, b) => order[a.level] - order[b.level] || a.title.localeCompare(b.title)).map((c) => (
              <li key={c.id}>
                <Link to={`/course/${c.id}`} className="course-map__item">
                  <CourseIcon icon={c.icon} id={c.id} size={34} />
                  <span className="course-map__text"><b>{c.title}</b><span className="muted">{cap(c.level)} · {c.progress.percent}%{c.exam_passed_at ? " · certified" : ""}</span></span>
                  <span className={`course-map__level course-map__level--${c.level}`} aria-hidden="true" />
                </Link>
              </li>
            ))}
          </ol>
        </Glass>
      ))}
    </div>
  );
}

export function cap(s: string): string {
  return s.charAt(0).toUpperCase() + s.slice(1);
}
