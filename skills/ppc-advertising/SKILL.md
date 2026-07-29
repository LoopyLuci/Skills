---
name: ppc-advertising
description: "Use when planning PPC ads. Keywords, bidding, tracking."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ppc, google-ads, facebook-ads, paid-media, advertising]
    related_skills: [conversion-rate-optimization, marketing-analytics-dashboard, content-marketing-workflow]
---

# PPC Advertising

## Overview

A comprehensive paid media management methodology covering the full lifecycle of pay-per-click advertising across Google Ads, Microsoft Ads, Meta (Facebook/Instagram) Ads, LinkedIn Ads, and programmatic platforms. This skill covers campaign structure, keyword match types, ad group organization, ad copy formulas, landing page alignment, bidding strategies (Manual CPC, Target CPA, Target ROAS), conversion tracking setup, UTM parameter management, audience targeting, A/B testing frameworks, quality score optimization, and performance analysis.

## When to Use

- Launching a new paid media campaign for a product or service
- Restructuring existing ad accounts for better performance
- Planning and forecasting paid media budgets
- Setting up conversion tracking and attribution
- Optimizing campaigns for lower CPA or higher ROAS
- Running A/B tests on ad copy, landing pages, or audiences
- Diagnosing underperforming campaigns and identifying fixes

## Body

### 1. Campaign Planning & Structure

#### 1.1 Account Hierarchy (Google Ads)

```
Account
├── Campaign (goal-aligned, separate budget)
│   ├── Ad Group 1 (tightly themed keywords)
│   │   ├── Keyword 1
│   │   ├── Keyword 2
│   │   ├── Ad 1 (headline, description, assets)
│   │   └── Ad 2 (A/B variant)
│   ├── Ad Group 2
│   │   ├── Keyword 3
│   │   ├── Keyword 4
│   │   ├── Ad 1
│   │   └── Ad 2
│   └── (max 20 ad groups per campaign recommended)
├── Campaign 2
└── ...
```

