---
name: agent-negotiation-strategies
description: "Use when implementing agent negotiation and bargaining."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [negotiation, bargaining, auctions, game-theory, multi-agent, agreement]
    related_skills: [agent-communication-languages, multi-agent-collaboration-patterns, agent-economics-markets, agent-reasoning-patterns]
---

# Agent Negotiation Strategies

Implementing agent negotiation strategies — from bargaining and auctions through game-theoretic negotiation, multi-issue negotiation, and argumentation.

## When to Use

- Agents need to reach agreements on resource allocation
- Implementing auction systems for task distribution
- Multi-issue negotiation between autonomous agents
- Building competitive negotiation agents
- Applying game theory to agent interactions

## Negotiation Protocols

```python
NEGOTIATION_PROTOCOLS = {
    'bargaining': 'Alternating offers between two agents until agreement',
    'english_auction': 'Ascending price, last bidder wins',
    'dutch_auction': 'Descending price, first bidder wins',
    'vickrey': 'Sealed bid, second-highest price wins',
    'contract_net': 'Manager broadcasts task, contractors bid, manager awards',
    'monotonic_concession': 'Agents concede gradually toward agreement',
}

class Negotiator:
    """Agent negotiation with concession strategies."""
    def __init__(self, reservation_price: float, 
                 concession_rate: float = 0.1):
        self.reservation = reservation_price  # walk-away point
        self.concession = concession_rate
        self.round = 0
    
    def propose(self, opponent_offer: float = None) -> float:
        self.round += 1
        if opponent_offer:
            # Concede toward opponent
            concession_amount = abs(opponent_offer - self.initial_offer) * self.concession
            return max(self.reservation, self.initial_offer - concession_amount * self.round)
        return self.initial_offer
    
    def accept(self, offer: float) -> bool:
        return offer >= self.reservation
```

## Common Pitfalls

1. **Irrational opponents** — real agents aren't perfectly rational; model bounded rationality
2. **Information asymmetry** — one agent knows more than another; design for incomplete info
3. **Lying and deception** — agents may misrepresent their preferences; build trust mechanisms
4. **Time pressure** — negotiations must terminate; implement deadlines
5. **Multi-issue complexity** — combining issues (price + timing + quality) needs sophisticated strategies

## Verification Checklist

- [ ] Negotiation protocol chosen and documented
- [ ] Reservation/walk-away point defined
- [ ] Concession strategy designed (linear, exponential, time-based)
- [ ] Deal acceptance criteria defined
- [ ] Negotiation timeout mechanism
- [ ] Reputation tracking for repeated negotiations
- [ ] Fallback plan for negotiation failure
