---
name: influencer-affiliate-programs
description: "Use when building influencer and affiliate programs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [influencer-marketing, affiliate-marketing, partnerships, creator-economy]
    related_skills: [social-media-advertising, digital-marketing-strategy, ppc-advertising-management, ecommerce-platform-management]
---

# Influencer and Affiliate Marketing Programs

Building and managing influencer partnerships and affiliate marketing programs.

## When to Use

- Launching an influencer marketing program
- Building an affiliate/channel partner program
- Recruiting and onboarding partners
- Tracking performance and managing payouts
- Scaling creator partnerships

## Program Types

```python
PROGRAM_TYPES = {
    'influencer_gifting': {'compensation': 'Free product', 'best_for': 'Launches, awareness', 'effort': 'Low'},
    'influencer_paid': {'compensation': 'Flat fee + product', 'best_for': 'Campaigns, content', 'effort': 'Medium'},
    'affiliate_percentage': {'compensation': '10-30% commission', 'best_for': 'Ecommerce, SaaS', 'effort': 'High'},
    'ambassador': {'compensation': 'Tiered commission + perks', 'best_for': 'Loyalty, long-term', 'effort': 'High'},
}
```

## Influencer Vetting

```python
def score_influencer(profile: Dict) -> Dict:
    score = 0
    er = (profile.get('avg_likes', 0) + profile.get('avg_comments', 0)) / max(profile.get('followers', 1000), 1) * 100
    
    if er > 5: score += 30
    elif er > 2: score += 15
    else: score -= 10
    
    score += profile.get('niche_match', 50) * 0.3
    score += profile.get('content_quality', 5) * 3
    if profile.get('past_controversies'): score -= 40
    
    return {'score': round(score), 'rating': 'Excellent' if score >= 80 else 'Good' if score >= 60 else 'Fair' if score >= 40 else 'Poor'}
```

## Affiliate Program Manager

```python
class AffiliateManager:
    def __init__(self, commission=0.20):
        self.commission = commission
        self.affiliates = {}
    
    def add_affiliate(self, name: str, email: str, rate: float = None) -> str:
        import uuid; aid = str(uuid.uuid4())[:8]
        self.affiliates[aid] = {'id': aid, 'name': name, 'email': email,
            'commission': rate or self.commission, 'sales': 0, 'earned': 0.0}
        return aid
    
    def record_sale(self, aid: str, amount: float):
        if aid in self.affiliates:
            a = self.affiliates[aid]
            a['sales'] += 1
            a['earned'] += amount * a['commission']
```

## Common Pitfalls

1. **Vanity metrics** — engagement rate matters more than followers
2. **No tracking** — can't attribute sales without promo codes or links
3. **No contract** — verbal agreements lead to disputes
4. **No FTC disclosure** — ensure all paid posts are labeled #ad

## Verification Checklist

- [ ] Program type selected
- [ ] Vetting criteria defined
- [ ] Tracking system set up
- [ ] Commission structure defined
- [ ] FTC disclosure compliance

## See Also

- social-media-advertising — paid social alongside influencer
- digital-marketing-strategy — partnerships in strategy
- ecommerce-platform-management — affiliate integration
