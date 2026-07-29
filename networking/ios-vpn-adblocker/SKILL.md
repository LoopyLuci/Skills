---
name: ios-vpn-adblocker
title: iOS VPN AdBlocker
description: Use when building iOS VPN-based adblocker with Swift.
category: networking
tags: [ios, swift, vpn, adblock, networkextension, apple]
---

# iOS VPN AdBlocker

**Trigger**: Use when implementing iOS adblocking via NetworkExtension VPN.

**Libraries**: NetworkExtension (NEPacketTunnelProvider, NEDNSSettingsManager), SwiftUI

**Implementation**: NEPacketTunnelProvider for full VPN tunnel with DNS filtering. NEDNSSettingsManager for DNS-over-HTTPS configuration pointing to Sentinel. Packet capture and forward loop in tunnel. Rust core compiled as static library (.a) via UniFFI for cross-language calls. Background mode with NEVPNStatusDidChange notification. Battery-efficient: coalesce packets.

**Connected**: `android-vpn-adblocker`, `mobile-dns-override`, `vpn-tunnel-engine`, `dns-adblock-engine`, `rust-core-ffi`
