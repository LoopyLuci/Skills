---
name: fullstack-dev-db-schema
description: Use when designing relational database schemas, indexes, migrations, and data models.
tags: [database, schema, sql, postgresql, migration, indexing, data-modeling]
related_skills: [fullstack-dev-api-design, android-native-dev]
---

# Database Schema Design

ORM-agnostic guide for relational database schema design covering data modeling, normalization, indexing, migrations, multi-tenancy, and common patterns.

## Quick Start Checklist

- [ ] Domain entities identified (1 entity = 1 table)
- [ ] Primary keys: UUID for public IDs, serial/bigserial for internal
- [ ] Foreign keys with explicit `ON DELETE` behavior
- [ ] `NOT NULL` by default (nullable only when business logic requires)
- [ ] `created_at` + `updated_at` on every table
- [ ] Indexes for every WHERE, JOIN, ORDER BY column
- [ ] Start normalized, denormalize only when measured
- [ ] Consistent naming: `snake_case`, plural table names

## Code Example: Table with Relationships

```sql
CREATE TABLE orders (
    id          bigserial PRIMARY KEY,
    public_id   uuid NOT NULL DEFAULT gen_random_uuid() UNIQUE,
    user_id     bigint NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    total       numeric(10,2) NOT NULL,
    status      text NOT NULL DEFAULT 'pending',
    created_at  timestamptz NOT NULL DEFAULT now(),
    updated_at  timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status) WHERE status = 'pending';
```

## Code Example: Safe Column Rename (3 Deploys)

```sql
-- Deploy 1: Add new column, backfill
ALTER TABLE users ADD COLUMN full_name text;
UPDATE users SET full_name = name;

-- Deploy 2: Switch reads to new column (app change)

-- Deploy 3: Drop old column
ALTER TABLE users DROP COLUMN name;
```

## Common Pitfalls

- **No indexes on foreign keys**: Always index FK columns used in JOINs
- **Destructive migrations in one step**: Always ADD → MIGRATE DATA → REMOVE OLD in separate deploys
- **NOT NULL added without backfill**: Add column as nullable, backfill data, then add constraint
- **Index without CONCURRENTLY**: Use `CREATE INDEX CONCURRENTLY` to avoid table locks on live DB
- **Singleton tables**: Tables with low cardinality columns (boolean) alone don't benefit from indexes

## Verification Checklist

- [ ] Primary key on every table
- [ ] Foreign keys with explicit ON DELETE
- [ ] Timestamps (created_at, updated_at) on every table
- [ ] Indexes on all WHERE/JOIN/ORDER BY columns
- [ ] Migrations are additive (no drop/rename in one step)
- [ ] CONCURRENTLY used for indexes on live DB
- [ ] No premature denormalization
