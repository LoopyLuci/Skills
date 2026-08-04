---
name: gke-productionize
description: Use when assessing and preparing GKE clusters and workloads for production readiness.
tags: [gke, kubernetes, google-cloud, production, reliability, security]
related_skills: [google-cloud-recipe-auth, google-cloud-waf-security, google-cloud-waf-cost-optimization]
---

# GKE Productionize Skill

Orchestrates comprehensive production readiness reviews for GKE clusters and workloads across scalability, security, reliability, observability, backup/DR, and cost optimization.

## Discovery Phase

```bash
# Cluster discovery
gcloud container clusters describe {cluster_name} --location {location} --project {project}

# Workload discovery
kubectl get deployment {app_name} -n {namespace} -o yaml
kubectl get hpa -n {namespace}
kubectl get pdb -n {namespace}
kubectl get networkpolicy -n {namespace}
```

## Production Readiness Areas

| Area | Action | Key Skill |
|------|--------|-----------|
| Scalability | Configure HPA, VPA, resource limits | `gke-workload-scaling` |
| Observability | Cloud Logging, Monitoring, Managed Prometheus | `gke-observability` |
| Reliability | Regional clusters, PDBs, health probes | `gke-reliability` |
| Security | Workload Identity, Network Policies, Shielded Nodes | `gke-platform-security` |
| Backup/DR | Backup for GKE, restore procedures | `gke-backup-dr` |
| Cost | Rightsizing, quotas, Spot VMs | `gke-cost-optimization` |

## Scoring

After assessment, provide RAG (Red/Amber/Green) status for each area with an overall readiness score.

## Common Pitfalls

- **Skipping discovery**: Always run discovery commands before making recommendations
- **Missing security basics**: Always check Pod Security Standards, dedicated service accounts, and NetworkPolicies
- **No backup plan**: Ensure Backup for GKE is configured for stateful workloads
- **Single-zone clusters**: Production clusters should be regional (multi-zone)

## Verification Checklist

- [ ] Cluster details gathered (Autopilot vs Standard, release channel)
- [ ] Workload resource requests/limits configured
- [ ] HPA and PDB configured for critical workloads
- [ ] Health probes (liveness, readiness, startup) configured
- [ ] Network policies enforce least-privilege
- [ ] Workload Identity configured for GCP API access
- [ ] Backup for GKE configured
