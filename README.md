# SirisLearn

**Version 1.2** ([release notes](docs/releases/1.2.md))

SirisLearn is a private learning app in the Siris family, something like
LinkedIn Learning but built for one person. Give it any topic and it writes
you a course: sections of short lessons, each followed by a 10-question quiz,
and a final exam with a certificate. A daily review brings back what you've
learned at growing intervals, so it sticks. It tracks XP, levels, a daily
goal, streaks, awards and your full learning history, saves what you learn to
your Second Brain, and shows up in SirisOS as a tile, a widget, search
results and inbox reminders.

It uses the same Liquid Glass design as SirisOS, installs to the iPhone home
screen as a PWA, works offline for lessons you've opened, and can send
reminders to your phone.

## How it works

1. **Ask for a topic.** On Today or in the Library, type what you want to learn
   (or tap an idea, taken from your Second Brain's busiest topics when it's
   linked), pick a level (beginner, intermediate, advanced) and a size (short
   ≈ 6 lessons, standard ≈ 14, deep dive ≈ 24), and optionally add notes ("I'm
   an engineer, go heavy on the maths").
2. **Claude plans the course** as sections of lessons, in about a minute, and
   files it under an area (engineering, technology…) with tags.
3. **Lessons are written as you go.** Opening a lesson writes it (a 5–10 minute
   read with a diagram, key points and, where it helps, a real photo from
   Wikimedia Commons with its credit) and writes the next one ahead. Set
   `SIRISLEARN_PREGENERATE=all` to write whole courses up front instead.
   **Listen** reads a lesson aloud with your device's voice, and **Ask Siris**
   explains anything in it another way.
4. **Each lesson ends with a 10-question quiz**: 6–7 multiple choice and 3–4
   written answers, with at least 3 picture questions. Every answer is marked
   straight away with an explanation; written answers are marked by Claude
   against the lesson's key points. Got one wrong? **Help me understand**
   asks Siris why.
5. **Retakes get fresh questions.** After each quiz a new set is written in
   the background, so a retake tests understanding, not memory of the last
   quiz. Without a model, questions you've seen come back with shuffled
   options.
6. **Score 70% to pass** the lesson (its key points are saved to your Second
   Brain). Pass every lesson to unlock the **final exam**: 20 questions from
   across the course; 80% earns a printable **certificate**.
7. **The daily review** brings back questions you've answered, spaced out
   (the Leitner system): right answers move up a box and return after 3, 7,
   14, 30 then 60 days; wrong ones return tomorrow.

### XP, levels, streaks and awards

| | |
| --- | --- |
| XP | 10 per right multiple-choice answer, 15 per right written answer (7 if partly right), +20 the first time you pass a lesson, +15 for 10/10, +100 for finishing a course, +150 for passing its final exam; in the daily review 5 per right answer (2 partly) +10 for finishing |
| Level | Level *n* needs 50·*n*·(*n*−1) XP: 100 for level 2, 300 for 3, 600 for 4… |
| Daily goal | XP per day (default 50; Casual 20 to Intense 200 in Settings) |
| Streak | Days in a row (in `SIRISLEARN_TIMEZONE`) with a **passed** quiz, a daily review or a passed exam. A failed quiz doesn't count. Until today's is done the streak is "at risk" |
| Streak freezes | One earned for every 7 days of streak (hold up to 2). A single missed day uses one automatically; frozen days show on the heatmap |
| Awards | 30, bronze to platinum: streaks (3 → 100 days), perfect scores, lessons and courses finished, final exams, daily reviews, long-memory cards, XP milestones, written and picture answers, goal days, freezes, Night owl, Early bird, Marathon, Comeback… Locked ones show your progress |

### Screens

- **Today**: streak (with freezes), daily-goal ring, level, the daily review,
  *Continue*, *Learn something new* with topic ideas, your courses, recent awards.
- **Library**: every course with its progress, filtered by status and area, as
  a grid or a **map** (courses by area, in level order).
- **Course**: sections and lessons, scores, the final exam, related courses.
- **Lesson**: photo, diagram, the read, key points, Listen, Ask Siris, *Start quiz*.
- **Quiz, daily review and final exam**: one question at a time, then results:
  score, XP, streak, goal, level-ups, new awards and a review of every answer.
- **Certificate**: printable (or save as PDF) once you pass a course's exam.
- **History**: a six-month heatmap, totals and a day-by-day timeline.
- **Awards** and **Settings** (daily goal, notifications, Second Brain, the
  course writer and what it has cost).

Deleting a course keeps its history and awards.

### Built-in courses

SirisLearn ships with hand-written courses, added to the library once (turn
off with `SIRISLEARN_SEED_PACKS=false`): see `apps/backend/app/packs/`. They
work without a model; with one, retakes still get fresh questions.

| Topic | Beginner | Intermediate | Expert |
| --- | --- | --- | --- |
| Docker | Docker from scratch | Docker in practice | Docker at expert level |
| Linux | Linux from scratch | Linux power user | Linux internals and administration |
| Water and civil engineering | Water and civil engineering fundamentals | Water engineering design | Water engineering at expert level |

Each has two sections of three lessons, with a diagram per lesson and ten
questions per lesson (multiple choice and open, some on pictures). Packs are
added once by id; editing a pack later doesn't change a copy already added.

## Deploy

```bash
git clone https://github.com/bradmairs/SirisLearn.git
cd SirisLearn
cp .env.example .env    # set the password, JWT secret, ANTHROPIC_API_KEY and SIRISLEARN_HUB_KEY
make up                 # http://<server>:8100
```

Everything lives in `data/sirislearn.db` (SQLite), with a daily copy in
`data/backups/`. Back up that folder.
`make update` pulls and rebuilds; `make logs`, `make status` as usual.

| Variable | Purpose |
| --- | --- |
| `SIRISLEARN_PORT`, `SIRISLEARN_BIND` | Host port (default `8100`) and bind address |
| `SIRISLEARN_TIMEZONE` | When a day starts and ends for streaks and the daily goal (default Australia/Melbourne) |
| `SIRISLEARN_ADMIN_USERNAME`, `SIRISLEARN_ADMIN_PASSWORD`, `SIRISLEARN_JWT_SECRET` | Sign-in |
| `ANTHROPIC_API_KEY` | Claude writes the courses and marks written answers |
| `SIRISLEARN_MODEL`, `SIRISLEARN_EFFORT` | Model (default `claude-opus-5-5`) and how hard it thinks per lesson (`medium`) |
| `OLLAMA_URL`, `SIRISLEARN_OLLAMA_MODEL` | Alternative: a model on the LAN Ollama (`SIRISLEARN_LLM_PROVIDER=ollama`) |
| `SIRISLEARN_PREGENERATE` | `next` (default: write lessons as you reach them) or `all` |
| `SIRISLEARN_HUB_KEY` | The key SirisOS uses to read the widget, search and status |
| `SIRISAI_URL`, `SIRISAI_API_KEY` (+ `SIRISAI_USER`) | Second Brain: save passed lessons, suggest topics |
| `SIRISOS_PUBLIC_URL` | "Continue in Siris" opens the SirisOS assistant |
| `SIRISLEARN_PUBLIC_URL` | Links back to lessons in Second Brain notes |
| `SIRISLEARN_PHOTOS` | Wikimedia Commons photos for lessons (default on) |
| `SIRISLEARN_REMINDER_HOUR`, `SIRISLEARN_REVIEW_HOUR`, `SIRISLEARN_PUSH_CONTACT` | Phone reminders (turned on per device in Settings) |
| `SIRISLEARN_BACKUP_DAYS` | Daily database backups kept in `data/backups` (default 14) |
| `SIRISLEARN_SEED_PACKS` | Add the built-in courses once (default `true`) |
| `SIRISLEARN_SEED_SAMPLE` | Add the starter course on first run (default `true`) |

Without a model, the app still works (history, awards, the starter course and
anything already written) but can't write new courses; Settings says so.

**Cost.** With Claude, each course is one planning call plus one call per
lesson (about 6–10k output tokens: the lesson, diagrams and quiz), plus one
per retake for fresh questions. Settings shows the running cost. The fixed
instructions and the course plan are prompt-cached, so lessons in the same
course reuse them. Written answers are marked with a short, low-effort call.
Requests use Claude's server-side refusal fallback, so a rare false-positive
decline is retried on another model instead of failing.

## Linking to SirisOS

SirisOS shows SirisLearn as a tile with a widget (streak, XP today against
the goal, level, active courses, and the next lesson), includes its courses
and lessons in ⌘K search, and puts "your N-day learning streak ends at
midnight" in the inbox when today's quiz isn't done yet. See SirisOS ADR 112.

In SirisOS's `.env`:

```bash
SIRISLEARN_URL=http://192.168.0.100:8100       # how the SirisOS container reaches it
SIRISLEARN_PUBLIC_URL=https://learn.example.org # optional: what links open on your phone
SIRISLEARN_HUB_KEY=<same value as SIRISLEARN_HUB_KEY here>
```

The hub routes (all need `X-API-Key: <SIRISLEARN_HUB_KEY>`; links are paths
in this app):

| Route | Returns |
| --- | --- |
| `GET /api/hub/v1/status` | `{status, version, llm: {provider, model, configured}}` |
| `GET /api/hub/v1/summary` | `streak {current, best, today_done, at_risk, freezes}`, `xp {total, today, goal, goal_met, week}`, `level`, `courses {total, active, completed, planning}`, `continue {course_title, lesson_title, url, progress}`, `review {due, next_due, cards}`, `achievements`, `recent` |
| `GET /api/hub/v1/search?q=` | `{hits: [{title, subtitle, url, kind: "course" \| "lesson"}]}` |

## Development

```bash
make backend   # API on :8000 (data in ./data)
make web       # Vite on :5173, proxying /api to :8000
make test      # pytest + typecheck + vitest
```

## Repository layout

- `apps/backend` (FastAPI, Python 3.13):
  - `app/main.py` health, sign-in, routers and the built web app;
  - `app/api.py` the web app's routes, `app/hub.py` the SirisOS routes;
  - `app/generator.py` plans courses and writes lessons in the background,
    `app/prompts.py` the instructions and JSON schemas, `app/llm.py` Claude
    (official SDK, structured outputs, caching, refusal fallback) and Ollama,
    `app/svg.py` cleans the model's diagrams;
  - `app/quiz.py` lesson quizzes, reviews and exams, and marking;
    `app/spaced.py` the daily review; `app/progress.py` XP, levels, streaks,
    freezes, goal and history; `app/achievements.py` the awards;
  - `app/siris.py` the Second Brain and SirisOS links, `app/photos.py`
    Wikimedia Commons, `app/push.py` notifications, `app/jobs.py` reminders
    and backups;
  - `app/db.py` SQLite storage, `app/sample.py` the starter course,
    `app/coursepacks.py` and `app/packs/` the built-in courses.
- `apps/web` (React + TypeScript PWA; `public/sw.js` is the offline and
  notification service worker): `src/glass/glass.css` is the SirisOS
  Liquid Glass design system, `src/screens/` the screens,
  `src/components/Markdown.tsx` renders lessons without raw HTML.
- `docs/releases/` release notes; `scripts/bump-version.sh` bumps the version.
