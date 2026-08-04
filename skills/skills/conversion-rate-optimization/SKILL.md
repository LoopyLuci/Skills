---
name: conversion-rate-optimization
description: "Use when optimizing landing pages and conversion rates."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [CRO, conversion, landing-pages, A/B-testing, optimization, UX]
    related_skills: [marketing-funnel-design, ab-testing-experimentation, website-analytics-tracking, digital-marketing-strategy]
---

# Conversion Rate Optimization (CRO)

Optimizing websites and landing pages to maximize conversion rates — from user research and hypothesis generation through A/B testing, implementation, and analysis.

## When to Use

- Improving conversion rates on landing pages, signup flows, checkout
- Reducing bounce rates and increasing engagement
- Optimizing forms, CTAs, and page layouts
- Data-driven UX improvements based on user behavior
- Maximizing ROI from existing traffic

## CRO Framework

```
Research → Hypothesis → Design → Implement → Test → Analyze → Learn
   ↑                                                     │
   └─────────────────── Iterate ─────────────────────────┘
```

## Heuristic Analysis

```python
from typing import Dict, List

class HeuristicAnalyzer:
    """Analyze page elements against CRO best practices."""
    
    HEURISTICS = {
        'clarity': {
            'headline': 'Does the headline clearly communicate the value proposition?',
            'cta': 'Is the primary CTA obvious and compelling?',
            'offer': 'Can users understand what they get in 5 seconds?',
        },
        'relevance': {
            'audience_match': 'Does the page match the audience from the traffic source?',
            'message_match': 'Does the headline match the ad/link that brought them here?',
        },
        'urgency': {
            'scarcity': 'Is there a reason to act now? (limited time, stock, offer)',
            'fomo': 'Is there social proof showing others are taking action?',
        },
        'trust': {
            'social_proof': 'Are testimonials, reviews, or logos visible?',
            'security': 'Are security badges, guarantees, or privacy statements shown?',
            'credibility': 'Are credentials, awards, or media mentions displayed?',
        },
        'friction': {
            'form_length': 'Is the form as short as possible?',
            'page_speed': 'Does the page load in under 3 seconds?',
            'mobile': 'Is the page fully optimized for mobile?',
            'distractions': 'Are there unnecessary links or navigation options?',
        },
    }
    
    @staticmethod
    def analyze_page(page_elements: Dict) -> Dict:
        """Score a page against CRO heuristics."""
        scores = {}
        recommendations = []
        
        for category, checks in HeuristicAnalyzer.HEURISTICS.items():
            category_score = 0
            category_total = len(checks)
            
            for check_name, question in checks.items():
                # Check if element exists
                element = page_elements.get(check_name)
                if element:
                    category_score += 1
                else:
                    recommendations.append(f"{category}: {check_name} — {question}")
            
            scores[category] = round(category_score / category_total * 100, 1) if category_total > 0 else 0
        
        overall = round(sum(scores.values()) / len(scores), 1) if scores else 0
        
        return {
            'scores': scores,
            'overall': overall,
            'rating': 'Excellent' if overall >= 80 else 'Good' if overall >= 60 else 'Needs improvement',
            'recommendations': recommendations,
        }
```

## Hypothesis Builder

