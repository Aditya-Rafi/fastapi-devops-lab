# Deployment Guide

This guide covers local deployment, CI/CD publishing, and production deployment
considerations for Lab DevOpsApp.

## Local Stack

Start all services:

```bash
docker compose up -d --build
```

Validate runtime health:

```bash
curl http://localhost/
curl http://localhost/health
```

Stop services:

```bash
docker compose down
```

Remove persistent local database data:

```bash
docker compose down -v
```

## Docker Image

Build the image:

```bash
docker build \
  --build-arg VERSION=0.1.0 \
  --build-arg BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
  --build-arg VCS_REF="$(git rev-parse --short HEAD 2>/dev/null || echo local)" \
  -t lab-devopsapp:0.1.0 .
```

Run the app container manually:

```bash
docker run --rm -p 8000:8000 \
  -e DATABASE_URL="postgres://postgres_user:postgres_password@host.docker.internal:5432/my_db" \
  -e REDIS_HOST="host.docker.internal" \
  -e REDIS_PORT="6379" \
  lab-devopsapp:0.1.0
```

## Testing

Run unit tests:

```bash
make test
```

Run integration tests:

```bash
make test-int
```

The integration test starts and stops the Docker Compose stack automatically.

## CI/CD

The GitHub Actions workflow is defined in `.github/workflows/ci.yml`.

Stages:

- Lint
- Unit tests
- Integration tests on `main`
- Docker image build
- Trivy image scan
- Docker Hub publish on `main`

Configure these GitHub repository secrets to publish images:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

Published tags:

- `<dockerhub-user>/lab-devopsapp:<git-sha>`
- `<dockerhub-user>/lab-devopsapp:latest`

## Production Configuration

Use runtime secrets or platform-managed secret stores for sensitive values.
Do not commit real credentials to `.env`, Compose files, or CI configuration.

Required runtime environment:

```text
DATABASE_URL=postgres://user:password@postgres-host:5432/database
REDIS_HOST=redis-host
REDIS_PORT=6379
```

## Kubernetes Example

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: lab-devopsapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: lab-devopsapp
  template:
    metadata:
      labels:
        app: lab-devopsapp
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
      containers:
        - name: app
          image: docker.io/example/lab-devopsapp:latest
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: lab-devopsapp-secrets
                  key: database-url
            - name: REDIS_HOST
              value: redis.default.svc.cluster.local
            - name: REDIS_PORT
              value: "6379"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 15
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
```

## Operations

Check service logs:

```bash
docker compose logs -f web
docker compose logs -f nginx
```

Check container health:

```bash
docker compose ps
```

Run a health request from inside the application container:

```bash
docker compose exec web python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8000/health').read().decode())"
```

## Troubleshooting

- If `/health` returns HTTP `500`, inspect Redis and PostgreSQL first.
- If Nginx returns a connection error, verify that `web` is healthy with
  `docker compose ps`.
- If CI deploy is skipped, verify that Docker Hub secrets are configured.
- If local `make` commands fail because of system Python restrictions, create
  `.venv` and rerun the command.
