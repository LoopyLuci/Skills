---
name: upsell-cross-sell-strategies
description: "Use when implementing upsell and cross-sell strategies."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [upsell, cross-sell, expansion-revenue, account-growth, product-bundles]
    related_skills: [customer-success-retention, product-led-growth, sales-enablement-playbooks, crm-sales-pipeline]
---

# Upsell and Cross-Sell Strategies

Implementing upsell and cross-sell strategies for revenue expansion — from identifying expansion opportunities through timing, sales motions, and bundle design.

## When to Use

- Increasing revenue from existing customers
- Designing product bundles and add-ons
- Building expansion revenue as a growth lever
- Training CS and sales teams on expansion selling
- Timing upsell/cross-sell offers for maximum conversion

## Expansion Strategies

```python
EXPANSION_STRATEGIES = {
    'usage_based': 'Customer exceeds plan limits → prompts upgrade',
    'feature_gating': 'Premium features visible but locked → upgrade nudge',
    'account_growth': 'More team members → seat expansion',
    'bundle': 'Related products offered together at discount',
    'upgrade_path': 'Starter → Professional → Enterprise with clear value jumps',
    'post_purchase': 'Complementary product offered after initial purchase',
}

class ExpansionMotion:
    """Design and track upsel/cross-sell motions."""
    
    MOTIONS = {
        'success_triggered': 'CS identifies need during check-in/renewal',
        'product_triggered': 'Usage data shows customer would benefit from upgrade',
        'marketing_triggered': 'Targeted campaign based on account profile',
        'support_triggered': 'Support ticket reveals need for premium feature',
    }
    
    @staticmethod
    def find_expansion_opportunities(accounts: List[Dict]) -> List[Dict]:
        """Score accounts by expansion potential."""
        for acct in accounts:
            score = 0
            if acct.get('usage_growth', 0) > 20: score += 3
            if acct.get('team_size', 0) > acct.get('licensed_seats', 0): score += 3
            if acct.get('support_tier') == 'enterprise': score += 2
            if acct.get('days_since_last_upsell', 999) > 180: score += 2
            if acct.get('nps_score', 0) >= 9: score += 2
            acct['expansion_score'] = score
        return sorted(accounts, key=lambda a: a['expansion_score'], reverse=True)
```

## Common Pitfalls

1. **Selling before value is proven** — upsell during onboarding erodes trust; wait for activation
2. **No clear value difference** — customers can't tell why they should upgrade; articulate tier value
3. **Too aggressive timing** — pitching upsell at every interaction annoys customers; use trigger-based
4. **Ignoring churn risk** — pushing expansion on accounts that are already churn risks; check health first
5. **No internal handoff** — CS identifies opportunity but sales doesn't follow up; create clear process

## Verification Checklist

- [ ] Expansion strategy identified (usage-based, feature-gated, bundle, seat-based)
- [ ] Account scoring model for expansion potential
- [ ] Trigger-based timing (usage threshold, value milestone, renewal)
- [ ] Sales-CS handoff process for expansion opportunities
- [ ] Clear product tier differentiation (value per tier)
- [ ] Bundle/packaging strategy (if applicable)
- [ ] Expansion revenue tracked as separate KPI
- [ ] Expansion motion tested and optimized (A/B offers, pricing, timing)
