"""Docker for beginners: containers from scratch."""

from app.coursepacks import mcq, open_q
from app.packs._draw import AMBER, BLUE, GREEN, INK, MUTED, PURPLE, RED, arrow, box, line, svg, text, title

# -- diagrams ------------------------------------------------------------------------------

VM_VS_CONTAINER = svg(
    title("Virtual machines vs containers"),
    text(125, 58, "Virtual machines", 14, AMBER, weight="bold"),
    box(30, 70, 60, 50, "App", AMBER, size=12), box(100, 70, 60, 50, "App", AMBER, size=12), box(170, 70, 60, 50, "App", AMBER, size=12),
    box(30, 128, 60, 34, "Guest OS", MUTED, size=11), box(100, 128, 60, 34, "Guest OS", MUTED, size=11), box(170, 128, 60, 34, "Guest OS", MUTED, size=11),
    box(30, 170, 200, 34, "Hypervisor", PURPLE), box(30, 212, 200, 34, "Host OS + hardware", INK),
    text(365, 58, "Containers", 14, GREEN, weight="bold"),
    box(260, 70, 60, 50, "App", GREEN, size=12), box(330, 70, 60, 50, "App", GREEN, size=12), box(400, 70, 60, 50, "App", GREEN, size=12),
    box(260, 128, 200, 34, "Container engine", BLUE), box(260, 170, 200, 76, "Host OS (shared kernel)", INK, sub="+ hardware"),
    text(240, 280, "Containers share the host kernel; each VM boots its own OS", 13, MUTED),
)

LAYERS = svg(
    title("An image is a stack of read-only layers"),
    box(120, 50, 240, 34, "Container layer (read-write)", GREEN),
    box(120, 92, 240, 30, "COPY app/  (layer 4)", BLUE, size=13),
    box(120, 128, 240, 30, "RUN pip install  (layer 3)", BLUE, size=13),
    box(120, 164, 240, 30, "WORKDIR /app  (layer 2)", BLUE, size=13),
    box(120, 200, 240, 30, "FROM python:3.13-slim  (base)", PURPLE, size=13),
    text(400, 70, "A", 16, GREEN, weight="bold"), text(400, 165, "B", 16, BLUE, weight="bold"),
    text(240, 262, "Layers are shared and cached between images", 13, MUTED),
)

PORTS = svg(
    title("docker run -p 8080:80 nginx"),
    box(30, 70, 140, 160, "", INK), text(100, 95, "Your computer", 13, INK),
    box(50, 150, 100, 40, "port 8080", AMBER, size=13),
    box(260, 70, 190, 160, "", GREEN), text(355, 95, "Container", 13, GREEN),
    box(300, 150, 110, 40, "port 80", BLUE, size=13), text(355, 215, "nginx listens here", 12, MUTED),
    arrow(150, 170, 298, 170, AMBER, "traffic", width=3),
    text(100, 262, "host port", 12, AMBER), text(355, 262, "container port", 12, BLUE),
)

DOCKERFILE_FLOW = svg(
    title("From Dockerfile to running container"),
    box(20, 110, 110, 60, "Dockerfile", AMBER, sub="recipe"),
    arrow(130, 140, 180, 140, BLUE, "build", dy=-10),
    box(185, 110, 110, 60, "Image", BLUE, sub="template"),
    arrow(295, 140, 345, 140, GREEN, "run", dy=-10),
    box(350, 110, 110, 60, "Container", GREEN, sub="running copy"),
    text(240, 220, "One image can start many containers", 13, MUTED),
    text(75, 200, "X", 16, AMBER, weight="bold"), text(240, 200, "Y", 16, BLUE, weight="bold"), text(405, 200, "Z", 16, GREEN, weight="bold"),
)

VOLUMES = svg(
    title("Where container data can live"),
    box(150, 50, 180, 70, "Container", GREEN, sub="writable layer: lost on rm"),
    box(30, 190, 130, 60, "Named volume", BLUE, sub="managed by Docker"),
    box(175, 190, 130, 60, "Bind mount", AMBER, sub="a host folder"),
    box(320, 190, 130, 60, "tmpfs", PURPLE, sub="in memory only"),
    arrow(200, 120, 110, 188, BLUE), arrow(240, 120, 240, 188, AMBER), arrow(280, 120, 370, 188, PURPLE),
    text(95, 270, "P", 15, BLUE, weight="bold"), text(240, 270, "Q", 15, AMBER, weight="bold"), text(385, 270, "R", 15, PURPLE, weight="bold"),
)

COMPOSE = svg(
    title("docker compose up: one file, several services"),
    box(30, 60, 150, 170, "", AMBER), text(105, 84, "compose.yaml", 13, AMBER),
    text(50, 115, "services:", 12, INK, anchor="start"), text(62, 140, "web:", 12, BLUE, anchor="start"),
    text(62, 165, "db:", 12, GREEN, anchor="start"), text(50, 195, "volumes:", 12, INK, anchor="start"),
    text(62, 218, "dbdata:", 12, PURPLE, anchor="start"),
    arrow(180, 145, 250, 110, BLUE), arrow(180, 160, 250, 200, GREEN),
    box(255, 80, 120, 55, "web", BLUE, sub="container"), box(255, 175, 120, 55, "db", GREEN, sub="container"),
    line(315, 135, 315, 175, MUTED, dash="5 4"), text(398, 160, "shared network", 12, MUTED),
    box(390, 220, 80, 36, "dbdata", PURPLE, size=12), line(375, 215, 392, 230, PURPLE),
)

