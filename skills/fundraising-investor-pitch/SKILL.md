---
name: fundraising-investor-pitch
description: "Use when preparing fundraising and investor presentations."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [fundraising, investor-pitch, venture-capital, startup-funding, deck, financial-model]
    related_skills: [financial-modeling-budgeting, saas-metrics-reporting, go-to-market-strategy, business-metrics-kpis]
---

# Fundraising and Investor Pitching

Preparing for venture fundraising — from pitch deck creation and financial modeling through investor outreach, due diligence, and term sheet negotiation.

## When to Use

- Raising a seed/Series A/B round
- Preparing an investor pitch deck
- Building financial projections for fundraising
- Managing due diligence process
- Negotiating term sheets

## Fundraising Stages

```python
FUNDRAISING_STAGES = {
    'pre_seed': '$100K-$1M, friends/family, pre-product', 
    'seed': '$1M-$5M, first institutional investors, early traction',
    'series_a': '$5M-$15M, product-market fit, repeatable revenue',
    'series_b': '$15M-$50M, scaling go-to-market, team growth',
    'series_c': '$50M+, market leadership, international expansion',
}

class PitchDeck:
    """Structure a startup pitch deck."""
    
    SLIDES = [
        'Title — Company name, tagline, founding team',
        'Problem — The pain point you solve (with story/data)',
        'Solution — Your product/service and how it works',
        'Market Size — TAM, SAM, SOM with credible sources',
        'Why Now — Market timing and tailwinds',
        'Product — Demo, screenshots, key features',
        'Traction — Revenue, users, growth metrics, logos',
        'Business Model — Unit economics, pricing, revenue model',
        'Competition — Landscape, your advantage (not a feature list)',
        'Team — Founders, key hires, advisory board',
        'Financials — 3-5 year projections with assumptions',
        'Ask — How much, what terms, use of funds',
    ]
    
    @staticmethod
    def ask_slide(amount: float, timeframe: str = '18 months') -> Dict:
        return {
            'raising': f"${amount:,.0f}",
            'timeframe': timeframe,
            'use_of_funds': {
                'Engineering': 0.40,
                'Sales & Marketing': 0.30,
                'Operations': 0.15,
                'Reserve': 0.15,
            },
        }
```

## Common Pitfalls

1. **No clear ask** — "we're raising $X" without explaining what you'll achieve
2. **Overly optimistic projections** — hockey-stick growth without basis; show realistic assumptions
3. **Too much product, not enough business** — investors care about market, traction, unit economics
4. **Ignoring competition** — claiming "no competitors" signals naivety
5. **Wrong investors** — pitching consumer VCs for enterprise product; target aligned investors

## Verification Checklist

- [ ] Pitch deck covers all 12 key slides
- [ ] Financial model with 3-5 year projections
- [ ] Use of funds clearly tied to milestones
- [ ] Competitive landscape analysis
- [ ] Target investor list (aligned stage + sector)
- [ ] Data room prepared (legal, financials, cap table, IP)
- [ ] Due diligence materials ready
- [ ] Term sheet fundamentals understood (valuation, liquidation preference, board)
