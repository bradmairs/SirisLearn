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
  area: string;
  tags: string[];
  pack: string;
  exam_best: number | null;
  exam_passed_at: string | null;
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

export interface ExamStatus {
  unlocked: boolean;
  questions: number;
  pass_mark: number;
  best: number | null;
  passed_at: string | null;
  lessons_left: number;
}

export interface CourseDetail extends CourseCard {
  notes: string;
  sections: { title: string; summary: string; lessons: LessonSummary[] }[];
  related: { id: string; title: string; icon: string; level: Level }[];
  exam: ExamStatus;
}

export interface Photo {
  url: string;
  page: string;
  title: string;
  author: string;
  licence: string;
}

export interface LessonDetail extends LessonSummary {
  course: { id: string; title: string; icon: string; level: Level };
  brain_saved_at: string | null;
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
    pool_size: number;
    unseen: number;
    photo?: Photo | null;
    photo_query?: string;
  } | null;
}

export interface Question {
  id: string;
  kind: "mcq" | "open";
  prompt: string;
  svg: string;
  image_alt: string;
  options?: string[];
  lesson_title?: string;
}

export type QuizKind = "lesson" | "review" | "exam";

export interface StartedQuiz {
  attempt_id: string;
  kind: QuizKind;
  fresh?: boolean;
  questions: Question[];
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
  lesson_id: string;
  lesson_title: string;
  review?: { box: number; due: string };
}

export interface Streak {
  current: number;
  best: number;
  today_done: boolean;
  at_risk: boolean;
  freezes: number;
  frozen_days: string[];
  freeze_in_use: boolean;
}

export interface ReviewStatus {
  due: number;
  next_due: string | null;
  cards: number;
  boxes: number[];
  intervals: number[];
  done_today: boolean;
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
  kind: QuizKind;
  correct: number;
  total: number;
  score: number;
  passed: boolean;
  first_pass?: boolean;
  xp: number;
  bonus: { label: string; xp: number }[];
  streak: Streak;
  goal: { goal: number; today: number; met_now: boolean };
  level: LevelInfo;
  level_up: boolean;
  achievements: Achievement[];
  course_completed?: boolean;
  lesson_id?: string;
  course_id?: string;
  certificate?: boolean;
  brain?: string;
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
  review: ReviewStatus;
  achievements: { unlocked: number; total: number; recent: { id: string; title: string; icon: string; unlocked_at: string }[] };
}

export interface HistoryEvent {
  id: number;
  ts: string;
  day: string;
  kind: "course_created" | "course_ready" | "lesson_read" | "quiz_finished" | "lesson_passed" | "course_completed" | "goal_met"
    | "achievement" | "review_finished" | "exam_finished" | "brain_saved";
  course_id: string | null;
  lesson_id: string | null;
  title: string;
  course_title: string;
  xp: number;
  detail: Record<string, unknown>;
}

export interface History {
  today: string;
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

export interface Usage {
  calls: number;
  cost: number;
  month: number;
  input_tokens: number;
  output_tokens: number;
  by_course: { course_id: string; title: string; cost: number; calls: number }[];
  by_purpose: { purpose: string; cost: number; calls: number }[];
}

export interface Settings {
  daily_goal: number;
  llm: { provider: string; model: string | null; configured: boolean };
  brain: { configured: boolean; enabled: boolean };
  sirisos_url: string | null;
  push: { subscriptions: number; reminder_hour: number; review_hour: number };
  usage: Usage;
  today: string;
}

export interface Certificate {
  name: string;
  course: string;
  level: Level;
  summary: string;
  issued: string;
  score: number | null;
  lessons: number;
  minutes: number;
  sections: string[];
  reference: string;
}
