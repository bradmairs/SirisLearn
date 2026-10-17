"""Docker in practice: intermediate."""

from app.coursepacks import mcq, open_q
from app.packs._draw import AMBER, BLUE, GREEN, INK, MUTED, PURPLE, RED, arrow, box, line, svg, text, title

MULTISTAGE = svg(
    title("Multi-stage build"),
    box(30, 60, 190, 170, "", AMBER), text(125, 84, "Stage 1: build", 14, AMBER, weight="bold"),
    text(125, 112, "FROM node:22 AS build", 12, INK), text(125, 136, "compilers, dev deps,", 12, MUTED),
    text(125, 156, "source code, caches", 12, MUTED), text(125, 196, "≈ 1.2 GB", 16, AMBER, weight="bold"),
    box(260, 60, 190, 170, "", GREEN), text(355, 84, "Stage 2: runtime", 14, GREEN, weight="bold"),
    text(355, 112, "FROM nginx:1.27-alpine", 12, INK), text(355, 136, "only the built files", 12, MUTED),
    text(355, 196, "≈ 50 MB", 16, GREEN, weight="bold"),
    arrow(220, 160, 258, 160, BLUE, "COPY --from=build", dy=-12, size=11),
    text(240, 270, "Only the final stage becomes the image you ship", 13, MUTED),
)

CACHE = svg(
    title("Which steps re-run after editing src/app.js?"),
    box(60, 50, 360, 30, "1  FROM node:22-slim", GREEN, size=13),
    box(60, 86, 360, 30, "2  WORKDIR /app", GREEN, size=13),
    box(60, 122, 360, 30, "3  COPY package*.json ./", GREEN, size=13),
    box(60, 158, 360, 30, "4  RUN npm ci", GREEN, size=13),
    box(60, 194, 360, 30, "5  COPY . .", AMBER, size=13),
    box(60, 230, 360, 30, "6  RUN npm run build", AMBER, size=13),
    text(240, 285, "green = from cache   amber = re-runs", 13, MUTED),
)

NETWORKS = svg(
    title("User-defined bridge networks"),
    box(20, 55, 210, 150, "", BLUE), text(125, 78, "network: frontend", 13, BLUE),
    box(250, 55, 210, 150, "", PURPLE), text(355, 78, "network: backend", 13, PURPLE),
    box(40, 100, 80, 50, "proxy", INK, size=13), box(190, 125, 100, 50, "app", GREEN, size=13),
    box(360, 100, 80, 50, "db", AMBER, size=13),
    line(120, 125, 190, 145, BLUE), line(290, 150, 360, 125, PURPLE),
    arrow(80, 240, 80, 152, AMBER, "-p 443:443", dx=40, dy=10),
    text(240, 280, "app joins both; proxy can't reach db", 13, MUTED),
)

HEALTH = svg(
    title("depends_on with a health check"),
    box(30, 70, 130, 60, "db", AMBER, sub="starting"), box(30, 160, 130, 60, "db", GREEN, sub="healthy"),
    arrow(95, 130, 95, 158, MUTED),
    box(300, 160, 150, 60, "web", BLUE, sub="starts now"),
    arrow(160, 190, 298, 190, GREEN, "condition: service_healthy", dy=-12, size=11),
    text(240, 262, "pg_isready every 5 s, until it passes", 13, MUTED),
)

LIMITS = svg(
    title("Memory limit reached"),
    line(50, 240, 450, 240, INK), line(50, 240, 50, 50, INK),
    line(50, 90, 450, 90, RED, dash="6 5"), text(400, 82, "limit 512 MB", 12, RED),
    '<path d="M50 220 C 120 210, 170 190, 220 160 S 300 110, 330 92" fill="none" stroke="#5fd3ff" stroke-width="3"/>',
    text(330, 120, "X", 16, AMBER, weight="bold"),
    line(330, 92, 330, 235, AMBER, dash="4 4"),
    '<path d="M335 230 C 360 225, 400 215, 445 200" fill="none" stroke="#8af5c8" stroke-width="3"/>',
    text(250, 268, "time", 12, MUTED), text(30, 145, "RAM", 12, MUTED),
)

SECRETS = svg(
    title("Where should a database password live?"),
    box(30, 60, 200, 50, "In the Dockerfile (ENV)", RED, size=13),
    box(30, 125, 200, 50, "In compose.yaml in git", RED, size=13),
    box(250, 60, 200, 50, ".env file, not committed", AMBER, size=13),
    box(250, 125, 200, 50, "Docker secret file", GREEN, size=13),
    text(130, 210, "A: baked into images / history", 12, RED), text(350, 210, "B: kept out of the image", 12, GREEN),
    text(240, 255, "Secrets in image layers can be read by anyone with the image", 12, MUTED),
)

