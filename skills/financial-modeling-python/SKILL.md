---
name: financial-modeling-python
description: "Use when building financial models. Python, DCF, valuation."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [finance, financial-modeling, python, valuation, dcf]
    related_skills: [banking-api-integration, algorithmic-trading-strategies]
---

# Financial Modeling with Python

## Overview
Build robust financial models using Python libraries (pandas, numpy, scipy) for valuation, cash flow analysis, risk assessment, and investment decision-making. Covers DCF modeling, M&A analysis, portfolio optimization, and scenario analysis with institutional-grade accuracy.

## When to Use
- "Value startup or public company"
- "Build discounted cash flow model"
- "Analyze M&A transaction"
- "Optimize investment portfolio"
- "Run Monte Carlo scenario analysis"

## Core Libraries
```python
import pandas as pd
import numpy as np
from scipy import stats
import yfinance as yf
from datetime import datetime, timedelta

# Example: DCF valuation model
def dcf_valuation(free_cash_flows, terminal_growth_rate, discount_rate):
    """
    Discounted Cash Flow valuation
    
    Args:
        free_cash_flows: list of projected FCFs (years 1-5)
        terminal_growth_rate: perpetual growth rate (e.g., 0.02 for 2%)
        discount_rate: WACC or required rate of return
    
    Returns:
        Total enterprise value
    """
    # Present value of projected cash flows
    pv_cash_flows = sum([
        fcf / ((1 + discount_rate) ** (i + 1))
        for i, fcf in enumerate(free_cash_flows)
    ])
    
    # Terminal value (perpetuity growth model)
    final_fcf = free_cash_flows[-1]
    terminal_value = (final_fcf * (1 + terminal_growth_rate)) / (
        discount_rate - terminal_growth_rate
    )
    pv_terminal_value = terminal_value / ((1 + discount_rate) ** len(free_cash_flows))
    
    return {
        "pv_cash_flows": round(pv_cash_flows, 2),
        "pv_terminal_value": round(pv_terminal_value, 2),
        "enterprise_value": round(pv_cash_flows + pv_terminal_value, 2)
    }

# Example: Portfolio optimization (efficient frontier)
def portfolio_optimization(returns_df, num_portfolios=10000):
    """
    Calculate efficient frontier with Monte Carlo simulation
    
    Args:
        returns_df: DataFrame with asset returns
        num_portfolios: number of portfolios to simulate
    
    Returns:
        Optimal portfolio weights (maximum Sharpe ratio)
    """
    returns = returns_df.pct_change().dropna()
    mean_returns = returns.mean() * 252  # Annualized
    cov_matrix = returns.cov() * 252      # Annualized
    
    results = np.zeros((3, num_portfolios))
    
    for i in range(num_portfolios):
        weights = np.random.random(len(returns.columns))
        weights /= np.sum(weights)
        
        portfolio_return = np.sum(mean_returns * weights)
        portfolio_volatility = np.sqrt(
            np.dot(weights.T, np.dot(cov_matrix, weights))
        )
        
        results[0, i] = portfolio_return
        results[1, i] = portfolio_volatility
        results[2, i] = portfolio_return / portfolio_volatility  # Sharpe
    
    # Select portfolio with highest Sharpe ratio
    best_idx = np.argmax(results[2])
    best_weights = weights  # From last iteration — should store properly
    
    return {
        "expected_return": results[0, best_idx],
        "volatility": results[1, best_idx],
        "sharpe_ratio": results[2, best_idx],
        "weights": dict(zip(returns.columns, best_weights))
    }
```

## Financial Ratios & Analysis
| Category | Ratio | Formula | Target |
|----------|-------|---------|--------|
| Profitability | ROE | Net Income / Shareholder Equity | >15% |
| Profitability | ROIC | NOPAT / Invested Capital | >10% |
| Liquidity | Current Ratio | Current Assets / Current Liabilities | 1.5-3 |
| Leverage | Debt/Equity | Total Debt / Shareholder Equity | <0.5 ideal |
| Efficiency | Asset Turnover | Revenue / Total Assets | Industry benchmark |
| Valuation | P/E | Market Price / EPS | Compare to peers |

