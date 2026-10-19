# FastAPI DevOps Lab

Production-oriented FastAPI service used to demonstrate practical DevOps patterns:
containerized application delivery, dependency health checks, reverse proxying,
automated tests, image scanning, and CI/CD with GitHub Actions.

## Architecture

```text
Client
  |
  v
Nginx :80
  |
  v
FastAPI :8000
  |-------- PostgreSQL :5432
  |-------- Redis :6379
```

## Features

- FastAPI application with `/` and `/health` endpoints
- PostgreSQL and Redis health validation
- Multi-stage Docker image build
- Non-root runtime container user
- Docker Compose stack for local integration testing
- Nginx reverse proxy
- Unit and integration tests
- Ruff linting
- GitHub Actions CI/CD pipeline
- Trivy container image scanning
- Dependabot configuration for dependencies and GitHub Actions

## Requirements

- Python 3.11+
- Docker Engine
- Docker Compose v2
- Make

## Quick Start

Start the full stack:

```bash
docker compose up -d --build
```

Check the application:

```bash
curl http://localhost/
curl http://localhost/health
```

Stop the stack:

```bash
docker compose down
```

## Local Development

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Run the application locally:

```bash
uvicorn apps.main:app --reload
```

For local runtime outside Docker, provide `DATABASE_URL`, `REDIS_HOST`, and
`REDIS_PORT` through your shell or a process manager.

## Make Targets

```bash
make help       # Show available commands
make build      # Build the application image
make lint       # Run Ruff lint checks
make test       # Run unit tests
make test-int   # Run Docker-based integration tests
make coverage   # Run unit tests with coverage output
make up         # Start Docker Compose stack
make down       # Stop Docker Compose stack
make clean      # Remove local caches and stop Compose stack
```

## Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Environment variables:

| Variable | Description | Default |
| --- | --- | --- |
| `DATABASE_URL` | PostgreSQL connection string | unset |
| `REDIS_HOST` | Redis hostname | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |
| `LOG_LEVEL` | Application log level placeholder | `info` |

## Health Checks

`GET /health` checks both Redis and PostgreSQL.

Healthy response:

```json
{
  "status": "healthy",
  "redis": "healthy",
  "database": "healthy"
}
```

If any dependency is unavailable, the endpoint returns HTTP `500`.

## CI/CD

The GitHub Actions pipeline runs on pushes and pull requests to `main`.

Pipeline stages:

1. Lint Python code with Ruff
2. Run unit tests
3. Run Docker Compose integration tests on `main`
4. Build the Docker image
5. Scan the image with Trivy
6. Publish the image to Docker Hub when secrets are configured

Required repository secrets for publishing:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

If the secrets are missing, the deploy job is skipped safely.

## Push to GitHub

Initialize and push the repository:

```bash
git init -b main
git add .
git commit -m "chore: prepare devops application repository"
git remote add origin git@github.com:<owner>/<repository>.git
git push -u origin main
```

Use the HTTPS remote instead if you do not use SSH:

```bash
git remote add origin https://github.com/<owner>/<repository>.git
```

## Project Structure

```text
.
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       └── ci.yml
├── apps/
│   └── main.py
├── nginx/
│   └── nginx.conf
├── tests/
│   ├── integration/
│   │   └── test_end_to_end.py
│   └── unit/
│       └── test_main.py
├── .dockerignore
├── .editorconfig
├── .env.example
├── .gitattributes
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── DEPLOYMENT.md
├── Dockerfile
├── LICENSE
├── Makefile
├── pyproject.toml
├── README.md
├── SECURITY.md
├── docker-compose.yml
├── requirements-dev.txt
└── requirements.txt
```

## Documentation

- [Deployment Guide](DEPLOYMENT.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [Changelog](CHANGELOG.md)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
