---
name: blog-analytics-interpreter
description: "Use when interpreting blog analytics. Traffic insights."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [blog, analytics, traffic, metrics, growth]
    related_skills: [blog-seo-post-optimizer, blog-publishing-workflow, content-repurposing]
---

# Blog Analytics Interpreter

## Overview

A deep-dive framework for understanding blog analytics. Covers traffic source analysis, content ranking (pageviews, time on page, bounce rate), conversion tracking, trend analysis (month-over-month, seasonal), subscriber growth, top exit pages, and data-driven recommendations. Move beyond vanity metrics to actionable insights.

## When to Use

- You're reviewing weekly or monthly blog performance
- Traffic dropped or spiked and you need to understand why
- You're preparing a content performance report for stakeholders
- You're deciding which content types to invest more in
- You're optimizing the blog for conversions (leads, sales, subscribers)

## Data Sources

| Source | Best For | Key Metrics |
|--------|----------|-------------|
| Google Analytics 4 | Full traffic analysis | Users, sessions, bounce, conversions |
| Google Search Console | Search performance | Impressions, clicks, avg position, CTR |
| Ahrefs / Semrush | Competitive analysis | Organic traffic, keyword rankings, backlinks |
| CMS-built-in (Ghost, WordPress, etc.) | Quick site-level stats | Pageviews, referrers, top posts |
| Social platform analytics | Channel-specific | Reach, engagement, link clicks |
| Email analytics (ConvertKit, Mailchimp) | Newsletter traffic | Opens, clicks, subscribers gained |
| Hotjar / Microsoft Clarity | User behavior | Heatmaps, session recordings, rage clicks |

## Traffic Sources Analysis

### Source Categories

| Source | Definition | What It Tells You |
|--------|------------|--------------------|
| **Organic Search** | Traffic from Google/Bing/DuckDuckGo | SEO health, keyword ranking success |
| **Direct** | Typed URL, bookmarks, untagged links | Brand awareness, offline marketing impact |
| **Social** | Twitter, LinkedIn, Reddit, FB, etc. | Content resonance, platform strategy |
| **Referral** | Links from other sites | Backlink quality, guest posting, partnerships |
| **Email** | Newsletter, drip campaigns | List health, subject line effectiveness |
| **Paid** | Google Ads, social ads, sponsored content | ROI on ad spend, landing page quality |

### Analysis Questions

**Organic:**
- Which keywords drive the most impressions vs clicks? (GSC → Queries report)
- Is CTR above or below industry avg for the position? (Position 1 avg CTR ≈ 27%)
- Are you ranking for the right intent (informational vs commercial)?
- Any impressions growing without clicks? → Improve meta title/description

**Direct:**
- Did it spike on a specific date? Correlate with a podcast, PR, or event
- If direct is >40% of traffic, you may be misattributing other sources

**Social:**
- Which platform drives the most engaged traffic (not just clicks)?
- LinkedIn → high time-on-page for B2B; Twitter → high bounce rate, low time
- Pinterest → visual categories only (design, food, fashion, DIY)

**Referral:**
- Top referring domains → build relationships with those publishers
- Low-quality referrals (spam sites) → disavow or add `nofollow`
- Guest posts on high-authority domains → expect sustained referral traffic

**Email:**
- Click-through rate >3% is good, >5% is excellent
- Subject line A/B tests → correlate with open rates
- Segment by signup source (content upgrade vs homepage)

## Content-Level Performance Analysis

### Top Content Report

Run this analysis monthly for your top 20 posts.

**Metrics to Track (post-level):**
```
Post Title
Pageviews (unique)
Avg Time on Page
Bounce Rate
Entrances (how often it was the first page)
Exit Rate (% who left from this page)
Social Shares
Backlinks (Ahrefs/Semrush)
Search Impressions (GSC)
Search Avg Position (GSC)
Conversions (goal completions if tracked)
```

**Performance Tiers:**
| Tier | Criteria | Action |
|------|----------|--------|
| **Stars** | Top 10% across 3+ metrics | Promote heavily, repurpose, update quarterly |
| **Workhorses** | Consistent traffic, moderate engagement | Check for freshness, add internal links |
| **Sleepers** | High search impressions but low CTR | Improve meta title/description |
| **Leaky buckets** | High traffic but high bounce/exit | Improve content quality or internal linking |
| **Duds** | Low across the board | Audit for consolidation or deletion |

### Content Quality Signals

| Signal | Good | Warning | Bad |
|--------|------|---------|-----|
| Avg Time on Page | 3–7 min (informational), <2 min (list) | < 30s | 0–10s (bounce) |
| Bounce Rate | 40–60% (informational), < 30% (tutorial) | 60–80% | > 80% |
| Pages per Session | > 2.0 | 1.2–2.0 | < 1.2 |
| Scroll Depth | > 75% | 50–75% | < 50% |

## Conversion Tracking

### Key Conversions for Blogs

| Conversion Type | How to Track | Benchmark |
|----------------|-------------|-----------|
| **Email Subscribe** | GA4 Event or form tool | 2–5% of pageviews |
| **Product Purchase** | Ecommerce tracking | Depends on niche |
| **Content Download** | GA4 Event | 10–20% of relevant pageviews |
| **Demo/Consultation** | GA4 Event + CRM | 1–3% of relevant pageviews |
| **Affiliate Click** | GA4 Event or affiliate tool | 0.5–2% of pageviews |
| **Ad Click** | Ad network tracking | Depends on ad type |

### Conversion Funnel Analysis

```
Landing Page (100%) → Read Post (X%) → Click CTA (Y%) → Complete Conversion (Z%)
```

