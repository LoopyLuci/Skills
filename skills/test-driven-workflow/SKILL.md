---
name: test-driven-workflow
description: RED GREEN REFACTOR cycle with pytest and coverage
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [test, driven, workflow]
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

## Trigger

Activate this skill when the user mentions:
- test, driven, workflow workflows or issues
- Building, fixing, or optimizing test driven workflow


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
