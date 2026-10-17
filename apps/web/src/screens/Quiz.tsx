import { useEffect, useRef, useState, type FormEvent } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { ArrowRight, Award, Brain, Check, CircleCheck, CircleX, Flame, HelpCircle, PartyPopper, RotateCcw, Snowflake, Sparkles, X, Zap } from "lucide-react";
import { api, post } from "../api/client";
import type { AnswerResult, LessonDetail, Question, QuizKind, QuizResult, StartedQuiz } from "../api/types";
import { AskSheet } from "../components/AskSheet";
import { Diagram } from "../components/Diagram";
import { Glass } from "../components/Glass";
import { iconFor } from "../components/icons";
import { Loading } from "../components/PageHead";
import { Ring } from "../components/Ring";

const LETTERS = "ABCDEF";
const VERDICT = {
  correct: { label: "Correct", Icon: CircleCheck, tone: "good" },
  partial: { label: "Partly right", Icon: CircleCheck, tone: "warning" },
  incorrect: { label: "Not quite", Icon: CircleX, tone: "critical" },
} as const;

/** A lesson's quiz: /lesson/:id/quiz */
export function Quiz() {
  const { id } = useParams();
  const [lesson, setLesson] = useState<LessonDetail | null>(null);
  useEffect(() => {
    api<LessonDetail>(`/api/lessons/${id}`).then(setLesson).catch(() => undefined);
  }, [id]);
  return <QuizRunner key={id} kind="lesson" startUrl={`/api/lessons/${id}/attempts`} exitTo={`/lesson/${id}`} lesson={lesson} />;
}

/** The daily review: /review */
export function Review() {
  return <QuizRunner kind="review" startUrl="/api/review" exitTo="/" />;
}

/** A course's final exam: /course/:id/exam */
export function Exam() {
  const { id } = useParams();
  return <QuizRunner key={id} kind="exam" startUrl={`/api/courses/${id}/exam`} exitTo={`/course/${id}`} courseId={id} />;
}

export function QuizRunner({ kind, startUrl, exitTo, lesson, courseId }: {
  kind: QuizKind; startUrl: string; exitTo: string; lesson?: LessonDetail | null; courseId?: string;
}) {
  const navigate = useNavigate();
  const [started, setStarted] = useState<StartedQuiz | null>(null);
  const [index, setIndex] = useState(0);
  const [results, setResults] = useState<Record<string, AnswerResult>>({});
  const [finished, setFinished] = useState<QuizResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [round, setRound] = useState(0);
  const begun = useRef<string | null>(null);

  useEffect(() => {
    const key = `${startUrl}:${round}`;
    if (begun.current === key) return; // StrictMode runs effects twice; start one attempt
    begun.current = key;
    setResults({});
    setIndex(0);
    setFinished(null);
    setStarted(null);
    post<StartedQuiz>(startUrl).then(setStarted).catch((err) => setError(err instanceof Error ? err.message : "Couldn't start."));
  }, [startUrl, round]);

  if (error) return <div className="stack quiz"><div className="error-banner" role="alert">{error}</div><Link to={exitTo} className="back-link">Go back</Link></div>;
  if (!started || !started.questions.length) return <Loading label="Starting" />;
  if (finished) return <Results result={finished} lesson={lesson} courseId={courseId} results={results} questions={started.questions} onRetake={() => setRound((r) => r + 1)} exitTo={exitTo} />;

  const questions = started.questions;
  const question = questions[index];
  const result = results[question.id];
  const last = index === questions.length - 1;

  async function finish() {
    try {
      setFinished(await post<QuizResult>(`/api/attempts/${started!.attempt_id}/finish`));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Couldn't finish.");
    }
  }

  return (
    <div className="quiz">
      <header className="quiz__top">
        <button type="button" className="icon-link" onClick={() => navigate(exitTo)} aria-label="Leave"><X size={20} aria-hidden="true" /></button>
        <ol className="quiz__dots" aria-label={`Question ${index + 1} of ${questions.length}`}>
          {questions.map((q, i) => {
            const r = results[q.id];
            return <li key={q.id} className={`quiz__dot ${i === index ? "quiz__dot--now" : ""} ${r ? `quiz__dot--${r.verdict}` : ""}`} />;
          })}
        </ol>
        <span className="quiz__count">{index + 1}/{questions.length}</span>
      </header>
      {index === 0 && !result && (
        <p className="quiz__intro muted">
          {kind === "review" ? "Daily review: questions you've answered before, back at growing intervals." :
            kind === "exam" ? "Final exam: questions from every lesson. Score 80% to earn the certificate." :
              started.fresh === false ? "Some of these you've seen before (options shuffled). New questions are on their way for next time." : null}
        </p>
      )}
      <QuestionCard key={question.id} kind={kind} question={question} attemptId={started.attempt_id} result={result}
        onResult={(r) => setResults((all) => ({ ...all, [question.id]: r }))}
        onNext={() => (last ? finish() : setIndex(index + 1))} last={last} />
    </div>
  );
}

