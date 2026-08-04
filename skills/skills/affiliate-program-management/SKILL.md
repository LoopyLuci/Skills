---
name: affiliate-program-management
description: "Use when managing affiliate programs. Tracking, payout."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [affiliate, program, management, tracking, commissions, payout]
    related_skills: [affiliate-marketing, affiliate-program-setup]
---

# Affiliate Program Management

## Overview
Operate and optimize an affiliate program: affiliate recruitment, onboarding, tracking setup, commission management, performance optimization, relationship building, compliance monitoring, and scaling strategies.

## When to Use
- "Manage my affiliate program day-to-day"
- "Optimize affiliate commissions and tracking"
- "Recruit new affiliates for my product"
- "Detect and prevent affiliate fraud"

## Affiliate Management Workflow

### Monthly Management Cycle
| Week | Focus | Key Activities |
|------|-------|----------------|
| Week 1 | Performance review | Analyze top/bottom performers, payouts, fraud |
| Week 2 | Affiliate outreach | Recruit new partners, engage top performers |
| Week 3 | Optimization | Creative refresh, commission tweaks, content |
| Week 4 | Planning + Compliance | Budget, strategy, policy review |

### Daily Check-in Tasks
- Monitor conversion rates by affiliate
- Check for fraudulent activity flags
- Review new applications (if approval required)
- Respond to affiliate support tickets

## Affiliate Recruitment & Onboarding

### Recruitment Strategies
| Channel | Approach | Success Rate |
|--------|----------|-------------|
| Competitor's affiliates | Reverse-engineer via similarweb/traffic data | High |
| Industry influencers | Direct outreach via social/email | Medium-High |
| Existing customers | Customer referral program + affiliate link | High |
| Content creators | YouTube/TikTok creators in your niche | Medium |
| Bloggers/reviewers | Product reviewers, niche bloggers | Medium |
| Agency partners | White-label/reseller programs | Medium-High |
| Affiliate networks | CJ, ShareASale, Impact Radius | Variable |

### Affiliate Onboarding Email Sequence
**Email 1 (Day 0): Welcome & Getting Started**
```
Subject: Welcome to [Brand] Affiliate Program — Your First Steps

Hi [Name],

Welcome! You're now approved for our affiliate program.

Your affiliate dashboard: [dashboard link]
Your unique tracking link: [link]
Commission rate: [X]% per sale
Cookie duration: [X] days

Getting started:
1. Review our media kit (attached)
2. Grab your preferred creative assets
3. Place your first affiliate link
4. Earn your first commission

FAQ: [affiliate-faq link]
Support: [support email]

Questions? Reply to this email — I'm here to help!

[Your Name]
Affiliate Manager
[Company]
```

**Email 2 (Day 2): Creative Assets & Best Practices**
```
Subject: Your Affiliate Assets + Best Practices for Maximum Conversions

Hi [Name],

Here are your resources for driving conversions:

🎨 Creative Assets:
- Banner ads (7 sizes): [link]
- Social media images: [link]
- Email signature badges: [link]
- Pre-written social copy: [link]

🚀 Best Practices:
1. Lead with value, not promotion
2. Share personal experiences with the product
3. Use your unique link in all posts
4. Focus on solving a problem, not selling a product

📊 Performance Tips:
- Best converting placements: [specific data if available]
- Top converting keywords: [data]
- Popular content formats: [data]

Need custom creatives? Just ask — I'll get them made for you.

[Your Name]
```

**Email 3 (Day 5): Performance Report & Motivation**
```
Subject: How Top Affiliates Are Crushing It + Your Performance

Hi [Name],

Quick check-in — how's your first few days going?

Here's what your top peers are doing:
- [Top affiliate name]: $X in sales with [strategy]
- [Top affiliate name]: 3.5% conversion with email
- [Top affiliate name]: $X in recurring commissions

Your current stats:
- Total clicks: [X]
- Conversion rate: [X%]
- Earnings this month: $[X]

Still early days — the average affiliate makes their first sale in [X] days.

Keep pushing! Let me know if you need anything.

[Your Name]
```