# -- lessons -------------------------------------------------------------------------------

L1 = {
    "title": "What containers are, and why they matter",
    "minutes": 7,
    "photo_query": "",
    "body": """"It works on my machine" is one of the oldest problems in software. An app depends on a particular language version, libraries and settings, and the moment it moves to another computer something is different. **Containers** solve this by packaging an app together with everything it needs, so it runs the same everywhere.

## What a container is

A **container** is a normal process on your computer that has been given its own private view of the system: its own files, its own network interfaces and its own list of processes. Inside, the app believes it is alone on a small, clean machine. Outside, it is just another process sharing the host's operating system **kernel**.

**Docker** is the most popular tool for building and running containers. It gives you a simple command line (`docker run`, `docker build` and friends) and a format for packaging apps called an **image**.

## Containers vs virtual machines

A **virtual machine (VM)** emulates a whole computer. Each VM boots its own full operating system on top of a **hypervisor**. That gives strong isolation, but every VM carries gigabytes of OS and takes time to boot.

A container skips the extra operating system. All containers on a host share its kernel, so they:

- start in well under a second rather than tens of seconds,
- are usually megabytes rather than gigabytes,
- let you run many more apps on the same hardware.

The trade-off: because they share a kernel, a Linux container needs a Linux kernel. On Windows and macOS, Docker Desktop quietly runs a small Linux VM to host your containers.

> **Common misconception:** containers are not "lightweight VMs". They are isolated processes. That's why they're fast, and why kernel-level security matters.

## Why people use them

- **Consistency**: the same image runs on your laptop, a test server and production.
- **Isolation**: two apps needing different versions of Python or PostgreSQL can sit side by side.
- **Speed**: spin up a database for testing in seconds, throw it away afterwards.
- **Self-hosting**: most home-lab software (media servers, dashboards, password managers) ships as a Docker image.

## The words you'll meet

- **Image**: a read-only template containing the app and its files.
- **Container**: a running (or stopped) instance of an image.
- **Registry**: a place images are stored and shared, such as **Docker Hub**.
- **Docker Engine**: the background service (daemon) that actually runs containers.

## In practice

Install Docker Desktop (Windows, macOS) or Docker Engine (Linux), then run `docker run hello-world`. Docker downloads a tiny image, starts a container from it, prints a message and exits. That one command shows the whole cycle: pull an image, create a container, run it.""",
    "key_points": [
        "A container is an isolated process that shares the host's kernel, not a separate computer.",
        "Virtual machines each boot a full guest OS on a hypervisor; containers don't, so they're smaller and faster.",
        "An image is the read-only template; a container is a running instance of it.",
        "Registries such as Docker Hub store and share images.",
    ],
    "figure_svg": VM_VS_CONTAINER,
    "figure_caption": "VMs each run a guest operating system on a hypervisor; containers share the host's kernel through the container engine.",
    "questions": [
        mcq("What is a container, really?", ["A full virtual computer with its own operating system", "An isolated process that shares the host's kernel",
            "A compressed backup of a server", "A programming language runtime"], 1,
            "A container is a normal process given its own view of files, network and processes. It shares the host kernel; it doesn't boot an OS."),
        mcq("In the diagram, what does each virtual machine have that the containers don't?", ["Its own app", "Its own guest operating system", "Access to hardware", "A network connection"], 1,
            "Each VM boots a full guest OS on the hypervisor. Containers share the host's kernel through the container engine.",
            VM_VS_CONTAINER, "Two stacks side by side: three apps on three guest operating systems on a hypervisor, and three apps directly on a container engine on a shared host OS."),
        mcq("Why do containers usually start much faster than virtual machines?", ["They use faster hardware", "They don't boot an operating system; they start a process",
            "They skip the network", "They are written in Go"], 1, "Starting a container is starting a process with isolation, not booting a whole OS."),
        mcq("Which term describes the read-only template a container is started from?", ["Volume", "Registry", "Image", "Daemon"], 2,
            "An image is the template. A registry stores images; a volume stores data; the daemon runs containers."),
        mcq("What is Docker Hub?", ["A registry where images are stored and shared", "The Docker command line", "A Linux distribution", "A kind of virtual machine"], 0,
            "Docker Hub is the default public registry that `docker pull` and `docker run` download images from."),
        mcq("On a Mac, how does Docker Desktop run Linux containers?", ["It translates them to macOS apps", "It runs them inside a small hidden Linux virtual machine",
            "It can't run Linux containers", "It uses the macOS kernel directly"], 1,
            "Linux containers need a Linux kernel, so Docker Desktop runs a lightweight Linux VM behind the scenes."),
        mcq("In the diagram, which layer is shared by all three containers?", ["The apps", "The guest operating systems", "The host OS kernel", "The hypervisor"], 2,
            "Containers share the host's kernel. There's no guest OS or hypervisor in the container stack.",
            VM_VS_CONTAINER, "Diagram comparing VMs (apps on guest OSes on a hypervisor) with containers (apps on a container engine on a shared host OS)."),
        open_q("Explain the difference between an image and a container.", "An image is a read-only template holding the app and its files. A container is a running (or stopped) instance created from that image; you can start many containers from one image.",
               ["image is a read-only template", "container is a running instance of an image"], "Think of the image as the recipe or class, the container as the meal or object."),
        open_q("Give two reasons someone might choose containers over virtual machines for running several small web apps.", "Containers start in seconds and use far less memory and disk because they don't each carry an OS, so many more fit on one server. They also package each app with its dependencies so they run consistently.",
               ["faster to start or lighter on resources", "no separate OS per app", "consistent packaging of dependencies"], "Lightweight, fast and consistent are the usual reasons; VMs win when you need strong isolation or a different OS kernel."),
        open_q("What does running `docker run hello-world` actually do, step by step?", "Docker looks for the hello-world image locally, pulls it from Docker Hub if it isn't there, creates a container from it, runs it (it prints a message) and the container exits.",
               ["pulls or downloads the image", "creates and runs a container", "the container exits after printing"], "It shows the whole cycle in one command: pull, create, run."),
    ],
}

