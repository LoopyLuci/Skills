---
name: real-estate-market-analysis
description: "Use when analyzing real estate markets and valuations."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [real-estate, market-analysis, comps, valuation, CMA, investment]
    related_skills: [real-estate-crm-leads, crm-sales-pipeline, business-metrics-kpis, digital-marketing-strategy]
---

# Real Estate Market Analysis

Analyzing real estate markets, property valuations, comparable sales, and investment opportunities.

## When to Use

- Pricing a property for listing or offer
- Evaluating investment opportunities
- Analyzing neighborhood and market trends
- Preparing CMAs for clients
- Making data-driven real estate decisions

## Comparative Market Analysis (CMA)

```python
class CMA:
    @staticmethod
    def analyze(subject: Dict, comps: List[Dict]) -> Dict:
        if not comps: return {}
        
        prices_per_sqft = [c.get('sold_price', 0) / max(c.get('sqft', 1), 1) for c in comps]
        avg_pps = sum(prices_per_sqft) / len(prices_per_sqft)
        estimated = avg_pps * subject.get('sqft', 0)
        
        # Adjust for differences
        adjustments = 0
        for comp in comps:
            adjustments += (subject.get('beds', 0) - comp.get('beds', 0)) * 10000
            adjustments += (subject.get('baths', 0) - comp.get('baths', 0)) * 7000
        
        avg_dom = sum(c.get('days_on_market', 30) for c in comps) / len(comps)
        
        return {
            'estimated_value': round(estimated + adjustments / len(comps), 0),
            'value_range': {
                'low': round(estimated * 0.95, 0),
                'high': round(estimated * 1.05, 0),
            },
            'avg_days_on_market': round(avg_dom, 1),
            'comps_used': len(comps),
        }
```

## Market Trend Analysis

```python
def analyze_trends(data: List[Dict]) -> Dict:
    if not data: return {}
    prices = [d.get('median_price', 0) for d in sorted(data, key=lambda x: x.get('date', ''))]
    doms = [d.get('days_on_market', 30) for d in data]
    
    avg_dom = sum(doms) / len(doms)
    change = ((prices[-1] - prices[0]) / max(prices[0], 1)) * 100
    
    return {
        'current_median': prices[-1],
        'price_change_pct': round(change, 1),
        'avg_days_on_market': round(avg_dom, 1),
        'market_type': "Seller's Market" if avg_dom < 30 else "Balanced" if avg_dom < 60 else "Buyer's Market",
    }
```

## Investment Analysis

```python
def analyze_rental(value: float, down_pct: float, rate: float,
                   rent: float, expenses: float) -> Dict:
    down = value * down_pct
    loan = value - down
    monthly_rate = rate / 12
    payments = 30 * 12
    mortgage = loan * (monthly_rate * (1+monthly_rate)**payments) / ((1+monthly_rate)**payments - 1)
    
    noi = rent * 12 - expenses * 12
    cash_flow = noi - mortgage * 12
    
    return {
        'down_payment': round(down, 0),
        'monthly_mortgage': round(mortgage, 2),
        'annual_cash_flow': round(cash_flow, 2),
        'cap_rate': round(noi / value * 100, 2),
        'cash_on_cash': round(cash_flow / down * 100, 2),
    }
```

## Common Pitfalls

1. **Outdated comps** — use only last 3-6 months
2. **No adjustments** — every property differs; adjust for beds, baths, condition
3. **Too few comps** — need 5+ for reliable analysis
4. **Over-relying on AVMs** — Zestimates are starting points, not definitive

## Verification Checklist

- [ ] 5+ comps from last 6 months
- [ ] Adjustments calculated for differences
- [ ] Market type identified
- [ ] Investment metrics (cap rate, cash-on-cash)

## See Also

- real-estate-crm-leads — managing property leads
- crm-sales-pipeline — tracking deals to close
- business-metrics-kpis — real estate business metrics