L1 = {
    "title": "Smaller, safer images with multi-stage builds",
    "minutes": 8,
    "photo_query": "",
    "body": """A beginner's Dockerfile tends to ship everything: compilers, build tools, test dependencies and source code. The image works, but it's huge, slow to pull and full of software an attacker could use. **Multi-stage builds** fix that.

## The idea

A Dockerfile can have several `FROM` lines. Each starts a new **stage**. You do the heavy work in an early stage and copy only the finished result into a small final stage:

```
FROM node:22 AS build
WORKDIR /src
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.27-alpine
COPY --from=build /src/dist /usr/share/nginx/html
```

Only the **last stage** becomes the image. The Node toolchain, `node_modules` and source code stay behind in the build stage. The shipped image is nginx plus static files, often 50 MB instead of over a gigabyte.

## Choosing a runtime base

The final stage should hold only what the app needs to run:

- **slim** variants (Debian minus extras) are a safe default for Python, Node and Java.
- **alpine** variants are tiny, but use the musl C library, which occasionally breaks compiled dependencies.
- **distroless** images (from Google) contain your app's runtime and nothing else: no shell, no package manager. Great for security, harder to debug.
- **scratch** is an empty image, perfect for a single static binary such as a Go program.

## Why smaller is better

- **Faster** pulls and deploys, especially on slow links or many servers.
- **Smaller attack surface**: fewer packages means fewer vulnerabilities to patch and fewer tools for an intruder.
- **Fewer surprises**: the image contains exactly what you meant to ship.

> **Common misconception:** deleting files in a later `RUN` shrinks the image. It doesn't: the files still exist in the earlier layer. Multi-stage builds (or cleaning up within the *same* `RUN`) are the fix.

## Targeting a stage

`docker build --target build -t myapp:dev .` stops at the named stage, which is handy for running tests in an image that still has the dev tools.

## In practice

Look at the size of your images with `docker images`. For anything over a few hundred MB, ask what the app really needs at runtime and move the rest into a build stage. For compiled languages the difference is dramatic: a Go service built from `golang:1.23` can ship as a 10 MB image on `scratch`.""",
    "key_points": [
        "Multi-stage builds use several FROM stages; only the last becomes the shipped image.",
        "COPY --from=stage copies just the build output into a small runtime stage.",
        "Slim, alpine, distroless and scratch are increasingly minimal runtime bases.",
        "Deleting files in a later layer doesn't shrink an image; the data is still in the earlier layer.",
    ],
    "figure_svg": MULTISTAGE,
    "figure_caption": "The heavy build stage stays behind; only the built files are copied into the small runtime image.",
    "questions": [
        mcq("In a multi-stage Dockerfile, which stage becomes the final image?", ["The first", "The last", "The largest", "All of them, merged"], 1,
            "Only the final stage is tagged and shipped (unless you use --target)."),
        mcq("In the diagram, what is copied from stage 1 to stage 2?", ["The whole Node toolchain", "Only the built files", "The source code", "The package cache"], 1,
            "COPY --from=build brings just the output, which is why the runtime image is small.",
            MULTISTAGE, "Two boxes: a 1.2 GB build stage with compilers and source, and a 50 MB runtime stage, with an arrow labelled COPY --from=build between them."),
        mcq("A Dockerfile downloads a 500 MB file in one RUN and deletes it in the next RUN. How does the image size change?", ["It shrinks by 500 MB", "The 500 MB stays in the earlier layer",
            "Docker deduplicates it away", "The build fails"], 1, "Layers are additive. Delete within the same RUN, or use a separate build stage."),
        mcq("Which base image contains nothing at all, suited to a single static binary?", ["alpine", "slim", "scratch", "distroless"], 2,
            "scratch is the empty image."),
        mcq("What's a downside of distroless images?", ["They're huge", "They have no shell, so debugging inside is harder", "They can't run Python", "They're not secure"], 1,
            "No shell or package manager is great for security but makes `docker exec ... sh` impossible."),
        mcq("What does `docker build --target build .` do?", ["Builds only up to the stage named build", "Pushes to a registry called build",
            "Builds every stage in parallel", "Deletes the build stage"], 0, "It stops at that stage, useful for test or dev images."),
        mcq("In the diagram, roughly how much smaller is the shipped image than the build stage?", ["About the same", "About half", "More than twenty times smaller", "Bigger"], 2,
            "About 1.2 GB down to about 50 MB.",
            MULTISTAGE, "Build stage about 1.2 GB; runtime stage about 50 MB."),
        open_q("Give two reasons a smaller image is better in production.", "Smaller images pull and deploy faster, and they contain fewer packages, so there are fewer vulnerabilities to patch and fewer tools an attacker could use.",
               ["faster to pull or deploy", "smaller attack surface or fewer vulnerabilities"], "Speed and security are the usual two."),
        open_q("Outline a multi-stage Dockerfile for a Go web service.", "Stage one uses a golang image to copy the source and run go build to produce a static binary; stage two starts FROM scratch (or distroless) and copies just that binary in, then sets it as the entrypoint.",
               ["build stage with golang compiles the binary", "final stage from scratch or distroless", "copy only the binary across"], "Static Go binaries are the classic scratch use case."),
        open_q("When might alpine be the wrong choice for a runtime image?", "When the app relies on compiled libraries built against glibc, because Alpine uses musl and those can fail or behave differently; a slim Debian image avoids that.",
               ["alpine uses musl not glibc", "compiled dependencies can break"], "Python wheels and some native Node modules are common culprits."),
    ],
}

