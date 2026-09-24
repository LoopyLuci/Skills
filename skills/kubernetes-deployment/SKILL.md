---
name: kubernetes-deployment
description: Deploy apps to k8s with deployments ingress and configmaps
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [kubernetes, deployment]
---

# Kubernetes Deployment

## Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: myapp }
spec:
  replicas: 3
  selector: { matchLabels: { app: myapp } }
  template:
    metadata: { labels: { app: myapp } }
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        ports: [{ containerPort: 8000 }]
```

## Apply
```bash
kubectl apply -f deployment.yaml
kubectl get pods
kubectl logs deployment/myapp -f
```

## Trigger

Activate this skill when the user mentions:
- kubernetes, deployment workflows or issues
- Building, fixing, or optimizing kubernetes deployment


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
