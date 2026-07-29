---
name: wireguard-vpn-controller
title: WireGuard VPN Controller
description: Use when managing WireGuard tunnels and peers.
category: networking
tags: [wireguard, vpn, tunnel, peers, config, rust]
---

# WireGuard VPN Controller

**Trigger**: Use when implementing WireGuard VPN peer and tunnel management.

**Libraries**: `wireguard-uapi`, `tun`, `ipnetwork`, `base64`

**Implementation**: WireGuard interface configuration via userspace kernel API (uapi over netlink). Peer management: add/remove/update public keys, allowed IPs, endpoints. Key generation (Curve25519 via `x25519-dalek`). Automatic keepalive and handshake monitoring. Split-tunnel configuration. Multi-peer mesh networking. Stats: transfer bytes, latest handshake.

**Connected**: `vpn-tunnel-engine`, `proxy-server-engine`, `firewall-rules-engine`, `connection-tracker`, `bandwidth-monitor`