L2 = {
    "title": "Images, layers and registries",
    "minutes": 7,
    "photo_query": "",
    "body": """Every container starts from an **image**, so it pays to understand what's inside one and where images come from.

## Layers

An image isn't one big file. It's a stack of read-only **layers**, each recording the file changes made by one build step: install some packages, copy your code, set a working directory. When you start a container, Docker adds a thin **writable layer** on top. Anything the container changes lands there, and is thrown away when the container is removed.

Layers are identified by a hash of their content, which gives two big wins:

- **Sharing**: ten images built on `python:3.13-slim` store that base layer once.
- **Caching**: when you rebuild, unchanged steps reuse their existing layers instead of running again.

## Names and tags

An image name looks like `registry/repository:tag`, for example `docker.io/library/nginx:1.27`.

- The **registry** defaults to Docker Hub (`docker.io`) when you leave it out.
- The **repository** is the image's name (`nginx`, or `grafana/grafana` for one owned by an organisation).
- The **tag** is a label, usually a version. If you leave it out you get **`latest`**, which simply means "whatever was last tagged latest", not necessarily the newest or most stable.

> **Tip:** pin a version tag such as `nginx:1.27` in anything you care about. `latest` can change under you the next time you pull.

Every image also has a **digest** (`sha256:…`), a fingerprint of its exact content. Tags can be moved to a new image; a digest never changes.

## Getting and managing images

- `docker pull nginx:1.27` downloads an image.
- `docker images` (or `docker image ls`) lists the images you have.
- `docker rmi nginx:1.27` removes one.
- `docker image prune` clears out unused, untagged images.

## Official and trusted images

Docker Hub has **Docker Official Images** (like `nginx`, `postgres`, `python`) maintained with Docker, and **verified publisher** images from companies. Anyone can publish an image, so prefer official or well-known sources and check how recently an image was updated.

Images also come in variants. `python:3.13` is a full Debian base; `python:3.13-slim` drops extras; `-alpine` variants use the tiny Alpine Linux. Smaller images download faster and contain less to attack, though Alpine's different C library occasionally causes compatibility surprises.

## In practice

Run `docker pull python:3.13-slim` then `docker image inspect python:3.13-slim` and look for `Layers`. Then `docker history python:3.13-slim` shows each layer and the step that created it.""",
    "key_points": [
        "Images are stacks of read-only layers; a running container adds one writable layer on top.",
        "Layers are shared between images and cached between builds.",
        "Names are registry/repository:tag; with no tag you get latest, which isn't necessarily stable.",
        "A digest identifies exact image content and never changes; tags can be moved.",
    ],
    "figure_svg": LAYERS,
    "figure_caption": "Read-only image layers (blue, purple base) with the container's writable layer (green) on top.",
    "questions": [
        mcq("In the diagram, what is the layer marked A?", ["The base image", "The container's writable layer", "A cached build step", "A registry"], 1,
            "The top green layer is added when a container starts. Changes made inside the container land there.",
            LAYERS, "A stack of boxes: a base image at the bottom, three build-step layers, and a container read-write layer marked A on top; the middle layers are marked B."),
        mcq("What happens to files written inside a container when the container is removed with docker rm?", ["They're saved to the image", "They're lost with the writable layer",
            "They move to Docker Hub", "They're kept in the base layer"], 1, "The writable layer belongs to the container. Remove the container and its changes go too, unless they were in a volume."),
        mcq("What tag do you get from `docker pull nginx`?", ["stable", "newest", "latest", "1.0"], 2,
            "With no tag Docker uses `latest`, which is just a label someone chose to move; it isn't guaranteed to be the newest or most stable."),
        mcq("Why do image layers make rebuilding faster?", ["Docker compresses them better", "Unchanged steps reuse cached layers instead of running again",
            "Layers are downloaded in parallel", "Layers skip the network"], 1, "Each layer is keyed by its content and the step that made it, so unchanged steps come from cache."),
        mcq("In `ghcr.io/grafana/grafana:11.2`, what is `11.2`?", ["The registry", "The repository", "The tag", "The digest"], 2,
            "registry/repository:tag. Here ghcr.io is the registry, grafana/grafana the repository and 11.2 the tag."),
        mcq("Which identifies an image's exact content and never changes?", ["Its tag", "Its digest (sha256)", "Its repository name", "Its size"], 1,
            "Tags can be re-pointed at new images; a digest is a hash of the content itself."),
        mcq("In the diagram, which layers are read-only and can be shared with other images?", ["Only A", "The layers marked B and the base", "None of them", "Only the top two"], 1,
            "All image layers (B and the base) are read-only and shareable; only the container layer A is writable.",
            LAYERS, "Layer stack with the container layer A on top and image layers B below it."),
        open_q("Why is pinning a version tag (like nginx:1.27) safer than using latest in a real deployment?", "Because latest can be moved to a different image at any time, so the next pull might bring a new major version and break things. A version tag keeps you on a known release until you choose to upgrade.",
               ["latest can change without you knowing", "a version tag gives a known, repeatable image"], "Repeatability is the point; even better is pinning by digest."),
        open_q("Two images are both built on python:3.13-slim. Explain how Docker stores them on disk.", "The python:3.13-slim base layers are stored once and shared by both images; only the layers that differ are stored separately, saving disk space and download time.",
               ["base layers stored once and shared", "only the differing layers are extra"], "Content-addressed layers make sharing automatic."),
        open_q("What's the trade-off of choosing an -alpine image variant?", "Alpine images are much smaller, so they download faster and contain less to attack, but Alpine uses a different C library (musl), which can cause compatibility problems with some software.",
               ["smaller and faster to download", "different C library can break compatibility"], "Slim Debian variants are a common middle ground."),
    ],
}

