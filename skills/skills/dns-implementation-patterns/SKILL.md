---
name: dns-implementation-patterns
description: "Use when implementing DNS servers, resolvers, and tools."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [dns, nameserver, resolver, DNSSEC, zone, record, authoritative, recursive]
    related_skills: [encrypted-dns-resolver, dns-cache-layer, dns-adblock-engine, dns-proxy-filter]
---

# DNS Implementation Patterns

Implementing DNS servers, resolvers, and tools — from authoritative and recursive nameservers through DNS security (DNSSEC), resolution optimization, and custom DNS applications.

## When to Use

- Building a custom DNS server or proxy
- Implementing DNS filtering or ad-blocking
- Understanding DNS protocol for network tools
- Setting up DNSSEC for zone security
- Optimizing DNS resolution performance

## DNS Record Types

```python
DNS_RECORDS = {
    'A': 'Maps hostname to IPv4 address',
    'AAAA': 'Maps hostname to IPv6 address',
    'CNAME': 'Alias of one name to another (canonical name)',
    'MX': 'Mail exchange server for domain',
    'TXT': 'Arbitrary text data (SPF, DKIM, verification)',
    'NS': 'Authoritative nameserver for the domain',
    'SOA': 'Start of Authority — zone parameters',
    'SRV': 'Service location (specific service/protocol)',
}

class DNSServer:
    """Minimal authoritative DNS server."""
    def __init__(self):
        self.zone_data = {}  # (domain, type) -> [values]
    
    def add_record(self, domain: str, record_type: str, value: str, ttl: int = 300):
        self.zone_data[(domain, record_type)] = {'values': [value], 'ttl': ttl}
    
    def resolve(self, domain: str, record_type: str = 'A') -> Dict:
        import dns.message, dns.query
        
        # Check local zone
        record = self.zone_data.get((domain, record_type))
        if record:
            return {'domain': domain, 'type': record_type, 'answers': record['values']}
        
        # Forward to upstream resolver
        query = dns.message.make_query(domain, record_type)
        response = dns.query.udp(query, '8.8.8.8')
        answers = [r.to_text() for r in response.answer] if response.answer else []
        return {'domain': domain, 'type': record_type, 'answers': answers}
```

## Common Pitfalls

1. **TTL too high** — long TTLs slow down changes; use 300s for dynamic records
2. **CNAME at apex** — CNAME records conflict with other types at zone apex; use ALIAS/ANAME
3. **No DNSSEC** — DNS spoofing is real; sign zones with DNSSEC
4. **Missing reverse DNS** — PTR records for mail servers required for deliverability
5. **Nameserver redundancy** — single nameserver violates RFC; have at least 2

## Verification Checklist

- [ ] All required record types configured (A, AAAA, MX, TXT, NS, SOA)
- [ ] TTLs appropriate (< 1 hour for dynamic, < 24 hours for static)
- [ ] DNSSEC enabled and签名验证通过
- [ ] Reverse DNS (PTR) configured for mail servers
- [ ] Multiple nameservers (minimum 2, ideally geo-distributed)
- [ ] Monitoring on query latency and error rates
