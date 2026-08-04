---
name: carbon-accounting-standards
description: "Use when doing carbon accounting. GHG, scopes, reporting."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [climatetech, carbon-accounting, ghg-protocol, scope-123]
    related_skills: [climate-risk-assessment, sustainability-reporting]
---

# Carbon Accounting & GHG Protocol

## Overview
Measure, report, and verify greenhouse gas (GHG) emissions following GHG Protocol, ISO 14064, and IFRS sustainability standards. Covers scope 1, 2, 3 emissions calculation, carbon footprinting, offset quantification, and regulatory compliance.

## When to Use
- "Calculate Scope 1/2/3 emissions inventory"
- "Prepare carbon footprint for ESG reporting"
- "Align emissions with Science-Based Targets"
- "Implement carbon accounting system"
- "Track and verify carbon offset projects"

## GHG Protocol Scopes
- **Scope 1**: Direct emissions (fuel combustion, process emissions, fugitives)
- **Scope 2**: Indirect emissions (purchased electricity, steam, heat)
- **Scope 3**: Value chain emissions (15 categories)

## Emissions Calculation
```python
def calculate_scope_1(fuels, factors):
    """Calculate direct emissions from fuel combustion"""
    total = sum(amount * factors.get(f, 0) for f, amount in fuels.items())
    return round(total / 1000, 2)  # tons CO2e

EMISSION_FACTORS = {
    "natural_gas_kwh": 0.185,
    "diesel_litre": 2.68,
    "propane_litre": 1.53,
    "refrigerant_r134a": 1430
}
```

## Verification Checklist
- [ ] All 3 scopes inventoried
- [ ] Emission factors verified and current
- [ ] Scope 3 covers all applicable categories
- [ ] Third-party verification arranged
- [ ] SBTi targets set
- [ ] Internal carbon price applied
- [ ] Offset inventory tracked
- [ ] Reporting aligned with GRI/SASB/TCFD