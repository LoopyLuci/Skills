---
name: build-oci-iam-main-tf
description: Use when oCI compartments and hierarchy, classic IAM groups (including member assignment), dynamic groups, IAM policies, and OCI Identity Domains resources when the request must be mapped to a supported upstream module, inputs collected and validated, and `main.tf`, `variables.tf`, and `terraform.tfvars` produced.
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

# Build OCI IAM Terraform

> **Adapted for the LoopyLuci Skills collection** from [oracle/skills](https://github.com/oracle/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- OCI compartments and hierarchy, classic IAM groups (including member assignment), dynamic groups, IAM policies, and OCI Identity Domains resources when the request must be mapped to a supported upstream module, inputs collected and validated, and `main.tf`, `variables.tf`, and `terraform.tfvars` produced

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Generate or update safe Terraform root configuration for OCI IAM using only the upstream `oci-landing-zones/terraform-oci-modules-iam` repository. Changes default to additive-only. Never invent module paths, input names, or resource models; never mutate, replace, rename, move, or re-parent an existing resource unless the user explicitly asks for that exact change; never install or run Terraform.

## Required workflow

1. **Inspect before writing.** Review the project root, Terraform files, repository documentation, provider/backend setup, and established layout — a `.tf` file is only one signal, so do not let its presence or absence alone define the project. For update, move, recovery, removal, or deletion, read any accessible local state file read-only to establish the exact state address; never modify state or run a state command. Treat a project as existing when one is in scope; otherwise create a minimal configuration in a user-selected target directory, asking for the target if none is given. Proceed on an existing-resource change only when the user explicitly names that resource and the intended mutation; otherwise stop and ask. Read `references/module-support.md` first and resolve each requested capability to an exact supported subdirectory. If a capability has no supported module, do not substitute an alternative: reply "The Terraform module for `<capability>` is not supported by `oci-landing-zones/terraform-oci-modules-iam`." Read `references/lifecycle-safety.md` before collecting inputs for any update, move, recovery, removal, or deletion.

2. **Collect inputs by module.** Read only the relevant section of `references/input-collection.md` (compartments, groups, dynamic groups, policies, or Identity Domains). Ask concise follow-ups for missing required values; preserve literal OCIDs and parent-child relationships rather than fabricating them. Once required inputs are complete and before reading `validation.md`, ask whether the user wants to supply documented optional parameters — do not read `validation.md` until they provide them or explicitly decline. If declined, use documented defaults only. Read `references/terraform-sources.md` before creating any module block.

3. **Validate.** Read `references/validation.md` after all requested inputs are collected and apply every non-placeholder rule; pause for a corrected value if an input is missing or known invalid. If OCI MCP is unavailable, say MCP validation was skipped and continue with non-MCP rules only. For update, move, recovery, removal, or destroy requests, require Terraform-state existence before proposing the mutation. Where a dedicated validation section does not yet exist for the resource family, apply the common rules plus its collection-reference structural checks — do not invent rules.

4. **Generate.** Read `references/main-tf-map.md` and the relevant source snippets. In an existing project, preserve its style and layout: file placement, formatting, naming, variable-data convention, provider/backend configuration, module organization, and Terraform version constraints. Make the smallest additive change and touch `main.tf`, `variables.tf`, or `terraform.tfvars` only where compatible. In a new project, create exactly those three files: provider block and required-provider constraint in `main.tf`, declarations and types in `variables.tf`, validated non-secret example values in `terraform.tfvars`. Keep authentication values as variables; never place private keys, API keys, tokens, or passwords in `terraform.tfvars`.

5. **Hand off.** Tell the user the upstream modules require Terraform 1.3.0 or later. Provide, but never run, `terraform init`, `terraform validate`, `terraform plan`, and `terraform apply`, and state that the plan must be reviewed before apply.

## Boundaries

- Use only the source repository and subdirectories listed in `module-support.md`.
- Never silently substitute direct `oci_*` resources for an unavailable submodule.
- A classic IAM **group** can assign existing user names as members; there is no separate `users` or `memberships` top-level module, so reject requests to create users or manage memberships independently.
- Do not claim Cloud Guard support — it belongs to other OCI landing-zone collections.
- Never run `terraform`, `tofu`, package managers, provider login, or installs.
- Never create, modify, replace, move, or delete a state file, and never create a lock file or `.terraform` directory.

## Reference routing

```text
request
  -> module-support.md
       -> unsupported: report "Terraform module is not supported" and stop
       -> supported: relevant input reference + terraform-sources.md
            -> validation.md
                 -> main-tf-map.md
                      -> generate or update the project files
```

| Need at this stage | Read |
| --- | --- |
| Confirm an exact submodule or reject a request | `references/module-support.md` |
| Update, move, recover, remove, or delete a resource | `references/lifecycle-safety.md` |
| Build exact Git sources and provider baseline | `references/terraform-sources.md` |
| Collect groups / dynamic groups / policies / compartments / Identity Domains | `references/input-collection.md` |
| Map validated values to files | `references/main-tf-map.md` |
| Apply the validation contract | `references/validation.md` |

## Verification

- [ ] Every capability resolved to a supported IAM submodule; unsupported requests refused.
- [ ] Optional-input question asked before validation.
- [ ] Existing project style preserved; smallest additive change only.
- [ ] No secrets in `terraform.tfvars`.
- [ ] No Terraform command executed.

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
- Path: `_sources/oracle_skills/oci/oci-landing-zone-terraform-module/terraform-oci-modules-iam-skill/SKILL.md`
- License: UPL-1.0 — Copyright (c) 2025 Oracle and/or its affiliates
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
