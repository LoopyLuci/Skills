---
name: protocol-identifier
title: Protocol Identifier
description: Use when identifying app protocols with nDPI signatures.
category: networking
tags: [dpi, protocol, identification, ndpi, classification, rust]
---

# Protocol Identifier

**Trigger**: Use when identifying application-layer protocols from packet payloads.

**Libraries**: nDPI (C, via FFI), `ndpi-sys` (Rust FFI), `pnet`

**Implementation**: nDPI via FFI: init `ndpi_init_detection_module`, feed packets via `ndpi_detection_process_packet`. Protocol tree categories: Web, Mail, P2P, VoIP, Streaming, Gaming, VPN/Proxy, Malware. Port-independent signature matching. Custom protocol signature JSON definitions. GPU offload via OpenCL (RX 7900 XTX). Cache results per flow.

**Connected**: `dns-adblock-engine`, `connection-tracker`, `pattern-matching-engine`, `tls-ssl-inspector`, `gpu-packet-classifier`, `gpu-anomaly-detector`
