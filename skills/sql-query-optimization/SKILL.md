---
name: sql-query-optimization
description: "Use when optimizing SQL query performance."
category: software-development
tags: [sql, optimization, database, queries, performance]
---
# SQL Query Optimization

Optimizing SQL queries for performance.

## Query Analysis

```sql
-- EXPLAIN ANALYZE (PostgreSQL)
EXPLAIN (ANALYZE, BUFFERS, TIMING) 
SELECT * FROM orders WHERE status = 'pending';

-- Look for:
-- Seq Scan on large tables → needs index
-- Nested Loop on large datasets → needs join optimization
-- Sort on unindexed column → needs index
-- High buffer usage → memory/cache issue
```

## Index Strategies

```sql
-- B-tree (default, for equality + range)
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created ON orders(created_at DESC);

-- Composite (column order matters)
-- Put equality columns first, range columns last
CREATE INDEX idx_orders_status_date ON orders(status, created_at);
-- WHERE status = 'pending' AND created_at > '2024-01-01' → USES INDEX

-- Partial (only index relevant rows)
CREATE INDEX idx_orders_active ON orders(created_at) 
    WHERE status != 'cancelled';

-- Covering (include extra columns to avoid table access)
CREATE INDEX idx_orders_covering ON orders(status) 
    INCLUDE (total_amount, customer_id);
```

## Join Optimization

```sql
-- Prefer hash joins for large, unsorted datasets
-- Prefer merge joins for pre-sorted data
-- Prefer nested loops for small right side

-- Set join order explicitly (PostgreSQL)
SET join_collapse_limit = 1;
SET from_collapse_limit = 1;
-- Then order tables in FROM clause from most selective to least

-- Use EXISTS instead of DISTINCT for existence
-- SLOW
SELECT DISTINCT c.* FROM customers c JOIN orders o ON c.id = o.customer_id;
-- FAST
SELECT * FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);
```

## Pagination Performance

```sql
-- OFFSET is slow for deep pages (reads all skipped rows)
-- SLOW
SELECT * FROM orders ORDER BY id LIMIT 20 OFFSET 100000;

-- Keyset/cursor pagination (fast, consistent)
-- FIRST PAGE
SELECT * FROM orders ORDER BY id LIMIT 20;
-- NEXT PAGE (use last id from previous page)
SELECT * FROM orders WHERE id > :last_id ORDER BY id LIMIT 20;
```

## Common Anti-Patterns

```sql
-- 1. SELECT * (fetches unnecessary columns)
SELECT id, name, email FROM users;  -- instead of SELECT *

-- 2. Functions on indexed columns (breaks index usage)
WHERE DATE(created_at) = '2024-01-01'
-- FIX: WHERE created_at >= '2024-01-01' AND created_at < '2024-01-02'

-- 3. Implicit type conversion
WHERE phone = 1234567890  -- varchar = integer → no index use
-- FIX: WHERE phone = '1234567890'

-- 4. N+1 in ORM (not SQL but common pattern)
# Bad: for user in users: query = SELECT * FROM orders WHERE user_id = user.id
# Good: Order.objects.filter(user_id__in=[u.id for u in users])
```

## Pitfalls

- Indexes speed up reads but slow writes — don't over-index
- Composite index column order matters: equality → range → group by
- EXPLAIN ANALYZE actually runs the query — use on SELECT only in production
- Vacuum/ANALYZE maintain statistics — stale stats = bad query plans
- Connection pooling prevents connection overhead but doesn't fix slow queries
