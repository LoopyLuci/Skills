---
name: oracle-data-guard
description: Use when a user asks about SQLcl DG commands, Data Guard Broker fixed views, FSFO or observer state, transport or apply lag, ASYNC/SYNC/FASTSYNC performance, redo apply tuning, SIRA/MIRA, or runnable Data Guard diagnostic SQL.
version: 2.0.0
author: LoopyLuci Community
license: UPL-1.0
platforms: [any]
metadata:
  hermes:
    tags: [oracle, db]
    source: oracle/skills
    adapted: true
---

# Oracle Data Guard

> **Adapted for the LoopyLuci Skills collection** from [oracle/skills](https://github.com/oracle/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- A user asks about SQLcl DG commands, Data Guard Broker fixed views, FSFO or observer state, transport or apply lag, ASYNC/SYNC/FASTSYNC performance, redo apply tuning, SIRA/MIRA, or runnable Data Guard diagnostic SQL

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Operational guidance for Oracle Data Guard and SQLcl DG. The bundled references are the source of truth — read only the smallest relevant one. Never imply that a live database, Broker configuration, or observer was inspected unless the user supplied output or a connected tool returned it.

## Routing

| Request | Reference |
| --- | --- |
| Broad Data Guard question or uncertain topic | `references/00_DG_RESOURCE_INDEX.md` |
| SQLcl `DG` syntax or supported `SHOW` commands | `references/01_SQLCL_DG_COMMANDS.md` |
| Broker configuration/properties, role changes, FSFO, observer, broker health | `references/02_BROKER_FIXED_VIEW_ROUTING.md` |
| Lag interpretation, transport-versus-apply triage | `references/03_OVERVIEW_AND_LAG_MODEL.md` |
| Redo transport lag | `references/04_TRANSPORT_TROUBLESHOOTING.md` |
| Deep ASYNC transport analysis, `krsb` statistics | `references/05_ASYNC_TRANSPORT_ADVANCED.md` |
| SYNC/FASTSYNC commit latency or remote write cost | `references/06_SYNC_TRANSPORT_PERFORMANCE.md` |
| Apply lag or recovery throughput | `references/07_APPLY_TROUBLESHOOTING.md` |
| SIRA/MIRA choice, recovery waits, tuning | `references/08_APPLY_TUNING_SIRA_MIRA.md` |
| Runnable diagnostic SQL | `references/09_SQL_QUERY_COOKBOOK.md` |
| Concise triage flow or playbook | `references/10_DECISION_TREES_AND_PLAYBOOKS.md` |

## Response workflow

1. Establish the topology and the concern: Broker versus SQLcl, transport versus apply, and ASYNC versus SYNC/FASTSYNC where it matters.
2. Read the selected reference. Consult `09_SQL_QUERY_COOKBOOK.md` only when executable SQL directly helps.
3. State what evidence is required, give safe diagnostic steps, and separate confirmed facts from hypotheses.
4. Treat sample timestamps as placeholders; ask for the real incident window when it changes a query.
5. When transport and apply lag are both zero, frame the work as a health check, baseline, configuration review, or commit-latency investigation — not as a lag incident.

## Safety

Observe before changing. Label any command that alters database settings, enables tracing, or changes recovery configuration, and pair it with the rollback or disable step where the reference provides one.

## Verification

- [ ] Only the smallest relevant reference was read.
- [ ] No live-inspection claim without user-supplied output.
- [ ] Hypotheses are labelled as hypotheses.
- [ ] Every change command carries a rollback step.

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
- Path: `_sources/oracle_skills/db/data-guard/SKILL.md`
- License: UPL-1.0 — Copyright (c) 2025 Oracle and/or its affiliates
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
