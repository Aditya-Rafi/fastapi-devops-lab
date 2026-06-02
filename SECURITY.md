# Security Policy

## Supported Versions

This repository tracks the `main` branch as the supported development line.
Security fixes should be applied to `main` first and released through the
standard CI/CD pipeline.

## Reporting a Vulnerability

Do not open a public issue for sensitive security findings.

Send a private report to the repository maintainer with:

- Affected component or endpoint
- Reproduction steps
- Expected and observed impact
- Suggested remediation, if available

## Security Controls

- Containers run as a non-root user.
- Docker images are built with a multi-stage Dockerfile.
- CI runs unit tests, integration tests, lint checks, image build validation,
  and container vulnerability scanning.
- Application configuration is read from environment variables.
- Secrets must be provided through GitHub Actions secrets or runtime secret
  stores, not committed into the repository.
