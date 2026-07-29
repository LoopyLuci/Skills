---
name: software-bill-of-materials
description: "Use when managing software bill of materials."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [SBOM, software-bill-of-materials, dependency-tracking, SPDX, CycloneDX, supply-chain]
    related_skills: [supply-chain-levels-slsa, devsecops-shift-left, vulnerability-scanning, dependency-audit]
---

# Software Bill of Materials

Managing software bill of materials (SBOM) — from SBOM generation (SPDX, CycloneDX) through dependency tracking, vulnerability correlation, and supply chain security.

## When to Use

- Tracking third-party dependencies in software
- Complying with executive order on software supply chain security
- Vulnerability correlation (SBOM + CVE database)
- Supply chain risk assessment
- Building software supply chain transparency

## SBOM Generation

```python
SBOM_FORMATS = {
    'spdx': 'Software Package Data Exchange — ISO standard, broad adoption',
    'cyclonedx': 'OWASP standard — security-focused, vulnerability support',
    'swid': 'ISO/IEC 19770-2 — software identification tag',
}

def generate_sbom_python(requirements_path: str) -> Dict:
    """Generate SBOM from Python dependencies."""
    import pkg_resources, hashlib, json
    sbom = {
        '$schema': 'http://cyclonedx.org/schema/bom-1.5.schema.json',
        'bomFormat': 'CycloneDX', 'specVersion': '1.5',
        'components': [],
        'dependencies': [],
    }
    
    with open(requirements_path) as f:
        for line in f:
            pkg_name = line.strip().split('=')[0].split('>')[0].split('<')[0]
            if pkg_name:
                try:
                    pkg = pkg_resources.get_distribution(pkg_name)
                    sbom['components'].append({
                        'type': 'library', 'name': pkg.key,
                        'version': pkg.version, 'purl': f'pkg:pypi/{pkg.key}@{pkg.version}',
                    })
                except: pass
    return sbom
```

## Verification Checklist

- [ ] SBOM format chosen (SPDX or CycloneDX)
- [ ] SBOM generation automated in CI/CD pipeline
- [ ] All direct and transitive dependencies included
- [ ] SBOM validated against schema
- [ ] Vulnerability correlation (SBOM + CVE database)
- [ ] SBOM signed for integrity
- [ ] SBOM stored and versioned alongside releases
- [ ] Customer access to SBOM on request
