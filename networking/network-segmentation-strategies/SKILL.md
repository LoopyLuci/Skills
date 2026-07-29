---
name: network-segmentation-strategies
description: "Use when designing network segmentation and isolation."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [network-segmentation, VLAN, subnet, micro-segmentation, zero-trust, isolation]
    related_skills: [zero-trust-network-architecture, container-networking-patterns, firewall-rules-engine, identity-access-management]
---

# Network Segmentation Strategies

Designing network segmentation and isolation — from VLANs and subnets through micro-segmentation, zero-trust network access, and multi-tenant isolation.

## When to Use

- Segregating sensitive systems from general access
- Implementing compliance requirements (PCI, HIPAA)
- Containing breaches through lateral movement prevention
- Designing multi-tenant SaaS infrastructure
- Implementing zero-trust network principles

## Segmentation Models

```python
SEGMENTATION_MODELS = {
    'flat': 'Single network — all systems can communicate (legacy, insecure)',
    'vlan_based': 'Logical segments by function (DMZ, internal, production, staging)',
    'micro_segmentation': 'Granular per-workload policies (zero-trust, SaaS multi-tenant)',
    'overlay': 'Software-defined segmentation on top of physical network (VXLAN, SDN)',
}

SEGMENTATION_TIERS = {
    'public': 'Internet-facing (web servers, API gateways, load balancers)',
    'application': 'Business logic (app servers, microservices)',
    'data': 'Databases, storage, caches (most restricted access)',
    'management': 'Administrative access (SSH, RDP, bastion hosts)',
    'internal_services': 'Internal tools, monitoring, CI/CD',
}

# Firewall rule pattern for segmentation
SEGMENTATION_RULES = """
# Internet → DMZ (web)
allow proto tcp from any to DMZ port 443
# DMZ → Application (backend API)
allow proto tcp from DMZ to APP port 8080
# Application → Database (read/write)
allow proto tcp from APP to DATA port 5432
# Deny everything else
deny ip any any
"""
```

## Common Pitfalls

1. **Overly permissive rules** — "allow any any" between segments defeats segmentation
2. **Segment sprawl** — hundreds of tiny segments become unmanageable; group by function
3. **No east-west monitoring** — lateral movement between segments isn't monitored
4. **Flat inside the segment** — once inside a segment, no further controls; implement host-based firewalls too
5. **Dependence on IP addresses** — IP-based segmentation breaks with dynamic IPs; use identity-based

## Verification Checklist

- [ ] Network tiers defined (public, app, data, management)
- [ ] Segmentation rules documented and enforced (firewall)
- [ ] Only required traffic allowed between segments
- [ ] East-west traffic monitored and logged
- [ ] Micro-segmentation for critical workloads (if applicable)
- [ ] Segmentation tested (attempt lateral movement, verify blocks)
- [ ] Compliance requirements met (PCI, HIPAA, SOC2)
- [ ] Overlay segmentation for multi-tenant (VXLAN, SDN)
