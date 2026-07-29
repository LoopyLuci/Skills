---
name: docker-dev-containers
description: "Use when configuring VS Code Dev Containers."
category: docker
tags: [docker, devcontainers, vscode, development, environment]
---
# Docker Dev Containers

Using VS Code Dev Containers for reproducible development environments.

## Structure

```
.devcontainer/
  devcontainer.json     # Configuration
  Dockerfile            # Optional: custom image
  docker-compose.yml    # Optional: multi-service setup
  .env                  # Optional: environment variables
```

## Basic devcontainer.json

```json
{
  "name": "My Project Dev",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu-22.04",
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "20"
    },
    "ghcr.io/devcontainers/features/docker-outside-of-docker:1": {}
  },
  "forwardPorts": [3000, 8080],
  "postCreateCommand": "npm install",
  "customizations": {
    "vscode": {
      "extensions": [
        "rust-lang.rust-analyzer",
        "ms-vscode.cpptools",
        "ms-azuretools.vscode-docker"
      ],
      "settings": {
        "editor.formatOnSave": true
      }
    }
  }
}
```

## Custom Dockerfile

```dockerfile
FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

RUN apt-get update && apt-get install -y \
    cmake ninja-build \
    clang-17 lldb-17 \
    libvulkan-dev vulkan-tools \
    && rm -rf /var/lib/apt/lists/*

USER vscode
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
```

```json
{
  "name": "C++/Rust Dev",
  "build": {
    "dockerfile": "Dockerfile",
    "context": ".."
  },
  "mounts": [
    "source=${env:HOME}${env:USERPROFILE}/.ssh,target=/home/vscode/.ssh,type=bind,readonly"
  ],
  "remoteUser": "vscode"
}
```

## Docker Compose Dev Container

```yaml
# .devcontainer/docker-compose.yml
services:
  app:
    build: ..
    volumes:
      - ..:/workspace:cached
    command: sleep infinity
    depends_on:
      db: { condition: service_healthy }
  db:
    image: postgres:16-alpine
    healthcheck: { test: ["CMD", "pg_isready", "-U", "postgres"] }
```

```json
{
  "name": "Full Stack",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",
  "forwardPorts": [3000, 5432],
  "shutdownAction": "stopCompose"
}
```

## Open in Dev Container

```powershell
# Command line
code --folder-uri "vscode-remote://dev-container+$(pwd)/.devcontainer"

# Or via VS Code UI:
# F1 → "Dev Containers: Reopen in Container"
```

## Lifecycle Hooks

```json
{
  "onCreateCommand": ".devcontainer/on-create.sh",
  "updateContentCommand": "npm install",
  "postCreateCommand": "npm run build",
  "postStartCommand": "git config --global --add safe.directory /workspace",
  "postAttachCommand": "echo 'Ready!'"
}
```

## Pitfalls

- **Rebuild** when changing devcontainer.json or Dockerfile (`F1 → Rebuild`)
- **SSH keys** need to be mounted or forwarded -- never baked into image
- **Performance** on Windows: mount source code inside WSL2, not /mnt/c/
- **docker-in-docker** vs docker-outside-docker: use "outside" for build performance
- **Features** are ordered -- dependency features must come before dependents
