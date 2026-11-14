---
name: apexlang-example-applications
description: Use when working with provides a list of APEXlang example applications with appropriate descriptions and access to the assets.
version: 2.0.0
author: LoopyLuci Community
license: UPL-1.0
platforms: [any]
metadata:
  hermes:
    tags: [oracle, apex, apexlang]
    source: oracle/skills
    adapted: true
---

# Apexlang Example Applications

> **Adapted for the LoopyLuci Skills collection** from [oracle/skills](https://github.com/oracle/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Provides a list of APEXlang example applications with appropriate descriptions and access to the assets. Each example folder contains the complete APEXlang source tree of one real application for use as authoring evidence and composition reference

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Index of the bundled APEXLang example applications. Each `example-N/` folder under `assets/` contains the complete, unedited APEXLang source tree of a real application, supplied as authoring evidence and composition reference.

## Available examples

| Folder | What it demonstrates |
| --- | --- |
| `example-0` | Basic APEXLang template. Not the most minimal possible starting point, but a practical one. |
| `example-1` | Demonstration HR, order-management variant. Broad component coverage: 14 interactive reports, 9 form pages with formInitialization/formAutoRowProcessing pairs, 8 JET charts, 8 classic reports, 3 faceted searches paired with cards and classic reports, 2 editable interactive grids (including a master-detail orders/order-items page built on interactiveGridAutoRowProcessing), a calendar, and an access-control section with roles, authorization schemes, and PL/SQL validations. Strongest first reference for the report-plus-modal-form pattern and for shared components (LOVs, lists, breadcrumbs). |
| `example-2` | Demonstration HR, data-loading variant. A sibling OEHR application with a near-identical page inventory plus data-load definitions in shared components and a few extra custom pages. Best used as a comparison case: the same business pages composed by a different team, which makes the stable component patterns (form pairs, report-to-form links, faceted search wiring) stand out from app-specific choices. |

## How to use

- Treat the source as read-only evidence — copy patterns, not files.
- Reach for `example-1` for the standard patterns and `example-2` to separate convention from incidental choice.
- Cite the example path when recommending a pattern.

## Verification

- [ ] The cited example folder exists under `assets/`.
- [ ] The recommended pattern actually appears in that example's source.

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
- Path: `_sources/oracle_skills/apex/apexlang/26.2/apexlang-example-applications/SKILL.md`
- License: UPL-1.0 — Copyright (c) 2025 Oracle and/or its affiliates
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