L2 = {
    "title": "Fast builds: the cache and .dockerignore",
    "minutes": 7,
    "photo_query": "",
    "body": """A build that takes five minutes after every one-line change kills your flow. Understanding the **build cache** usually gets it down to seconds.

## How the cache decides

For each instruction, Docker (BuildKit) asks: have I run *exactly this* before, on *exactly this* starting layer?

- For `RUN`, the cache key is the command text plus the layer it runs on.
- For `COPY` and `ADD`, it's also a checksum of the files being copied.

If the key matches, the layer is reused (`CACHED` in the output). The first miss invalidates **everything after it**, because every later layer sits on a changed one.

## Ordering for the cache

Put slow, rarely changing steps first and fast, often changing ones last:

1. Base image and system packages.
2. Dependency manifests (`package.json`, `requirements.txt`, `go.mod`) copied on their own.
3. Install dependencies.
4. Copy the rest of the source.
5. Build.

Editing source now only re-runs steps 4 and 5.

## .dockerignore

The **build context** (usually `.`) is sent to the builder before anything runs. Without a `.dockerignore`, that includes `.git`, `node_modules`, build output and maybe gigabytes of data. Worse, any of it changing invalidates a `COPY . .` even if the app didn't change.

A typical `.dockerignore`:

```
.git
node_modules
dist
*.log
.env
```

## Cache mounts

BuildKit can give a `RUN` step a persistent cache directory that isn't stored in the image:

```
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
```

Even when this layer must re-run (because requirements changed), pip reuses its downloads, so it's much faster.

## Common cache busters

- `COPY . .` too early in the file.
- `RUN apt-get update` in a separate layer from `apt-get install` (the update gets cached and goes stale; combine them in one `RUN`).
- Embedding something that changes every build, like a timestamp, early on.

> **Tip:** `docker build --no-cache` forces a clean rebuild, useful occasionally to pick up security updates in base packages.

## In practice

Run your build twice in a row: the second should be almost entirely `CACHED`. Then edit one source file and rebuild: only the steps from your source `COPY` onwards should run. If more re-runs, look for the first step that missed and ask why.""",
    "key_points": [
        "A cache miss at one step forces every later step to re-run.",
        "Copy dependency manifests and install before copying the rest of the source.",
        ".dockerignore keeps .git, node_modules, build output and secrets out of the build context.",
        "BuildKit cache mounts keep package-manager downloads between builds without bloating the image.",
    ],
    "figure_svg": CACHE,
    "figure_caption": "After editing src/app.js, steps 1–4 come from the cache; steps 5 and 6 re-run.",
    "questions": [
        mcq("In the diagram, why does step 5 re-run after editing src/app.js?", ["Docker always re-runs COPY", "COPY . . includes app.js, so its file checksum changed",
            "Step 4 failed", "The base image updated"], 1, "COPY's cache key includes the checksum of the copied files.",
            CACHE, "Six Dockerfile steps: 1 to 4 in green (cached), 5 COPY . . and 6 RUN npm run build in amber (re-run)."),
        mcq("Why does step 6 re-run in the diagram even though its command didn't change?", ["It sits on the changed layer from step 5", "RUN is never cached",
            "npm forces it", "The .dockerignore changed"], 0, "Everything after the first miss re-runs because it builds on a new layer.",
            CACHE, "Steps 5 and 6 re-run after step 5 misses the cache."),
        mcq("Which belongs in .dockerignore for a Node project?", ["package.json", "node_modules", "Dockerfile", "src"], 1,
            "node_modules is installed inside the build; sending your local copy is slow and can break things."),
        mcq("Why combine `apt-get update && apt-get install -y curl` in one RUN?", ["It's shorter", "A separately cached update layer goes stale and installs old package lists",
            "apt-get requires it", "It makes the image larger"], 1, "If update is cached on its own, a later install change reuses the old package index."),
        mcq("What does a BuildKit cache mount give you?", ["A volume in the final image", "A persistent build-time cache that isn't stored in the image",
            "Faster pushes", "A shared network"], 1, "Downloads are reused across builds without adding to image size."),
        mcq("Which change would make the whole Dockerfile re-run from the top?", ["Editing app.js", "Changing the FROM image tag", "Editing README.md (if ignored)", "Adding a comment at the end"], 1,
            "A different base invalidates every layer above it."),
        mcq("What's a hidden cost of a large build context?", ["Larger final image always", "It's uploaded to the builder before every build and can bust COPY caches",
            "It disables BuildKit", "Nothing"], 1, "The whole context is sent each time, and unrelated file changes can invalidate COPY . ."),
        open_q("Explain how the build cache decides whether to reuse a COPY layer.", "It reuses the layer only if the instruction is the same, it's building on the same parent layer, and the checksums of the files being copied haven't changed.",
               ["same instruction and parent layer", "file checksums unchanged"], "File content, not timestamps, is what counts."),
        open_q("Your build re-installs all dependencies every time you edit any source file. What's wrong and how do you fix it?", "The Dockerfile copies all the source before installing dependencies, so any edit busts the install layer. Copy only the dependency manifest first, install, then copy the rest of the source.",
               ["source copied before installing dependencies", "copy the manifest first, install, then copy source"], "This one change usually saves the most time."),
        open_q("When would you deliberately use --no-cache?", "When you want a clean rebuild, for example to pick up the latest security updates in base-image packages or to rule out a stale cached layer while debugging.",
               ["to force fresh package or security updates", "to rule out stale cache when debugging"], "Scheduled clean rebuilds keep images patched."),
    ],
}

