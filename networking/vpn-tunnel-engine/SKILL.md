---
name: vpn-tunnel-engine
title: VPN Tunnel Engine
description: Use when building VPN tunnels with TUN/TAP interfaces.
category: networking
tags: [vpn, tunnel, tun, tap, wireguard, rust]
---

# VPN Tunnel Engine

**Trigger**: Use when implementing VPN tunnel connectivity with TUN/TAP interfaces.

**Libraries**: `tun` (TUN/TAP interface), `wireguard-uapi`, `ipnetwork`, `pnet`

**Implementation**: Virtual TUN/TAP interface creation via platform APIs. Packet read/write loop with tokio async. IP packet routing between interfaces. WireGuard protocol integration for encrypted tunnels. Split-tunnel routing: only route specific subnets through VPN. DNS push via tunnel. Interface metrics and keepalive.

**Connected**: `proxy-server-engine`, `wireguard-vpn-controller`, `packet-capture-engine`, `firewall-rules-engine`, `ios-vpn-adblocker`, `android-vpn-adblocker`
