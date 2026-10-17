"""Docker at expert level: internals, security and production."""

from app.coursepacks import mcq, open_q
from app.packs._draw import AMBER, BLUE, GREEN, INK, MUTED, PURPLE, RED, arrow, box, circle, line, svg, text, title

KERNEL = svg(
    title("What makes a container"),
    box(30, 55, 420, 40, "your process (PID 1 inside, PID 48213 on the host)", GREEN, size=13),
    box(30, 110, 200, 110, "", BLUE), text(130, 132, "namespaces: what it sees", 13, BLUE),
    text(130, 158, "pid · net · mnt · uts", 12, INK), text(130, 180, "ipc · user · cgroup", 12, INK), text(130, 206, "A", 15, BLUE, weight="bold"),
    box(250, 110, 200, 110, "", AMBER), text(350, 132, "cgroups: what it gets", 13, AMBER),
    text(350, 158, "memory · cpu · pids", 12, INK), text(350, 180, "io", 12, INK), text(350, 206, "B", 15, AMBER, weight="bold"),
    box(30, 235, 420, 36, "+ capabilities, seccomp, LSM (AppArmor/SELinux), overlay filesystem", PURPLE, size=12),
)

OVERLAY = svg(
    title("overlayfs: how the container sees one filesystem"),
    box(60, 50, 360, 40, "merged (what the container sees)", GREEN, size=13),
    box(60, 110, 360, 36, "upperdir: container's writes", AMBER, size=13),
    box(60, 156, 360, 30, "lowerdir 3: app layer", BLUE, size=12),
    box(60, 192, 360, 30, "lowerdir 2: dependencies", BLUE, size=12),
    box(60, 228, 360, 30, "lowerdir 1: base image", BLUE, size=12),
    arrow(440, 120, 440, 95, AMBER), text(455, 140, "copy-", 11, AMBER, anchor="start"), text(455, 154, "up", 11, AMBER, anchor="start"),
)

ATTACK = svg(
    title("Hardening layers"),
    circle(240, 160, 120, RED), circle(240, 160, 92, AMBER), circle(240, 160, 64, BLUE), circle(240, 160, 36, GREEN, label="app", size=12),
    text(240, 52, "rootless / user namespaces", 12, RED), text(240, 80, "drop capabilities, no-new-privileges", 12, AMBER),
    text(240, 108, "read-only root fs, non-root user", 12, BLUE),
    text(240, 300 - 12, "each ring limits what a compromise can do", 12, MUTED),
)

MULTIARCH = svg(
    title("One tag, many architectures"),
    box(170, 55, 140, 50, "myapp:2.0", INK, sub="manifest list"),
    arrow(200, 105, 90, 160, BLUE), arrow(240, 105, 240, 160, GREEN), arrow(280, 105, 390, 160, AMBER),
    box(30, 162, 120, 50, "linux/amd64", BLUE, sub="sha256:1a…", size=13),
    box(180, 162, 120, 50, "linux/arm64", GREEN, sub="sha256:7c…", size=13),
    box(330, 162, 120, 50, "linux/arm/v7", AMBER, sub="sha256:e2…", size=13),
    text(240, 250, "A Raspberry Pi pulls the arm64 image; a PC pulls amd64", 12, MUTED),
)

ORCH = svg(
    title("Desired state vs actual state"),
    box(30, 60, 160, 90, "", BLUE), text(110, 84, "Desired", 14, BLUE, weight="bold"), text(110, 110, "web: 3 replicas", 12, INK), text(110, 132, "image: web:2.4", 12, INK),
    box(290, 60, 160, 90, "", AMBER), text(370, 84, "Actual", 14, AMBER, weight="bold"), text(370, 110, "web: 2 running", 12, INK), text(370, 132, "node-3 died", 12, RED),
    arrow(190, 105, 288, 105, MUTED, "compare", dy=-10),
    box(140, 190, 200, 60, "Controller", GREEN, sub="starts 1 replica on node-1"),
    arrow(370, 150, 300, 188, AMBER), arrow(180, 188, 110, 152, GREEN),
)

USE = svg(
    title("USE for a slow container"),
    box(30, 60, 130, 170, "", BLUE), text(95, 84, "Utilisation", 13, BLUE, weight="bold"), text(95, 116, "CPU 100%?", 12, INK), text(95, 140, "memory near", 12, INK), text(95, 158, "limit?", 12, INK),
    box(175, 60, 130, 170, "", AMBER), text(240, 84, "Saturation", 13, AMBER, weight="bold"), text(240, 116, "CPU throttled?", 12, INK), text(240, 140, "I/O queue?", 12, INK), text(240, 164, "swap?", 12, INK),
    box(320, 60, 130, 170, "", RED), text(385, 84, "Errors", 13, RED, weight="bold"), text(385, 116, "OOM kills?", 12, INK), text(385, 140, "restarts?", 12, INK), text(385, 164, "5xx in logs?", 12, INK),
    text(240, 262, "check every resource for all three", 12, MUTED),
)

