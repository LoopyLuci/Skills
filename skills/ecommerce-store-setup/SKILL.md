---
name: ecommerce-store-setup
description: "Ecommerce: platform, products, checkout, launch."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ecommerce, shopify, woocommerce, online-store, selling]
    related_skills: [affiliate-marketing, freelance-business-operations, legal-and-compliance-basics]
---

# Ecommerce Store Setup

## Overview
A complete guide to launching and optimizing an ecommerce store. Covers platform selection, product page optimization, checkout flow, payment processing, shipping/tax, inventory management, abandoned cart recovery, and launch checklist.

## When to Use
- Choosing an ecommerce platform (Shopify vs WooCommerce vs BigCommerce vs Squarespace)
- Setting up product pages that convert
- Optimizing checkout flow and payment processing
- Configuring shipping zones, rates, and tax collection
- Setting up inventory tracking and low-stock alerts
- Implementing abandoned cart email recovery
- Running through a pre-launch checklist
- Auditing an existing store for optimization opportunities

## Body

### 1. Platform Selection

| Platform | Best For | Monthly Cost | Transaction Fees | Strengths | Weaknesses |
|----------|----------|-------------|-----------------|-----------|------------|
| **Shopify** | Most merchants, dropshipping, physical goods | $29–$299/mo | 2.4%–2.9% + $0.30 | Fully hosted, app ecosystem, POS system | Migration is hard |
| **WooCommerce** | WordPress, customization, no monthly fees | Free (+$10–$30/mo hosting) | Stripe/PayPal fees | Full control, SEO native | DIY maintenance, security |
| **BigCommerce** | Wholesale, B2B, large catalogs | $29–$299/mo | 0% on own gateway | No transaction fees, B2B features | Complex theme customization |
| **Squarespace** | Small stores, creators, low volume | $23–$49/mo | 2.9% + $0.30 | Beautiful templates, easy setup | Limited apps, scalability |

**Decision:** < 10 products → Squarespace; 10–1000 → Shopify; 1000+ → WooCommerce/BigCommerce. B2B → BigCommerce. Already WordPress → WooCommerce. Low tech → Shopify.

### 2. Product Page Optimization

**Structure:**
1. **Headline** (H1): Product name + key benefit
2. **Hero**: 3–5 high-res images + 1 demo video (15–30s)
3. **Price**: Clear, with compare-at strikethrough if on sale
4. **Add to Cart**: High contrast, above-fold, sticky on scroll
5. **Short desc**: 3–5 bullet benefits (not features)
6. **Variants**: Size, color, quantity selector
7. **Trust badges**: Free shipping, 30-day returns, secure checkout, reviews
8. **Full desc**: Problem → Solution → Specifications
9. **Reviews**: Minimum 5 reviews, photo reviews encouraged
10. **FAQ**: 5–8 common questions
11. **Upsells**: "Frequently Bought Together"
12. **Return policy**: Prominently linked

**Image specs:** 800×800px min (2048×2048px ideal), white or lifestyle bg, zoom-to-inspect, alt text for SEO.

### 3. Checkout Optimization (avg 70% abandonment)

| Tactic | Impact |
|--------|--------|
| Guest checkout (no forced account) | +15–25% |
| Progress indicator (3 steps) | +5–10% |
| Show shipping costs early in cart | +10–15% |
| Multiple payments (Cards, PayPal, Apple/Google Pay, BNPL) | +10–20% |
| Trust seals (SSL, McAfee, BBB) | +5–10% |
| Mobile-optimized (thumb-friendly) | +20–40% |
| Exit-intent popup with 10% off | +5–15% recovered |

**Abandoned cart emails:**
1. **1h**: "Forgot something? 👀" — show product + CTA
2. **24h**: "Still thinking?" — reviews + free shipping reminder
3. **72h**: "Cart expiring — 10% off" — discount + scarcity

### 4. Payments, Shipping & Tax

**Payments priority:** Platform-native (lowest fees) → PayPal → Apple/Google Pay → BNPL (Klarna/Afterpay, +30–50% AOV) → Regional methods.

**Shipping tiers:** Free over $X (set 20–30% above AOV) → Flat-rate below → Expedited at cost → International via carrier API.

**Tax:** Auto-tax engine (platform or TaxJar/Avalara). VAT for EU/UK. Economic nexus thresholds per state. Different rules for digital goods.

### 5. Inventory & Cart Recovery

**Inventory:** Real-time multi-channel sync. Low-stock alert at 20% of reorder point. Safety stock = 2 weeks average sales. FIFO for perishables.

**Cart recovery:** Enable tracking → 3-email sequence → SMS (if available) → Retargeting pixel → Exit-intent popup. Rates: Email 10–15%, SMS 20–30%.

### 6. Launch Checklist

- [ ] Custom domain + SSL active
- [ ] Mobile responsive verified
- [ ] All products: 3+ images, SEO meta, descriptions, variants, SKUs
- [ ] Payment gateway tested end-to-end (real transaction)
- [ ] Shipping zones + rates configured and tested
- [ ] Legal policies published (privacy, returns, terms, shipping)
- [ ] Cookie consent banner active
- [ ] GA4 + Meta pixel + Google Merchant Center installed
- [ ] Email marketing connected (Klaviyo/Mailchimp), welcome email active
- [ ] Fulfillment workflow documented

## Common Pitfalls

- **Platform lock-in**: Test 30 days before committing. Migration is expensive.
- **No mobile optimization**: 60–80% traffic is mobile.
- **Hidden costs**: Apps + themes + transaction fees = $50–200/mo beyond plan.
- **SEO neglect**: Unique meta descriptions, alt text, URL slugs required.
- **One-size shipping**: #1 cart abandonment reason. Free shipping on threshold.
- **No post-purchase flow**: 60% of first-time buyers never return.
- **Too many products**: Start with 10–20 hero products, expand later.

## Verification Checklist

- [ ] Platform selected and trial active
- [ ] 10+ optimized product pages with images and SEO
- [ ] Test purchase completed end-to-end
- [ ] Shipping + tax configured and documented
- [ ] Abandoned cart email sequence active
- [ ] Launch checklist complete
- [ ] Legal policies published
- [ ] Analytics/pixels firing correctly
- [ ] Fulfillment workflow documented