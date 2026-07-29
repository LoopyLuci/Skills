---
name: legal-compliance-business
description: "Use when managing legal and regulatory compliance."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [legal, compliance, regulations, GDPR, CCPA, business-law, contracts]
    related_skills: [contract-management-basics, business-insurance-guide, hr-recruiting-onboarding, tax-planning-small-business]
---

# Legal Compliance for Business

Managing legal and regulatory compliance — from business formation and contracts through data privacy, employment law, and intellectual property.

## When to Use

- Ensuring business complies with relevant regulations
- Understanding data privacy requirements (GDPR, CCPA)
- Setting up proper legal agreements and terms
- Managing intellectual property and trademarks

## Compliance Areas

```python
COMPLIANCE_AREAS = {
    'data_privacy': 'GDPR (EU), CCPA/CPRA (California), LGPD (Brazil) — consent, access, deletion',
    'employment': 'Wage laws, anti-discrimination, termination, independent contractor rules',
    'ip': 'Trademarks (brand), copyrights (content), patents (inventions), trade secrets',
    'consumer_protection': 'Truth in advertising, refund policies, terms of service',
    'accessibility': 'ADA, WCAG 2.1 — website accessibility for users with disabilities',
}

def check_data_privacy_requirements(regions: List[str], data_types: List[str]) -> List[str]:
    requirements = []
    if 'GDPR' in regions: requirements += ['Privacy policy', 'Consent mechanism', 'DSAR process', 'Data processing agreement']
    if 'CCPA' in regions: requirements += ['Opt-out mechanism', 'Data disclosure process', 'Non-discrimination']
    if 'PHI' in data_types: requirements += ['HIPAA compliance', 'BAAs with vendors']
    return requirements
```

## Verification Checklist

- [ ] Privacy policy posted and compliant with applicable laws
- [ ] Terms of service/conditions of use in place
- [ ] Cookie consent mechanism implemented
- [ ] Data processing agreements with vendors
- [ ] Employee handbook with policies (anti-harassment, code of conduct)
- [ ] IP assignments for contractors and employees
- [ ] Trademarks registered (if applicable)
- [ ] Accessibility compliance (WCAG 2.1 AA target)
- [ ] Independent contractor vs employee classification reviewed
