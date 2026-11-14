---
name: build-oci-exadata-database-main-tf
description: Use when cloud Exadata Infrastructure, Cloud VM Clusters, DB Homes, Container Databases, and Pluggable Databases.
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

# Build OCI Exadata Database Terraform

> **Adapted for the LoopyLuci Skills collection** from [oracle/skills](https://github.com/oracle/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Cloud Exadata Infrastructure, Cloud VM Clusters, DB Homes, Container Databases, and Pluggable Databases

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Generates — and updates — Terraform configuration restricted to OCI Exadata Database Service on Dedicated Infrastructure, mapped strictly onto the upstream `exadata-database` module. Changes default to additive-only, only the module's five resource families are ever produced, and nothing outside the module (IAM, network, object-storage prerequisites, Terraform execution) is touched. Deployment prerequisites such as VCNs, subnets, and Object Storage are explained as non-blocking deployment context, never used as gates on generating configuration.

## Required Workflow

1. **Inspect the target before writing.** Survey the project root, Terraform files, provider/backend setup, established layout, and existing module blocks. For an update, recovery, removal, or deletion request, inspect accessible local Terraform state read-only for the exact state address; never modify state or run Terraform state commands. Treat a project or configuration in scope as an existing project; otherwise ask for a target directory rather than hardcoding one or overwriting unrelated files. Read `references/module.md` first — if the request falls outside the module's five resource families, say: **"The Terraform module for `<capability>` is not supported by `oci-landing-zones/terraform-oci-modules-oracle-database/tree/main/exadata-database`."** Read `references/lifecycle-safety.md` for any non-additive request.
2. **Collect inputs in dependency order.** Read `references/reference.md` (informational deployment context, not a generation gate) and the applicable sections of `references/input-collection.md`. Collect shared tenancy and compartment values first; collect VCN/subnet, subscription, and SSH-key values only for the resource families that use them, in infrastructure → VM cluster → DB home → database → PDB order. Validate only values supplied by the user or required in the requested module object — never request VCN, subnet, route, NSG, or Object Storage values for a standalone `cloud_exadata_infrastructures_configuration`, and never block generation for an operational deployment prerequisite that is not an input of the requested object. Read the upstream `SPEC.md` before writing any resource objects. Preserve literal OCIDs and map-key references; do not infer an OCID, availability domain, database/GI/system version, capacity, or network topology. Offer documented optional inputs only after all required inputs are present; if declined, use documented defaults and never invent optional values. Treat database passwords, TDE wallet passwords, API private-key passwords, and remote-clone credentials as secrets — keep them out of tracked files, never echo them back, and use a secure secret-injection mechanism already established by the project. Read `references/terraform-sources.md` before writing a module block.
3. **Validate before producing usable configuration.** Read `references/validation.md` only after inputs are collected, and apply every non-placeholder rule. OCI MCP validation is mandatory: pause if the `get_oci_command_help` and `run_oci_command` OCI MCP tools are unavailable or cannot be invoked, and pause for a corrected value when an input is missing or known invalid. Do not claim OCI-side availability, quota, capacity, version compatibility, or IAM access has been verified unless it was actually verified through the required OCI MCP read. For mutations of existing resources, require confirmed Terraform-state ownership first.
4. **Generate after validation succeeds.** Read `references/main-tf-map.md`. In an existing project, preserve its layout, provider/backend blocks, naming, variables, and secret-handling approach; make the smallest scoped change and do not add a duplicate module block. In a new project, create exactly `main.tf`, `variables.tf`, and `terraform.tfvars`: the OCI provider baseline and module block go in `main.tf`, typed declarations in `variables.tf`, and only validated non-secret literal values in `terraform.tfvars`. Never place Terraform functions, interpolations, traversals, or dynamic expressions (including `file()`, `templatefile()`, `${...}`, or `path.module`) in a `.tfvars` file. Resolve repository-local public-key files in `main.tf` with a local value or module-argument merge, making the corresponding variable attribute optional when that expression supplies it. Default the module source to `ref=main`; use a release tag or commit SHA only when the user explicitly provides one, and do not ask the user to approve the default.
5. **Hand off without execution.** Tell the user this upstream module requires Terraform 1.5.0 or later. Provide, but never run: `terraform init`, `terraform validate`, `terraform plan`, and `terraform apply`. Explain that an Exadata operation can take many hours and the plan must be reviewed before apply; note that upstream documentation says a later apply may resume after certain transient provisioning conflicts — without promising that it will.

## Boundaries

- Use only `git::https://github.com/oci-landing-zones/terraform-oci-modules-oracle-database.git//exadata-database?ref=<ref>` for the module source, defaulting `<ref>` to `main` unless the user explicitly provides a release tag or commit SHA. Treat `https://github.com/oci-landing-zones/terraform-oci-modules-oracle-database/tree/main/exadata-database` as the canonical upstream folder path.
- Support only Cloud Exadata Infrastructure, Cloud VM Clusters, DB Homes, Container Databases, and Pluggable Databases. Do not generate IAM, VCN, subnet, route-table, gateway, NSG, or Object Storage prerequisite resources; do not substitute direct `oci_*` resources or a different module.
- Do not run `terraform`, `tofu`, package-manager, provider-login, OCI write, or install commands.
- Do not create, modify, replace, move, delete, import, or unlock Terraform state; do not create a lock file or `.terraform` directory.
- Do not put private-key material, passwords, tokens, or wallet secrets in `terraform.tfvars`, examples, or repository files.

## Reference Routing

| Need at this stage | Read |
| --- | --- |
| Confirm supported capabilities and module contract | `references/module.md` |
| Confirm deployment prerequisites and network baseline | `references/reference.md` |
| Collect resource-family inputs | `references/input-collection.md` |
| Update, remove, recover, or destroy a resource | `references/lifecycle-safety.md` |
| Create the source, provider, or minimal project baseline | `references/terraform-sources.md` |
| Validate values and dependencies | `references/validation.md` |
| Map validated values to Terraform files | `references/main-tf-map.md` |

## Verification

- [ ] `references/module.md` checked first; unsupported capabilities declined with the exact quoted sentence
- [ ] Target project inspected; state read-only for non-additive requests; existing layout preserved on updates
- [ ] Only requested-object inputs validated — no VCN/subnet/NSG/Object Storage collection for standalone infrastructure configs, and no blocking on operational prerequisites
- [ ] Secrets kept out of tracked files using the project's established injection mechanism
- [ ] OCI MCP validation performed; pauses raised rather than claiming unverified availability, quota, version, or IAM facts
- [ ] New projects contain exactly `main.tf`, `variables.tf`, `terraform.tfvars`, with `.tfvars` holding only validated non-secret literals
- [ ] Module source pinned to `ref=main` (or a user-supplied tag/SHA); no duplicate module blocks
- [ ] Handoff states the Terraform 1.5.0+ requirement and provides — but does not run — init, validate, plan, and apply

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
- Path: `_sources/oracle_skills/oci/oci-landing-zone-terraform-module/terraform-oci-modules-exadata-database-skill/SKILL.md`
- License: UPL-1.0 — Copyright (c) 2025 Oracle and/or its affiliates
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
