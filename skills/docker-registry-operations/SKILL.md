---
name: docker-registry-operations
description: "Use when pushing/pulling/managing registry images."
category: docker
tags: [docker, registry, push, pull, dockerhub]
---
# Docker Registry Operations

Working with image registries.

## Auth
```powershell
docker login
docker login ghcr.io -u USER --password-stdin < token.txt
docker login myregistry.com:5000 -u admin -p password
```

## Tag & Push
```powershell
docker tag myapp:latest myrepo/myapp:latest
docker push myrepo/myapp:latest
docker push --all-tags myrepo/myapp
```

## Pull
```powershell
docker pull nginx:alpine
docker pull ghcr.io/owner/image:tag
```

## Cross-Registry
```powershell
docker pull oldreg.com/myapp:latest
docker tag oldreg.com/myapp:latest newreg.com/myapp:latest
docker push newreg.com/myapp:latest
```

## Multi-Arch
```powershell
docker buildx build --platform linux/amd64,linux/arm64 \\
    -t myrepo/myapp:latest --push .
```

## Pitfalls
- Tags are mutable -- use @sha256: for production
- Docker Hub rate limits anonymous pulls
- GC doesn't free disk until blob deletion
