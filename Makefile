.PHONY: help up down build logs shell-api shell-web db-migrate db-upgrade db-downgrade test lint format

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ---------------------------------------------------------------------------
# Docker
# ---------------------------------------------------------------------------
up: ## Start all services
	docker compose up -d

up-build: ## Build and start all services
	docker compose up -d --build

down: ## Stop all services
	docker compose down

down-v: ## Stop all services and remove volumes
	docker compose down -v

build: ## Build all images
	docker compose build

logs: ## Tail logs for all services
	docker compose logs -f

logs-api: ## Tail API logs
	docker compose logs -f api

logs-web: ## Tail frontend logs
	docker compose logs -f web

# ---------------------------------------------------------------------------
# Shell access
# ---------------------------------------------------------------------------
shell-api: ## Open shell in API container
	docker compose exec api bash

shell-web: ## Open shell in frontend container
	docker compose exec web sh

shell-db: ## Open psql shell
	docker compose exec postgres psql -U adforge -d adforge

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
db-migrate: ## Create a new Alembic migration (usage: make db-migrate msg="add users table")
	docker compose exec api alembic revision --autogenerate -m "$(msg)"

db-upgrade: ## Apply all pending migrations
	docker compose exec api alembic upgrade head

db-downgrade: ## Rollback last migration
	docker compose exec api alembic downgrade -1

db-reset: ## Drop and recreate the database
	docker compose down -v
	docker compose up -d postgres redis
	sleep 3
	docker compose up -d api
	sleep 2
	$(MAKE) db-upgrade

# ---------------------------------------------------------------------------
# Testing & Quality
# ---------------------------------------------------------------------------
test: ## Run backend tests
	docker compose exec api pytest -v

test-cov: ## Run tests with coverage
	docker compose exec api pytest --cov=app --cov-report=html -v

lint: ## Lint backend code
	docker compose exec api ruff check app/

format: ## Format backend code
	docker compose exec api ruff format app/
