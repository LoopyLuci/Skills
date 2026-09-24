---
name: vpn-tunnel-setup
description: Set up WireGuard Tailscale for secure remote access
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [vpn, tunnel, setup]
---

# VPN Tunnel Setup

## WireGuard
```ini
[Interface]
PrivateKey = <private>
Address = 10.0.0.2/24

[Peer]
PublicKey = <public>
Endpoint = server.com:51820
AllowedIPs = 10.0.0.0/24
```

## Tailscale (Zero Config)
```bash
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up
tailscale status
```

## Trigger

Activate this skill when the user mentions:
- vpn, tunnel, setup workflows or issues
- Building, fixing, or optimizing vpn tunnel setup


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
