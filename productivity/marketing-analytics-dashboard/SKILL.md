---
name: marketing-analytics-dashboard
description: "Use when building marketing dashboards. KPIs, funnels."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [marketing, analytics, dashboard, kpi, metrics, reporting]
    related_skills: [marketing-strategy-framework, conversion-rate-optimization, ppc-advertising]
---

# Marketing Analytics Dashboard

## Overview

A comprehensive marketing analytics and reporting methodology covering KPI selection by business type (e-commerce: CAC/LTV/AOV/ROAS, SaaS: MRR/churn/NPS/Net Revenue Retention, lead gen: MQL→SQL→SAL conversion rates), dashboard design principles (hierarchy, context, actionability), funnel visualization techniques, cohort analysis for retention and LTV modeling, attribution models (first-touch, last-touch, linear, time-decay, U-shaped, data-driven), and reporting cadence. This skill provides templates and decision frameworks for building performance marketing dashboards that drive data-informed decisions.

## When to Use

- Building a marketing analytics dashboard from scratch (any BI tool)
- Selecting the right KPIs for a specific business model (e-commerce, SaaS, lead gen, content)
- Setting up funnel and cohort analyses in GA4, Mixpanel, Amplitude, or similar
- Evaluating and choosing an attribution model
- Creating weekly/monthly executive marketing reports
- Auditing existing dashboards for actionability gaps
- Standardizing marketing metrics across teams and channels
- Setting up automated anomaly detection and alerting

## Body

### 1. KPI Selection by Business Type

#### 1.1 E-commerce / Retail

| KPI | Formula | Target | Benchmark | Frequency |
|---|---|---|---|---|
| **Revenue** | Total sales | ↑ MoM | Varies | Daily |
| **AOV (Avg. Order Value)** | Revenue / Orders | ↑ | $45–$150 (varies) | Weekly |
| **CAC (Customer Acq. Cost)** | Total Mktg Cost / New Customers | ↓ | < 30% of LTV | Monthly |
| **LTV (Lifetime Value)** | AOV × Avg. Purchase Frequency × Avg. Customer Lifespan | ↑ | 3× CAC min | Monthly |
| **LTV:CAC Ratio** | LTV / CAC | ↑ | 3:1 (healthy), 5:1+ (great) | Monthly |
| **ROAS (Return on Ad Spend)** | Revenue from Ads / Ad Spend | ↑ | 4:1+ | Weekly |
| **Conversion Rate (CVR)** | Orders / Sessions | ↑ | 2–5% | Weekly |
| **Cart Abandonment Rate** | (Carts Started - Completed) / Carts Started | ↓ | 70–75% (industry avg) | Weekly |
| **Gross Margin** | (Revenue - COGS) / Revenue | ↑ | 50%+ | Monthly |
| **Repeat Purchase Rate** | Customers with 2+ purchases / All Customers | ↑ | 25–40% | Monthly |
| **Customer Retention Rate** | Customers at end of period (excl. new) / Customers at start | ↑ | 60–80% (annual) | Monthly |
| **Net Promoter Score (NPS)** | % Promoters - % Detractors | ↑ | 30+ (good, -100 to 100 scale) | Quarterly |

**North Star Metric:** Orders per week (or Revenue per visitor)

#### 1.2 SaaS / Subscription

