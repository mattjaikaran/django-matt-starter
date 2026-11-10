# Testing

## Running

```bash
make test
# equivalently
pytest -v --cov=apps --cov-report=term-missing
```

`config/test_settings.py` sets `USE_SQLITE=true` before importing the base
settings, so tests use SQLite and do not need a database container. CI runs the
same suite against PostgreSQL 16.

## Layout and fixtures

- Tests live in `tests/`, one module per feature (for example `test_auth.py`).
- `tests/conftest.py` provides `client`, `user` and `admin_user` fixtures.
- Use `@pytest.mark.django_db` for tests that touch the database.
- pytest-asyncio runs in `auto` mode; async tests need no marker.

## What to test

- New or changed behavior needs a test that fails before the change and passes
  after it.
- Cover the boundary: status codes, response fields, validation errors and
  permission checks.
- Prefer the Django test client and real URLs over calling controllers directly.

## Coverage

`make test` reports coverage for `apps/`. There is no enforced threshold; keep
new code covered by the tests that exercise it.
