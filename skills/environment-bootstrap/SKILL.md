---
name: environment-bootstrap
description: One command dev environment Python Node Docker setup
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [environment, bootstrap]
---

# Environment Bootstrap

## Python
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Node.js
```bash
nvm install --lts
nvm use --lts
npm install
```

## Docker
```bash
docker compose up -d
docker compose logs -f
```

## setup.sh Pattern
```bash
#!/bin/bash
set -e
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
echo "Ready!"
```

## Trigger

Activate this skill when the user mentions:
- environment, bootstrap workflows or issues
- Building, fixing, or optimizing environment bootstrap


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
