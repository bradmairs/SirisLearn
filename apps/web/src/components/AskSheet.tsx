import { useState, type FormEvent } from "react";
import { ArrowUpRight, Sparkles } from "lucide-react";
import { post } from "../api/client";
import { Glass } from "./Glass";
import { Markdown } from "./Markdown";
import { Sheet } from "./Sheet";

/** Ask Siris about a lesson: a one-off explanation from the tutor, with a
 * hand-off to the SirisOS assistant when it's linked. */
export function AskSheet({ lessonId, lessonTitle, initial = "", onClose }: { lessonId: string; lessonTitle: string; initial?: string; onClose: () => void }) {
  const [question, setQuestion] = useState(initial);
  const [answer, setAnswer] = useState<string | null>(null);
  const [handoff, setHandoff] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function ask(e: FormEvent) {
    e.preventDefault();
    if (question.trim().length < 2) return;
    setBusy(true);
    setError(null);
    try {
      const out = await post<{ answer: string; sirisos_assistant: string | null }>(`/api/lessons/${lessonId}/ask`, { question: question.trim() });
      setAnswer(out.answer);
      setHandoff(out.sirisos_assistant);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Siris couldn't answer that.");
    } finally {
      setBusy(false);
    }
  }

  const followUp = handoff ? `${handoff}?q=${encodeURIComponent(`About "${lessonTitle}" (SirisLearn): ${question.trim()}`)}` : null;
  return (
    <Sheet label="Ask Siris" onClose={onClose}>
      <h2 className="sheet__title"><Sparkles size={20} aria-hidden="true" /> Ask Siris</h2>
      <p className="muted">About “{lessonTitle}”</p>
      <form className="stack ask" onSubmit={ask}>
        <textarea className="field" rows={3} value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="What would you like explained?" aria-label="Your question" maxLength={2000} />
        <Glass as="button" type="submit" variant="tint" shape="pill" interactive className="button" disabled={busy || question.trim().length < 2}>
          {busy ? "Thinking…" : answer ? "Ask again" : "Ask"}
        </Glass>
      </form>
      {error && <div className="error-banner" role="alert">{error}</div>}
      {answer && (
        <div className="ask__answer" aria-live="polite">
          <Markdown text={answer} />
          {followUp && <a className="chip chip--button" href={followUp} target="_blank" rel="noreferrer">Continue in Siris <ArrowUpRight size={14} aria-hidden="true" /></a>}
        </div>
      )}
    </Sheet>
  );
}