L3 = {
    "title": "Container networking",
    "minutes": 8,
    "photo_query": "",
    "body": """Every container gets its own network stack: its own interfaces, IP address and ports. Docker connects them using **networks**, and choosing the right one decides who can talk to whom.

## The network drivers you'll use

- **bridge** (the default): a private virtual network on the host. Containers get private IPs and reach the outside world through NAT. Outsiders can't reach them unless you **publish** a port with `-p`.
- **host**: no isolation; the container uses the host's network directly. No `-p` needed (or possible), and the app binds straight onto the host's ports. Useful for some monitoring or discovery tools; it gives up a layer of isolation.
- **none**: no networking at all.
- **macvlan/ipvlan**: give a container its own address on your LAN, as if it were a separate machine. Handy for some home-lab cases (like a DNS server), but more complex.

## User-defined bridges

Containers on Docker's *default* bridge can only reach each other by IP. Create your own bridge and you get **DNS by container name**:

```
docker network create appnet
docker run -d --name db --network appnet postgres:16
docker run -d --name web --network appnet -p 8080:8000 myapp
```

Now `web` connects to `db:5432`. Compose does this for you automatically, one network per project.

## Isolation with multiple networks

A container can join several networks. Put the reverse proxy and app on a `frontend` network, and the app and database on a `backend` network. The app sits on both; the proxy can't reach the database at all. That's **network segmentation**: a compromised proxy can't talk directly to your data.

## Publishing ports carefully

`-p 8080:80` publishes on **all** host interfaces, so anyone who can reach the host can reach the container. Bind to one interface instead:

- `-p 127.0.0.1:8080:80` reachable only from the host itself (for example, behind a reverse proxy).
- `-p 192.168.0.10:8080:80` only on that LAN address.

> **Watch out:** on Linux, Docker writes its own firewall (iptables) rules for published ports, and these can bypass host firewalls like UFW. Don't rely on UFW alone to hide a published port; bind to 127.0.0.1 or don't publish it.

## Debugging

- `docker network ls` and `docker network inspect appnet` show networks and who's attached.
- From inside a container: `docker exec -it web sh`, then `getent hosts db` or `wget -qO- http://db:5432` to test name resolution and connectivity.
- A throwaway toolbox container on the same network (`nicolaka/netshoot` is popular) has every network tool you could want.

## In practice

Put each Compose app's database on an internal network with no published ports. Publish only the reverse proxy (ports 80 and 443) to the world, and bind any admin UIs to `127.0.0.1` or your LAN address.""",
    "key_points": [
        "Bridge networks are private; publish ports with -p to let outsiders in. Host networking removes isolation.",
        "User-defined bridges (and Compose networks) give DNS by container or service name.",
        "Containers can join several networks; use that to keep databases away from public-facing services.",
        "-p binds to all interfaces by default; bind to 127.0.0.1 or a LAN IP, and remember Docker's rules can bypass UFW.",
    ],
    "figure_svg": NETWORKS,
    "figure_caption": "The app joins both networks; the proxy (published on 443) can't reach the database directly.",
    "questions": [
        mcq("Two containers on Docker's default bridge network: how can one reach the other?", ["By container name", "By IP address only", "They can't communicate", "Through the host's DNS"], 1,
            "Name-based DNS works on user-defined networks, not the default bridge."),
        mcq("In the diagram, can the proxy connect to the database?", ["Yes, through the app's network", "No, they share no network", "Yes, through port 443", "Only by name"], 1,
            "The proxy is on frontend only and the db on backend only. Only the app is on both.",
            NETWORKS, "Two networks: frontend with proxy and app, backend with app and db; the proxy publishes port 443."),
        mcq("What does `-p 127.0.0.1:8080:80` change compared with `-p 8080:80`?", ["Nothing", "The port is only reachable from the host itself",
            "It uses IPv6", "It publishes on every interface"], 1, "Binding to 127.0.0.1 keeps it off the LAN, ideal behind a reverse proxy."),
        mcq("Which network mode makes the container use the host's network stack directly?", ["bridge", "host", "none", "overlay"], 1,
            "host mode removes network isolation; -p doesn't apply."),
        mcq("Why can a published Docker port be reachable even though UFW blocks it?", ["UFW is broken", "Docker inserts its own iptables rules for published ports",
            "Ports above 1024 bypass firewalls", "Containers use IPv6"], 1, "Docker manages NAT rules that come before UFW's. Bind addresses or don't publish."),
        mcq("In the diagram, which container is attached to both networks?", ["proxy", "app", "db", "None"], 1,
            "The app bridges both segments: it receives requests from the proxy and talks to the database.",
            NETWORKS, "Network segmentation diagram with proxy, app and db."),
        mcq("Which tool is a handy throwaway container for debugging networks?", ["nginx", "netshoot", "postgres", "scratch"], 1,
            "nicolaka/netshoot bundles dig, curl, tcpdump and more."),
        open_q("Explain why you'd put a database on a separate internal network from a public reverse proxy.", "So that only the app can reach the database; if the internet-facing proxy is compromised it still has no direct network path to the data. That's network segmentation.",
               ["only the app can reach the database", "limits damage if the proxy is compromised"], "Defence in depth: each hop is a barrier."),
        open_q("A container can't connect to db:5432 on a user-defined network. List the checks you'd make.", "Check both containers are on the same network (docker network inspect), check the name resolves from inside (getent hosts db), check the database container is running and listening on 5432 (logs), and check the connection details such as the port and credentials.",
               ["same network", "name resolves from inside", "database running and listening"], "Resolution, reachability, then the app itself."),
        open_q("When would you choose macvlan over a bridge network in a home lab?", "When a container needs its own IP address on the LAN, as if it were a separate machine, for example a DNS or DHCP server that other devices must reach directly on standard ports.",
               ["container gets its own LAN IP", "e.g. DNS or services needing standard ports"], "It's powerful but adds complexity; bridge is still the default."),
    ],
}