```python
class CROHypothesis:
    """Build and prioritize CRO test hypotheses."""
    
    def __init__(self, description: str, element: str, 
                 change: str, expected_impact: str,
                 confidence: str = 'medium', effort: str = 'medium'):
        self.description = description
        self.element = element
        self.change = change
        self.expected = expected_impact
        self.confidence = confidence
        self.effort = effort
    
    @property
    def score(self) -> float:
        """PIE score (Potential, Importance, Ease)."""
        scores = {'high': 10, 'medium': 7, 'low': 3}
        potential = scores.get(self.expected.replace('increase ', '').replace('reduce ', '').strip(), 5)
        importance = scores.get(self.confidence, 5)
        ease = scores.get(self.effort, 5) * -1 + 11  # Invert: high effort = low ease
        return round((potential + importance + ease) / 3, 1)
    
    def to_dict(self) -> Dict:
        return {
            'description': self.description,
            'element': self.element,
            'change': self.change,
            'expected_impact': self.expected,
            'confidence': self.confidence,
            'effort': self.effort,
            'ice_score': self.score,
        }


class HypothesisGenerator:
    """Generate CRO test hypotheses based on common patterns."""
    
    PATTERNS = {
        'cta': [
            ("Change CTA button color to contrast with page", "high", "low"),
            ("Make CTA text specific and benefit-driven", "high", "low"),
            ("Add urgency to CTA ('Limited time' / 'Only X left')", "medium", "low"),
            ("Move CTA above the fold", "high", "medium"),
            ("Add directional cue pointing to CTA", "low", "low"),
        ],
        'headline': [
            ("Add subheadline that reinforces the value prop", "high", "low"),
            ("Test benefit-driven vs feature-driven headline", "medium", "low"),
            ("Add number/data point to headline", "medium", "low"),
        ],
        'social_proof': [
            ("Add customer testimonial near CTA", "high", "medium"),
            ("Add logo strip of recognizable clients", "medium", "medium"),
            ("Show real-time social proof (X people viewing)", "medium", "high"),
            ("Add case study result statistic", "high", "medium"),
        ],
        'form': [
            ("Reduce form fields to absolute minimum", "high", "medium"),
            ("Add inline validation errors", "medium", "medium"),
            ("Use single-column layout", "medium", "low"),
            ("Add trust elements near form/CTA", "medium", "low"),
        ],
        'trust': [
            ("Add money-back guarantee badge", "high", "low"),
            ("Add security seal near payment form", "medium", "low"),
            ("Display total price upfront (no hidden fees)", "high", "low"),
            ("Add FAQ section to address objections", "medium", "high"),
        ],
        'urgency': [
            ("Add countdown timer for limited-time offer", "high", "medium"),
            ("Show low stock alert", "medium", "high"),
            ("Display 'X people bought this today'", "medium", "high"),
        ],
    }
    
    @staticmethod
    def generate_hypotheses(page_area: str = None) -> List[Dict]:
        """Generate test hypotheses for a page area."""
        if page_area and page_area in HypothesisGenerator.PATTERNS:
            patterns = {page_area: HypothesisGenerator.PATTERNS[page_area]}
        else:
            patterns = HypothesisGenerator.PATTERNS
        
        hypotheses = []
        for area, tests in patterns.items():
            for desc, conf, effort in tests:
                h = CROHypothesis(
                    description=desc,
                    element=area,
                    change=desc.split(' ')[1:4],  # Simplified extraction
                    expected_impact=f"increase conversion",
                    confidence=conf,
                    effort=effort,
                )
                hypotheses.append(h.to_dict())
        
        return sorted(hypotheses, key=lambda h: h['ice_score'], reverse=True)
```

## Elements to Test

```python
TEST_PRIORITY_MATRIX = {
    'high_impact_low_effort': [
        'CTA button text, color, size, placement',
        'Headline and subheadline',
        'Form length (remove fields)',
        'Trust badges near conversion points',
        'Social proof placement',
        'Page load speed optimization',
    ],
    'high_impact_high_effort': [
        'Complete page redesign',
        'Navigation structure',
        'Pricing page layout and tiers',
        'Checkout flow redesign',
        'New landing page template',
    ],
    'low_impact_low_effort': [
        'Image placement and selection',
        'Font size and readability',
        'Button microcopy changes',
        'Color scheme variations',
    ],
}

def recommend_test_priority(budget: str, timeline: str) -> List[str]:
    """Recommend what to test based on resources."""
    if budget == 'low' and timeline == 'short':
        return TEST_PRIORITY_MATRIX['high_impact_low_effort']
    elif budget == 'high':
        return TEST_PRIORITY_MATRIX['high_impact_high_effort']
    return TEST_PRIORITY_MATRIX['high_impact_low_effort']
```

## Common Pitfalls

1. **Testing without traffic** — statistical significance requires sufficient sample size; don't test with <1000 visitors
2. **Stopping too early** — peeking at results and stopping at "significant" inflates false positives; set sample size in advance
3. **Testing too many things at once** — changes compound, can't attribute cause; test one element at a time
4. **Ignoring micro-conversions** — optimize for email signups, add-to-cart, not just final purchase
5. **Confirmation bias** — running tests hoping for a specific result; let data decide
6. **Not segmenting results** — overall results can hide lift in specific segments; analyze by device, source, new vs returning

## Verification Checklist

- [ ] CRO heuristic analysis completed
- [ ] Top 5 hypotheses prioritized by ICE score
- [ ] Test plan with single variable changes
- [ ] Sample size calculated before test starts
- [ ] Test duration set (minimum 7 days to capture day-of-week effects)
- [ ] Goals defined (primary and secondary)
- [ ] Results analyzed with statistical significance (≥95%)
- [ ] Winners implemented and losers documented
- [ ] Learnings documented for future tests

## See Also

- ab-testing-experimentation — A/B testing methodology
- marketing-funnel-design — optimizing funnel stage conversion
- website-analytics-tracking — measuring CRO test results
- digital-marketing-strategy — CRO as part of strategy