L1 = {
    "title": "Under the hood: namespaces and cgroups",
    "minutes": 9,
    "photo_query": "",
    "body": """There's no "container" object in the Linux kernel. A container is an ordinary process wrapped in several kernel features. Knowing them explains Docker's behaviour, its limits and most of its security story.

## Namespaces: what a process can see

A **namespace** gives a process its own view of one kind of system resource:

- **pid**: its own process tree, where it's PID 1. On the host it has a normal PID.
- **net**: its own interfaces, IPs, routing table and ports.
- **mnt**: its own mount table, so it sees the image's filesystem as `/`.
- **uts**: its own hostname.
- **ipc**: its own shared memory and message queues.
- **user**: its own user and group IDs, so root inside can map to an unprivileged user outside.
- **cgroup**: its own view of the cgroup hierarchy.

You can see this from the host: `docker inspect -f '{{.State.Pid}}' web` gives the host PID, and `ls -l /proc/<pid>/ns` lists its namespaces. `nsenter -t <pid> -n ip addr` runs a host tool inside the container's network namespace, which is very useful for debugging distroless images.

## cgroups: what a process can use

**Control groups (cgroups)** limit and account for resources: memory, CPU time, number of processes (`pids`), and block I/O. `--memory`, `--cpus` and `--pids-limit` are written into the container's cgroup. Modern distributions use **cgroup v2**, a single unified hierarchy; `docker info` shows which you have.

The memory limit is where the **OOM killer** acts: when a cgroup is out of memory, the kernel kills a process *in that cgroup*, not a random one on the host.

## The other ingredients

- **Capabilities** split root's powers into pieces (`CAP_NET_ADMIN`, `CAP_SYS_ADMIN`...). Docker drops most of them by default.
- **seccomp** filters which system calls a process may make; Docker's default profile blocks around 40 dangerous ones.
- **AppArmor/SELinux** (Linux Security Modules) add mandatory access control.
- **overlayfs** assembles the image layers into one filesystem.

## Who does what

`docker` CLI → **dockerd** (the API and image management) → **containerd** (container lifecycle) → **runc** (the low-level runtime that actually calls the kernel to create namespaces and cgroups, then runs your process). runc follows the **OCI runtime spec**, which is why other runtimes (crun, gVisor's runsc, Kata) can slot in.

> **Common misconception:** containers are a security boundary as strong as VMs. They share the kernel, so a kernel exploit can escape. For hostile workloads, use gVisor, Kata Containers or real VMs.

## PID 1 matters

Inside the container your app is PID 1, which the kernel treats specially: it gets **no default signal handlers**, so a SIGTERM may be ignored, and it must **reap zombie** child processes. If your app wasn't written to be an init, run it with `--init` (Docker adds the tiny `tini`) so signals and zombies are handled.

## In practice

Start a container, find its host PID, and compare `ps` inside and outside, `/proc/<pid>/ns`, and `cat /sys/fs/cgroup/...` for its memory limit. Seeing the plumbing once makes every later debugging session easier.""",
    "key_points": [
        "Namespaces (pid, net, mnt, uts, ipc, user, cgroup) control what a container can see.",
        "cgroups control and account for what it can use: memory, CPU, pids, I/O; OOM kills stay inside the cgroup.",
        "Capabilities, seccomp and AppArmor/SELinux restrict what root inside can do; runc creates it all via the OCI spec.",
        "PID 1 gets no default signal handlers and must reap zombies; use --init if the app isn't built for it.",
    ],
    "figure_svg": KERNEL,
    "figure_caption": "A container is a process plus namespaces (A, what it sees), cgroups (B, what it gets) and further restrictions.",
    "questions": [
        mcq("Which kernel feature gives a container its own process tree, where it's PID 1?", ["cgroups", "The pid namespace", "seccomp", "overlayfs"], 1,
            "The pid namespace isolates process IDs."),
        mcq("In the diagram, which group would enforce a 512 MB memory limit?", ["A, namespaces", "B, cgroups", "The overlay filesystem", "seccomp"], 1,
            "cgroups limit resources; namespaces only change what the process can see.",
            KERNEL, "A container process with two boxes beneath: namespaces A (pid, net, mnt, uts, ipc, user, cgroup) and cgroups B (memory, cpu, pids, io)."),
        mcq("Which component actually creates the namespaces and cgroups and starts the process?", ["The docker CLI", "dockerd", "runc", "The registry"], 2,
            "runc is the OCI runtime that talks to the kernel; containerd drives it."),
        mcq("What does seccomp do?", ["Encrypts container traffic", "Filters which system calls a process may make", "Limits memory", "Signs images"], 1,
            "Docker's default seccomp profile blocks dangerous syscalls."),
        mcq("Why might `docker stop` take 10 seconds and then kill an app?", ["The network is slow", "The app is PID 1 with no SIGTERM handler, so it ignores the signal until SIGKILL",
            "Docker always waits 10 seconds", "The image is too large"], 1, "PID 1 has no default handlers; handle SIGTERM or use --init."),
        mcq("How can you run the host's `ip` tool inside a container's network namespace?", ["docker exec ip", "nsenter -t <pid> -n ip addr", "docker network inspect", "chroot"], 1,
            "nsenter joins the namespaces of a target PID, great for images with no tools."),
        mcq("In the diagram, which group includes the user namespace that can map root inside to an unprivileged user outside?", ["A", "B", "Neither", "Both"], 0,
            "user is one of the namespaces (A).",
            KERNEL, "Namespaces A and cgroups B under a container process."),
        open_q("Explain why containers are a weaker isolation boundary than virtual machines.", "All containers share the host kernel, so a kernel vulnerability or misconfiguration can let a process escape to the host; a VM runs its own kernel behind a hypervisor, a much smaller shared surface.",
               ["containers share the host kernel", "a kernel exploit can escape", "VMs have their own kernel"], "Use gVisor, Kata or VMs for untrusted code."),
        open_q("What problems does running with --init solve?", "It runs a tiny init (tini) as PID 1 that forwards signals like SIGTERM to the app so it shuts down cleanly, and reaps zombie child processes.",
               ["forwards signals", "reaps zombie processes"], "Especially useful for shell scripts and apps that spawn children."),
        open_q("A container was OOM-killed. Does that mean the host ran out of memory? Explain.", "Not necessarily: the container hit its own cgroup memory limit, and the kernel killed a process inside that cgroup; the host may still have plenty of free memory.",
               ["it hit the cgroup limit", "kill happens inside the cgroup", "host may have memory free"], "Check OOMKilled and the configured limit."),
    ],
}

