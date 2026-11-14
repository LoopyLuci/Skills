---
name: oke-gva-deployer
description: Use when the user asks to enable, deploy, or configure Generic VNIC Attachment (GVA) for OCI Kubernetes Engine (OKE), create node pools with secondary VNIC profiles, review update plans for existing GVA node pools, map Application Resources to workloads, or explain GVA functionality, constraints, and scheduling behavior.
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

# OKE Generic VNIC Attachment (GVA) Deployer

> **Adapted for the LoopyLuci Skills collection** from [oracle/skills](https://github.com/oracle/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- The user asks to enable, deploy, or configure Generic VNIC Attachment (GVA) for OCI Kubernetes Engine (OKE), create node pools with secondary VNIC profiles, review update plans for existing GVA node pools, map Application Resources to workloads, or explain GVA functionality, constraints, and scheduling behavior

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

OKE Generic VNIC Attachment (GVA) adds secondary VNICs to node pools so pods can request dedicated network resources through Kubernetes extended resources. This skill deploys GVA, validates prerequisites, designs secondary VNIC profiles, creates or reviews node pools, and rolls out workloads that consume Application Resources. It prefers live OCI discovery over asking the user, and it keeps node-pool creation conversational rather than scripted.

## Hard constraints

- Never inspect existing node pools in this workflow: no `oci ce node-pool list` or `oci ce node-pool get`.
- Never collect node-level detail: skip `kubectl get nodes`, `kubectl describe node`, and similar unless the user explicitly asks for node information.
- Source required values only from cluster metadata (`oci ce cluster get`), networking discovery, and explicit user input.
- Node-pool creation is always interactive. Updates require an explicit review, and a non-interactive update command may run only when an update-specific interactive flow exists and the user approves it.
- Every new node-pool request re-collects mutable inputs — never reuse saved JSON payloads, old `tmp/` payloads, earlier-turn values, or previously generated commands without re-prompting in the current flow.
- Never begin discovery against an implicit or default cluster. Wait until the user names or selects the target cluster in the current turn.
- Never default to the OCI config region. Ask for the region in the current flow and use exactly that value in every OCI CLI call for the workflow.

Supporting material: `references/gva.md` (feature summary, constraints, sample CLI and pod specs) and `validation-report-template.md` (node-pool validation report format). Scripts: `../../scripts/gva-discover.sh` (cluster/subnet/NSG discovery) and `../../scripts/gva-menu.sh` (guided flow that prints a CLI command and test manifest).

## Phase 0 — Intake

1. Confirm the target cluster first. If the prompt lacks a cluster name, context, or OCID, ask before any discovery or command generation. Do not assume a default even if scripts offer one, and require explicit selection when multiple kube contexts exist.
2. Resolve the cluster OCID from `~/.kube/config` where possible.
3. Take tenancy defaults from `~/.oci/config` only for non-region values; the region always comes from the user.
4. Pull cluster details with the OCI CLI and auto-populate what it returns.
5. Prompt only for what is still missing.

If the cluster runs Flannel or Cilium rather than VCN-Native CNI, stop and explain that GVA is unsupported.

## Phase 1 — Fast discovery (mandatory first pass)

Run this narrow sequence before any broader sweep:

1. Resolve the cluster OCID from the kubeconfig.
2. Read cluster details:

```bash
oci ce cluster get --cluster-id <cluster-ocid> --region <region>
```

3. List VCNs in the cluster compartment only:

```bash
oci network vcn list --compartment-id <compartment-ocid> --region <region>
```

4. Ask which VCN to use.
5. List subnets in that VCN only:

```bash
oci network subnet list --compartment-id <compartment-ocid> --vcn-id <selected-vcn-ocid> --region <region>
```

6. List NSGs in that VCN (fall back to compartment scope if needed):

```bash
oci network nsg list --compartment-id <compartment-ocid> --vcn-id <selected-vcn-ocid> --region <region>
```

Only when this fails, fall back to the broader helper.

## Phase 1b — Discovery helper fallback

With OCI CLI authenticated:

```bash
bash ../../scripts/gva-discover.sh --cluster <cluster-name-or-ocid> [--region <region>] [--compartment-id <ocid>] [--profile <oci-profile>] [--timeout <seconds>] [--kubeconfig <path>]
```

Its JSON output populates cluster OCID, Kubernetes version, compartment OCID, region, the subnet list (name, OCID, CIDR), and the NSG list (name, OCID). Empty lists or failed calls degrade to manual prompts for that item; node-pool discovery is never the fallback.

## Phase 2 — Conversational menu UX (mandatory)

Drive configuration one item per turn in chat; never ask for several unrelated fields at once.

- Offer numeric choices (1, 2, 3…) or a direct custom value, and stay consistent about numeric menus.
- Availability Domains are the exception: accept only discovered AD selections, no free-text ADs.
- Label nothing "recommended" unless the user asks for recommendations.
- Expand menus when the user wants more options rather than truncating.
- Confirm each accepted value before moving on.
- Start a fresh create flow for mutable values (pool name, shape, count, subnet, AD, image, each GVA profile) even if a previous run gathered them already; an old `--from-json` body is never the source of truth.

Menu order:

1. VCN selection
2. `node_pool_name`
3. `node_shape`
4. Flex shape config (OCPUs + memory) when applicable
5. Node count
6. Availability Domains — allow one, two, or all three, comma-separated
7. Primary node subnet
8. Image, filtered to the cluster's Kubernetes version, with architecture/family compatibility checked before finalizing
9. Per secondary VNIC profile: `applicationResource` label, GVA secondary subnet, NSG selection (`none` allowed), `ipCount` (1–256)
10. Repeat step 9 while the user wants another profile.

Presentation rules:

- VCN and subnet menus list every discovered option with name, CIDR, and OCID or selectable key.
- Image menus list OKE images matching the cluster Kubernetes version; if metadata cannot prove shape compatibility, mark that check TODO/live and get explicit confirmation before finalizing.
- NSG menus list all discovered NSGs plus a "none" option.
- AD menus take numeric multi-select only (`1,2,3`) and reject custom values.
- When a validation rule narrows a menu (e.g. the secondary-subnet 2+ CIDR rule), render it in the full menu format (numeric key + name + CIDR), renumbered contiguously from `1..N` — never reuse original indices like `4,10,11`.

Compatibility guardrails:

- Validate image vs. node shape architecture/family before finalizing; on mismatch (ARM image, x86 shape) stop and have the user change one of them.
- Build one VNIC profile per secondary-VNIC entry from step 9/10.
- Reject any secondary subnet that is not IPv4-only (no IPv6 CIDR) or has fewer than two IPv4 CIDR blocks.

If the user asks for script automation you may run `bash ../../scripts/gva-menu.sh` or `bash ../../scripts/gva-discover.sh ...`, but keep the same conversational behavior and never let a script default pick the cluster.

## Phase 3 — Design the VNIC profiles

Produce a profile table with `applicationResource` (the label pods request), `subnetId`, `ipCount` (max 256), optional `nsgIds`, `displayName`, `assignPublicIp` (default false), and optional `tags`. Validate that each `applicationResource` is unique, total IPs cover the expected pod count plus buffer, subnets match the intended traffic isolation, and every GVA secondary subnet is IPv4-only with more than one IPv4 CIDR block.

## Phase 3b — Required-variable checklist

Collect and confirm all of these before generating create or update commands: cluster context/name, cluster OCID, region, compartment OCID, VCN OCID, Kubernetes version, node-pool name (explicit — never auto-finalized), node shape, OCPUs/memory for Flex, node count, Availability Domain(s), primary node subnet, image OCID matching the cluster Kubernetes version, the secondary VNIC profile list with each profile's `applicationResource`, subnet, NSG IDs, `ipCount` (1–256), recommended display name, whether more profiles are needed (explicit yes/no loop), optional parameters (tags, labels, boot volume, SSH key), and a final explicit create confirmation in the current turn.

## Phase 4 — Create node pool or review an update

Node-pool creation stays interactive: previews are fine, but do not execute non-interactive create or update commands.

Before creating, check that the installed OCI CLI has the GA GVA flags:

```bash
oci --version
oci ce node-pool create --help | grep -E 'secondary-vnics|cni-type'
```

If the flags are missing, stop and ask the operator to upgrade the regular OCI CLI through their normal install path — a preview CLI is no longer required. `../../scripts/gva-menu.sh` performs the same check; if it fails, print the command and ask for a CLI version with GVA flag support.

When the user works with the OCI CLI, build the create command from the confirmed profiles:

```bash
oci ce node-pool create \
  --compartment-id "<compartment_ocid>" \
  --cluster-id "<cluster_ocid>" \
  --name "<node_pool_name>" \
  --kubernetes-version "<k8s_version>" \
  --node-shape "<shape>" \
  --node-shape-config '{"ocpus":<n>,"memoryInGBs":<gb>}' \
  --size <node_count> \
  --cni-type OCI_VCN_IP_NATIVE \
  --placement-configs '[{"availabilityDomain":"<ad>","subnetId":"<primary_subnet_ocid>"}]' \
  --node-source-details '{"sourceType":"IMAGE","imageId":"<image_ocid>"}' \
  --secondary-vnics '<secondary_vnics_json>'
```

Use availability domains discovered from IAM for the tenant (e.g. `GrCh:US-ASHBURN-AD-1`), not guessed aliases. For Terraform users, ask which module/resource they use and map the same profile fields without guessing.

## Phase 5 — Verify node resources

Give the user these read-only verification steps (do not run node queries yourself) and ask them to confirm GVA resources on the nodes:

```bash
kubectl describe node <node_name>
```

Expected signals: extended resources such as `oke-application-resource.oci.oraclecloud.com/<AppResource>` and the taint `oci.oraclecloud.com/application-resource-only:NoSchedule`.

## Phase 6 — Deploy workloads

Provide a pod/deployment snippet that requests exactly one unit of the chosen Application Resource and tolerates the GVA taint. Restate the validation rules for the user: exactly one Application Resource type per pod, resource count exactly 1, and pods without the toleration will not schedule.

## Troubleshooting quick hits

- **Pods Pending** — no available IPs for the requested resource, missing toleration, or wrong resource name.
- **Validation webhook errors** — the pod requests multiple resources or a wrong count.
- **Capacity** — grow the node pool or rebalance `ipCount` across profiles.

## Deliverables

1. A short explanation of how GVA works.
2. The finalized VNIC profile table.
3. A ready-to-run CLI command (or Terraform mapping notes).
4. A sample workload manifest.
5. A verification checklist with pass/fail placeholders for node-resource validation after `kubectl describe node <node_name>`.
6. A final validation report following `validation-report-template.md` once post-create evidence exists.

## Sources

- https://docs.oracle.com/en-us/iaas/Content/ContEng/Tasks/contengAttaching_Multiple_VNICs.htm
- https://docs.oracle.com/en-us/iaas/Content/ContEng/Concepts/contengpodnetworking_topic-OCI_CNI_plugin.htm
- https://docs.oracle.com/en-us/iaas/tools/oci-cli/latest/oci_cli_docs/cmdref/ce/node-pool/create.html
- https://docs.oracle.com/en-us/iaas/tools/oci-cli/latest/oci_cli_docs/cmdref/ce/node-pool/update.html
- https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
- https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/

## Related Skills in This Repo

- [apexlang-inventory](../apexlang-inventory/SKILL.md) — Use when working with provides an overview of APEX application components, APEXlang syntax...
- [oke-troubleshooter](../oke-troubleshooter/SKILL.md) — Use when the user wants to diagnose or root-cause issues with an OCI Kubernetes Engine clu...
- [oci-functions-deploy](../oci-functions-deploy/SKILL.md) — Use when asked to validate/install Fn, OCI CLI, and Docker, configure or create Fn context...
- [oke-cluster-generator](../oke-cluster-generator/SKILL.md) — Use when the user asks to build, generate, create, design, or scaffold an OKE (OCI Kuberne...

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [oracle/skills](https://github.com/oracle/skills)
- Path: `_sources/oracle_skills/oci/oke/skills/oke-gva-deployer/SKILL.md`
- License: UPL-1.0 — Copyright (c) 2025 Oracle and/or its affiliates
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
