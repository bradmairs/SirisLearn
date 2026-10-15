import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import { ArrowLeft, ArrowRight, CircleCheck, Clock, ListChecks, LoaderCircle, RefreshCw } from "lucide-react";
import { post } from "../api/client";
import { useApi } from "../api/useApi";
import type { LessonDetail } from "../api/types";
import { Diagram } from "../components/Diagram";
import { Glass } from "../components/Glass";
import { Markdown } from "../components/Markdown";
import { Loading, PageHead } from "../components/PageHead";

interface Attempt { id: string; finished_at: string; correct: number; total: number; score: number; xp: number }

export function Lesson() {
  const { id } = useParams();
  const { data: lesson, error, reload } = useApi<LessonDetail>(`/api/lessons/${id}`, { poll: (l) => l.status === "writing" || l.status === "pending" });
  const attempts = useApi<Attempt[]>(lesson?.status === "ready" ? `/api/lessons/${id}/attempts` : null);
  const [rewriting, setRewriting] = useState(false);

  if (error && !lesson) return <><PageHead back="/library" backLabel="Library" title="Lesson" /><div className="error-banner" role="alert">{error}</div></>;
  if (!lesson) return <Loading />;

  async function rewrite() {
    if (lesson!.status === "ready" && !window.confirm("Write this lesson again from scratch? Your scores so far are kept.")) return;
    setRewriting(true);
    try {
      await post(`/api/lessons/${lesson!.id}/regenerate`);
      reload();
    } finally {
      setRewriting(false);
    }
  }

  const c = lesson.content;
  return (
    <article className="lesson">
      <PageHead back={`/course/${lesson.course.id}`} backLabel={lesson.course.title} eyebrow={`${lesson.section} · Lesson ${lesson.number} of ${lesson.of}`} title={lesson.title} />

      {(lesson.status === "writing" || lesson.status === "pending") && (
        <Glass className="writing" aria-live="polite">
          <LoaderCircle className="spin" aria-hidden="true" />
          <div><p className="stat-card__title">Writing this lesson…</p><p className="muted">The lesson, a diagram and a 10-question quiz. Usually under two minutes.</p></div>
        </Glass>
      )}
      {lesson.status === "error" && (
        <div className="error-banner row" role="alert">
          <span style={{ flex: 1 }}>{lesson.error || "This lesson couldn't be written."}</span>
          <button type="button" className="button button--small chip--button" onClick={rewrite} disabled={rewriting}><RefreshCw size={15} aria-hidden="true" /> Retry</button>
        </div>
      )}

      {c && (
        <>
          <div className="lesson__meta">
            <span className="chip"><Clock size={13} aria-hidden="true" /> {c.minutes} min read</span>
            <span className="chip"><ListChecks size={13} aria-hidden="true" /> {c.question_count} questions</span>
            {lesson.passed_at && <span className="chip tone-good"><CircleCheck size={13} aria-hidden="true" /> Passed · best {Math.round((lesson.best_score ?? 0) * 100)}%</span>}
          </div>
          <Glass className="lesson__body">
            <Diagram svg={c.figure_svg} alt={c.figure_caption || "Lesson diagram"} caption={c.figure_caption} />
            <Markdown text={c.body} />
          </Glass>
          {c.key_points.length > 0 && (
            <Glass className="key-points">
              <h2 className="section-title">Key points</h2>
              <ul>{c.key_points.map((p, i) => <li key={i}>{p}</li>)}</ul>
            </Glass>
          )}
          <Glass className="quiz-cta">
            <div>
              <p className="stat-card__title">{lesson.passed_at ? "Retake the quiz" : "Ready? Test yourself"}</p>
              <p className="muted">{c.question_count} questions. Score 70% or more to pass and earn the lesson bonus.</p>
              {attempts.data && attempts.data.length > 0 && (
                <p className="muted">Previous: {attempts.data.slice(0, 4).map((a) => `${Math.round(a.score * 100)}%`).join(", ")}</p>
              )}
            </div>
            <Glass as={Link} to={`/lesson/${lesson.id}/quiz`} variant="tint" shape="pill" interactive className="button">
              Start quiz <ArrowRight aria-hidden="true" />
            </Glass>
          </Glass>
        </>
      )}

      <nav className="lesson__nav" aria-label="Lessons">
        {lesson.previous_id ? <Link className="chip chip--button" to={`/lesson/${lesson.previous_id}`}><ArrowLeft size={15} aria-hidden="true" /> Previous</Link> : <span />}
        {c && <button type="button" className="chip chip--button" onClick={rewrite} disabled={rewriting}><RefreshCw size={14} aria-hidden="true" /> Rewrite lesson</button>}
        {lesson.next_id ? <Link className="chip chip--button" to={`/lesson/${lesson.next_id}`}>Next <ArrowRight size={15} aria-hidden="true" /></Link> : <span />}
      </nav>
    </article>
  );
}
