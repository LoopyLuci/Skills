---
name: pricing-strategy-optimization
description: "Use when developing pricing strategies and models."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pricing, strategy, monetization, packaging, tiers, value-based, discounting]
    related_skills: [product-management-roadmap, saas-metrics-reporting, competitive-intelligence-analysis, ecommerce-platform-management]
---

# Pricing Strategy and Optimization

Developing and optimizing pricing strategies — from value-based pricing and tiered models through discounts, packaging, pricing experiments, and elasticity analysis.

## When to Use

- Setting initial pricing for a new product
- Optimizing existing pricing to increase revenue
- Designing pricing tiers and packaging
- Running pricing experiments and A/B tests
- Analyzing price elasticity and willingness to pay

## Pricing Models

```python
PRICING_MODELS = {
    'cost_plus': {
        'description': 'Cost + desired margin',
        'best_for': 'Physical products, manufacturing, retail',
        'formula': 'Price = Cost / (1 - Desired Margin)',
    },
    'value_based': {
        'description': 'Based on perceived value to customer',
        'best_for': 'B2B, SaaS, services, differentiated products',
        'formula': 'Price = Value Delivered × Share of Value Captured',
    },
    'competitor_based': {
        'description': 'Match, undercut, or premium vs competitors',
        'best_for': 'Commodity products, competitive markets',
        'formula': 'Price = Competitor Price ± Differentiation Premium',
    },
    'tiered': {
        'description': 'Multiple tiers with different feature sets',
        'best_for': 'SaaS, subscriptions, services',
        'formula': 'Basic (low) → Pro (medium) → Enterprise (high)',
    },
    'penetration': {
        'description': 'Low initial price to gain market share',
        'best_for': 'New markets, competitive entry',
        'formula': 'Low price → gain users → raise over time',
    },
    'skimming': {
        'description': 'High initial price, lower over time',
        'best_for': 'Innovation, limited competition, early adopters',
        'formula': 'High price → lower as competition enters',
    },
    'freemium': {
        'description': 'Free basic tier, paid premium',
        'best_for': 'SaaS, apps, platforms with network effects',
        'formula': 'Free (limited) → Paid (full)',
    },
    'usage_based': {
        'description': 'Pay for what you use (per-unit)',
        'best_for': 'APIs, cloud services, utilities',
        'formula': 'Price × Units Consumed',
    },
}

def recommend_model(product_type: str, market: str, differentiation: str) -> str:
    if product_type == 'physical':
        return 'cost_plus'
    elif market == 'new' and differentiation == 'high':
        return 'skimming'
    elif market == 'competitive' and differentiation == 'low':
        return 'competitor_based'
    elif product_type in ('saas', 'digital'):
        return 'tiered'
    return 'value_based'
```

## Tier Design

```python
class TierDesigner:
    """Design SaaS/software pricing tiers."""
    
    def __init__(self, base_name: str, base_price: float):
        self.base = base_name
        self.price = base_price
        self.tiers = []
    
    def add_tier(self, name: str, price: float, 
                 features: List[str], limits: Dict = None) -> 'TierDesigner':
        self.tiers.append({
            'name': name,
            'price': price,
            'price_display': f"${price:.0f}/mo" if price < 1000 else f"${price:.0f}/yr",
            'features': features,
            'limits': limits or {},
        })
        return self
    
    def validate_tiers(self) -> List[str]:
        """Check tier design best practices."""
        issues = []
        prices = [t['price'] for t in self.tiers]
        
        # 3 tiers is optimal (Goldilocks effect)
        if len(self.tiers) < 2:
            issues.append("Add at least one more tier (3-tier is optimal)")
        elif len(self.tiers) > 4:
            issues.append("Too many tiers — consider consolidating")
        
        # Price multiples
        if len(prices) >= 2:
            ratios = [prices[i+1]/prices[i] for i in range(len(prices)-1)]
            for i, ratio in enumerate(ratios):
                if ratio < 1.5:
                    issues.append(f"Price gap between {self.tiers[i]['name']} and {self.tiers[i+1]['name']} is small (<1.5x)")
                elif ratio > 4:
                    issues.append(f"Large price gap ({ratio:.1f}x) between {self.tiers[i]['name']} and {self.tiers[i+1]['name']}")
        
        if not issues:
            issues.append("Tier structure follows best practices")
        
        return issues
    
    def generate_pricing_page(self) -> str:
        page = f"\n💰 {self.base} — Pricing\n" + "=" * 40 + "\n"
        for t in self.tiers:
            page += f"\n**{t['name']}** — {t['price_display']}\n"
            for f in t['features']:
                page += f"  ✅ {f}\n"
            if t['limits']:
                for k, v in t['limits'].items():
                    page += f"  📊 {k}: {v}\n"
            page += "\n" + "-" * 30 + "\n"
        return page
```

