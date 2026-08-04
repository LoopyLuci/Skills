---
name: docker-buildx-multiarch
description: "Use when building multi-architecture Docker images."
category: docker
tags: [docker, buildx, multiarch, cross-platform, arm]
---
# Docker Buildx Multi-Architecture

Building multi-architecture Docker images with Buildx.

## Setup

```powershell
# Create a builder instance
docker buildx create --name mybuilder --driver docker-container --use

# Start it
docker buildx inspect --bootstrap

# Check supported platforms
docker buildx ls
```

## Build for Multiple Architectures

```powershell
# Single build, multi-platform
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 \
    -t myrepo/myapp:latest --push .

# Build only, no push
docker buildx build --platform linux/amd64,linux/arm64 \
    -t myapp:latest --load .

# With build args
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --build-arg NODE_ENV=production \
    -t myrepo/myapp:1.0.0 \
    -t myrepo/myapp:latest \
    --push \
    --cache-from type=registry,ref=myrepo/myapp:cache \
    --cache-to type=registry,ref=myrepo/myapp:cache,mode=max \
    .
```

## Dockerfile Best Practices for Multi-Arch

```dockerfile
# Use platform-specific base images
FROM --platform=$BUILDPLATFORM node:20-alpine AS builder
ARG TARGETPLATFORM
ARG BUILDPLATFORM
RUN echo "Building for $TARGETPLATFORM from $BUILDPLATFORM"

# Build with native arch for speed, then target arch
FROM --platform=$TARGETPLATFORM alpine:3.18
COPY --from=builder /app/build /app
```

## Inspect Multi-Arch Images

```powershell
# View manifest list
docker buildx imagetools inspect myrepo/myapp:latest

# Pull specific architecture
docker pull --platform linux/arm64 myrepo/myapp:latest

# Inspect local after --load
docker inspect myapp:latest --format '{{.Os}}/{{.Architecture}}'
```

## QEMU Emulation (Cross-Platform Build)

```powershell
# Required for building ARM on x86 (handled by buildx automatically)
docker run --privileged --rm tonistiigi/binfmt --install all

# Verify installed emulators
ls /proc/sys/fs/binfmt_misc/ | grep qemu
```

## Export/Import Build Cache

```powershell
# Cache to registry (shared between CI runs)
docker buildx build --cache-from type=registry,ref=myrepo/cache \
    --cache-to type=registry,ref=myrepo/cache,mode=max \
    --platform linux/amd64,linux/arm64 \
    -t myrepo/myapp:latest --push .

# Local cache
docker buildx build --cache-from type=local,src=.buildx-cache \
    --cache-to type=local,dest=.buildx-cache,mode=max \
    -t myapp:latest .
```

## Pitfalls

- `--load` only works for single-platform builds (use `--push` for multi-arch)
- QEMU emulation is slower than native builds -- use native builders when possible
- Dockerfile must avoid arch-specific commands without `--platform` flags
- BuildKit cache registry needs `mode=max` for multi-arch layer reuse
- Not all base images support all architectures