**Campaign structure rules:**
- Separate campaigns for: Search, Display, Shopping, Video, Discovery, Performance Max
- Separate campaigns by: Brand vs. Non-brand, Geography (if local), Product category, Device (if performance differs)
- Separate ad groups by: Keyword theme (tightly related — don't mix topics), Match type (exact/phrase in one, broad in another), Landing page (same theme = same page)

#### 1.2 Campaign Types & Objectives

| Platform | Campaign Type | Best For | Objective Options |
|---|---|---|---|
| Google Ads | Search | Intent-driven clicks, leads, sales | Sales, Leads, Website Traffic |
| Google Ads | Performance Max | E-commerce, omnichannel | Sales, Leads |
| Google Ads | Shopping | E-commerce product sales | Sales |
| Google Ads | Display | Retargeting, awareness | Brand Awareness, Reach |
| Google Ads | Demand Gen | Full-funnel awareness | Brand, Consideration |
| Google Ads | Discovery | Visual prospecting | Sales, Leads |
| Meta Ads | Conversion | Direct response, sales | Sales, Leads, Value |
| Meta Ads | Traffic | Website visits | Traffic |
| Meta Ads | Lead Gen | Lead collection (native forms) | Leads |
| Meta Ads | Awareness | Brand reach, video views | Brand Awareness, Reach |
| Meta Ads | Engagement | Post engagement, messages | Engagement |
| LinkedIn Ads | Sponsored Content | B2B lead generation | Website Visits, Leads |
| LinkedIn Ads | Sponsored Messaging | High-intent B2B outreach | Leads, Website Visits |
| LinkedIn Ads | Text Ads | Low-cost B2B traffic | Website Visits |

### 2. Keyword Strategy

#### 2.1 Match Types (Google Ads)

| Match Type | Symbol | Matching Behavior | Example (keyword: red shoes) | Reach | Precision |
|---|---|---|---|---|---|
| **Exact** | [keyword] | Only exact match and close variants | Searches for "red shoes", "red shoe" | Low | Very high |
| **Phrase** | "keyword" | Contains the phrase (word order matters) | "buy red shoes online", "cheap red shoes" | Medium | High |
| **Broad** | keyword | Any related search, synonyms, variations | "blue sneakers", "running footwear" | High | Low |
| **Broad (modified)** | +keyword | Contains (or close variant) each +word | "red +shoes" — must have "shoes" or variant | Medium-High | Medium |

**Match type strategy by campaign phase:**

| Phase | Exact | Phrase | Broad | Rationale |
|---|---|---|---|---|
| Launch (weeks 1–2) | 30% | 50% | 20% | Collect data, control spend |
| Optimization (weeks 3–6) | 40% | 40% | 20% | Scale winners, refine negatives |
| Scaling (weeks 7+) | 50% | 30% | 20% | Maximize reach on proven terms |
| Mature account | 60% | 25% | 15% | Protect CPA, high precision |

#### 2.2 Negative Keywords

**Types of negatives to add:**

| Category | Example Negatives | Why |
|---|---|---|
| Free seekers | free, trial, complimentary, gratis | Low-intent unless you offer free |
| Job seekers | job, career, hiring, position | Irrelevant search |
| Student / Research | essay, homework, definition, what is | Informational only (no purchase intent) |
| Competitors | [competitor brand names] | Protects brand budget |
| Incompatible intent | "how to", "repair", "replacement" | Match intent to your offer |
| Incompatible audience | [locations you don't serve], [irrelevant segments] | Waste removal |

**Negative build process:**
1. Start with a seed list (above) at campaign launch
2. Review Search Terms Report weekly
3. Add irrelevant terms as negatives immediately
4. Review quarterly for missed patterns

#### 2.3 Search Terms Analysis Flow

```
Weekly: Export Search Terms Report from Google Ads
  ↓
Mark as:
  ├── Relevant & converting → Add to exact match campaign, Increase bid
  ├── Relevant & not converting → Add as phrase match, Monitor
  ├── Relevant but broad → Add as exact match with lower bid, Test
  └── Irrelevant → Add as negative keyword
  ↓
Review patterns:
  ├── New theme emerging? Create new ad group/campaign
  └── Keyword covering too many themes? Break into separate ad groups
```

### 3. Ad Copy & Creative

#### 3.1 Google Ads Responsive Search Ad (RSA) Structure

Each RSA can have up to **15 headlines** and **4 descriptions**. The system tests combinations. Optimize across all assets.

**Headline formulas (pick 3–5 per theme):**

| Formula | Example | Best For |
|---|---|---|
| **Benefit + Keyword** | "Save 50% on [product] Today" | Promotions |
| **Social Proof + CTA** | "Join 10,000+ Happy Customers" | Trust building |
| **Question + Solution** | "Need [service]? Get Quote Free" | Problem-aware |
| **How-to + Speed** | "Start [action] in Under 5 Minutes" | Low friction |
| **Number + Promise** | "3 Steps to [benefit] — Watch Demo" | Process explaining |
| **Pain + Relief** | "Tired of [pain]? Switch Now" | Pain awareness |
| **Price + Value** | "Premium [Product] — From $29/mo" | Price-sensitive |
| **Urgency + Scarcity** | "Limited Stock — Order Today" | Impulse decisions |

**Description formulas:**

| Position | Content | Character Limit |
|---|---|---|
| Description 1 | Unique value proposition + primary CTA | 90 |
| Description 2 | Features, benefits, social proof + secondary CTA | 90 |
| Description 3 | Price, promotion, guarantee, or urgency (pin if critical) | 90 |

**RSA optimization rules:**
- Pin 3–5 headlines and 2–3 descriptions for minimum viable ad
- Use at least 8–10 headlines and 3 descriptions for maximum ML optimization
- Don't duplicate the same message across headlines (Google can show multiple headlines at once — duplicates waste space)
- Use the "pinned" feature sparingly — only for legally required or brand-critical copy
- Rotate in new assets every 30 days to avoid ad fatigue

#### 3.2 Meta/Facebook Ad Creative

```
Primary Text (150–500 chars): Hook + problem + solution + CTA
Headline (27–40 chars): Short, punchy value proposition
Description (15–30 chars): Brief supportive info
CTA Button: Choose from platform options (Shop Now, Learn More, Sign Up, Contact Us)
Creative: Image (1:1 or 4:5), Video (15s–60s), Carousel, Collection
```

**Meta creative formulas:**
- **Problem/Solution:** Show problem → reveal your solution as the fix
- **Before/After:** Visual transformation
- **Testimonial:** Customer quote + result
- **Educational:** Tip or insight → your product enables it
- **Behind the Scenes:** Transparent, human brand content
- **UGC (User-Generated Content):** Real customer photos/videos

**Creative testing framework (CxT):**

```
Audience A × Creative 1 → Measure CPA
Audience A × Creative 2 → Measure CPA
Audience B × Creative 1 → Measure CPA
Audience B × Creative 2 → Measure CPA
```

Minimum 3 variations per dimension for valid results.

### 4. Landing Page Alignment

#### 4.1 Quality Score Factors (Google Ads)

| Factor | Weight | Optimization |
|---|---|---|
| Expected CTR | High | Ad copy relevance, keyword match |
| Ad Relevance | High | Keyword-to-ad alignment |
| Landing Page Experience | High | Page relevance, load speed, mobile UX |

**QS optimization checklist:**
- [ ] Ad copy includes keyword from ad group (preferably in headline)
- [ ] Landing page headline matches ad message (message match)
- [ ] Landing page includes the keyword naturally
- [ ] Landing page loads in < 2 seconds on mobile
- [ ] Clear, single CTA above the fold
- [ ] CTA button matches ad CTA text
- [ ] Trust signals visible (testimonials, security badges, guarantees)
- [ ] No unrelated navigation or distracting elements
- [ ] Form/tracking pixel fires correctly
- [ ] Page is mobile-responsive with 44pt+ tap targets

#### 4.2 Message Match Matrix

```
Ad Headline: "Save 20% on Enterprise CRM"
Ad Description: "Trusted by 5,000+ teams. Free 14-day trial."
                       ↓
Landing Page H1: "Save 20% on Enterprise CRM"
Landing Page Subhead: "Trusted by 5,000+ teams. Try free for 14 days."
Landing Page CTA: "Claim 20% Off → Start Free Trial"
```

**Rule:** The user should feel they arrived at the exact page they expected. Any disconnect increases bounce rate and lowers QS.

### 5. Bidding Strategies

#### 5.1 Bidding Strategy Selection

| Strategy | When to Use | How It Works | Best For |
|---|---|---|---|
| **Manual CPC** | New campaigns (< 50 conversions), testing | You set max CPC bids | Data collection, control |
| **Enhanced CPC (ECPC)** | Transition from manual to automated | Manual bids + auto-adjust for likely conversions | Stepping stone to automation |
| **Target CPA** | Stable conversion data (50+ conv/30d) | Auto-bids to hit target cost per acquisition | Lead gen, form fills |
| **Target ROAS** | E-commerce with known ROAS goal | Auto-bids to hit target return on ad spend | Shopping, online sales |
| **Maximize Clicks** | Brand awareness, low budget | Spend full budget on as many clicks as possible | Traffic-focused |
| **Maximize Conversions** | New to auto-bidding, no CPA target | Spend full budget to get most conversions | General lead gen |
| **Maximize Conversion Value** | E-commerce, no ROAS target | Spend full budget for highest conversion value | General e-commerce |
| **Target Impression Share** | Brand defense, absolute top | Bid to appear at top or absolute top of page | Brand awareness |

#### 5.2 Bidding Strategy Maturity Model

```
Phase 1 (< 50 conversions)
├── Manual CPC + ECPC
└── Collect conversion data, refine keywords, negatives, ad copy

Phase 2 (50–200 conversions)
├── Transition to Target CPA (set at 120% of historical avg CPA)
└── Enable audience signals, refine target

Phase 3 (200+ conversions)
├── Target CPA (at or below historical avg)
├── Add Target ROAS for e-commerce
└── Experiment with Performance Max
```

### 6. Conversion Tracking & Attribution

#### 6.1 Conversion Tracking Setup

**Google Ads:**
1. Install Google Tag (gtag.js) or Google Tag Manager (GTM) on site
2. Create conversion actions in Google Ads
3. Add event snippet to thank-you/confirmation pages
4. Test with Tag Assistant or Google Ads preview mode

**Key conversions to track:**

| Conversion Type | Value | Required for |
|---|---|---|
| Purchase / Sale | Actual revenue | E-commerce, ROAS bidding |
| Lead / Form Submit | Average CPL assigned | Lead gen, CPA bidding |
| Phone Call | Average CPL assigned | Call-based businesses |
| Sign-up (Free Trial) | Estimated LTV × CVR | SaaS, subscription |
| Add to Cart | No value (micro-conversion) | E-commerce funnel analysis |
| Email Signup | No value (micro-conversion) | Content/lead gen |
| Page View (key page) | No value (micro-conversion) | Engagement analysis |

#### 6.2 UTM Parameter Structure

Standard naming convention for all paid campaigns:

```
?utm_source=google
&utm_medium=cpc
&utm_campaign=campaign_name
&utm_term={keyword}
&utm_content=ad_variant
```

| Parameter | Source | Auto-tagging? | Notes |
|---|---|---|---|
| utm_source | google, facebook, linkedin, bing, twitter | G-Ads auto-tag replaces source | Manual for non-Google platforms |
| utm_medium | cpc, paid_social, display, email | Used by GA4 for channel grouping | Be consistent — don't mix "cpc" and "ppc" |
| utm_campaign | Descriptive name | G-Ads auto-tag has campaign ID | Name format: [campaign]_[date] |
| utm_term | Keyword or targeting | G-Ads auto-tags {keyword} | Essential for search term analysis |
| utm_content | Creative/ad variant | G-Ads auto-tags {creative} | Use for A/B test variants |

**Naming convention template:**
```
utm_campaign = {campaign_type}_{product/offer}_{targeting}_{date}
Example: search_crm-software_smb-us_202507
```

**Auto-tagging:** Enable Google Ads auto-tagging (default). For platforms without auto-tagging (Meta, LinkedIn, Bing), use manual UTM parameters.

### 7. Audience Targeting

#### 7.1 Google Ads Audiences

| Audience Type | Source | Best Use |
|---|---|---|
| **Remarketing** | Site visitors (via Google Tag) | Re-engage past visitors |
| **Customer Match** | Email list upload | Target or exclude known customers |
| **In-Market** | Google inferred purchase intent | Prospecting for ready buyers |
| **Affinity** | Long-term interests and habits | Broad awareness |
| **Custom Segments** | Keywords, URLs, apps people engage with | Tailored prospecting |
| **Detailed Demographics** | Age, gender, income, parental status | Demographic targeting |
| **Similar Segments** | Based on existing remarketing lists | Scale lookalikes |
| **Your Data (GA4)** | GA4 audiences synced to Google Ads | Predictive audiences, engaged users |

**Targeting hierarchy (from narrowest to broadest):**
1. Customer Match (known customers)
2. Remarketing (past visitors)
3. Similar Segments (lookalike to site visitors)
4. Custom Segments (intent-based)
5. In-Market (ready to buy)
6. Affinity (interested)
7. Demographics (broad)

#### 7.2 Meta/Facebook Audiences

| Audience Type | Source | Best Use |
|---|---|---|
| **Retargeting** | Pixel, Customer List, App Activity | Re-engage site/app visitors |
| **Lookalike (LAL)** | Seed audience (1%–10% similarity) | Scale new users similar to best customers |
| **Interest** | Platform-declared interests (e.g., "Digital Marketing") | Broad targeting by affinities |
| **Behavior** | Purchase behavior, device usage | Behavioral segmentation |
| **Custom Audience** | Uploaded list, video viewers, page engagers | Highly specific targeting |
| **Layered Targeting** | Combinations of interests + demographics + behaviors | Precision targeting |

**Lookalike best practices:**
- Use 1% LAL for highest similarity (smallest audience, best performance)
- Use 3–5% LAL for balance of scale and similarity
- Use value-based LAL (LTV seed) for e-commerce
- Refresh seed audience every 30 days

### 8. A/B Testing Framework

#### 8.1 What to Test

| Element | Test Duration | Sample Size (per variant) | Platform |
|---|---|---|---|
| Ad copy (headline, description) | 7–14 days | 100+ clicks | Google, Meta |
| Landing page | 14–21 days | 100+ conversions | Both |
| Audience/targeting | 7–14 days | 500+ impressions | Meta, LinkedIn |
| Bid strategy | 14–28 days | 100+ conversions | Google |
| Ad format (image vs. video) | 14–21 days | 10K+ impressions | Meta |
| Call to action | 7–14 days | 100+ clicks | Google, Meta |
| Offer (discount vs. value-add) | 14–21 days | 50+ conversions | Both |
| Landing page form length | 14–21 days | 100+ form starts | Both |

#### 8.2 Testing Protocol

1. **Hypothesize:** "Changing [element] from [A] to [B] will improve [metric] by [X%] because [reasoning]."
2. **Design:** One variable per test. Isolate cleanly.
3. **Sample:** Use a statistical significance calculator (e.g., Optimizely's Sample Size Calculator). Target 80% power, 95% confidence.
4. **Run:** Minimum 7 days (or until statistically significant). Avoid ending tests early (peeking problem).
5. **Analyze:** If p < 0.05 and lift > 5%, declare a winner. Otherwise, inconclusive — iterate.
6. **Implement:** Roll out winning variant to 100%. Document results.
7. **Document:** Log in a shared test results sheet:

```
| Date | Campaign | Test Element | Variant A | Variant B | Metric | Winner | Lift | Significance | Notes |
```

### 9. Budget Management

#### 9.1 Budget Allocation Model

| Account Phase | % Budget to Brand | % to Non-Brand | % to Remarketing | % to Test |
|---|---|---|---|---|
| Launch (0–3 months) | 30% | 40% | 10% | 20% |
| Growth (3–12 months) | 20% | 50% | 15% | 15% |
| Mature (12+ months) | 15% | 50% | 20% | 15% |

#### 9.2 Budget Pacing Formula

```
Daily Budget = Monthly Budget / 30

Pacing Check (mid-month):
Actual Spend / (Days Elapsed × Daily Budget) = % of Budget Used
If > 105%: Reduce bids or pause low-performers
If < 95%: Increase bids, expand keywords, or add audiences
```

### 10. Performance KPIs & Benchmarks

#### 10.1 Industry Benchmarks

| Metric | Google Ads (Search) | Google Ads (Display) | Meta Ads | LinkedIn Ads |
|---|---|---|---|---|
| Avg. CTR | 3.17% | 0.46% | 0.90% | 0.44% |
| Avg. CPC | $1.16 (B2B: $3.33) | $0.63 | $0.94 | $5.26 (B2B) |
| Avg. Conversion Rate | 3.75% | 0.77% | 4.1% | 3.0% |
| Avg. CPA (Lead Gen) | $31 (B2B: $53) | $82 | $23 | $92 |
| Avg. ROAS (E-com) | 4:1 | N/A | 3:1 | N/A |

#### 10.2 Account Health Scorecard

| Checklist Item | Pass | Fail | Action if Failing |
|---|---|---|---|
| Conversion tracking verified | ✓ | ✗ | Fix tag, verify with Tag Assistant |
| Search Terms Report reviewed last 7 days | ✓ | ✗ | Set recurring weekly review |
| Negative keywords updated last 7 days | ✓ | ✗ | Add new negatives from search terms |
| Ad rotation set to "Optimize" | ✓ | ✗ | Change campaign setting |
| At least 2 RSAs or 3 ads per ad group | ✓ | ✗ | Write new ads |
| Landing pages mobile-friendly | ✓ | ✗ | Test with Mobile-Friendly Test tool |
| Quality Score > 6 on top terms | ✓ | ✗ | Improve ad relevancy, landing page |
| Budget not limited (lost IS < 10%) | ✓ | ✗ | Increase budget or reduce spend |
| Impression share (top) > 50% | ✓ | ✗ | Increase bids or budget |
| Attribution model reviewed this quarter | ✓ | ✗ | Evaluate data-driven vs. last-click |
| A/B test active or planned this month | ✓ | ✗ | Start a test |
| UTM parameters consistent and validated | ✓ | ✗ | Standardize naming convention |

## Common Pitfalls

1. **No negative keyword strategy:** Without active negative keyword management, 20–30% of spend can go to irrelevant searches. Review search terms weekly.
2. **Mixing match types and themes in one ad group:** Different match types deliver different intent — keep them separate. Same for different topics.
3. **Launching automated bidding without conversion history:** Target CPA needs 50+ conversions in 30 days. Start with Manual CPC + ECPC.
4. **Directing all ads to the homepage:** The landing page must match the ad's message. A generic homepage after a specific ad causes high bounce rates and low QS.
5. **No conversion tracking or broken tracking:** Without proper conversion tracking, all bidding optimization is flying blind. Verify tags fire correctly before launch.
6. **Pausing campaigns too early:** Give campaigns 7–14 days minimum before making major changes. Statistical learning needs data — especially for automated bidding.
7. **Ignoring mobile performance:** 60%+ of search clicks are on mobile. Test mobile landing pages, check mobile bid adjustments, use mobile-preferred ads.
8. **No audience layering (Meta/LinkedIn):** Broad targeting on social platforms wastes budget. Layer at least 2–3 targeting criteria for efficient spend.
9. **Over-using broad match:** Broad match without smart bidding and a strong negative list burns budget. Use phrase and exact for new campaigns.
10. **Not using ad extensions (Google Ads):** Sitelinks, callouts, structured snippets, and call extensions improve CTR by 10–20%. Use every relevant extension.

## Verification Checklist

- [ ] Campaign structure follows proper hierarchy (Account → Campaign → Ad Group)
- [ ] Keywords organized by theme and match type (separate ad groups)
- [ ] Negative keyword strategy documented and search terms reviewed weekly
- [ ] Responsive Search Ads have 8+ headlines and 3+ descriptions
- [ ] Ad copy matches landing page (message match verified)
- [ ] Conversion tracking implemented and verified (all key conversion types)
- [ ] UTM parameters standardized across all platforms
- [ ] Landing pages mobile-friendly, < 2s load time, single CTA
- [ ] Bidding strategy appropriate for account maturity (conversion data volume)
- [ ] Budget allocation and pacing plan documented
- [ ] Quality Score baseline recorded for top 20 keywords
- [ ] Audience targeting strategy documented by platform
- [ ] A/B testing plan active (ad copy, landing page, audience tests scheduled)
- [ ] Ad extensions deployed (sitelinks, callouts, call, structured snippets)
- [ ] Account health scorecard passed (all green)
- [ ] Attribution model chosen and documented
- [ ] Pause/stop-loss rules defined (e.g., pause keywords when CPA > 2× target)
- [ ] Cross-platform performance dashboard configured
- [ ] Remarketing/retargeting lists set up (30-day, 90-day, specific page visitors)
