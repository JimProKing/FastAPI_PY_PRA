## Quick orientation for AI coding agents

This repository appears to be a FastAPI learning/practice project. The key places to inspect are:

- Project root: [README.md](README.md)
- Example Python lessons: [ch02](ch02)
- Docker setup: [ch04_Docker_Image/Dockerfile](ch04_Docker_Image/Dockerfile) and [ch04_Docker_Image/docker-compose.yaml](ch04_Docker_Image/docker-compose.yaml)

Purpose: small tutorial examples (printed demos in `ch02`) plus an attempted containerized FastAPI app under `ch04_Docker_Image`. Several files referenced by the Dockerfile (e.g. `pyproject.toml`, `api/main.py`) are not present — treat them as intentionally-missing scaffolding when implementing app features.

What the agent should know and do first

- Read the simple examples in `ch02/01_BASIC/*` to learn repo coding style (scripts print to stdout; no tests or packages).
- Verify presence of packaging files before changing Docker-related code: look for `pyproject.toml` and `poetry.lock` at repo root. If missing, prompt the user before creating them.
- Search for an `api` package or `main.py`. The Dockerfile expects an ASGI app at `api.main:app`. If absent, create `api/__init__.py` and `api/main.py` with a minimal FastAPI app and clear TODO comments.

Dev/build/run patterns (concrete commands)

- Run small examples locally:

```bash
python3 ch02/01_BASIC/animal.py
python3 ch02/01_BASIC/dog.py
```

- Expected (intended) application workflow when `pyproject.toml` + `api.main` exist:

```bash
# install (poetry-managed project)
poetry install

# dev server (intended command from Dockerfile)
poetry run uvicorn api.main:app --host 0.0.0.0 --reload
```

- Docker (intended):

```bash
docker-compose up --build
# or
docker build -t fastapi-pra . && docker run -p 8000:8000 fastapi-pra
```

Notes about discovered issues (agents should validate these before applying fixes)

- `ch04_Docker_Image/Dockerfile` contains multiple likely typos and brittle patterns:
  - `COPY pyproject.toml*poetry.lock*./` is invalid syntax; expect `COPY pyproject.toml poetry.lock ./`.
  - `RUN if [-f pyproject.toml]; then ... fi` lacks spaces in the `[` test and will fail in POSIX shells; expect `if [ -f pyproject.toml ]; then ... fi`.
  - ENTRYPOINT uses `unicorn` (typo) instead of `uvicorn` and passes `api.main:app` — verify `api/main.py` exists.

- `ch04_Docker_Image/docker-compose.yaml` has `volumns` typo and a `.dockervenv` path — double-check volume names and intended mount points.

Project-specific conventions and patterns

- The `ch02` folder contains numbered, self-contained scripts used for teaching; prefer lightweight, single-file edits when working here.
- The repository currently favors creating a poetry-managed project when containerizing; do not convert to other managers unless the user asks.
- There are no tests or CI configs found — when adding tests, keep them isolated in a new `tests/` folder and follow simple pytest conventions.

Integration points to be careful about

- Dockerfile <-> `pyproject.toml`: Dockerfile assumes a poetry project; confirm versions and `virtualenvs.in-project` usage when adding files.
- Server entrypoint uses `api.main:app`: any new endpoints or routers should be registered in `api/main.py`.

When making changes, be conservative and explicit

- If files referenced by Dockerfile are missing, add minimal scaffolding with clear TODOs and comments, and notify the user.
- When fixing Dockerfile or compose typos, include a short note in the commit explaining the change and why it was necessary (e.g., fix `unicorn`→`uvicorn`).

Examples (what to add when scaffolding is required)

- Minimal `api/main.py` to create before running containers:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"ok": True}

# TODO: register routers here
```

Feedback request

If any of the above assumptions are incorrect (for example, you intend a different package layout or a different Python server), tell me which layout and I will update these instructions and the scaffolding accordingly.
