"""A starter course, added on first run so SirisLearn is usable (and
explorable) before a model is set up. It's a normal course: delete it any
time. SIRISLEARN_SEED_SAMPLE=false skips it."""

from __future__ import annotations

from app import config
from app.db import Store, new_id, now_iso
from app.generator import clean_lesson

BG = '<rect width="480" height="300" rx="16" fill="#0b1620"/>'
FONT = 'font-family="sans-serif"'

FORGETTING_CURVE = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300">{BG}
<line x1="60" y1="250" x2="450" y2="250" stroke="#e4f3fc" stroke-width="2"/>
<line x1="60" y1="250" x2="60" y2="40" stroke="#e4f3fc" stroke-width="2"/>
<text x="255" y="285" fill="#e4f3fc" font-size="14" {FONT} text-anchor="middle">Days since learning</text>
<text x="24" y="150" fill="#e4f3fc" font-size="14" {FONT} text-anchor="middle" transform="rotate(-90 24 150)">Recall</text>
<path d="M60 50 C 90 150, 120 200, 200 220 S 380 235, 450 238" fill="none" stroke="#ff6b6b" stroke-width="3"/>
<path d="M60 50 C 80 100, 95 120, 120 125 L 120 55 C 150 95, 180 110, 220 112 L 220 58 C 270 80, 330 90, 450 96" fill="none" stroke="#8af5c8" stroke-width="3"/>
<circle cx="120" cy="55" r="5" fill="#5fd3ff"/><circle cx="220" cy="58" r="5" fill="#5fd3ff"/>
<text x="300" y="215" fill="#ff6b6b" font-size="14" {FONT}>No review</text>
<text x="300" y="80" fill="#8af5c8" font-size="14" {FONT}>Spaced reviews</text>
<text x="128" y="45" fill="#5fd3ff" font-size="13" {FONT}>review</text>
</svg>"""

INTERVALS = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300">{BG}
<line x1="40" y1="160" x2="450" y2="160" stroke="#e4f3fc" stroke-width="2"/>
<g {FONT} font-size="14" fill="#e4f3fc" text-anchor="middle">
<circle cx="50" cy="160" r="9" fill="#5fd3ff"/><text x="50" y="195">Day 0</text>
<circle cx="80" cy="160" r="9" fill="#5fd3ff"/><text x="86" y="135">A</text>
<circle cx="140" cy="160" r="9" fill="#5fd3ff"/><text x="140" y="195">Day 3</text>
<circle cx="250" cy="160" r="9" fill="#ffb547"/><text x="250" y="135">B</text>
<circle cx="430" cy="160" r="9" fill="#5fd3ff"/><text x="430" y="195">Day 30</text>
</g>
<text x="240" y="60" fill="#e4f3fc" font-size="15" {FONT} text-anchor="middle">Review schedule for one flashcard</text>
<text x="240" y="245" fill="#7c93a6" font-size="13" {FONT} text-anchor="middle">Each dot is a review</text>
</svg>"""

TWO_GROUPS = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300">{BG}
<line x1="60" y1="250" x2="440" y2="250" stroke="#e4f3fc" stroke-width="2"/>
<rect x="110" y="150" width="90" height="100" rx="6" fill="#ffb547"/>
<rect x="280" y="80" width="90" height="170" rx="6" fill="#5fd3ff"/>
<g {FONT} font-size="14" fill="#e4f3fc" text-anchor="middle">
<text x="155" y="275">Group X</text><text x="325" y="275">Group Y</text>
<text x="155" y="140">40%</text><text x="325" y="70">70%</text>
<text x="240" y="35">Recall one week later</text>
</g>
</svg>"""

LEITNER = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 300">{BG}
<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#8af5c8"/></marker>
<marker id="b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#ff6b6b"/></marker></defs>
<g {FONT} font-size="14" fill="#e4f3fc" text-anchor="middle">
<rect x="30" y="110" width="110" height="70" rx="10" fill="none" stroke="#e4f3fc" stroke-width="2"/><text x="85" y="140">Box 1</text><text x="85" y="160" font-size="13" fill="#7c93a6">every day</text>
<rect x="185" y="110" width="110" height="70" rx="10" fill="none" stroke="#e4f3fc" stroke-width="2"/><text x="240" y="140">Box 2</text><text x="240" y="160" font-size="13" fill="#7c93a6">every 3 days</text>
<rect x="340" y="110" width="110" height="70" rx="10" fill="none" stroke="#e4f3fc" stroke-width="2"/><text x="395" y="140">Box 3</text><text x="395" y="160" font-size="13" fill="#7c93a6">weekly</text>
<path d="M140 125 L183 125" stroke="#8af5c8" stroke-width="2.5" marker-end="url(#a)"/>
<path d="M295 125 L338 125" stroke="#8af5c8" stroke-width="2.5" marker-end="url(#a)"/>
<path d="M395 182 C 380 250, 110 250, 85 184" fill="none" stroke="#ff6b6b" stroke-width="2.5" marker-end="url(#b)"/>
<text x="240" y="90" fill="#8af5c8">P</text>
<text x="240" y="262" fill="#ff6b6b">Q</text>
</g>
</svg>"""

