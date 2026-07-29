---
name: network-forensics-analysis
description: "Use when performing network forensic and pcap analysis."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [network-forensics, pcap, wireshark, packet-analysis, incident-investigation]
    related_skills: [security-incident-response, threat-hunting-methods, packet-capture-engine, traffic-analyzer]
---

# Network Forensic Analysis

Analyzing packet captures and network evidence for security investigations — from capture methodology through protocol analysis, timeline reconstruction, and evidence preservation.

## When to Use

- Investigating a security incident from network evidence
- Analyzing pcap files for indicators of compromise
- Reconstructing network sessions and timelines
- Preparing network evidence for legal proceedings

## Forensics Process

```python
FORENSICS_PHASES = {
    'preservation': 'Capture and hash evidence, maintain chain of custody',
    'triage': 'Identify suspicious sessions, IPs, ports, and protocols',
    'analysis': 'Deep packet inspection, protocol decode, file extraction',
    'correlation': 'Correlate with logs, endpoints, and threat intel',
}
```

## Common Pitfalls

1. **Truncated captures** — missing packet payloads lose evidence
2. **No chain of custody** — evidence integrity must be provable
3. **Analyzing originals** — always work from copies, not original evidence
4. **Missing encrypted traffic** — focus on metadata, DNS, TLS handshakes
5. **No timeline** — timestamps need synchronized clocks (NTP)

## Verification Checklist

- [ ] Full packet captures with timestamps
- [ ] Cryptographic hashes of evidence files
- [ ] Chain of custody documented
- [ ] Timeline reconstructed from multiple sources
- [ ] Protocol analysis for HTTP, DNS, TLS covering attack vector
