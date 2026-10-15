# SirisLearn

**Version 1.0** ([release notes](docs/releases/1.0.md))

SirisLearn is a private learning app in the Siris family, something like
LinkedIn Learning but built for one person. Give it any topic and it writes
you a course: sections of short lessons, each followed by a 10-question quiz.
It tracks XP, levels, a daily goal, streaks, awards and your full learning
history, and shows up in SirisOS as a tile, a widget, search results and
inbox reminders.

It uses the same Liquid Glass design as SirisOS and installs to the iPhone
home screen as a PWA.

## How it works

1. **Ask for a topic.** On Today or in the Library, type what you want to learn,
   pick a level (beginner, intermediate, advanced) and a size (short ≈ 6
   lessons, standard ≈ 14, deep dive ≈ 24), and optionally add notes ("I'm an
   engineer, go heavy on the maths").
2. **Claude plans the course** as sections of lessons, in about a minute.
3. **Lessons are written as you go.** Opening a lesson writes it (a 5–10 minute
   read with a diagram and key points) and writes the next one ahead, so it's
   ready when you get there. Set `SIRISLEARN_PREGENERATE=all` to write whole
   courses up front instead.
4. **Each lesson ends with a 10-question quiz**: 6–7 multiple choice and 3–4
   written answers, with at least 3 picture questions (diagrams to read,
   label or estimate from). Every answer is marked straight away with an
   explanation. Written answers are marked by Claude against the lesson's key
   points ("correct", "partly right" or "not quite", with feedback).
5. **Score 70% to pass** the lesson. Pass every lesson to finish the course.

### XP, levels, streaks and awards

| | |
| --- | --- |
| XP | 10 per right multiple-choice answer, 15 per right written answer (7 if partly right), +20 the first time you pass a lesson, +15 for 10/10, +100 for finishing a course |
| Level | Level *n* needs 50·*n*·(*n*−1) XP: 100 for level 2, 300 for 3, 600 for 4… |
| Daily goal | XP per day (default 50; Casual 20 to Intense 200 in Settings) |
| Streak | Days in a row with at least one finished quiz (in `SIRISLEARN_TIMEZONE`). Until today's quiz is done, the streak is "at risk" |
| Awards | 24, bronze to platinum: streaks (3 → 100 days), perfect scores, lessons and courses finished, XP milestones, written and picture answers, goal days, Night owl, Early bird, Marathon, Comeback… Locked ones show your progress |

### Screens

- **Today**: streak, daily-goal ring, level, *Continue* (the next lesson in the
  course you touched last), *Learn something new*, your courses, recent awards.
- **Library**: every course with its progress; in progress, completed, archived.
- **Course**: the sections and lessons, what's passed, your best score on each,
  what's being written. Retry anything that failed; archive or delete.
- **Lesson**: the read, the diagram and key points, previous scores, *Start
  quiz*, and *Rewrite lesson* if you'd like it explained differently.
- **Quiz**: one question at a time, then results: score, XP earned, streak,
  goal, level-ups, new awards, and a review of every answer.
- **History**: a six-month heatmap, totals (XP, active days, lessons passed,
  quizzes, accuracy, time in quizzes) and a day-by-day timeline.
- **Awards** and **Settings** (daily goal, which model writes the courses).

Deleting a course keeps its history and awards.

## Deploy

```bash
git clone https://github.com/bradmairs/SirisLearn.git
cd SirisLearn
cp .env.example .env    # set the password, JWT secret, ANTHROPIC_API_KEY and SIRISLEARN_HUB_KEY
make up                 # http://<server>:8100
```

Everything lives in `data/sirislearn.db` (SQLite). Back up that folder.
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
| `SIRISLEARN_SEED_SAMPLE` | Add the starter course on first run (default `true`) |

Without a model, the app still works (history, awards, the starter course and
anything already written) but can't write new courses; Settings says so.

**Cost.** With Claude, each course is one planning call plus one call per
lesson (about 6–10k output tokens: the lesson, diagrams and quiz). The fixed
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
| `GET /api/hub/v1/summary` | `streak {current, best, today_done, at_risk}`, `xp {total, today, goal, goal_met, week}`, `level`, `courses {total, active, completed, planning}`, `continue {course_title, lesson_title, url, progress}`, `achievements`, `recent` |
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
  - `app/quiz.py` attempts and marking, `app/progress.py` XP, levels, streaks,
    goal and history, `app/achievements.py` the awards;
  - `app/db.py` SQLite storage, `app/sample.py` the starter course.
- `apps/web` (React + TypeScript PWA): `src/glass/glass.css` is the SirisOS
  Liquid Glass design system, `src/screens/` the screens,
  `src/components/Markdown.tsx` renders lessons without raw HTML.
- `docs/releases/` release notes; `scripts/bump-version.sh` bumps the version.
