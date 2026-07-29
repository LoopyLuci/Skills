---
name: network-scanning-enumeration
description: "Use when scanning and enumerating network targets."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [network-scanning, nmap, masscan, enumeration, service-detection, fingerprinting]
    related_skills: [vulnerability-assessment-scanning, network-sniffing-packet-capture, penetration-testing-methodology, osint-reconnaissance-techniques]
---

# Network Scanning and Enumeration

Scanning and enumerating network targets — from Nmap discovery scans through service fingerprinting, banner grabbing, and comprehensive enumeration.

## When to Use

- Discovering live hosts on a network during pentests
- Identifying open ports and running services
- Service version fingerprinting and OS detection
- Network mapping and attack surface enumeration

## Nmap Techniques

```python
NMAP_SCANS = {
    'ping_sweep': "nmap -sn 10.0.0.0/24 — discover live hosts",
    'port_scan': "nmap -sS -p- -T4 10.0.0.1 — full TCP SYN scan (ports 1-65535)",
    'service_detect': "nmap -sV -p 22,80,443 10.0.0.1 — service version detection",
    'os_detect': "nmap -O 10.0.0.1 — OS fingerprinting",
    'script_scan': "nmap -sC -p 80,443 10.0.0.1 — default NSE scripts",
    'vuln_scan': "nmap --script vuln -p 80,443 10.0.0.1 — vulnerability scan",
    'udp_scan': "nmap -sU -p 53,161,500 10.0.0.1 — UDP service discovery",
    'stealth': "nmap -sS -T2 -f --data-length 200 10.0.0.1 — fragmented, slower SYN scan",
}

# Masscan for wide ranges
MASSCAN_EXAMPLE = "masscan 10.0.0.0/8 -p80,443 --rate=10000"

class Enumerator:
    """Enumerate target for pentest information gathering."""
    def __init__(self, target: str):
        self.target = target
    
    def dns_enumeration(self) -> Dict:
        return {
            'A_record': None, 'MX_records': [], 'NS_records': [],
            'txt_records': [], 'zone_transfer': False,
        }
    
    def service_enumeration(self, ports: List[int]) -> List[Dict]:
        services = []
        for port in ports:
            services.append({'port': port, 'service': 'unknown', 'banner': ''})
        return services
```

## Verification Checklist

- [ ] Host discovery performed (ping sweep, ARP scan)
- [ ] Port scanning on all 65535 TCP ports (and common UDP)
- [ ] Service version detection on open ports
- [ ] OS fingerprinting attempted
- [ ] NSE scripts run for additional enumeration
- [ ] Banner grabbing for identified services
- [ ] DNS enumeration (records, zone transfer check)
- [ ] Target scope respected (no scanning out-of-bound IPs)
- [ ] Scan results documented with evidence
