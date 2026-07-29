---
name: vpn-tunnel-setup
description: "Set up WireGuard Tailscale for secure remote access"
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
