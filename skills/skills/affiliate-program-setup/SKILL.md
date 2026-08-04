---
name: affiliate-program-setup
description: "Use when running affiliate programs. Recruitment, payouts."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [affiliate, program, recruitment, payouts, commissions, tracking]
    related_skills: [affiliate-marketing, seo-strategy]
---

# Affiliate Program Setup

## Overview
Launch and operate a performance-based affiliate program: platform selection, commission structure design, affiliate recruitment, creative asset delivery, tracking implementation, payout processing, compliance setup, and scaling strategies.

## When to Use
- "Start an affiliate program for my product"
- "Set up affiliate tracking for my SaaS"
- "Recruit affiliates for my business"
- "Manage affiliate payouts and compliance"

## Platform Selection

| Platform | Best For | Setup Cost | Monthly Cost | Payout Methods |
|----------|----------|------------|--------------|----------------|
| Post Affiliate Pro | Full control, custom domains | $0 | $99-349/mo | PayPal, Stripe, Bank transfer |
| Refersion | Shopify + SaaS brands | $0 | $89-399/mo | PayPal, Stripe, Bank transfer |
| ShareASale (Awin) | Large merchant catalog, established network | $0 | 20% of sale | Network handles payouts |
| CJ Affiliate | Enterprise brands, established publishers | $0 | ~2-10% transaction fee | Network handles payouts |
| Impact | Enterprise, advanced automation | Custom | Custom | Multiple methods |
| Tapfiliate | SMB, easy setup | $0 | $69-249/mo | PayPal, Stripe, Bank transfer |

## Commission Structure Design

### Decision Framework
| Factor | Question | Your Answer |
|--------|----------|-------------|
| Product price | How expensive is your product? | e.g., $100/month, $1000 license |
| Margins | What's your minimum viable commission? | e.g., 20% minimum |
| Competition | What are competitors paying? | Research via competitor affiliate pages |
| Affiliate quality | High-tier vs broad recruitment? | Target quality over quantity |
| Budget | Fixed monthly budget for acquisitions? | Plan based on LTV, not product cost |

### Commission Models

| Model | Structure | Best For | Pros | Cons |
|-------|-----------|----------|------|------|
| Percentage of sale | 10-30% of transaction | E-commerce, digital products | Simple, scales with price | Lower for high-ticket items |
| Tiered percentage | 10% first 10 sales, 15% next 20 | Incentivizing high-volume | Motivates more sales | Complex to explain |
| Recurring | 10-50% monthly, 3-30 months | SaaS, subscription, membership | High LTV for affiliates | Expensive if churn is high |
| CPA (Cost Per Action) | $5-50 per signup/demo | Lead generation, freemium | Predictable cost | Lower conversion on actions |
| Custom (hybrid) | Base + % + bonuses | Enterprise, complex products | High motivation | Difficult to track |
| Two-tier | Earn on referred affiliates' sales | Network effects, B2B | Builds pyramid | Complicated, spam risk |

### Tier Structure Example (SaaS)
| Tier | Monthly Commission | Volume Requirement | Cookie Length |
|------|-------------------|-------------------|---------------|
| Bronze | 20% | First 10 conversions/month | 30 days |
| Silver | 25% | 11-50 conversions/month | 45 days |
| Gold | 30% | 51-100 conversions/month | 60 days |
| Platinum | 35% + $500 bonus | 100+ conversions/month | 90 days |

### Cookie Duration Guidelines
| Business Type | Recommended Duration | Reasoning |
|---------------|---------------------|----------|
| E-commerce | 30 days | Purchase happens quickly |
| SaaS (monthly) | 60 days | Consideration period + free trial |
| SaaS (annual) | 90 days | Longer sales cycle |
| High-ticket B2B | 120 days | Long sales cycle, multiple stakeholders |
| Subscription | 60-90 days | Retention risk in first 90 days |

## Affiliate Recruitment