## Performance Tracking & Metrics

### Affiliate Scorecard Template
| Affiliate | Clicks | Conversions | Conversion Rate | Earnings | EPC | Tier |
|-----------|--------|-------------|-----------------|----------|-----|------|
| [Name] | 1,250 | 45 | 3.6% | $2,250 | $1.80 | Platinum |
| [Name] | 850 | 32 | 3.8% | $1,600 | $1.88 | Gold |
| [Name] | 500 | 8 | 1.6% | $400 | $0.80 | Silver |

### Key Performance Indicators
| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Conversion rate | >2% average | <0.5% |
| EPC (Earnings per Click) | >$1.00 | <$0.30 |
| Click-through rate | >0.5% | <0.1% |
| Cookie conversion | >1.5% | <0.3% |
| Monthly sales growth | >10% | <0% (two months) |

### Performance Tiers
| Tier | Conversion Rate | EPC | Benefits |
|------|----------------|-----|----------|
| Platinum | >5% | >$3.00 | 5% base commission + $300 monthly bonus |
| Gold | 3-5% | $1.50-$3.00 | 4% base + priority support |
| Silver | 2-3% | $0.75-$1.50 | 3.5% base |
| Bronze | 1-2% | $0.30-$0.75 | 3% base |
| Starter | <1% | <$0.30 | 3% base (no benefits) |

## Commission Management

### Commission Structure Options
| Model | Description | Best For |
|-------|-------------|----------|
| Flat rate | Fixed % of sale | Simple, predictable |
| Tiered | Higher % at volume thresholds | Motivating top performers |
| Recurring | % of subscription for X months | SaaS, memberships |
| Hybrid | Upfront + recurring | High-value products |
| Performance bonus | Extra for hitting targets | Seasonal pushes, launches |

### Payout Management System
| Payout Method | Min Amount | Processing Time | Fee |
|---------------|------------|-----------------|-----|
| PayPal | $25 | Instant-24h | 2.9% |
| Stripe | $10 | 2-3 days | 2.9% |
| Bank Transfer | $50 | 3-5 days | $1-2 |
| Wise | $25 | 1-2 days | 1-2% |
| Check | $100 | 7-10 days | $3 |

### Payout Automation Rules
```yaml
Payout Schedule:
  Frequency: First Monday of each month
  Threshold: $25 minimum
  Hold Period: 7 days (fraud prevention)
  Processing: Automatic batch

Exceptions:
  - High-risk affiliates: Manual review
  - New affiliates (<30 days): 14-day hold
  - International: 7-day hold
```

## Affiliate Relationship Management

### Tier-Based Communication Strategy
| Tier | Communication | Frequency |
|------|---------------|-----------|
| Platinum | Personal account manager, quarterly business reviews, exclusive early access | Monthly + quarterly |
| Gold | Dedicated support, monthly performance reports, beta access | Bi-weekly |
| Silver | Standard support, monthly newsletter, seasonal promotions | Monthly |
| Bronze/Starter | Self-service dashboard, automated reports | Monthly |

### Affiliate Newsletter Template
```
Subject: [Month] Affiliate Performance + New Opportunities

Hey partners,

Quick update on what's new:

📈 Performance Highlights
- This month's top performers: [names + earnings]
- New record: [X conversions] from email traffic
- Most improved affiliate: [name] (+X% conversion)

🎁 New Offers
- [Product/Launch]: Commissions now available!
- [Seasonal promo]: Boost your earnings this [season]
- [Bonus opportunity]: Extra [X%]% for top 10 affiliates

🎯 What's Working
- Best performing content: [data]
- Top converting placements: [data]
- New creatives: [links]

🚀 Training & Resources
- [Link to video]: "3 Proven Ways to Promote [Product]"
- [Link to blog]: "Advanced Affiliate Copywriting Tips"
- [Link to webinar]: "Live Q&A This Thursday"

📅 Upcoming
- New product launch: [date]
- Affiliate summit: [date]
- Quarterly bonus round: [dates]

Questions? Reply to this email!

[Your Name]
Affiliate Manager
```

