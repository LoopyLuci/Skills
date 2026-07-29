---
name: pattern-matching-engine
title: Pattern Matching Engine
description: Use when doing YARA/Suricata regex detection on packets.
category: networking
tags: [yara, suricata, regex, hyperscan, signature, rust]
---

# Pattern Matching Engine

**Trigger**: Use when doing signature-based detection via YARA, Snort/Suricata rules, or regex.

**Libraries**: `yara-rust` (YARA bindings), `pcre2-rust`, `aho-corasick`, Hyperscan (HW-accelerated regex)

**Implementation**: YARA compile rulesets, scan reassembled payloads. Hyperscan for thousands of simultaneous regex patterns. Aho-Corasick for high-throughput fixed-string matching. Categories: malware, exploits, data exfiltration, C2. SMTS distribution across 24 threads. Atomic hot-reload of pattern databases.

**Connected**: `protocol-identifier`, `tls-ssl-inspector`, `gpu-packet-classifier`, `gpu-anomaly-detector`, `ml-threat-detection`
