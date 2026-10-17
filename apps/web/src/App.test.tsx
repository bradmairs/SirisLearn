import { render, screen } from "@testing-library/react";
import { App } from "./App";
import { session } from "./api/client";

const summary = {
  today: "2026-10-15",
  streak: { current: 4, best: 9, today_done: false, at_risk: true, freezes: 1, frozen_days: [], freeze_in_use: false },
  xp: { total: 420, today: 20, goal: 50, goal_met: false, week: 180 },
  level: { level: 3, xp_into: 120, xp_for_next: 300, progress: 0.4 },
  courses: { total: 2, active: 2, completed: 0, planning: 0 },
  activity: { quizzes: 1, lessons_passed: 0 },
  continue: { course_id: "c1", course_title: "Heat pumps", icon: "zap", lesson_id: "l1", lesson_title: "Moving heat", lesson_status: "ready", progress: { lessons: 5, passed: 2, written: 3, writing: 0, percent: 40 } },
  review: { due: 6, next_due: null, cards: 30, boxes: [6, 10, 14, 0, 0, 0], intervals: [1, 3, 7, 14, 30, 60], done_today: false },
  achievements: { unlocked: 1, total: 24, recent: [{ id: "on-a-roll", title: "On a roll", icon: "flame", unlocked_at: "x" }] },
};

test("signed out shows the sign-in form", () => {
  render(<App />);
  expect(screen.getByRole("form", { name: "Sign in" })).toBeInTheDocument();
});

test("Today shows the streak, goal, level and what's next", async () => {
  session.save("token", "brad");
  vi.stubGlobal("fetch", vi.fn(async (url: string) => {
    const body = url === "/api/summary" ? summary : url === "/api/courses" ? [] : url === "/api/suggestions" ? { source: "brain", ideas: ["Pump curves"] } : {};
    return new Response(JSON.stringify(body), { status: 200, headers: { "Content-Type": "application/json" } });
  }));
  render(<App />);
  expect(await screen.findByText("Moving heat")).toBeInTheDocument();
  expect(screen.getByText(/Good (morning|afternoon|evening)|Up late/)).toHaveTextContent("Brad");
  expect(screen.getByText("Pass a quiz or do your review today to keep it")).toBeInTheDocument();
  expect(screen.getByText("Daily review · 6 cards due")).toBeInTheDocument();
  expect(screen.getByRole("link", { name: /Daily review/ })).toHaveAttribute("href", "/review");
  expect(screen.getByText(/1 freeze/)).toBeInTheDocument();
  expect(await screen.findByRole("button", { name: "Pump curves" })).toBeInTheDocument();
  expect(screen.getByText("From your Second Brain")).toBeInTheDocument();
  expect(screen.getByText("Level 3")).toBeInTheDocument();
  expect(screen.getByText("30 XP to go today")).toBeInTheDocument();
  expect(screen.getByRole("link", { name: /Moving heat/ })).toHaveAttribute("href", "/lesson/l1");
  expect(screen.getByText("On a roll")).toBeInTheDocument();
});