## Fraud Detection & Prevention

### Fraud Red Flags
| Red Flag | Description | Action |
|----------|-------------|--------|
| **High click-to-sale ratio** | 100 clicks, 50 sales in 1 hour | Manual review required |
| **Geographic anomalies** | Traffic from unexpected countries | Verify and possibly block |
| **Unusual conversion patterns** | Sales spike at odd hours repeatedly | Manual review |
| **Cookie stuffing** | High conversions with low click-throughs | Audit tracking links |
| **Bot traffic** | Same IP converting multiple times | Block IPs, investigate |
| **Promotional abuse** | Using competitor's ads to drive traffic | Policy violation |
| **Incentivized conversions** | Cashback or rewards for signing up | Violates terms |

### Prevention Tools
| Tool | Purpose | Cost |
|------|---------|------|
| **Voluum** | Advanced tracking + fraud detection | $99-349/mo |
| **ThriveTracker** | Real-time tracking + bot detection | $79-249/mo |
| **HasOffers/Impact** | Enterprise fraud detection | $500+/mo |
| **Custom IP blacklist** | Block known bad actors | Free |
| **Conversion validation** | Require additional verification step | Free-setup |

## Compliance Management

### FTC/ASA Disclosure Monitoring
- Monthly scan of top affiliate posts for #ad/#sponsored
- Flag affiliates missing disclosures
- Send compliance warnings
- Escalate to suspension for repeat offenders

### Tax Compliance (US)
| Requirement | Threshold | Tool |
|-------------|-----------|------|
| 1099-MISC | $600+ annual | Track via affiliate platform |
| Sales tax | Varies by state | AvaTax + affiliate platform |
| VAT (EU) | Variable | VAT reporting in platform |

### Affiliate Program Agreement Updates
Review and update agreement quarterly for:
- Commission rate changes
- New product launches
- Policy updates (disclosure requirements)
- Territory expansions
- Exclusivity clauses

## Scaling Strategies

### Tier Expansion
```
Phase 1: 10 affiliates, 5% conversion, $500/month
Phase 2: 50 affiliates, 3% conversion, $2,500/month
Phase 3: 200 affiliates, 2% conversion, $10,000/month
Phase 4: 500 affiliates, 1.5% conversion, $25,000/month
```

### Channel Diversification
1. **Social Media**: Instagram, TikTok, YouTube influencers
2. **Content Sites**: Review sites, comparison sites, coupon sites
3. **Email Lists**: Newsletter swaps, sponsored content
4. **SEO Traffic**: Affiliates creating SEO-optimized content
5. **Paid Ads**: Affiliates running their own Facebook/Google ads
6. **Podcast Sponsorships**: Audio advertising through podcasts
7. **Event Sponsorships**: Conference booths, meetup sponsorships

## Common Pitfalls
1. **No onboarding system** — new affiliates don't know how to promote effectively
2. **One-size-fits-all communication** — platinum affiliates need personal attention
3. **Ignoring underperformers** — a quick call might unlock a high-potential affiliate
4. **Poor tracking setup** — can't optimize what you can't measure
5. **Fraud blindness** — not monitoring for fraudulent conversions
6. **Late commission payments** — destroys relationships and motivation
7. **No performance data sharing** — affiliates fly blind without conversion data
8. **Ignoring affiliate feedback** — affiliates know the market better than you
9. **One commission structure** — top affiliates want better rates
10. **No community** — affiliates working in isolation are less motivated

## Verification Checklist
- [ ] Monthly management cycle schedule defined
- [ ] Recruitment pipeline (5 channels) established
- [ ] Onboarding email sequence (3 emails) ready
- [ ] Affiliate scorecard template created
- [ ] Performance tiers defined with benefits
- [ ] Payout system and schedule documented
- [ ] Communication strategy tiered by affiliate level
- [ ] Fraud detection system in place (red flags + tools)
- [ ] Compliance monitoring (disclosure checks, tax reporting)
- [ ] Scaling plan with affiliate count milestones