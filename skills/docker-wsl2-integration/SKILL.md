---
name: docker-wsl2-integration
description: "Use when configuring Docker Desktop WSL2 backend on Windows."
category: docker
tags: [docker, wsl2, windows, integration, gpu, daemon]
---

# Docker WSL2 Integration

Configuring Docker Desktop's WSL2 backend on Windows.

## Architecture

Docker Desktop on WSL2 uses two internal WSL2 distros:
- **`docker-desktop`** — the Docker engine/daemon
- **`docker-desktop-data`** — images, volumes, build cache (VHDX)

## Enable & Verify

### Through Docker Desktop Settings
Settings → Resources → WSL Integration → Enable with default WSL distro → Apply

```powershell
# Verify from Windows
docker ps
# Verify from WSL2
wsl -d Ubuntu docker ps
```

## TCP Daemon Access

```powershell
# Settings → General → "Expose daemon on tcp://localhost:2375 without TLS"
$env:DOCKER_HOST = "tcp://localhost:2375"

# Or set in ~/.bashrc
echo 'export DOCKER_HOST=tcp://localhost:2375' >> ~/.bashrc
```

## File Sharing Performance

```powershell
# /mnt/c/ is SLOW for Docker mounts — keep code in WSL2 filesystem
cd ~
mkdir project && cd project
git clone <repo>
docker compose up   # fast

# WSL2 files visible from Windows at:
# \\wsl.localhost\Ubuntu\home\user\
```

## GPU Passthrough

```powershell
# Install NVIDIA drivers on Windows (covers WSL2 too)
docker run --gpus all nvidia/cuda:12.2-runtime-ubuntu22.04 nvidia-smi

# Vulkan in WSL2
docker run --gpus all -it ubuntu-vulkan vkcube
```

## Docker Engine Inside WSL2 (Without Docker Desktop)

```bash
sudo apt-get update && sudo apt-get install -y docker.io docker-compose-v2
sudo usermod -aG docker $USER
sudo dockerd &
```

## Troubleshooting

```powershell
# Check WSL2 status
wsl --list --verbose
# Restart WSL2 entirely
wsl --shutdown
# Check Docker Desktop logs
Get-Content "$env:LOCALAPPDATA\Docker\log\*.log" -Tail 50
```

## Pitfalls

- **DrvFs mounts** are slow — keep code in WSL2 filesystem
- **`wsl --shutdown`** kills docker-desktop distros
- **VPNs** can break WSL2 networking — `wsl --shutdown` then restart
- **docker-desktop-data VHDX** can grow huge — compact with diskpart or reset
- **Docker context** may switch between Windows and WSL2 — check with `docker context ls`
