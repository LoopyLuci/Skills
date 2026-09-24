---
name: database-migration-patterns
description: Safe schema migrations alembic rollback zero downtime
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [database, migration, patterns]
---

# Database Migration Patterns

## Alembic
```bash
pip install alembic
alembic init migrations
alembic revision --autogenerate -m "add users table"
alembic upgrade head
```

## Rollback
```bash
alembic downgrade -1
```

## Zero-Downtime Steps
1. Add column nullable
2. Deploy app (writes to new column)
3. Backfill data
4. Add NOT NULL constraint
5. Deploy app (reads from new column)
6. Drop old column

## Trigger

Activate this skill when the user mentions:
- database, migration, patterns workflows or issues
- Building, fixing, or optimizing database migration patterns


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