L4 = {
    "title": "Compose for real services: health checks and dependencies",
    "minutes": 8,
    "photo_query": "",
    "body": """The beginner course got a web app and database running with Compose. Real services need a bit more care: knowing when a service is actually ready, restarting on failure, and keeping configuration tidy.

## Health checks

A running container isn't necessarily a working one. A **health check** is a command Docker runs periodically inside the container to test it:

```
services:
  db:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U notes"]
      interval: 5s
      timeout: 3s
      retries: 10
      start_period: 10s
```

The container's status becomes `starting`, then `healthy` or `unhealthy`, visible in `docker ps`.

## Waiting for readiness

Combine the health check with `depends_on` conditions:

```
  web:
    depends_on:
      db:
        condition: service_healthy
```

Now Compose doesn't start `web` until `db` reports healthy. Other conditions are `service_started` (the default) and `service_completed_successfully`, for one-off jobs like a database migration that must finish first.

> **Tip:** still make your app retry its database connection. Health checks help at startup, but databases restart, networks blip, and a resilient app copes.

## Restart policies

`restart:` tells Docker what to do when a container exits:

- `no` (default): leave it stopped.
- `on-failure`: restart only after a non-zero exit code.
- `always`: always restart, including after a host reboot.
- `unless-stopped`: like always, but stays stopped if you stopped it yourself. The usual choice for self-hosted services.

## Environment and .env

Keep values out of the YAML:

- A `.env` file next to `compose.yaml` supplies variables for `${VAR}` substitution, with defaults like `${PORT:-8080}`.
- `env_file: app.env` passes a file of variables into a container's environment.
- `docker compose config` prints the final, fully resolved file: the fastest way to check what Compose will actually do.

## Profiles and overrides

- **profiles** let optional services (a debugging tool, an admin UI) start only when asked: `docker compose --profile tools up -d`.
- A `compose.override.yaml` is merged automatically, which is handy for local-only tweaks like extra ports or bind-mounted source code.

## In practice

For each service you run, ask three questions: how does Docker know it's healthy, what should happen if it crashes, and where does its configuration come from? A health check, `restart: unless-stopped` and a `.env` file answer all three.""",
    "key_points": [
        "A health check runs a command in the container to report starting, healthy or unhealthy.",
        "depends_on with condition: service_healthy waits for readiness, not just start.",
        "restart: unless-stopped is the usual policy for long-running services.",
        "Use .env and ${VAR} substitution for configuration; docker compose config shows the resolved file.",
    ],
    "figure_svg": HEALTH,
    "figure_caption": "web starts only once db's health check (pg_isready) passes.",
    "questions": [
        mcq("What does `condition: service_healthy` add to depends_on?", ["Nothing", "Waits until the dependency's health check passes before starting",
            "Restarts the dependency if unhealthy", "Shares a volume"], 1, "Without it, depends_on only waits for the container to start."),
        mcq("In the diagram, when does web start?", ["As soon as db starts", "When db becomes healthy", "Every 5 seconds", "Before db"], 1,
            "web waits for db's health check to pass.",
            HEALTH, "db goes from starting to healthy; an arrow labelled condition: service_healthy then starts web."),
        mcq("Which restart policy keeps a service running across reboots but respects a manual docker stop?", ["no", "on-failure", "always", "unless-stopped"], 3,
            "unless-stopped restarts automatically except when you stopped it on purpose."),
        mcq("Which command shows the compose file after variables and overrides are applied?", ["docker compose ps", "docker compose config", "docker compose logs", "docker compose top"], 1,
            "config prints the fully resolved configuration."),
        mcq("What does `${PORT:-8080}` mean in a compose file?", ["Use PORT, or 8080 if it isn't set", "Subtract 8080 from PORT", "Always 8080", "Fail if PORT is unset"], 0,
            "The :- form supplies a default."),
        mcq("A migration job must finish before the app starts. Which condition fits?", ["service_started", "service_healthy", "service_completed_successfully", "on-failure"], 2,
            "It waits for the job container to exit with code 0."),
        mcq("In the diagram, which command is the health check running?", ["curl", "pg_isready", "ping", "docker ps"], 1,
            "pg_isready tests whether Postgres accepts connections.",
            HEALTH, "Health check diagram: pg_isready every 5 seconds until it passes."),
        open_q("Why should an app still retry its database connection even with health-check-based depends_on?", "Because the condition only helps at startup; later the database can restart or the network can blip, and an app that retries reconnects instead of crashing.",
               ["depends_on only helps at startup", "database or network can fail later"], "Resilience belongs in the app too."),
        open_q("Write a health check for a web service that answers on http://localhost:8000/health.", "healthcheck: test: [\"CMD\", \"curl\", \"-fsS\", \"http://localhost:8000/health\"], with an interval like 10s, a timeout of 3s and a few retries (curl must exist in the image).",
               ["test runs curl or wget against /health", "fails on HTTP errors (-f)", "interval, timeout and retries"], "Make sure the tool you call exists in the image."),
        open_q("What's a compose profile useful for?", "For optional services that should only start when you ask, such as an admin UI or debugging tool, enabled with --profile name.",
               ["optional services", "started only when the profile is enabled"], "Keeps the default up lean."),
    ],
}