| KPI | Formula | Target | Benchmark | Frequency |
|---|---|---|---|---|
| **MRR (Monthly Recurring Revenue)** | Avg. Revenue per Account × Total Accounts | ↑ | Varies | Daily |
| **NRR (Net Revenue Retention)** | (Starting MRR + Expansion - Churn) / Starting MRR | ↑ | > 100% (best) / > 90% (good) | Monthly |
| **Churn Rate (Logo)** | Customers Lost / Total Customers | ↓ | < 5%/mo (SaaS avg: 5–7%) | Monthly |
| **Churn Rate (Revenue)** | MRR Churned / Total MRR | ↓ | < 2%/mo (good SaaS) | Monthly |
| **CAC (Customer Acq. Cost)** | Sales + Marketing Cost / New Customers | ↓ | < 1 year payback | Monthly |
| **LTV (Lifetime Value)** | ARPU / Monthly Churn Rate | ↑ | 3×+ CAC | Monthly |
| **ARPU (Avg. Rev. Per User)** | Total MRR / Total Customers | ↑ | Varies | Monthly |
| **Trial → Paid Conversion** | Trial Converted / Total Trials | ↑ | 15–25% | Weekly |
| **Time to First Value** | Time from signup to core action | ↓ | < 60 min (B2C), < 7 days (B2B) | Weekly |
| **Activation Rate** | Users who reached aha moment / Total Signups | ↑ | 30–60% | Weekly |
| **DAU/MAU Ratio** | Daily Active / Monthly Active Users | ↑ | 20%+ (good), 50%+ (great) | Daily |
| **NPS** | % Promoters - % Detractors | ↑ | 30+ (good) | Quarterly |
| **CAC Payback Period** | CAC / (ARPU × Gross Margin %) | ↓ | < 12 months | Monthly |

**North Star Metric:** Weekly Active Users (WAU) or Net Revenue Retention (NRR)

#### 1.3 Lead Generation / B2B

| KPI | Formula | Target | Benchmark | Frequency |
|---|---|---|---|---|
| **MQL (Marketing Qualified Lead)** | Number meeting lead score threshold | ↑ | 10–20% of total leads | Weekly |
| **SQL (Sales Qualified Lead)** | MQLs accepted by sales team | ↑ | 50–70% of MQLs | Weekly |
| **SAL (Sales Accepted Lead)** | SQLs that sales contacts | ↑ | 80–90% of SQLs | Weekly |
| **MQL → SQL Conversion Rate** | SQLs / MQLs | ↑ | 50–70% | Monthly |
| **SQL → Opportunity Rate** | Opportunities / SQLs | ↑ | 20–40% | Monthly |
| **Opportunity → Closed Won Rate** | Closed Won / Opportunities | ↑ | 20–30% (varies by industry) | Monthly |
| **MQL → Customer Conversion Rate** | New Customers / MQLs | ↑ | 5–15% | Monthly |
| **Cost per Lead (CPL)** | Total Mktg Cost / Total Leads | ↓ | Varies by industry | Weekly |
| **Cost per MQL** | Total Mktg Cost / MQLs | ↓ | Higher than CPL | Weekly |
| **Cost per SQL** | Total Mktg Cost / SQLs | ↓ | 3–5× CPL | Weekly |
| **CAC** | Total Sales + Mktg Cost / New Customers | ↓ | Varies | Monthly |
| **Lead-to-Customer Time** | Avg days from lead to close | ↓ | B2B: 30–90 days | Monthly |
| **Pipeline Velocity** | (Value × Win Rate × Deal Count) / Sales Cycle Length | ↑ | Varies | Monthly |

**North Star Metric:** Pipeline Generated ($) or SQLs per month

#### 1.4 Content / Media

| KPI | Formula | Target | Frequency |
|---|---|---|---|
| **Organic Sessions** | Total organic search traffic | ↑ MoM | Weekly |
| **New vs. Returning Visitors** | New users / Returning users | Balance depends on goals | Weekly |
| **Avg. Time on Page** | Total time / Pageviews | > 3 min | Weekly |
| **Bounce Rate** | Single-page sessions / Total sessions | < 55% (content sites) | Weekly |
| **Pages per Session** | Total pageviews / Sessions | > 2.5 | Weekly |
| **Email Subscriber Growth** | Net new subscribers / Total list | > 2% per month | Weekly |
| **Social Shares per Article** | Total social shares / Article | > 50 | Monthly |
| **Content-to-Lead Conversion** | Form fills from content / Total content visits | > 3% | Monthly |
| **Backlinks per Article** | New backlinks / Article published | > 5 | Monthly |
| **Newsletter CTR** | Clicks / Opens | 10–30% | Weekly |
| **Ad Revenue (if monetized)** | RPM × Traffic | ↑ | Monthly |

