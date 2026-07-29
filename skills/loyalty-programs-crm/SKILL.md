---
name: loyalty-programs-crm
description: "Use when designing and managing customer loyalty programs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [loyalty, rewards, points, VIP, customer-retention, referral-programs]
    related_skills: [customer-success-retention, crm-sales-pipeline, email-marketing-campaigns, ecommerce-platform-management]
---

# Loyalty Programs and CRM

Designing and managing customer loyalty and rewards programs — from points-based systems through tiered VIP programs, referral rewards, and retention mechanics.

## When to Use

- Launching a customer loyalty program
- Designing points, rewards, or tiers system
- Building a referral program for customer acquisition
- Implementing VIP/status tiers
- Measuring loyalty program ROI and engagement

## Program Types

```python
LOYALTY_TYPES = {
    'points': {
        'description': 'Earn points per purchase, redeem for rewards',
        'best_for': 'Ecommerce, retail, food & beverage',
        'example': '$1 = 10 points, 500 points = $5 off',
        'complexity': 'Medium',
    },
    'tiered': {
        'description': 'Multiple status levels with increasing benefits',
        'best_for': 'Airlines, hotels, subscription services, B2B',
        'example': 'Silver → Gold → Platinum (based on annual spend)',
        'complexity': 'High',
    },
    'paid': {
        'description': 'Customer pays for membership to unlock benefits',
        'best_for': 'Ecommerce (Amazon Prime), retail (REI), subscriptions',
        'example': '$99/year for free shipping and exclusive perks',
        'complexity': 'Low',
    },
    'referral': {
        'description': 'Reward customers for referring new customers',
        'best_for': 'SaaS, services, any business with high LTV',
        'example': 'Give $20, get $20 when friend makes first purchase',
        'complexity': 'Low',
    },
    'cashback': {
        'description': 'Percentage of purchase returned as credit',
        'best_for': 'Credit cards, ecommerce, high-frequency purchases',
        'example': '5% cashback on every purchase',
        'complexity': 'Low',
    },
    'punch_card': {
        'description': 'Buy N items, get 1 free (digital punch card)',
        'best_for': 'Coffee shops, restaurants, local services',
        'example': 'Buy 10 coffees, get 1 free',
        'complexity': 'Very Low',
    },
}
```

## Loyalty Program Engine

```python
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

class LoyaltyProgram:
    """Manage loyalty program operations."""
    
    def __init__(self, name: str, program_type: str):
        self.name = name
        self.type = program_type
        self.members = {}
        self.rewards_catalog = []
        self.tiers = {}
    
    def add_tier(self, name: str, min_points: int, 
                 benefits: List[str], multiplier: float = 1.0) -> 'LoyaltyProgram':
        self.tiers[name] = {
            'min_points': min_points, 'benefits': benefits,
            'points_multiplier': multiplier,
        }
        return self
    
    def enroll_member(self, customer_id: str, name: str, 
                      email: str, initial_points: int = 0) -> str:
        self.members[customer_id] = {
            'id': customer_id, 'name': name, 'email': email,
            'points': initial_points, 'lifetime_points': initial_points,
            'tier': 'Standard', 'tier_progress': {},
            'referrals': 0, 'rewards_redeemed': 0,
            'enrolled_at': datetime.now().isoformat(),
        }
        self._update_tier(customer_id)
        return customer_id
    
    def add_points(self, customer_id: str, points: int, 
                   source: str = 'purchase'):
        if customer_id in self.members:
            member = self.members[customer_id]
            member['points'] += points
            member['lifetime_points'] += points
            self._update_tier(customer_id)
    
    def redeem_points(self, customer_id: str, points: int,
                      reward_id: str = None) -> bool:
        if customer_id in self.members and self.members[customer_id]['points'] >= points:
            self.members[customer_id]['points'] -= points
            self.members[customer_id]['rewards_redeemed'] += 1
            return True
        return False
    
    def _update_tier(self, customer_id: str):
        member = self.members[customer_id]
        lifetime = member['lifetime_points']
        current_tier = 'Standard'
        
        for tier_name, tier_config in sorted(self.tiers.items(), key=lambda x: x[1]['min_points'], reverse=True):
            if lifetime >= tier_config['min_points']:
                current_tier = tier_name
                break
        
        member['tier'] = current_tier
    
    def get_member_summary(self, customer_id: str) -> Dict:
        if customer_id not in self.members: return {}
        m = self.members[customer_id]
        return {
            'name': m['name'], 'tier': m['tier'],
            'points': m['points'], 'lifetime_points': m['lifetime_points'],
            'referrals': m['referrals'], 'rewards_redeemed': m['rewards_redeemed'],
        }
    
    def calculate_program_roi(self, total_program_cost: float) -> Dict:
        active = len(self.members)
        total_redeemed = sum(m['rewards_redeemed'] for m in self.members.values())
        return {
            'total_members': active,
            'total_rewards_redeemed': total_redeemed,
            'program_cost': total_program_cost,
            'cost_per_member': round(total_program_cost / max(active, 1), 2),
        }
```

## Referral Program Design

```python
REFERRAL_BEST_PRACTICES = {
    'incentive_structure': {
        'referrer': '$10-50 or equivalent in points/credit',
        'referee': '$10-50 discount on first purchase',
        'timing': 'Reward referrer after referee makes first purchase',
    },
    'promotion': [
        'Post-purchase email (best time to ask for referral)',
        'Account dashboard (always visible referral link)',
        'Post-delivery follow-up (after product experience)',
        'Social media share buttons',
    ],
    'tracking': {
        'unique_link': 'Per-customer referral link',
        'referral_code': 'Optional: promo code for friend',
        'cookie_window': '30-90 days for attribution',
    },
}

def estimate_referral_program(referrers: int, avg_referrals_per_person: float,
                               conversion_rate: float, avg_ltv: float,
                               reward_cost: float) -> Dict:
    total_referrals = referrers * avg_referrals_per_person
    converted = total_referrals * conversion_rate
    revenue = converted * avg_ltv
    cost = total_referrals * reward_cost
    
    return {
        'estimated_referrals': round(total_referrals),
        'estimated_conversions': round(converted),
        'estimated_revenue': round(revenue, 2),
        'program_cost': round(cost, 2),
        'net_roi': round((revenue - cost) / max(cost, 1), 2),
    }
```

## Common Pitfalls

1. **Too complex to understand** — customers won't engage if they can't figure it out
2. **Rewards not valuable enough** — 1% cashback doesn't drive behavior change
3. **Points expiry too aggressive** — expiring in 30 days frustrates customers
4. **No tier differentiation** — if everyone is VIP, no one is VIP
5. **Poor tracking and attribution** — can't measure if program is working
6. **Not promoting the program** — customers can't join what they don't know about

## Verification Checklist

- [ ] Program type selected (points, tiered, paid, referral, cashback, punch)
- [ ] Points earning structure defined (per dollar)
- [ ] Reward catalog with clear redemption options
- [ ] Tier structure with meaningful benefits
- [ ] Referral program with dual-sided incentives
- [ ] Tracking system for points, tiers, referrals
- [ ] Program promoted at key touchpoints (purchase, account, email)
- [ ] ROI measurement framework established
- [ ] Terms and conditions documented

## See Also

- customer-success-retention — retention through loyalty
- ecommerce-platform-management — integrating loyalty with store
- email-marketing-campaigns — loyalty program communications
- crm-sales-pipeline — customer tier tracking in CRM
