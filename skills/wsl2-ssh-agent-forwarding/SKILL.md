---
name: wsl2-ssh-agent-forwarding
description: "Use when forwarding SSH agent to WSL2."
category: software-development
tags: [wsl2, ssh, agent, forwarding, authentication]
---
# WSL2 SSH Agent Forwarding

Forwarding SSH agent from Windows to WSL2.

## Windows OpenSSH Agent (Built-in)

```powershell
# Ensure OpenSSH Agent is running on Windows
Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent

# Add key to Windows agent
ssh-add $env:USERPROFILE\.ssh\id_rsa
```

## WSL2 → Windows Agent Forwarding

```bash
# Inside WSL2, add to ~/.bashrc or ~/.zshrc:
# Use npiperelay or socat to forward agent socket

# Method 1: npiperelay (recommended)
# Install on Windows:
winget install --id npiperelay.npiperelay -e

# Inside WSL2, add to ~/.bashrc:
if [ -z "$SSH_AUTH_SOCK" ]; then
    export SSH_AUTH_SOCK=$HOME/.ssh/agent.sock
    if [ ! -S "$SSH_AUTH_SOCK" ]; then
        rm -f "$SSH_AUTH_SOCK"
        (setsid nohup socat UNIX-LISTEN:$SSH_AUTH_SOCK,fork \
            EXEC:"npiperelay.exe -ei -s //./pipe/openssh-ssh-agent",nofork &) >/dev/null 2>&1
    fi
fi
```

## Test the Forwarding

```shell
# Inside WSL2
ssh-add -l  # Should show your Windows keys
ssh git@github.com  # Should work without password
```

## SSH Config (Inside WSL2)

```bash
# ~/.ssh/config
Host github.com
    User git
    IdentityFile ~/.ssh/id_ed25519  # Optional, agent handles it
    ForwardAgent yes

Host *
    ForwardAgent yes
```

## Alternative: Copy Keys Directly

```bash
# Simple approach -- copy keys from Windows to WSL2
cp /mnt/c/Users/limpi/.ssh/id_ed25519 ~/.ssh/
cp /mnt/c/Users/limpi/.ssh/id_ed25519.pub ~/.ssh/
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
```

## Docker Build SSH Forwarding

```bash
# Pass SSH agent to Docker builds (Dockerfile: --mount=type=ssh)
# Build command:
docker buildx build --ssh default=$SSH_AUTH_SOCK -t myapp .

# Dockerfile:
# RUN --mount=type=ssh git clone git@github.com:org/private-repo.git
```

## Pitfalls

- npiperelay.exe must be in Windows PATH for WSL2 to find it
- socat must be installed inside WSL2: `sudo apt-get install socat`
- Agent socket path must match between WSL2 and Windows
- SSH agent on Windows might not start automatically -- check service
- Key permissions: 600 for private key, 644 for public key
