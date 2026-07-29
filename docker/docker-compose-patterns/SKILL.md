---
name: docker-compose-patterns
description: "Use when orchestrating multi-service Docker environments."
category: docker
tags: [docker, compose, orchestration, yaml]
---

# Docker Compose Patterns

Common, production-grade Docker Compose patterns for dev environments and multi-service architectures.

## Basic Structure

```yaml
version: "3.9"
services:
  app:
    build: .
    ports: ["3000:3000"]
    volumes: [".:/app", "/app/node_modules"]
    depends_on: { db: { condition: service_healthy } }
  db:
    image: postgres:16-alpine
    volumes: ["pgdata:/var/lib/postgresql/data"]
    healthcheck: { test: ["CMD-SHELL", "pg_isready"], interval: 10s }
volumes: { pgdata: }
```

## Profiles

```yaml
services:
  app: { profiles: ["base", "dev", "prod"] }
  mailhog: { profiles: ["dev"] }
  prometheus: { profiles: ["monitoring"] }
# docker compose --profile dev up -d
```

## DRY Anchors

```yaml
x-logging: &log { driver: "json-file", options: { max-size: "10m" } }
services:
  web: { image: nginx, logging: *log }
  api: { image: myapi, logging: *log }
```

## Init Containers

```yaml
services:
  app: { image: myapp, depends_on: [db-migrate] }
  db-migrate:
    image: myapp; entrypoint: ["npm", "run", "migrate"]
    depends_on: { db: { condition: service_healthy } }
```

## Networks

```yaml
services:
  api: { networks: [frontend, backend] }
  db: { networks: [backend] }
networks:
  frontend: {}
  backend: { internal: true }
```

## Commands

```powershell
docker compose up -d --build
docker compose down -v --rmi all
docker compose logs -f; docker compose exec app bash
docker compose run --rm app npm test
docker compose config; docker compose build --parallel
```

## Pitfalls

- **depends_on** waits for start, not readiness — use `condition: service_healthy`
- **$VAR** in compose — escape with `$$` for literal `$`
- **.env** is auto-loaded — don't commit it
- **v2** is current; v1 (docker-compose) deprecated
