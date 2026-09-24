---
name: docker-compose-workflows
description: Multi service local dev with Docker Compose networking volumes
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [docker, compose, workflows]
---

# Docker Compose Workflows

## Basic Setup
```yaml
version: "3.8"
services:
  app:
    build: .
    ports: ["8000:8000"]
    volumes: [".:/app"]
    depends_on: [db]
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: myapp
```

## Commands
```bash
docker compose up -d        # Start
docker compose logs -f      # Follow logs
docker compose down -v      # Stop + remove volumes
docker compose restart      # Restart services
```

## Trigger

Activate this skill when the user mentions:
- docker, compose, workflows workflows or issues
- Building, fixing, or optimizing docker compose workflows


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
