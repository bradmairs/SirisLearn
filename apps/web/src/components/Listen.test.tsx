import { speakable } from "./Listen";

test("lesson Markdown becomes plain paragraphs to read aloud", () => {
  expect(speakable("## Heading\n\nSome **bold** and `code`.\n\n- one\n- two\n\n> a tip\n\n```\nskip me\n```")).toEqual([
    "Heading", "Some bold and code.", "one two", "a tip",
  ]);
});