L5 = {
    "title": "Configuration and secrets",
    "minutes": 7,
    "photo_query": "",
    "body": """Most apps need passwords, API keys and certificates. Where you put them decides who can read them. The rule of thumb: **secrets never go into an image**, and preferably not into plain environment variables either.

## Why not in the image

Anything written in a Dockerfile (an `ENV DB_PASSWORD=...`, a copied `.env`, a key added and later deleted) lives in an image layer. Anyone who can pull the image can read it with `docker history` or by unpacking the layers. Push it to a public registry and it's public forever.

## Environment variables: convenient, imperfect

Passing secrets with `-e` or Compose `environment:` keeps them out of the image, and it's how most apps expect configuration. But environment variables:

- show up in `docker inspect` to anyone with Docker access,
- are inherited by every child process,
- often end up in crash reports and debug logs.

They're acceptable for a home server you control; avoid them for high-value secrets.

## Secret files

A better pattern is to mount the secret as a **file** that only the app reads. Compose supports this directly:

```
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
secrets:
  db_password:
    file: ./secrets/db_password.txt
```

The secret appears at `/run/secrets/db_password` inside the container. Many official images (Postgres, MySQL, and others) accept a `_FILE` variant of their password variables for exactly this.

## Build-time secrets

Sometimes the *build* needs a secret, such as a token for a private package registry. Never use `ARG` or `ENV` for that; both can leak into the image metadata. BuildKit has proper build secrets:

```
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci
```

built with `docker build --secret id=npmrc,src=$HOME/.npmrc .` The file is available during that step only and never saved in a layer.

## Keeping secrets out of git

- Add `.env` and `secrets/` to `.gitignore`.
- Commit a `.env.example` with placeholder values so the next person (or future you) knows what to set.
- Use different credentials for each service and environment, so one leak doesn't unlock everything.

> **If a secret leaks**, rotate it: change the password or revoke the key. Deleting the commit or image doesn't un-leak it.

## In practice

Audit one of your compose projects: search the Dockerfiles for `ENV` lines with passwords, check `.env` is in `.gitignore`, and move the most sensitive password to a secret file using the image's `_FILE` variable.""",
    "key_points": [
        "Secrets in a Dockerfile end up in image layers that anyone with the image can read.",
        "Environment variables keep secrets out of images but show in docker inspect and logs.",
        "Mount secrets as files (Compose secrets, *_FILE variables) for better protection.",
        "Use BuildKit --secret for build-time credentials; keep .env out of git; rotate anything that leaks.",
    ],
    "figure_svg": SECRETS,
    "figure_caption": "Secrets baked into images or committed files (A) leak; a .env file kept out of git or a secret file (B) keeps them out of the image.",
    "questions": [
        mcq("In the diagram, why is the top-left option (ENV in the Dockerfile) marked red?", ["ENV is slow", "It's stored in the image, readable by anyone who has the image",
            "Passwords can't be environment variables", "It only works on Linux"], 1, "Image metadata and layers are not secret.",
            SECRETS, "Four places for a password: in the Dockerfile, in compose.yaml in git (both red), a .env file not committed and a Docker secret file (both green)."),
        mcq("In the diagram, which options keep the password out of the image?", ["The two on the left (A)", "The two on the right (B)", "All four", "None"], 1,
            "A .env file kept out of git and a secret file are both supplied at run time.",
            SECRETS, "Four boxes: in the Dockerfile and in compose.yaml in git (red, A), a .env file not committed and a Docker secret file (green, B)."),
        mcq("What does POSTGRES_PASSWORD_FILE do?", ["Writes the password to a file", "Tells Postgres to read its password from that file path",
            "Encrypts the password", "Disables the password"], 1, "The _FILE convention lets the secret live in a mounted file instead of an env var."),
        mcq("Where does a Compose secret appear inside the container?", ["/etc/secrets", "/run/secrets/<name>", "In the environment", "In the image"], 1,
            "Compose mounts secrets under /run/secrets."),
        mcq("Which is the right way to give a build step a private registry token?", ["ARG TOKEN", "ENV TOKEN", "RUN --mount=type=secret", "COPY token.txt"], 2,
            "BuildKit secrets are available to that step only and never stored in a layer."),
        mcq("A password was committed to a public repo and you deleted the commit. What else must you do?", ["Nothing", "Rotate (change) the password", "Rename the repo", "Make the repo private"], 1,
            "Assume it was copied the moment it was public."),
        mcq("Which is a weakness of passing secrets as environment variables?", ["They're visible in docker inspect", "They make images bigger", "They can't contain symbols", "They need a restart to read"], 0,
            "Anyone with access to the Docker daemon can read them, and they leak into logs."),
        open_q("Explain why a secret added in one layer and deleted in the next is still exposed.", "Each layer is stored separately, so the earlier layer still contains the secret file even though a later layer hides it; anyone with the image can extract that layer.",
               ["layers are stored separately", "earlier layer still contains it"], "Images are append-only histories."),
        open_q("What should a .env.example contain, and why commit it?", "The names of every variable the app needs with placeholder or safe default values, so someone setting it up knows what to fill in, without exposing real secrets.",
               ["variable names with placeholders", "documents the setup without real secrets"], "It's documentation that can't leak anything."),
        open_q("Give one reason to use different credentials for each service.", "So that if one service's credentials leak, the attacker can't use them to get into the others; it limits the blast radius and lets you rotate one without touching the rest.",
               ["limits damage if one leaks", "rotate independently"], "Least privilege applies to passwords too."),
    ],
}

