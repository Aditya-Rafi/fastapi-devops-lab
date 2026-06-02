PYTHON ?= $(shell if [ -x .venv/bin/python ]; then echo .venv/bin/python; else echo python3; fi)
PIP ?= $(PYTHON) -m pip

.PHONY: help build test test-int lint coverage up down clean

help:
	@echo "Available commands:"
	@echo "  make build          - Build Docker image"
	@echo "  make test           - Run unit tests"
	@echo "  make test-int       - Run integration tests with docker-compose"
	@echo "  make lint           - Run linting checks"
	@echo "  make coverage       - Run unit tests with coverage"
	@echo "  make up             - Start docker-compose stack"
	@echo "  make down           - Stop docker-compose stack"
	@echo "  make clean          - Clean build artifacts and cache"

build:
	docker build -t lab-devopsapp:latest .

test:
	$(PIP) install -r requirements-dev.txt
	$(PYTHON) -m pytest tests/unit -v

test-int:
	RUN_INTEGRATION_TESTS=true $(PYTHON) -m pytest tests/integration -v

lint:
	$(PIP) install -r requirements-dev.txt
	$(PYTHON) -m ruff check apps tests

coverage:
	$(PIP) install -r requirements-dev.txt
	$(PYTHON) -m pytest tests/unit --cov=apps --cov-report=term-missing

up:
	docker compose up -d

down:
	docker compose down

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .ruff_cache .mypy_cache .coverage htmlcov
	docker compose down 2>/dev/null || true