## Pricing Experiment

```python
class PricingExperiment:
    """Design and analyze pricing experiments."""
    
    @staticmethod
    def van_westendorp(survey_responses: List[Dict]) -> Dict:
        """Van Westendorp Price Sensitivity Meter.
        
        Asks: At what price is this product...
        - Too expensive (would not consider)
        - Expensive (but would consider)
        - Cheap (a bargain)
        - Too cheap (quality concerns)
        """
        too_cheap = [r['too_cheap'] for r in survey_responses if r.get('too_cheap')]
        cheap = [r['cheap'] for r in survey_responses if r.get('cheap')]
        expensive = [r['expensive'] for r in survey_responses if r.get('expensive')]
        too_expensive = [r['too_expensive'] for r in survey_responses if r.get('too_expensive')]
        
        def median(vals): return sorted(vals)[len(vals)//2] if vals else 0
        
        return {
            'point_of_marginal_cheapness': median(cheap),
            'point_of_marginal_expensiveness': median(expensive),
            'optimal_price_point': median(cheap + expensive) // 2,
            'indifference_price_point': median(cheap + expensive) // 2,
        }
    
    @staticmethod
    def conjoint_analysis(feature_levels: List[Dict], 
                          responses: List[Dict]) -> Dict:
        """Simple conjoint analysis to determine feature willingness-to-pay."""
        utilities = {}
        for level in feature_levels:
            name = level['name']
            avg_utility = 0
            count = 0
            for r in responses:
                if name in r.get('chosen', {}):
                    avg_utility += r['chosen'].get('price', 0)
                    count += 1
            utilities[name] = round(avg_utility / max(count, 1), 2)
        return utilities
```

## Discounting Strategy

```python
DISCOUNTING_GUIDELINES = {
    'annual_subscription': {
        'recommended_discount': '15-20%',
        'rationale': 'Reduces churn, improves cash flow, increases LTV',
        'impact_on_metrics': 'Lower MRR but higher ARR, lower churn',
    },
    'enterprise_deal': {
        'recommended_discount': '10-30% (volume-based)',
        'rationale': 'Larger deals justify discount; protect list price',
        'impact_on_metrics': 'Higher ACV but lower ARPU',
    },
    'first_time_buyer': {
        'recommended_discount': '15-25%',
        'rationale': 'Reduces barrier to trial; can expire after first period',
        'impact_on_metrics': 'Higher conversion rate, may attract price-sensitive customers',
    },
    'win_back': {
        'recommended_discount': '25-50%',
        'rationale': 'Lapsed customers need more incentive to return',
        'impact_on_metrics': 'Recovers some churned MRR',
    },
    'bundling': {
        'recommended_discount': '10-25% off bundle vs individual',
        'rationale': 'Increases perceived value, reduces comparison shopping',
        'impact_on_metrics': 'Higher AOV, lower churn',
    },
}

def recommend_discount(scenario: str, deal_size: float = None) -> Dict:
    guide = DISCOUNTING_GUIDELINES.get(scenario, {})
    return guide
```

## Common Pitfalls

1. **Cost-plus ignores value** — customers don't care about your costs; price to value
2. **Too many tiers** — analysis paralysis; 3-4 tiers max
3. **Not testing pricing** — pricing is the most impactful lever; A/B test it
4. **Discounting without discipline** — discounts train customers to wait for sales; use sparingly
5. **Anchoring too low** — you can always discount but rarely raise prices; start higher
6. **Ignoring psychology** — $99 feels significantly cheaper than $100; use charm pricing

## Verification Checklist

- [ ] Pricing model selected (value-based, cost-plus, competitor, etc.)
- [ ] Willingness-to-pay research conducted
- [ ] Tier structure follows best practices (3 tiers, clear differentiation)
- [ ] Price anchoring strategy defined
- [ ] Discount policy documented (who, when, how much)
- [ ] Annual/monthly pricing with appropriate discount
- [ ] Pricing page clearly communicates value per tier
- [ ] A/B testing plan for pricing changes

## See Also

- product-management-roadmap — pricing for product tiers
- saas-metrics-reporting — measuring pricing impact on revenue
- competitive-intelligence-analysis — market pricing benchmarks
- ecommerce-platform-management — ecommerce pricing strategies
