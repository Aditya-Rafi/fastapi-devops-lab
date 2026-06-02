# Contributing Guide

Thank you for contributing to Lab DevOpsApp. This project is maintained as a
DevOps learning and reference repository, so changes should keep the application
small, reproducible, and easy to operate.

## Development Setup

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Start the local stack:

```bash
docker compose up -d --build
```

## Quality Gates

Run these checks before opening a pull request:

```bash
make lint
make test
make test-int
```

Optional coverage report:

```bash
make coverage
```

## Pull Request Guidelines

- Keep changes focused and easy to review.
- Do not commit generated files, virtual environments, caches, or secrets.
- Update documentation when behavior, commands, or deployment steps change.
- Add or update tests for behavior changes.
- Keep Docker and CI changes reproducible in a fresh environment.

## Commit Messages

Use clear, conventional-style commit messages:

```text
feat: add readiness endpoint
fix: return proper health check status code
test: cover unhealthy dependency response
ci: add image scanning workflow
docs: update deployment guide
```

## Secrets

Never commit real credentials. Use one of these instead:

- `.env` for local-only development values
- GitHub Actions secrets for CI/CD
- Platform secret stores for production runtime

## Release Notes

When preparing a release:

1. Update `CHANGELOG.md`.
2. Build and test the image.
3. Push to `main`.
4. Let GitHub Actions publish the Docker image when Docker Hub secrets exist.
