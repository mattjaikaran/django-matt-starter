# Developer commands.
#
# Each recipe except `help` and `setup` calls the Makefile target of the same
# name, so there is one implementation. mattstack exposes every recipe as
# `just backend-<recipe>`.

set shell := ["bash", "-cu"]

# The virtualenv's tools (ruff, mypy, pytest) come first on PATH, so recipes
# work without activating it; a missing .venv leaves PATH unchanged.

export PATH := justfile_directory() + "/.venv/bin:" + env("PATH", "")

# List the recipes
help:
    @just --list

# Create the virtualenv, install dev dependencies and copy .env.example
setup:
    uv venv
    @make dev
    test -f .env || cp .env.example .env

# Install runtime dependencies
install:
    @make install

# Install dev dependencies
dev:
    @make dev

# Run the development server on port 8000
run:
    @make run

# Run pytest with coverage
test:
    @make test

# Run Ruff and mypy
lint:
    @make lint

# Format with Ruff
format:
    @make format

# Generate and apply migrations
migrate:
    @make migrate

# Check migration leaves, safety and merges
migrations-check:
    @make migrations-check

# Preview migration renames; --apply writes them
migrations-renumber *args:
    @make migrations-renumber ARGS="{{ args }}"

# Validate AGENTS.md and the skills
agents-check:
    @make agents-check

# Create a superuser
superuser:
    @make superuser

# Open the Django shell
shell:
    @make shell

# Export TypeScript types to ../frontend/src/types
sync-types:
    @make sync-types

# Start PostgreSQL and Redis
docker-up:
    @make docker-up

# Start the full compose stack
docker-up-all:
    @make docker-up-all

# Stop the compose stack
docker-down:
    @make docker-down

# Start the dev compose profile
docker-dev:
    @make docker-dev

# Build the API image
docker-build:
    @make docker-build

# Follow compose logs
docker-logs:
    @make docker-logs

# Remove caches and build output
clean:
    @make clean
