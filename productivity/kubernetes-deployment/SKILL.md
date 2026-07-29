---
name: kubernetes-deployment
description: "Deploy apps to k8s with deployments ingress and configmaps"
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
