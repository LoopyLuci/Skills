---
name: project-scaffolding
description: "Generate project templates with lint CI and structure"
---

# Project Scaffolding

## Python Package Template
```bash
mkdir myproject && cd myproject
mkdir src/myproject tests
touch src/myproject/__init__.py src/myproject/main.py
touch tests/__init__.py tests/test_main.py
```

## Essential Files
```bash
cat > README.md << 'EOF'
# Project
EOF
cat > .gitignore << 'EOF'
__pycache__/ .venv/ .env dist/
EOF
```

## CI Template
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -e ".[dev]"
      - run: pytest
      - run: ruff check .
```
