---
name: ssh-key-management
description: Generate deploy and rotate SSH keys agents and hardening
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [ssh, key, management]
---

# SSH Key Management

## Generate
```bash
ssh-keygen -t ed25519 -C "your@email.com"
```

## Deploy
```bash
ssh-copy-id user@host
# Or manually:
cat ~/.ssh/id_ed25519.pub | ssh user@host "cat >> ~/.ssh/authorized_keys"
```

## Agent
```bash
eval $(ssh-agent -s)
ssh-add ~/.ssh/id_ed25519
```

## Config
```sshconfig
Host myserver
    HostName 192.168.1.100
    User ubuntu
    IdentityFile ~/.ssh/id_ed25519
    Port 2222
```

## Trigger

Activate this skill when the user mentions:
- ssh, key, management workflows or issues
- Building, fixing, or optimizing ssh key management


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