L3 = {
    "title": "Running and managing containers",
    "minutes": 8,
    "photo_query": "",
    "body": """You know what images are. Now let's run things. Almost everything here is a variation on `docker run`.

## docker run

`docker run [options] image [command]` creates a container from an image and starts it. The options you'll use constantly:

- `-d` (**detached**): run in the background and give you your prompt back.
- `--name web`: give the container a name you choose, instead of a random one.
- `-p 8080:80`: **publish a port**. Traffic to port 8080 on your computer is forwarded to port 80 inside the container. The order is always **host:container**.
- `-e KEY=value`: set an **environment variable**, the usual way to configure a containerised app.
- `-it`: interactive with a terminal, for running a shell: `docker run -it ubuntu bash`.
- `--rm`: delete the container automatically when it exits; ideal for one-off commands.

For example, `docker run -d --name web -p 8080:80 nginx:1.27` starts a web server you can open at `http://localhost:8080`.

## Looking at what's running

- `docker ps` lists running containers; `docker ps -a` includes stopped ones.
- `docker logs web` shows what the container printed; add `-f` to follow it live.
- `docker exec -it web sh` opens a shell **inside** a running container, handy for poking around.
- `docker inspect web` dumps everything Docker knows about it, as JSON.
- `docker stats` shows live CPU and memory use.

## The container lifecycle

A container is **created**, **running**, then **exited** (stopped). Stopping doesn't delete it: its writable layer is still there.

- `docker stop web` asks the process to shut down (SIGTERM, then a forced kill after a grace period).
- `docker start web` starts a stopped container again, with its files intact.
- `docker restart web` stops and starts it.
- `docker rm web` deletes a stopped container (`-f` forces a running one).

> **Common misconception:** `docker stop` and `docker rm` are different. Stopping keeps the container (and its writable layer) on disk; removing deletes it.

A container runs as long as its **main process** runs. If that process exits, the container exits, which is why a container started with a command that finishes immediately stops straight away.

## Cleaning up

Stopped containers and unused images pile up. `docker container prune` removes stopped containers, and `docker system prune` clears stopped containers, unused networks, dangling images and build cache in one go (it asks first).

## In practice

1. `docker run -d --name web -p 8080:80 nginx:1.27` and open `localhost:8080`.
2. `docker logs -f web` and refresh the page to watch requests arrive.
3. `docker exec -it web sh`, then `ls /usr/share/nginx/html` to see the files it serves.
4. `docker stop web && docker rm web` to tidy up.""",
    "key_points": [
        "docker run creates and starts a container; -d runs it in the background, --name names it.",
        "-p host:container publishes a port; -e sets environment variables.",
        "docker ps, logs, exec and inspect let you see what's running and look inside.",
        "Stopping keeps a container on disk; removing deletes it. A container lives as long as its main process.",
    ],
    "figure_svg": PORTS,
    "figure_caption": "With -p 8080:80, traffic to port 8080 on your computer is forwarded to port 80 inside the container.",
    "questions": [
        mcq("In `docker run -p 8080:80 nginx`, which port do you open in your browser?", ["80", "8080", "Either", "Neither"], 1,
            "The format is host:container. You browse to the host port, 8080, which forwards to 80 inside the container.",
            PORTS, "Your computer's port 8080 forwards traffic to port 80 inside an nginx container."),
        mcq("What does the -d flag do?", ["Deletes the container when it exits", "Runs the container in the background", "Enables debugging", "Downloads the image only"], 1,
            "-d is detached mode. --rm is the one that deletes on exit."),
        mcq("Which command shows a container's output?", ["docker ps", "docker logs", "docker inspect", "docker images"], 1,
            "docker logs prints what the container wrote to stdout and stderr; -f follows it live."),
        mcq("How do you open a shell inside a container that's already running?", ["docker run -it web sh", "docker exec -it web sh", "docker attach --shell web", "docker shell web"], 1,
            "exec runs a new process in an existing container. docker run would create a new container."),
        mcq("What's the difference between docker stop and docker rm?", ["None, they're aliases", "stop keeps the container on disk; rm deletes it",
            "stop deletes it; rm pauses it", "rm only removes images"], 1, "A stopped container can be started again with its files intact; rm deletes it."),
        mcq("A container exits immediately after `docker run`. What's the most likely reason?", ["The image is corrupt", "Its main process finished, so the container ended",
            "Docker ran out of memory", "Port 80 was busy"], 1, "A container runs only as long as its main process. A command that completes straight away ends the container."),
        mcq("In the diagram, which number is the container port?", ["8080", "80", "443", "There isn't one"], 1,
            "80 is where nginx listens inside the container; 8080 is the published host port.",
            PORTS, "Diagram of -p 8080:80: host port 8080 on the left forwarding to container port 80 on the right."),
        open_q("Write a docker run command that starts postgres:16 in the background, named db, with the environment variable POSTGRES_PASSWORD set to secret.", "docker run -d --name db -e POSTGRES_PASSWORD=secret postgres:16",
               ["-d for background", "--name db", "-e POSTGRES_PASSWORD=secret", "postgres:16 as the image"], "Options go before the image name; anything after the image is the command to run."),
        open_q("Your web container isn't responding. Describe how you'd investigate using Docker commands.", "Check it's running with docker ps (or ps -a to see if it exited), read its output with docker logs, check the published ports in docker ps or docker inspect, and use docker exec to open a shell inside and test the app.",
               ["docker ps to check it's running", "docker logs to read errors", "check ports or exec inside to test"], "Logs first is a good habit; most problems announce themselves there."),
        open_q("Why is --rm useful for one-off commands like `docker run --rm alpine date`?", "Because the container is deleted automatically when it exits, so one-off runs don't leave stopped containers piling up on disk.",
               ["container is removed automatically on exit", "avoids leftover stopped containers"], "Without --rm every run leaves a stopped container behind until you prune."),
    ],
}

