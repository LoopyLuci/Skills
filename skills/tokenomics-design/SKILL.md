---
name: tokenomics-design
description: "Use when designing token economics and incentive systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [tokenomics, token-economics, incentives, DeFi, governance, staking, DAO]
    related_skills: [blockchain-development-solidity, defi-smart-contracts, zero-knowledge-proofs, agent-economics-markets]
---

# Tokenomics Design

Designing token economics — from token types and distribution through incentive mechanisms, governance, staking, and sustainable economic models.

## When to Use

- Designing token models for web3 projects
- Building incentive systems (staking, rewards, fees)
- DAO governance token design
- Game economy design with tokens
- Balancing supply, demand, and utility

## Tokenomics Framework

```python
TOKENOMICS_ELEMENTS = {
    'token_type': 'Utility (gas, access), Governance (voting), Security (investment), Stablecoin (pegged)',
    'supply': 'Fixed (Bitcoin), Inflationary (Ethereum), Elastic (Ampleforth), Burn mechanism',
    'distribution': 'Public sale, private sale, airdrop, liquidity mining, team/advisor vesting',
    'incentives': 'Staking rewards, yield farming, LP incentives, fee sharing',
    'governance': 'On-chain voting, delegation, quorum, timelock, veto power',
}

class TokenModel:
    """Design token economic model."""
    def __init__(self, name: str, total_supply: int):
        self.name = name
        self.total_supply = total_supply
        self.allocations = {}
    
    def allocate(self, category: str, percentage: float, 
                 vesting_months: int = 0, cliff_months: int = 0):
        self.allocations[category] = {
            'pct': percentage, 'tokens': int(self.total_supply * percentage),
            'vesting': vesting_months, 'cliff': cliff_months,
        }
    
    def circulating_supply(self, month: int) -> int:
        """Calculate circulating supply at given month since TGE."""
        circulating = 0
        for alloc in self.allocations.values():
            if month >= alloc['cliff']:
                vested_months = min(month - alloc['cliff'], alloc['vesting'])
                if alloc['vesting'] > 0:
                    circulating += alloc['tokens'] * vested_months // alloc['vesting']
                else:
                    circulating += alloc['tokens']
        return circulating
```

## Verification Checklist

- [ ] Token type defined (utility, governance, security, stablecoin)
- [ ] Supply schedule (fixed, inflationary, elastic) with rationale
- [ ] Distribution allocations with vesting schedules
- [ ] Incentive mechanisms (staking, rewards, fee sharing)
- [ ] Governance model (voting, delegation, quorum)
- [ ] Treasury management strategy
- [ ] Sustainability analysis (inflation vs. utility demand)
- [ ] Regulatory compliance (securities law)
