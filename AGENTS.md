# Django Matt Starter

Backend guidance for coding agents. Read it before a non-trivial change.
Cross-stack rules (branches, commits, secrets, harness adapters) live in the
root `AGENTS.md`; this file holds what is true of this backend alone.

## Stack

- Django with [django-matt](https://github.com/mattjaikaran/django-matt) for
  routing, JWT auth and OpenAPI.
- Granian as the ASGI server (`granian>=2.0.0`).
- PostgreSQL in production; SQLite when `USE_SQLITE=True`.
- Pydantic schemas for request and response validation.
- Pytest with pytest-django; Python 3.12+ (CI uses 3.14); uv for dependencies.
- `just` runs every command; `just help` lists the recipes. Each recipe puts
  `.venv/bin` first on `PATH` and calls the `Makefile` target of the same name,
  so `make` still works and mattstack exposes each recipe as `backend-<recipe>`.

## Layout and layers

- `apps/users/` — email-based user model, `models/`, `schemas/`, `controllers/`.
- `apps/core/` — shared models and the `seed_data` command.
- `config/` — settings, URL config, ASGI/WSGI entry points, migration lint rules.
- `scripts/` — repository checks: migrations, file length, agent docs.
- `tests/` — pytest suite.
- One concern per module: `models/`, `schemas/`, `controllers/`. Register routes
  from `apps/api.py`, never in URL configuration.
- Controllers are async and validate with Pydantic schemas at the API boundary.
- Request flow and module boundaries: [docs/architecture.md](docs/architecture.md).

## Commands

All commands run from the repository root.

| Command | Purpose |
| --- | --- |
| `just setup` | Create the virtualenv, install dev dependencies and copy `.env.example` to `.env` when missing |
| `just run` | Development server on port 8000 |
| `just test` | pytest with coverage |
| `just lint` | Ruff and mypy |
| `just format` | Ruff format and autofix |
| `just migrate` | `makemigrations`, then `migrate` |
| `just migrations-check` | Leaf, safety and no-merge checks |
| `just migrations-renumber` | Preview a migration rename; add `--apply` to write it |
| `just agents-check` | Validate this file and the skills |
| `just docker-up` / `just docker-down` | PostgreSQL and Redis containers |

Install notes, the full recipe list and CI: [docs/commands.md](docs/commands.md).

## Code standards

- Follow the Ruff configuration in `pyproject.toml` (line length 100,
  `E,F,I,N,W,UP`) and keep `mypy apps/` clean.
- Keep Python files under 400 lines; pre-commit enforces this.
- Use type hints, Pydantic schemas at API boundaries, and async controllers.
- Production requires `DEBUG=False` and an explicit `ALLOWED_HOSTS`.
- Details: [docs/code-standards.md](docs/code-standards.md).

## Gates

- Run `just format` before a commit; run `just lint` and `just test` before
  pushing.
- A behavior change needs a test that fails before the change and passes after.
- Fixtures and coverage: [docs/testing.md](docs/testing.md).

## Migrations

- Migrations are linearized, never merged. **Never run `makemigrations --merge`**
  and never add a merge migration.
- Never edit a migration that is already on `main`; add a new migration instead.
- After changing a model or migration, run `just migrations-check` before pushing.
- On a conflict (two leaf nodes, or a number reused from `main`), run
  `just migrations-renumber`, then `just migrations-renumber --apply`.
  Procedure: [.claude/skills/migrations/SKILL.md](.claude/skills/migrations/SKILL.md).
- When the tool prints `escalate to owner` (`RunPython`, `RunSQL`, `RemoveField`,
  `RenameField`, `DeleteModel`, `replaces`, or a clashing `AlterField`), stop and
  report the exact output.
- Exceptions for django-safe-migrations go in `config/migration_lint.py`;
  accepted findings sit in `scripts/baselines/migration-safety.json`. Inline
  `# safe-migrations: ignore` comments are banned.
