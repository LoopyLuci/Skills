---
name: github-codespaces-config
description: Configure dev containers and dotfiles for GitHub Codespaces.
---

# GitHub Codespaces Configuration

**Trigger**: Use when setting up dev containers for Codespaces, configuring dependencies, or customizing the development environment.

## Quick Start

```bash
# Create devcontainer config from the CLI
gh codespace create --repo owner/repo
```

Or add `.devcontainer/devcontainer.json` to your repo:

## Dev Container Configuration

### Minimal — Just the Image
`.devcontainer/devcontainer.json`:
```json
{
  "name": "My Project",
  "image": "mcr.microsoft.com/devcontainers/universal:2",
  "postCreateCommand": "npm install",
  "forwardPorts": [3000],
  "customizations": {
    "vscode": {
      "extensions": ["rust-lang.rust-analyzer"]
    }
  }
}
```

### Full Example — Python + Node
```json
{
  "name": "Full Stack App",
  "image": "mcr.microsoft.com/devcontainers/universal:2",
  "features": {
    "ghcr.io/devcontainers/features/rust:1": {},
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/node:1": {
      "version": "20"
    }
  },
  "postCreateCommand": "npm ci && pip install -r requirements.txt",
  "postStartCommand": "npm run dev",
  "forwardPorts": [3000, 8000],
  "portsAttributes": {
    "3000": {
      "label": "Frontend",
      "onAutoForward": "openBrowser"
    },
    "8000": {
      "label": "API",
      "onAutoForward": "notify"
    }
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "rust-lang.rust-analyzer",
        "ms-python.python",
        "esbenp.prettier-vscode",
        "bradlc.vscode-tailwindcss"
      ],
      "settings": {
        "files.autoSave": "onFocusChange"
      }
    }
  }
}
```

### Dockerfile-Based
`.devcontainer/Dockerfile`:
```dockerfile
FROM mcr.microsoft.com/devcontainers/rust:latest
RUN apt-get update && apt-get install -y protobuf-compiler
```

`.devcontainer/devcontainer.json`:
```json
{
  "name": "Rust + Proto",
  "build": {
    "dockerfile": "Dockerfile"
  },
  "postCreateCommand": "rustup component add clippy rustfmt",
  "customizations": {
    "vscode": {
      "extensions": ["rust-lang.rust-analyzer"]
    }
  }
}
```

## Dotfiles

```bash
# Configure dotfiles repo
# Settings → Codespaces → Automatically install dotfiles
# Point to: github.com/your/dotfiles
```

Your dotfiles repo should have:
```
dotfiles/
├── install.sh          # Runs on Codespace creation
├── .bashrc            # Shell config
├── .gitconfig         # Git aliases and settings (no email — uses codespace email)
└── .tmux.conf         # Tmux config
```

## Environment Variables & Secrets

```json
{
  "name": "My App",
  "image": "mcr.microsoft.com/devcontainers/universal:2",
  "remoteEnv": {
    "NODE_ENV": "development",
    "DATABASE_URL": "${localEnv:DATABASE_URL}"
  },
  "secrets": {
    "API_KEY": "sk-..."
  }
}
```

## Using CLI

```bash
# Create codespace
gh codespace create --repo owner/repo --branch feature-x
gh codespace create --repo owner/repo --machine premiumLinux

# List codespaces
gh codespace list

# SSH into codespace
gh codespace ssh

# Open in VS Code
gh codespace code

# Stop/Delete
gh codespace stop
gh codespace delete

# Port forwarding
gh codespace ports visibility 3000:public
```

## Features (Extending Devcontainer)

Official feature catalog: `ghcr.io/devcontainers/features/`

```json
"features": {
  "ghcr.io/devcontainers/features/rust:1": {},
  "ghcr.io/devcontainers/features/docker-in-docker:2": {},
  "ghcr.io/devcontainers/features/go:1": {
    "version": "1.22"
  },
  "ghcr.io/devcontainers/features/terraform:1": {},
  "ghcr.io/devcontainers/features/kubectl-helm-minikube:1": {},
  "ghcr.io/devcontainers/features/sshd:1": {}
}
```

## Lifecycle Scripts

| Hook | Timing | Use |
|------|--------|-----|
| `postCreateCommand` | After container created | Install dependencies |
| `postStartCommand` | Every start | Start dev server |
| `postAttachCommand` | Every VS Code attach | Show instructions |
| `initializeCommand` | Before container create | Host machine setup |

## Pitfalls
- **Core hours**: Free tier: 30 hours/month for personal accounts, 60 for Pro — monitor usage
- **Large images**: Devcontainers with all features take 2-5 min to build — keep minimal
- **Secrets**: Use GitHub Codespaces secrets, not hardcoded in JSON
- **Volume mounts**: Codespaces use ephemeral storage — commit frequently
- **Port 80/443**: Reserved — use custom ports for web apps

## Verification
```bash
gh codespace list                     # Active codespaces
gh api repos/:owner/:repo/codespaces  # API check
gh codespace logs                     # Container build logs
```