L6 = {
    "title": "Running containers well: logs, restarts and resources",
    "minutes": 8,
    "photo_query": "",
    "body": """Once your services run around the clock, the questions change: where do the logs go, what happens when something crashes or leaks memory, and how do you keep one container from starving the rest?

## Logging

Docker captures a container's **stdout and stderr**. That's why containerised apps should log to the console, not to files inside the container. `docker logs` and `docker compose logs` read them.

By default Docker uses the **json-file** driver, which keeps growing until the disk fills. Cap it:

```
services:
  web:
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

That keeps at most three 10 MB files per container. You can set the same defaults for every container in `/etc/docker/daemon.json`. The **local** driver is a good compact alternative, and drivers like **syslog**, **journald**, **fluentd** or **gelf** ship logs to a central system.

## Resource limits

A container can use all of the host's CPU and memory unless you say otherwise:

```
services:
  web:
    mem_limit: 512m
    cpus: 1.5
```

- **Memory** is a hard limit. If the container goes over, the kernel's **OOM killer** stops a process in it. `docker inspect` then shows `OOMKilled: true` and the exit code is usually **137** (killed by signal 9).
- **CPU** is a soft limit: the container is throttled, not killed, when it exceeds its share.

Set memory limits on anything that could leak or spike (databases with big caches, apps with unbounded queues), so one runaway service can't take down the host.

## Restarts and crash loops

With `restart: unless-stopped`, a crashing container restarts automatically, with an increasing delay between attempts. If `docker ps` shows `Restarting (1) 5 seconds ago` again and again, it's a **crash loop**: check `docker logs` for the error, and `docker inspect` for the exit code and whether it was OOM-killed.

## Keeping an eye on things

- `docker stats` shows live CPU, memory, network and disk I/O for each container.
- `docker system df` shows how much disk images, containers, volumes and build cache use.
- `docker events` streams what's happening (starts, stops, health changes, OOM kills).

For more than a handful of services, a monitoring stack (for example cAdvisor and Prometheus with Grafana dashboards) collects the same numbers over time and can alert you.

> **Tip:** exit code 137 means killed by SIGKILL, very often the memory limit. 143 means it was stopped with SIGTERM, which is normal for `docker stop`.

## In practice

Add log rotation defaults to `daemon.json`, set `mem_limit` on your databases and anything memory-hungry, and run `docker system df` monthly. If a service keeps restarting, check logs, then exit code, then OOM status, in that order.""",
    "key_points": [
        "Containers should log to stdout/stderr; cap json-file logs with max-size and max-file or the disk fills.",
        "Memory limits are hard (the OOM killer stops the process, exit code 137); CPU limits throttle.",
        "A container restarting over and over is a crash loop: read the logs, exit code and OOMKilled status.",
        "docker stats, system df and events show live resource use, disk use and what's happening.",
    ],
    "figure_svg": LIMITS,
    "figure_caption": "Memory climbs to the 512 MB limit; at X the kernel kills the process and Docker restarts the container.",
    "questions": [
        mcq("Where should a containerised app write its logs?", ["To /var/log inside the container", "To stdout and stderr", "To a volume only", "Nowhere"], 1,
            "Docker collects stdout/stderr, so docker logs and log drivers work."),
        mcq("What happens with the default json-file log driver if you don't set limits?", ["Logs are deleted daily", "The files keep growing and can fill the disk",
            "Logging stops at 1 GB", "Docker compresses them"], 1, "Set max-size and max-file."),
        mcq("In the graph, what happens at point X?", ["CPU is throttled", "The container hits its memory limit and is OOM-killed, then restarts",
            "The container is paused", "Swap is enabled"], 1, "Memory is a hard limit: reaching it gets the process killed.",
            LIMITS, "A memory line climbs to a dashed 512 MB limit at X, drops to near zero, then starts climbing again."),
        mcq("A container exits with code 137. What's the most likely cause?", ["A syntax error", "It was killed with SIGKILL, often by the memory limit", "A normal docker stop", "A port conflict"], 1,
            "137 = 128 + 9 (SIGKILL). Check OOMKilled in docker inspect."),
        mcq("What happens when a container exceeds its CPU limit?", ["It's killed", "It's throttled", "It's restarted", "Nothing, CPU limits don't exist"], 1,
            "CPU limits slow the container down rather than killing it."),
        mcq("Which command shows how much disk Docker's images, volumes and build cache use?", ["docker stats", "docker system df", "docker ps -s", "docker volume ls"], 1,
            "system df breaks usage down by type."),
        mcq("In the graph, which line is the memory limit?", ["The blue rising line", "The dashed red line at 512 MB", "The green line after X", "The dotted amber line"], 1,
            "The dashed red line marks the configured limit.",
            LIMITS, "Memory usage graph with a dashed red line labelled limit 512 MB."),
        open_q("A service shows 'Restarting' over and over. Describe how you'd diagnose it.", "Read docker logs for the error just before it exits, check the exit code and OOMKilled flag with docker inspect, and if it was OOM-killed raise or tune the memory limit; otherwise fix the configuration or app error the logs show.",
               ["read the logs", "check exit code and OOMKilled", "fix the cause shown"], "Logs, exit code, OOM: in that order."),
        open_q("Why set a memory limit on a database container on a shared home server?", "So that if it leaks or caches aggressively it can't use all the host's memory and cause other containers or the host to be killed or swap heavily; the damage stays inside that container.",
               ["prevents one container starving the host", "contains the damage"], "Limits turn a host outage into one service restarting."),
        open_q("Write the Compose logging settings that keep at most three 10 MB log files for a service.", "logging: driver: json-file, options: max-size: \"10m\", max-file: \"3\".",
               ["max-size 10m", "max-file 3"], "Or set the defaults once in daemon.json."),
    ],
}

