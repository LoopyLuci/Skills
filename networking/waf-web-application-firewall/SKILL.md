---
name: waf-web-application-firewall
description: "Use when implementing web application firewalls and rules."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [WAF, web-application-firewall, modsecurity, OWASP, rules, SQL-injection, XSS]
    related_skills: [web-security-patterns, network-ids-ips-patterns, ddos-mitigation-strategies, api-gateway-load-balancing]
---

# Web Application Firewall (WAF)

Implementing and managing WAFs — from rule writing and OWASP Core Rule Set through deployment, tuning, and bypass prevention.

## When to Use

- Protecting apps from SQL injection, XSS, and OWASP Top 10 attacks
- Implementing virtual patching for known vulnerabilities
- Filtering malicious traffic before it reaches app servers
- PCI DSS compliance (requirement 6.6)

## WAF Solutions

```python
WAF_SOLUTIONS = {
    'modsecurity': 'Open-source WAF engine, OWASP CRS rules',
    'cloudflare': 'Cloud WAF, managed rules, rate limiting, bot mgmt',
    'aws_waf': 'AWS-managed, integrates with ALB/CloudFront',
}

RULES = [
    {'id': '942100', 'desc': 'SQL Injection', 'pattern': r'(?i)\b(union|select|drop)\b.*\b(from|where)\b'},
    {'id': '941100', 'desc': 'XSS', 'pattern': r'(?i)(<script|javascript:|onerror=)'},
    {'id': '930100', 'desc': 'Path Traversal', 'pattern': r'\.\.\/|\.\.\\'},
]
```

## Common Pitfalls

1. **False positives** — blocking legitimate traffic; tune CRS paranoia level
2. **Blind blocking** — deploy in detection mode first, block after tuning
3. **Bypass vectors** — test with encoded payloads and alternative methods
4. **WAF as only defense** — complements, doesn't replace secure coding

## Verification Checklist

- [ ] Detection mode first, tune before blocking
- [ ] OWASP CRS at appropriate paranoia level
- [ ] Custom rules for app-specific threats
- [ ] Rate limiting configured
- [ ] Logs integrated with SIEM
