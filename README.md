# Docker Fundamentals

A free, hands-on course in containers, in seven lessons, for developers who
build AI web apps. You take one small Python service, put it in a container,
make it safe to ship, give it a database and a real model, and follow it to
AWS, Cloudflare and Kubernetes.

**Read it here: https://espad0.github.io/docker-fundamentals/**

The lessons use [Podman](https://podman.io), a free tool that works like
Docker, on a Mac with Apple silicon. The ideas are the same, and most commands
work with `docker` in place of `podman`.

## The lessons

| # | Lesson | What it covers |
|---|---|---|
| 1 | [What a Container Is](https://espad0.github.io/docker-fundamentals/lesson-01/) | A process, an image made of layers, the Linux VM on a Mac, and what happens when a container stops |
| 2 | [Building Container Images](https://espad0.github.io/docker-fundamentals/lesson-02/) | The Containerfile, the build context, the layer cache, the start command and ports |
| 3 | [Production-Ready Images](https://espad0.github.io/docker-fundamentals/lesson-03/) | A non-root user, settings and secrets at run time, health checks, logs, a pinned base image |
| 4 | [Volumes, Networks and Compose](https://espad0.github.io/docker-fundamentals/lesson-04/) | Volumes, shared folders, networks, and a Postgres database with Compose |
| 5 | [Serving a Real Model](https://espad0.github.io/docker-fundamentals/lesson-05/) | PyTorch without GPU libraries, readiness, memory and CPU limits, streaming, and what GPUs need |
| 6 | [Shipping to AWS and Cloudflare](https://espad0.github.io/docker-fundamentals/lesson-06/) | Registries, building for servers from a Mac, GitLab CI, AWS ECS Express Mode, Cloudflare Containers |
| 7 | [Your App on Kubernetes](https://espad0.github.io/docker-fundamentals/lesson-07/) | A strict image, measured memory and CPU, the objects a devops team writes, a local cluster with kind, failures on purpose, a handoff sheet |

About 9 hours in total, including the labs.

## Before you start

Install the tools with [Homebrew](https://brew.sh), then create and start
Podman's Linux VM:

```bash
brew install podman jq docker-compose
podman machine init
podman machine start
```

Get the practice apps. The lessons work in `~/practice`:

```bash
git clone https://github.com/Espad0/docker-fundamentals.git
mkdir -p ~/practice
cp -R docker-fundamentals/starter/hello-ai docker-fundamentals/starter/hello-model ~/practice/
```

## What is in this repository

| Folder | Contents |
|---|---|
| `docs/` | The course website: a home page and one page per lesson. Plain HTML, no build step. |
| `starter/` | The two practice apps as they are at the start of the labs |
| `solutions/` | The finished files of each lab, and the sheet-tool app of Lesson 7 |

## How it was made and tested

This course was written with Claude, Anthropic's AI model, in September and
October 2026. Every command that runs locally was run on one Mac before it
went into a lesson.

That Mac is "the test Mac" in the lessons: a Mac with an Apple M5 processor,
Podman 6.0.2 with its Linux VM in rootful mode, Docker Compose 5.5.1, and
for Lesson 7 kind 0.33.0 with Kubernetes 1.37.0.
Outputs, sizes and timings come from it, so yours will differ a little.

Some things were **not** run:

- The AWS and Cloudflare account steps in Lesson 6. They are written from the
  providers' documentation, checked on 28 September 2026.
- The AWS parts of Lesson 7: the production files need an EKS cluster. They
  were only checked against the local kind cluster without being applied.
- One Docker-only rule about volumes in Lesson 4. The test Mac has Podman only.
- Outputs of a rootless Podman machine, which is Podman's default.
- The install commands above. The test Mac already had the tools.

Versions move. Package versions, image sizes and base-image digests are from
autumn 2026.

## Corrections

If something is wrong or out of date, please open an issue or a pull request.
Each lesson is a single file, `docs/lesson-NN/index.html`.

## Licence

- Lesson text and diagrams: [CC BY 4.0](LICENSE-CONTENT.md)
- Code and configuration files: [MIT](LICENSE)
