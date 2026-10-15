export type Level = "beginner" | "intermediate" | "advanced";
export type Length = "short" | "standard" | "deep";
export type CourseStatus = "planning" | "ready" | "error";
export type LessonStatus = "pending" | "writing" | "ready" | "error";

export interface CourseProgress {
  lessons: number;
  passed: number;
  written: number;
  writing: number;
  percent: number;
}

export interface CourseCard {
  id: string;
  topic: string;
  title: string;
  summary: string;
  icon: string;
  level: Level;
  length: Length;
  status: CourseStatus;
  error: string;
  created_at: string;
  updated_at: string;
  completed_at: string | null;
  archived: boolean;
  progress: CourseProgress;
  next_lesson: { id: string; title: string; status: LessonStatus; position: number } | null;
}

export interface LessonSummary {
  id: string;
  title: string;
  summary: string;
  status: LessonStatus;
  error: string;
  best_score: number | null;
  passed_at: string | null;
  read_at: string | null;
  position: number;
}

export interface CourseDetail extends CourseCard {
  notes: string;
  sections: { title: string; summary: string; lessons: LessonSummary[] }[];
}

export interface LessonDetail extends LessonSummary {
  course: { id: string; title: string; icon: string };
  section: string;
  number: number;
  of: number;
  previous_id: string | null;
  next_id: string | null;
  content: {
    body: string;
    minutes: number;
    key_points: string[];
    figure_svg: string;
    figure_caption: string;
    question_count: number;
  } | null;
}

export interface Question {
  id: string;
  kind: "mcq" | "open";
  prompt: string;
  svg: string;
  image_alt: string;
  options?: string[];
}

export type Verdict = "correct" | "partial" | "incorrect";

export interface AnswerResult {
  verdict: Verdict;
  score: number;
  xp: number;
  kind: "mcq" | "open";
  explanation: string;
  feedback: string;
  choice?: number;
  answer_index?: number;
  text?: string;
  model_answer?: string;
  key_points?: string[];
  marked_by?: string;
}

export interface Streak {
  current: number;
  best: number;
  today_done: boolean;
  at_risk: boolean;
}

export interface LevelInfo {
  level: number;
  xp_into: number;
  xp_for_next: number;
  progress: number;
}

export interface Achievement {
  id: string;
  title: string;
  description: string;
  icon: string;
  tier: "bronze" | "silver" | "gold" | "platinum";
  target: number;
  value: number;
  unlocked_at: string | null;
}

export interface QuizResult {
  attempt_id: string;
  correct: number;
  total: number;
  score: number;
  passed: boolean;
  first_pass: boolean;
  xp: number;
  bonus: { label: string; xp: number }[];
  streak: Streak;
  goal: { goal: number; today: number; met_now: boolean };
  level: LevelInfo;
  level_up: boolean;
  achievements: Achievement[];
  course_completed: boolean;
}

export interface Summary {
  today: string;
  streak: Streak;
  xp: { total: number; today: number; goal: number; goal_met: boolean; week: number };
  level: LevelInfo;
  courses: { total: number; active: number; completed: number; planning: number };
  activity: { quizzes: number; lessons_passed: number };
  continue: {
    course_id: string;
    course_title: string;
    icon: string;
    lesson_id: string;
    lesson_title: string;
    lesson_status: LessonStatus;
    progress: CourseProgress;
  } | null;
  achievements: { unlocked: number; total: number; recent: { id: string; title: string; icon: string; unlocked_at: string }[] };
}

export interface HistoryEvent {
  id: number;
  ts: string;
  day: string;
  kind: "course_created" | "course_ready" | "lesson_read" | "quiz_finished" | "lesson_passed" | "course_completed" | "goal_met" | "achievement";
  course_id: string | null;
  lesson_id: string | null;
  title: string;
  course_title: string;
  xp: number;
  detail: Record<string, unknown>;
}

export interface History {
  heatmap: { day: string; xp: number }[];
  goal: number;
  stats: {
    xp: number;
    active_days: number;
    quizzes: number;
    lessons_read: number;
    lessons_passed: number;
    courses_completed: number;
    questions: number;
    accuracy: number | null;
    quiz_minutes: number;
    goal_days: number;
  };
  streak: Streak;
  events: HistoryEvent[];
  next_before: number | null;
}

export interface Settings {
  daily_goal: number;
  llm: { provider: string; model: string | null; configured: boolean };
}
