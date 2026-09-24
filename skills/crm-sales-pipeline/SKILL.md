---
name: crm-sales-pipeline
description: "Use when building CRM and sales pipeline management systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [crm, sales, pipeline, deals, lead-management, salesforce]
    related_skills: [real-estate-crm-leads, email-marketing-campaigns, business-metrics-kpis, customer-segmentation-analysis]
---

# Crm Sales Pipeline

"Use when building CRM and sales pipeline management systems."

## Trigger

Activate this skill when the user mentions:
- crm,  sales,  pipeline,  deals,  lead-management,  salesforce workflows or issues
- Building, fixing, or optimizing crm sales pipeline
- Questions about crm best practices

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

`crm, sales, pipeline, deals, lead-management, salesforce`

---

*LoopyLuci/Skills - 2026-09-24*
