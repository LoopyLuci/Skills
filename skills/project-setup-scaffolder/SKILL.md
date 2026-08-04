---
name: project-setup-scaffolder
description: "Use for project scaffolding. Folder structure, lint, CI."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [programming, project-setup, scaffolding, boilerplate, configuration, tooling]
    related_skills: [dependency-management, code-review-checklist, codebase-onboarding]
---

# Project Setup Scaffolder

## Overview

Comprehensive project scaffolding methodology covering folder structure, build configuration, linting/formatting, CI/CD templates, test frameworks, Docker setup, environment variable management, and pre-commit hooks. Includes per-language templates for Python, JavaScript/TypeScript, Go, Rust, and generic projects.

## When to Use

- Starting a new project from scratch
- Standardizing project structure across a team or organization
- Setting up CI/CD for an existing project
- Adding linting, formatting, or pre-commit hooks to an existing project
- Creating a template repository for reuse
- Onboarding a new microservice or package into a monorepo

## Workflow

### Phase 1: Choose Directory Structure

**Python (application):**
```
project/
├── src/
│   └── project/
│       ├── __init__.py
│       ├── main.py              # Entry point
│       ├── config.py            # Configuration
│       ├── models/              # Data models
│       ├── services/            # Business logic
│       ├── api/                 # HTTP handlers
│       └── cli/                 # CLI commands
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Shared fixtures
│   ├── test_services/
│   └── test_api/
├── docs/
├── scripts/
│   └── seed_data.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci.yml
├── .env.example
├── .gitignore
├── pyproject.toml               # All config in one file
├── README.md
├── Makefile
└── Dockerfile
```

**JavaScript/TypeScript (application):**
```
project/
├── src/
│   ├── index.ts                 # Entry point
│   ├── config/
│   ├── routes/
│   ├── controllers/
│   ├── services/
│   ├── middleware/
│   └── types/
├── tests/
│   ├── unit/
│   └── integration/
├── public/
├── scripts/
├── .github/workflows/
├── .env.example
├── .gitignore
├── .eslintrc.cjs
├── .prettierrc
├── tsconfig.json
├── jest.config.ts
├── package.json
├── Dockerfile
├── docker-compose.yml
├── README.md
└── Makefile
```

**Go (standard):**
```
project/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── config/
│   ├── handler/
│   ├── middleware/
│   ├── model/
│   ├── repository/
│   └── service/
├── pkg/
│   └── shared/
├── migrations/
├── scripts/
├── .github/workflows/
├── .env.example
├── .gitignore
├── go.mod
├── go.sum
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── README.md
```

### Phase 2: Build Configuration

**Python — pyproject.toml (single source of truth):**

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "my-project"
version = "0.1.0"
description = "My project description"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.110,<1",
    "sqlalchemy>=2.0,<3",
    "alembic>=1.13,<2",
    "pydantic>=2.0,<3",
]
optional-dependencies = {
    dev = [
        "pytest>=8,<9",
        "pytest-cov>=5,<6",
        "ruff>=0.4,<1",
        "mypy>=1.9,<2",
        "pre-commit>=3.7,<4",
    ]
}

[tool.setuptools.packages.find]
where = ["src"]
include = ["my_project*"]

[tool.ruff]
target-version = "py311"
line-length = 100
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "SIM", "ARG", "C4", "T20"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "lf"

[tool.mypy]
strict = true
ignore_missing_imports = true
disallow_untyped_defs = true
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --tb=short --cov=src --cov-report=term-missing --cov-fail-under=80"
```

**JavaScript/TypeScript — package.json:**

```json
{
  "name": "my-project",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "test": "vitest run",
    "test:watch": "vitest",
    "lint": "eslint src/ --ext .ts",
    "format": "prettier --write 'src/**/*.ts'",
    "typecheck": "tsc --noEmit",
    "ci": "npm run lint && npm run typecheck && npm run test"
  },
  "devDependencies": {
    "typescript": "^5.4",
    "tsx": "^4.7",
    "vitest": "^1.6",
    "eslint": "^8.57",
    "@typescript-eslint/eslint-plugin": "^7.0",
    "@typescript-eslint/parser": "^7.0",
    "prettier": "^3.2"
  }
}
```

### Phase 3: Pre-commit Hooks

**Python — .pre-commit-config.yaml:**

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
        args: ['--maxkb=500']
      - id: detect-private-key

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
        additional_dependencies: [pydantic, sqlalchemy]
        args: [--strict]

  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        types: [python]
        pass_filenames: false
        always_run: true
        args: ["--cov=src", "--cov-fail-under=80", "-x"]
```

```bash
# Install and activate
pip install pre-commit
pre-commit install
pre-commit autoupdate
pre-commit run --all-files  # Run on initial setup
```

**JavaScript/TypeScript — husky + lint-staged:**

```json
// package.json
{
  "scripts": {
    "prepare": "husky"
  },
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,yaml}": ["prettier --write"]
  }
}
```

