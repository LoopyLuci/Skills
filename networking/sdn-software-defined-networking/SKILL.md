---
name: sdn-software-defined-networking
description: "Use when implementing SDN and network virtualization."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sdn, openflow, network-virtualization, SDN-controller, network-programmability]
    related_skills: [network-automation-scripting, container-networking-patterns, bgp-routing-patterns, terraform-module-patterns]
---

# Software-Defined Networking (SDN)

Implementing software-defined networking — from SDN controllers and OpenFlow through network virtualization, intent-based networking, and network programmability.

## When to Use

- Decoupling network control plane from data plane
- Implementing programmable network infrastructure
- Automating network provisioning and configuration
- Building virtual networks and network overlays
- Implementing intent-based networking

## SDN Architecture

```python
SDN_LAYERS = {
    'infrastructure': 'Physical/virtual switches, routers, middleboxes (data plane)',
    'control': 'SDN controller (ONOS, OpenDaylight, Ryu) — central control plane',
    'application': 'Network apps — routing, firewall, load balancing (business logic)',
}

# Mininet-style network topology definition
def create_topology():
    """Define a software-defined network topology."""
    return {
        'switches': ['s1', 's2', 's3'],
        'hosts': ['h1', 'h2', 'h3', 'h4'],
        'links': [
            ('h1', 's1'), ('h2', 's1'),
            ('h3', 's2'), ('h4', 's2'),
            ('s1', 's3'), ('s2', 's3'),
        ],
        'controller': 'ryu',
    }
```

## Common Pitfalls

1. **Controller bottleneck** — centralized controller becomes single point of failure; cluster it
2. **Flow table exhaustion** — OpenFlow switches have limited flow table entries
3. **Southbound latency** — control-to-data plane latency can impact convergence
4. **Security of controller** — compromised controller compromises entire network
5. **Vendor lock-in** — proprietary extensions reduce SDN benefits

## Verification Checklist

- [ ] SDN controller clustered for high availability
- [ ] Flow table size monitored on switches
- [ ] Southbound protocol secured (TLS for OpenFlow)
- [ ] Northbound API documented and versioned
- [ ] Network state synchronized across controller cluster
