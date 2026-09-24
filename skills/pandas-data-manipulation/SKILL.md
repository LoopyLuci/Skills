---
name: pandas-data-manipulation
description: Use when manipulating data with Pandas.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [pandas, dataframe, groupby, merge, reshape]
---

# Pandas Data Manipulation

"Use when manipulating data with Pandas."

## Trigger

Activate this skill when the user mentions:
- "pandas",  "dataframe",  "groupby",  "merge",  "reshape" workflows or issues
- Building, fixing, or optimizing pandas data manipulation
- Questions about "pandas" best practices

## Core Concepts

- Data modeling (dimensional, normalized)
- ETL/ELT patterns and idempotency
- Data quality and validation
- Lineage and cataloging
- Privacy and data protection

## Step-by-Step Workflow

1. **Discover** — Profile data, assess quality
   - Expected: Data profile report with quality scores
2. **Design** — Model for use case
   - Expected: Approved data model
3. **Build** — Implement pipelines with testing
   - Expected: Idempotent pipelines with quality checks
4. **Validate** — Reconcile, test business rules
   - Expected: Validated data with quality metrics
5. **Operate** — Monitor, optimize, iterate
   - Expected: Monitored pipelines with SLA tracking

## Tools & Technologies

- dbt
- Airflow/Prefect
- Spark/DuckDB
- Data catalogs

## Best Practices

- Document decisions and rationale (ADRs, design docs, runbooks)
- Version everything - code, configs, data, and documentation
- Test incrementally; never claim passing without verification
- Respect domain-specific regulations and ethical standards
- Measure outcomes with meaningful metrics

## Common Pitfalls

- **No data quality gates** → Garbage in, garbage out → Validate at every stage
- **Monolithic pipelines** → Hard to debug → Small idempotent tasks

## Tags

`"pandas", "dataframe", "groupby", "merge", "reshape"`

---

*LoopyLuci/Skills - 2026-09-24*
