---
name: infrastructure-policy-as-code
description: "Use when implementing policy as code for infrastructure."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [policy-as-code, OPA, Sentinel, Kyverno, conftest, compliance]
    related_skills: [gitops-argocd-flux, cloud-cost-optimization-finops, terraform-module-patterns, devsecops-shift-left]
---

# Infrastructure Policy as Code

Implementing policy as code — from OPA/Rego and Kyverno through compliance checks in CI/CD, admission controllers, and infrastructure governance.

## When to Use

- Enforcing infrastructure compliance (security, cost, naming)
- Automated policy checking in CI/CD pipelines
- Kubernetes admission control
- Multi-cloud policy governance
- Security and compliance automation

## Policy Engines

```python
POLICY_ENGINES = {
    'opa': 'Open Policy Agent — Rego language, versatile, CI + admission control',
    'kyverno': 'Kubernetes-native, YAML policies, mutate/validate/generate',
    'conftest': 'OPA-based, test configuration files in CI (Terraform, K8s, Docker)',
    'sentinel': 'HashiCorp — Terraform Cloud/Enterprise, policy-as-code for IaC',
}

# OPA/Rego example: enforce required labels
REGO_POLICY = """
package kubernetes.admission

deny[msg] {
    input.request.kind.kind == "Deployment"
    not input.request.object.metadata.labels.owner
    msg := "Deployments must specify 'owner' label"
}

deny[msg] {
    input.request.object.metadata.labels.environment
    env := input.request.object.metadata.labels.environment
    not env in ["dev", "staging", "prod"]
    msg := sprintf("Invalid environment: %v", [env])
}
"""

def check_with_conftest(config_path: str, policy_path: str) -> List[str]:
    import subprocess, json
    result = subprocess.run(
        ['conftest', 'test', config_path, '-p', policy_path, '--output', 'json'],
        capture_output=True, text=True
    )
    output = json.loads(result.stdout)
    return [f['message'] for f in output if not f.get('success', True)]
```

## Verification Checklist

- [ ] Policy engine selected (OPA, Kyverno, Conftest, Sentinel)
- [ ] Policies defined for security (public S3 buckets, privileged containers)
- [ ] Policies defined for cost (instance types, regions, tags)
- [ ] CI/CD integration (conftest in pipeline)
- [ ] Admission controller deployed (Kyverno/OPA Gatekeeper)
- [ ] Policy exceptions handling (break-glass procedure)
- [ ] Policy tests written (conftest test cases)
