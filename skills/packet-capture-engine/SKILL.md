---
name: packet-capture-engine
description: Use when capturing raw packets across platforms with pcap.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [packet, capture, pcap, npcap, rust, cross-platform]
---

# Packet Capture Engine

**Trigger**: Use when capturing raw network packets across platforms for inspection.

**Libraries**: `pcap` (libpcap bindings), `pnet` (packet manipulation), `etherparse` (parsing)

**Implementation**: Ring buffer capture via `pcap::Capture::from_device` → async `PacketStream`. BPF pre-filtering at kernel level. Multi-queue distribution: one thread per NIC queue via RSS. Zero-copy via shared memory rings (Linux PACKET_MMAP, Windows NPcap). Nanosecond timestamping (PCAPNG format).

**Connected**: `firewall-rules-engine`, `port-scanner-detection`, `protocol-identifier`, `traffic-analyzer`, `multi-queue-capture`
