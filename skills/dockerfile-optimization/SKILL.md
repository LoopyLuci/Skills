---
name: dockerfile-optimization
description: "Use when optimizing Docker builds: layers, cache."
category: docker
tags: [docker, dockerfile, build, optimization, multistage]
---
# Dockerfile Optimization

Optimizing Docker builds for speed, size, and security.

## Multi-stage Build
```dockerfile
FROM golang:1.21 AS builder
WORKDIR /app; COPY go.mod .; RUN go mod download
COPY . .; RUN CGO_ENABLED=0 go build -o server
FROM alpine:3.18
COPY --from=builder /app/server /server
CMD ["/server"]
```

## Layer Caching
```dockerfile
FROM node:20-alpine
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
```

## Combine RUN
```dockerfile
RUN apt-get update && apt-get install -y curl \\
    && rm -rf /var/lib/apt/lists/*
```

## BuildKit
```powershell
$env:DOCKER_BUILDKIT=1
docker build --no-cache --progress=plain -t myapp .
```

## Pitfalls
- **COPY .** before deps invalidates caches
- **apt install** without cleanup bloats image
- **Distroless** has no shell -- use docker debug
