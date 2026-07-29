---
name: devsecops-shift-left
description: "Use when implementing DevSecOps and shift-left security."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [DevSecOps, shift-left, SAST, DAST, SCA, security-testing, CI-security]
    related_skills: [software-bill-of-materials, supply-chain-levels-slsa, continuous-integration-advanced, security-audit-standards]
---

# DevSecOps and Shift-Left Security

Implementing DevSecOps practices — from SAST/DAST/SCA scanning in CI through threat modeling, secrets detection, and security champions program.

## When to Use

- Integrating security into development workflows
- Shifting security testing left (earlier in development)
- Automating vulnerability scanning in CI/CD
- Building security champions culture

## DevSecOps Tools

```python
DEVSECOPS_TOOLS = {
    'sast': 'Static Analysis — Semgrep, SonarQube, CodeQL — find vulnerabilities in source code',
    'dast': 'Dynamic Analysis — OWASP ZAP, Burp Suite — test running applications',
    'sca': 'Software Composition Analysis — Dependabot, Snyk, Trivy — dependency vulnerabilities',
    'secrets': 'Secret detection — GitGuardian, truffleHog, Gitleaks — prevent credential leaks',
    'container_scan': 'Image scanning — Trivy, Grype, Clair — vulnerabilities in container images',
}

class DevSecOpsPipeline:
    """Security gates in CI/CD pipeline."""
    def __init__(self):
        self.gates = []
    
    def add_gate(self, name: str, tool: str, fail_on: str = 'critical'):
        self.gates.append({'name': name, 'tool': tool, 'fail_on': fail_on})
    
    def run_gates(self):
        results = {}
        for gate in self.gates:
            results[gate['name']] = self._execute(gate['tool'], gate['fail_on'])
        return results
```

## Verification Checklist

- [ ] SAST scanning in PR pipeline (fail on critical findings)
- [ ] SCA/dependency scanning automated (alert on new CVEs)
- [ ] Secrets scanning in pre-commit hooks and CI
- [ ] DAST scheduled for deployed applications
- [ ] Container image scanning in CI
- [ ] Threat modeling for new features (STRIDE)
- [ ] Security champions program across development teams
- [ ] Security training for developers (OWASP Top 10)
