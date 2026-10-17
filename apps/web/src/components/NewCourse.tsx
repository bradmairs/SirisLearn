import { useEffect, useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { Brain, ChevronDown, Sparkles } from "lucide-react";
import { api, post } from "../api/client";
import type { CourseCard, Length, Level } from "../api/types";
import { Glass } from "./Glass";

const LEVELS: { id: Level; label: string }[] = [
  { id: "beginner", label: "Beginner" },
  { id: "intermediate", label: "Intermediate" },
  { id: "advanced", label: "Advanced" },
];
const LENGTHS: { id: Length; label: string; hint: string }[] = [
  { id: "short", label: "Short", hint: "about 6 lessons" },
  { id: "standard", label: "Standard", hint: "about 14 lessons" },
  { id: "deep", label: "Deep dive", hint: "about 24 lessons" },
];
const PLACEHOLDERS = ["How black holes form", "Personal finance basics", "Stoic philosophy", "Machine learning fundamentals"];

/** "What do you want to learn?" A topic, a level and a size become a course. */
export function NewCourse({ compact = false }: { compact?: boolean }) {
  const navigate = useNavigate();
  const [topic, setTopic] = useState("");
  const [level, setLevel] = useState<Level>("beginner");
  const [length, setLength] = useState<Length>("standard");
  const [notes, setNotes] = useState("");
  const [more, setMore] = useState(!compact);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [ideas, setIdeas] = useState<{ source: string; ideas: string[] } | null>(null);
  useEffect(() => {
    api<{ source: string; ideas: string[] }>("/api/suggestions").then(setIdeas).catch(() => undefined);
  }, []);

  async function submit(e: FormEvent) {
    e.preventDefault();
    if (topic.trim().length < 2) return;
    setBusy(true);
    setError(null);
    try {
      const course = await post<CourseCard>("/api/courses", { topic: topic.trim(), level, length, notes: notes.trim() });
      navigate(`/course/${course.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Couldn't start the course.");
      setBusy(false);
    }
  }

  return (
    <Glass as="form" className="new-course" onSubmit={submit} aria-label="Start a new course">
      <label className="new-course__label" htmlFor="topic">What do you want to learn?</label>
      <div className="new-course__row">
        <Sparkles className="new-course__spark" aria-hidden="true" />
        <input id="topic" className="new-course__input" placeholder={PLACEHOLDERS[new Date().getDate() % PLACEHOLDERS.length]} value={topic}
          onChange={(e) => setTopic(e.target.value)} onFocus={() => setMore(true)} maxLength={300} autoComplete="off" />
        <Glass as="button" type="submit" variant="tint" shape="pill" interactive className="button button--small" disabled={busy || topic.trim().length < 2}>
          {busy ? "Starting…" : "Create"}
        </Glass>
      </div>
      {ideas && ideas.ideas.length > 0 && !topic && (
        <div className="chip-row new-course__ideas" aria-label="Ideas">
          {ideas.source === "brain" && <span className="new-course__from"><Brain size={13} aria-hidden="true" /> From your Second Brain</span>}
          {ideas.ideas.map((idea) => (
            <button key={idea} type="button" className="chip chip--button" onClick={() => { setTopic(idea); setMore(true); }}>{idea}</button>
          ))}
        </div>
      )}
      {more && (
        <div className="new-course__options">
          <div className="chip-row" role="radiogroup" aria-label="Level">
            {LEVELS.map((l) => (
              <button key={l.id} type="button" role="radio" aria-checked={level === l.id} className={`chip chip--button ${level === l.id ? "chip--active" : ""}`} onClick={() => setLevel(l.id)}>{l.label}</button>
            ))}
          </div>
          <div className="chip-row" role="radiogroup" aria-label="Course size">
            {LENGTHS.map((l) => (
              <button key={l.id} type="button" role="radio" aria-checked={length === l.id} title={l.hint} className={`chip chip--button ${length === l.id ? "chip--active" : ""}`} onClick={() => setLength(l.id)}>{l.label}</button>
            ))}
          </div>
          <details className="new-course__notes">
            <summary>Anything to focus on or skip? <ChevronDown size={14} aria-hidden="true" /></summary>
            <textarea className="field" rows={3} maxLength={2000} placeholder="e.g. I'm an engineer, go heavy on the maths; skip the history." value={notes} onChange={(e) => setNotes(e.target.value)} />
          </details>
        </div>
      )}
      {error && <div className="error-banner" role="alert">{error}</div>}
    </Glass>
  );
}
