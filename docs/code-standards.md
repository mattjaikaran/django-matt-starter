# Code standards

## Formatting and linting

- Ruff is the formatter and linter; configuration lives in `pyproject.toml`.
  Line length 100, target Python 3.12, rules `E,F,I,N,W,UP`.
- Run `make format` before committing and `make lint` before pushing.
- mypy runs over `apps/`. Keep annotations on public functions and controller
  methods.
- Python files must stay under 400 lines (`scripts/check_file_length.py`).

## Module boundaries

- `models/` holds Django models only; no request handling.
- `schemas/` holds Pydantic schemas for input validation and response shaping.
- `controllers/` holds async handlers and route registration.
- `config/` holds settings and URL wiring; business logic does not belong there.
- Shared helpers belong in `apps/core/`, not in a catch-all module.

## Django conventions

- Use the project's custom user model via `get_user_model()`, never the concrete
  `User` import for queries.
- Use Django's async ORM methods in async controllers.
- Raise django-matt `APIError` subclasses for expected failures; let unexpected
  exceptions surface.
- Imports are absolute from `apps` or `config`.

## Pre-commit

Install once with `pre-commit install`. Hooks run Ruff, the file-length check,
the migration no-merge check, and repository hygiene hooks. Do not bypass them
with `--no-verify`.
