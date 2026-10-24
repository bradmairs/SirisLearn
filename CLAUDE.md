# Working on SirisLearn

Read [README.md](README.md) (the handover) first. SirisLearn follows the
SirisOS conventions: same design system, same versioning.

## Versions and shipping

- **Bump the version in every pull request**: `scripts/bump-version.sh patch` (+0.01) for fixes and small changes, `scripts/bump-version.sh minor` (+0.1) for a new feature or screen. Fill in the `docs/releases/<version>.md` it starts. See [docs/releases.md](docs/releases.md).
- **Merge to main automatically** (Brad's standing instruction): open the pull request, wait for CI to go green, then mark it ready and merge it (squash) without asking. Fix red CI first; never merge red.
- Merging a `VERSION` change tags `v<version>` and publishes the GitHub release.

## Checks before pushing

- Backend: `cd apps/backend && python -m pytest -q`
- Web: `cd apps/web && npx tsc -b --noEmit && npm test`

## Things to keep true

- The SirisOS hub contract (`app/hub.py`, README "Linking to SirisOS") is read by SirisOS's `SirisLearnConnector`. Change it only together with SirisOS.
- Model output is untrusted: lessons go through `generator.clean_lesson`, diagrams through `svg.sanitize`, and the web app renders Markdown without raw HTML and SVGs only as `<img>`.
- Answers (`answer_index`, `model_answer`, `key_points`, `explanation`) never reach the browser before the question is answered.
- `glass.css` is copied from SirisOS; keep it in step rather than diverging.

## Siris: record what you build (Brad's standing instruction)

Siris is Brad's second brain, the private repo `bradmairs/Siris-Second-Brain`, and his manual for rebuilding everything. When a session in this repo builds, changes, deploys or retires a feature, record it in Siris before finishing, without being asked:

- Follow `plugins/siris-brain/skills/learn/SKILL.md` in that repo. In a cloud session, attach it first (owner `bradmairs`, repo `Siris-Second-Brain`, push access). Always write through its engine (`tools/brain.py learn`), never by editing notes directly, then commit and push.
- Add to this app's note, **"SirisLearn"**, so it gets a dated update instead of a duplicate.
- Capture what changed and why, the version, how to deploy or update it, the settings that matter (names only), and lessons learned. Never write secrets.
- End your reply with one line, e.g. `🧠 Siris learned: [[SirisLearn]] (updated)`.