L2 = {
    "title": "Images in depth: OCI, overlayfs and BuildKit",
    "minutes": 9,
    "photo_query": "",
    "body": """An image is a precise, standard format, and knowing it makes you better at building, storing and trusting images.

## The OCI image format

The **Open Container Initiative (OCI)** standardises images so any compliant tool (Docker, Podman, containerd, Kubernetes) can use them. An image is made of:

- a **manifest** listing the layers and the config, each by **digest** (sha256 of its content);
- a **config** JSON with the entrypoint, environment, working directory, user and the history;
- the **layers**, compressed tar archives of filesystem changes. A deleted file is recorded as a "whiteout" marker, which is why deleting doesn't shrink earlier layers.

Because everything is addressed by content hash, a digest like `myapp@sha256:…` pins an exact, verifiable image.

## overlayfs and copy-on-write

On the host, the **overlay2** storage driver stacks the layers as **lowerdirs** (read-only) with the container's **upperdir** (writable) on top, presenting a **merged** view. When the container modifies a file from a lower layer, overlayfs first **copies it up** into the upperdir: the first write to a big file (a database file shipped in the image, say) copies the whole file. That's one reason data that changes belongs in volumes, which bypass overlayfs entirely.

## BuildKit

Modern Docker builds use **BuildKit**, which brings:

- **Parallel stages**: independent stages of a multi-stage build run at the same time.
- **Smarter caching**, including exporting and importing cache from a registry (`--cache-to`/`--cache-from`) so CI builds reuse previous results.
- **Mounts** for build steps: cache mounts for package managers, secret mounts for credentials, SSH mounts for private git.
- **docker buildx**, the front end for advanced builds, including multi-architecture images.

## Reproducibility

A reproducible build gives the same image from the same inputs. Help it along by:

- pinning base images by digest (`FROM python:3.13-slim@sha256:…`), not just tags;
- pinning dependency versions with lock files;
- avoiding timestamps and random data baked into layers.

## Labels and metadata

Add **OCI labels** (`org.opencontainers.image.source`, `.version`, `.revision`) so anyone can trace an image back to the commit that built it. Registries and scanners display them.

> **Tip:** `docker buildx imagetools inspect myapp:2.0` shows the manifest (and every platform for multi-arch images) without pulling the image.

## In practice

Run `docker save myapp:1.0 -o myapp.tar`, untar it and look inside: `index.json`, the manifest, the config and the layer tarballs. Then build with BuildKit's plain progress (`--progress=plain`) and watch which stages run in parallel.""",
    "key_points": [
        "OCI images are a manifest, a config and content-addressed layers; digests pin exact content.",
        "overlay2 stacks read-only lowerdirs with a writable upperdir; modifying a lower file copies it up first.",
        "BuildKit adds parallel stages, registry cache export/import, and cache/secret/SSH mounts.",
        "Pin bases by digest, lock dependencies and add OCI labels for reproducible, traceable images.",
    ],
    "figure_svg": OVERLAY,
    "figure_caption": "overlayfs merges read-only image layers (lowerdirs) with the container's writable upperdir; changed files are copied up.",
    "questions": [
        mcq("What does an OCI image manifest contain?", ["The app's source code", "References to the config and layers by digest", "The container's logs", "Registry passwords"], 1,
            "The manifest lists content-addressed blobs: config and layers."),
        mcq("In the diagram, where do a container's writes go?", ["lowerdir 1", "lowerdir 3", "upperdir", "Directly into the image"], 2,
            "The writable upperdir holds the container's changes; lowerdirs are read-only image layers.",
            OVERLAY, "A stack: merged view at the top, then upperdir (container writes), then three lowerdirs (app, dependencies, base); an arrow marked copy-up points from the upperdir upward."),
        mcq("A container modifies one byte of a 2 GB file that came from the image. What happens with overlay2?", ["Only the byte is written", "The whole file is copied up into the upperdir first",
            "The write fails", "The image is rebuilt"], 1, "Copy-on-write works at file granularity; that's why changing data belongs in volumes."),
        mcq("Why does `FROM python:3.13-slim@sha256:…` make builds more reproducible?", ["It downloads faster", "The digest always refers to exactly the same image content",
            "It uses less disk", "It enables BuildKit"], 1, "Tags move; digests don't."),
        mcq("Which BuildKit feature lets a CI runner reuse layers from previous builds on other machines?", ["--squash", "--cache-to/--cache-from a registry", "--no-cache", "--target"], 1,
            "Exporting the build cache to a registry and importing it later makes cold CI builds warm."),
        mcq("How is a deleted file represented in a layer?", ["The earlier layer is edited", "A whiteout marker in the new layer", "It isn't; deletes are ignored", "By a new manifest"], 1,
            "Whiteouts hide the file in the merged view; the bytes remain in the earlier layer."),
        mcq("In the diagram, which layers are shared by every container started from this image?", ["Only the upperdir", "The lowerdirs", "The merged view", "None"], 1,
            "Lowerdirs are the read-only image layers; each container gets its own upperdir.",
            OVERLAY, "overlayfs stack with three lowerdirs under a container upperdir."),
        open_q("Explain why databases should keep their data files in volumes rather than the container filesystem.", "Volumes bypass overlayfs, so writes go straight to the host filesystem without copy-up overhead, and the data survives the container being removed or upgraded.",
               ["avoids overlayfs copy-up overhead", "data survives container removal"], "Performance and durability together."),
        open_q("Name three kinds of BuildKit mount and what each is for.", "Cache mounts keep package-manager downloads between builds, secret mounts expose credentials to one build step without storing them, and SSH mounts let a step use your SSH agent, for example to clone a private repo.",
               ["cache mounts for package caches", "secret mounts for credentials", "SSH mounts for private repos"], "All three avoid baking anything into a layer."),
        open_q("How do OCI labels help with images you run in production?", "Labels such as org.opencontainers.image.source and revision record where and from which commit the image was built, so you can trace a running image back to its code and version.",
               ["record source, version and commit", "trace an image back to its code"], "Scanners and registries show them too."),
    ],
}

