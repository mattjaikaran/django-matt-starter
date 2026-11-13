# Commands

All commands run from the repository root. `just help` lists the recipes and
`make help` the targets. Each recipe except `just help` and `just setup` puts
`.venv/bin` first on `PATH` and calls the Makefile target of the same name, so
either runner runs the same command; mattstack exposes each recipe as
`backend-<recipe>`.

## Prerequisites

- Python 3.12+; CI runs 3.14.
- [uv](https://github.com/astral-sh/uv).
- SSH access to `github.com/mattjaikaran/django-matt`. The dependency in
  `pyproject.toml` uses a `git+ssh` URL, so installs fail without a key that
  GitHub accepts. CI injects `SSH_PRIVATE_KEY`.
- PostgreSQL 16, or `USE_SQLITE=True` in `.env`. Redis is optional: the compose
  stack runs it, but the current settings do not require it.

## Clean checkout

```bash
just setup
source .venv/bin/activate
just migrate
just run
```

`just install` installs runtime dependencies only; `just setup` creates the
virtualenv, installs the `dev` extras (pytest, Ruff, mypy, django-stubs,
django-safe-migrations) and copies `.env.example` to `.env` when it is missing.

## Recipes

| Recipe | Runs |
| --- | --- |
| `just setup` | `uv venv`, `just dev`, then `.env.example` to `.env` when missing |
| `just install` | `uv pip install -e .` |
| `just dev` | `uv pip install -e ".[dev]"` |
| `just run` | `python manage.py runserver` |
| `just test` | pytest with `--cov=apps` |
| `just lint` | `ruff check .` and `mypy apps/` |
| `just format` | `ruff format .` and `ruff check --fix .` |
| `just migrate` | `makemigrations` then `migrate` |
| `just migrations-check` | leaf, safety and no-merge checks |
| `just migrations-renumber` | dry run; add `--apply` to rename |
| `just agents-check` | validate `AGENTS.md` and the skills |
| `just superuser` | `createsuperuser` |
| `just shell` | Django shell |
| `just sync-types` | export TypeScript types to `../frontend/src/types` |
| `just docker-up` | PostgreSQL and Redis in Docker |
| `just docker-up-all` | the full compose stack |
| `just docker-dev` | the `dev` compose profile with hot reload |
| `just docker-build` | build the API image |
| `just docker-logs` | follow compose logs |
| `just docker-down` | stop the compose stack |
| `just clean` | remove caches and build output |

## CI

`.github/workflows/ci.yml` runs on pushes to `main` and `develop`, and on pull
requests. A draft PR runs nothing: marking it ready for review starts the run.
On a PR, a docs-only diff (Markdown, `docs/`, `tasks/specs/`) runs only the
Changes and Agent docs jobs; Lint, Test, Type Check and Migrations wait for a
non-docs change. A newer push cancels the older PR run. Job names are
unchanged, so required status checks keep working.

## Factory runs

The factory gives each run its own git worktree, added from the primary clone
with `git worktree add -B <branch> <path> origin/<branch>`. Git refuses that
command while the branch is checked out somewhere else, so the run ends with
`fatal: '<branch>' is already used by worktree at '<path>'` and exit 1. Two
states cause it:

- The primary clone sits on the PR branch: leave it on `main`.
- A deleted worktree is still registered and holds the branch: `git worktree
  list` shows it.

Either state is cleared in the primary clone, and the same command then
succeeds:

```bash
git -C <primary> switch main
git -C <primary> worktree prune
```

## Tests

`just test` uses `config.test_settings`, which forces `USE_SQLITE=true`, so no
database container is needed. CI runs the same suite with PostgreSQL.

## Migrations

`just migrations-check` runs `scripts/db/check_migrations.py`: it detects merge
migrations, checks for multiple leaf nodes, and runs django-safe-migrations
against the configured base. The check needs the Django environment, so it runs
with the `dev` dependencies installed.
