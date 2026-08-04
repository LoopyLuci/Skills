---

name: ci-cd-pipeline-setup
description: "GitHub Actions matrix builds caching and conditional deploys"

---

# CI/CD Pipeline Setup

## GitHub Actions
```yaml
name: CI/CD
on: [push, pull_request]
jobs:
  test:
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: ${{ matrix.python-version }} }
      - uses: actions/cache@v4
        with: { path: ~/.cache/pip, key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }} }
      - run: pip install -e ".[dev]"
      - run: pytest
  deploy:
    needs: [test]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying..."
```
