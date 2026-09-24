---
name: mobile-dns-override
description: Use when configuring private DNS on iOS and Android.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [mobile, dns, override, private, ios, android, configuration]
---

# Mobile DNS Override

**Trigger**: Use when configuring DNS-over-HTTPS or private DNS on mobile devices.

**Libraries**: iOS: NetworkExtension/NEDNSSettingsManager. Android: Private DNS (DNS over TLS) API.

**Implementation**: iOS: NEDNSSettingsManager to configure DoH server. Android: Private DNS mode via DNS over TLS to Sentinel. Enterprise MDM profile generation for mass deployment. QR code configuration for easy setup. Fallback to plain DNS when encrypted not available. DNS leak prevention: bind DNS to VPN tunnel interface.

**Connected**: `ios-vpn-adblocker`, `android-vpn-adblocker`, `encrypted-dns-resolver`, `dns-adblock-engine`
