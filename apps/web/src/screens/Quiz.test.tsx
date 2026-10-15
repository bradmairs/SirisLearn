import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { Quiz } from "./Quiz";

const lesson = { id: "l1", title: "Moving heat", course: { id: "c1", title: "Heat pumps", icon: "zap" }, next_id: "l2", status: "ready" };
const questions = [
  { id: "q1", kind: "mcq", prompt: "Which way does heat flow?", svg: "", image_alt: "", options: ["Hot to cold", "Cold to hot", "Neither", "Both"] },
  { id: "q2", kind: "open", prompt: "Explain a heat pump.", svg: "<svg xmlns='http://www.w3.org/2000/svg'/>", image_alt: "A diagram" },
];

function mockApi() {
  const calls: { url: string; body?: unknown }[] = [];
  vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => {
    const body = init?.body ? JSON.parse(init.body as string) : undefined;
    calls.push({ url, body });
    const json = (value: unknown) => new Response(JSON.stringify(value), { status: 200, headers: { "Content-Type": "application/json" } });
    if (url === "/api/lessons/l1") return json(lesson);
    if (url === "/api/lessons/l1/attempts") return json({ attempt_id: "a1", questions });
    if (url === "/api/attempts/a1/answer" && body.question_id === "q1")
      return json({ verdict: "correct", score: 1, xp: 10, kind: "mcq", explanation: "Heat flows downhill.", feedback: "", choice: 0, answer_index: 0 });
    if (url === "/api/attempts/a1/answer")
      return json({ verdict: "partial", score: 0.5, xp: 7, kind: "open", explanation: "", feedback: "Mention the refrigerant.", model_answer: "It moves heat using a refrigerant.", text: body.text });
    if (url === "/api/attempts/a1/finish")
      return json({ attempt_id: "a1", correct: 1.5, total: 2, score: 0.75, passed: true, first_pass: true, xp: 37, bonus: [{ label: "Lesson passed", xp: 20 }],
        streak: { current: 3, best: 3, today_done: true, at_risk: false }, goal: { goal: 50, today: 37, met_now: false },
        level: { level: 1, xp_into: 37, xp_for_next: 100, progress: 0.37 }, level_up: false,
        achievements: [{ id: "first-steps", title: "First steps", description: "Finish your first quiz.", icon: "footprints", tier: "bronze", target: 1, value: 1, unlocked_at: "x" }],
        course_completed: false });
    return new Response("{}", { status: 404 });
  }));
  return calls;
}

test("answers each question, shows feedback, then the results", async () => {
  const calls = mockApi();
  const user = userEvent.setup();
  render(
    <MemoryRouter initialEntries={["/lesson/l1/quiz"]}>
      <Routes><Route path="/lesson/:id/quiz" element={<Quiz />} /></Routes>
    </MemoryRouter>,
  );
  await screen.findByText("Which way does heat flow?");
  const check = screen.getByRole("button", { name: "Check answer" });
  expect(check).toBeDisabled();
  await user.click(screen.getByRole("radio", { name: /Hot to cold/ }));
  await user.click(check);
  expect(await screen.findByText("Correct")).toBeInTheDocument();
  expect(screen.getByText("+10 XP")).toBeInTheDocument();
  await user.click(screen.getByRole("button", { name: /Next question/ }));

  expect(await screen.findByAltText("A diagram")).toBeInTheDocument();
  await user.type(screen.getByLabelText("Your answer"), "It moves heat");
  await user.click(screen.getByRole("button", { name: "Check answer" }));
  expect(await screen.findByText("Partly right")).toBeInTheDocument();
  expect(screen.getByText(/It moves heat using a refrigerant/)).toBeInTheDocument();
  await user.click(screen.getByRole("button", { name: /See results/ }));

  expect(await screen.findByRole("heading", { name: "Lesson passed" })).toBeInTheDocument();
  expect(screen.getByText("75%")).toBeInTheDocument();
  expect(screen.getByText("First steps")).toBeInTheDocument();
  expect(screen.getByRole("link", { name: /Next lesson/ })).toHaveAttribute("href", "/lesson/l2");
  await waitFor(() => expect(calls.filter((c) => c.url === "/api/lessons/l1/attempts")).toHaveLength(1));
});
