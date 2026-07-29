---
name: container-security-hardening
description: "Use when hardening container images and deployments."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [container-security, docker, kubernetes, images, vulnerability-scanning, seccomp]
    related_skills: [container-networking-patterns, kubernetes-deployment, vulnerability-scanning, security-incident-response]
---

# Container Security Hardening

Hardening container images and deployments — from minimal base images through vulnerability scanning, runtime security, and Kubernetes Pod Security Standards.

## When to Use

- Reducing attack surface of container images
- Scanning for vulnerabilities in container images
- Running containers with least privilege
- Implementing Kubernetes pod security
- Building secure CI/CD container pipelines

## Hardening Practices

```python
CONTAINER_HARDENING = {
    'base_images': 'Use distroless (Google) or scratch, avoid full OS images',
    'non_root': 'USER nobody in Dockerfile, never run as root',
    'read_only': 'Read-only root filesystem, tmpfs for what needs write',
    'minimal_layers': 'Single RUN apt, multi-stage builds, squashing layers',
    'scanning': 'Trivy, Grype, Clair in CI — fail builds on critical CVEs',
}

DOCKERFILE_SECURE = """
# Multi-stage: build stage
FROM golang:1.21 AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o app .

# Distroless runtime stage
FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=builder /app/app /app
USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["/app"]
"""
```

## Verification Checklist

- [ ] Base image is minimal (distroless or scratch)
- [ ] Container runs as non-root user
- [ ] Root filesystem is read-only
- [ ] Image scanned for vulnerabilities (Trivy/Grype)
- [ ] No sensitive data in image (env vars, secrets)
- [ ] Seccomp/apparmor profiles applied
- [ ] Resource limits set (CPU, memory)
- [ ] Image signed and verified in deployment
