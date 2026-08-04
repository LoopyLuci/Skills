---
name: energy-storage-economics
description: "Use when analyzing energy storage. Battery, ROI, economics."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [climatetech, energy-storage, battery, roi, economics, lcoe]
    related_skills: [renewable-energy-design, energy-storage-systems]
---

# Energy Storage Economics

## Overview
Analyze the techno-economic viability of energy storage systems including lithium-ion, flow batteries, compressed air, pumped hydro, and emerging technologies. Covers LCOE calculation for storage, revenue stacking, grid services monetization, degradation modeling, and investment decision frameworks.

## When to Use
- "Calculate LCOE for energy storage system"
- "Evaluate battery storage revenue stacking opportunities"
- "Model battery degradation over time"
- "Size storage for grid services revenue"
- "Compare storage technologies economically"

## Storage Technology Comparison

### Battery Technologies
| Technology | Lifespan (years) | Cycle Life | Round-trip Efficiency | CapEx ($/kWh) | Use Cases |
|------------|------------------|------------|----------------------|---------------|-----------|
| Lithium-ion (NMC) | 10-15 | 3000-5000 | 85-90% | 250-400 | Residential, C&I, grid |
| Lithium-ion (LFP) | 15-20 | 6000-8000 | 85-90% | 300-500 | Utility, long-duration |
| Sodium-ion | 10-15 | 4000-6000 | 80-85% | 200-300 | Emerging, stationary |
| Flow (Vanadium) | 20+ | 10000+ | 70-75% | 500-800 | Long-duration grid |
| Compressed Air | 15-20 | 20000+ | 50-60% | 200-400 | Grid-scale, long duration |
| Pumped Hydro | 30-50 | 30000+ | 70-85% | 100-200 | Grid-scale, long duration |

## Economic Analysis Framework

### LCOE for Storage (LCOS)
```python
def calculate_lcos(capital_cost_per_kwh, fixed_om_annual_pct, variable_cost_per_kwh_cycle,
                   cycles_per_year, efficiency_loss_pct, lifetime_years, discount_rate):
    """
    Calculate Levelized Cost of Storage ($/kWh stored)
    
    Args:
        capital_cost_per_kwh: $/kWh of storage capacity
        fixed_om_annual_pct: % of capital cost per year for O&M
        variable_cost_per_kwh_cycle: $/kWh throughput (cycles)
        cycles_per_year: number of full cycles per year
        efficiency_loss_pct: round-trip efficiency loss (e.g., 0.10 for 10%)
        lifetime_years: useful life
        discount_rate: discount rate for NPV
    
    Returns:
        LCOS in $/kWh stored
    
    Example:
    >>> calculate_lcos(300, 0.02, 0.01, 200, 0.15, 15, 0.08)
    """
    # Annual capital recovery
    annual_capital = capital_cost_per_kwh * (
        discount_rate * (1 + discount_rate)**lifetime_years /
        ((1 + discount_rate)**lifetime_years - 1)
    )
    
    # Annual fixed O&M
    annual_fixed_om = capital_cost_per_kwh * fixed_om_annual_pct
    
    # Annual variable cost per kWh stored
    annual_variable = variable_cost_per_kwh_cycle * cycles_per_year
    
    # Efficiency loss cost
    efficiency_cost = capital_cost_per_kwh * efficiency_loss_pct * discount_rate
    
    # Total annualized cost per kWh of capacity
    annualized_cost_per_kwh = (
        annual_capital + annual_fixed_om + annual_variable + efficiency_cost
    )
    
    # LCOS per kWh stored/cycled
    lcos = annualized_cost_per_kwh / cycles_per_year
    
    return {
        "lcos_usd_per_kwh": round(lcos, 3),
        "annual_capital_recovery": round(annual_capital, 2),
        "annual_fixed_om": round(annual_fixed_om, 2),
        "annual_variable_cost": round(annual_variable, 2),
        "efficiency_cost": round(efficiency_cost, 2),
        "capacity_factor_utilization": round(cycles_per_year / 365, 2)
    }

# Example calculation for utility-scale lithium-ion
example_lcos = calculate_lcos(
    capitall_cost_per_kwh=350,      # $350/kWh for LFP batteries
    fixed_om_annual_pct=0.02,       # 2% of capital annually
    variable_cost_per_kwh_cycle=0.005,  # $0.005/kWh/cycle
    cycles_per_year=300,            # Conservative for daily cycling
    efficiency_loss_pct=0.15,       # 15% AC-to-DC round-trip losses
    lifetime_years=15,
    discount_rate=0.08
)
# Expected LCOS: ~$0.15-0.25/kWh stored
```

## Revenue Stacking & Grid Services

