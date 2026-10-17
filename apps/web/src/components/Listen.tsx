import { useEffect, useRef, useState } from "react";
import { Headphones, Pause, Play, Square } from "lucide-react";

/** Lesson text without Markdown, split into sentences-ish chunks for speech. */
export function speakable(markdown: string): string[] {
  return markdown
    .replace(/```[\s\S]*?```/g, " ")
    .split(/\n{2,}/)
    .map((block) => block.replace(/^#+\s*/gm, "").replace(/^\s*(?:[-*+]|\d+[.)])\s+/gm, "").replace(/^>\s?/gm, "")
      .replace(/[*_`]/g, "").replace(/\s+/g, " ").trim())
    .filter(Boolean);
}

const RATES = [1, 1.25, 1.5];

/** Read the lesson aloud with the device's own voices (works offline). */
export function Listen({ text }: { text: string }) {
  const synth = typeof window !== "undefined" ? window.speechSynthesis : undefined;
  const [state, setState] = useState<"idle" | "playing" | "paused">("idle");
  const [rate, setRate] = useState(1);
  const queue = useRef<string[]>([]);
  const stopped = useRef(false);

  useEffect(() => () => synth?.cancel(), [synth]);
  if (!synth || typeof SpeechSynthesisUtterance === "undefined") return null;

  function speakNext() {
    const chunk = queue.current.shift();
    if (!chunk || stopped.current) {
      setState("idle");
      return;
    }
    const u = new SpeechSynthesisUtterance(chunk);
    u.rate = rate;
    u.onend = speakNext;
    synth!.speak(u);
  }

  function play() {
    if (state === "paused") {
      synth!.resume();
      setState("playing");
      return;
    }
    synth!.cancel();
    stopped.current = false;
    queue.current = speakable(text);
    setState("playing");
    speakNext();
  }

  function stop() {
    stopped.current = true;
    synth!.cancel();
    setState("idle");
  }

  return (
    <div className="listen" role="group" aria-label="Listen to this lesson">
      {state === "playing" ? (
        <button type="button" className="chip chip--button" onClick={() => { synth.pause(); setState("paused"); }}><Pause size={14} aria-hidden="true" /> Pause</button>
      ) : (
        <button type="button" className="chip chip--button" onClick={play}>{state === "paused" ? <Play size={14} aria-hidden="true" /> : <Headphones size={14} aria-hidden="true" />} {state === "paused" ? "Resume" : "Listen"}</button>
      )}
      {state !== "idle" && <button type="button" className="chip chip--button" onClick={stop} aria-label="Stop"><Square size={13} aria-hidden="true" /></button>}
      <button type="button" className="chip chip--button" onClick={() => setRate(RATES[(RATES.indexOf(rate) + 1) % RATES.length])} aria-label="Speed" title="Speed (applies to the next paragraph)">{rate}×</button>
    </div>
  );
}
