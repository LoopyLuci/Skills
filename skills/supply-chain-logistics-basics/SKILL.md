---
name: supply-chain-logistics-basics
description: "Use when managing supply chain and logistics operations."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [supply-chain, logistics, inventory, warehouse, procurement, shipping]
    related_skills: [vendor-management-procurement, ecommerce-platform-management, retail-pos-systems, business-continuity-planning]
---

# Supply Chain and Logistics Basics

Managing supply chain and logistics operations — from procurement and inventory management through warehouse operations, shipping, and supply chain risk.

## When to Use

- Setting up supply chain for a physical product business
- Managing inventory across multiple locations
- Optimizing shipping and fulfillment operations
- Assessing and mitigating supply chain risks
- Building supplier relationships

## Supply Chain Functions

```python
SC_FUNCTIONS = {
    'procurement': 'Sourcing, supplier selection, purchase orders, vendor management',
    'inventory': 'Stock levels, reorder points, ABC analysis, cycle counting',
    'warehousing': 'Receiving, put-away, picking, packing, shipping',
    'transportation': 'Carrier selection, routing, freight audit, last-mile delivery',
}

def abc_analysis(items: List[Dict]) -> Dict:
    """Classify inventory by value (A=80%, B=15%, C=5%)."""
    sorted_items = sorted(items, key=lambda x: x['annual_value'], reverse=True)
    total = sum(i['annual_value'] for i in sorted_items)
    
    a_items, b_items, c_items = [], [], []
    cumulative = 0
    for item in sorted_items:
        cumulative += item['annual_value'] / total
        if cumulative <= 0.80: a_items.append(item)
        elif cumulative <= 0.95: b_items.append(item)
        else: c_items.append(item)
    
    return {'A': a_items, 'B': b_items, 'C': c_items}
```

## Verification Checklist

- [ ] Key suppliers identified and contracts in place
- [ ] Inventory categorized by ABC analysis
- [ ] Reorder points calculated for key items
- [ ] Shipping carriers evaluated and selected
- [ ] Warehouse layout optimized for picking efficiency
- [ ] Supply chain risks identified and mitigation plans
- [ ] Inventory accuracy measured (cycle count results)
- [ ] Backup suppliers for critical components