### 2. Dashboard Design Principles

#### 2.1 Dashboard Hierarchy

```
Level 1: Executive Summary (1 page)
├── North Star Metric (big number + trend)
├── 4–6 Tier 1 KPIs (revenue, new customers, avg CVR, CAC)
├── Last 30 days trend line (or comparison vs. prior period)
└── Top 3 alerts / highlights

Level 2: Channel Performance (1 page per channel)
├── Channel-specific KPIs (e.g., SEO: organic traffic, keyword rankings)
├── Performance vs. budget
├── Trend: last 90 days
└── Top/bottom performers (campaigns, keywords, content)

Level 3: Deep Dive (ad hoc / weekly review)
├── Funnel analysis (stage-by-stage drop-off)
├── Cohort analysis (retention, LTV)
├── Segmentation analysis (by device, source, geography, persona)
└── Attribution model comparison
```

#### 2.2 Dashboard Design Rules

| Rule | Explanation | Example |
|---|---|---|
| **One metric per chart** | Don't overload a single visualization | Revenue as bar, CVR as line OVER the bar = confusing |
| **Context always** | A number alone is meaningless | "3.2% CVR" vs "3.2% CVR (+0.4% vs last month, -0.8% vs target)" |
| **Compare to benchmark** | Current vs. prior period vs. target vs. industry | Show all three comparisons |
| **Smallest meaningful time unit** | Don't show daily data for monthly KPIs | Churn rate: monthly view, not daily |
| **Start axes at zero** | Avoid misleading visual scaling | Bar chart with Y-axis starting at 0 |
| **Color meaning** | Consistent color for same metric across pages | Revenue always in green, always on left column |
| **Limit to 5–7 KPIs per page** | Cognitive load maximum per view | Above that = information overload |
| **Mobile view** | Dashboards viewed on phones? | Key numbers first, scrollable |

#### 2.3 Dashboard Types by Audience

| Audience | Frequency | Content | Tool | Best Format |
|---|---|---|---|---|
| **Executive / CEO** | Monthly | North Star, Revenue, CAC, LTV, NPS, Market Share | Looker, Tableau, PPT | 5 KPIs, big numbers, trend arrows |
| **Marketing Director** | Weekly | Full Tier 1 KPIs, channel performance, budget vs. actual, pipeline | Looker, Metabase, Google Data Studio | 1-page summary + 3 detail tabs |
| **Channel Owner (SEO, Paid, Content)** | Daily/Weekly | Channel-specific KPIs, top/bottom performers, test results | GA4, native platform dashboards | Focused, action-oriented |
| **Finance / Ops** | Monthly | CAC, LTV, ROAS, Budget vs. Actual, Attribution | Looker, Excel, Tableau | Numbers-focused, drill-down |

### 3. Funnel Visualization

#### 3.1 Marketing Funnel Stages

```
┌─────────────────────────────────┐
│       AWARENESS (Reach)         │
│   Visitors, Impressions, Reach  │
├─────────────────────────────────┤
│       INTEREST (Traffic)        │
│   Page views, Sessions, Clicks  │
├─────────────────────────────────┤
│     CONSIDERATION (Engage)      │
│   Time on site, Pages/session   │
├─────────────────────────────────┤
│       INTENT (Leads)            │
│   Form fills, Email signups     │
├─────────────────────────────────┤
│       PURCHASE (Conversion)     │
│   Sales, Subscriptions, Deals   │
├─────────────────────────────────┤
│      RETENTION (Loyalty)        │
│   Repeat purchases, Retention   │
├─────────────────────────────────┤
│      ADVOCACY (Referral)        │
│   NPS, Referrals, Reviews       │
└─────────────────────────────────┘
```

#### 3.2 Funnel CVR by Channel