LESSON_1 = {
    "title": "Why we forget, and how to stop it",
    "minutes": 7,
    "body": """Most of what you read today will be gone within a week. That isn't a flaw in you: it's how memory works, and once you know the pattern you can work with it instead of against it.

## The forgetting curve

In the 1880s the psychologist **Hermann Ebbinghaus** memorised lists of nonsense syllables and tested himself at different delays. He found that memory fades fast at first and then more slowly: a large share is lost within the first day or two, and what survives fades gently after that. This shape is called the **forgetting curve**, and it has been replicated many times since.

The steepness of the curve isn't fixed. Material that is meaningful, connected to what you already know, or **reviewed at the right moments** fades far more slowly.

## Retrieval beats re-reading

The most effective way to make something stick is to **pull it out of memory**, not to put it back in. This is called **retrieval practice** (or the *testing effect*). Re-reading feels productive because the text looks familiar, but familiarity isn't recall. Answering a question forces your brain to reconstruct the idea, and that effort strengthens the memory.

In a well-known experiment, students who read a passage once and then practised recalling it remembered much more a week later than students who spent the same time re-reading it, even though the re-readers felt more confident.

> **Common misconception:** if studying feels easy, it's working. Often the opposite is true: a little struggle while recalling is a sign the practice is doing its job. Researchers call these **desirable difficulties**.

## Spacing your reviews

Reviewing something just as you're starting to forget it resets the curve, and each reset makes the next drop shallower. This is the **spacing effect**: the same total study time, spread out over days, beats cramming it into one session for long-term memory.

Good spacing usually means expanding gaps: review after about a day, then a few days, then a week or two, then a month.

## In practice

- After each lesson, take the quiz instead of re-reading the notes.
- When you get a question wrong, read the explanation, then come back to it another day.
- Little and often beats one long session: a daily streak of short quizzes is exactly what the research supports.""",
    "key_points": [
        "Memory fades fastest just after learning, then more slowly: the forgetting curve.",
        "Actively recalling information strengthens memory more than re-reading it.",
        "Spacing reviews out over time beats cramming for long-term retention.",
        "Some struggle while recalling is a desirable difficulty, not a sign of failure.",
    ],
    "figure_svg": FORGETTING_CURVE,
    "figure_caption": "Without review, recall drops steeply (red). Each spaced review (blue dots) lifts it back up, and it fades more slowly each time (green).",
    "questions": [
        {"kind": "mcq", "prompt": "What did Ebbinghaus's forgetting curve show?", "svg": "", "image_alt": "",
         "options": ["Memory fades at a steady rate every day", "Memory fades fast at first, then more slowly",
                     "Memory stays stable for a week, then drops suddenly", "Memory improves for a few days before fading"],
         "answer_index": 1, "model_answer": "", "key_points": [],
         "explanation": "Most loss happens soon after learning; what survives fades more gently. It isn't a steady, linear decline."},
        {"kind": "mcq", "prompt": "In this graph, what does the red line show?", "svg": FORGETTING_CURVE,
         "image_alt": "A graph of recall against days since learning, with a red curve dropping steeply and a green curve that jumps back up at two blue review points.",
         "options": ["Recall when you review on a schedule", "How long each review takes",
                     "Recall when you never review", "How hard the material is"],
         "answer_index": 2, "model_answer": "", "key_points": [],
         "explanation": "The red line falls away with nothing to lift it: it's labelled 'No review'. The green line is the one with spaced reviews."},
        {"kind": "mcq", "prompt": "Which study method does the research say builds the strongest long-term memory?", "svg": "", "image_alt": "",
         "options": ["Re-reading your notes several times", "Highlighting the key sentences",
                     "Testing yourself on the material", "Copying the text out by hand"],
         "answer_index": 2, "model_answer": "", "key_points": [],
         "explanation": "Retrieval practice (testing yourself) strengthens memory. Re-reading and highlighting feel productive but mostly build familiarity."},
        {"kind": "mcq", "prompt": "Why does re-reading often feel more effective than it is?", "svg": "", "image_alt": "",
         "options": ["Because familiar text is mistaken for knowing it", "Because reading is slower than testing",
                     "Because the brain can only store what it reads twice", "Because re-reading tires you out"],
         "answer_index": 0, "model_answer": "", "key_points": [],
         "explanation": "Text you've seen before feels familiar, and that fluency is easy to mistake for being able to recall it."},
        {"kind": "mcq", "prompt": "Two groups studied the same passage for the same time. Based on the lesson, which group in the chart most likely practised recalling it?",
         "svg": TWO_GROUPS, "image_alt": "A bar chart of recall one week later: Group X at 40 percent and Group Y at 70 percent.",
         "options": ["Group X", "Group Y", "Neither: they'd score the same", "You can't tell anything from recall"],
         "answer_index": 1, "model_answer": "", "key_points": [],
         "explanation": "Retrieval practice leads to much better recall a week later, so the higher bar (Group Y) fits the group that practised recalling."},
        {"kind": "mcq", "prompt": "What is the spacing effect?", "svg": "", "image_alt": "",
         "options": ["Leaving blank space in your notes helps memory", "Studying in several different rooms",
                     "The same study time spread over days beats cramming it", "Shorter lessons are always better than longer ones"],
         "answer_index": 2, "model_answer": "", "key_points": [],
         "explanation": "Spreading reviews over time gives better long-term retention than one long session, even with the same total time."},
        {"kind": "mcq", "prompt": "In the review schedule pictured, which gap is the right one to put at point B?", "svg": INTERVALS,
         "image_alt": "A timeline from day 0 to day 30 with reviews at day 0, a point A just after day 0, day 3, a point B in orange about a third of the way to day 30, and day 30.",
         "options": ["Day 1", "Day 2", "About day 10", "Day 29"],
         "answer_index": 2, "model_answer": "", "key_points": [],
         "explanation": "Good spacing expands: about a day, then a few days, then a week or two, then a month. Between day 3 and day 30, about day 10 fits."},
        {"kind": "open", "prompt": "In your own words, explain why testing yourself helps you remember more than re-reading does.", "svg": "", "image_alt": "",
         "options": [], "answer_index": -1,
         "model_answer": "Testing makes you retrieve the idea from memory, and that effortful reconstruction strengthens it. Re-reading only makes the text feel familiar, which isn't the same as being able to recall it.",
         "key_points": ["retrieving or recalling strengthens memory", "re-reading only builds familiarity"],
         "explanation": "The act of recall is what strengthens memory; familiarity from re-reading can fool you into thinking you know it."},
        {"kind": "open", "prompt": "You have a test in three weeks and five hours to study. Describe how you'd spread those hours out, and why.", "svg": "", "image_alt": "",
         "options": [], "answer_index": -1,
         "model_answer": "Split the five hours into short sessions spread across the three weeks, with gaps that grow (a day, a few days, a week), and spend them quizzing myself rather than re-reading. Spaced retrieval keeps resetting the forgetting curve so more survives to the test.",
         "key_points": ["short sessions spread over the weeks", "growing gaps between sessions", "self-testing during sessions"],
         "explanation": "Spacing plus retrieval practice gives the most durable memory for the same total time."},
        {"kind": "open", "prompt": "What is a 'desirable difficulty', and why might a hard quiz be a good sign?", "svg": "", "image_alt": "",
         "options": [], "answer_index": -1,
         "model_answer": "A desirable difficulty is a struggle during learning that makes the memory stronger, like having to work to recall an answer. A hard quiz means you're actually retrieving rather than recognising, which is what builds lasting memory.",
         "key_points": ["struggle that improves learning", "effortful recall strengthens memory"],
         "explanation": "Effort during recall is part of what makes it work, so some difficulty is a feature, not a failure."},
    ],
}