L3 = {
    "title": "Hardening containers",
    "minutes": 9,
    "photo_query": "",
    "body": """Docker's defaults are reasonable, but most containers run with far more privilege than they need. Hardening means removing privileges in layers, so a compromised app can do as little as possible.

## Don't run as root

By default the process inside runs as **root (UID 0)**. Without user namespaces, that's the same UID as root on the host; a container escape then lands as root. Add a user in the Dockerfile and switch to it:

```
RUN useradd --uid 10001 --no-create-home app
USER 10001
```

Use a numeric UID so tools (and Kubernetes' `runAsNonRoot`) can verify it.

## Drop capabilities and privilege escalation

Even Docker's trimmed root keeps about 14 capabilities. Most apps need none:

```
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE --security-opt no-new-privileges myapp
```

`no-new-privileges` stops setuid binaries from gaining privileges. And **never** use `--privileged` unless you know exactly why: it gives the container nearly full access to the host, including all devices.

## Read-only root filesystem

`--read-only` makes the container's filesystem read-only. Add `--tmpfs /tmp` (and volumes for real data) where the app must write. An attacker can't drop tools or modify the app.

## Rootless mode and user namespaces

- **userns-remap** maps root inside containers to an unprivileged range of UIDs on the host.
- **Rootless Docker** runs the whole daemon as a normal user. An escape gets that user's rights, not root's. Some features (low ports, certain networking) need extra setup.

## The Docker socket is root

Mounting `/var/run/docker.sock` into a container (common for dashboards and reverse proxies like Traefik) gives that container **full control of Docker, which means root on the host**. Prefer a read-only socket proxy that only allows the API calls the tool needs.

## Supply chain

Hardening runtime is wasted if the image itself is compromised:

- Use trusted, minimal bases and rebuild regularly to pick up patches.
- **Scan** images for known vulnerabilities (Trivy, Grype, Docker Scout) in CI.
- Generate an **SBOM** (software bill of materials) so you know what's inside.
- **Sign** images (cosign, Docker Content Trust) and verify signatures before deploying.

> **Rule of thumb:** each layer (non-root user, dropped capabilities, read-only filesystem, seccomp/AppArmor, rootless) is imperfect alone. Together they turn a breach into a dead end.

## In practice

Take a service you run and try: a non-root USER, `--cap-drop ALL`, `--read-only` with a tmpfs, and `no-new-privileges`. Add back only what breaks, one thing at a time, and note why it's needed. In Compose these are `user`, `cap_drop`, `cap_add`, `read_only`, `tmpfs` and `security_opt`.""",
    "key_points": [
        "Run as a non-root numeric UID; root in a container is root on the host without user namespaces.",
        "Drop all capabilities and add back only what's needed; use no-new-privileges; avoid --privileged.",
        "A read-only root filesystem plus tmpfs/volumes for writes stops tampering.",
        "The Docker socket grants host root; scan, SBOM and sign images to protect the supply chain.",
    ],
    "figure_svg": ATTACK,
    "figure_caption": "Hardening in rings: each layer limits what a compromised app can do.",
    "questions": [
        mcq("Why is running as root in a container risky?", ["Root is slower", "Without user namespaces, root inside is UID 0 on the host if the container is escaped",
            "Root can't write files", "Images won't build"], 1, "An escape inherits the process's UID."),
        mcq("What does mounting /var/run/docker.sock into a container effectively give it?", ["Read-only metrics", "Full control of Docker, equivalent to root on the host",
            "Network access", "Nothing important"], 1, "It can start a privileged container with the host's / mounted."),
        mcq("Which flag gives a container nearly full access to the host's devices and kernel features?", ["--cap-drop ALL", "--read-only", "--privileged", "--init"], 2,
            "--privileged removes most isolation. Avoid it."),
        mcq("In the diagram, which ring covers dropping capabilities?", ["The outer red ring", "The amber ring", "The blue ring", "The green centre"], 1,
            "The amber ring is capabilities and no-new-privileges.",
            ATTACK, "Concentric rings around the app: green app, blue read-only root fs and non-root user, amber dropped capabilities and no-new-privileges, red rootless/user namespaces."),
        mcq("What does no-new-privileges prevent?", ["Network access", "Gaining privileges through setuid binaries", "Writing to /tmp", "Pulling images"], 1,
            "It blocks privilege escalation via setuid/setgid."),
        mcq("Which tool scans images for known vulnerabilities?", ["cosign", "Trivy", "tini", "runc"], 1,
            "Trivy (or Grype, Docker Scout) scans; cosign signs."),
        mcq("In the diagram, which ring is the outermost defence, limiting damage even after a full container escape?", ["Read-only root fs", "Dropped capabilities", "Rootless Docker / user namespaces", "The app itself"], 2,
            "With rootless or userns-remap, an escape lands as an unprivileged host user.",
            ATTACK, "Hardening rings with rootless/user namespaces outermost."),
        open_q("A Traefik container needs the Docker socket to discover services. How would you reduce the risk?", "Put a socket proxy in front of the Docker socket that only allows the read-only API calls Traefik needs, mount that instead of the real socket, and keep Traefik itself non-root and capability-dropped.",
               ["use a filtering socket proxy", "allow only read-only calls needed"], "Least privilege for the API, not just the process."),
        open_q("Describe a step-by-step approach to hardening an existing service without breaking it.", "Apply restrictions one at a time: switch to a non-root user, drop all capabilities, make the filesystem read-only with tmpfs or volumes for writable paths, add no-new-privileges, test after each change and add back only what's genuinely needed, documenting why.",
               ["one change at a time and test", "non-root, cap-drop, read-only, no-new-privileges", "add back only what's needed"], "Iterate rather than guessing."),
        open_q("What is an SBOM, and why is it useful?", "A software bill of materials lists every package and version inside an image, so when a new vulnerability is announced you can quickly find which images contain the affected component.",
               ["list of packages and versions in the image", "find affected images when a vulnerability appears"], "Generate one in CI alongside scanning."),
    ],
}