| Channel | Awareness → Visit | Visit → Lead | Lead → Sale | Overall CVR |
|---|---|---|---|---|
| Organic Search | 100% (already visit) | 3–7% | 5–15% | 0.15–1.05% |
| Paid Search | 100% | 4–10% | 5–15% | 0.2–1.5% |
| Social Organic | 100% | 1–3% | 3–10% | 0.03–0.3% |
| Social Paid | 100% | 2–5% | 3–10% | 0.06–0.5% |
| Email | 100% | 5–15% | 10–20% | 0.5–3.0% |
| Referral | 100% | 5–12% | 10–20% | 0.5–2.4% |
| Direct | 100% | 3–8% | 10–20% | 0.3–1.6% |

#### 3.3 Funnel Visualization Template

```
                    ┌──────────────────────────────────────────────┐
                    │     ALL VISITORS: 100,000                    │
                    │     ──────────────────────                   │
                    │     ┌─────┐ ┌─────┐ ┌─────┐                │
                    │     │Org  │ │Paid │ │Social│                │
                    │     │45%  │ │25%  │ │15%  │                │
                    │     └─────┘ └─────┘ └─────┘                │
                    └──────────────────────────────────────────────┘
                                       │
                                       ▼
                    ╔══════════════════════════════════════════╗
                    ║   ENGAGED VISITORS: 45,000 (45%)        ║
                    ║   (≥ 30s on site, > 50% scroll)         ║
                    ╚══════════════════════════════════════════╝
                                       │
                                       ▼
                    ╔══════════════════════════════════════════╗
                    ║   LEADS: 3,000 (3% of all visitors)     ║
                    ║   (form fills, email signups, downloads) ║
                    ║   CPL: $25                               ║
                    ╚══════════════════════════════════════════╝
                                       │
                                       ▼
                    ╔══════════════════════════════════════════╗
                    ║   MQLs: 1,500 (50% of leads)            ║
                    ║   Cost per MQL: $50                      ║
                    ╚══════════════════════════════════════════╝
                                       │
                                       ▼
                    ╔══════════════════════════════════════════╗
                    ║   SQLs: 750 (50% of MQLs)               ║
                    ║   Cost per SQL: $100                     ║
                    ╚══════════════════════════════════════════╝
                                       │
                                       ▼
                    ╔══════════════════════════════════════════╗
                    ║   OPPORTUNITIES: 300 (40% of SQLs)      ║
                    ║   Pipeline Value: $450,000               ║
                    ╚══════════════════════════════════════════╝
                                       │
                                       ▼
                    ╔══════════════════════════════════════════╗
                    ║   CLOSED WON: 90 (30% of opportunities) ║
                    ║   Revenue: $180,000                      ║
                    ║   CAC: $500                              ║
                    ╚══════════════════════════════════════════╝
```

### 4. Cohort Analysis

#### 4.1 Retention Cohort Table

| Acquisition Month | Month 0 | Month 1 | Month 2 | Month 3 | Month 6 | Month 12 |
|---|---|---|---|---|---|---|
| Jan 2025 | 100% | 45% | 38% | 32% | 25% | 18% |
| Feb 2025 | 100% | 48% | 40% | 34% | 27% | — |
| Mar 2025 | 100% | 42% | 35% | 30% | — | — |
| Apr 2025 | 100% | 47% | 39% | — | — | — |
| May 2025 | 100% | 44% | — | — | — | — |

**Insights from this cohort table:**
- Month 1 retention (42–48%) is stable — check onboarding flow for consistency
- Month 2→3 drop (32–34%) is a key inflection point — investigate what happens between months 2–3
- 12-month retention (18%) needs improvement — target 25%+

#### 4.2 Revenue / LTV Cohort

| Acquisition Month | M0 | M1 | M2 | M3 | M6 | M12 | Cumulative LTV |
|---|---|---|---|---|---|---|---|
| Jan 2025 | $0 | $15 | $12 | $10 | $35 | $75 | $147 |
| Feb 2025 | $0 | $18 | $14 | $11 | $38 | — | — |
| Mar 2025 | $0 | $13 | $11 | $9 | — | — | — |

**LTV projection formula (for incomplete cohorts):**
```
Projected LTV = (Cumulative Revenue to Date) / (Retention Rate to Date × Expected Annual Retention)
```

