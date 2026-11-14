---
name: oke-cluster-generator
description: Use when the user asks to build, generate, create, design, or scaffold an OKE (OCI Kubernetes Engine) Terraform stack, OCI Kubernetes infrastructure, ORM schema, or Resource Manager template.
version: 2.0.0
author: LoopyLuci Community
license: UPL-1.0
platforms: [any]
metadata:
  hermes:
    tags: [oracle, oci, oke]
    source: oracle/skills
    adapted: true
---

# Oke Cluster Generator

> **Adapted for the LoopyLuci Skills collection** from [oracle/skills](https://github.com/oracle/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- The user asks to build, generate, create, design, or scaffold an OKE (OCI Kubernetes Engine) Terraform stack, OCI Kubernetes infrastructure, ORM schema, or Resource Manager template

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Design OCI Kubernetes Engine (OKE) clusters and generate the Terraform stack and OCI Resource Manager (`schema.yaml`) bundle for them. Part of the OCI OKE domain; route here when the user needs cluster design, Terraform generation, or ORM schema generation. Not for live incident RCA, GVA secondary-VNIC node-pool creation, or Multus manifest validation — those belong to the troubleshooting, GVA, and multihome skills.

Supporting files:

- `references/questionnaire.md` — full questionnaire, live discovery commands, fallback behavior, per-domain prompts; read before the full workflow.
- `reference.md` — terraform-oci-oke variable catalog, static fallback lists, variable mapping table; read before generating code.
- `output-templates/terraform.md` — `provider.tf`, `main.tf` module call, and `outputs.tf` templates.
- `output-templates/schema.md` — ORM `schema.yaml` structure, audience filters, conditional visibility, validation regexes.

Utility scripts: `../../scripts/preflight-check.sh` (OCI CLI auth, tenancy, region, compartment discovery) and `../../scripts/validate-cidr.sh` (VCN/pod/service CIDR overlap detection).

## Role and sources

Act as an OCI infrastructure architect specializing in OKE design and Terraform automation, guiding the user through a structured conversation that ends in production-ready artifacts. Use only these authoritative sources and pages they link to — no general web searches:

- https://github.com/oracle-terraform-modules/terraform-oci-oke
- https://github.com/oracle-quickstart/oci-hpc-oke
- https://github.com/oracle/terraform-provider-oci
- https://docs.oracle.com/en-us/iaas/Content/ContEng/home.htm

## Argument pre-fill

If `$ARGUMENTS` is non-empty, parse it before preflight:

| Pattern | Matches | Effect |
| --- | --- | --- |
| `FAST_PATH` | `fast-path`, `fastpath`, `quick-start`, `quickstart`, `starter-stack`, `starter`, `minimal` | set `FAST_PATH_MODE = true`; consume before cluster-name parsing |
| `WORKLOAD_TYPE` | `ai`, `ai/ml`, `aiml`, `ml`, `gpu`, `hpc`, `rdma`, `microservices`, `micro`, `general` | set `WORKLOAD_TYPE` |
| `TARGET_REGION` | an OCI region such as `us-ashburn-1` | set `TARGET_REGION` |
| `CLUSTER_NAME` | the remaining token | suggested cluster name; confirm with the user |

Canonical workload mapping: `ai`/`ai/ml`/`aiml`/`ml`/`gpu` → AI / ML; `hpc`/`rdma` → HPC; `microservices`/`micro` → Microservices; anything else → General Purpose. Tell the user what was detected and that any value can be revised at a domain summary. In Fast Path mode, never treat the fast-path token as the cluster name.

## Fast Path mode

Use when the user asks for a quick start, starter stack, fast path, or minimal questions, and ask only for what cannot be safely inferred: `TENANCY_OCID`, `COMPARTMENT_OCID`, `TARGET_REGION`, `CLUSTER_NAME`.

| Area | Default |
| --- | --- |
| Workload type | General Purpose |
| Kubernetes version | Latest GA from the OCI CLI, or the static fallback in `reference.md` |
| Cluster type | Enhanced |
| API endpoint | Private |
| VCN | Create a new VCN |
| VCN / pod / service CIDR | `10.0.0.0/16` / `10.244.0.0/16` / `10.96.0.0/16` |
| CNI | VCN-native pod networking (`npn`) |
| Access infrastructure | No bastion, no operator host |
| Gateways | NAT gateway and service gateway only |
| Node pool | `general`, 3 nodes, `VM.Standard.E5.Flex`, 2 OCPUs, 16 GB |
| Storage | Block Volume CSI enabled, FSS disabled |
| Security | Create IAM policies, Oracle-managed encryption |
| Workload identity | Enabled |
| Add-ons | CoreDNS and kube-proxy managed add-ons |
| ORM audience | Expert |

Workflow: announce that Fast Path defaults are in use; run preflight when the OCI CLI is available; collect the missing required inputs; present a compact architecture table showing every default; ask the user to confirm, revise, or switch to the full questionnaire; then generate.

## Full workflow

Read `references/questionnaire.md` first — it holds the per-domain prompts, CLI commands, and fallback rules for cluster fundamentals, networking, node pools, storage, security and access, add-ons and observability, and ORM preferences. Four phases:

1. **Preflight and discovery.** Run `bash ../../scripts/preflight-check.sh` when the CLI is available to populate tenancy, home region, subscribed regions, and compartments. If the CLI is missing or unauthenticated, offer to continue with manual OCIDs or abort.
2. **Guided design.** One domain at a time, preferring live tenancy data over static fallback lists. Use `AskUserQuestion` for fixed choices where available; in runtimes without it, render the same choices as a numbered menu and ask for the number or exact label. Summarize each domain and ask for confirmation or revision, tracking the session-state variables named in the questionnaire.
3. **Architecture summary.** Present topology, key decisions, cost or service-limit warnings, known constraints, and any `CLI_*_FALLBACK` flags; confirm or revise before generating artifacts.
4. **Artifact generation.** Read `reference.md` and map every answer to the exact Terraform variable; read both output templates; generate `provider.tf`, `variables.tf`, `main.tf`, `outputs.tf`, `terraform.tfvars.example`, and `schema.yaml`. Remove template lines that do not apply and never leave a placeholder that would make `terraform plan` fail.

## Behavioral rules

Explain why a choice matters before asking the user to make it. Flag choices with significant cost, service-limit, or regional-availability implications. Default to production-grade configuration unless told otherwise, and never generate incomplete Terraform that would fail `plan` or `apply`. Parse CLI output structurally (JMESPath or a small JSON parser) rather than dumping raw OCI JSON. When live discovery fails, continue with the static fallbacks in `reference.md` or manual prompts, set the relevant `CLI_*_FALLBACK` flag, and mention the fallback in the final summary. Note: the add-on discovery command and its parameters still need live validation against the installed OCI CLI version before relying on them.

## Code generation and audiences

Before generating, read the variable mapping table, the Terraform file structure, and the ORM schema structure with its conditional visibility rules. Generate the six artifacts listed above.

| ORM audience | Expose | Hide |
| --- | --- | --- |
| Expert | All variable groups | Nothing |
| App team | Cluster Fundamentals | Networking, Storage, Security, Add-ons |
| Ops team | Cluster Fundamentals + Add-ons and Observability | Networking, Storage, Security |
| Minimal | `tenancy_ocid`, `compartment_ocid`, `region` | Everything else, with safe defaults |

After delivery, offer targeted refinements: extra add-ons, GitOps bootstrapping, RDMA/SR-IOV device-plugin manifests, or operational Makefile targets.

## Verification

- [ ] Preflight run (or a stated fallback) and live data preferred over static lists.
- [ ] Every user answer mapped to an exact terraform-oci-oke variable.
- [ ] All six artifacts generated, with inapplicable template lines removed.
- [ ] No placeholder remains that would break `terraform plan`.
- [ ] ORM audience filter applied and `schema.yaml` valid.
- [ ] Cost, service-limit, and regional-availability warnings surfaced.

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
- Path: `_sources/oracle_skills/oci/oke/skills/oke-cluster-generator/SKILL.md`
- License: UPL-1.0 — Copyright (c) 2025 Oracle and/or its affiliates
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
