# Containers and Docker for a Python API
Created 2026-08-03 · Last verified 2026-08-03
Provenance: AI-drafted · Credits: Docker docs; Docker Community (official Python image)

## What it is

A container is an application plus its runtime environment, packaged as one
unit that runs the same anywhere Docker does. A **Dockerfile** is the recipe
that builds a **image** (the immutable package); running it creates a
**container** (the live instance). For a Python API this answers the classic
"it works on my machine" problem: Python version, system libraries, and pip
deps all ship inside the image.

## How it works

- **Every image starts from a base image** — the `FROM` instruction. "All
  Dockerfiles start from a base image. A base is the image that your image
  extends." The official `python` image provides the interpreter and pip;
  `FROM scratch` is the empty starting point you build on only when you can
  supply everything yourself (the docs warn runtime deps like C libraries and
  CA certificates make this hard).
- **The canonical Python API recipe** (from the official Python image docs):

  ```dockerfile
  FROM python:3
  WORKDIR /usr/src/app
  COPY requirements.txt ./
  RUN pip install --no-cache-dir -r requirements.txt
  COPY . .
  CMD [ "python", "./your-daemon-or-script.py" ]
  ```

  Build and run with `docker build -t my-python-app .` and
  `docker run -it --rm --name my-running-app my-python-app`.
- **Layers and caching:** each instruction adds a filesystem layer; the
  *next* command in the Dockerfile is the *first* layer that changes. Order
  matters — copying `requirements.txt` and installing before copying the rest
  of the source means dependency installs are cached and only rerun when the
  requirements actually change.
- **Include only what you need** — the docs tie image size to attack surface:
  "it's also important to include only the things you need in your image, to
  reduce the image size and attack surface."
- **Image variants:** the official Python image comes in flavors with real
  tradeoffs — the full image (most compat), `-slim` (minimal Debian; pip
  installs that need to compile C extensions can fail), and `-alpine`
  (smallest, ~5MB base, but musl libc instead of glibc — software with deep
  libc assumptions can misbehave).

## How it fails (review checklist)

- **Huge images:** installing the world (or forgetting to use `-slim`/multi-
  stage) bloats pull times and attack surface; include only what runs the app.
- **Order kills caching:** copying source before `pip install` invalidates the
  dependency layer on every source edit, making rebuilds slow.
- **Missing runtime deps in minimal images:** `-slim` lacks build toolchains,
  `scratch` lacks CA certificates — an image that "worked in build" fails at
  runtime with opaque errors.
- **Running as root** by default: production containers should drop to a
  non-root user inside the image.
- **Not checking what's in the base:** base images are a trust boundary — use
  official/verified images, pin tags, keep them updated.
- **The `-alpine`/musl surprise:** C-heavy Python wheels can break; default to
  the full image and optimize size only when you measure it matters.

## Build that proves it

Proven by [builds/production-deploy.md](../builds/production-deploy.md): a `Dockerfile`
that containerizes *this* web app (learning.md stage 7, dogfooding the
workspace product). Short rep: the `## Drill` below.

## Drill

Goal: write, build, and run your first Dockerfile, and explain what each line
does.

Steps:
1. Install Docker Desktop (or a working `docker` CLI) if you don't have it.
2. In a scratch dir, create `hello.py`:
   ```python
   import sys
   print("hello from python", sys.version.split()[0])
   ```
   and `requirements.txt` (empty is fine).
3. Write `Dockerfile` (the official-image recipe, simplified):
   ```dockerfile
   FROM python:3-slim
   WORKDIR /usr/src/app
   COPY requirements.txt ./
   RUN pip install --no-cache-dir -r requirements.txt
   COPY hello.py .
   CMD ["python", "./hello.py"]
   ```
4. Build and run:
   ```
   docker build -t hello-lab .
   docker run --rm hello-lab
   ```
   Expect output like `hello from python 3.14.6`.
5. Now reorder one line — put `COPY hello.py .` *before* the `RUN pip
   install` — rebuild and note whether the install step reruns. This is the
   layer-caching lesson.

Self-check (pass/fail — run it alone):
- `docker run --rm hello-lab` prints the Python version line.
- `docker images` lists `hello-lab`.
- You can name what each instruction does (`FROM` base, `WORKDIR` working dir,
  `COPY` files into the image, `RUN` execute at build time, `CMD` the command
  at run time) and state which reorder makes the dependency layer cache
  miss and why.
- You can say what `-slim` trades away (Debian build toolchain → some
  compiled wheels can fail to install).

Why this matters: the Dockerfile you just wrote is the same shape as the one
that will containerize this repo's web app (stage-7 build) and nearly
every production Python API you'll deploy.

## Kubernetes and container orchestration

A single Docker host gives you containers; orchestration is what you need
when containers must run across a *cluster* of machines:

- **What orchestration adds** — scheduling (which host runs which container),
  self-healing (a dead container is restarted elsewhere), and scaling across
  hosts (more replicas when load grows). Docker alone runs one machine; k8s
  runs the fleet.
- **Core ideas** — a **Deployment** declares the desired state (image, replica
  count); a **Pod** is the smallest unit — one or more containers sharing a
  network; a **Service** is the stable name/load-balancer in front of a set of
  pods. You describe the goal, and the control plane converges reality to it.
- **When a junior backend needs it** — much production Python now actually
  runs on k8s, so being able to read a Deployment/Service manifest is table
  stakes at larger companies; but Docker-only is fine to learn first. The
  Dockerfile you already wrote is the exact artifact k8s consumes, and the
  concepts here (images, ports, healthchecks) transfer directly.

## Further reading
- Docker, https://docs.docker.com/build/building/base-images/ — "Base images",
  Docker Build docs (fetched Aug 3 2026)
- Docker Community, https://hub.docker.com/_/python — "python — Official
  Image", Docker Hub (fetched Aug 3 2026; current tags e.g. `3.14.6-slim`,
  `3.14.6-alpine3.24`)
- Kubernetes, https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/ —
  "What is Kubernetes", Kubernetes docs (fetched Aug 5 2026)
