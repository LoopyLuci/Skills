---
name: docker-compose-migration
description: "Use when migrating from v1 to v2 Docker Compose."
category: docker
tags: [docker, compose, migration, v1, v2]
---
# Docker Compose Migration

Migrating from Docker Compose v1 (docker-compose) to v2 (docker compose).

## Key Differences

| Aspect | v1 (docker-compose) | v2 (docker compose) |
|--------|--------------------|--------------------|
| Command | `docker-compose` (hyphen) | `docker compose` (space, plugin) |
| Python vs Go | Python | Go (built into Docker CLI) |
| Version | Deprecated | Current |
| `version:` field | Required | Ignored (v3.8 assumed) |
| `depends_on` | No health check wait | `condition: service_healthy` works |
| Build | `docker-compose build` | `docker compose build` |
| Logs | `docker-compose logs` | `docker compose logs` |

## Check Current Version

```powershell
# v1
docker-compose --version

# v2
docker compose version
```

## Migration Steps

### 1. Update scripts and aliases

```powershell
# Old (v1)
docker-compose up -d
docker-compose down -v

# New (v2)  
docker compose up -d
docker compose down -v

# Or create an alias
function docker-compose { docker compose @args }
```

### 2. Remove `version:` from compose files

```yaml
# OLD -- remove this line:
version: "3.8"

services:
  app:
    image: nginx
```

```yaml
# NEW -- no version needed
services:
  app:
    image: nginx
```

### 3. Use service_healthy in depends_on

```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "postgres"]
      interval: 5s
      timeout: 3s
      retries: 5
```

### 4. Update CI/CD pipelines

```yaml
# Old
docker-compose -f docker-compose.test.yml up -d
docker-compose exec -T app npm test
docker-compose down -v

# New
docker compose -f docker-compose.test.yml up -d
docker compose exec -T app npm test
docker compose down -v
```

### 5. Remove v1 (if desired)

```powershell
# Check if v1 is installed
docker-compose --version

# Remove v1 (varies by install method)
# If installed via pip:
pip uninstall docker-compose

# If installed via package:
sudo apt-get remove docker-compose

# If installed via curl:
rm /usr/local/bin/docker-compose
```

## New Features in v2

```yaml
# Watch mode (live reload)
services:
  app:
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
        - action: rebuild
          path: package.json
# docker compose watch

# Profiles
services:
  debug:
    profiles: ["debug"]
    build: .
    stdin_open: true
    tty: true
```

## Verification

```powershell
# v2 is the default
docker compose version

# Both should produce same output
docker compose config
docker-compose config 2>$null
```

## Pitfalls

- v1 is deprecated and may not receive security updates
- `docker compose` (v2) is a CLI plugin -- ensure it's installed with Docker Desktop/Engine
- Some `docker-compose` flags differ in v2 -- check `docker compose --help`
- `--compatibility` flag in v2 emulates v1 behavior for problematic options
- Third-party tools referencing `docker-compose` need updating
