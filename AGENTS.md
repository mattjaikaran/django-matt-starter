# AGENTS.md

Instructions for coding agents. Read this file first; the nearest `AGENTS.md` wins.

## Project overview

`django-matt-starter` ("myproject") is a minimal Django API template built on
[django-matt](https://github.com/mattjaikaran/django-matt).

- `apps/users/` — email-based user model, JWT auth controllers, Pydantic schemas.
- `apps/core/` — shared models and the `seed_data` management command.
- `config/` — settings, URL config, WSGI/ASGI entry points, migration lint rules.
- `scripts/` — repository checks: migrations, file length, agent docs.
- `tests/` — pytest suite.

Request flow and module boundaries: [docs/architecture.md](docs/architecture.md).

## Setup and commands

Prerequisites: Python 3.12+ (CI uses 3.14), [uv](https://github.com/astral-sh/uv),
and SSH access to the private `django-matt` dependency. PostgreSQL is optional
when `USE_SQLITE=True`.

| Command | Purpose |
| --- | --- |
| `uv venv && make dev` | Create the virtualenv and install dev dependencies |
| `cp .env.example .env` | Local environment settings |
| `make migrate` | `makemigrations`, then `migrate` |
| `make run` | Development server on port 8000 |
| `make test` | pytest with coverage |
| `make lint` | Ruff and mypy |
| `make format` | Ruff format and autofix |
| `make migrations-check` | Leaf, safety and no-merge checks |
| `make migrations-renumber ARGS=--apply` | Rename a conflicting migration |
| `make agents-check` | Validate this file and the skills |
| `make docker-up` / `make docker-down` | PostgreSQL and Redis containers |

All commands run from the repository root. Install notes and the full target
list: [docs/commands.md](docs/commands.md).

## Code standards

- Follow the Ruff configuration in `pyproject.toml` (line length 100,
  `E,F,I,N,W,UP`) and keep `mypy apps/` clean.
- Keep Python files under 400 lines; pre-commit enforces this.
- One concern per module: `models/`, `schemas/`, `controllers/`. Register routes
  from `apps/api.py`, not in URL configuration.
- Use type hints and Pydantic schemas at API boundaries; controllers are async.
- Details: [docs/code-standards.md](docs/code-standards.md).

## Testing

- Run `make test` before pushing.
- Tests use pytest and `config.test_settings`; add tests under `tests/`.
- A behavior change needs a test that fails before the change and passes after.
- Fixtures and coverage: [docs/testing.md](docs/testing.md).

## Git and commits

- Conventional Commits: `type(scope): Imperative summary`.
- Subject at most 50 characters; body wrapped at 72.
- Work on a branch; never commit directly to `main`.
- Install hooks once with `pre-commit install`.

## Spec workflow (agent-run)

- Specs live in `tasks/specs/<issue>.md` and list **Files owned** plus the
  verification gate for the run.
- An agent edits only the files its spec owns. If a required change falls
  outside that list, stop and report it.
- Format and example: [tasks/specs/README.md](tasks/specs/README.md).

## Migrations

- Migrations are linearized, never merged. **Never run `makemigrations --merge`**
  and never add a merge migration.
- Never edit a migration that is already on `main`; add a new migration instead.
- After changing a model or migration, run `make migrations-check` before pushing.
- On a conflict (two leaf nodes, or a number reused from `main`), run
  `make migrations-renumber`, then `make migrations-renumber ARGS=--apply`.
  Procedure: [.claude/skills/migrations/SKILL.md](.claude/skills/migrations/SKILL.md).
- When the tool prints `escalate to owner` (`RunPython`, `RunSQL`, `RemoveField`,
  `RenameField`, `DeleteModel`, `replaces`, or a clashing `AlterField`), stop and
  report the exact output.
- Exceptions for django-safe-migrations go in `config/migration_lint.py`;
  accepted findings sit in `scripts/baselines/migration-safety.json`. Inline
  `# safe-migrations: ignore` comments are banned.

## Skills

- Skills live in `.claude/skills/<name>/SKILL.md` with `name` and `description`
  frontmatter, so only the description loads until the skill is used.
- Keep one skills location. Add `.agents/skills` only as a symlink when another
  tool requires it.

## Security

- Never commit secrets or real credentials. `.env` is gitignored; document new
  variables in `.env.example`.
- The `detect-private-key` and `no-commit-to-branch` pre-commit hooks enforce
  the hard rules; do not disable them.
- Production requires `DEBUG=False` and an explicit `ALLOWED_HOSTS`.
