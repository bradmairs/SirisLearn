import { useEffect, useRef, useState, type FormEvent } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { ArrowRight, Check, CircleCheck, CircleX, Flame, PartyPopper, RotateCcw, Sparkles, X, Zap } from "lucide-react";
import { api, post } from "../api/client";
import type { AnswerResult, LessonDetail, Question, QuizResult } from "../api/types";
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

export function Quiz() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState<LessonDetail | null>(null);
  const [attemptId, setAttemptId] = useState<string | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [index, setIndex] = useState(0);
  const [results, setResults] = useState<Record<string, AnswerResult>>({});
  const [finished, setFinished] = useState<QuizResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [round, setRound] = useState(0);
  const started = useRef<string | null>(null);

  useEffect(() => {
    const key = `${id}:${round}`;
    if (started.current === key) return; // StrictMode runs effects twice; start one attempt
    started.current = key;
    setResults({});
    setIndex(0);
    setFinished(null);
    void (async () => {
      try {
        const [l, attempt] = await Promise.all([
          api<LessonDetail>(`/api/lessons/${id}`),
          post<{ attempt_id: string; questions: Question[] }>(`/api/lessons/${id}/attempts`),
        ]);
        setLesson(l);
        setAttemptId(attempt.attempt_id);
        setQuestions(attempt.questions);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Couldn't start the quiz.");
      }
    })();
  }, [id, round]);

  if (error) return <div className="stack"><div className="error-banner" role="alert">{error}</div><Link to={`/lesson/${id}`} className="back-link">Back to the lesson</Link></div>;
  if (!lesson || !attemptId || !questions.length) return <Loading label="Starting the quiz" />;
  if (finished) return <Results result={finished} lesson={lesson} results={results} questions={questions} onRetake={() => setRound((r) => r + 1)} />;

  const question = questions[index];
  const result = results[question.id];
  const last = index === questions.length - 1;

  async function finish() {
    try {
      setFinished(await post<QuizResult>(`/api/attempts/${attemptId}/finish`));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Couldn't finish the quiz.");
    }
  }

  return (
    <div className="quiz">
      <header className="quiz__top">
        <button type="button" className="icon-link" onClick={() => navigate(`/lesson/${id}`)} aria-label="Leave the quiz"><X size={20} aria-hidden="true" /></button>
        <ol className="quiz__dots" aria-label={`Question ${index + 1} of ${questions.length}`}>
          {questions.map((q, i) => {
            const r = results[q.id];
            return <li key={q.id} className={`quiz__dot ${i === index ? "quiz__dot--now" : ""} ${r ? `quiz__dot--${r.verdict}` : ""}`} />;
          })}
        </ol>
        <span className="quiz__count">{index + 1}/{questions.length}</span>
      </header>
      <QuestionCard key={question.id} question={question} attemptId={attemptId} result={result}
        onResult={(r) => setResults((all) => ({ ...all, [question.id]: r }))}
        onNext={() => (last ? finish() : setIndex(index + 1))} last={last} />
    </div>
  );
}

function QuestionCard({ question, attemptId, result, onResult, onNext, last }: {
  question: Question; attemptId: string; result?: AnswerResult; onResult: (r: AnswerResult) => void; onNext: () => void; last: boolean;
}) {
  const [choice, setChoice] = useState<number | null>(null);
  const [text, setText] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
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
      const n = "1234".indexOf(e.key);
      if (n >= 0 && n < (question.options?.length ?? 0)) setChoice(n);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [question, result]);

  const verdict = result ? VERDICT[result.verdict] : null;
  return (
    <Glass as="form" className="question" onSubmit={submit}>
      <span className="question__kind">{question.kind === "mcq" ? "Multiple choice" : "Written answer"}{question.svg ? " · picture" : ""}</span>
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
    </Glass>
  );
}

function Results({ result, lesson, results, questions, onRetake }: {
  result: QuizResult; lesson: LessonDetail; results: Record<string, AnswerResult>; questions: Question[]; onRetake: () => void;
}) {
  const [review, setReview] = useState(false);
  const pct = Math.round(result.score * 100);
  const answeredXp = Object.values(results).reduce((n, r) => n + r.xp, 0);
  return (
    <div className="results">
      <Glass variant="strong" shape="xl" className="results__card">
        <Ring value={result.score} size={140} stroke={10} label={`${pct}%`} color={result.passed ? "var(--good)" : "var(--warning)"}>
          <span className="ring__big ring__big--xl">{pct}%</span>
          <span className="ring__small">{fmt(result.correct)}/{result.total}</span>
        </Ring>
        <h1 className="results__title">{result.course_completed ? "Course complete!" : result.score === 1 ? "Perfect score!" : result.passed ? "Lesson passed" : "Keep going"}</h1>
        <p className="muted">{result.passed ? lesson.title : `You need 70% to pass. Re-read the lesson and try again.`}</p>

        <ul className="xp-list">
          <li><Zap aria-hidden="true" /> Answers <b>+{answeredXp} XP</b></li>
          {result.bonus.map((b) => <li key={b.label}><Sparkles aria-hidden="true" /> {b.label} <b>+{b.xp} XP</b></li>)}
        </ul>

        <div className="results__badges">
          <span className={`chip ${result.streak.today_done ? "chip--flame" : ""}`}><Flame size={14} aria-hidden="true" /> {result.streak.current} day streak</span>
          <span className="chip">{result.goal.today}/{result.goal.goal} XP today{result.goal.met_now ? " · goal met!" : ""}</span>
          <span className="chip">Level {result.level.level}{result.level_up ? " · level up!" : ""}</span>
        </div>

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
          {lesson.next_id && result.passed && (
            <Glass as={Link} to={`/lesson/${lesson.next_id}`} variant="tint" shape="pill" interactive className="button">Next lesson <ArrowRight aria-hidden="true" /></Glass>
          )}
          <Glass as="button" type="button" shape="pill" interactive className="button" onClick={onRetake}><RotateCcw aria-hidden="true" /> Retake</Glass>
          <Glass as={Link} to={`/course/${lesson.course.id}`} shape="pill" interactive className="button">Course</Glass>
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