```bash
npx husky-init && npm install
npx husky add .husky/pre-commit "npx lint-staged"
```

### Phase 4: CI/CD Template

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  PYTHON_VERSION: "3.11"
  NODE_VERSION: "20"

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install ruff
      - run: ruff check src/ tests/

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: test
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'
      - run: pip install -e ".[dev]"
      - run: pytest --cov=src --cov-fail-under=80 --cov-report=xml
      - uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml

  docker:
    runs-on: ubuntu-latest
    needs: [lint, test]
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
```

### Phase 5: Docker Setup

```dockerfile
# Python Dockerfile — multi-stage build
FROM python:3.11-slim AS builder

WORKDIR /app
COPY pyproject.toml .
RUN pip install --user --no-cache-dirs -e ".[dev]"

FROM python:3.11-slim AS runtime

RUN addgroup --system --gid 1001 app && \
    adduser --system --uid 1001 --gid 1001 app

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY --chown=app:app src/ src/
COPY --chown=app:app alembic/ alembic/
COPY --chown=app:app alembic.ini .

ENV PATH=/root/.local/bin:$PATH \
    PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER app
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "project.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
services:
  app:
    build:
      context: .
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./src:/app/src  # Hot reload in dev
    command: ["uvicorn", "project.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${DB_NAME:-myproject}
      POSTGRES_USER: ${DB_USER:-app}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-secret}
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-app} -d ${DB_NAME:-myproject}"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
```

### Phase 6: Environment Variables

```bash
# .env.example — checked into git, no secrets
# Copy to .env and fill in secrets locally
# NEVER commit .env to git

# Application
APP_NAME=my-project
APP_ENV=development
LOG_LEVEL=debug
SECRET_KEY=change-me-in-production

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myproject
DB_USER=app
DB_PASSWORD=
DB_POOL_SIZE=10
DB_POOL_OVERFLOW=20

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# External Services
API_BASE_URL=http://localhost:8000
THIRD_PARTY_API_KEY=

# Feature Flags
FEATURE_NEW_PAYMENT=false
FEATURE_ANALYTICS=true
```

```python
# src/project/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "my-project"
    app_env: str = "development"
    log_level: str = "debug"
    secret_key: str

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "myproject"
    db_user: str = "app"
    db_password: str = ""
    db_pool_size: int = 10
    db_pool_overflow: int = 20

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""

    third_party_api_key: str = ""

    feature_new_payment: bool = False
    feature_analytics: bool = True

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

### Phase 7: Gitignore & Editor Config

```gitignore
# .gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
*.egg
dist/
build/
.venv/
venv/
*.so

# Environment
.env
.env.local
.env.*.local

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
coverage/
.coverage
.coverage.*
htmlcov/
.pytest_cache/
.mypy_cache/
.ruff_cache/
```

## Common Pitfalls

- **No src/ layout**: Putting code in a flat project root causes import issues. Always use `src/<package>/` layout for Python projects.
- **Skipping type hints**: In typed languages, always configure strict type checking from day one. Much harder to retrofit.
- **CI without caching**: Every CI run reinstalls all deps from scratch. Always configure pip/npm/cargo caching in CI workflows.
- **No Docker health checks**: Docker Compose depends_on without health checks can start your app before the database is ready.
- **Not pinning dependency versions**: Use `>=X,<Y` ranges to get bug fixes without breaking changes.
- **Committed .env files**: A single committed .env will leak secrets across the team. Always use .env.example with real .env in .gitignore.
- **Missing .dockerignore**: Without it, Docker sends the entire project including node_modules and __pycache__ to the daemon.
- **No pre-commit hooks**: Formatting and linting should be automatic, not a manual step. Set up pre-commit on day one.
- **Forgetting Windows paths**: With docker, paths must work cross-platform. Use Makefile targets that translate.
- **Not setting PYTHONPATH**: Python projects need explicit PYTHONPATH configuration in Dockerfiles and CI.

## Verification Checklist

- [ ] Project structure follows language conventions (src/ layout for Python, cmd/ for Go, etc.)
- [ ] Build configuration single-source-of-truth (pyproject.toml, Cargo.toml, go.mod, package.json)
- [ ] Linting configured and passing (ruff/ruff-format for Python, eslint/prettier for JS/TS)
- [ ] Type checking configured and strict mode enabled
- [ ] Pre-commit hooks installed and running on every commit
- [ ] CI pipeline configured (lint → test → build → (optionally) deploy)
- [ ] Docker multi-stage build with health checks
- [ ] docker-compose.yml with all services and proper dependency ordering
- [ ] .env.example checked in, .env in .gitignore
- [ ] Config class loads from environment with sensible defaults
- [ ] .gitignore covers OS, IDE, language, and project-specific patterns
- [ ] .dockerignore excludes development artifacts from build context
- [ ] README written with quickstart instructions
- [ ] Makefile or equivalent task runner with common commands (setup, dev, test, lint, build)