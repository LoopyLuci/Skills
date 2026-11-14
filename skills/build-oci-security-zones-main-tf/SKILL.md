---
name: build-oci-security-zones-main-tf
description: Use when cloud Guard Security Zone recipes and Security Zones when requests must be mapped to the documented module, inputs collected and validated, and `main.tf`, `variables.tf`, and `terraform.tfvars` produced.
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

# Build OCI Security Zones Terraform

> **Adapted for the LoopyLuci Skills collection** from [oracle/skills](https://github.com/oracle/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Cloud Guard Security Zone recipes and Security Zones when requests must be mapped to the documented module, inputs collected and validated, and `main.tf`, `variables.tf`, and `terraform.tfvars` produced

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Generate or update Terraform configuration for OCI Security Zones using only the upstream `oci-landing-zones/terraform-oci-modules-security/tree/main/security-zones` module. Changes default to additive-only. Never invent module paths, input names, resource models, policy OCIDs, compartment relationships, or prerequisites, and never install or run Terraform.

## Required workflow

1. **Inspect before writing.** Review the project root, Terraform files, provider/backend setup, layout, and existing module blocks. For updates, removals, or deletions, read accessible local state read-only to confirm the exact state address; never modify state or run state commands. Treat a project as existing when one is in scope — otherwise ask for a target directory rather than hardcoding one. Read `references/module.md` first; if the request falls outside Security Zone recipes or Security Zones, reply "The Terraform module for `<capability>` is not supported by `oci-landing-zones/terraform-oci-modules-security/tree/main/security-zones`." Read `references/lifecycle-safety.md` for any non-additive request.

2. **Collect exact inputs.** Follow `references/input-collection.md`: `tenancy_ocid` (or a compartment OCID to resolve it through OCI MCP), the OCI group authorized to apply the configuration, at least one Security Zone definition with its recipe key, and the matching recipe definition. Before asking for `cis_level`, explain the CIS choices — the module default is `"1"` unless a top-level `default_cis_level` overrides it; Level 1 enables `deny public_buckets` and `deny db_instance_public_access`; Level 2 adds `deny block_volume_without_vault_key`, `deny boot_volume_without_vault_key`, `deny buckets_without_vault_key`, and `deny file_system_without_vault_key`. Ask the user to choose Level 1 or Level 2 or accept the default. Then ask whether to add specific Oracle Security Zone policies beyond the CIS baseline or to choose from the full catalog. Validate only user-supplied policy names or OCIDs through OCI MCP and add only the returned OCIDs to `security_policies_ocids`. For the catalog, list every active policy (name, description, services, category, OCID) in a Markdown table and let the user choose — never infer relevance and never omit entries. If the user declines, omit `security_policies_ocids`. Preserve literal OCIDs and stable logical keys; never infer a compartment OCID, policy OCID, reporting region, CIS level, or recipe-to-zone association from a name. Collect `compartments_dependency` only when a recipe or zone uses a compartment-reference key instead of a literal OCID. Offer documented optional inputs only after all required values exist; if declined, use documented defaults. Read the upstream `SPEC.md` before writing, and `references/terraform-sources.md` before writing a module block.

3. **Validate.** Follow `references/validation.md` after collection; apply every non-placeholder rule and pause for corrected values. Use OCI MCP read-only calls to confirm the supplied group has an active tenancy policy granting `manage cloud-guard-family in tenancy` or `manage all-resources in tenancy` — this check is mandatory; stop if OCI MCP is unavailable, listing fails, or neither authorization is found. Validate tenancy and literal compartment OCIDs through OCI MCP when available; never use the local OCI CLI or claim OCI-side validation. For a mutation of an existing resource, require confirmed Terraform-state ownership first.

4. **Generate.** Follow `references/main-tf-map.md`. In an existing project, preserve its layout, provider/backend blocks, naming, variables, and secret handling; make the smallest scoped change and never add a duplicate module block. In a new project, create exactly `main.tf`, `variables.tf`, and `terraform.tfvars`: provider baseline and module block in `main.tf`, typed declarations in `variables.tf`, validated non-secret values in `terraform.tfvars`.

5. **Hand off.** State that the module needs Terraform 1.3.0+ and `manage cloud-guard-family in tenancy` or `manage all-resources in tenancy`. Note that the module enables Cloud Guard when disabled and never disables it. Provide — but never run — `terraform init`, `terraform validate`, `terraform plan`, `terraform apply`, and state that the plan must be reviewed before apply, especially because associating a Security Zone with a compartment replaces any existing Cloud Guard target there and affects its subcompartments.

## Boundaries

- Source only `git::https://github.com/oci-landing-zones/terraform-oci-modules-security.git//security-zones?ref=<ref>`; default `<ref>` to `main` unless the user gives a release tag or commit SHA.
- Support only Security Zone recipes and Security Zones defined by `security_zones_configuration`. Do not generate Cloud Guard targets, detector recipes, responder recipes, responders, problem remediation, IAM, networks, Vault keys, or raw `oci_*` substitutes.
- Never run `terraform`, `tofu`, package managers, provider login, OCI write commands, or installs.
- Never create, modify, replace, move, delete, import, or unlock Terraform state; never create a lock file or `.terraform` directory.
- Never place private keys, passwords, tokens, or other secrets in `terraform.tfvars`, examples, or repository files.

## Reference routing

| Need at this stage | Read |
| --- | --- |
| Confirm supported capabilities and side effects | `references/module.md` |
| Collect recipes, zones, and optional inputs | `references/input-collection.md` |
| Update, remove, or destroy a resource | `references/lifecycle-safety.md` |
| Create source, provider, or project baseline | `references/terraform-sources.md` |
| Validate values and relationships | `references/validation.md` |
| Map validated values to Terraform files | `references/main-tf-map.md` |

## Verification

- [ ] Every capability resolved to the Security Zones module; unsupported requests refused with the required wording.
- [ ] CIS level explained and chosen before configuration was written.
- [ ] Mandatory tenancy policy check performed through OCI MCP.
- [ ] Only additive changes unless the user named the exact resource and mutation.
- [ ] No Terraform command was executed.

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
- Path: `_sources/oracle_skills/oci/oci-landing-zone-terraform-module/terraform-oci-module-security-zone-skill/SKILL.md`
- License: UPL-1.0 — Copyright (c) 2025 Oracle and/or its affiliates
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
