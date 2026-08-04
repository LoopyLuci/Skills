---
name: drug-discovery-pipeline
description: "Use when planning drug discovery. Target ID to IND filing."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [drug-discovery, pharma, medicinal-chemistry, clinical-development]
    related_skills: [genomics-data-processing, bioinformatics-sequences-analysis]
---

# Drug Discovery Pipeline Management

## Overview
Navigate the complete drug discovery pipeline from target identification through IND (Investigational New Drug) filing. Covers target validation, hit identification, lead optimization, preclinical development, and regulatory strategy. Produces project timelines, milestone plans, and risk assessments.

## When to Use
- "Plan a drug discovery project timeline"
- "Identify and validate drug targets"
- "Screen compounds for hits"
- "Optimize lead compounds"
- "Prepare IND filing documentation"

## The Drug Discovery Pipeline Stages

### Stage 1: Discovery (0–4 years)
| Phase | Activities | Deliverables | Key Metrics |
|-------|-----------|-------------|-------------|
| Target ID & Validation | Bioinformatics, literature review, pathway analysis | Target dossier | Druggability score ≥0.5 |
| Hit Identification | HTS, fragment screening, virtual screening | 10–100 hit compounds | Hit rate ≥0.01% |
| Hit-to-Lead | SAR exploration, early potency optimization | 5–10 lead series | Potency <100 nM |
| Lead Optimization | Improve potency, selectivity, ADME | 2–3 clinical candidates | All CMC milestones met |

### Stage 2: Preclinical Development (1–3 years)
| Phase | Activities | Deliverables | Key Metrics |
|-------|-----------|-------------|-------------|
| Candidate Selection | Tox studies, efficacy models | Clinical candidate | Safety margin >10x |
| IND-Enabling Studies | GLP tox, genotox, carcinogenicity | IND package | All regulatory requirements |
| Formulation Development | Drug product development | Final formulation | Stability >24 months |
| Manufacturing Scale-up | GMP production | Phase 1 drug supply | ≥90% recovery |

### Stage 3: Clinical Development (6–10 years)
| Phase | Activities | Sample Size | Duration |
|-------|-----------|-------------|---------|
| Phase I | Safety, PK/PD in healthy volunteers | 20–100 | 1 year |
| Phase II | Dose-ranging, preliminary efficacy | 100–300 | 2 years |
| Phase III | Large-scale efficacy vs standard of care | 1,000–3,000+ | 3 years |
| NDA/BLA Filing | Regulatory submission | — | 6–12 months |

## Common Pitfalls
1. **Poor target selection** — 40% of failures stem from invalid targets. Use multi-omics validation.
2. **Ignoring ADME early** — compounds with poor absorption or metabolic stability sink late. Integrate ADME assays in hit-to-lead.
3. **Insufficient tox studies** — delays IND filing. Start tox studies 1.5 years before planned IND submission.
4. **Wrong species for tox** — use same species planned for clinical toxicology.
5. **CMC gaps** — manufacturing and analytical methods must be validated before first-in-human.
6. **Overpromising timelines** — account for setbacks. Build 20-30% buffer time into each phase.

## Verification Checklist
- [ ] Target validation with ≥3 orthogonal methods
- [ ] Hit rate >0.01% in primary screen
- [ ] Lead compound potency <100 nM with ≥10x selectivity
- [ ] In vitro ADME profile documented
- [ ] In vivo efficacy demonstrated in ≥2 disease models
- [ ] GLP toxicology study protocol approved
- [ ] IND-enabling chemistry complete with specification
- [ ] Regulatory strategy meeting scheduled with FDA/EMA
- [ ] GxP compliance documentation in place
- [ ] Risk assessment updated with latest data