L4 = {
    "title": "Writing your first Dockerfile",
    "minutes": 8,
    "photo_query": "",
    "body": """Using other people's images is useful; packaging your own app is where Docker shines. You do that with a **Dockerfile**, a text file of instructions that `docker build` turns into an image.

## A first Dockerfile

Here's one for a small Python web app:

```
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "app.py"]
```

Line by line:

- **FROM** picks the **base image** to build on. Every Dockerfile starts with one.
- **WORKDIR** sets the working directory for the following steps (and creates it).
- **COPY** copies files from your project (the **build context**) into the image.
- **RUN** runs a command at **build time** and saves the result as a new layer, here installing dependencies.
- **EXPOSE** documents which port the app listens on. It doesn't publish anything; you still need `-p` when you run it.
- **CMD** is the default command when a container starts from the image.

## Building and running it

`docker build -t myapp:1.0 .` builds the image. `-t` tags it, and the final `.` is the **build context**: the folder whose files `COPY` can see. Then `docker run -d -p 8000:8000 myapp:1.0` runs it.

## Order matters: the build cache

Each instruction makes a layer, and Docker reuses a cached layer if the instruction and its inputs haven't changed. Once one step changes, **every step after it re-runs**.

That's why the example copies `requirements.txt` and installs dependencies *before* copying the rest of the code. Your code changes constantly; your dependencies rarely do. With this order, editing `app.py` only re-runs the final `COPY`, not the slow `pip install`.

> **Tip:** put the things that change least near the top of the Dockerfile and the things that change most near the bottom.

## RUN vs CMD

People often mix these up:

- **RUN** happens once, while the image is being built.
- **CMD** happens every time a container starts.

`RUN apt-get install …` belongs in the build. `CMD ["python", "app.py"]` is what the container does when it runs. Write CMD in the JSON (exec) form with square brackets so your app receives stop signals properly.

## A .dockerignore file

Add a `.dockerignore` next to the Dockerfile listing things that shouldn't be sent to the build: `.git`, `node_modules`, local virtual environments, secrets like `.env`. It makes builds faster and keeps junk (and passwords) out of your image.

## In practice

Take any small project, write a Dockerfile following the pattern above, build it with `docker build -t test .`, change one line of code and rebuild. Watch how many steps say `CACHED`.""",
    "key_points": [
        "A Dockerfile is a recipe; docker build turns it into an image, docker run starts containers from it.",
        "FROM sets the base image, COPY adds files, RUN runs build-time commands, CMD is the default start command.",
        "EXPOSE only documents a port; publishing still needs -p.",
        "Copy dependency lists and install them before copying code so the cache isn't busted by every code change.",
    ],
    "figure_svg": DOCKERFILE_FLOW,
    "figure_caption": "A Dockerfile is built into an image; containers are run from the image.",
    "questions": [
        mcq("Which instruction must come first in a Dockerfile (apart from comments and ARG)?", ["RUN", "COPY", "FROM", "CMD"], 2,
            "FROM sets the base image every other step builds on."),
        mcq("What's the difference between RUN and CMD?", ["They're the same", "RUN executes at build time; CMD is the default command when a container starts",
            "RUN starts the container; CMD builds the image", "CMD runs as root; RUN doesn't"], 1, "RUN bakes results into the image; CMD runs each time a container starts."),
        mcq("Does EXPOSE 8000 make the app reachable from your computer?", ["Yes, always", "No, it only documents the port; you still publish it with -p",
            "Only on Linux", "Only if CMD uses port 8000"], 1, "EXPOSE is documentation (and a hint for some tools). -p does the publishing."),
        mcq("In the diagram, what happens at the arrow between Y and Z?", ["docker build", "docker run", "docker push", "docker pull"], 1,
            "The image (Y) is run to create a container (Z). The arrow from the Dockerfile (X) to the image is docker build.",
            DOCKERFILE_FLOW, "Three boxes left to right: Dockerfile (X), Image (Y), Container (Z), joined by arrows labelled build and run."),
        mcq("Why copy requirements.txt and run pip install before COPY . . ?", ["pip needs to run first alphabetically", "So editing code doesn't invalidate the cached dependency install",
            "COPY . . deletes requirements.txt", "It makes the image smaller"], 1, "Once a step changes, every later step re-runs. Dependencies change rarely, so install them early."),
        mcq("What does the final `.` in `docker build -t myapp .` mean?", ["Build in the background", "The current folder is the build context",
            "Use the latest tag", "Build every Dockerfile"], 1, "The build context is the set of files COPY can use; `.` means this folder."),
        mcq("In the diagram, which item can you create many containers from?", ["X", "Y", "Z", "None of them"], 1,
            "One image (Y) can start any number of containers.",
            DOCKERFILE_FLOW, "Dockerfile X builds image Y, which runs container Z."),
        open_q("What's a .dockerignore file for, and what would you put in it?", "It lists files and folders to leave out of the build context, so builds are faster and junk or secrets don't end up in the image. Typical entries are .git, node_modules, local virtual environments and .env files.",
               ["excludes files from the build context", "faster builds", "keeps secrets or junk out of the image"], "Anything sent in the context can be COPY'd into the image, intentionally or not."),
        open_q("You change one line in app.py and rebuild. Explain which Dockerfile steps re-run in the example Dockerfile and why.", "Only the final COPY . . step (and anything after it) re-runs, because the earlier steps' inputs haven't changed, so Docker reuses their cached layers including the pip install.",
               ["only COPY . . and later steps re-run", "earlier steps come from cache because their inputs didn't change"], "This is exactly why the order matters."),
        open_q("Why write CMD as CMD [\"python\", \"app.py\"] instead of CMD python app.py?", "The JSON (exec) form runs python directly as the container's main process, so it receives stop signals like SIGTERM and can shut down cleanly. The shell form wraps it in a shell that may not pass signals on.",
               ["exec form runs the process directly", "app receives stop signals"], "Graceful shutdown matters for databases and web servers."),
    ],
}

