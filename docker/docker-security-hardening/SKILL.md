---
name: docker-security-hardening
description: "Use when hardening Docker containers and images."
category: docker
tags: [docker, security, hardening, scanning]
---
# Docker Security Hardening

Hardening containers and images.

## Non-Root User
```dockerfile
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
COPY --chown=appuser:appgroup . /app
```

## Read-Only Rootfs
```powershell
docker run --read-only --tmpfs /tmp --tmpfs /var/run myapp
```

## Drop Capabilities
```powershell
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE myapp
```

## Image Scanning
```powershell
docker scout quickview myapp:latest
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \\
    aquasec/trivy image myapp:latest
```

## Secrets (don't bake in)
```powershell
docker run --secret id=db_pass,src=./secrets/db_pass.txt myapp
```

## Dockerfile
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends pkg \\
    && rm -rf /var/lib/apt/lists/*
FROM node:20.11.0-alpine3.18    # pin versions, not "latest"
```

## Pitfalls
- "latest" tags change -- pin versions
- Env vars with secrets leak to docker history -- use --secret
- --privileged defeats all security -- avoid