L4 = {
    "title": "Multi-architecture images and registries",
    "minutes": 8,
    "photo_query": "",
    "body": """Your laptop may be ARM (Apple silicon), your server x86-64 and your home lab a Raspberry Pi. Images are built for a specific **platform**, so production work means building for all of them and managing where images live.

## Platforms and manifest lists

A platform is `os/architecture[/variant]`: `linux/amd64`, `linux/arm64`, `linux/arm/v7`. One tag can point to a **manifest list** (an OCI image index) holding a separate image per platform. When you pull, Docker picks the one matching your machine. That's how `nginx:1.27` "just works" on a Pi and a PC.

Running the wrong architecture fails with `exec format error`, or runs very slowly under emulation.

## Building for several platforms

With **buildx**:

```
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/brad/myapp:2.0 --push .
```

Two ways it builds the foreign architecture:

- **QEMU emulation**: simple, works everywhere, but compiling under emulation can be 5–20× slower.
- **Cross-compilation**: the build stage runs natively (`FROM --platform=$BUILDPLATFORM`) and compiles for `$TARGETPLATFORM`. Go, Rust and .NET do this well and it's fast.
- Or native builders: a buildx builder with real ARM and x86 nodes.

## Registries

Beyond Docker Hub there are **GitHub Container Registry** (ghcr.io), cloud registries, and self-hosted ones (the `registry:2` image, Harbor, Gitea's built-in registry). Considerations:

- **Rate limits**: Docker Hub limits anonymous pulls, which can break CI and big deployments; authenticate or use a **pull-through cache** mirror.
- **Retention**: clean up old tags so storage doesn't grow forever.
- **Access**: separate read-only pull credentials for servers from push credentials for CI.

## Tagging strategy

Good images carry several tags:

- an **immutable** version tag per release, like `2.0.3`, never re-pushed;
- floating tags `2.0` and `2` that follow the newest patch and minor;
- the **git commit SHA** for exact traceability.

Deploy by version tag or digest, never `latest`. For extra certainty, deploy by digest: `myapp@sha256:…`.

> **Tip:** `docker buildx imagetools inspect nginx:1.27` lists every platform in a manifest list and its digest.

## In practice

Add a `--platform linux/amd64,linux/arm64` build to your CI for one project, push to ghcr.io, and pull it on two different machines. Check `docker image inspect --format '{{.Architecture}}'` on each to confirm each got its native image.""",
    "key_points": [
        "Images are per platform (os/arch); a manifest list lets one tag serve many architectures.",
        "buildx builds multi-platform images by QEMU emulation, cross-compilation or native nodes.",
        "Mind registry rate limits, retention and separate pull/push credentials.",
        "Use immutable version tags plus commit SHAs, and deploy by version or digest rather than latest.",
    ],
    "figure_svg": MULTIARCH,
    "figure_caption": "One tag points to a manifest list; each machine pulls the image built for its architecture.",
    "questions": [
        mcq("What error typically appears when running an image built for the wrong architecture?", ["permission denied", "exec format error", "no space left", "connection refused"], 1,
            "The binary can't run on that CPU."),
        mcq("In the diagram, which image does a 64-bit Raspberry Pi pull?", ["linux/amd64", "linux/arm64", "linux/arm/v7", "All three"], 1,
            "A 64-bit Pi runs arm64 and gets that entry from the manifest list.",
            MULTIARCH, "A tag myapp:2.0 points to a manifest list with three images: linux/amd64, linux/arm64 and linux/arm/v7, each with its own digest."),
        mcq("Why is cross-compilation usually faster than QEMU emulation for multi-arch builds?", ["It skips tests", "The compiler runs natively and only targets the other architecture",
            "It uses less disk", "It doesn't need buildx"], 1, "Emulating every instruction of a compiler is slow."),
        mcq("Which tag should be immutable?", ["latest", "2", "2.0", "2.0.3"], 3,
            "Patch-level release tags should never be re-pushed; 2 and 2.0 float."),
        mcq("What problem does a pull-through cache registry solve?", ["Image signing", "Docker Hub rate limits and repeated downloads", "Multi-arch builds", "Secrets"], 1,
            "It caches upstream images locally."),
        mcq("Which Dockerfile line lets a build stage run natively while targeting another platform?", ["FROM --platform=$BUILDPLATFORM golang:1.23 AS build", "ARG ARCH=arm64",
            "RUN qemu", "FROM scratch"], 0, "BUILDPLATFORM is the builder's native platform."),
        mcq("In the diagram, what do the three images share?", ["The same digest", "The same tag via the manifest list", "The same layers", "The same architecture"], 1,
            "Each has its own digest and layers; the tag points to the list.",
            MULTIARCH, "Manifest list diagram with three per-platform images."),
        open_q("Describe a sensible tagging scheme for a release of version 2.0.3 built from commit a1b2c3d.", "Push an immutable 2.0.3 tag, move the floating 2.0 and 2 tags to it, and add a tag with the commit SHA a1b2c3d for traceability; deploy using 2.0.3 or the digest.",
               ["immutable 2.0.3", "floating 2.0 and 2", "commit SHA tag"], "Avoid deploying latest."),
        open_q("Why separate pull credentials for servers from push credentials for CI?", "So that a compromised server can only read images and can't push a malicious image that other servers would then deploy; only CI can publish.",
               ["servers only read", "a compromised server can't publish images"], "Least privilege again."),
        open_q("Explain how a single tag like nginx:1.27 can work on both a PC and a Raspberry Pi.", "The tag points to a manifest list containing an image for each platform; when you pull, Docker selects the image that matches your machine's OS and architecture.",
               ["tag points to a manifest list", "Docker picks the matching platform"], "Check with buildx imagetools inspect."),
    ],
}

