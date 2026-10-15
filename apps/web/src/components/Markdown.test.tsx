import { render, screen } from "@testing-library/react";
import { Markdown, parse } from "./Markdown";

test("parses headings, lists, quotes and paragraphs", () => {
  const blocks = parse("Intro line\nstill intro\n\n## Heading\n- one\n- two\n\n1. first\n2. second\n\n> a tip\n\n```\ncode\n```");
  expect(blocks.map((b) => b.type)).toEqual(["p", "h", "ul", "ol", "quote", "code"]);
  expect(blocks[0]).toEqual({ type: "p", text: "Intro line still intro" });
});

test("renders inline formatting without injecting HTML", () => {
  render(<Markdown text={'**Bold** and *italic* and `code` <img src=x onerror="alert(1)">'} />);
  expect(screen.getByText("Bold").tagName).toBe("STRONG");
  expect(screen.getByText("italic").tagName).toBe("EM");
  expect(screen.getByText("code").tagName).toBe("CODE");
  expect(document.querySelector("img")).toBeNull();
});
