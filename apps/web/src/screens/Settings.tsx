import { useEffect, useState } from "react";
import { Bell, BellOff, Brain, LogOut } from "lucide-react";
import { post, put } from "../api/client";
import { currentSubscription, disablePush, enablePush, pushSupported } from "../api/push";
import { useApi } from "../api/useApi";
import type { Settings as SettingsData } from "../api/types";
import { Glass } from "../components/Glass";
import { Loading, PageHead } from "../components/PageHead";

const GOALS = [{ xp: 20, label: "Casual" }, { xp: 50, label: "Regular" }, { xp: 100, label: "Serious" }, { xp: 200, label: "Intense" }];
const PURPOSES: Record<string, string> = { plan: "Planning courses", lesson: "Writing lessons", questions: "Fresh retake questions", mark: "Marking written answers", tutor: "Ask Siris" };

function money(n: number): string {
  return n < 0.01 && n > 0 ? "< $0.01" : `$${n.toFixed(2)}`;
}

function hour(h: number): string {
  return new Date(2000, 0, 1, h).toLocaleTimeString(undefined, { hour: "numeric" });
}

export function Settings({ onSignOut }: { onSignOut: () => void }) {
  const { data, error, setData } = useApi<SettingsData>("/api/settings");
  const [goal, setGoal] = useState(50);
  const [saved, setSaved] = useState(false);
  const [pushOn, setPushOn] = useState<boolean | null>(null);
  const [pushBusy, setPushBusy] = useState(false);
  const [pushNote, setPushNote] = useState<string | null>(null);
  useEffect(() => {
    if (data) setGoal(data.daily_goal);
  }, [data]);
  useEffect(() => {
    currentSubscription().then((s) => setPushOn(!!s)).catch(() => setPushOn(false));
  }, []);

  async function save(body: Record<string, unknown>) {
    setSaved(false);
    setData(await put<SettingsData>("/api/settings", body));
    setSaved(true);
  }

  async function togglePush() {
    setPushBusy(true);
    setPushNote(null);
    try {
      if (pushOn) {
        await disablePush();
        setPushOn(false);
      } else {
        await enablePush();
        setPushOn(true);
        await post("/api/push/test");
        setPushNote("Sent a test notification.");
      }
    } catch (err) {
      setPushNote(err instanceof Error ? err.message : "Couldn't change notifications.");
    } finally {
      setPushBusy(false);
    }
  }

  if (error) return <><PageHead title="Settings" /><div className="error-banner" role="alert">{error}</div></>;
  if (!data) return <Loading />;
  const u = data.usage;
  return (
    <>
      <PageHead title="Settings" />
      <h2 className="section-title">Daily goal</h2>
      <Glass className="settings-card stack">
        <p className="muted">XP to earn each day. A quiz is worth up to about 150 XP; the daily review up to 60.</p>
        <div className="chip-row" role="radiogroup" aria-label="Daily goal">
          {GOALS.map((g) => (
            <button key={g.xp} type="button" role="radio" aria-checked={goal === g.xp} className={`chip chip--button ${goal === g.xp ? "chip--active" : ""}`} onClick={() => { setGoal(g.xp); void save({ daily_goal: g.xp }); }}>
              {g.label} · {g.xp} XP
            </button>
          ))}
        </div>
        {saved && <p className="muted tone-good" role="status">Saved.</p>}
      </Glass>

      <h2 className="section-title">Notifications</h2>
      <Glass className="settings-card stack">
        <p className="muted">A reminder at {hour(data.push.reminder_hour)} when your streak would end at midnight, and at {hour(data.push.review_hour)} when cards are due for review.</p>
        {pushSupported() ? (
          <Glass as="button" type="button" shape="pill" interactive className="button button--small" onClick={togglePush} disabled={pushBusy || pushOn === null}>
            {pushOn ? <><BellOff aria-hidden="true" /> Turn off on this device</> : <><Bell aria-hidden="true" /> Turn on for this device</>}
          </Glass>
        ) : (
          <p className="warning-banner">This browser can't receive notifications. On iPhone, add SirisLearn to your home screen (Share, Add to Home Screen) and open it from there.</p>
        )}
        {pushNote && <p className="muted" role="status">{pushNote}</p>}
      </Glass>

      <h2 className="section-title">Second Brain</h2>
      <Glass className="settings-card stack">
        {data.brain.configured ? (
          <>
            <p className="muted">When you pass a lesson, its key points are saved to your Second Brain, where Siris files and links them.</p>
            <label className="toggle">
              <input type="checkbox" checked={data.brain.enabled} onChange={(e) => void save({ brain_capture: e.target.checked })} />
              <span><Brain size={15} aria-hidden="true" /> Save passed lessons to the Second Brain</span>
            </label>
          </>
        ) : (
          <p className="muted">Link SirisAI (<code>SIRISAI_URL</code> and <code>SIRISAI_API_KEY</code> in the server's <code>.env</code>) to save what you learn to your Second Brain and get topic ideas from it.</p>
        )}
      </Glass>

      <h2 className="section-title">Course writer</h2>
      <Glass className="settings-card stack">
        {data.llm.configured ? (
          <p>Courses are written by <b>{data.llm.provider === "anthropic" ? "Claude" : data.llm.provider}</b>{data.llm.model ? <> (<code>{data.llm.model}</code>)</> : null}.</p>
        ) : (
          <div className="warning-banner">No model is set up, so new courses can't be written yet. Add <code>ANTHROPIC_API_KEY</code> (or an Ollama model) to the server's <code>.env</code> and restart.</div>
        )}
        <div className="usage">
          <div className="usage__totals">
            <span><b>{money(u.month)}</b><span className="metric__label">This month</span></span>
            <span><b>{money(u.cost)}</b><span className="metric__label">All time</span></span>
            <span><b>{u.calls.toLocaleString()}</b><span className="metric__label">Model calls</span></span>
          </div>
          {u.by_purpose.length > 0 && (
            <table className="usage__table">
              <tbody>
                {u.by_purpose.map((p) => <tr key={p.purpose}><td>{PURPOSES[p.purpose] ?? p.purpose}</td><td>{p.calls}</td><td>{money(p.cost)}</td></tr>)}
              </tbody>
            </table>
          )}
          {u.by_course.length > 0 && (
            <>
              <p className="metric__label">Most expensive courses</p>
              <table className="usage__table">
                <tbody>
                  {u.by_course.map((c) => <tr key={c.course_id}><td>{c.title}</td><td>{c.calls}</td><td>{money(c.cost)}</td></tr>)}
                </tbody>
              </table>
            </>
          )}
          <p className="muted">Estimated from token counts at list prices; your Anthropic bill is the final word.</p>
        </div>
      </Glass>

      <h2 className="section-title">Account</h2>
      <Glass as="button" type="button" shape="pill" interactive className="button" onClick={onSignOut}><LogOut aria-hidden="true" /> Sign out</Glass>
    </>
  );
}
