---
name: apexlang-deploy
description: Use when working with deploys the application specified in APEXLang to a provided database.
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

# Apexlang Deploy

> **Adapted for the LoopyLuci Skills collection** from [oracle/skills](https://github.com/oracle/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Deploys the application specified in APEXLang to a provided database

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

This skill imports an APEXLang-defined application into a target database. It wraps `scripts/deploy-apex-app.sh <app-directory>`, which uses SQLcl to perform the import. Two environment variables must be set beforehand: `SQLCL_BIN` (absolute path to the SQLcl executable) and `SQLCL_CONNECTION_STRING` (the SQLcl connection string).

Set both variables, then run `scripts/deploy-apex-app.sh <app-directory>` to deploy the application directory to the provided database.

## Verification

- [ ] `SQLCL_BIN` points at the SQLcl executable and `SQLCL_CONNECTION_STRING` names the target database.
- [ ] The script exits without error.
- [ ] Any reported import failure is addressed before considering the deployment done.

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
- Path: `_sources/oracle_skills/apex/apexlang/26.2/apexlang-deploy/SKILL.md`
- License: UPL-1.0 — Copyright (c) 2025 Oracle and/or its affiliates
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
