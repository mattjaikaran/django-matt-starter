# Architecture

## Stack

- Django with django-matt for routing, JWT auth and OpenAPI generation.
- Granian as the ASGI server (`granian>=2.0.0`).
- PostgreSQL in production; SQLite when `USE_SQLITE=True`.
- Pydantic schemas for request and response validation.
- Pytest with pytest-django for tests.

## Layout

```
apps/
├── api.py                 # DjangoMattAPI instance and route registration
├── core/
│   ├── models.py          # shared base models
│   └── management/commands/seed_data.py
└── users/
    ├── admin.py
    ├── models/user.py     # email-based custom user
    ├── schemas/           # Pydantic request/response models
    └── controllers/       # AuthController and route registration
config/
├── settings.py            # environment-driven Django settings
├── test_settings.py       # forces SQLite for tests
├── urls.py                # admin and /api/ mount
├── migration_lint.py      # django-safe-migrations exceptions
└── wsgi.py, asgi.py
scripts/
├── db/                    # migration graph, check, renumber
├── check_file_length.py
└── check_agents_docs.py
tests/
```

## Request flow

`config/urls.py` mounts the django-matt API under `/api/`. `apps/api.py` builds
the API instance, registers auth routes from `apps/users/controllers/routes.py`,
and defines the `health` and `protected` endpoints.

Controllers are async and raise `APIError` or `ValidationAPIError` from
django-matt, which the framework turns into JSON error responses. Schemas in
`apps/users/schemas/` validate request bodies and serialize responses. Models
stay in `models/` and use Django's async ORM methods (`aget`, `acreate`,
`aexists`) inside controllers.

## Adding an endpoint

1. Add or extend a Pydantic schema in `apps/<app>/schemas/`.
2. Add an async controller method in `apps/<app>/controllers/`.
3. Register the route in that app's `routes.py`.
4. Add a test under `tests/`.

## Settings

`config/settings.py` reads environment variables through `python-dotenv`.
Secrets and deployment values come from `.env` locally and from the environment
in production. `config/test_settings.py` sets `USE_SQLITE=true` before importing
the base settings, so the test suite never needs PostgreSQL.

## Migrations

The migration graph is linear. `scripts/db/check_migrations.py` refuses merge
migrations and multiple leaves, and `scripts/db/renumber_migrations.py` renames
a branch's migrations after the latest migration on `main`. Rules and the
conflict procedure live in `AGENTS.md` and `.claude/skills/migrations/`.
