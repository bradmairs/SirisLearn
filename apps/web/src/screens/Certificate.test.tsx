import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { Certificate } from "./Certificate";

test("shows the certificate for a passed course", async () => {
  vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify({
    name: "Brad", course: "Docker for beginners", level: "beginner", summary: "Containers from scratch.", issued: "2026-10-17T05:00:00+00:00",
    score: 0.9, lessons: 6, minutes: 48, sections: ["Basics", "Compose"], reference: "SL-ABC123-20261017",
  }), { status: 200, headers: { "Content-Type": "application/json" } })));
  render(
    <MemoryRouter initialEntries={["/certificate/c1"]}>
      <Routes><Route path="/certificate/:id" element={<Certificate />} /></Routes>
    </MemoryRouter>,
  );
  expect(await screen.findByRole("heading", { name: "Brad" })).toBeInTheDocument();
  expect(screen.getByRole("heading", { name: "Docker for beginners" })).toBeInTheDocument();
  expect(screen.getByText("90%")).toBeInTheDocument();
  expect(screen.getByText("Ref. SL-ABC123-20261017")).toBeInTheDocument();
});
