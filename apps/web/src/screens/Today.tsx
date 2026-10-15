import { Link } from "react-router-dom";
import { ArrowRight, Award, CircleCheck, Flame, Zap } from "lucide-react";
import { useApi } from "../api/useApi";
import type { CourseCard, Summary } from "../api/types";
import { Glass } from "../components/Glass";
import { CourseIcon, iconFor } from "../components/icons";
import { NewCourse } from "../components/NewCourse";
import { Loading, PageHead } from "../components/PageHead";
import { Ring } from "../components/Ring";
import { CourseTile } from "./Library";

function greeting(): string {
  const h = new Date().getHours();
  return h < 5 ? "Up late" : h < 12 ? "Good morning" : h < 18 ? "Good afternoon" : "Good evening";
}

export function Today({ user }: { user: string }) {
  const summary = useApi<Summary>("/api/summary", { poll: (s) => s.courses.planning > 0, pollMs: 4000 });
  const courses = useApi<CourseCard[]>("/api/courses", { poll: (cs) => cs.some((c) => c.status === "planning"), pollMs: 4000 });
  const s = summary.data;
  const name = user.charAt(0).toUpperCase() + user.slice(1);
  const active = (courses.data ?? []).filter((c) => !c.archived && !c.completed_at).slice(0, 4);

  return (
    <>
      <PageHead eyebrow={`${greeting()}, ${name}`} title="Today" />
      {summary.error && <div className="error-banner" role="alert">{summary.error}</div>}
      {!s ? <Loading /> : (
        <>
          <div className="stat-row">
            <StreakCard streak={s.streak} />
            <Glass className="stat-card">
              <Ring value={s.xp.today / s.xp.goal} label={`${s.xp.today} of ${s.xp.goal} XP today`} color={s.xp.goal_met ? "var(--good)" : "var(--accent)"}>
                <span className="ring__big">{s.xp.today}</span>
                <span className="ring__small">/ {s.xp.goal} XP</span>
              </Ring>
              <div>
                <p className="stat-card__title">{s.xp.goal_met ? "Daily goal met" : "Daily goal"}</p>
                <p className="muted">{s.xp.goal_met ? "Nice work. Anything more is a bonus." : `${s.xp.goal - s.xp.today} XP to go today`}</p>
              </div>
            </Glass>
            <Glass className="stat-card">
              <span className="level-badge" aria-hidden="true"><Zap /></span>
              <div style={{ flex: 1, minWidth: 0 }}>
                <p className="stat-card__title">Level {s.level.level}</p>
                <div className="bar" role="progressbar" aria-valuenow={s.level.xp_into} aria-valuemax={s.level.xp_for_next} aria-label="Progress to next level">
                  <span style={{ width: `${s.level.progress * 100}%` }} />
                </div>
                <p className="muted">{s.level.xp_for_next - s.level.xp_into} XP to level {s.level.level + 1} · {s.xp.total.toLocaleString()} total</p>
              </div>
            </Glass>
          </div>

          {s.continue && (
            <Glass as={Link} to={`/lesson/${s.continue.lesson_id}`} interactive className="continue">
              <CourseIcon icon={s.continue.icon} id={s.continue.course_id} size={56} />
              <div className="continue__text">
                <span className="continue__eyebrow">Continue · {s.continue.course_title}</span>
                <span className="continue__title">{s.continue.lesson_title}</span>
                <div className="bar bar--thin"><span style={{ width: `${s.continue.progress.percent}%` }} /></div>
                <span className="muted">{s.continue.progress.passed} of {s.continue.progress.lessons} lessons passed</span>
              </div>
              <ArrowRight className="continue__go" aria-hidden="true" />
            </Glass>
          )}
        </>
      )}

      <h2 className="section-title">Learn something new</h2>
      <NewCourse compact />

      {active.length > 0 && (
        <>
          <div className="section-head">
            <h2 className="section-title">Your courses</h2>
            <Link to="/library" className="see-all">See all</Link>
          </div>
          <div className="course-grid">{active.map((c) => <CourseTile key={c.id} course={c} />)}</div>
        </>
      )}

      {s && s.achievements.recent.length > 0 && (
        <>
          <div className="section-head">
            <h2 className="section-title">Recent awards</h2>
            <Link to="/awards" className="see-all">{s.achievements.unlocked} of {s.achievements.total}</Link>
          </div>
          <div className="award-strip">
            {s.achievements.recent.map((a) => {
              const Icon = iconFor(a.icon);
              return (
                <Glass key={a.id} as={Link} to="/awards" className="award-chip">
                  <Icon aria-hidden="true" /> <span>{a.title}</span>
                </Glass>
              );
            })}
            <Glass as={Link} to="/awards" className="award-chip award-chip--more"><Award aria-hidden="true" /> <span>All awards</span></Glass>
          </div>
        </>
      )}
    </>
  );
}

export function StreakCard({ streak }: { streak: Summary["streak"] }) {
  const lit = streak.current > 0;
  return (
    <Glass className={`stat-card streak ${lit ? "streak--lit" : ""} ${streak.at_risk ? "streak--risk" : ""}`}>
      <span className="streak__flame" aria-hidden="true"><Flame /></span>
      <div>
        <p className="stat-card__title"><span className="streak__count">{streak.current}</span> day streak</p>
        <p className="muted">
          {streak.today_done ? <><CircleCheck size={14} className="tone-good" aria-hidden="true" /> Done for today</> :
            streak.at_risk ? "Finish a quiz today to keep it going" :
              "Finish a quiz to start a streak"}
        </p>
        {streak.best > 0 && <p className="muted">Best: {streak.best} day{streak.best === 1 ? "" : "s"}</p>}
      </div>
    </Glass>
  );
}
