---
name: bgp-routing-patterns
description: "Use when implementing BGP routing and traffic engineering."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [bgp, routing, BGP-iBGP, eBGP, traffic-engineering, AS, peering, anycast]
    related_skills: [sdn-software-defined-networking, dns-implementation-patterns, network-automation-scripting, connection-monitor]
---

# BGP Routing Patterns

Implementing BGP routing and traffic engineering — from iBGP/eBGP design through route selection, path manipulation, anycast, and BGP security.

## When to Use

- Designing BGP peering at an IXP or data center
- Implementing multi-homed internet connectivity
- Traffic engineering with BGP path manipulation
- Building anycast network services (DNS, CDN)
- Securing BGP with RPKI and BGPsec

## BGP Fundamentals

```python
BGP_TYPES = {
    'eBGP': 'External BGP — between different autonomous systems',
    'iBGP': 'Internal BGP — between routers in the same AS',
}

BGP_PATH_ATTRIBUTES = {
    'weight': 'Cisco proprietary, highest weight preferred',
    'local_pref': 'Highest local preference preferred (within AS)',
    'as_path': 'Shortest AS_PATH preferred',
    'origin': 'IGP < EGP < Incomplete',
    'med': 'Multi-Exit Discriminator — lowest preferred',
}

# BGP route manipulation
BGP_POLICY = """
route-map SET-LOCAL-PREF permit 10
 match ip address prefix-list CUSTOMER
 set local-preference 200
!

route-map PREPEND permit 10
 set as-path prepend 64501 64501 64501
!
"""
```

## Common Pitfalls

1. **Route leaks** — accidentally announcing routes you shouldn't; use prefix filtering
2. **BGP hijacking** — malicious AS announces your prefixes; use RPKI/ROA
3. **No inbound traffic engineering** — can't control where traffic enters; use AS path prepending
4. **iBGP full mesh** — doesn't scale; use route reflectors or confederations
5. **No prefix limits** — peer can advertise unlimited prefixes; set max-prefix limits

## Verification Checklist

- [ ] iBGP design chosen (full mesh, route reflectors, or confederations)
- [ ] Inbound and outbound prefix filters configured
- [ ] RPKI/ROA validation implemented
- [ ] max-prefix limits set on all eBGP peers
- [ ] BGP monitoring (routes received, path flaps, convergence time)
- [ ] Traffic engineering policy documented
- [ ] BGP community strategy defined
