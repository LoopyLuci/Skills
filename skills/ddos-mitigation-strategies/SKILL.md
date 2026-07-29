---
name: ddos-mitigation-strategies
description: "Use when implementing DDoS protection and mitigation."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ddos, mitigation, protection, volumetric, scrubbing, rate-limiting]
    related_skills: [waf-web-application-firewall, security-incident-response, network-ids-ips-patterns, bgp-routing-patterns]
---

# DDoS Mitigation Strategies

Implementing DDoS protection and mitigation — from volumetric and protocol attacks through application-layer mitigation, scrubbing centers, and incident response.

## When to Use

- Protecting web applications and APIs from DDoS attacks
- Building DDoS response playbooks
- Selecting DDoS mitigation services
- Implementing rate limiting and traffic filtering
- Designing resilient infrastructure against volumetric attacks

## Attack Types and Mitigations

```python
DDoS_VECTORS = {
    'volumetric': {
        'example': 'UDP amplification, ICMP flood, DNS reflection',
        'scale': 'Hundreds of Gbps to Tbps',
        'mitigation': 'Cloud scrubbing centers, BGP black-hole, rate limiting',
    },
    'protocol': {
        'example': 'SYN flood, ACK flood, fragmented packet attack',
        'scale': 'Millions of packets per second',
        'mitigation': 'SYN cookies, connection tracking, TCP stack hardening',
    },
    'application': {
        'example': 'HTTP flood, slow loris, API abuse, query flooding',
        'scale': 'Hundreds of thousands of requests per second',
        'mitigation': 'WAF rate limiting, CAPTCHA, challenge pages, bot detection',
    },
}

class DDoSResponder:
    """Automated DDoS detection and mitigation response."""
    def __init__(self, threshold_pps: int = 500000):
        self.threshold = threshold_pps
        self.mitigations = []
    
    def analyze_traffic(self, current_pps: int, current_bps: int) -> str:
        if current_pps > self.threshold:
            return self._trigger_mitigation('volumetric')
        return 'normal'
    
    def _trigger_mitigation(self, attack_type: str):
        actions = {
            'volumetric': 'Enable BGP blackhole, activate cloud scrubber',
            'protocol': 'Enable SYN cookies, rate-limit new connections',
            'application': 'Enable WAF challenge, rate-limit per-IP',
        }
        return actions.get(attack_type, 'Monitor')
```

## Common Pitfalls

1. **No baseline** — don't know what normal traffic looks like; establish baseline
2. **Mitigation false positives** — rate-limiting too aggressively blocks legitimate users
3. **Single mitigation layer** — only cloud or only on-premise; defense in depth
4. **Late detection** — by the time you detect, impact has occurred; use always-on monitoring
5. **No testing** — mitigation mechanisms fail when needed if not tested regularly

## Verification Checklist

- [ ] Normal traffic baseline established
- [ ] Cloud-based scrubbing service (Cloudflare, AWS Shield, Akamai, etc.)
- [ ] On-premise rate limiting and filtering
- [ ] BGP blackhole / RTBH configured
- [ ] WAF with DDoS rules enabled
- [ ] Auto-scaling for legitimate traffic increase
- [ ] DDoS response playbook documented and tested
- [ ] Tabletop exercises conducted quarterly