L5 = {
    "title": "Orchestration: Swarm, Kubernetes and desired state",
    "minutes": 9,
    "photo_query": "",
    "body": """Compose runs containers on one machine. When you need several machines, automatic recovery and rolling upgrades, you need an **orchestrator**. The big idea behind all of them is **desired state**.

## Desired state and reconciliation

Instead of telling the system *what to do* ("start a container"), you declare *what should be true* ("3 replicas of web:2.4 should be running"). **Controllers** constantly compare desired state with actual state and act to close the gap: a node dies, two replicas remain, so a controller schedules a third elsewhere. This **reconciliation loop** is what makes orchestrated systems self-healing.

## Docker Swarm

Swarm is built into Docker. `docker swarm init` makes a manager; other machines `join`. You deploy a Compose-style file as a **stack**: `docker stack deploy -c compose.yaml app`.

- **Services** with a replica count, spread over nodes.
- An **overlay network** connecting containers across machines, with built-in service discovery and load balancing (the routing mesh).
- **Rolling updates** and rollbacks; secrets and configs distributed securely.
- Managers use the **Raft** consensus algorithm, so run **3 or 5** managers: a majority must agree, so 3 tolerates one failure.

Swarm is simple and a natural step up from Compose for small clusters.

## Kubernetes

Kubernetes is the industry standard, more powerful and more complex. Its core objects:

- **Pod**: one or more containers scheduled together, sharing a network namespace.
- **Deployment**: desired replicas of a pod template, with rolling updates.
- **Service**: a stable name and virtual IP load-balancing to matching pods.
- **Ingress/Gateway**: HTTP routing from outside.
- **ConfigMap/Secret**, **PersistentVolumeClaim** for config and storage.
- **Probes**: liveness (restart if failing), readiness (only send traffic when ready) and startup.

Kubernetes doesn't use Docker as its runtime any more; it uses **containerd** or CRI-O directly. Your Docker-built OCI images run unchanged.

For a home lab, lightweight distributions like **k3s** or **MicroK8s** give real Kubernetes on small machines.

## Do you need one?

Orchestration adds real complexity. A single well-run host with Compose, backups and monitoring is often right for personal and small-business workloads. Reach for Swarm or Kubernetes when you genuinely need multiple machines, zero-downtime upgrades or automatic failover.

> **Common misconception:** an orchestrator makes your *app* highly available. It restarts and reschedules containers; your app still has to cope with restarts, and stateful services (databases) need replication of their own.

## In practice

Convert a Compose project into a Swarm stack on three small VMs, or a k3s deployment with a Deployment and Service. Then kill a node and watch the controller restore the desired replica count.""",
    "key_points": [
        "Orchestrators reconcile declared desired state with actual state, which makes them self-healing.",
        "Swarm is built into Docker: stacks, services, overlay networks, rolling updates; run 3 or 5 managers for Raft.",
        "Kubernetes core: pods, deployments, services, ingress, config/secrets, volumes and probes; it runs OCI images via containerd.",
        "Orchestration restarts containers but doesn't make stateful apps highly available by itself.",
    ],
    "figure_svg": ORCH,
    "figure_caption": "A controller compares desired state (3 replicas) with actual state (2 running) and starts one more.",
    "questions": [
        mcq("What does a controller in an orchestrator do?", ["Builds images", "Compares desired and actual state and acts to close the gap", "Stores logs", "Signs containers"], 1,
            "That reconciliation loop is the core of Swarm and Kubernetes."),
        mcq("In the diagram, why does the controller start another replica?", ["The image changed", "Actual state (2 running) is below desired state (3)", "A user ran docker run", "The network failed"], 1,
            "Node-3 died, leaving 2 of 3 replicas, so the controller schedules one more.",
            ORCH, "Desired: web 3 replicas, image web:2.4. Actual: web 2 running, node-3 died. A controller starts 1 replica on node-1."),
        mcq("Why run 3 Swarm managers rather than 2?", ["2 is not allowed", "Raft needs a majority; 3 tolerates one failure, 2 tolerates none",
            "More managers are faster", "Managers run workloads"], 1, "With 2, losing one leaves no majority."),
        mcq("In Kubernetes, which object gives pods a stable name and load-balances to them?", ["Deployment", "Service", "ConfigMap", "PersistentVolumeClaim"], 1,
            "Pods come and go; a Service is the stable front."),
        mcq("What does a readiness probe control?", ["Whether the container is restarted", "Whether traffic is sent to the pod", "How many replicas run", "Image pulls"], 1,
            "Failing readiness removes the pod from the Service; failing liveness restarts it."),
        mcq("Which runtime does modern Kubernetes typically use?", ["Docker Engine", "containerd or CRI-O", "QEMU", "Swarm"], 1,
            "dockershim was removed; OCI images still run unchanged."),
        mcq("In the diagram, which box represents what you declare?", ["Actual", "Desired", "Controller", "node-3"], 1,
            "You declare desired state; the system observes actual state.",
            ORCH, "Desired and Actual boxes with a controller reconciling them."),
        open_q("Explain declarative 'desired state' with an example.", "You state the end result, such as 'three replicas of web:2.4 should run', rather than issuing commands; the orchestrator continuously works to make reality match, for example starting a replacement when a container or node dies.",
               ["declare the end result, not steps", "system continuously makes reality match"], "That's why it self-heals."),
        open_q("When would you choose a single host with Compose over Kubernetes?", "When the workload is small or personal, fits on one machine and brief downtime for upgrades is acceptable, because Compose is far simpler to run, back up and debug than a cluster.",
               ["small workload on one machine", "downtime acceptable", "much simpler to operate"], "Complexity is a real cost."),
        open_q("Why doesn't running a database in an orchestrator automatically make it highly available?", "The orchestrator can restart or reschedule the database container, but the data lives in one place; true high availability needs the database's own replication and failover, plus storage that follows it.",
               ["orchestrator only restarts or reschedules", "needs database replication and failover"], "State is the hard part."),
    ],
}