#### 4.3 Behavior Cohort Analysis

Group users not by acquisition date, but by action date:

| First Purchase Month | Avg. Days to 2nd Purchase | 2nd Purchase Rate | Avg Days to 3rd Purchase | 3rd Purchase Rate |
|---|---|---|---|---|
| Jan 2025 | 14 days | 35% | 30 days | 22% |
| Feb 2025 | 16 days | 33% | 28 days | 24% |
| Mar 2025 | 12 days | 38% | 26 days | 27% |

**Key insight:** If 2nd purchase rate improves over time (35% → 38%), recent changes to the post-purchase experience are working.

### 5. Attribution Models

#### 5.1 Model Comparison

| Model | How It Works | Best For | Limitations |
|---|---|---|---|
| **First Touch** | 100% credit to first interaction | Brand awareness campaigns | Ignores all nurturing and closing touchpoints |
| **Last Touch** | 100% credit to last interaction before conversion | Bottom-of-funnel optimization | Ignores top-of-funnel awareness and consideration |
| **Last Non-Direct Click** | 100% to last non-direct channel (default in GA) | General use (removes direct as default) | Still last-click bias |
| **Linear** | Equal credit to all touchpoints | Full-funnel understanding | No weighting for importance |
| **Time Decay** | More credit to touchpoints closer to conversion | Longer sales cycles (B2B) | May undervalue top-of-funnel |
| **U-Shaped (Position-Based)** | 40% to first, 40% to last, 20% split among middle | Balanced first + last touch | Still under-values middle touches |
| **W-Shaped** | 30% first, 30% middle (lead creation), 30% last, 10% split | Lead gen with clear stages | Complex, requires stage mapping |
| **Data-Driven (Algorithmic)** | ML model distributes credit based on actual influence | Large accounts (30K+ conversions/year) | Requires significant data, opaque logic |

#### 5.2 Attribution Model Selection by Business Type

| Business | Recommended Model | Rationale |
|---|---|---|
| E-commerce (short cycle) | Last Non-Direct Click + Data-Driven | Short consideration window; last click correlates well |
| B2B SaaS (long cycle) | Time Decay or U-Shaped | Sales cycle spans weeks/months; multiple touches matter |
| Lead Gen B2B | W-Shaped or U-Shaped | Clear stages (lead → MQL → close) need stage-based credit |
| Content / Media | First Touch or Linear | Content contributes mostly at the awareness stage |
| Low-volume B2B | Last Touch or Time Decay | Insufficient data for data-driven models |
| High-volume E-com | Data-Driven | Enough data to train ML attribution model |

#### 5.3 Attribution Comparison Dashboard

```
CHANNEL ATTRIBUTION COMPARISON
┌─────────────┬──────────┬──────────┬──────────┬──────────┐
│ Channel     │ First    │ Last     │ Linear   │ Data     │
│             │ Touch    │ Touch    │          │ Driven   │
├─────────────┼──────────┼──────────┼──────────┼──────────┤
│ Organic     │ 45%      │ 20%      │ 32%      │ 30%      │
│ Paid Search │ 20%      │ 35%      │ 28%      │ 31%      │
│ Social      │ 15%      │ 8%       │ 12%      │ 11%      │
│ Email       │ 5%       │ 22%      │ 14%      │ 16%      │
│ Direct      │ 10%      │ 12%      │ 10%      │ 9%       │
│ Referral    │ 5%       │ 3%       │ 4%       │ 3%       │
└─────────────┴──────────┴──────────┴──────────┴──────────┘

IF first-touch dominated → Brand/awareness channels over-attributed
IF last-touch dominated → Conversion/nurture channels over-attributed
Data-Driven is most accurate (if data volume sufficient)
```

### 6. Reporting Cadence & Templates

#### 6.1 Reporting Calendar