### Target Affiliate Personas
| Persona | Description | Recruitment Approach |
|---------|-------------|---------------------|
| Micro-Influencers | 1K-50K followers, niche audience | Instagram, TikTok outreach, micro-influencer platforms |
| Content Creators | Bloggers, YouTubers, podcasters | Guest post outreach, podcast sponsorship |
| Industry Experts | Consultants, coaches in adjacent spaces | Speaking at their webinars, cross-promotion |
| Complementary Businesses | Non-competing companies with same audience | Partnership programs, referral swaps |
| Existing Customers | Happy customers who'd refer | Customer referral program + affiliate link |
| Agency Partners | Marketing/digital agencies | White-label reseller program |

### Recruitment Email Template
```
Subject: Partnership Opportunity — [Your Brand] + [Their Name/Business]

Hi [Name],

I've been following your content on [specific platform/thing they do],
particularly your [specific post/video] about [topic]. Your audience clearly
values your expertise in [area].

We're [Your Company], a [brief description — 1 sentence]. We help
[target audience] [solve specific problem]
through [brief differentiator].

Our affiliate program might be a great fit for you because:
- [Commission/benefit] (e.g., "30% recurring commissions")
- [Unique selling point for affiliates] (e.g., "90-day cookie, highest in industry")
- [Your audience would benefit] (specific connection)

Would you be interested in a quick chat about how this could work?
I'm happy to send over our media kit and answer any questions.

Best,
[Your Name]
[Your Title]
[Your Company]
[Your Contact Info]
```

### Outreach Tools
- **Email finder**: Hunter.io, Apollo, LinkedIn Sales Navigator
- **Influencer platforms**: AspireIQ, Upfluence, Traackr
- **Micro-influencer platforms**: Heepsy, Influeex, HypeAuditor

## Creative Asset Delivery

### Asset Types by Affiliate Persona
| Asset | Micro-Influencer | Content Creator | Industry Expert | Agency |
|-------|------------------|-----------------|-----------------|--------|
| Pre-made social graphics | ✅ | ✅ | ❌ | |
| Raw product videos | ✅ | ✅ | ❌ | |
| Product images (high-res) | ✅ | ✅ | | |
| Logo variations | | | ✅ | ✅ |
| Case study documents | | | ✅ | ✅ |
| White-label reports | | | | ✅ |
| Presentation decks | | | | ✅ |
| Demo accounts | | ✅ | ✅ | ✅ |
| Tracking link generator | ✅ | ✅ | ✅ | ✅ |

### Asset Delivery System
1. **Affiliate dashboard**: Central portal for downloading assets
2. **Brand guidelines**: Colors, fonts, logo usage, prohibited uses
3. **Asset tagging**: Tag assets by campaign, persona, format
4. **Approval workflow**: New assets reviewed before publishing
5. **Version control**: Latest version always available

## Tracking & Attribution

### Tracking Implementation
| Method | Best For | Accuracy | Setup Effort |
|--------|----------|----------|--------------|
| Cookie-based (standard) | All affiliate programs | Medium (clear cookies, cross-device) | Low |
| Server-to-server tracking | High-ticket, enterprise | High | Medium |
| UTM parameters | Campaign tracking, attribution | Medium | Low |
| Pixel tracking | E-commerce, retargeting | Medium | Low |
| Blockchain/AI tracking | Fraud prevention | High | High |

### Attribution Models
| Model | Description | Best For |
|-------|-------------|----------|
| Last-click (default) | 100% credit to last affiliate click | General |
| First-click | 100% to first touch | Awareness campaigns |
| Linear | Equal split across all clicks | Multi-touch campaigns |
| Time decay | More credit to clicks nearer conversion | Long sales cycles |
| Custom | Weighted (e.g., 60% last, 40% first) | High-consideration products |

## Payout Management

### Payout Schedule Options
| Frequency | Threshold | Best For |
|-----------|-----------|----------|
| Weekly | $25 | High-volume, transactional |
| Bi-weekly | $50 | Standard B2C/SaaS |
| Monthly | $100 | Most affiliate programs |
| Net 30 | $500 | Enterprise, high-ticket |

