---
name: threat-modeling-stride
description: "Use when threat modeling systems and applications."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [threat-modeling, STRIDE, PASTA, attack-trees, DFD, risk-assessment]
    related_skills: [penetration-testing-methodology, vulnerability-assessment-scanning, webapp-penetration-testing, security-incident-response]
---

# Threat Modeling

Threat modeling systems and applications — from STRIDE and PASTA methodologies through Data Flow Diagrams, attack trees, and risk mitigation.

## When to Use

- Identifying security threats during system design
- Building threat models for existing applications
- Using STRIDE, PASTA, or LINDDUN methodologies
- Prioritizing security controls based on threat landscape

## Threat Modeling Methodologies

```python
THREAT_MODELING_METHODS = {
    'stride': 'Microsoft — Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation of Privilege',
    'pasta': 'Process for Attack Simulation and Threat Analysis — 7-stage risk-centric methodology',
    'linddun': 'Privacy-focused — Linkability, Identifiability, Non-repudiation, Det. Unlinkability, etc.',
    'attack_trees': 'Root goal (steal data) decomposed into sub-goals (phishing, exploit, physical)',
}

class ThreatModel:
    """Build threat models using STRIDE per component."""
    def __init__(self, system_name: str):
        self.name = system_name
        self.components = []
        self.data_flows = []
    
    def add_component(self, name: str, type: str = 'process', 
                       trust_boundary: str = 'internal'):
        self.components.append({
            'name': name, 'type': type, 'boundary': trust_boundary,
            'stride_threats': [],
        })
    
    def analyze_stride(self, component: str) -> List[str]:
        threats = []
        # Example analysis:
        if 'web' in component.lower():
            threats += ['Spoofing: user impersonation', 'Tampering: input validation', 'Info Disclosure: SQL injection']
        if 'database' in component.lower():
            threats += ['Tampering: unauthorized writes', 'Info Disclosure: unencrypted PII', 'DoS: connection exhaustion']
        return threats
```

## Verification Checklist

- [ ] System boundaries defined (trust boundaries, external entities)
- [ ] Data Flow Diagram (DFD) created
- [ ] STRIDE analysis per component/flow
- [ ] Threats ranked (DREAD or custom risk scoring)
- [ ] Mitigations identified per threat
- [ ] Attack trees for high-risk scenarios
- [ ] Threat model reviewed by stakeholders
- [ ] Threats tracked in remediation backlog
- [ ] Threat model updated when system changes