Track drop-off points:
- High traffic page but no conversions → CTA is weak, missing, or irrelevant
- Middle-of-funnel content doing all the converting while top-of-funnel pages get all the traffic → redistribute CTAs
- High email subscribes but low email engagement → lead quality or nurture sequence issue

## Trend Analysis

### Month-over-Month (MoM) Comparison

| Metric | Up MoM | Flat MoM | Down MoM |
|--------|--------|----------|----------|
| **Organic Traffic** | New content ranking, seasonal boost | Steady state | Algorithm update, lost rankings, seasonal dip |
| **Social Traffic** | Viral post, platform algorithm change | Consistent sharing | Reduced posting frequency, algorithm change |
| **Email Traffic** | Good send, list growth | Wash cycle | Fatigue, deliverability issue |
| **Subscriber Growth** | Effective lead magnets, viral post | Organic growth | No new offers, low posting cadence |

### Seasonal Adjustment

Use Google Analytics "Year-over-Year" (YoY) comparison to distinguish seasonal patterns from actual growth/decline.

**Formula:** `(This Month - Same Month Last Year) / Same Month Last Year × 100 = YoY Growth %`

**If all traffic is down 20% vs last month but up 15% YoY:**
- MoM drop is seasonal (e.g., holiday lull) — not a crisis
- Continue current strategy

**If all traffic is down 10% YoY from a stable baseline:**
- Investigate: Google algorithm update? Lost backlinks? Competitor gain? Content decay?

### Anomaly Detection

When you see a spike or drop:
1. Check dates — correlate with content publish dates, promotions, events
2. Check source — did one channel spike/drop while others are flat?
3. Isolate — is it one post or the whole site?
4. Google Search Console — did a specific keyword collapse or surge?
5. External factors — Google update, competitor move, seasonal event

## Subscriber Growth Analysis

### Key Metrics

| Metric | Good | Great | Excellent |
|--------|------|-------|-----------|
| New subscribers/week | 10–50 | 50–200 | 200+ |
| Churn rate (< monthly) | < 2% | < 1% | < 0.5% |
| Open rate | 20–30% | 30–40% | 40%+ |
| Click rate | 2–3% | 3–5% | 5%+ |
| Subscriber conversion rate (of blog visitors) | 1–3% | 3–5% | 5%+ |

### Top Growth Drivers

- **Content upgrades** (downloadable checklists, templates) convert 3–10x better than generic "subscribe" CTAs
- **Pop-ups with exit intent** add 5–15% more subscribers
- **Welcome sequences** reduce churn by 20–40%
- **Referral programs** are the highest-quality subscriber source

## Top Exit Pages Analysis

Find which pages users leave from most — especially pages that SHOULD keep users on site.

**Bad exit pages:**
- Post pages with content that should drive to a next post but doesn't
- "Thank you" or confirmation pages (expected — but optimize the path)
- Category/index pages (sign they didn't find what they wanted)

**Fix plans:**

| Exit Page Type | Fix |
|----------------|-----|
| Post with related posts section but no clicks | Improve related post suggestions, add "read next" in-content CTA |
| Category page with high exit | Add featured posts, better filtering, or dynamic content |
| Landing page with zero conversion | Redesign CTA, add scarcity/urgency |
| About page with high exit | Add a "start here" guide or popular posts section |

## Actionable Recommendations Generator

Based on your data, generate a prioritized action list:

```
Priority A (Do this week):
  - [Post X] has a 90% bounce rate: rewrite intro and add internal links
  - Organic traffic from [keyword Y] dropped 30%: refresh post with current data
  - [Post Z] is the top landing page but has 0 conversions: add an email CTA

Priority B (Do this month):
  - Start a FAQ schema implementation for top 5 informational posts
  - Build a content cluster around the top performing topic
  - A/B test meta titles for the 5 posts with highest impressions-to-click gap

Priority C (This quarter):
  - Review all posts older than 2 years — refresh, merge, or archive
  - Implement a content upgrade on the top 3 posts per month
  - Run a competitor content audit on their top 10 posts vs yours
```

## Reporting Template

### Monthly Report Structure
```
1. Executive Summary (3 bullet points)
2. Traffic Overview (MoM comparison table)
3. Top 10 Posts (ranked by pageviews)
4. Organic Search Performance (top 10 keywords, impressions, clicks, avg position)
5. Social Performance (per-platform breakdown)
6. Email Performance (opens, clicks, growth)
7. Conversion Funnel (traffic → subscribe → engage)
8. Key Takeaways & Recommendations
9. Next Month's Focus Areas
```

## Common Pitfalls

- **Vanity metrics:** Pageviews don't matter if they don't convert or retain
- **Not segmenting:** Blending all traffic obscures channel-specific issues
- **One-time analysis:** Analytics isn't a snapshot — monthly trends beat single-month numbers
- **No benchmarking:** "5,000 sessions" means nothing without comparison to last month, last year, or industry benchmarks
- **Ignoring search intent breakdown:** Informational traffic doesn't convert directly — need a lead magnet bridge
- **Setting up analytics wrong:** Without goal tracking, UTM parameters, and filtered internal traffic, the data is unreliable
- **Over-reacting to monthly fluctuations:** Small sample sizes produce noise — look at 3-month rolling averages

## Verification Checklist

- [ ] GA4 property configured with goal tracking for key conversions
- [ ] GSC property linked to GA4
- [ ] UTM parameters on all external links (social, email, guest posts)
- [ ] Internal IPs filtered out of analytics
- [ ] Monthly top-20 content report exported and reviewed
- [ ] Traffic sources analyzed (organic, direct, social, referral, email, paid)
- [ ] MoM AND YoY comparison checked
- [ ] Top exit pages identified and fix prioritized
- [ ] Subscriber growth rate and churn calculated
- [ ] 3–5 actionable recommendations generated and prioritized
- [ ] Monthly report ready for stakeholders