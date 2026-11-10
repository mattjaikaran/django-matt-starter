---
name: migrations
description: Resolve Django migration conflicts and verify model changes. Use when adding migrations or when make migrations-check reports a leaf, merge or safety failure.
---

# Migrations

Read the Migrations section of `AGENTS.md` first; it defines the rules this
procedure follows.

## Verify a model change

1. Run `make migrate` to generate and apply the new migration.
2. Run `make migrations-check`.
3. Stop when the check passes.

## Resolve a conflict

1. Run `make migrations-renumber` and review the planned renames.
2. Run `make migrations-renumber ARGS=--apply`.
3. Run `make migrations-check` again.
4. If the output contains `escalate to owner`, stop and report the exact output.

## Failure notes

- Multiple leaf nodes: run the conflict procedure above.
- django-safe-migrations: apply the safe pattern the tool prints.
- Missing django-safe-migrations: install the dev extras with `make dev`.
