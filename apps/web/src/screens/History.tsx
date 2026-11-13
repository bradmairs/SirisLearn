import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Award, BadgeCheck, BookOpen, Brain, CircleCheck, Dumbbell, Flag, GraduationCap, ListChecks, Newspaper, RefreshCw, Repeat, Route, Sparkles, Target } from "lucide-react";
import { api } from "../api/client";
import { useApi } from "../api/useApi";
import type { History as HistoryData, HistoryEvent } from "../api/types";
import { Glass } from "../components/Glass";
import { Loading, PageHead } from "../components/PageHead";
import { StreakCard } from "./Today";

const EVENTS: Record<HistoryEvent["kind"], { Icon: typeof Award; text: (e: HistoryEvent) => string }> = {
  course_created: { Icon: Sparkles, text: (e) => `Started a course on ${e.title}` },
  course_ready: { Icon: Flag, text: (e) => `Course ready: ${e.title}` },
  lesson_read: { Icon: BookOpen, text: (e) => `Read ${e.title}` },
  quiz_finished: { Icon: ListChecks, text: (e) => `Quiz: ${e.title} · ${score(e)}` },
  lesson_passed: { Icon: CircleCheck, text: (e) => `Passed ${e.title}` },
  course_completed: { Icon: GraduationCap, text: (e) => `Finished the course ${e.title}` },
  goal_met: { Icon: Target, text: (e) => `Hit your ${e.title.charAt(0).toLowerCase()}${e.title.slice(1)}` },
  achievement: { Icon: Award, text: (e) => `Unlocked ${e.title}` },
  review_finished: { Icon: Repeat, text: (e) => `${e.title} · ${score(e)}` },
  exam_finished: { Icon: BadgeCheck, text: (e) => `${e.title} · ${score(e)}${(e.detail as { passed?: boolean }).passed ? " · passed" : ""}` },
  brain_saved: { Icon: Brain, text: (e) => `Saved ${e.title} to your Second Brain` },
  practice_finished: { Icon: Dumbbell, text: (e) => `${e.title} · ${score(e)}` },
  lesson_refreshed: { Icon: RefreshCw, text: (e) => `Brought ${e.title} up to date` },
  ai_update: { Icon: Newspaper, text: (e) => `New lesson: ${e.title}` },
  path_created: { Icon: Route, text: (e) => `Set a learning path: ${e.title}` },
};

function score(e: HistoryEvent): string {
  const d = e.detail as { correct?: number; total?: number };
  return d.total ? `${Math.round(((d.correct ?? 0) / d.total) * 100)}%` : "";
}

export function History() {
  const { data, error } = useApi<HistoryData>("/api/history?days=182");
  const [events, setEvents] = useState<HistoryEvent[]>([]);
  const [before, setBefore] = useState<number | null>(null);
  useEffect(() => {
    if (data) {
      setEvents(data.events);
      setBefore(data.next_before);
    }
  }, [data]);

  async function more() {
    if (!before) return;
    const page = await api<HistoryData>(`/api/history?days=7&before=${before}`);
    setEvents((all) => [...all, ...page.events]);
    setBefore(page.next_before);
  }

  if (error) return <><PageHead title="History" /><div className="error-banner" role="alert">{error}</div></>;
  if (!data) return <Loading />;
  const s = data.stats;
  const days = groupByDay(events);
  const formatDay = (day: string) => dayLabel(day, data.today);

  return (
    <>
      <PageHead eyebrow="Your learning" title="History" />
      <div className="stat-row">
        <StreakCard streak={data.streak} />
      </div>
      <div className="stat-grid">
        <Stat value={s.xp.toLocaleString()} label="Total XP" />
        <Stat value={s.active_days} label="Active days" />
        <Stat value={s.lessons_passed} label="Lessons passed" />
        <Stat value={s.quizzes} label="Quizzes taken" />
        <Stat value={s.accuracy === null ? "–" : `${Math.round(s.accuracy * 100)}%`} label="Accuracy" />
        <Stat value={s.courses_completed} label="Courses finished" />
        <Stat value={s.goal_days} label="Goal days" />
        <Stat value={`${s.quiz_minutes} min`} label="In quizzes" />
      </div>

      <h2 className="section-title">Last six months</h2>
      <Glass className="heatmap-card">
        <Heatmap cells={data.heatmap} goal={data.goal} frozen={data.streak.frozen_days} />
      </Glass>

      <h2 className="section-title">Timeline</h2>
      {days.length === 0 ? <Glass className="empty"><p className="muted">Nothing yet. Your lessons, quizzes and awards will show up here.</p></Glass> : (
        <div className="timeline">
          {days.map(([day, items]) => (
            <section key={day} className="timeline__day">
              <h3 className="timeline__date">{formatDay(day)}<span className="muted"> · {items.reduce((n, e) => n + e.xp, 0)} XP</span></h3>
              <Glass className="timeline__list">
                {items.map((e) => {
                  const { Icon, text } = EVENTS[e.kind] ?? EVENTS.lesson_read;
                  const body = (
                    <>
                      <span className={`timeline__icon timeline__icon--${e.kind}`}><Icon size={16} aria-hidden="true" /></span>
                      <span className="item__text">
                        <span className="item__title">{text(e)}</span>
                        <span className="item__subtitle">{[e.course_title !== e.title ? e.course_title : "", time(e.ts)].filter(Boolean).join(" · ")}</span>
                      </span>
                      {e.xp > 0 && <span className="timeline__xp">+{e.xp}</span>}
                    </>
                  );
                  const to = e.lesson_id ? `/lesson/${e.lesson_id}` : e.kind === "achievement" ? "/awards" : e.course_id ? `/course/${e.course_id}` : null;
                  return to ? <Link key={e.id} to={to} className="item">{body}</Link> : <div key={e.id} className="item">{body}</div>;
                })}
              </Glass>
            </section>
          ))}
          {before && <button type="button" className="chip chip--button" onClick={more}>Show older</button>}
        </div>
      )}
    </>
  );
}