L5 = {
    "title": "Keeping data: volumes and bind mounts",
    "minutes": 7,
    "photo_query": "",
    "body": """Containers are meant to be disposable: you remove them and start fresh ones from the image whenever you upgrade. But a database, a photo library or a config file needs to survive that. Docker gives you three places to keep data outside a container's writable layer.

## Named volumes

A **volume** is storage managed by Docker, kept in Docker's own area of the host's disk (on Linux, under `/var/lib/docker/volumes`).

```
docker volume create pgdata
docker run -d --name db -e POSTGRES_PASSWORD=secret -v pgdata:/var/lib/postgresql/data postgres:16
```

`-v pgdata:/var/lib/postgresql/data` mounts the volume `pgdata` at that path inside the container. Remove the container, start a new one with the same `-v`, and the data is still there. Volumes are the recommended way to persist app data: Docker manages them, they're easy to back up, and they perform well.

## Bind mounts

A **bind mount** maps a folder (or file) from the host into the container:

```
docker run -d -p 8080:80 -v /home/brad/site:/usr/share/nginx/html:ro nginx:1.27
```

Now nginx serves whatever is in `/home/brad/site`, and edits on the host show up immediately. Bind mounts are ideal for config files and for development, where you want the container to see your source code live. The `:ro` suffix makes it **read-only** inside the container.

The catch: the container sees the host's files with the host's permissions and paths, so a bind mount ties the container to that particular machine's folder layout.

## tmpfs mounts

A **tmpfs** mount lives only in memory. It's fast and disappears when the container stops, useful for scratch files or secrets you never want written to disk.

## Choosing

| Need | Use |
| --- | --- |
| A database's or app's own data | Named volume |
| A config file or source code you edit on the host | Bind mount |
| Temporary or sensitive scratch data | tmpfs |

> **Common misconception:** "I'll just keep data inside the container." That works until you upgrade the image: the new container starts from a clean image and the old writable layer is gone.

## Managing volumes

- `docker volume ls` lists volumes; `docker volume inspect pgdata` shows where one lives.
- `docker volume rm pgdata` deletes one (only when no container uses it).
- `docker volume prune` removes volumes no container uses, so read the list before you confirm.

## In practice

Run PostgreSQL with a named volume, create a table, then `docker rm -f db` and start a new container with the same `-v pgdata:...`. Your table is still there. That's the pattern behind upgrading any self-hosted app: pull the new image, recreate the container, keep the volume.""",
    "key_points": [
        "A container's writable layer is lost when it's removed, so persistent data must live elsewhere.",
        "Named volumes are managed by Docker and are the default choice for app data.",
        "Bind mounts map a host folder into the container: great for config and development, tied to that host's layout.",
        "tmpfs mounts live in memory only; :ro makes a mount read-only.",
    ],
    "figure_svg": VOLUMES,
    "figure_caption": "Data written to a container's writable layer is lost on removal; volumes (P), bind mounts (Q) and tmpfs (R) keep it elsewhere.",
    "questions": [
        mcq("You upgrade an app by removing its container and starting a new one from a newer image. Where must its database files be to survive?", ["In the container's writable layer",
            "In a volume (or bind mount)", "In the image", "In /tmp inside the container"], 1, "The writable layer goes with the old container. Volumes and bind mounts live outside it."),
        mcq("In the diagram, which storage type is labelled Q?", ["Named volume", "Bind mount", "tmpfs", "Image layer"], 1,
            "Q is the bind mount: a folder from the host mapped into the container.",
            VOLUMES, "A container at the top with arrows to three storage types: named volume P, bind mount Q and tmpfs R."),
        mcq("What does `-v pgdata:/var/lib/postgresql/data` do?", ["Copies the folder into the image", "Mounts the named volume pgdata at that path in the container",
            "Deletes pgdata", "Shares the container's data with the host's home folder"], 1, "name:path mounts a named volume; /host/path:path would be a bind mount."),
        mcq("Which is best for a config file you want to edit on the host and have the container read?", ["A named volume", "A bind mount", "tmpfs", "Baking it into the image each time"], 1,
            "A bind mount shows host edits inside the container straight away."),
        mcq("What does :ro at the end of a mount mean?", ["Root only", "Read-only inside the container", "Run once", "Remove on exit"], 1,
            "The container can read but not change the mounted files."),
        mcq("In the diagram, which storage disappears when the container stops?", ["P", "Q", "R", "All of them"], 2,
            "R is tmpfs, held in memory only.",
            VOLUMES, "Container with arrows to named volume P, bind mount Q and tmpfs R."),
        mcq("Why should you read the list before confirming `docker volume prune`?", ["It's slow", "It deletes volumes no container currently uses, which could include data you still want",
            "It removes images too", "It restarts Docker"], 1, "A stopped-and-removed database's volume counts as unused."),
        open_q("Explain the difference between a named volume and a bind mount.", "A named volume is storage Docker creates and manages in its own area of the host. A bind mount maps a specific folder or file from the host's filesystem into the container, so the container depends on that host path and its permissions.",
               ["Docker manages volumes", "bind mount maps a specific host folder"], "Volumes are portable and managed; bind mounts are direct and host-specific."),
        open_q("Describe how you'd upgrade a self-hosted app from version 1 to version 2 without losing its data.", "Make sure its data is in a volume, back it up, pull the version 2 image, stop and remove the old container, then start a new container from the new image with the same volume mounted.",
               ["data kept in a volume", "pull the new image", "recreate the container with the same volume"], "Backing up first is cheap insurance."),
        open_q("Why might you put a secret in a tmpfs mount rather than a volume?", "Because tmpfs lives only in memory, the secret is never written to disk and disappears when the container stops, reducing the chance of it leaking from storage or backups.",
               ["kept in memory, never written to disk", "gone when the container stops"], "Less persistence means less to leak."),
    ],
}

