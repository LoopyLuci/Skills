---
name: vpn-implementation-patterns
description: "Use when implementing VPN tunnels and remote access."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [VPN, tunnel, WireGuard, OpenVPN, IPsec, remote-access, site-to-site]
    related_skills: [wireguard-vpn-controller, network-segmentation-strategies, firewall-rules-engine, identity-access-management]
---

# VPN Implementation Patterns

Implementing VPN tunnels and remote access — from WireGuard and OpenVPN through IPsec/IKEv2, site-to-site VPNs, and remote access design patterns.

## When to Use

- Providing secure remote access for employees
- Connecting branch offices via site-to-site VPN
- Building secure communication between cloud and on-premise
- Implementing zero-trust network access alongside VPN
- Replacing legacy VPN with modern alternatives

## VPN Protocols

```python
VPN_PROTOCOLS = {
    'wireguard': {
        'strength': 'Modern, fast, simple, kernel-level, audited',
        'use_case': 'General purpose, site-to-site, remote access',
        'setup': 'Minimal config, single file, public/private keys',
    },
    'openvpn': {
        'strength': 'Mature, widely supported, rich auth options',
        'use_case': 'Remote access, enterprise, complex auth needs',
        'setup': 'Certificate-based, more config options',
    },
    'ipsec': {
        'strength': 'Industry standard, hardware offload, strong encryption',
        'use_case': 'Site-to-site, cloud-to-on-premise, legacy compatibility',
        'setup': 'IKEv2 with strongSwan or built-in OS support',
    },
}

# WireGuard config template
WIREGUARD_CONFIG = """
[Interface]
PrivateKey = <server-private-key>
Address = 10.0.0.1/24
ListenPort = 51820

[Peer]
PublicKey = <client-public-key>
AllowedIPs = 10.0.0.2/32
"""
```

## Common Pitfalls

1. **Split tunneling not configured** — all traffic through VPN slows internet access; route only private ranges
2. **Key management** — WireGuard keys on compromised clients; implement key rotation
3. **No failover** — single VPN server = single point of failure; cluster or have backup
4. **MTU issues** — VPN encapsulation reduces MTU; adjust MTU (typically 1420 for WireGuard)
5. **Performance bottleneck** — VPN server CPU can't handle throughput; consider kernel-level WireGuard

## Verification Checklist

- [ ] Protocol selected (WireGuard, OpenVPN, IPsec)
- [ ] Split tunneling configured (only route private IPs)
- [ ] Authentication method defined (keys, certificates, SSO)
- [ ] MTU configured correctly
- [ ] Firewall allows VPN protocol on correct port
- [ ] DNS configuration for internal resources
- [ ] Monitoring on connection count, bandwidth, errors
- [ ] Revocation process for compromised devices
- [ ] Failover/high availability for production VPN
