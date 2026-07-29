---
name: postgresql-advanced-queries
description: "Use when writing advanced PostgreSQL queries."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [postgresql, SQL, CTEs, window-functions, jsonb, full-text-search]
    related_skills: [sql-advanced-patterns, database-design-patterns, data-modeling-foundations]
---

# Advanced PostgreSQL Queries

Writing advanced PostgreSQL queries — from CTEs and window functions through JSONB, full-text search, recursive queries, and performance tuning.

## When to Use

- Writing complex analytical SQL queries
- Using PostgreSQL-specific features (JSONB, GIN indexes)
- Full-text search with tsvector
- Recursive CTEs for tree/graph data
- Query optimization with EXPLAIN ANALYZE

## PostgreSQL Patterns

```sql
-- Recursive CTE for tree traversal
WITH RECURSIVE org_tree AS (
    SELECT id, name, manager_id, 1 AS depth
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, ot.depth + 1
    FROM employees e INNER JOIN org_tree ot ON e.manager_id = ot.id
)
SELECT * FROM org_tree ORDER BY depth, name;

-- Full-text search
SELECT title, ts_rank(to_tsvector('english', body), plainto_tsquery('search terms')) AS rank
FROM articles
WHERE to_tsvector('english', body) @@ plainto_tsquery('search terms')
ORDER BY rank DESC;

-- JSONB queries
SELECT data->>'name' AS name, data->>'email' AS email
FROM users WHERE data @> '{"role": "admin"}'::jsonb;
```

## Verification Checklist

- [ ] Recursive CTE has termination condition
- [ ] Window functions (ROW_NUMBER, LAG, LEAD) correct
- [ ] GIN indexes for JSONB and full-text search
- [ ] EXPLAIN ANALYZE for query performance
- [ ] Partial indexes for filtered queries
- [ ] Materialized views for expensive queries
- [ ] Table partitioning for large tables
