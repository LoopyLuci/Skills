---
name: code-review-automation
description: "Use when automating code review processes."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [code-review, automation, linting, static-analysis, PR-checklist, CI]
    related_skills: [behavior-driven-development, testing-pyramid-practice, devsecops-shift-left, code-review-checklist]
---

# Code Review Automation

Automating code review processes — from static analysis and linting through automated PR checks, review assignment, and AI-assisted code review.

## When to Use

- Reducing manual review burden on senior engineers
- Catching common issues before human review
- Enforcing coding standards automatically
- Automating reviewer assignment based on expertise
- Building consistent PR quality gates

## Automation Patterns

```python
AUTOMATED_REVIEWS = {
    'linting': 'ESLint, Ruff, clang-format — style, formatting, basic errors',
    'static_analysis': 'SonarQube, CodeQL, Semgrep — bugs, security, complexity',
    'type_checking': 'mypy, TypeScript strict, Rust borrow checker — type safety',
    'test_cov': 'Ensure tests cover changed code, no coverage regression',
    'ai_review': 'LLM-assisted review for logic, edge cases, documentation',
}

class PRGate:
    """Automated PR review gates that must pass."""
    def __init__(self):
        self.gates = []
    
    def add_gate(self, name: str, check_fn: callable, 
                 required: bool = True):
        self.gates.append({'name': name, 'check': check_fn, 'required': required})
    
    def evaluate(self, pr_data: Dict) -> Dict:
        results = {}
        for gate in self.gates:
            try:
                passed = gate['check'](pr_data)
                results[gate['name']] = {'passed': passed}
            except Exception as e:
                results[gate['name']] = {'passed': False, 'error': str(e)}
        return results
```

## Verification Checklist

- [ ] Linting enforced in CI (fail on errors)
- [ ] Static analysis configured (security, complexity, duplication)
- [ ] Type checking in CI
- [ ] Test coverage gate (no decrease, or minimum threshold)
- [ ] Automated reviewer assignment (by expertise area)
- [ ] AI-assisted review integrated (summarize changes, flag concerns)
- [ ] PR template with checklist for human reviewers
- [ ] Review turnaround time tracked (SLA: <4 hours for team reviews)
