---
name: agent-ethics-alignment
description: "Use when implementing ethics and alignment for agents."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agent-ethics, alignment, safety, guardrails, values, constraints]
    related_skills: [agent-safety-monitoring, ai-fairness-mitigation, agent-safety-alignment, rlhf-implementation-guide]
---

# Agent Ethics and Alignment

Implementing ethics and alignment for AI agents — from value definition and constraint enforcement through ethical reasoning frameworks and alignment monitoring.

## When to Use

- Ensuring agent actions align with human values
- Implementing ethical constraints on agent behavior
- Building guardrails that prevent harmful actions
- Monitoring agent alignment during operation
- Designing transparent and accountable agent systems

## Ethics Framework

```python
ETHICS_PRINCIPLES = {
    'beneficence': 'Act to benefit humans and avoid harm',
    'non_maleficence': 'Do not cause harm through action or inaction',
    'autonomy': 'Respect human decision-making and informed consent',
    'justice': 'Distribute benefits and burdens fairly',
    'transparency': 'Agent decisions should be explainable and auditable',
}

class EthicalConstraint:
    """Define and enforce ethical constraints on agent actions."""
    def __init__(self):
        self.constraints = []
        self.action_log = []
    
    def add_constraint(self, name: str, check_fn: callable, 
                       severity: str = 'block'):
        self.constraints.append({
            'name': name, 'check': check_fn, 'severity': severity,
        })
    
    def evaluate_action(self, action: Dict) -> Dict:
        for c in self.constraints:
            result = c['check'](action)
            if not result['passed']:
                self.action_log.append({'action': action, 'constraint': c['name'], 'blocked': True})
                return {'allowed': False, 'reason': result['reason']}
        return {'allowed': True}
```

## Verification Checklist

- [ ] Ethics principles defined (beneficence, non-maleficence, autonomy, justice, transparency)
- [ ] Constraints implementable as code checks
- [ ] Block vs warn severity levels for different violations
- [ ] Agent actions logged for audit and review
- [ ] Human override mechanism for edge cases
- [ ] Alignment tested with adversarial scenarios
- [ ] Ethics review before deploying new agent capabilities
