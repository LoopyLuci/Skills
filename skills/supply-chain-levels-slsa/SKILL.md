---
name: supply-chain-levels-slsa
description: "Use when implementing SLSA supply chain levels."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [SLSA, supply-chain, levels, integrity, provenance, build-attestation]
    related_skills: [software-bill-of-materials, devsecops-shift-left, ci-cd-pipeline-setup, container-security-hardening]
---

# SLSA Supply Chain Levels

Implementing SLSA (Supply-chain Levels for Software Artifacts) — from build integrity through provenance attestation, hermetic builds, and reproducible builds.

## When to Use

- Improving software supply chain security
- Meeting SLSA compliance requirements
- Ensuring build integrity and provenance
- Preventing supply chain attacks
- Building trustworthy CI/CD pipelines

## SLSA Levels

```python
SLSA_LEVELS = {
    1: 'Build script — automated builds, provenance exists (provenance shows source + build)',
    2: 'Version control + hosted build — source in VCS, build service runs build script',
    3: 'Hardened build — no user-defined build steps, hermetic, reproducible, dependencies verified',
    4: 'Two-party review — all changes reviewed, build independently verifiable, cryptographic signing',
}

class SLSACompliance:
    """Check SLSA level compliance of build pipeline."""
    
    def __init__(self):
        self.requirements = {
            1: ['Automated builds', 'Provenance generated'],
            2: ['Source in version control', 'Hosted build service', 'Provenance authenticated'],
            3: ['Hermetic builds', 'Reproducible builds', 'Dependencies verified', 'Build as code'],
            4: ['Two-party review', 'Build independent verification', 'Provenance signed by two parties'],
        }
    
    def check_level(self, current_fulfillments: List[str], target: int = 2) -> Dict:
        met = []
        unmet = []
        for req in self.requirements.get(target, []):
            if req in current_fulfillments: met.append(req)
            else: unmet.append(req)
        return {'level': target, 'met': len(met), 'total': len(met) + len(unmet), 'gaps': unmet}
```

## Verification Checklist

- [ ] Current SLSA level assessed
- [ ] Build provenance generated (in-toto attestation)
- [ ] Build service hosted (not developer machine)
- [ ] Build script defined as code (Dockerfile, CI config)
- [ ] Hermetic builds (no network access during build)
- [ ] Build artifacts signed (cosign or similar)
- [ ] Dependencies verified (checksums, SLSA-verified)
- [ ] Two-party review for code changes