function Stat({ value, label }: { value: string | number; label: string }) {
  return <Glass className="stat"><span className="metric__value">{value}</span><span className="metric__label">{label}</span></Glass>;
}

/** Weeks as columns, Monday at the top; colour by XP against the daily goal. */
export function Heatmap({ cells, goal, frozen = [] }: { cells: { day: string; xp: number }[]; goal: number; frozen?: string[] }) {
  if (!cells.length) return null;
  const first = new Date(`${cells[0].day}T00:00:00`);
  const pad = (first.getDay() + 6) % 7;
  const padded: ({ day: string; xp: number } | null)[] = [...Array(pad).fill(null), ...cells];
  const weeks: (typeof padded)[] = [];
  for (let i = 0; i < padded.length; i += 7) weeks.push(padded.slice(i, i + 7));
  const level = (xp: number) => (xp <= 0 ? 0 : xp < goal / 2 ? 1 : xp < goal ? 2 : xp < goal * 2 ? 3 : 4);
  return (
    <div className="heatmap" role="img" aria-label={`Daily XP for the last ${cells.length} days`}>
      {weeks.map((week, w) => (
        <div key={w} className="heatmap__week">
          {week.map((cell, d) => cell ? (
            <span key={d} className={`heatmap__cell heat-${level(cell.xp)} ${frozen.includes(cell.day) ? "heatmap__cell--frozen" : ""}`}
              title={`${cell.day}: ${cell.xp} XP${frozen.includes(cell.day) ? " (streak freeze)" : ""}`} />
          ) : <span key={d} className="heatmap__cell heatmap__cell--pad" />)}
        </div>
      ))}
      <div className="heatmap__legend muted">Less <span className="heatmap__cell heat-0" /><span className="heatmap__cell heat-1" /><span className="heatmap__cell heat-2" /><span className="heatmap__cell heat-3" /><span className="heatmap__cell heat-4" /> More{frozen.length > 0 && <> · <span className="heatmap__cell heatmap__cell--frozen" /> Freeze</>}</div>
    </div>
  );
}

function groupByDay(events: HistoryEvent[]): [string, HistoryEvent[]][] {
  const out = new Map<string, HistoryEvent[]>();
  for (const e of events) out.set(e.day, [...(out.get(e.day) ?? []), e]);
  return [...out.entries()];
}

/** "Today", "Yesterday" or a date, counted from the server's day (the
 * app's time zone), not the browser's. */
export function dayLabel(day: string, today: string): string {
  const date = new Date(`${day}T00:00:00`);
  const diff = Math.round((new Date(`${today}T00:00:00`).getTime() - date.getTime()) / 86400000);
  if (diff === 0) return "Today";
  if (diff === 1) return "Yesterday";
  return date.toLocaleDateString(undefined, { weekday: "short", day: "numeric", month: "short", year: day.slice(0, 4) === today.slice(0, 4) ? undefined : "numeric" });
}

function time(ts: string): string {
  return new Date(ts).toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" });
}
