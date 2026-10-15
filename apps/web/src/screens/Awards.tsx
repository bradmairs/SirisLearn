import { Lock, Zap } from "lucide-react";
import { useApi } from "../api/useApi";
import type { Achievement, LevelInfo, Streak } from "../api/types";
import { Glass } from "../components/Glass";
import { iconFor } from "../components/icons";
import { Loading, PageHead } from "../components/PageHead";
import { StreakCard } from "./Today";

interface Board { achievements: Achievement[]; unlocked: number; total: number; level: LevelInfo; streak: Streak }

export function Awards() {
  const { data, error } = useApi<Board>("/api/achievements");
  if (error) return <><PageHead title="Awards" /><div className="error-banner" role="alert">{error}</div></>;
  if (!data) return <Loading />;
  return (
    <>
      <PageHead eyebrow={`${data.unlocked} of ${data.total} unlocked`} title="Awards" />
      <div className="stat-row">
        <Glass className="stat-card">
          <span className="level-badge" aria-hidden="true"><Zap /></span>
          <div style={{ flex: 1, minWidth: 0 }}>
            <p className="stat-card__title">Level {data.level.level}</p>
            <div className="bar"><span style={{ width: `${data.level.progress * 100}%` }} /></div>
            <p className="muted">{data.level.xp_for_next - data.level.xp_into} XP to level {data.level.level + 1}</p>
          </div>
        </Glass>
        <StreakCard streak={data.streak} />
      </div>
      <div className="award-grid">
        {data.achievements.map((a) => <AwardCard key={a.id} award={a} />)}
      </div>
    </>
  );
}

function AwardCard({ award }: { award: Achievement }) {
  const Icon = iconFor(award.icon);
  const unlocked = !!award.unlocked_at;
  return (
    <Glass className={`award ${unlocked ? `award--on tier-${award.tier}` : "award--off"}`}>
      <span className="award__icon" aria-hidden="true">{unlocked ? <Icon /> : <Lock />}</span>
      <span className="award__title">{award.title}</span>
      <span className="award__desc">{award.description}</span>
      {unlocked ? (
        <span className="award__when">{award.tier} · {new Date(award.unlocked_at!).toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" })}</span>
      ) : (
        <>
          <div className="bar bar--thin" aria-label={`${award.value} of ${award.target}`}><span style={{ width: `${(award.value / award.target) * 100}%` }} /></div>
          <span className="award__when">{award.value.toLocaleString()} / {award.target.toLocaleString()}</span>
        </>
      )}
    </Glass>
  );
}