| Report Type | Audience | Format | Frequency | Time Required |
|---|---|---|---|---|
| **Daily Snapshot** | Channel owners | Dashboard (auto-update) | Daily | 5 min review |
| **Weekly Performance** | Marketing team | Slide deck / doc | Monday AM | 30 min prep |
| **Monthly Executive** | CEO, leadership | PPT + dashboard | Month + 5 days | 2 hours prep |
| **Quarterly Review** | Board / investors | PPT + narrative | Quarter + 2 weeks | 1 day prep |
| **Campaign Post-Mortem** | Marketing team | Single page / doc | After each campaign | 1–4 hours |
| **Annual Marketing Review** | Company-wide | Presentation | January | 3–5 days |

#### 6.2 Weekly Marketing Report Template

```
# Weekly Marketing Report — [Date] to [Date]

## Executive Summary
- Revenue: $XXX,XXX (+X% vs prior week, X% vs target) 
- New Customers: XXX (+X%)
- Avg. CAC: $XXX (X% vs target)
- Top Highlight: [What went well]
- Top Flag: [What needs attention]

## Channel Performance

### Organic Search
- Visits: XX,XXX (+X%)
- Leads: XXX (+X%)
- Conversion Rate: X.XX%
- Top Pages: [Page 1], [Page 2]
- Notes: [Any keyword movements, algo changes]

### Paid Search
- Spend: $X,XXX (+X%)
- Clicks: XXX (+X%)
- CVR: X.XX% (+X%)
- CPA: $XXX (+X%)
- Top Campaigns: [Campaign 1], [Campaign 2]

### Email
- Sent: XX,XXX
- Open Rate: XX.X% (+X% vs benchmark)
- CTR: X.XX% (+X% vs benchmark)
- Unsubscribes: XX (X.XX%)
- Top Sends: [Campaign 1], [Campaign 2]

## Pipeline (B2B)
- New MQLs: XXX 
- New SQLs: XXX
- Opportunities Created: XX ($XX,XXX)
- Closed Won: XX ($XX,XXX)

## Tests in Flight
- [Test 1]: Running since [date], results so far: X
- [Test 2]: Scheduled to launch [date]

## Action Items
- [ ] [Action] — Owner — Due date
- [ ] [Action] — Owner — Due date
```

#### 6.3 Monthly Executive Dashboard Template

```
# Monthly Marketing Dashboard — [Month Year]

## North Star
**Orders per Week (Ecom)** or **SQLs/Month (B2B)** or **NRR (SaaS)**
Current: X,XXX | Prior Month: X,XXX | Target: X,XXX | Status: ✅ / ⚠️ / ❌

## Revenue & Growth
| Metric | Current | Prior Mo | MoM | Target | Status |
|--------|---------|----------|-----|--------|--------|
| Total Revenue | $X | $X | +X% | $X | ✅ |
| New Customers | X | X | +X% | X | ✅ |
| Avg. CAC | $X | $X | -X% | $X | ✅ |
| LTV:CAC | X:1 | X:1 | +X | 3:1 | ⚠️ |
| Gross Margin | X% | X% | +X% | X% | ✅ |

## Channel Breakdown
| Channel | Spend | Leads/Conversions | CPA/CVR | ROAS | MoM Change |
|---------|-------|-------------------|---------|------|------------|
| Organic | $0 | X | X% | N/A | +X% |
| Paid Search | $X | X | $X | X:1 | +X% |
| Social Paid | $X | X | $X | X:1 | -X% |
| Email | $X | X | $X | X:1 | +X% |
| **Total** | **$X** | **X** | **$X** | **X:1** | |

## Key Highlights
1. [Positive outcome with specific data]
2. [Positive outcome with specific data]
3. [Area of concern with specific data]

## Recommendations for Next Month
1. [Actionable recommendation]
2. [Actionable recommendation]
3. [Actionable recommendation]
```

### 7. Anomaly Detection & Alerting

#### 7.1 Alert Triggers