PACK = {
    "id": "docker-intermediate",
    "version": 1,
    "topic": "Docker",
    "title": "Docker in practice",
    "summary": "Build small, fast, safe images and run multi-service apps properly: networks, health checks, secrets, logs and resource limits. For people who already use docker run and Compose.",
    "icon": "code",
    "level": "intermediate",
    "length": "short",
    "area": "technology",
    "tags": ["docker", "containers", "devops", "compose"],
    "sections": [
        {"title": "Better images", "summary": "Smaller, faster, safer builds and how containers connect.", "lessons": [
            {"title": L1["title"], "summary": "Use multi-stage builds and minimal bases to ship small images.", "lesson": L1},
            {"title": L2["title"], "summary": "Order Dockerfiles and contexts so rebuilds take seconds.", "lesson": L2},
            {"title": L3["title"], "summary": "Choose networks and publish ports without exposing more than you mean to.", "lesson": L3},
        ]},
        {"title": "Running services", "summary": "Keep multi-container apps healthy, configured and observable.", "lessons": [
            {"title": L4["title"], "summary": "Use health checks, dependency conditions and restart policies.", "lesson": L4},
            {"title": L5["title"], "summary": "Keep secrets out of images and git, and supply them safely.", "lesson": L5},
            {"title": L6["title"], "summary": "Control logs and resources and diagnose crash loops.", "lesson": L6},
        ]},
    ],
}
