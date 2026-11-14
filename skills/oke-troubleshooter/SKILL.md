---
name: oke-troubleshooter
description: Use when the user wants to diagnose or root-cause issues with an OCI Kubernetes Engine cluster or workload.
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

# Oke Troubleshooter

> **Adapted for the LoopyLuci Skills collection** from [oracle/skills](https://github.com/oracle/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- The user wants to diagnose or root-cause issues with an OCI Kubernetes Engine cluster or workload

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Act as an experienced Site Reliability Engineer for OCI Kubernetes Engine and guide an evidence-driven investigation spanning Kubernetes signals and OCI infrastructure. Not for greenfield Terraform generation, GVA node-pool creation, or routine Multus deployment with no incident — those belong to the cluster generator, GVA deployer, and multihome skills.

Load references on demand: `symptom-triage.md` (symptom to diagnostic domains), `evidence-collectors.md` (command recipes), `final-report-template.md` (report shape), `../../shared/oci-resource-map.md` (Kubernetes-to-OCI mapping), and `../oke-multihome-deployer/references/oke-dpdk-mlx5-notes.md` (DPDK, Multus, mlx5, `vfio-pci`, hugepages, RDMA/verbs). Optional delegation accelerators — `oke-evidence-collector`, `oke-hypothesis-analyst`, `oke-lb-log-collector` — are used only when the runtime supports delegation and never block on it.

Helper scripts (global error contract: exit 0 success, 1 expected issues, 2 unexpected; JSON errors on stderr): `oke-discover.sh`, `oke-addon-health.sh`, `oke-pod-network-check.sh`, `oke-autoscaler-check.sh`, `oke-dns-check.sh`, `oke-ingress-check.sh`, `oke-private-endpoint-check.sh`, `oke-ocir-image-pull-check.sh`, `oke-workload-identity-check.sh`, `oke-incident-timeline.sh`, `oke-object-correlator.sh`.

## Execution mode

Run locally in the parent skill by default. Use the optional agents only as accelerators when delegation is clearly supported; if they are unavailable, disabled, or return malformed output, continue locally with the same command list and payload shape — never abort an investigation solely because delegation failed. Normalize local evidence to the JSON shape documented in `evidence-collectors.md`. Never run a mutating Kubernetes or OCI action without showing the exact command and getting explicit approval in this session: `kubectl apply`/`patch`/`annotate`/`delete`, `rollout restart`, `scale`, node cordon/drain/debug, OCI create/update/delete, and LB logging enablement are all approval-required, and approving one command does not approve follow-ups.

## Phase 0 — input and preflight

1. **Parse arguments.** `$ARGUMENTS` may hold a symptom string; if empty, ask for a concise description. Extract namespace hints and resource names.
2. **Discover cluster context.** Ask for the cluster name if absent, then list kubeconfig contexts and suggest likely names before prompting. Derive `active_cluster_region` from the active context and treat it as authoritative; resolve the cluster OCID from `~/.kube/config` where possible; use `~/.oci/config` only for auth/profile hints, never region selection. Run:
   ```bash
   bash ../../scripts/oke-discover.sh --cluster <name-or-ocid> [--region <region>] [--profile <oci-profile>] [--timeout <seconds>] [--kubeconfig <path>] [--deployment <name>]
   ```
   Always pass `--region <active_cluster_region>` to discovery and every later OCI call; never rely on an implicit or default region. Use the JSON output to populate `cluster_ocid`, `compartment_ocid`, `region`, `kubernetes_version`, and deployment namespace. If discovery reports a different region, flag the mismatch, keep `active_cluster_region` for subsequent commands, and confirm only if it blocks resolution. Prompt only for fields still missing after discovery.
   **Single-cluster scope:** the user-provided cluster is the only target for the whole session — no baseline checks or inventory against any other cluster. If the current `kubectl` context does not match the discovered identity, stop and ask the user to switch context or supply the correct kubeconfig. Retry OCI lookups only for the same cluster.
3. **Confirm context.** Ask only for remaining essentials: namespace, target Deployment/Service, time window (`15m` or `1h`, default `1h`), impact level.
4. **Tool availability.** Run `kubectl version --client` and `oci --version`; record `KUBECTL_AVAILABLE`/`OCI_AVAILABLE`, warn that evidence will be partial, and continue with what exists.
5. **Session state.** Initialize the state structure with symptom, namespace, time window, cluster/compartment/region, domains, a `dependency_map` (entrypoint, hops, critical path, latency budget), `fallbacks`, `evidence`, and a `node_doctor` block.

## Phase 1 — symptom triage

Load `symptom-triage.md` and identify candidate domains matching the symptom keywords (including application-performance cases such as "deployment nginx is slow"). Present them with brief rationales and let the user confirm, add, or remove domains and add focus (a pod, service, node pool, PVC, IAM entity). For latency symptoms, model dependency context before collecting evidence: request entrypoint (Ingress/API/Job), target deployment, downstream services, which hops are critical versus background, and baseline latency with per-hop budgets where known. Store the clarifying answers (`POD_NAME`, `SERVICE_NAME`, `DEPLOYMENT_NAME`, `LABEL_SELECTOR`, `BASELINE_LATENCY`, `DEPENDENCY_MAP`).

## Phase 2 — dependency path modeling

For latency or throughput symptoms, build a dependency map before running domain collectors: entrypoint, hops (from/to/protocol), critical path, and per-hop latency budgets. If the data is incomplete, continue with a partial map and mark the confidence reduction explicitly.

## Phase 3 — evidence collection

1. **Object graph first.** When enough selectors are known, run the correlator with all discovered selectors (even one known target):
   ```bash
   bash ../../scripts/oke-object-correlator.sh \
     --namespace <ns> --cluster-id <cluster_ocid> --compartment-id <compartment_ocid> --region <region> \
     [--pod <pod>] [--deployment <deployment>] [--service <service>] [--ingress <ingress>] [--pvc <pvc>] [--node <node>]
   ```
   Treat its output as evidence (`domain`, `graph.kubernetes`, `graph.oci`, `graph.edges`, `findings`, `anomalies`, `raw_snippets`, `fallback_used`) and use it to narrow follow-on checks: a Service backed by an unhealthy OCI Load Balancer points at backend sets, node subnets, NSGs, security lists, route tables, gateways/peering, and endpoint readiness; a Pod on a Node/Compute instance points at all primary and secondary VNIC attachments and their subnets, NSGs, route tables, node pool, and AD; a PVC backed by a Block Volume means comparing volume AD and attachment state before blaming CSI. If `fallback_used=true`, continue with domain collectors and call out which links could not be resolved.
2. **Per domain.** Look up commands in `evidence-collectors.md`, fill placeholders, and auto-run **read-only** commands without prompting. Never auto-run remediation: show the exact command, explain its impact, and wait for explicit approval. For networking/LB work prefer the delegated LB collector when available; otherwise run the LB commands locally and normalize the same fields, asking the user only when `logging_status` is `disabled`/`unknown` (report only / print command / run now). For OKE-specific domains prefer the helper scripts (`oke-addon-health.sh`, `oke-pod-network-check.sh`, `oke-autoscaler-check.sh`, `oke-dns-check.sh`, `oke-ingress-check.sh`, `oke-private-endpoint-check.sh`, `oke-ocir-image-pull-check.sh`, `oke-workload-identity-check.sh`, `oke-incident-timeline.sh`) over generic batches; treat their JSON as evidence with `domain`, `findings`, `anomalies`, `raw_snippets`, `fallback_used`.
3. **Node Doctor (optional, Node Health domain).** Start with one candidate node and ask before continuing to others; default the debug image to `docker.io/library/ubuntu` each run and allow override; present the exact sequence and get per-node confirmation:
   ```bash
   bash ../../scripts/node-doctor-run.sh --node <node-name> --image <image-name>
   ```
   Offer execute now / print commands only / skip. This flow is privileged and potentially disruptive — never auto-run. Capture `node_doctor_attempted`, `executed`, `node`, `image`, `result` (`pass|fail|unknown`), `command_rc`, findings, raw snippet, and fallback reason; on failure record the fallback and continue.
4. **Execute.** Build the collector payload (symptom, domains, namespace, time window, selectors, dependency map, object graph, fallbacks, compartment OCID), hand it to `oke-evidence-collector` if delegation is available, otherwise run locally and normalize. On delegated failure, fall back to local immediately.
5. **Summarize** key findings before analysis, noting `fallback_used` signals and missing data.

## Phase 4 — hypothesis ranking

Build the analyst payload (symptom, domains, dependency map, object graph, evidence, fallbacks). Delegate to `oke-hypothesis-analyst` when available; otherwise rank locally: 9–10 direct converging evidence for one root cause; 6–8 strong multi-signal correlation with limited ambiguity; 3–5 plausible but missing a decisive signal; 1–2 weak signal or mostly evidence-gap guidance. Each hypothesis carries a score, bottleneck hop attribution where relevant, evidence bullets, remediation commands, and prevention guidance. Prefer hypotheses supported by explicit graph edges across Kubernetes and OCI over isolated symptoms. Confirm that quoted evidence references real collected snippets; on delegated failure, rank locally.

## Phase 5 — report and next steps

Load `final-report-template.md` and present its structure: a table of top hypotheses with scores and a confidence level; for latency incidents a hop-by-hop budget table (expected p99, observed p99, delta, confidence); remediation commands in fenced blocks, executed only after the user approves the exact command; and concise prevention bullets. State limitations — missing tooling, failed commands, unexplored domains, missing dependency telemetry. Offer to rerun for another namespace/resource, deep-dive IAM/capacity/service-limit evidence, or export findings, and remind the user to redact sensitive data before sharing.

## Error handling and security

Missing CLI: continue with available evidence, set fallback flags, warn. Permission denied: include remediation such as ensuring the tenancy OCID can access the compartment. Delegation failure: continue locally. Unexpected script error: emit JSON per the contract and stop the current phase while keeping collected data. Never echo secret values or service-account tokens — redact with `***` — and avoid storing credentials in outputs or state.

## Latency walkthrough

For "deployment is slow" with downstream dependencies: capture symptom, namespace, deployment, and window; build the dependency map with per-hop budgets; compare observed hop p99 against budget, compute deltas, and attack the largest over-budget hop on the critical path first, validating with client- and server-side evidence; then re-measure end-to-end p99. Deliver actionable insight even from partial data.

## Verification

- [ ] Cluster identity confirmed and single-cluster scope enforced.
- [ ] Read-only evidence auto-run; every mutating command shown and approved.
- [ ] Object graph used to narrow domain checks.
- [ ] Evidence normalized to the documented JSON shape, fallbacks recorded.
- [ ] Hypotheses scored with evidence citations; limitations stated.
- [ ] No secrets echoed; report delivered in the template shape.

## Related Skills in This Repo

- [apexlang-inventory](../apexlang-inventory/SKILL.md) — Use when working with provides an overview of APEX application components, APEXlang syntax...
- [oke-gva-deployer](../oke-gva-deployer/SKILL.md) — Use when the user asks to enable, deploy, or configure Generic VNIC Attachment (GVA) for O...
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
- Path: `_sources/oracle_skills/oci/oke/skills/oke-troubleshooter/SKILL.md`
- License: UPL-1.0 — Copyright (c) 2025 Oracle and/or its affiliates
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