LESSON_2 = {
    "title": "Building a review habit that lasts",
    "minutes": 6,
    "body": """Knowing that spaced retrieval works is the easy part. The hard part is doing it week after week. This lesson turns the science into a routine.

## Flashcards and the Leitner system

A simple way to schedule reviews is the **Leitner system**, invented by the science journalist Sebastian Leitner in the 1970s. Cards live in numbered boxes:

1. New cards start in **Box 1**, reviewed every day.
2. Answer a card correctly and it **moves up** a box, so you see it less often.
3. Get it wrong and it goes **back to Box 1**.

The result is that your time goes where it's needed: cards you struggle with come back often, and cards you know well fade into the background. Modern apps such as Anki use algorithms that work the same way, with more precise intervals.

## Interleaving

When you practise, mixing related topics or problem types is called **interleaving**. Practising one type at a time (*blocking*) feels smoother, but interleaving makes you choose which idea applies, which is closer to real life and tends to produce better long-term results.

## Habits beat willpower

Researchers who study habits find that behaviour sticks when it's **small, consistent and tied to a cue**. "Study more" fails; "do one quiz with my morning coffee" works. A visible **streak** helps too, because it gives you a reason not to break the chain.

> **Tip:** set a daily goal small enough to hit on a bad day. Missing a day matters far less than giving up after missing one.

## In practice

- Treat each SirisLearn quiz as a review: retake lessons you scored lower on after a few days.
- Mix courses across the week rather than finishing one before starting the next.
- Anchor your daily session to something you already do every day.""",
    "key_points": [
        "The Leitner system moves cards up a box when right and back to Box 1 when wrong.",
        "Interleaving different topics beats practising one type at a time for long-term learning.",
        "Small, consistent habits tied to a cue last longer than willpower.",
    ],
    "figure_svg": LEITNER,
    "figure_caption": "In the Leitner system, a correct answer moves a card up a box (green); a wrong answer sends it back to Box 1 (red).",
    "questions": [
        {"kind": "mcq", "prompt": "In the Leitner system, what happens to a card you answer correctly?", "svg": "", "image_alt": "",
         "options": ["It stays in the same box", "It moves up a box and is reviewed less often",
                     "It's removed from the deck", "It goes back to Box 1"],
         "answer_index": 1, "model_answer": "", "key_points": [],
         "explanation": "Correct cards move up a box, so they come back less often. Wrong cards go back to Box 1."},
        {"kind": "mcq", "prompt": "In the diagram, what does the red arrow marked Q represent?", "svg": LEITNER,
         "image_alt": "Three boxes in a row labelled Box 1 every day, Box 2 every 3 days and Box 3 weekly. Green arrows marked P point from each box to the next; a red arrow marked Q curves from Box 3 back to Box 1.",
         "options": ["A card answered correctly", "A new card being added",
                     "A card answered wrongly going back to Box 1", "A card being deleted"],
         "answer_index": 2, "model_answer": "", "key_points": [],
         "explanation": "Q runs from the last box back to Box 1: that's what happens to a card you get wrong, wherever it was."},
        {"kind": "mcq", "prompt": "In the same diagram, what do the green arrows marked P represent?", "svg": LEITNER,
         "image_alt": "Three boxes in a row labelled Box 1 every day, Box 2 every 3 days and Box 3 weekly, with green arrows marked P from each box to the next.",
         "options": ["Cards answered correctly moving up", "Cards answered wrongly", "The order you should study the boxes", "Cards that are due today"],
         "answer_index": 0, "model_answer": "", "key_points": [],
         "explanation": "A correct answer moves a card up a box, towards less frequent review."},
        {"kind": "mcq", "prompt": "Why does the Leitner system make good use of study time?", "svg": "", "image_alt": "",
         "options": ["It reviews every card every day", "It shows hard cards often and easy cards rarely",
                     "It only shows new cards", "It removes cards after one correct answer"],
         "answer_index": 1, "model_answer": "", "key_points": [],
         "explanation": "Time goes to the cards you struggle with, while ones you know well come back less and less."},
        {"kind": "mcq", "prompt": "What is interleaving?", "svg": "", "image_alt": "",
         "options": ["Studying with a partner", "Mixing different topics or problem types in one session",
                     "Taking breaks between study sessions", "Writing notes between the lines"],
         "answer_index": 1, "model_answer": "", "key_points": [],
         "explanation": "Interleaving mixes problem types, so you have to choose which idea applies. Breaks between sessions are spacing, a different idea."},
        {"kind": "mcq", "prompt": "Which daily goal is most likely to become a lasting habit?", "svg": "", "image_alt": "",
         "options": ["Study as much as possible every day", "Do one quiz with my morning coffee",
                     "Study for three hours every Sunday", "Study whenever I feel motivated"],
         "answer_index": 1, "model_answer": "", "key_points": [],
         "explanation": "Small, consistent behaviours tied to a cue (morning coffee) stick far better than big goals or waiting for motivation."},
        {"kind": "mcq", "prompt": "Who devised the box-based flashcard system described in this lesson?", "svg": "", "image_alt": "",
         "options": ["Hermann Ebbinghaus", "Sebastian Leitner", "B. F. Skinner", "Maria Montessori"],
         "answer_index": 1, "model_answer": "", "key_points": [],
         "explanation": "Sebastian Leitner described the system in the 1970s. Ebbinghaus is behind the forgetting curve from the previous lesson."},
        {"kind": "open", "prompt": "Explain why interleaving can feel harder than blocking yet lead to better long-term learning.", "svg": "", "image_alt": "",
         "options": [], "answer_index": -1,
         "model_answer": "Interleaving forces you to work out which idea or method fits each problem, which takes more effort than repeating one method in a row. That extra effort is a desirable difficulty: it builds the skill of choosing and makes the learning last.",
         "key_points": ["you have to choose which method applies", "the extra effort strengthens long-term learning"],
         "explanation": "Blocking feels smooth because you already know which method to use; interleaving trains the choice itself."},
        {"kind": "open", "prompt": "You missed two days of your learning streak. Based on this lesson, what should you do next, and why?", "svg": "", "image_alt": "",
         "options": [], "answer_index": -1,
         "model_answer": "Just start again today with a small, easy session tied to my usual cue. Missing a couple of days matters far less than giving up, and keeping the habit small makes it easy to restart.",
         "key_points": ["restart straight away", "keep the session small", "missing days matters less than quitting"],
         "explanation": "Consistency over time is what counts; a missed day only hurts if it turns into stopping."},
        {"kind": "open", "prompt": "Design a simple weekly routine that uses spacing, retrieval and interleaving across two courses.", "svg": "", "image_alt": "",
         "options": [], "answer_index": -1,
         "model_answer": "Do one short quiz a day, alternating between the two courses, and on the weekend retake the lessons I scored lowest on from earlier in the week. That mixes topics, uses quizzes rather than re-reading, and revisits material after a gap.",
         "key_points": ["short regular sessions or quizzes", "alternate or mix the courses", "revisit earlier lessons after a gap"],
         "explanation": "A good routine mixes topics (interleaving), relies on quizzes (retrieval) and comes back to material later (spacing)."},
    ],
}

