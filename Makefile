.PHONY: help install dev test lint format migrate run docker-up docker-down clean migrations-check migrations-renumber agents-check

# Default target
help:
	@echo "Available commands:"
	@echo "  make install     - Install dependencies with uv"
	@echo "  make dev         - Install dev dependencies"
	@echo "  make run         - Run development server"
	@echo "  make test        - Run tests"
	@echo "  make lint        - Run linter"
	@echo "  make format      - Format code"
	@echo "  make migrate     - Run migrations"
	@echo "  make migrations-check - Leaf, lint and no-merge checks"
	@echo "  make migrations-renumber - Fix a migration conflict (ARGS=--apply)"
	@echo "  make agents-check - Validate AGENTS.md and skills"
	@echo "  make docker-up   - Start Docker containers"
	@echo "  make docker-down - Stop Docker containers"
	@echo "  make clean       - Clean up generated files"

# Install dependencies
install:
	uv pip install -e .

# Install dev dependencies
dev:
	uv pip install -e ".[dev]"

# Run development server
run:
	python manage.py runserver

# Run tests
test:
	pytest -v --cov=apps --cov-report=term-missing

# Run linter
lint:
	ruff check .
	mypy apps/

# Format code
format:
	ruff format .
	ruff check --fix .

# Database migrations
migrate:
	python manage.py makemigrations
	python manage.py migrate

# Migrations are linearized, never merged: never `makemigrations --merge`.
migrations-check:
	python3 scripts/db/check_migrations.py

# Dry run; `make migrations-renumber ARGS=--apply` writes the renames.
migrations-renumber:
	python3 scripts/db/renumber_migrations.py $(ARGS)

# Agent docs: AGENTS.md links, CLAUDE.md import, skill frontmatter.
agents-check:
	python3 scripts/check_agents_docs.py

# Create superuser
superuser:
	python manage.py createsuperuser

# Docker commands
docker-up:
	docker compose up -d db redis

docker-up-all:
	docker compose up -d

docker-down:
	docker compose down

docker-dev:
	docker compose --profile dev up

docker-build:
	docker compose build

docker-logs:
	docker compose logs -f

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf *.egg-info/

# Generate types for frontend
sync-types:
	python manage.py sync_types --target typescript --output ../frontend/src/types

# Shell
shell:
	python manage.py shell
