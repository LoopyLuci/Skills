---
name: gitops-argocd-flux
description: "Use when implementing GitOps with ArgoCD or Flux."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [GitOps, ArgoCD, Flux, Kubernetes, declarative, continuous-delivery]
    related_skills: [kubernetes-deployment, ci-cd-pipeline-setup, continuous-integration-advanced, terraform-module-patterns]
---

# GitOps with ArgoCD and Flux

Implementing GitOps for Kubernetes deployments — from Git as single source of truth through automated sync, drift detection, and multi-cluster management.

## When to Use

- Declarative Kubernetes deployments via Git
- Automated drift detection and correction
- Multi-cluster and multi-environment management
- Progressive delivery (canary, blue-green)
- Compliance: audit trail via Git history

## GitOps Patterns

```yaml
# ArgoCD Application manifest
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app-prod
spec:
  project: default
  source:
    repoURL: https://github.com/company/gitops.git
    targetRevision: main
    path: apps/my-app/overlays/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true   # Remove resources not in Git
      selfHeal: true # Revert manual changes

# Flux Kustomization
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: apps
spec:
  interval: 5m
  sourceRef:
    kind: GitRepository
    name: flux-system
  path: ./apps/production
  prune: true
```

## Verification Checklist

- [ ] GitOps tool selected (ArgoCD or Flux)
- [ ] Repository structure organized (apps, envs, clusters)
- [ ] Automated sync configured (sync policy)
- [ ] Drift detection and self-healing enabled
- [ ] Secrets managed (SealedSecrets, External Secrets, SOPS)
- [ ] Multi-cluster support configured
- [ ] Rollback via Git revert tested
- [ ] Access control (RBAC for GitOps tool)
- [ ] Monitoring (sync status, health, notifications)