L6 = {
    "title": "Docker Compose: several containers, one file",
    "minutes": 8,
    "photo_query": "",
    "body": """Real apps are rarely one container. A web app needs its database; a self-hosted service needs a cache and a reverse proxy. Typing long `docker run` commands for each, in the right order with the right networks, gets old fast. **Docker Compose** describes the whole set in one YAML file and starts it with one command.

## A compose file

Save this as `compose.yaml`:

```
services:
  web:
    image: ghcr.io/example/notes:2.1
    ports:
      - "8080:8000"
    environment:
      DATABASE_URL: postgres://notes:secret@db:5432/notes
    depends_on:
      - db
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: notes
      POSTGRES_PASSWORD: secret
    volumes:
      - dbdata:/var/lib/postgresql/data
volumes:
  dbdata:
```

Each entry under **services** becomes a container. The keys map directly to `docker run` options: `image`, `ports` (-p), `environment` (-e), `volumes` (-v). The top-level **volumes** section declares the named volume.

## The commands

- `docker compose up -d` creates the network, volumes and containers, and starts everything in the background.
- `docker compose ps` lists this project's containers; `docker compose logs -f web` follows one service's logs.
- `docker compose pull` then `docker compose up -d` upgrades to newer images, recreating only what changed.
- `docker compose down` stops and removes the containers and network. Your **named volumes are kept** unless you add `-v`.

## Networking for free

Compose puts the project's services on their own network, and each service can reach the others **by its service name**. That's why the web app's `DATABASE_URL` says `db:5432`: `db` is the service name, resolved by Docker's built-in DNS. You don't publish the database's port at all; only `web` is reachable from outside.

## depends_on

`depends_on` controls **start order**: Compose starts `db` before `web`. On its own it doesn't wait for the database to be *ready*, only started. (Adding a health check and `condition: service_healthy` fixes that, which the intermediate course covers.)

> **Tip:** keep the compose file in a folder of its own, with a `.env` file beside it for passwords. Compose reads `.env` automatically and you can write `${POSTGRES_PASSWORD}` in the YAML.

## In practice

Most self-hosted software publishes a ready-made `compose.yaml`. The everyday workflow is: copy it into a folder, set the passwords, `docker compose up -d`, and later `docker compose pull && docker compose up -d` to upgrade. Version-control that folder and your whole setup is reproducible.""",
    "key_points": [
        "Compose describes several containers, their ports, environment, volumes and networks in one YAML file.",
        "docker compose up -d starts everything; down removes containers and network but keeps named volumes unless you add -v.",
        "Services on the same Compose network reach each other by service name through Docker's DNS.",
        "depends_on sets start order but doesn't by itself wait for a service to be ready.",
    ],
    "figure_svg": COMPOSE,
    "figure_caption": "One compose.yaml defines the web and db services and their volume; Compose runs them on a shared network.",
    "questions": [
        mcq("In the compose file, how does the web service find the database?", ["By the host's IP address", "By the service name db, resolved by Docker's DNS",
            "Through port 8080", "By reading the volume"], 1, "Services on a Compose network reach each other by service name."),
        mcq("What does `docker compose down` do to named volumes by default?", ["Deletes them", "Keeps them", "Backs them up", "Moves them to the image"], 1,
            "Volumes survive down unless you pass -v, so your data is safe across restarts."),
        mcq("In the diagram, what joins the web and db containers?", ["A bind mount", "A shared network", "A shared image", "Port 8080"], 1,
            "Compose creates a network for the project and attaches both services to it.",
            COMPOSE, "A compose.yaml listing web and db services and a dbdata volume, with arrows to web and db containers on a shared network and the volume attached to db."),
        mcq("What does depends_on: [db] guarantee?", ["The database is ready to accept connections before web starts", "db is started before web",
            "web restarts if db fails", "db and web share a volume"], 1, "It's about start order only. Readiness needs a health check condition."),
        mcq("Why doesn't the database service need a ports: entry in this setup?", ["Postgres doesn't use ports", "Only web needs to be reachable from outside; web reaches db over the internal network",
            "Compose publishes every port automatically", "The volume handles connections"], 1, "Not publishing the database keeps it off your LAN entirely."),
        mcq("How do you upgrade services to newer images in a Compose project?", ["docker compose restart", "docker compose pull, then docker compose up -d",
            "docker compose down -v", "Edit the volume"], 1, "pull fetches new images; up -d recreates only the containers whose image or config changed."),
        mcq("In the diagram, which service is the dbdata volume attached to?", ["web", "db", "Both", "Neither"], 1,
            "The volume is mounted into db, where Postgres keeps its data.",
            COMPOSE, "Compose diagram with the dbdata volume attached to the db container."),
        open_q("Why is a compose file better than a list of docker run commands for a multi-container app?", "It describes all the services, ports, environment, volumes and networking in one version-controllable file, so the whole app starts, stops and upgrades with one command and is reproducible on another machine.",
               ["everything in one file", "one command to start or stop", "reproducible and version-controllable"], "It's documentation and automation at once."),
        open_q("Where would you keep the database password for a compose project, and how does the YAML use it?", "In a .env file next to compose.yaml (kept out of git), which Compose reads automatically; the YAML refers to it with ${POSTGRES_PASSWORD}.",
               [".env file next to the compose file", "referenced with ${VARIABLE} in the YAML"], "Keep .env out of version control."),
        open_q("Your web container fails on first start because the database isn't ready yet, even with depends_on. Explain why.", "depends_on only makes Compose start db first; it doesn't wait until Postgres is ready to accept connections, so web can try to connect while the database is still initialising.",
               ["depends_on only orders startup", "doesn't wait for the database to be ready"], "Health checks with condition: service_healthy, or retry logic in the app, solve it."),
    ],
}

