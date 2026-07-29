---
name: test-driven-workflow
description: "RED GREEN REFACTOR cycle with pytest and coverage"
---

# TDD Workflow

## Cycle
1. RED: Write failing test first
2. GREEN: Write minimal code to pass
3. REFACTOR: Clean up while keeping tests green

```bash
# Run tests in watch mode
pytest-watch
# Run with coverage
pytest --cov=src --cov-report=term-missing
```
