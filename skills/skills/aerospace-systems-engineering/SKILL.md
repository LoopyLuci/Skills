---
name: aerospace-systems-engineering
description: "Use when engineering aerospace systems. Safety, risk."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [aerospace, systems-engineering, safety-critical, requirements]
    related_skills: [orbital-mechanics, semiconductor-manufacturing]
---

# Aerospace Systems Engineering

## Overview
Design, develop, and validate safety-critical aerospace systems using systems engineering, risk management, and certification processes. Covers requirements engineering, system architecture, safety analysis (FMECA/HAZOP), testing/validation, and aerospace standards (DO-178C, DO-254, ARP4754A).

## When to Use
- "Design aerospace flight control system"
- "Perform safety analysis for aircraft systems"
- "Plan DO-178C software certification"
- "Manage aerospace requirements traceability"
- "Test aerospace systems with fault injection"

## Systems Engineering V-Model (ARP4754A)
```mermaid
V-Model: System Requirements → Architecture → Design → Implementation → Testing ← Verification ← Validation
```

### Requirements Traceability
```python
class AerospaceReqTraceability:
    def __init__(self):
        self.traceability_matrix = {}
    
    def add_requirement(self, req_id, safety_level, source="DO-178C"):
        """
        Add aerospace requirement with safety level (A-E)
        """
        self.traceability_matrix[req_id] = {
            "safety_level": safety_level,  # A=Catastrophic, B=Hazardous, C=Major, D=Minor, E=None
            "source": source,
            "design_elements": [],
            "test_cases": [],
            "verification_method": None
        }
```

## Safety Analysis Methods

### Functional Hazard Assessment (FHA)
| Condition | Level | Description |
|-----------|-------|-------------|
| Catastrophic | A | Multiple fatalities |
| Hazardous | B | Serious injury |
| Major | C | Minor injury |
| Minor | D | Passenger discomfort |

## Common Pitfalls
1. **Insufficient requirements traceability** — no linkage from req to design to test
2. **Not addressing all hazard conditions** — incomplete FHA analysis
3. **Wrong DO-178C level assignment** — safety level misidentified
4. **Insufficient test coverage** — especially MC/DC for Level A
5. **Poor configuration management** — lost changes during development
6. **Not conducting peer reviews** — required for all levels per DO-178C
7. **Inadequate safety margins** — hardware margins too tight
8. **Not planning contingencies** — off-nominal conditions not tested
9. **Skipping fault injection testing** — latent failures undetected
10. **Not maintaining certification artifacts** — audit trail gaps

## Verification Checklist
- [ ] Requirements traceable per DO-178C
- [ ] FHA/FTA completed for all safety levels
- [ ] Test coverage meets software level (MC/DC for Level A)
- [ ] Configuration management system active
- [ ] Peer reviews documented per DO-178C
- [ ] Fault injection testing completed