function QuestionCard({ kind, question, attemptId, result, onResult, onNext, last }: {
  kind: QuizKind; question: Question; attemptId: string; result?: AnswerResult; onResult: (r: AnswerResult) => void; onNext: () => void; last: boolean;
}) {
  const [choice, setChoice] = useState<number | null>(null);
  const [text, setText] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [asking, setAsking] = useState(false);
  const nextRef = useRef<HTMLButtonElement>(null);
  const ready = question.kind === "mcq" ? choice !== null : text.trim().length > 0;

  async function submit(e?: FormEvent) {
    e?.preventDefault();
    if (!ready || busy || result) return;
    setBusy(true);
    setError(null);
    try {
      onResult(await post<AnswerResult>(`/api/attempts/${attemptId}/answer`, question.kind === "mcq" ? { question_id: question.id, choice } : { question_id: question.id, text }));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Couldn't mark that answer.");
    } finally {
      setBusy(false);
    }
  }

  useEffect(() => {
    if (result) nextRef.current?.focus();
  }, [result]);

  useEffect(() => {
    if (question.kind !== "mcq" || result) return;
    const onKey = (e: KeyboardEvent) => {
      if ((e.target as HTMLElement)?.tagName === "TEXTAREA") return;
      const n = "1234".indexOf(e.key);
      if (n >= 0 && n < (question.options?.length ?? 0)) setChoice(n);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [question, result]);

  const verdict = result ? VERDICT[result.verdict] : null;
  const askPrompt = result && question.kind === "mcq"
    ? `I answered "${question.options![result.choice!]}" to "${question.prompt}", but the answer is "${question.options![result.answer_index!]}". Can you help me understand why?`
    : result ? `For "${question.prompt}" I wrote: "${result.text}". What did I miss?` : "";
  return (
    <Glass as="form" className="question" onSubmit={submit}>
      <span className="question__kind">
        {question.kind === "mcq" ? "Multiple choice" : "Written answer"}{question.svg ? " · picture" : ""}
        {kind !== "lesson" && question.lesson_title ? <span className="question__from"> · {question.lesson_title}</span> : null}
      </span>
      {question.svg && <Diagram svg={question.svg} alt={question.image_alt || "Picture for this question"} />}
      <h2 className="question__prompt">{question.prompt}</h2>

      {question.kind === "mcq" ? (
        <div className="options" role="radiogroup" aria-label="Answers">
          {question.options!.map((option, i) => {
            const state = !result ? (choice === i ? "picked" : "") :
              i === result.answer_index ? "right" : i === result.choice ? "wrong" : "dim";
            return (
              <button key={i} type="button" role="radio" aria-checked={choice === i} disabled={!!result}
                className={`option ${state ? `option--${state}` : ""}`} onClick={() => setChoice(i)}>
                <span className="option__letter">{state === "right" ? <Check size={15} /> : state === "wrong" ? <X size={15} /> : LETTERS[i]}</span>
                <span>{option}</span>
              </button>
            );
          })}
        </div>
      ) : (
        <textarea className="field answer-box" rows={4} placeholder="Type your answer in a sentence or two…" value={result?.text ?? text}
          onChange={(e) => setText(e.target.value)} readOnly={!!result} maxLength={4000} aria-label="Your answer"
          onKeyDown={(e) => { if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) void submit(); }} />
      )}

      {error && <div className="error-banner" role="alert">{error}</div>}

      {result && verdict && (
        <div className={`feedback feedback--${verdict.tone}`} role="status">
          <p className="feedback__verdict"><verdict.Icon aria-hidden="true" /> {verdict.label}{result.xp > 0 && <span className="feedback__xp">+{result.xp} XP</span>}</p>
          {result.feedback && <p>{result.feedback}</p>}
          {result.kind === "open" && result.model_answer && (
            <p className="feedback__model"><strong>A strong answer:</strong> {result.model_answer}</p>
          )}
          {result.explanation && <p className="muted">{result.explanation}</p>}
          {result.review && <p className="feedback__next muted">{result.verdict === "correct" ? `Back for review in ${days(result.review.due)}.` : "This one comes back in tomorrow's review."}</p>}
          {result.verdict !== "correct" && (
            <button type="button" className="chip chip--button feedback__help" onClick={() => setAsking(true)}><HelpCircle size={14} aria-hidden="true" /> Help me understand</button>
          )}
        </div>
      )}

      <div className="question__actions">
        {!result ? (
          <Glass as="button" type="submit" variant="tint" shape="pill" interactive className="button" disabled={!ready || busy}>
            {busy ? (question.kind === "open" ? "Marking…" : "Checking…") : "Check answer"}
          </Glass>
        ) : (
          <Glass as="button" type="button" ref={nextRef} variant="tint" shape="pill" interactive className="button" onClick={onNext}>
            {last ? "See results" : "Next question"} <ArrowRight aria-hidden="true" />
          </Glass>
        )}
      </div>
      {asking && result && <AskSheet lessonId={result.lesson_id} lessonTitle={result.lesson_title} initial={askPrompt} onClose={() => setAsking(false)} />}
    </Glass>
  );
}

function days(due: string): string {
  const n = Math.round((new Date(`${due}T00:00:00`).getTime() - new Date(new Date().toDateString()).getTime()) / 86400000);
  return n <= 1 ? "a day" : `${n} days`;
}

function Results({ result, lesson, courseId, results, questions, onRetake, exitTo }: {
  result: QuizResult; lesson?: LessonDetail | null; courseId?: string; results: Record<string, AnswerResult>; questions: Question[];
  onRetake: () => void; exitTo: string;
}) {
  const [review, setReview] = useState(false);
  const pct = Math.round(result.score * 100);
  const answeredXp = Object.values(results).reduce((n, r) => n + r.xp, 0);
  const title = result.kind === "review" ? "Review done" :
    result.kind === "exam" ? (result.passed ? "Exam passed!" : "Not this time") :
      result.course_completed ? "Course complete!" : result.score === 1 ? "Perfect score!" : result.passed ? "Lesson passed" : "Keep going";
  const subtitle = result.kind === "review" ? "Cards you got right come back later; the rest come back tomorrow." :
    result.kind === "exam" ? (result.passed ? "You've earned the certificate for this course." : "You need 80% to pass. Review the lessons and try again.") :
      result.passed ? lesson?.title ?? "" : "You need 70% to pass. Re-read the lesson and try again.";
  return (
    <div className="results">
      <Glass variant="strong" shape="xl" className="results__card">
        <Ring value={result.score} size={140} stroke={10} label={`${pct}%`} color={result.passed ? "var(--good)" : "var(--warning)"}>
          <span className="ring__big ring__big--xl">{pct}%</span>
          <span className="ring__small">{fmt(result.correct)}/{result.total}</span>
        </Ring>
        <h1 className="results__title">{title}</h1>
        <p className="muted">{subtitle}</p>

        <ul className="xp-list">
          {answeredXp > 0 && <li><Zap aria-hidden="true" /> Answers <b>+{answeredXp} XP</b></li>}
          {result.bonus.map((b) => <li key={b.label}><Sparkles aria-hidden="true" /> {b.label} <b>+{b.xp} XP</b></li>)}
          {result.xp === 0 && <li><Zap aria-hidden="true" /> No XP this time</li>}
        </ul>

        <div className="results__badges">
          <span className={`chip ${result.streak.today_done ? "chip--flame" : ""}`}><Flame size={14} aria-hidden="true" /> {result.streak.current} day streak</span>
          {result.streak.freezes > 0 && <span className="chip chip--ice"><Snowflake size={14} aria-hidden="true" /> {result.streak.freezes} freeze{result.streak.freezes > 1 ? "s" : ""}</span>}
          <span className="chip">{result.goal.today}/{result.goal.goal} XP today{result.goal.met_now ? " · goal met!" : ""}</span>
          <span className="chip">Level {result.level.level}{result.level_up ? " · level up!" : ""}</span>
          {result.brain && <span className="chip chip--brain"><Brain size={14} aria-hidden="true" /> Saving to your Second Brain</span>}
        </div>
        {result.kind === "lesson" && !result.passed && !result.streak.today_done && result.streak.current > 0 && (
          <p className="muted">A failed quiz doesn't keep your streak. Pass a quiz or do your daily review today.</p>
        )}

        {result.achievements.length > 0 && (
          <div className="unlocked">
            <p className="stat-card__title"><PartyPopper size={18} aria-hidden="true" /> New award{result.achievements.length > 1 ? "s" : ""}</p>
            {result.achievements.map((a) => {
              const Icon = iconFor(a.icon);
              return <div key={a.id} className={`unlocked__item tier-${a.tier}`}><Icon aria-hidden="true" /><span><b>{a.title}</b><br /><span className="muted">{a.description}</span></span></div>;
            })}
          </div>
        )}

        <div className="results__actions">
          {result.kind === "lesson" && lesson?.next_id && result.passed && (
            <Glass as={Link} to={`/lesson/${lesson.next_id}`} variant="tint" shape="pill" interactive className="button">Next lesson <ArrowRight aria-hidden="true" /></Glass>
          )}
          {result.kind === "exam" && result.certificate && courseId && (
            <Glass as={Link} to={`/certificate/${courseId}`} variant="tint" shape="pill" interactive className="button"><Award aria-hidden="true" /> Certificate</Glass>
          )}
          {result.kind !== "review" && <Glass as="button" type="button" shape="pill" interactive className="button" onClick={onRetake}><RotateCcw aria-hidden="true" /> {result.kind === "exam" ? "Try again" : "Retake"}</Glass>}
          <Glass as={Link} to={result.kind === "lesson" && lesson ? `/course/${lesson.course.id}` : exitTo} shape="pill" interactive className="button">
            {result.kind === "review" ? "Done" : "Course"}
          </Glass>
        </div>
      </Glass>

      <button type="button" className="chip chip--button results__review-toggle" onClick={() => setReview((r) => !r)} aria-expanded={review}>
        {review ? "Hide answers" : "Review your answers"}
      </button>
      {review && (
        <div className="stack">
          {questions.map((q, i) => {
            const r = results[q.id];
            const v = r ? VERDICT[r.verdict] : VERDICT.incorrect;
            return (
              <Glass key={q.id} className="review">
                <p className={`review__verdict tone-${v.tone}`}><v.Icon size={16} aria-hidden="true" /> {i + 1}. {r ? v.label : "Not answered"}</p>
                <p className="review__prompt">{q.prompt}</p>
                {q.kind === "mcq" && r ? (
                  <p className="muted">You chose <b>{q.options![r.choice!]}</b>{r.verdict !== "correct" && <> · answer: <b>{q.options![r.answer_index!]}</b></>}</p>
                ) : r ? (
                  <><p className="muted">You wrote: “{r.text}”</p>{r.feedback && <p className="muted">{r.feedback}</p>}</>
                ) : null}
                {r?.explanation && <p className="muted">{r.explanation}</p>}
              </Glass>
            );
          })}
        </div>
      )}
    </div>
  );
}

function fmt(n: number): string {
  return Number.isInteger(n) ? String(n) : n.toFixed(1);
}