## Monte Carlo Simulation for Risk Analysis
```python
def monte_carlo_simulation(initial_value, mean_return, std_dev, periods, simulations):
    """
    Run Monte Carlo price simulation
    
    Args:
        initial_value: starting price
        mean_return: expected annual return
        std_dev: annual volatility
        periods: number of years
        simulations: number of simulation runs
    
    Returns:
        Terminal values for each simulation
    """
    dt = 1 / 252  # Daily steps
    results = []
    
    for _ in range(simulations):
        prices = [initial_value]
        for _ in range(periods * 252):
            # Geometric Brownian Motion
            drift = (mean_return - 0.5 * std_dev ** 2) * dt
            shock = std_dev * np.sqrt(dt) * np.random.normal(0, 1)
            new_price = prices[-1] * np.exp(drift + shock)
            prices.append(new_price)
        results.append(prices[-1])
    
    return {
        "mean_terminal_value": np.mean(results),
        "median_terminal_value": np.median(results),
        "percentile_5": np.percentile(results, 5),
        "percentile_95": np.percentile(results, 95),
        "probability_of_loss": len([r for r in results if r < initial_value]) / len(results)
    }
```

## M&A Analysis Models

### Comparable Company Analysis
```python
def comparable_company_analysis(company_metrics, peer_group_metrics):
    """
    Valuation multiples comparison
    """
    valuation_multiples = {
        'EV/Revenue': company_metrics['ev'] / company_metrics['revenue'],
        'EV/EBITDA': company_metrics['ev'] / company_metrics['ebitda'],
        'P/E': company_metrics['market_cap'] / company_metrics['net_income'],
        'P/B': company_metrics['market_cap'] / company_metrics['book_value']
    }
    
    peer_multiples = {metric: [] for metric in valuation_multiples.keys()}
    
    for peer in peer_group_metrics:
        peer_multiples['EV/Revenue'].append(peer['ev'] / peer['revenue'])
        peer_multiples['EV/EBITDA'].append(peer['ev'] / peer['ebitda'])
    
    implied_valuations = {}
    for metric, multiple in valuation_multiples.items():
        peer_multiple_range = {
            "min": min(peer_multiples[metric]),
            "median": np.median(peer_multiples[metric]),
            "mean": np.mean(peer_multiples[metric]),
            "max": max(peer_multiples[metric])
        }
        implied_valuations[metric] = {
            "current_multiple": multiple,
            "peer_median": peer_multiple_range["median"],
            "implied_value_at_median": peer_multiple_range["median"] * 
                company_metrics[metric.split('/')[1].strip().lower()]
        }
    
    return implied_valuations
```

## Common Pitfalls
1. **Overly optimistic projections** — extend growth period too far into future
2. **Wrong discount rate** — using generic WACC instead of project-specific cost of capital
3. **Ignoring cyclicality** — models fail during market downturns
4. **Not sensitivity analysis** — single-point estimates hide risk
5. **Terminal value dominates** — 70-80% of DCF value from terminal value = unstable
6. **Missing non-operating assets** — excess cash, investments not included
7. **Incorrect free cash flow definition** — FCF ≠ net income ± non-cash items
8. **Not adjusting for off-balance sheet items** — leases, pension obligations, derivatives

## Verification Checklist
- [ ] All projections justified with supporting analysis
- [ ] Discount rate calculated from CAPM/WACC, not arbitrary
- [ ] Terminal value <50% of total enterprise value
- [ ] Sensitivity analysis completed for 3 key variables
- [ ] Debt, cash, and non-operating assets accounted for
- [ ] Scenario analysis for bull/base/bear cases
- [ ] Peer group appropriately matched for comps
- [ ] Model validated against historical results
- [ ] Monte Carlo simulation confirms probability distribution
- [ ] Output formatted for board/management presentation