### Revenue Streams for Grid-Scale Storage
| Service | Revenue ($/kW-year) | Duration | Frequency |
|---------|-------------------|----------|-----------|
| Frequency Regulation (FCR) | $50-100 | 10-30 min | Hourly |
| Peak Shaving | $100-300 | 4-6 hours | Daily |
| Time-of-Use Arbitrage | $50-200 | 4-12 hours | Daily |
| Voltage Support (VAr) | $20-50 | Continuous | Continuous |
| Black Start | $800-1,500 | Event-based | Rare |
| Transmission & Distribution Deferral | $200-500 | 10-20 years | Long-term |

### Revenue Optimization Model
```python
def revenue_stack_analysis(storage_kw, storage_kwh, market_data):
    """
    Calculate total revenue potential from stacking services
    """
    revenues = {}
    
    # 1. Frequency Regulation (highest value, fast response)
    regulation_revenue = (
        storage_kw * market_data['regulation_price_per_kw_year'] * 
        storage_kwh / (storage_kw * 0.25)  # Typically 15-minute duration
    )
    revenues['regulation'] = min(regulation_revenue, storage_kw * 80)
    
    # 2. Peak Shaving (energy arbitrage)
    peak_shaving_revenue = (
        storage_kwh * market_data['peak_demand_charge_savings']
    )
    revenues['peak_shaving'] = min(peak_shaving_revenue, storage_kwh * 350)
    
    # 3. Energy Arbitrage
    arbitrage_revenue = (
        storage_kwh * market_data['daily_price_spread'] * 
        market_data['arbitrage_efficiency']
    )
    revenues['energy_arbitrage'] = min(arbitrage_revenue, storage_kwh * 365)
    
    # 4. Transmission Deferral Value
    tdr_revenue = (
        storage_kw * market_data['tdr_value_per_kw_year']
    )
    revenues['tdr'] = tdr_revenue
    
    total_revenue = sum(revenues.values())
    lcos = calculate_lcos(**market_data['cost_parameters'])
    
    return {
        "total_annual_revenue": round(total_revenue, 2),
        "revenue_breakdown": {k: round(v/max(revenues.values())*100, 1) 
                             for k, v in revenues.items()},
        "profitability": total_revenue > lcos['lcos_usd_per_kwh'] * storage_kwh,
        "payback_period_years": round(
            (market_data['capex_total']) / total_revenue, 1
        )
    }
```

## Battery Degradation Modeling

### Calendar and Cycle Aging
```python
def battery_degradation_model(initial_capacity, cycles, years, operating_temp):
    """
    Model lithium-ion battery degradation over time
    
    Sources:
    - Cycle aging (use-dependent)
    - Calendar aging (time-dependent, temp-dependent)
    """
    # Cycle aging coefficient (cycles per 1% capacity loss)
    cycle_endurance = 2000  # Cycles to 80% capacity (typical LFP)
    cycle_degradation = cycles / (cycle_endurance / 0.20)  # 20% degradation at EOL
    
    # Calendar aging (Arrhenius model)
    # Accelerated at high temperature
    calendar_aging_rate = 0.02  # 2%/year at 25°C
    temp_factor = np.exp((operating_temp - 25) * 0.05)  # 5% per °C
    calendar_degradation = calendar_aging_rate * years * temp_factor
    
    total_degradation = cycle_degradation + calendar_degradation
    remaining_capacity = initial_capacity * (1 - min(total_degradation, 0.8))
    
    return {
        "cycle_degradation_pct": round(cycle_degradation * 100, 2),
        "calendar_degradation_pct": round(calendar_degradation * 100, 2),
        "total_degradation_pct": round(total_degradation * 100, 2),
        "remaining_capacity_kwh": round(remaining_capacity, 2),
        "replacement_needed": total_degradation > 0.8
    }
```

## Common Pitfalls
1. **Overestimating cycle life** — real-world degrades faster than lab specs
2. **Not accounting for calendar aging** — battery degrades even idle
3. **Ignoring temperature effects** — degradation accelerates above 35°C
4. **Wrong revenue stacking** — services compete for same time periods
5. **Underestimating fixed O&M costs** — monitoring, replacement labor
6. **Not considering depth of discharge** — shallow cycling vs deep cycling
7. **Wrong degradation model** — oversimplified linear or only cycle-based
8. **Ignoring end-of-life replacement costs** — battery replacement every 10-15 years
9. **Overestimating available power** — batteries lose peak power as they age
10. **Not accounting for state of charge effects** — high SoC accelerates degradation

## Verification Checklist
- [ ] LCOS calculated using consistent discount rate
- [ ] Degradation model includes both calendar and cycle aging
- [ ] Revenue stacks are non-competing (can provide simultaneously)
- [ ] Temperature effects on degradation modeled
- [ ] Replacement costs included for lifetime analysis
- [ ] Market price forecasts based on 5+ year historical data
- [ ] System performance validated with manufacturer data
- [ ] Regulatory and interconnection costs factored in
- [ ] Sensitivity analysis performed on key variables (±20%)
- [ ] Payback period < lifetime of asset