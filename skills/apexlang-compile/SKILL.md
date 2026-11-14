---
name: apexlang-compile
description: Use when working with provides access to the APEXLang compiler to build and validate an application from a given file tree.
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

# Apexlang Compile

> **Adapted for the LoopyLuci Skills collection** from [oracle/skills](https://github.com/oracle/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Provides access to the APEXLang compiler to build and validate an application from a given file tree

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

The APEXLang compiler validates an APEX application tree before anything gets deployed. This skill wraps `scripts/validate-apex-app.sh <app-directory>`, which starts SQLcl headlessly (`/nolog`) and runs `apex validate` against the supplied directory, surfacing compiler errors you can fix in place. It requires `SQLCL_BIN` to point at the absolute path of the SQLcl executable.

Run `scripts/validate-apex-app.sh <app-directory>` to build and validate the application directory. The helper launches SQLcl with `/nolog` and executes `apex validate` for that directory.

## Verification

- [ ] `SQLCL_BIN` is set to the absolute path of the SQLcl executable.
- [ ] `apex validate` completes without errors for the target `<app-directory>`.
- [ ] Any reported issues are resolved before moving on to deployment.

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
- Path: `_sources/oracle_skills/apex/apexlang/26.2/apexlang-compile/SKILL.md`
- License: UPL-1.0 — Copyright (c) 2025 Oracle and/or its affiliates
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
