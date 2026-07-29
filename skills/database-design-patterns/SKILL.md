---
name: database-design-patterns
description: "Use when designing database schemas and migrations."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [database, sql, nosql, schema, indexing, migration, postgresql]
    related_skills: [sql-query-optimization, data-structures-algorithms, system-design-patterns, api-design-rest-graphql]
---

# Database Design Patterns

Designing efficient database schemas, indexing strategies, migration workflows, and data access patterns for SQL and NoSQL databases.

## When to Use

- Designing a new database schema from scratch
- Optimizing slow queries with proper indexing
- Planning database migrations without downtime
- Choosing between SQL, NoSQL, or hybrid approaches
- Modeling complex domain relationships in relational databases

## Schema Design Patterns

### Single Table Inheritance

```sql
CREATE TABLE assets (
    id SERIAL PRIMARY KEY,
    type VARCHAR(20) NOT NULL CHECK (type IN ('document', 'image', 'video')),
    title TEXT NOT NULL,
    page_count INTEGER,
    width INTEGER, height INTEGER,
    duration INTEGER, resolution VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Concrete Table Inheritance

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY, title TEXT NOT NULL, page_count INTEGER
);
CREATE TABLE images (
    id SERIAL PRIMARY KEY, title TEXT NOT NULL, width INTEGER, height INTEGER
);
```

### Class Table Inheritance

```sql
CREATE TABLE assets (
    id SERIAL PRIMARY KEY, type VARCHAR(20) NOT NULL, title TEXT NOT NULL
);
CREATE TABLE documents (asset_id INTEGER PRIMARY KEY REFERENCES assets(id), page_count INTEGER);
CREATE TABLE images (asset_id INTEGER PRIMARY KEY REFERENCES assets(id), width INTEGER, height INTEGER);
```

## Indexing Patterns

### Composite Index Column Order

```sql
-- For: WHERE status = 'active' AND created_at > '2024-01-01'
-- Place high-selectivity columns FIRST
CREATE INDEX idx_orders_status_created ON orders (status, created_at);
```

### Covering Index

```sql
-- Index-Only Scan: never touches the heap
-- For: SELECT user_id, email FROM users WHERE status = 'active';
CREATE INDEX idx_users_status_covering ON users (status) INCLUDE (user_id, email);
```

### Partial Index

```sql
-- Index only active records (much smaller, faster writes)
CREATE INDEX idx_orders_active ON orders (created_at) WHERE status = 'active';
```

### Expression Index

```sql
CREATE INDEX idx_users_lower_email ON users (LOWER(email));
-- SELECT * FROM users WHERE LOWER(email) = 'user@example.com';
```

## Migration Patterns

### Expand-Contract (Zero-Downtime)

```sql
-- Phase 1: EXPAND — add new column
ALTER TABLE users ADD COLUMN email_new VARCHAR(255);
-- App writes to both columns

-- Phase 2: Backfill
UPDATE users SET email_new = email WHERE email_new IS NULL;

-- Phase 3: CONTRACT
ALTER TABLE users DROP COLUMN email;
ALTER TABLE users RENAME COLUMN email_new TO email;
```

## NoSQL Patterns

### Document Denormalization

```python
user = {
    "_id": "user_123",
    "name": "Alice",
    "addresses": [
        {"type": "home", "street": "123 Main St"},
        {"type": "work", "street": "456 Corp Ave"}
    ]
}
# Pro: Single read for user + addresses
# Con: Update anomalies on separately-edited embedded docs
```

### CQRS

```python
class CQRSHandler:
    def __init__(self):
        self.write_db = PostgresWriteDB()     # Normalized
        self.read_db = ElasticsearchReadDB()   # Denormalized
    
    def handle_command(self, command):
        result = self.write_db.execute(command)
        self.sync_to_read_model(result)
        return result
    
    def handle_query(self, query):
        return self.read_db.search(query)
```

## Common Pitfalls

1. **Premature denormalization** — normalize first, denormalize only when query patterns demand it
2. **Missing foreign keys** — relational integrity enforced at app level drifts over time
3. **Index-everything** — writes become slow; index only what queries filter on
4. **SELECT * in production** — always name columns; breaks when schema changes
5. **No migration plan** — schema changes without backfill cause downtime
6. **Ignoring EXPLAIN ANALYZE** — the optimizer shows what's really happening; always check

## Verification Checklist

- [ ] Schema normalized to 3NF before any denormalization
- [ ] Indexes match actual query patterns (check slow query log)
- [ ] Migrations are reversible (up + down functions)
- [ ] Foreign keys enforced at DB level
- [ ] EXPLAIN ANALYZE confirms index usage on critical queries
- [ ] No N+1 queries in common access patterns

## See Also

- sql-query-optimization — optimizing queries against your schema
- data-structures-algorithms — choosing right data structures
- system-design-patterns — database at scale
