import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { Practice } from "./Quiz";

const questions = [
  { id: "l1:q1", kind: "calc", prompt: "Shaft power for 30 L/s at 25 m and 70%?", svg: "", image_alt: "", unit: "kW", lesson_title: "Pumps" },
  { id: "l1:q2", kind: "scenario", prompt: "Odour at a rising main. What do you do?", svg: "", image_alt: "", lesson_title: "Pumps" },
];

function mockApi() {
  const answers: unknown[] = [];
  let calcTries = 0;
  vi.stubGlobal("fetch", vi.fn(async (url: string, init?: RequestInit) => {
    const body = init?.body ? JSON.parse(init.body as string) : undefined;
    const json = (value: unknown) => new Response(JSON.stringify(value), { status: 200, headers: { "Content-Type": "application/json" } });
    if (url === "/api/lessons/l1") return json({ id: "l1", title: "Pumps", course: { id: "c1", title: "Water", icon: "waves" }, status: "ready" });
    if (url === "/api/lessons/l1/practice") return json({ attempt_id: "a1", kind: "practice", questions });
    if (url === "/api/attempts/a1/answer") {
      answers.push(body);
      const base = { explanation: "Divide by efficiency.", lesson_id: "l1", lesson_title: "Pumps", text: body.text };
      if (body.question_id === "l1:q1") {
        calcTries += 1;
        return calcTries === 1
          ? json({ lesson_id: "l1", lesson_title: "Pumps", text: body.text, verdict: "partial", score: 0.5, xp: 2, kind: "calc",
            feedback: "Right digits, wrong size. Check your unit conversions.", can_retry: true, hidden: true, review: { box: 0, due: "2099-01-02" } })
          : json({ ...base, verdict: "correct", score: 0.5, xp: 2, kind: "calc", feedback: "Right: 10.5 kW.", answer_value: 10.5, unit: "kW", tolerance: 3,
            working: "1. ρgQH = 7358 W.", can_retry: false, second_try: true, first_verdict: "partial" });
      }
      return json({ lesson_id: "l1", lesson_title: "Pumps", text: body.text, verdict: "partial", score: 0.5, xp: 2, kind: "scenario",
        feedback: "You covered 1 of 2 key points.", points: [], covered: 1, of: 2, can_retry: true, hidden: true });
    }
    if (url === "/api/attempts/a1/reveal") {
      return json({ lesson_id: "l1", lesson_title: "Pumps", text: "It's septic.", verdict: "partial", score: 0.5, xp: 2, kind: "scenario", feedback: "Good start.",
        explanation: "", model_answer: "Check detention and dose.", can_retry: false, revealed: true,
        points: [{ point: "septicity from long detention", met: true }, { point: "chemical dosing", met: false }] });
    }
    return new Response("{}", { status: 404 });
  }));
  return answers;
}

test("a calculation shows its working and can be tried once more; a scenario shows the rubric", async () => {
  const answers = mockApi();
  const user = userEvent.setup();
  render(
    <MemoryRouter initialEntries={["/lesson/l1/practice"]}>
      <Routes><Route path="/lesson/:id/practice" element={<Practice />} /></Routes>
    </MemoryRouter>,
  );
  expect(await screen.findByText(/Practice: Pumps|Practice\./)).toBeInTheDocument();
  expect(screen.getByText("Calculation")).toBeInTheDocument();
  expect(screen.getByText("kW")).toBeInTheDocument();
  await user.type(screen.getByLabelText("Your answer in kW"), "10511");
  await user.click(screen.getByRole("button", { name: "Check answer" }));
  expect(await screen.findByText(/Right digits, wrong size/)).toBeInTheDocument();
  expect(screen.queryByText("Working")).not.toBeInTheDocument(); // no answer while a second try is open
  expect(screen.getByRole("button", { name: /Show answer/ })).toBeInTheDocument();

  await user.click(screen.getByRole("button", { name: /Try again/ }));
  expect(screen.getByText(/second try/)).toBeInTheDocument();
  expect(screen.getByText(/First try: “10511”/)).toBeInTheDocument();
  await user.type(screen.getByLabelText("Your answer in kW"), "10.5");
  await user.click(screen.getByRole("button", { name: "Check answer" }));
  expect(await screen.findByText(/Correct on the second try/)).toBeInTheDocument();
  expect(screen.getByText("Working")).toBeInTheDocument();
  expect(screen.getByText(/right within 3%/)).toBeInTheDocument();
  expect(screen.queryByRole("button", { name: /Try again/ })).not.toBeInTheDocument();
  expect(answers).toEqual([{ question_id: "l1:q1", text: "10511" }, { question_id: "l1:q1", text: "10.5" }]);

  await user.click(screen.getByRole("button", { name: /Next question/ }));
  expect(await screen.findByText("Scenario")).toBeInTheDocument();
  await user.type(screen.getByLabelText("Your answer"), "It's septic.");
  await user.click(screen.getByRole("button", { name: "Check answer" }));
  expect(await screen.findByText("You covered 1 of 2 key points.")).toBeInTheDocument();
  await user.click(screen.getByRole("button", { name: /Show answer/ }));
  expect(await screen.findByLabelText("Covered")).toBeInTheDocument();
  expect(screen.queryByRole("button", { name: /Try again/ })).not.toBeInTheDocument();
  expect(screen.getByLabelText("Missing")).toBeInTheDocument();
  expect(screen.getByText("chemical dosing")).toBeInTheDocument();
});