L6 = {
    "title": "Production debugging and observability",
    "minutes": 9,
    "photo_query": "",
    "body": """When something is wrong in production, you need a method, not guesswork. This lesson pulls the earlier ones together into a debugging toolkit for containers.

## Start with a method

The **USE method** (Brendan Gregg): for every resource (CPU, memory, disk I/O, network) check **Utilisation** (how busy), **Saturation** (how much work is queued or throttled) and **Errors**. For request-serving apps, add **RED**: Rate, Errors and Duration of requests.

## Container-specific signals

- **CPU throttling**: a container with `--cpus` can look idle on average but stall in bursts. Check `nr_throttled` and `throttled_usec` in the cgroup's `cpu.stat`.
- **Memory**: `memory.current` against `memory.max` in the cgroup; a near-limit container may be reclaiming page cache constantly before an OOM kill.
- **OOM kills**: `docker inspect` shows `OOMKilled`, and `dmesg` or `journalctl -k` records the kill.
- **Exit codes**: 137 is SIGKILL (often OOM), 143 is SIGTERM, 139 is a segfault, 1 is usually an app error.
- **Restart counts** and **health status** in `docker ps` and `docker inspect`.

## Getting inside minimal images

Distroless and scratch images have no shell. Options:

- `docker debug` (Docker Desktop and newer Docker) attaches a toolbox to any container.
- Run a debug container that **shares the target's namespaces**: `docker run -it --rm --pid container:web --network container:web nicolaka/netshoot`. You see its processes and network with a full set of tools.
- `nsenter` from the host, as in the internals lesson.

## Observability in three signals

- **Metrics**: cAdvisor (or the Docker daemon's metrics endpoint) exports per-container CPU, memory, network and I/O to **Prometheus**; **Grafana** graphs and alerts on them.
- **Logs**: ship stdout/stderr to Loki, Elasticsearch or similar with a log driver or agent, with labels for service and container.
- **Traces**: instrument apps with **OpenTelemetry** to follow a request across services.

Correlate the three by time and service name; most incidents show up first as a metric anomaly, are explained by logs, and are pinned down by traces.

## Performance traps

- Writing heavily to the container filesystem (copy-on-write) instead of a volume.
- DNS lookups to a slow resolver on every request; Docker's embedded DNS at `127.0.0.11` forwards to the host's resolvers.
- Java, .NET or Node runtimes sizing heaps from host memory instead of the cgroup limit in old versions (modern versions are container-aware).
- Logging so much that the log driver blocks the app (set `mode: non-blocking` with a buffer if needed).

> **Tip:** write down what you checked and what you found during an incident. The notes become the runbook that makes the next one quick.

## In practice

Set up cAdvisor, Prometheus and Grafana on your Docker host, import a container dashboard, and set two alerts: a container restarting repeatedly, and memory above 90% of its limit for 10 minutes.""",
    "key_points": [
        "Use a method: USE (utilisation, saturation, errors) per resource and RED for request-driven services.",
        "Check CPU throttling, memory against the cgroup limit, OOMKilled, exit codes and restarts.",
        "Debug minimal images with docker debug, a toolbox sharing the target's namespaces, or nsenter.",
        "Collect metrics (cAdvisor, Prometheus, Grafana), logs and traces (OpenTelemetry) and correlate them.",
    ],
    "figure_svg": USE,
    "figure_caption": "The USE method: check utilisation, saturation and errors for every resource.",
    "questions": [
        mcq("What do the letters in the USE method stand for?", ["Uptime, Speed, Errors", "Utilisation, Saturation, Errors", "Users, Sessions, Events", "Updates, Scans, Exploits"], 1,
            "Check each resource for all three."),
        mcq("In the diagram, CPU throttling belongs in which column?", ["Utilisation", "Saturation", "Errors", "None"], 1,
            "Throttling is work waiting for CPU, a saturation signal.",
            USE, "Three columns: Utilisation (CPU 100%, memory near limit), Saturation (CPU throttled, I/O queue, swap), Errors (OOM kills, restarts, 5xx in logs)."),
        mcq("How can you get a full set of network tools into a distroless container's view?", ["Install them with apt", "Run a debug container sharing its pid and network namespaces",
            "Rebuild with --debug", "Use docker logs"], 1, "--pid container:web --network container:web shares its namespaces."),
        mcq("A container's average CPU is low, but requests stall periodically and it has --cpus set. What should you check?", ["Disk space", "CPU throttling counters in the cgroup", "The image tag", "DNS"], 1,
            "Bursty workloads hit the quota and get throttled even with low average use."),
        mcq("Exit code 139 usually means?", ["Out of memory", "A segmentation fault", "Normal stop", "Image not found"], 1,
            "128 + 11 (SIGSEGV)."),
        mcq("Which tool exports per-container resource metrics for Prometheus?", ["cAdvisor", "cosign", "tini", "buildx"], 0,
            "cAdvisor reads cgroup stats for every container."),
        mcq("In the diagram, which column would 'container restarted 12 times' go in?", ["Utilisation", "Saturation", "Errors", "None"], 2,
            "Restarts are an error signal.",
            USE, "USE method columns for a slow container."),
        open_q("Describe how you'd investigate a container that becomes slow under load but never crashes.", "Apply USE to each resource: check CPU utilisation and throttling, memory against the cgroup limit and reclaim, disk I/O wait and network; look at request rate, errors and latency in metrics and logs; then trace slow requests to find which dependency is slow.",
               ["check each resource for utilisation, saturation, errors", "CPU throttling or memory pressure", "use metrics, logs and traces"], "Method beats guessing."),
        open_q("Why can an older Java app in a container use more memory than its limit and get OOM-killed?", "Older JVMs sized their default heap from the host's total memory rather than the container's cgroup limit, so the heap could grow past the limit; modern container-aware JVMs (or explicit heap settings) avoid it.",
               ["sized heap from host memory", "ignores the cgroup limit", "fix with container-aware JVM or explicit settings"], "Same story for some older .NET and Node versions."),
        open_q("Name the three signals of observability and what each is best at.", "Metrics show trends and anomalies over time and drive alerts; logs explain what happened in detail at a point in time; traces follow a single request across services to show where time was spent.",
               ["metrics for trends and alerts", "logs for detailed events", "traces for a request across services"], "Correlate them by time and service."),
    ],
}

