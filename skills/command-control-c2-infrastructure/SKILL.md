---
name: command-control-c2-infrastructure
description: "Use when building C2 infrastructure for red teams."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [C2, command-control, mythic, cobalt-strike, sliver, domain-fronting, redirector]
    related_skills: [red-team-operations, evasion-techniques-av-bypass, lateral-movement-pivoting, port-redirection-tunneling]
---

# Command and Control (C2) Infrastructure

Building C2 infrastructure for red team operations — from C2 frameworks (Mythic, Sliver, Cobalt Strike) through redirectors, domain fronting, and opsec.

## When to Use

- Setting up C2 infrastructure for red team engagements
- Choosing between C2 frameworks (Mythic, Sliver, Cobalt Strike, Havoc)
- Implementing domain fronting and CDN redirectors
- Opsec-safe C2 communication

## C2 Architecture

```python
C2_FRAMEWORKS = {
    'mythic': 'Open-source, multi-agent (Apollo, Poseidon, Athena), web UI, extensible',
    'sliver': 'Open-source, Go-based, mTLS/HTTP(S)/DNS, game-over-254d, Github stars',
    'cobalt_strike': 'Commercial — Malleable C2, TCP/HTTP/DNS/SMB, aggressor scripts',
    'havoc': 'Open-source C2 with Cobalt Strike-like features, NtCreateThreadEx injection',
}

C2_INFRA = {
    'redirector': 'Nginx/Apache reverse proxy, filters by User-Agent, Cookie, URI path',
    'domain_fronting': 'CDN hosting (Cloudflare, Azure, CloudFront), HTTPS to CDN != final host',
    'c2_profiles': 'Malleable C2 profiles (Cobalt Strike) — mimic legit traffic (JQuery, API, JS)',
    'callback_intervals': 'Jitter 20-30%, intervals 30-60s, weekend/holiday suppression',
}

# Nginx redirector config template
NGINX_REDIRECTOR = """
server {
    listen 443 ssl;
    server_name legitimate-domain.com;
    
    location / {
        # Forward only valid C2 requests
        if ($http_user_agent !~* "Mozilla|Chrome") { return 404; }
        proxy_pass https://actual-c2-server:443;
    }
}
"""
```

## Verification Checklist

- [ ] C2 framework chosen (Mythic, Sliver, Cobalt Strike, or Havoc)
- [ ] Redirector(s) deployed and tested (domain fronting or CDN)
- [ ] C2 profile configured (malleable C2 to mimic normal traffic)
- [ ] Multiple fallback endpoints (HTTPS, DNS, SMB, custom protocol)
- [ ] Callback intervals and jitter configured
- [ ] Opsec: burn-after-use domains, short-lived certificates
- [ ] Egress filtering tested (what protocols work from target network)
- [ ] P2P mode configured (if agents should talk through each other)
- [ ] Logging and data collection operational
