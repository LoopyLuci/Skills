---
name: blog-analytics-interpreter
description: "Use when interpreting blog analytics. Traffic insights."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [blog, analytics, traffic, metrics, growth]
    related_skills: [blog-seo-post-optimizer, blog-publishing-workflow, content-repurposing]
---

# Blog Analytics Interpreter

"Use when interpreting blog analytics. Traffic insights."

## Trigger

Activate this skill when the user mentions:
- blog,  analytics,  traffic,  metrics,  growth workflows or issues
- Building, fixing, or optimizing blog analytics interpreter
- Questions about blog best practices

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

`blog, analytics, traffic, metrics, growth`

---

*LoopyLuci/Skills - 2026-09-24*
