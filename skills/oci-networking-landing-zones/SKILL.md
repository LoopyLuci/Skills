---
name: oci-networking-landing-zones
description: Use when vCNs, subnets, route tables, internet/NAT/service gateways, security lists and rules, NSGs and rules, and ZPR security-attribute assignments when inputs must be collected and validated through read-only OCI API MCP checks, then integrated without disrupting an existing Terraform pipeline or provider setup.
version: 2.0.0
author: LoopyLuci Community
license: UPL-1.0
platforms: [any]
metadata:
  hermes:
    tags: [oracle, oci, oci-landing-zone-terraform-module]
    source: oracle/skills
    adapted: true
---

# Build OCI Networking Landing Zones Terraform

> **Adapted for the LoopyLuci Skills collection** from [oracle/skills](https://github.com/oracle/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- VCNs, subnets, route tables, internet/NAT/service gateways, security lists and rules, NSGs and rules, and ZPR security-attribute assignments when inputs must be collected and validated through read-only OCI API MCP checks, then integrated without disrupting an existing Terraform pipeline or provider setup

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Generate or update safe OCI network Terraform configuration using only `oci-landing-zones/terraform-oci-modules-networking`. Use the OCI API MCP server for read-only validation only — never to create, update, delete, or mutate OCI resources — and never install or run Terraform locally.

## Required workflow

1. **Inspect before writing.** Review the Terraform repository, provider aliases, backend, module source pins, variable-data convention, and existing `network_configuration` values. For any lifecycle request, inspect accessible state read-only; if pipeline state is inaccessible, require the customer to supply the exact pipeline state address and ownership confirmation. Read `references/module-support.md`; if the capability is unavailable, report it with the required response and stop that portion. Read `references/lifecycle-safety.md` for update, removal, replacement, or deletion.

2. **Collect supported inputs.** Read the shared section plus only the matching resource sections of `references/input-collection.md`; read its existing-VCN injection section whenever the target VCN already exists. Ask for missing required values and the customer-approved traffic purpose for every gateway, route, public access, or security rule. Do not infer topology, OCIDs, CIDRs, or access scope. Once required values are complete, ask whether the customer wants documented optional parameters; use documented defaults if declined.

3. **Validate.** Read `references/validation.md` after all requested inputs are collected. Use OCI API MCP read commands only to validate supplied and referenced resources, and a dry-run flag only when current MCP help confirms it is supported and non-mutating. Pause for corrected input when a value is missing or known invalid. If OCI API MCP is unavailable, say MCP validation was skipped and continue only with documented non-MCP checks.

4. **Generate the smallest compatible change.** Read `references/terraform-sources.md` and `references/main-tf-map.md`; the configuration map decides whether to extend an existing root module, add one supported root module, or reject the request. Reuse the existing compatible OCI provider, aliases, backend, module source pin, variables, and module block; never add duplicate providers, change credentials, or disturb the existing setup. Create VCNs under `vcns`; add resources to an existing VCN only through `inject_into_existing_vcns`. Preserve stable map keys and existing values.

5. **Hand off.** Do not run local Terraform. State that the customer pipeline must run the approved validation, plan, and apply stages and that the plan must be reviewed before apply.

## Boundaries

- Use only `oci-landing-zones/terraform-oci-modules-networking`; no direct `oci_*` substitutes, other landing-zone repositories, or custom modules.
- Never create or change ZPR policies — the networking module supports security-attribute assignment but not ZPR policy management.
- Never replace, delete, move, rename, or modify an existing resource unless the customer names it, confirms state ownership, and approves the exact action.
- Never change providers, aliases, backend, authentication, Terraform version constraints, or module pins unless explicitly requested.
- Never execute `terraform`, `tofu`, state commands, provider login, installations, or pipeline commands.

## Reference routing

```text
request
  -> module-support.md
       -> unsupported: report and stop that portion
       -> supported: relevant input section + terraform-sources.md
            -> lifecycle-safety.md when lifecycle change
            -> validation.md
                 -> main-tf-map.md
                      -> generate configuration for pipeline review
```

| Need | Read |
| --- | --- |
| Confirm support or reject the capability | `references/module-support.md` |
| Collect VCN, subnet, route, gateway, security, or ZPR inputs | `references/input-collection.md` |
| Apply OCI API MCP and structural validation | `references/validation.md` |
| Preserve provider, source, backend, and pipeline behavior | `references/terraform-sources.md` |
| Handle update, removal, replacement, or delete | `references/lifecycle-safety.md` |
| Place data in `vcns` or `inject_into_existing_vcns` | `references/main-tf-map.md` |

## Verification

- [ ] Capability confirmed against the networking module.
- [ ] Existing provider, backend, and module pins preserved.
- [ ] Existing VCN changes routed through `inject_into_existing_vcns`.
- [ ] OCI API MCP used read-only; no mutation performed.
- [ ] No Terraform command executed locally.

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
- Path: `_sources/oracle_skills/oci/oci-landing-zone-terraform-module/terraform-oci-modules-networking-skill/SKILL.md`
- License: UPL-1.0 — Copyright (c) 2025 Oracle and/or its affiliates
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