| Metric | Trigger | Action |
|---|---|---|
| Traffic | Drop > 20% in 24h | Check: tracking code, site availability, SERP position, algo update |
| Conversion Rate | Drop > 15% in 7 days | Check: landing page changes, checkout flow, form errors, technical issues |
| CPA | Increase > 30% in 7 days | Check: competitor activity, audience fatigue, bid changes, landing page |
| Bounce Rate | Increase > 15% in 24h | Check: page load speed, mobile rendering, content changes, traffic source |
| Cart Abandonment | Increase > 10% in 7 days | Check: checkout flow, shipping costs, payment gateway errors |
| Spend | Daily spend > 120% of budget | Check: bid strategy, budgets, broad match expansion |

#### 7.2 Alert Severity Levels

| Level | Response Time | Example |
|---|---|---|
| **Critical** (P0) | < 1 hour | Tracking code broken, site down, payment gateway down |
| **High** (P1) | < 4 hours | CPA spike > 50%, traffic drop > 50%, conversion drop > 25% |
| **Medium** (P2) | < 24 hours | Gradual CPA increase, minor traffic dip, budget pacing off |
| **Low** (P3) | < 1 week | Low-quality score on non-critical terms, minor metric drift |

## Common Pitfalls

1. **Vanity metrics over actionable KPIs:** Impressions, page views, and social likes feel good but don't drive decisions. Focus on metrics that lead to action: CAC, CVR, churn, pipeline velocity.
2. **Too many KPIs on one dashboard:** A dashboard with 50+ metrics is a report, not a dashboard. Limit to 5–7 KPIs per page and drill down for detail.
3. **No context or benchmarks:** "3,412 conversions" is noise. "3,412 conversions (+12% MoM, -5% vs target)" is a signal. Always include comparison periods and targets.
4. **Ignoring data quality:** Bad tracking in = bad decisions out. Verify UTM parameters, conversion tags, and integration points monthly.
5. **Attributing everything to the last click:** Last-click attribution over-values bottom-of-funnel channels and under-values brand-building. Use multi-touch or data-driven models.
6. **Mixed cohort comparisons:** Comparing different acquisition cohorts (e.g., social vs. email) without segmentation masks real performance differences. Always segment cohorts by source.
7. **No alerting system:** Dashboards that nobody checks daily are useless. Set up automated alerts for critical metric changes.
8. **Data silos:** Marketing data in GA4, ad platform data in their native dashboards, revenue data in the CRM — building a dashboard that connects them is essential for full-funnel visibility.
9. **Over-reliance on platform attribution:** Google and Meta's in-platform attribution over-attribute themselves. Use a third-party attribution tool or a statistical model for unbiased measurement.
10. **Not reviewing and updating dashboards:** Business models change, new channels emerge, old KPIs become irrelevant. Review dashboard structure quarterly.

## Verification Checklist

- [ ] North Star Metric defined and aligned with business goals
- [ ] Tier 1 KPIs selected (5–7 max) matching business type (ecom/SaaS/lead gen/content)
- [ ] Tier 2/3 KPIs defined for drill-down analyses
- [ ] Dashboard hierarchy designed (Executive → Channel → Deep Dive)
- [ ] Context/comparison logic built into every KPI visualization
- [ ] Funnel visualization built with stage-by-stage conversion rates
- [ ] Cohort analysis configured (retention cohorts and/or revenue cohorts)
- [ ] Attribution model selected and documented (with justification)
- [ ] Attribution comparison dashboard built (first/last/linear/data-driven)
- [ ] Data quality audit completed (UTM consistency, conversion tracking)
- [ ] Reporting calendar defined (daily/weekly/monthly/quarterly)
- [ ] Weekly report template finalized and automated where possible
- [ ] Monthly executive dashboard built in BI tool
- [ ] Automated alerts configured for critical and high-severity triggers
- [ ] Dashboard reviewed with stakeholders for actionability feedback
- [ ] Data sources connected and verified (GA4, ad platforms, CRM, payment)
- [ ] Access controls and permissions set (who sees what)
- [ ] Dashboard refresh schedule set (real-time, hourly, daily)
- [ ] CCPA/GDPR compliance: no PII in dashboards
- [ ] Mobile-friendly dashboard view tested