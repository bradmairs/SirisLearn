# Releases and versions

SirisLearn has one version, in [`/VERSION`](../VERSION) (e.g. `1.0`, `1.01`, `1.1`).
The API (`apps/backend/app/version.py`) and the web app (`apps/web/src/version.ts`,
shown in the side menu) follow it, and CI checks they match.

Each change bumps it in the same pull request, the same way as SirisOS:

- **+0.01** (`scripts/bump-version.sh patch`): fixes, tweaks and small changes.
- **+0.1** (`scripts/bump-version.sh minor`): a new feature, screen or integration.

The script writes all three and starts `docs/releases/<version>.md`; fill it in.
Merging a `VERSION` change to main tags `v<version>` and publishes the GitHub
release from those notes (`.github/workflows/release.yml`).
