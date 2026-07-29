---
name: retail-pos-systems
description: "Use when managing retail operations and POS systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [retail, POS, point-of-sale, inventory, store-management, omnichannel]
    related_skills: [ecommerce-platform-management, business-metrics-kpis, crm-sales-pipeline, inventory-management]
---

# Retail and Point-of-Sale Systems

Managing retail store operations, point-of-sale systems, inventory, omnichannel fulfillment, and retail analytics.

## When to Use

- Setting up a retail store POS system
- Managing multi-location retail inventory
- Implementing omnichannel (online + in-store) operations
- Training staff on POS workflows
- Analyzing retail performance metrics

## POS System Comparison

```python
POS_SYSTEMS = {
    'square': {
        'best_for': 'Small business, pop-ups, food trucks, mobile',
        'hardware_cost': '$0-300',
        'software_cost': '$0-60/mo',
        'processing': '2.6% + $0.10',
        'features': ['iPad POS', 'Inventory', 'Employee mgmt', 'eCommerce integration'],
    },
    'shopify_pos': {
        'best_for': 'Existing Shopify stores, omnichannel retail',
        'hardware_cost': '$0-300',
        'software_cost': '$89/mo (included in Shopify)',
        'processing': '2.4% + $0.30 (Shopify Payments)',
        'features': ['Native Shopify sync', 'Unified inventory', 'Buy online pickup in-store', 'POS Go mobile'],
    },
    'lightspeed': {
        'best_for': 'Mid-market, apparel, restaurants, golf',
        'hardware_cost': '$0-500',
        'software_cost': '$89-269/mo',
        'processing': '2.4% + $0.15',
        'features': ['Advanced inventory', 'CRM built-in', 'Reporting', 'Multi-location'],
    },
    'clover': {
        'best_for': 'Restaurants, full-service retail',
        'hardware_cost': '$100-1500',
        'software_cost': '$14.95-134.95/mo',
        'processing': 'Variable (depends on processor)',
        'features': ['All-in-one hardware', 'Payment processing', 'Employee management', 'Order ahead'],
    },
    'vend_by_lightspeed': {
        'best_for': 'Independent retailers, multi-store',
        'hardware_cost': '$0-500',
        'software_cost': '$119-229/mo',
        'processing': '2.4% + $0.15',
        'features': ['Inventory mgmt', 'CRM', 'Customer loyalty', 'Purchase orders'],
    },
}

def recommend_pos(business_type: str, has_ecommerce: bool, budget: str) -> str:
    if business_type in ('restaurant', 'cafe', 'food'):
        return 'Clover'
    if has_ecommerce:
        return 'Shopify POS'
    if budget == 'low':
        return 'Square'
    return 'Lightspeed'
```

## Inventory Management

```python
from typing import Dict, List
from datetime import datetime, timedelta
import json

class RetailInventory:
    """Manage multi-location retail inventory."""
    
    def __init__(self):
        self.products = {}
        self.locations = {}
        self.transfers = []
    
    def add_location(self, name: str, address: str, 
                     is_warehouse: bool = False) -> str:
        import uuid
        lid = str(uuid.uuid4())[:8]
        self.locations[lid] = {
            'id': lid, 'name': name, 'address': address,
            'type': 'warehouse' if is_warehouse else 'store',
            'created': datetime.now().isoformat(),
        }
        return lid
    
    def add_product(self, sku: str, name: str, cost: float, 
                    price: float, category: str = '') -> str:
        import uuid
        pid = str(uuid.uuid4())[:8]
        self.products[pid] = {
            'id': pid, 'sku': sku, 'name': name,
            'cost': cost, 'price': price, 'margin': round((price-cost)/price*100, 1),
            'category': category, 'location_stock': {},
        }
        return pid
    
    def receive_stock(self, product_id: str, location_id: str, qty: int):
        if product_id in self.products:
            loc = self.products[product_id]['location_stock']
            loc[location_id] = loc.get(location_id, 0) + qty
    
    def transfer_stock(self, product_id: str, from_loc: str, 
                       to_loc: str, qty: int):
        stock = self.products[product_id]['location_stock']
        if stock.get(from_loc, 0) >= qty:
            stock[from_loc] = stock.get(from_loc, 0) - qty
            stock[to_loc] = stock.get(to_loc, 0) + qty
            self.transfers.append({
                'product_id': product_id, 'from': from_loc,
                'to': to_loc, 'qty': qty,
                'date': datetime.now().isoformat(),
            })
            return True
        return False
    
    def get_low_stock_alerts(self, threshold: int = 5) -> List[Dict]:
        alerts = []
        for pid, prod in self.products.items():
            total = sum(prod['location_stock'].values())
            if 0 < total <= threshold:
                alerts.append({
                    'sku': prod['sku'], 'name': prod['name'],
                    'total_stock': total, 'locations': prod['location_stock'],
                })
            elif total == 0:
                alerts.append({
                    'sku': prod['sku'], 'name': prod['name'],
                    'total_stock': 0, 'status': 'OUT_OF_STOCK',
                })
        return alerts
```

## Retail KPIs

```python
RETAIL_KPIS = {
    'same_store_sales': 'YoY sales growth for stores open >12 months',
    'sales_per_sqft': 'Revenue / total square footage',
    'inventory_turnover': 'COGS / average inventory value',
    'sell_through_rate': 'Units sold / units received (%)',
    'shrinkage': 'Inventory loss from theft/error (% of sales)',
    'conversion_rate': 'Transactions / foot traffic (%)',
    'avg_transaction_value': 'Total revenue / number of transactions',
    'foot_traffic': 'Number of people entering the store',
    'capture_rate': 'Customers who pass by vs enter (%)',
    'employee_utilization': 'Productive hours / paid hours (%)',
    'omni_channel_rate': 'Online orders fulfilled by store (%)',
}

def report_retail_performance(data: Dict) -> str:
    report = "🏪 Retail Performance Report\n" + "=" * 40 + "\n"
    report += f"Same-Store Sales Growth: {data.get('same_store_sales', 'N/A')}%\n"
    report += f"Sales/sqft: ${data.get('sales_per_sqft', 0):.2f}\n"
    report += f"Conversion Rate: {data.get('conversion_rate', 0):.1f}%\n"
    report += f"Avg Transaction: ${data.get('avg_transaction_value', 0):.2f}\n"
    report += f"Shrinkage: {data.get('shrinkage', 0):.1f}%\n"
    return report
```

## Common Pitfalls

1. **Online vs in-store inventory not synced** — selling something in-store that's already sold online
2. **Not auditing cycle counts** — system inventory drifts from physical; cycle count weekly
3. **Wrong POS for business type** — restaurant POS won't work for apparel; choose specialized
4. **Ignoring omnichannel customers** — customers expect buy-online-pick-up-in-store; enable it
5. **No staff training on POS** — slow checkout frustrates customers; train thoroughly
6. **Processing fee surprises** — POS processing fees add up; negotiate or compare rates

## Verification Checklist

- [ ] POS system selected for business type
- [ ] Hardware ordered and configured
- [ ] Products loaded into POS (SKU, price, barcode)
- [ ] Inventory synced across locations
- [ ] Payment processing configured and tested
- [ ] Employee/PIN setup for staff
- [ ] Omnichannel features enabled (BOPIS, ship-from-store)
- [ ] Reporting dashboard configured
- [ ] Backup procedures for POS downtime

## See Also

- ecommerce-platform-management — online store integration
- business-metrics-kpis — retail KPIs
- crm-sales-pipeline — customer data integration
- inventory-management — deeper inventory patterns
