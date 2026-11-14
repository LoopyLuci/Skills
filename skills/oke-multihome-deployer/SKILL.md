---
name: oke-multihome-deployer
description: Use when the user asks to auto-discover OKE cluster subnets or node pools for multihome, create OKE multihome pod manifests, configure Multus NADs for secondary VNIC interfaces, validate multihomed pod connectivity, inspect OCI CNI IPAM allocation on OKE nodes, or package repeatable OKE GVA multihome deployment steps.
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

# OKE Multihome Deployer

> **Adapted for the LoopyLuci Skills collection** from [oracle/skills](https://github.com/oracle/skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- The user asks to auto-discover OKE cluster subnets or node pools for multihome, create OKE multihome pod manifests, configure Multus NADs for secondary VNIC interfaces, validate multihomed pod connectivity, inspect OCI CNI IPAM allocation on OKE nodes, or package repeatable OKE GVA multihome deployment steps

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Deploy and verify Multus-based pod multihoming on OCI Kubernetes Engine, on top of an OKE node pool that already has GVA secondary VNIC profiles attached. Do not use this skill to create or update GVA node pools — run `oke-gva-deployer` first for that. For broad incident RCA, DPDK/SR-IOV failures, or non-Multus pod symptoms, start with `oke-troubleshooter`.

## Core workflow

1. **Confirm target cluster/context and auth.** Prefer explicit `OCI_CLI_PROFILE` and `OCI_CLI_AUTH`; with OCI security-token auth pass `--auth security_token` or set `OCI_CLI_AUTH=security_token`. If `kubectl` fails with `exec: executable oci failed`, ask the user to refresh the OCI session before applying anything.
2. **Discover cluster, node pool, and subnet data before generating YAML.** Run `scripts/discover-oke-multihome.py`, preferring `--cluster-id` when the user supplies it, otherwise `--context`, then `--cluster-name` with `--compartment-id`. The script queries OKE node pools and fetches every referenced placement and secondary VNIC subnet. Use the discovered node names for `--pod NAME=NODE_NAME` entries.
3. **Verify prerequisites from Kubernetes and node-side checks.** OKE CNI must be `OCI_VCN_IP_NATIVE`; worker nodes must expose secondary VNIC interfaces (treat `enp1s0` and `enp2s0` as common defaults, then confirm the real names from discovery or node evidence); the OCI CNI binaries `oci-ipam`, `oci-ipvlan`, and `oci-ptp` should exist on nodes; a plain `ipvlan` CNI binary is needed for a plain `ipvlan` secondary NAD.
4. **Install the Multus thick plugin if absent**, from `https://raw.githubusercontent.com/k8snetworkplumbingwg/multus-cni/master/deployments/multus-daemonset-thick.yml`. This manifest is not yet pinned to a tested release tag — keep the repository's current reference until live validation against the target OKE Kubernetes version is complete.
5. **Generate or edit the deployment manifest** with `scripts/generate-multihome-manifest.py`. The default network NAD is `kube-system/gva-default-network` using `oci-ipvlan` on the first secondary VNIC path; the secondary NAD is workload-namespace scoped, using `ipvlan` on the second path with `oci-ipam`.
6. **Apply and verify.** Use fully qualified images such as `docker.io/nicolaka/netshoot:v0.13` (CRI-O may reject short names). Check the pod annotation `k8s.v1.cni.cncf.io/network-status`, exec `ip -br addr` in each pod, and ping the peer `net1` IP in both directions. Report with `validation-report-template.md` whether validation passed, failed, or remains incomplete.

## Discovery

```bash
OCI_CLI_PROFILE=<oci-profile> OCI_CLI_AUTH=<oci-auth-mode> \
python3 <skill>/scripts/discover-oke-multihome.py \
  --cluster-id <cluster_ocid> --region <region> --pretty > oke-multihome-discovery.json
```

If the kubeconfig's exec user args already contain the cluster OCID, use `--context <kubectl_context>` instead. From the JSON, choose the node pool with GVA `secondaryVnics`, the primary placement subnets, the secondary VNIC subnet IDs/CIDRs that decide which interface path maps to which pod network, and up to two ready node names for pinned smoke-test pods. Never guess subnet CIDRs or node names when discovery can retrieve them.

## Manifest generation

```bash
python3 <skill>/scripts/generate-multihome-manifest.py \
  --namespace gva-multihome-test \
  --default-interface <confirmed-first-secondary-vnic-interface> \
  --secondary-interface <confirmed-second-secondary-vnic-interface> \
  --pod gva-multihome-a=<node-name-a> \
  --pod gva-multihome-b=<node-name-b> \
  > gva-multihome-pods.yaml
```

Use Kubernetes node names exactly as `kubectl get nodes` returns them; in OKE clusters configured like the handoff, node names may be node private IPs.

## Verification commands

```bash
kubectl -n kube-system get pods -l name=multus -o wide
kubectl -n gva-multihome-test get pods -o wide
kubectl -n gva-multihome-test exec gva-multihome-a -- ip -br addr
kubectl -n gva-multihome-test exec gva-multihome-b -- ip -br addr
kubectl -n gva-multihome-test exec gva-multihome-a -- ping -c 3 -W 2 <pod-b-net1-ip>
kubectl -n gva-multihome-test exec gva-multihome-b -- ping -c 3 -W 2 <pod-a-net1-ip>
```

Inspect the network-status annotation:

```bash
kubectl -n gva-multihome-test get pod gva-multihome-a gva-multihome-b \
  -o jsonpath='{range .items[*]}{.metadata.name}{" on "}{.spec.nodeName}{"\n"}{.metadata.annotations.k8s\.v1\.cni\.cncf\.io/network-status}{"\n\n"}{end}'
```

## Troubleshooting

Read `references/oke-multihome-notes.md` when Multus pods are missing or failing, pods are stuck creating a sandbox or network, `ipvlan` is missing on the host, OCI IPAM capacity or allocation behavior is unclear, or floating IP/VIP behavior is being explored. Read `references/oke-dpdk-mlx5-notes.md` when the workload uses DPDK, SR-IOV device-plugin resources, Mellanox/NVIDIA VFs, `mlx5`, `vfio-pci`, hugepages, or `/dev/infiniband`; when a pod requests Multus networks and device-plugin resources but `network-status` shows only `eth0`; or when deciding whether the fault is Multus/NAD attachment, resource allocation, driver binding, RDMA/verbs exposure, hugepages, or app PCI/interface mapping. For node-side inspection, prefer a privileged diagnostic DaemonSet that mounts `/` at `/host` and runs `chroot /host`, rather than SSHing to each worker.

## Sources

- https://docs.oracle.com/en-us/iaas/Content/ContEng/Tasks/contengAttaching_Multiple_VNICs.htm
- https://docs.oracle.com/en-us/iaas/Content/ContEng/Concepts/contengpodnetworking_topic-OCI_CNI_plugin.htm
- https://github.com/k8snetworkplumbingwg/multus-cni
- https://github.com/k8snetworkplumbingwg/network-attachment-definition-client
- https://www.cni.dev/plugins/current/main/ipvlan/
- https://kubernetes.io/docs/tasks/debug/debug-cluster/kubectl-node-debug/

## Verification

- [ ] GVA secondary VNIC profiles already present; discovery run and its output used.
- [ ] OKE CNI is `OCI_VCN_IP_NATIVE`; secondary interfaces confirmed from evidence.
- [ ] Multus thick plugin installed; manifests generated by script, not hand-written.
- [ ] `network-status` shows both interfaces; bidirectional `net1` ping succeeds.
- [ ] Validation report produced, including when validation failed or is incomplete.

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
- Path: `_sources/oracle_skills/oci/oke/skills/oke-multihome-deployer/SKILL.md`
- License: UPL-1.0 — Copyright (c) 2025 Oracle and/or its affiliates
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