PACK = {
    "id": "docker-advanced",
    "version": 1,
    "topic": "Docker",
    "title": "Docker at expert level",
    "summary": "How containers really work in the kernel, OCI images and BuildKit, hardening and supply-chain security, multi-arch registries, orchestration and production debugging. For experienced Docker users.",
    "icon": "code",
    "level": "advanced",
    "length": "short",
    "area": "technology",
    "tags": ["docker", "containers", "devops", "security", "kubernetes"],
    "sections": [
        {"title": "Under the hood", "summary": "The kernel features, image format and security model behind containers.", "lessons": [
            {"title": L1["title"], "summary": "Explain namespaces, cgroups and the runtime stack, and why PID 1 matters.", "lesson": L1},
            {"title": L2["title"], "summary": "Understand OCI images, overlayfs copy-on-write and BuildKit.", "lesson": L2},
            {"title": L3["title"], "summary": "Harden containers and protect the image supply chain.", "lesson": L3},
        ]},
        {"title": "Production", "summary": "Distribute, orchestrate and debug containers at scale.", "lessons": [
            {"title": L4["title"], "summary": "Build multi-platform images and run registries and tags well.", "lesson": L4},
            {"title": L5["title"], "summary": "Apply desired state with Swarm and Kubernetes, and know when not to.", "lesson": L5},
            {"title": L6["title"], "summary": "Debug and observe containers systematically in production.", "lesson": L6},
        ]},
    ],
}
