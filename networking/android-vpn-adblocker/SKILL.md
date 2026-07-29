---
name: android-vpn-adblocker
title: Android VPN AdBlocker
description: Use when building Android VPN-based adblocker with Kotlin.
category: networking
tags: [android, kotlin, vpn, adblock, vpnservice, kotlin]
---

# Android VPN AdBlocker

**Trigger**: Use when implementing Android adblocking via VpnService.

**Libraries**: VpnService (Android API), Kotlin Coroutines, Jetpack Compose

**Implementation**: VpnService subclass for VPN tunnel mode with DNS interception. Local DNS proxy thread forwarding to Sentinel. Rust core as shared library (.so) via JNI/UniFFI. Always-on VPN requirement. Split-tunnel to exclude local traffic. Battery optimization: use AlarmManager for periodic instead of always-on. Notification channel for persistent VPN notification.

**Connected**: `ios-vpn-adblocker`, `mobile-dns-override`, `vpn-tunnel-engine`, `dns-adblock-engine`, `rust-core-ffi`
