import { useEffect, useState } from "react";
import { LogOut } from "lucide-react";
import { put } from "../api/client";
import { useApi } from "../api/useApi";
import type { Settings as SettingsData } from "../api/types";
import { Glass } from "../components/Glass";
import { Loading, PageHead } from "../components/PageHead";

const GOALS = [{ xp: 20, label: "Casual" }, { xp: 50, label: "Regular" }, { xp: 100, label: "Serious" }, { xp: 200, label: "Intense" }];

export function Settings({ onSignOut }: { onSignOut: () => void }) {
  const { data, error, setData } = useApi<SettingsData>("/api/settings");
  const [goal, setGoal] = useState(50);
  const [saved, setSaved] = useState(false);
  useEffect(() => {
    if (data) setGoal(data.daily_goal);
  }, [data]);

  async function save(xp: number) {
    setGoal(xp);
    setSaved(false);
    setData(await put<SettingsData>("/api/settings", { daily_goal: xp }));
    setSaved(true);
  }

  if (error) return <><PageHead title="Settings" /><div className="error-banner" role="alert">{error}</div></>;
  if (!data) return <Loading />;
  return (
    <>
      <PageHead title="Settings" />
      <h2 className="section-title">Daily goal</h2>
      <Glass className="settings-card stack">
        <p className="muted">XP to earn each day. A quiz is worth up to about 150 XP.</p>
        <div className="chip-row" role="radiogroup" aria-label="Daily goal">
          {GOALS.map((g) => (
            <button key={g.xp} type="button" role="radio" aria-checked={goal === g.xp} className={`chip chip--button ${goal === g.xp ? "chip--active" : ""}`} onClick={() => save(g.xp)}>
              {g.label} · {g.xp} XP
            </button>
          ))}
        </div>
        {saved && <p className="muted tone-good" role="status">Saved.</p>}
      </Glass>

      <h2 className="section-title">Course writer</h2>
      <Glass className="settings-card stack">
        {data.llm.configured ? (
          <p>Courses are written by <b>{data.llm.provider === "anthropic" ? "Claude" : data.llm.provider}</b>{data.llm.model ? <> (<code>{data.llm.model}</code>)</> : null}.</p>
        ) : (
          <div className="warning-banner">No model is set up, so new courses can't be written yet. Add <code>ANTHROPIC_API_KEY</code> (or an Ollama model) to the server's <code>.env</code> and restart.</div>
        )}
      </Glass>

      <h2 className="section-title">Account</h2>
      <Glass as="button" type="button" shape="pill" interactive className="button" onClick={onSignOut}><LogOut aria-hidden="true" /> Sign out</Glass>
    </>
  );
}
