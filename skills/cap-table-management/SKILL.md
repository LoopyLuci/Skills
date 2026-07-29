---
name: cap-table-management
description: "Use when managing cap tables and equity structures."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cap-table, equity, stock, options, dilution, valuation, fundraising]
    related_skills: [fundraising-investor-pitch, financial-modeling-budgeting, board-presentation-deck, equity-compensation-basics]
---

# Cap Table Management

Managing capitalization tables and equity structures — from equity types and issuance through dilution modeling, option pools, and investor reporting.

## When to Use

- Managing startup cap table and equity ownership
- Modeling dilution for fundraising rounds
- Granting employee stock options
- Preparing for exits (acquisition or IPO)
- Reporting equity to investors and board

## Equity Types

```python
EQUITY_TYPES = {
    'common_stock': 'Standard equity (founders, employees via exercise)',
    'preferred_stock': 'Investor equity with liquidation preference',
    'options': 'Right to purchase common stock at strike price',
    'rsu': 'Restricted Stock Units — shares granted, vest over time',
    'warrants': 'Right to purchase shares at fixed price (investors, partners)',
    'convertible_note': 'Debt that converts to equity at next round',
    'safe': 'Simple Agreement for Future Equity (YC standard)',
}

class CapTable:
    """Maintain cap table and model dilution."""
    def __init__(self):
        self.shareholders = {}  # name -> {shares, type, price}
        self.total_shares = 0
        self.option_pool = 0
    
    def add_shareholder(self, name: str, shares: int, 
                        equity_type: str, price: float = 0):
        self.shareholders[name] = {
            'shares': shares, 'type': equity_type, 'price': price
        }
        self.total_shares += shares
    
    def dilution_model(self, new_investment: float, 
                       pre_money: float) -> Dict:
        """Model dilution from a new funding round."""
        pre_shares = self.total_shares
        price_per_share = pre_money / pre_shares
        new_shares = new_investment / price_per_share
        post_shares = pre_shares + new_shares
        
        return {
            'pre_money': pre_money,
            'investment': new_investment,
            'new_shares': int(new_shares),
            'fully_diluted': int(post_shares),
            'dilution_pct': round(new_shares / post_shares * 100, 1),
        }
```

## Common Pitfalls

1. **No cap table system** — managing in spreadsheets after 10+ shareholders is risky
2. **Option pool too small** — can't hire without equity; maintain 10-15% pool
3. **Forgetting to model dilution** — founders surprised at how much they're diluted post-Series B
4. **No 409A valuation** — options priced below FMV create tax issues; get annual valuation
5. **Inexperienced legal counsel** — equity law is complex; hire startup-experienced lawyers

## Verification Checklist

- [ ] Cap table maintained in software (Carta, Pulley, Shareworks, or managed spreadsheet)
- [ ] All equity types tracked (common, preferred, options, warrants, SAFEs, convertibles)
- [ ] 409A valuation updated annually (for options)
- [ ] Option pool size appropriate (10-15% of fully diluted)
- [ ] Dilution modeled for next 2-3 rounds
- [ ] Vesting schedules tracked (typically 4-year with 1-year cliff)
- [ ] Shareholder reports prepared for board meetings
- [ ] Legal counsel reviews all equity grants
