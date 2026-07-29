---
name: docker-ci-cd-integration
description: "Use when using Docker in CI/CD pipelines."
category: docker
tags: [docker, cicd, github-actions, gitlab-ci, pipeline]
---
# Docker CI/CD Integration

Using Docker in CI/CD pipelines for build, test, and deploy.

## GitHub Actions

```yaml
# .github/workflows/docker.yml
name: Docker Build and Push

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=semver,pattern={{version}}
            type=sha,format=short

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          platforms: linux/amd64,linux/arm64
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## GitLab CI

```yaml
# .gitlab-ci.yml
variables:
  DOCKER_HOST: tcp://docker:2375
  DOCKER_TLS_CERTDIR: ""
  DOCKER_DRIVER: overlay2

services:
  - docker:dind

stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - docker compose -f docker-compose.test.yml up -d --wait
    - docker compose exec -T app npm test
    - docker compose down -v

build:
  stage: build
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker buildx create --use
    - docker buildx build --platform linux/amd64,linux/arm64
        -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
        -t $CI_REGISTRY_IMAGE:latest
        --push .
```

## Local CI Simulation

```powershell
# Run the same build locally
docker buildx build --platform linux/amd64 -t myapp:test .
docker compose -f docker-compose.test.yml up -d --wait
docker compose exec -T app npm test
docker compose down -v
```

## Docker-in-Docker (DinD) vs Docker-Outside-Docker (DooD)

```yaml
# DinD (run Docker inside Docker -- needs privileged)
services:
  docker:
    image: docker:dind
    privileged: true

# DooD (bind-mount host Docker socket -- no privileged mode)
runs-on: ubuntu-latest
services:
  docker:
    image: docker:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

## Caching Strategy

```yaml
# GitHub Actions: cache between runs
- uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max

# Self-hosted: registry cache
  with:
    cache-from: type=registry,ref=myrepo/cache
    cache-to: type=registry,ref=myrepo/cache,mode=max

# Local: filesystem cache
  with:
    cache-from: type=local,src=/tmp/.buildx-cache
    cache-to: type=local,dest=/tmp/.buildx-cache
```

## Testing in CI

```yaml
# Service containers in CI
jobs:
  test:
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_PASSWORD: testpass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - run: npm test
        env:
          DB_URL: postgres://postgres:testpass@postgres:5432/postgres
```

## Pitfalls

- **DinD** needs `privileged: true` -- security risk; prefer DooD when possible
- **Cache registry** needs `mode=max` to cache multi-stage build layers
- **GitHub Actions** cache has 10GB limit per repo -- rotate regularly
- **Docker socket mounting** gives container root access to host -- restrict carefully
- **Matrix builds** for multi-arch can be separate jobs or one multi-platform build
