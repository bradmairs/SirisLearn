import { Link } from "react-router-dom";
import { ArrowRight, BookOpen, Dumbbell, Target, TrendingUp } from "lucide-react";
import { useApi } from "../api/useApi";
import type { Insights as InsightsData, WeakSpot } from "../api/types";
import { Glass } from "../components/Glass";
import { CourseIcon } from "../components/icons";
import { Loading, PageHead } from "../components/PageHead";

const pct = (n: number) => `${Math.round(n * 100)}%`;

/** Weak spots: /insights */
export function Insights() {
  const { data, error } = useApi<InsightsData>("/api/insights");
  return (
    <>
      <PageHead eyebrow={data ? `Your last ${data.days} days` : "Progress"} title="Weak spots" />
      {error && <div className="error-banner" role="alert">{error}</div>}
      {!data ? <Loading /> : data.answered === 0 ? (
        <Glass className="empty"><Target aria-hidden="true" /><p>Answer a few quizzes and your weak spots show up here.</p></Glass>
      ) : (
        <>
          {data.kinds.length > 0 && (
            <Glass className="kind-bars">
              <h2 className="section-title">By kind of question</h2>
              {data.kinds.map((k) => (
                <div key={k.kind} className="kind-bars__row">
                  <span className="kind-bars__label">{k.label}</span>
                  <div className="bar" role="progressbar" aria-valuenow={Math.round(k.accuracy * 100)} aria-valuemax={100} aria-label={`${k.label}: ${pct(k.accuracy)}`}>
                    <span style={{ width: `${k.accuracy * 100}%`, background: k.accuracy < data.weak_below ? "var(--warning)" : undefined }} />
                  </div>
                  <span className="kind-bars__value">{pct(k.accuracy)}<span className="muted"> · {k.answered}</span></span>
                </div>
              ))}
            </Glass>
          )}

          <h2 className="section-title">Lessons to work on</h2>
          {data.weak.length === 0 ? (
            <Glass className="empty"><TrendingUp aria-hidden="true" /><p>No weak spots: every lesson with {data.min_answers}+ answers is at {pct(data.weak_below)} or better.</p></Glass>
          ) : (
            <div className="stack">{data.weak.map((w) => <WeakSpotCard key={w.lesson_id} spot={w} />)}</div>
          )}

          {data.strong.length > 0 && (
            <>
              <h2 className="section-title">Going well</h2>
              <div className="stack">
                {data.strong.map((s) => (
                  <Glass key={s.lesson_id} as={Link} to={`/lesson/${s.lesson_id}`} interactive className="weak weak--strong">
                    <CourseIcon icon={s.icon} id={s.course_id} size={40} />
                    <div className="weak__text"><span className="weak__title">{s.title}</span><span className="muted">{s.course_title}</span></div>
                    <span className="weak__score tone-good">{pct(s.accuracy)}</span>
                  </Glass>
                ))}
              </div>
            </>
          )}
        </>
      )}
    </>
  );
}

export function WeakSpotCard({ spot, compact = false }: { spot: WeakSpot; compact?: boolean }) {
  return (
    <Glass className="weak">
      <CourseIcon icon={spot.icon} id={spot.course_id} size={compact ? 40 : 48} />
      <div className="weak__text">
        {compact && <span className="continue__eyebrow">Weak spot</span>}
        <span className="weak__title">{spot.title}</span>
        <span className="muted">{spot.course_title} · {pct(spot.accuracy)} right over {spot.answered} answers{spot.missed ? ` · ${spot.missed} to relearn` : ""}</span>
        <div className="bar bar--thin"><span style={{ width: `${spot.accuracy * 100}%`, background: "var(--warning)" }} /></div>
      </div>
      <div className="weak__actions">
        {spot.ready && <Glass as={Link} to={`/lesson/${spot.lesson_id}/practice`} variant="tint" shape="pill" interactive className="button button--small"><Dumbbell aria-hidden="true" /> Practise</Glass>}
        {!compact && <Link to={`/lesson/${spot.lesson_id}`} className="chip chip--button"><BookOpen size={14} aria-hidden="true" /> Re-read</Link>}
        {compact && <Link to="/insights" className="chip chip--button">All <ArrowRight size={14} aria-hidden="true" /></Link>}
      </div>
    </Glass>
  );
}
