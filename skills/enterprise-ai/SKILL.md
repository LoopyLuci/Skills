---
name: enterprise-ai
description: Use when the user asks for OCI Generative AI, Enterprise AI Models, Enterprise AI Agents, governed GenAI applications, agentic workflows, RAG on Oracle Cloud, OCI Generative AI pricing or cost estimator inputs, or a simplified path across OCI, Autonomous Database, APEX, and other Oracle services.
version: 2.0.0
author: LoopyLuci Community
license: UPL-1.0
platforms: [any]
metadata:
  hermes:
    tags: [oracle, oci]
    source: oracle/skills
    adapted: true
---

# OCI Enterprise AI Skills

> **Adapted for the LoopyLuci Skills collection** from [oracle/skills](https://github.com/oracle/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- The user asks for OCI Generative AI, Enterprise AI Models, Enterprise AI Agents, governed GenAI applications, agentic workflows, RAG on Oracle Cloud, OCI Generative AI pricing or cost estimator inputs, or a simplified path across OCI, Autonomous Database, APEX, and other Oracle services

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Front door for Oracle Enterprise AI work on OCI: models, agents, RAG, Responses API workflows, custom and imported models, fine-tuning, endpoints, private endpoints, vector stores, File Search, Code Interpreter, MCP tools, SQL Search, hosted agentic applications, and Oracle platform integrations. Start here when the goal is the AI outcome rather than a specific service name.

## How to use

1. Find the user's goal in the journey table below.
2. Read only the smallest topic file that matches the task.
3. Route database-owned implementation detail to `db/features/` rather than duplicating Select AI, vector search, or `DBMS_VECTOR` guidance here.

## Structure

```
oci/enterprise-ai/
├── models/            # OCI-hosted and custom/imported models
├── agent-workflows/   # Responses API agents, hosted apps, agent tools
├── governance/        # IAM, private endpoints, guardrails, audit
├── data/              # RAG and search
├── cost/              # pricing and cost estimation
├── integrations/      # Oracle platform connections
└── agents/
    └── openai.yaml
```

## User journey routing

| Goal | Start with |
| --- | --- |
| Choose or invoke OCI-hosted models, embeddings, rerank, endpoints, dedicated serving | `models/enterprise-ai-models.md` |
| Import, fine-tune, host, or lifecycle-manage a custom model | `models/custom-and-imported-models.md` |
| Build an API-first agent with OpenAI-compatible OCI APIs | `agent-workflows/responses-api-agents.md` |
| Deploy a packaged agent runtime on OCI-managed infrastructure | `agent-workflows/hosted-applications.md` |
| Choose a tool pattern: File Search, Code Interpreter, Function Calling, MCP, SQL Search | `agent-workflows/agent-tools.md` |
| Ground answers in documents, vector stores, SQL, or database vector search | `data/rag-and-search.md` |
| Estimate OCI Generative AI or Generative AI Agents cost drivers | `cost/cost-estimation.md` |
| Secure model or agent access with IAM, private networking, OAuth, guardrails, audit | `governance/private-endpoints-and-governance.md` |
| Connect to Autonomous Database, APEX, Oracle Integration, Fusion, or OCI AI Services | `integrations/oracle-platform-integrations.md` |

## Multi-step flows

| Task | Sequence |
| --- | --- |
| Governed enterprise assistant | responses-api-agents → agent-tools → rag-and-search → cost-estimation → private-endpoints-and-governance |
| Model experimentation to production serving | enterprise-ai-models → cost-estimation → private-endpoints-and-governance |
| Bring a custom model into OCI serving | custom-and-imported-models → enterprise-ai-models → cost-estimation → private-endpoints-and-governance |
| Deploy a packaged agent runtime | responses-api-agents → hosted-applications → cost-estimation → private-endpoints-and-governance |
| RAG over files | rag-and-search → agent-tools → cost-estimation → responses-api-agents |
| RAG over Oracle Database | rag-and-search → `db/features/vector-search.md` → `db/features/dbms-vector.md` → `db/features/select-ai.md` when in-database generation is needed |
| Add AI to APEX or Autonomous Database apps | oracle-platform-integrations → relevant `db/features/` or `apex/apexlang/` guidance |
| Design production access controls | private-endpoints-and-governance → enterprise-ai-models or responses-api-agents, depending on workload |

## Scope boundaries

Keep cloud-side model, agent, tool, endpoint, hosting, and governance decisions in this domain. Oracle Database-owned AI implementation belongs in `db/features/` (`select-ai.md`, `vector-search.md`, `dbms-vector.md`, `ai-profiles.md`); APEX artifact generation and APEX AI agent component templates belong in `apex/apexlang/`. Because Enterprise AI services change often, prefer official Oracle documentation for model availability, supported tools, IAM verbs, endpoint formats, and service limits.

## Sources

- https://docs.oracle.com/en-us/iaas/Content/generative-ai/overview.htm
- https://docs.oracle.com/en-us/iaas/Content/generative-ai/home.htm
- https://docs.oracle.com/en-us/iaas/Content/generative-ai/models.htm
- https://docs.oracle.com/en-us/iaas/Content/generative-ai/fine-tune-models.htm
- https://docs.oracle.com/en-us/iaas/Content/generative-ai/imported-models.htm
- https://docs.oracle.com/en-us/iaas/Content/generative-ai/agents.htm
- https://docs.oracle.com/en-us/iaas/Content/generative-ai/governance.htm
- https://docs.oracle.com/en-us/iaas/Content/generative-ai/oci-openai.htm
- https://www.oracle.com/artificial-intelligence/enterprise-ai/cost-estimator/
- https://docs.oracle.com/en-us/iaas/Content/generative-ai/calculate-cost.htm

## Verification

- [ ] The smallest matching topic file was read; no unrelated topics loaded.
- [ ] Database-owned details routed to `db/features/`, APEX details to `apex/apexlang/`.
- [ ] Current official docs consulted for availability, tools, IAM verbs, endpoints, and limits.

## Related Skills in This Repo

- [apexlang-inventory](../apexlang-inventory/SKILL.md) — Use when working with provides an overview of APEX application components, APEXlang syntax...
- [oke-troubleshooter](../oke-troubleshooter/SKILL.md) — Use when the user wants to diagnose or root-cause issues with an OCI Kubernetes Engine clu...
- [oke-gva-deployer](../oke-gva-deployer/SKILL.md) — Use when the user asks to enable, deploy, or configure Generic VNIC Attachment (GVA) for O...
- [oci-functions-deploy](../oci-functions-deploy/SKILL.md) — Use when asked to validate/install Fn, OCI CLI, and Docker, configure or create Fn context...

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [oracle/skills](https://github.com/oracle/skills)
- Path: `_sources/oracle_skills/oci/enterprise-ai/SKILL.md`
- License: UPL-1.0 — Copyright (c) 2025 Oracle and/or its affiliates
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
