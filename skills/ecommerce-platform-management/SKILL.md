---
name: ecommerce-platform-management
description: "Use when managing ecommerce platforms and online stores."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ecommerce, shopify, woocommerce, online-store, product-management, checkout]
    related_skills: [email-marketing-campaigns, conversion-rate-optimization, seo-search-engine-optimization, digital-marketing-strategy]
---

# Ecommerce Platform Management

Managing ecommerce platforms and online stores — from platform selection and product management through checkout optimization, shipping, and analytics.

## When to Use

- Setting up a new online store (Shopify, WooCommerce, BigCommerce, etc.)
- Managing products, inventory, and pricing
- Optimizing product pages and checkout flows
- Managing orders, shipping, and fulfillment
- Analyzing ecommerce metrics and performance

## Platform Comparison

```python
PLATFORMS = {
    'shopify': {
        'best_for': 'Small to medium businesses, dropshipping, quick setup',
        'pricing': '$29-299/mo + 2.9% + $0.30 transaction fees',
        'ease_of_use': 'Very easy',
        'themes': '100+ paid and free',
        'apps': '8,000+ apps in App Store',
        'strengths': 'Fast setup, hosted, great POS integration',
        'weaknesses': 'Transaction fees, limited customization without apps',
    },
    'woocommerce': {
        'best_for': 'WordPress users, full control, large catalogs',
        'pricing': 'Free plugin + hosting ($10-50/mo) + payment fees',
        'ease_of_use': 'Moderate',
        'themes': 'Thousands (WordPress ecosystem)',
        'apps': '1000+ extensions',
        'strengths': 'Full control, no transaction fees, unlimited customization',
        'weaknesses': 'Requires hosting maintenance, more technical setup',
    },
    'bigcommerce': {
        'best_for': 'Mid-market, B2B, growing businesses',
        'pricing': '$29-299/mo (no transaction fees)',
        'ease_of_use': 'Easy',
        'themes': '100+ paid and free',
        'apps': '600+ apps',
        'strengths': 'No transaction fees, built-in features, B2B tools',
        'weaknesses': 'Less app ecosystem than Shopify',
    },
}

def recommend(budget: str, catalog_size: int, technical_skill: str) -> str:
    if technical_skill == 'high' and budget == 'low':
        return 'WooCommerce'
    elif catalog_size > 1000:
        return 'BigCommerce'
    return 'Shopify'
```

## Product Management

```python
from typing import Dict, List
from datetime import datetime
import json

class ProductManager:
    """Manage products, variants, inventory, and pricing."""
    
    def __init__(self):
        self.products = {}
    
    def add_product(self, title: str, description: str, price: float,
                    cost: float, sku: str, inventory: int = 0,
                    category: str = '', tags: List[str] = None,
                    weight: float = 0, images: List[str] = None) -> str:
        import uuid
        pid = str(uuid.uuid4())[:8]
        
        self.products[pid] = {
            'id': pid, 'title': title, 'description': description,
            'price': price, 'cost': cost, 'margin': round((price - cost) / price * 100, 1),
            'sku': sku, 'inventory': inventory, 'category': category,
            'tags': tags or [], 'weight': weight,
            'images': images or [],
            'variants': [],
            'status': 'draft',  # draft, active, archived
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
        }
        return pid
    
    def add_variant(self, product_id: str, name: str, 
                    price_modifier: float = 0, sku: str = '',
                    inventory: int = 0) -> str:
        if product_id not in self.products: return ''
        vid = str(uuid.uuid4())[:8]
        self.products[product_id]['variants'].append({
            'id': vid, 'name': name,
            'price': self.products[product_id]['price'] + price_modifier,
            'sku': sku, 'inventory': inventory,
        })
        return vid
    
    def update_inventory(self, product_id: str, quantity: int, 
                         variant_id: str = None):
        if variant_id:
            for v in self.products[product_id]['variants']:
                if v['id'] == variant_id:
                    v['inventory'] = quantity
                    break
        else:
            self.products[product_id]['inventory'] = quantity
    
    def get_low_stock(self, threshold: int = 10) -> List[Dict]:
        low = []
        for p in self.products.values():
            if p['inventory'] <= threshold and p['inventory'] > 0:
                low.append({'title': p['title'], 'sku': p['sku'], 'remaining': p['inventory']})
        return low
    
    def get_margin_analysis(self) -> Dict:
        margins = [p['margin'] for p in self.products.values() if p['status'] == 'active']
        if not margins: return {}
        return {
            'avg_margin': round(sum(margins) / len(margins), 1),
            'highest': max(margins),
            'lowest': min(margins),
            'total_products': len(margins),
        }
```

