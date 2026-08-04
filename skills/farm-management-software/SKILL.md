---
name: farm-management-software
description: "Use when planning farm management. Software, workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [farm-management, agtech, agronomy, operations]
    related_skills: [precision-agriculture, crop-yield-modeling]
---

# Farm Management Software

## Overview
Plan and implement farm management software covering field mapping, crop planning, input optimization, labor scheduling, equipment tracking, financial tracking, and regulatory compliance. Integrates agronomy, economics, and operations into a unified platform with mobile and offline capabilities.

## When to Use
- "Plan farm operations for growing season"
- "Design farm management software architecture"
- "Optimize fertilizer/pesticide input usage"
- "Schedule farm labor and equipment"
- "Track farm financials and profitability"

## Data Model
```json
{
  "fields": [{"id": "F001", "name": "North 40", "area_ha": 40.5, 
              "soil_type": "Silt Loam", "zone_id": "Z1"}],
  "zones": [{"zone_id": "Z1", "tillage": "no-till", "rotation": "legume"}],
  "operations": {"planting": {"date": "2024-05-01", "crop": "corn"}}
}
```

## Operations Planning
```python
class FarmOpsPlanner:
    def __init__(self, farm_data):
        self.farm = farm_data
    
    def generate_season_plan(self, crop_type, start_date):
        plan = []
        # Seed ordering, soil testing, planting, scouting, harvest
        growth_stages = self.get_growth_stages(crop_type)
        for stage, days_after in growth_stages.items():
            plan.append({"activity": stage, "date": start_date + timedelta(days=days_after)})
        return plan
```

## Input Optimization
```python
def vra_fertilizer(zone_data, soil_test):
    # Variable rate nitrogen based on soil nitrate and organic matter
    n_recommendation = zone_data['target_yield'] * 1.2 - soil_test['soil_n']
    return {
        'pre_plant': round(n_recommendation * 0.3),
        'at_plant': round(n_recommendation * 0.5),
        'side_dress': round(n_recommendation * 0.2)
    }
```

## Financial Tracking
```python
def field_profitability(ops, costs, market_price):
    total_cost = costs['seed'] + costs['fertilizer'] + costs['chemicals'] + costs['fuel']
    revenue = ops['yield'] * market_price
    return {
        'cost': round(total_cost, 2),
        'revenue': round(revenue, 2),
        'profit': round(revenue - total_cost, 2),
        'roi_percent': round((revenue - total_cost) / total_cost * 100, 1)
    }
```

## Compliance Tracking
- Pesticide application (EPA Form 3540-1)
- Nutrient management plans
- Worker safety (OSHA)
- Organic certification (if applicable)

## Common Pitfalls
1. Insufficient historical data integration
2. Not mobile-friendly for field operations
3. Ignoring connectivity gaps (offline modes needed)
4. Over-complex interface — farmers need simplicity
5. Poor equipment integration (ISOBUS compatibility)
6. No agronomist collaboration for validation
7. Ignoring financial impact clarity
8. Not handling field variability zones
9. Data lock-in without export capability

## Verification Checklist
- [ ] Field boundaries geo-referenced and mapped
- [ ] Soil sampling plan completed for all zones
- [ ] Weather data integrated (station or API)
- [ ] Planting/harvest equipment calibrated
- [ ] Input prescriptions generated per zone
- [ ] Labor/equipment scheduling optimized
- [ ] Financial tracking linked to operations
- [ ] Compliance checklist integrated
- [ ] Mobile interface tested offline
- [ ] Backup and recovery procedures established