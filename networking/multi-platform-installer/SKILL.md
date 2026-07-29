---
name: multi-platform-installer
title: Multi-Platform Installer
description: Use when building installers for all target platforms.
category: networking
tags: [installer, cross-platform, packaging, distribution, deployment]
---

# Multi-Platform Installer

**Trigger**: Use when building distribution packages and installers.

**Libraries**: WiX Toolset (Windows .msi), `cargo-bundle` (macOS .app), Flatpak/AppImage (Linux), Fastlane (mobile)

**Implementation**: Windows MSI via WiX with service setup. macOS .app bundle via cargo-bundle with launchd plist. Linux: .deb (cargo-deb), .rpm, Flatpak. iOS: TestFlight via Fastlane. Android: AAB via Gradle + Google Play. Docker image for server deployment: multi-stage Dockerfile, distroless base. Homebrew formula for macOS. Chocolatey package for Windows.

**Connected**: `service-orchestrator`, `svelte-web-dashboard`, `rust-core-ffi`, `ios-vpn-adblocker`, `android-vpn-adblocker`