## Order Management

```python
class OrderManager:
    """Manage orders, fulfillment, and customer communication."""
    
    def __init__(self):
        self.orders = {}
    
    def create_order(self, customer: Dict, items: List[Dict],
                     shipping_address: Dict, notes: str = '') -> str:
        import uuid
        oid = str(uuid.uuid4())[:8]
        
        subtotal = sum(i.get('price', 0) * i.get('quantity', 1) for i in items)
        tax = subtotal * 0.08  # Simplified
        shipping = 5.99 if subtotal < 50 else 0
        total = subtotal + tax + shipping
        
        self.orders[oid] = {
            'id': oid, 'customer': customer, 'items': items,
            'subtotal': subtotal, 'tax': tax, 'shipping': shipping,
            'total': round(total, 2),
            'status': 'pending',  # pending, confirmed, processing, shipped, delivered, cancelled
            'shipping_address': shipping_address,
            'notes': notes,
            'created_at': datetime.now().isoformat(),
        }
        return oid
    
    def update_status(self, order_id: str, status: str):
        if order_id in self.orders:
            self.orders[order_id]['status'] = status
    
    def get_order_summary(self, period_days: int = 30) -> Dict:
        now = datetime.now()
        from datetime import timedelta
        cutoff = now - timedelta(days=period_days)
        
        recent = [o for o in self.orders.values() 
                 if datetime.fromisoformat(o['created_at']) >= cutoff]
        
        total_revenue = sum(o['total'] for o in recent if o['status'] != 'cancelled')
        order_count = len(recent)
        
        return {
            'period_days': period_days,
            'total_orders': order_count,
            'total_revenue': round(total_revenue, 2),
            'avg_order_value': round(total_revenue / max(order_count, 1), 2),
            'pending': sum(1 for o in recent if o['status'] == 'pending'),
            'fulfilled': sum(1 for o in recent if o['status'] in ('shipped', 'delivered')),
        }
```

## Ecommerce Metrics

```python
ECOMMERCE_METRICS = {
    'conversion_rate': 'Orders / Sessions (%)',
    'aov': 'Average Order Value ($)',
    'atc_rate': 'Add-to-Cart Rate (%)',
    'checkout_rate': 'Checkout Initiation Rate (%)',
    'abandoned_cart': 'Cart Abandonment Rate (%)',
    'customer_acquisition_cost': 'CAC ($)',
    'ltv': 'Customer Lifetime Value ($)',
    'ltv_cac': 'LTV to CAC Ratio',
    'gross_margin': 'Revenue - COGS / Revenue (%)',
    'inventory_turnover': 'COGS / Average Inventory',
    'return_rate': 'Percentage of orders returned (%)',
}

def analyze_ecommerce_performance(data: Dict) -> str:
    report = "📊 Ecommerce Performance Report\n" + "=" * 40 + "\n"
    report += f"Revenue: ${data.get('revenue', 0):,.2f}\n"
    report += f"Orders: {data.get('orders', 0)}\n"
    report += f"AOV: ${data.get('aov', 0):.2f}\n"
    report += f"Conversion Rate: {data.get('conversion_rate', 0):.2f}%\n"
    report += f"Gross Margin: {data.get('gross_margin', 0):.1f}%\n"
    report += f"Cart Abandonment: {data.get('abandoned_cart', 0):.1f}%\n"
    return report
```

## Common Pitfalls

1. **Poor product photography** — customers can't touch products; invest in high-quality images
2. **Hidden costs at checkout** — surprise shipping costs cause 60%+ cart abandonment
3. **No mobile optimization** — 70%+ of ecommerce traffic is mobile
4. **Product page SEO** — product pages can rank for high-intent searches; optimize them
5. **Inventory sync issues** — selling out-of-stock items damages trust; sync in real-time
6. **Checkout friction** — every extra field reduces conversion; ask only what's necessary

## Verification Checklist

- [ ] Platform selected and configured
- [ ] Products added with images, descriptions, prices, variants
- [ ] Payment gateway configured
- [ ] Shipping zones and rates set up
- [ ] Tax settings configured
- [ ] Mobile-responsive theme active
- [ ] Analytics / tracking pixel installed
- [ ] Abandoned cart recovery set up
- [ ] Order fulfillment workflow defined
- [ ] Product pages SEO-optimized

## See Also

- email-marketing-campaigns — abandoned cart and post-purchase emails
- conversion-rate-optimization — optimizing product and checkout pages
- seo-search-engine-optimization — ranking product pages
- digital-marketing-strategy — ecommerce marketing strategy