PACK = {
    "id": "docker-beginner",
    "version": 1,
    "topic": "Docker",
    "title": "Docker from scratch",
    "summary": "What containers are, how images work, and how to run, build and compose your own. For complete beginners who want to self-host apps or package their own.",
    "icon": "code",
    "level": "beginner",
    "length": "short",
    "area": "technology",
    "tags": ["docker", "containers", "devops", "self-hosting"],
    "sections": [
        {"title": "Containers and images", "summary": "What containers are and how to run them.", "lessons": [
            {"title": L1["title"], "summary": "Explain what a container is and how it differs from a virtual machine.", "lesson": L1},
            {"title": L2["title"], "summary": "Describe image layers, tags, digests and registries.", "lesson": L2},
            {"title": L3["title"], "summary": "Run, inspect, stop and remove containers with confidence.", "lesson": L3},
        ]},
        {"title": "Building and composing", "summary": "Package your own app and run multi-container setups.", "lessons": [
            {"title": L4["title"], "summary": "Write a Dockerfile that builds quickly and runs correctly.", "lesson": L4},
            {"title": L5["title"], "summary": "Keep data safe across upgrades with volumes and bind mounts.", "lesson": L5},
            {"title": L6["title"], "summary": "Describe and run a multi-container app with Docker Compose.", "lesson": L6},
        ]},
    ],
}
