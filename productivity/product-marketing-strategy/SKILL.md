---
name: product-marketing-strategy
description: "Use when creating product marketing strategies."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [product-marketing, positioning, messaging, launch, buyer-persona, GTM]
    related_skills: [go-to-market-strategy, product-led-growth, demand-generation, content-marketing-workflow]
---

# Product Marketing Strategy

Creating product marketing strategies — from positioning and messaging through buyer personas, competitive differentiation, launch plans, and sales enablement.

## When to Use

- Launching a new product or feature
- Developing product positioning and messaging
- Creating buyer personas and understanding customer needs
- Building sales enablement materials
- Planning product launches

## Product Marketing Framework

```python
PRODUCT_MARKETING = {
    'positioning': 'Define market category, target audience, unique value proposition',
    'messaging': 'Value prop → key messages → proof points → elevator pitch',
    'personas': 'Buyer persona, user persona, economic buyer, champion',
    'differentiation': 'Competitive matrix, unique advantages, positioning map',
    'launch': 'Internal launch → Early access → Public launch → Post-launch',
}

class ProductMarketing:
    """Build product marketing strategy."""
    def __init__(self, product: str):
        self.product = product
        self.positioning = {}
    
    def define_positioning(self, target: str, category: str, 
                           value_prop: str, competitors: List[str]):
        self.positioning = {
            'target': target, 'category': category,
            'value_proposition': value_prop,
            'competitors': competitors,
            'elevator_pitch': f"For {target}, our {self.product} helps {value_prop}",
        }
    
    def messaging_house(self) -> Dict:
        return {
            'root': self.positioning.get('value_prop', ''),
            'pillars': ['Feature benefit 1', 'Feature benefit 2', 'Feature benefit 3'],
            'proof': ['Case study', 'Testimonial', 'Data point'],
        }
```

## Verification Checklist

- [ ] Positioning defined (target, category, value proposition, competitors)
- [ ] Buyer personas created (goals, pains, decision criteria)
- [ ] Messaging hierarchy (root → pillars → proof points)
- [ ] Competitive differentiation documented
- [ ] Launch plan with phases (internal, early access, public, post-launch)
- [ ] Sales enablement materials (deck, battle card, FAQ, case studies)
- [ ] Launch metrics defined (awareness, pipeline, revenue)
