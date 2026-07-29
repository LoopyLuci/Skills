---
name: environment-bootstrap
description: "One command dev environment Python Node Docker setup"
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
