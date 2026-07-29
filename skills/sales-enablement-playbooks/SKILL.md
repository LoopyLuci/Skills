---
name: sales-enablement-playbooks
description: "Use when building sales enablement content and playbooks."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sales-enablement, playbooks, objection-handling, battle-cards, sales-training]
    related_skills: [crm-sales-pipeline, competitive-intelligence-analysis, product-management-roadmap, pricing-strategy-optimization]
---

# Sales Enablement and Playbooks

Building sales enablement programs — from playbooks and battle cards through objection handling, competitive positioning, and sales training content.

## When to Use

- Creating sales playbooks for your team
- Building competitive battle cards for sales calls
- Training sales reps on product positioning
- Developing objection handling responses
- Measuring sales enablement effectiveness

## Sales Playbook Framework

```python
from typing import Dict, List, Optional

class SalesPlaybook:
    """Create and manage sales playbooks."""
    
    def __init__(self, product_name: str, company: str):
        self.product = product_name
        self.company = company
        self.sections = {}
    
    def add_battle_card(self, competitor: str, positioning: str,
                        advantages: List[str], weaknesses: List[str],
                        objection_responses: List[Dict]) -> 'SalesPlaybook':
        self.sections[f'battle_card_{competitor}'] = {
            'type': 'battle_card',
            'competitor': competitor,
            'positioning': positioning,
            'advantages': advantages,
            'weaknesses': weaknesses,
            'objections': objection_responses,
        }
        return self
    
    def add_discovery_questions(self, role: str, questions: List[str]) -> 'SalesPlaybook':
        self.sections[f'discovery_{role}'] = {
            'type': 'discovery_questions',
            'target_role': role,
            'questions': questions,
        }
        return self
    
    def add_demo_flow(self, scenario: str, steps: List[str],
                      key_features: List[str]) -> 'SalesPlaybook':
        self.sections[f'demo_{scenario[:20]}'] = {
            'type': 'demo_flow',
            'scenario': scenario,
            'steps': steps,
            'key_features': key_features,
        }
        return self
    
    def generate_pdf(self) -> str:
        doc = f"📋 {self.company} — Sales Playbook\n" + "=" * 50 + "\n"
        for key, section in self.sections.items():
            if section['type'] == 'battle_card':
                doc += f"\n## Vs {section['competitor']}\n"
                doc += f"Positioning: {section['positioning']}\n"
                doc += f"Advantages: {', '.join(section['advantages'])}\n"
            elif section['type'] == 'discovery_questions':
                doc += f"\n## Discovery: {section['target_role']}\n"
                for q in section['questions']:
                    doc += f"  • {q}\n"
            elif section['type'] == 'demo_flow':
                doc += f"\n## Demo: {section['scenario']}\n"
                for s in section['steps']:
                    doc += f"  {s}\n"
        return doc


def standard_discovery_questions() -> Dict:
    return {
        'decision_maker': [
            "What's your top priority this quarter?",
            "How are you currently solving [problem]?",
            "What does success look like for this project?",
            "What's the timeline for making a decision?",
            "Who else is involved in the decision?",
        ],
        'economic_buyer': [
            "What budget has been allocated for this?",
            "How do you measure ROI on solutions like this?",
            "What's the cost of not solving this problem?",
            "Have you budgeted for implementation and training?",
        ],
        'technical_evaluator': [
            "What's your tech stack currently?",
            "What are your key integration requirements?",
            "What security/compliance requirements do you have?",
            "What's your evaluation process and timeline?",
        ],
    }
```

## Objection Handling

```python
OBJECTION_LIBRARY = {
    'too_expensive': {
        'category': 'pricing',
        'response_framework': 'LAER: Listen, Acknowledge, Explore, Respond',
        'responses': [
            "I understand budget is a concern. Can I ask what you're comparing it to?",
            "Many customers felt the same way until they saw the ROI. Let me share a case study.",
            "What if we could show a 3x return in the first 6 months? Would that change things?",
        ],
        'proof_points': ['ROI calculator', 'Case studies', 'TCO comparison'],
    },
    'happy_with_current': {
        'category': 'competitive',
        'response_framework': 'Feel, Felt, Found',
        'responses': [
            "I understand — many of our customers felt the same way with their previous solution. What they found was...",
            "What does your current solution NOT do that you wish it did?",
            "If you could change one thing about your current setup, what would it be?",
        ],
    },
    'not_now': {
        'category': 'timing',
        'responses': [
            "I understand timing isn't right. What would need to change for this to become a priority?",
            "What if we could get you up and running in a week with no commitment?",
            "Would you be open to a 30-minute intro demo so when the time comes, you're ready?",
        ],
    },
}

def get_objection_response(objection: str, industry: str = None) -> Dict:
    result = OBJECTION_LIBRARY.get(objection, {
        'responses': ["That's a great question. Let me address that..."],
    })
    return result
```

## Common Pitfalls

1. **Playbooks that sit on a shelf** — if reps don't use them, they're worthless; embed in workflow
2. **Generic content** — playbooks must address specific roles, competitors, and scenarios
3. **No objection handling practice** — having the responses isn't enough; role-play them
4. **Outdated battle cards** — competitor positioning changes monthly; update quarterly
5. **No measurement** — don't know if enablement improves win rates; track it

## Verification Checklist

- [ ] Sales playbook created with battle cards for top 3 competitors
- [ ] Discovery questions for each buyer role
- [ ] Demo flows for top 3 use cases
- [ ] Objection handling library with scripts
- [ ] Sales training sessions scheduled
- [ ] Playbook adoption tracked (are reps using it?)
- [ ] Win/loss analysis informing playbook updates

## See Also

- crm-sales-pipeline — pipeline management with enablement
- competitive-intelligence-analysis — battle card input
- product-management-roadmap — product positioning
- pricing-strategy-optimization — pricing objections