COURSE = {
    "topic": "How to learn anything faster",
    "title": "How to learn anything faster",
    "summary": "The science of memory and how to use it: why we forget, and the habits that make learning stick. A short starter course that also shows how SirisLearn works.",
    "icon": "brain",
    "level": "beginner",
    "length": "short",
    "sections": [{"title": "Learning that sticks", "summary": "How memory fades and the proven ways to keep it."}],
    "lessons": [
        ("Why we forget, and how to stop it", "Explain the forgetting curve and why retrieval and spacing work.", LESSON_1),
        ("Building a review habit that lasts", "Set up a review routine using the Leitner system, interleaving and small habits.", LESSON_2),
    ],
}


def seed(store: Store) -> None:
    if config.env("SIRISLEARN_SEED_SAMPLE", "true").lower() in ("0", "false", "no"):
        return
    if store.setting("sample_seeded") or store.courses():
        return
    now = now_iso()
    course = {k: COURSE[k] for k in ("topic", "title", "summary", "icon", "level", "length", "sections")}
    course.update(id=new_id(), status="ready", created_at=now, updated_at=now)
    store.insert("courses", course)
    store.replace_lessons(course["id"], [
        {"id": new_id(), "course_id": course["id"], "section_idx": 0, "position": i, "title": title, "summary": summary,
         "status": "ready", "content": clean_lesson(content), "generated_at": now}
        for i, (title, summary, content) in enumerate(COURSE["lessons"])
    ])
    store.set_setting("sample_seeded", now)
