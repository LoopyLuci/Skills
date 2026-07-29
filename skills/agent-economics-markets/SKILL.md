---
name: agent-economics-markets
description: "Use when designing agent economies and market systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agent-economics, markets, auctions, pricing, resource-allocation, token-economy]
    related_skills: [agent-negotiation-strategies, multi-agent-collaboration-patterns, agent-evaluation-metrics, agent-cost-optimization]
---

# Agent Economics and Markets

Designing economic systems for multi-agent environments — from resource allocation and pricing through auction mechanisms, token economies, and market-based control.

## When to Use

- Allocating scarce resources among competing agents
- Implementing pricing mechanisms for agent services
- Building auction systems for task distribution
- Creating token economies for agent incentives
- Designing market-based control systems

## Economic Mechanisms

```python
ECONOMIC_MECHANISMS = {
    'price_mechanism': 'Agents bid for resources, market clears at equilibrium price',
    'auction': 'Tasks or resources allocated via auction (English, Dutch, Vickrey)',
    'token_economy': 'Agents earn/spend tokens for services and resources',
    'barter': 'Agents exchange services directly without medium of exchange',
    'prediction_market': 'Agents bet on outcomes, market price reflects collective belief',
}

class AuctionHouse:
    """Run agent auctions for resource allocation."""
    def __init__(self, auction_type: str = 'english'):
        self.type = auction_type
        self.bids = {}
    
    def run_english_auction(self, reserve_price: float, 
                            bid_increment: float = 10.0) -> Dict:
        """Ascending price auction, highest bidder wins."""
        current_price = reserve_price
        winner = None
        while True:
            bids_at_price = {
                a: b for a, b in self.bids.items() if b >= current_price
            }
            if not bids_at_price:
                break
            winner = max(bids_at_price, key=bids_at_price.get)
            current_price += bid_increment
        
        return {
            'type': 'english_auction',
            'winner': winner,
            'price': current_price - bid_increment,
        }
```

## Common Pitfalls

1. **No concept of value** — agents need utility functions to make economic decisions
2. **Market manipulation** — agents can collude or manipulate prices; design against it
3. **Wealth inequality** — some agents accumulate disproportionate resources; redistribution mechanisms
4. **No bankruptcy handling** — agents run out of tokens; need credit or basic income
5. **Overhead** — running markets has communication cost; balance with direct allocation

## Verification Checklist

- [ ] Resource scarcity justifies market mechanism
- [ ] Agent utility functions defined (what they value, by how much)
- [ ] Market mechanism chosen (price, auction, token, barter)
- [ ] Anti-manipulation safeguards (proxy bidding, privacy, limits)
- [ ] Bankruptcy/redistribution mechanisms defined
- [ ] Market clearing frequency defined (continuous, periodic)
- [ ] Economic efficiency measured (allocative efficiency, welfare)
- [ ] Market overhead (communication, computation) within budget
