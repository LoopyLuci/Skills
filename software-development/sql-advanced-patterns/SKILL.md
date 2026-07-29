---
name: sql-advanced-patterns
description: "Use when writing advanced SQL queries and optimizations."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sql, advanced-sql, CTE, window-functions, optimization, execution-plan]
    related_skills: [database-design-patterns, data-modeling-foundations, database-schema-design, database-migration-patterns]
---

# Advanced SQL Patterns

Writing advanced SQL queries — from CTEs and window functions through query optimization, execution plan analysis, and performance tuning.

## When to Use

- Writing complex analytical SQL queries
- Optimizing slow-running queries
- Using window functions for running totals, ranking, moving averages
- Recursive CTEs for hierarchical data
- Understanding and improving query execution plans

## SQL Patterns

```sql
-- Window function: running total
SELECT date, amount,
       SUM(amount) OVER (ORDER BY date) as running_total,
       AVG(amount) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7d
FROM transactions;

-- Recursive CTE: org hierarchy
WITH RECURSIVE org_tree AS (
    SELECT id, name, manager_id, 1 as level
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, ot.level + 1
    FROM employees e JOIN org_tree ot ON e.manager_id = ot.id
)
SELECT * FROM org_tree ORDER BY level;

-- Pivot with conditional aggregation
SELECT 
    department,
    COUNT(*) FILTER (WHERE status = 'active') as active,
    COUNT(*) FILTER (WHERE status = 'inactive') as inactive
FROM employees GROUP BY department;
```

## Verification Checklist

- [ ] Window functions avoid self-joins for running totals
- [ ] CTEs improve readability and maintainability
- [ ] Queries use indexes effectively (check EXPLAIN ANALYZE)
- [ ] No N+1 queries (batched with IN or JOIN)
- [ ] Recursive CTEs have termination condition
- [ ] Query execution time under acceptable threshold
