---

name: kubernetes-pod-design
description: "Use when designing Kubernetes pod configurations."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [kubernetes, pods, containers, probes, resources, init-containers]
    related_skills: [kubernetes-deployment, container-security-hardening, gitops-argocd-flux]

---

# Kubernetes Pod Design

Designing Kubernetes pod configurations — from resource requests/limits through liveness/readiness probes, init containers, and pod security contexts.

## When to Use

- Configuring Kubernetes pods for production
- Setting resource requests and limits
- Implementing health check probes
- Pod security and service mesh sidecars

## Pod Design Patterns

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: production-pod
spec:
  securityContext:
    runAsNonRoot: true
    seccompProfile: { type: RuntimeDefault }
  initContainers:
  - name: init-db
    image: busybox
    command: ['sh', '-c', 'until nc -z db-service 5432; do sleep 1; done']
  containers:
  - name: app
    image: app:1.0
    resources:
      requests: { cpu: 250m, memory: 256Mi }
      limits:   { cpu: 500m, memory: 512Mi }
    livenessProbe:
      httpGet: { path: /healthz, port: 8080 }
      initialDelaySeconds: 30
    readinessProbe:
      httpGet: { path: /ready, port: 8080 }
      initialDelaySeconds: 5
```

## Verification Checklist

- [ ] Resource requests and limits set for all containers
- [ ] Liveness and readiness probes configured
- [ ] Security context (non-root, read-only rootfs)
- [ ] Init containers for setup tasks
- [ ] Pod anti-affinity for HA
- [ ] Termination grace period configured
