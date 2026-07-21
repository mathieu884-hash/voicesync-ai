.PHONY: help build up down logs test lint format clean migrate seed

# Variables
PROJECT_NAME=voicesync-ai
BACKEND_DIR=backend
FRONTEND_DIR=frontend

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker images
	docker-compose build

up: ## Start all containers
	docker-compose up -d
	echo "Application is running at http://localhost:3000"
	echo "API Docs at http://localhost:8000/docs"

down: ## Stop all containers
	docker-compose down

restart: ## Restart all containers
	docker-compose restart

logs: ## View logs from all services
	docker-compose logs -f

logs-backend: ## View backend logs
	docker-compose logs -f backend

logs-frontend: ## View frontend logs
	docker-compose logs -f frontend

ps: ## List running containers
	docker-compose ps

shell-backend: ## Access backend shell
	docker-compose exec backend bash

shell-frontend: ## Access frontend shell
	docker-compose exec frontend bash

shell-db: ## Access database shell
	docker-compose exec db psql -U voicesync_user -d voicesync_db

migrate: ## Run database migrations
	docker-compose exec backend python -m alembic upgrade head

migrate-create: ## Create new migration
	docker-compose exec backend python -m alembic revision --autogenerate -m "$(name)"

migrate-downgrade: ## Downgrade last migration
	docker-compose exec backend python -m alembic downgrade -1

seed: ## Seed database with sample data
	docker-compose exec backend python scripts/seed_db.py

test: ## Run tests
	docker-compose exec backend pytest

test-backend: ## Run backend tests
	docker-compose exec backend pytest $(BACKEND_DIR)

test-frontend: ## Run frontend tests
	docker-compose exec frontend npm test

test-coverage: ## Run tests with coverage report
	docker-compose exec backend pytest --cov=$(BACKEND_DIR) --cov-report=html

lint: ## Run linters
	docker-compose exec backend pylint $(BACKEND_DIR)
	docker-compose exec frontend npm run lint

format: ## Format code
	docker-compose exec backend black $(BACKEND_DIR)
	docker-compose exec backend isort $(BACKEND_DIR)
	docker-compose exec frontend npm run format

clean: ## Clean up
	docker-compose down -v
	rm -rf backend/__pycache__ backend/.pytest_cache
	rm -rf frontend/node_modules frontend/.next

install-hooks: ## Install git hooks
	pre-commit install

update-deps: ## Update dependencies
	$(BACKEND_DIR)/update_deps.sh
	$(FRONTEND_DIR)/npm update

requirements: ## Generate requirements.txt
	docker-compose exec backend pip freeze > $(BACKEND_DIR)/requirements.txt

data-export: ## Export database to SQL file
	docker-compose exec db pg_dump -U voicesync_user voicesync_db > backup_$(shell date +%Y%m%d_%H%M%S).sql

data-import: ## Import SQL file to database
	docker-compose exec -T db psql -U voicesync_user voicesync_db < $(FILE)

prod-up: ## Start production environment
	docker-compose -f docker-compose.prod.yml up -d

prod-down: ## Stop production environment
	docker-compose -f docker-compose.prod.yml down

prune: ## Remove unused Docker images/volumes
	docker system prune -a

stats: ## Show Docker stats
	docker stats
