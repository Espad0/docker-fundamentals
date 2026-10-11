# Solutions

The finished files of each lab. The same solutions are on the lesson pages,
behind the "Show solution" buttons. Try the lab first.

| Folder | Files |
|---|---|
| `lesson-02` | `Containerfile` and `.containerignore` for hello-ai |
| `lesson-03` | The production `Containerfile`, and `main.py` with the API key setting |
| `lesson-04` | hello-ai with a Postgres database: `main.py`, `requirements.txt`, `Containerfile`, `compose.yaml`, `compose.override.yaml` |
| `lesson-05` | `Containerfile` for hello-model |
| `lesson-06` | `.gitlab-ci.yml` and the `cloudflare` folder |
| `lesson-07` | The Kubernetes file, and the version that runs locally with `podman kube play` |

The `FROM` lines pin the base image by a digest from late September 2026.
Lesson 3 shows how to look up the current one.