### Payout Methods
1. **PayPal** — Fastest (24-48 hrs), low threshold, but fees + PayPal account required
2. **Stripe Connect** — Good for global, 2-7 days, integrated with platform
3. **Bank Transfer (ACH/Wire)** — Reliable, $0.50-1.00 fee, 2-5 business days
4. **Wise (formerly TransferWise)** — Best for international, low fees
5. **Check** — Slowest, use only for large legacy partners

### Payment Terms Template
```
Affiliate Payment Terms
- Net 30 payment schedule
- $50 minimum payout
- Payments processed on the 15th of each month for prior month commissions
- Payment method: [PayPal/Stripe/Bank transfer]
- Taxes: Affiliates responsible for their own tax obligations
- Chargeback fee: $25 if disputed
```

## Compliance & Fraud Prevention

### FTC/ASA Disclosure Requirements
- Affiliates MUST disclose partnerships with words like:
  - "#ad", "#sponsored", "Paid partnership with [brand]"
  - Must be as prominent as the post itself
  - Not just in the caption — must be visible in image/video

### Fraud Prevention Measures
| Method | How It Works |
|--------|-------------|
| Cookie stacking detection | Track multiple referrals, flag suspicious patterns |
| IP reputation | Check affiliate IPs against fraud databases |
| Conversion velocity | Flag affiliates with unusually high conversion rates |
| Manual review | Periodic audit of top-performing affiliates |
| Attribution window capping | Limit cookie duration to reduce fraud |

### Tax Compliance
- **US**: Issue 1099-MISC for affiliates earning $600+ annually
- **EU**: VAT reporting on affiliate commissions paid
- **Global**: Check local tax obligations — many countries have thresholds

## Performance Optimization

### Affiliate Incentive Programs
| Program | Criteria | Reward |
|---------|----------|--------|
| Top Performer Award | Highest revenue in 30 days | $500 bonus + badge |
| Growth Champion | 200% growth month-over-month | Commission bump for 3 months |
| Content Creator | 5+ quality posts with affiliate links | Early access + free product |
| Retention | Stay for 6 months | $100 loyalty bonus |

### Performance Tiers
| Tier | Monthly Revenue | Commission | Benefits |
|------|-----------------|------------|----------|
| Starter | < $1,000 | Base rate | Standard support |
| Rising | $1,000-$5,000 | +5% bump | Priority support |
| Elite | $5,000-$25,000 | +10% bump | Dedicated account manager |
| VIP | $25,000+ | +15% bump, custom tiers | Co-marketing opportunities |

### A/B Testing for Affiliate Programs
Test one variable at a time:
1. **Commission rate**: 15% vs 25% — measure signups + revenue
2. **Cookie duration**: 30 vs 60 days — measure conversion quality
3. **Creative assets**: Test different images/videos — CTR + conversion rate
4. **Dashboard UX**: Test different layouts — affiliate engagement
5. **Payment terms**: Net 30 vs Net 15 vs Weekly — signup rates

## Common Pitfalls
1. **Unclear terms** — commissions, cookies, payout schedules must be in writing
2. **Poor creative** — affiliates can't promote with terrible screenshots or stock photos
3. **No dedicated support** — affiliates need quick answers to convert effectively
4. **Ignoring fraud** — affiliate fraud can drain your budget quickly if unchecked
5. **One-size-fits-all commissions** — top affiliates deserve better rates, tiered structures incentivize growth
6. **No communication** — affiliates need regular updates, new assets, campaign info
7. **Delayed payments** — slow payouts kill affiliate motivation; pay consistently and on time

## Verification Checklist
- [ ] Platform/platforms selected with pricing and features documented
- [ ] Commission structure designed with tier logic and cookie duration
- [ ] 3-5 affiliate personas identified with recruitment approach for each
- [ ] Creative assets created or commissioned (social graphics, videos, images)
- [ ] Tracking implemented (cookie, UTM, or server-to-server)
- [ ] Attribution model selected and documented
- [ ] Payout schedule, methods, and terms defined
- [ ] Compliance checklist (FTC disclosures, tax reporting)
- [ ] Fraud prevention measures implemented
- [ ] Affiliate dashboard/landing page built
- [ ] Launch announcement ready (email sequence, social posts)