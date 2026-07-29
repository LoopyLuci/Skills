---
name: marketing-strategy-framework
description: "Use when building marketing strategy. SWOT, RACE, budgets."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [marketing, strategy, planning, go-to-market, growth]
    related_skills: [competitor-analysis, brand-identity-development, marketing-analytics-dashboard]
---

# Marketing Strategy Framework

## Overview

A comprehensive marketing strategy framework that covers the full lifecycle from research and positioning through channel selection, budgeting, execution planning, and measurement. This skill integrates the **RACE** (Reach → Act → Convert → Engage) and **AARRR** (Acquisition → Activation → Retention → Referral → Revenue) growth frameworks with classic strategic tools (SWOT, competitive analysis, value proposition design) to produce an actionable 90-day marketing plan with measurable KPIs.

## When to Use

- Launching a new product or service and need a go-to-market strategy
- Reviewing or overhauling an existing marketing plan
- Preparing a marketing budget and resource allocation proposal
- Building a pitch deck or business case for marketing investment
- Scaling from early traction to systematic growth
- Any quarterly/annual marketing planning cycle

## Body

### 1. Strategic Foundation (Weeks 1–2)

#### 1.1 SWOT Analysis

| Strengths (Internal, Helpful) | Weaknesses (Internal, Harmful) |
|---|---|
| Proprietary tech / IP | Limited brand awareness |
| Strong unit economics | Small team bandwidth |
| Loyal existing customers | No content library |
| Deep domain expertise | Low organic search presence |

| Opportunities (External, Helpful) | Threats (External, Harmful) |
|---|---|
| Untapped adjacent segments | Well-funded competitors |
| Regulatory tailwinds | Market saturation risk |
| Platform/ecosystem shifts | Changing privacy regulations |
| Growing TAM | Economic downturn exposure |

**How to run a SWOT workshop:**
1. Gather cross-functional stakeholders (product, sales, support, leadership).
2. Use a shared doc / whiteboard — one column per quadrant.
3. Set a timer: 15 min per quadrant. Quantity over quality first.
4. Cluster related items, vote on top 3 per quadrant.
5. Convert weaknesses into risk-mitigation actions. Convert threats into contingency plans.

#### 1.2 Competitive Landscape

See also: [competitor-analysis](/skills/competitor-analysis)

Create a competitive map with 2 axes (e.g., Price vs. Features, Enterprise vs. SMB). Plot yourself and top 5 competitors. Identify whitespace.

| Competitor | Positioning | Strengths | Weaknesses | Our Advantage |
|---|---|---|---|---|
| Competitor A | Enterprise, premium | Brand, sales team | Slow innovation | Speed + price |
| Competitor B | Freemium, SMB | Virality, UX | No enterprise | Security + support |
| Competitor C | Mid-market | Integrations | Poor onboarding | Onboarding NPS |

#### 1.3 Target Audience Definition

Create 2–3 detailed buyer personas per market segment. Each persona includes:

- **Demographics:** Age, role, company size, industry, location
- **Psychographics:** Goals, fears, values, decision criteria
- **Behavioral:** Channels they use, content they consume, purchase triggers
- **Job-to-be-Done:** "When ___, I want ___, so I can ___."
- **Objections:** Price, switching cost, trust, implementation complexity

**Persona template:**

```
## Persona: [Name/Role]

**Demographics**
- Title:
- Company size:
- Industry:
- Budget authority:

**Goals**
- Primary:
- Secondary:

**Pain Points**
- #1:
- #2:
- #3:

**Information Sources**
- Blogs:
- Social:
- Events:
- Peers:

**Buying Triggers**
- Trigger event:
- Timeline:
- Evaluation criteria:

**Objections**
- Why they might say no:
```

#### 1.4 Value Proposition Design

Use the **Value Proposition Canvas**:

```
┌─────────────────────────────┐     ┌─────────────────────────────┐
│      Customer Profile        │     │      Value Map               │
│                              │     │                              │
│  Gains ────┐                │     │  ┌─── Gain Creators           │
│             │                │◄────┤  │                           │
│  Pains ────┤                │     │  │  Pain Relievers            │
│             │                │     │  │                           │
│  Jobs ─────┘                │     │  │  Products & Services       │
│                              │     │  └───────────────────────────│
└─────────────────────────────┘     └─────────────────────────────┘
```

**Fit criteria:** Your value proposition fits when Gain Creators match Customer Gains, Pain Relievers match Customer Pains, and Products & Services match Customer Jobs.

**Elevator Pitch Formula:**
> For [target audience] who [need], [product name] is a [category] that [key benefit]. Unlike [competitor], we [key differentiator].

### 2. Framework Selection: RACE + AARRR

#### 2.1 RACE Framework (Planning & Execution)

| Phase | Goal | Channels | Metrics |
|---|---|---|---|
| **Reach** | Build awareness & attract audience | SEO, Paid Ads, PR, Social, Content, Events | Impressions, Reach, Traffic, Share of Voice |
| **Act** | Convert visitors to leads/signups | Landing Pages, CTAs, Forms, Webinars | Conversion Rate, Leads, Signups, CPA |
| **Convert** | Turn leads into paying customers | Email Nurture, Sales Outreach, Trials, Demos | SQLs, Deals Closed, Revenue, CAC |
| **Engage** | Retain & grow existing customers | Email, Community, Support, Upsells | Churn Rate, LTV, NPS, Expansion Revenue |

#### 2.2 AARRR Framework (Growth Metrics)

| Stage | Description | Leading Indicator | Lagging Indicator |
|---|---|---|---|
| **Acquisition** | Users discover you | Traffic, Impressions | CAC, CPA |
| **Activation** | Users get first value | Time-to-Value, Activation Rate | % reached Aha moment |
| **Retention** | Users come back | DAU/MAU, Session Frequency | Churn Rate, Retention Curve |
| **Referral** | Users bring others | Viral Coefficient, Referral Rate | % of traffic from referrals |
| **Revenue** | Users pay you | MRR, ARPU | LTV, Gross Margin |

### 3. Channel Selection Matrix

Score each potential channel on 5 dimensions (1–5 scale):

| Channel | Audience Fit | Cost Efficiency | Scalability | Time to Impact | Expertise Required | **Total** |
|---|---|---|---|---|---|---|
| SEO / Content | 4 | 5 | 5 | 2 | 4 | 20 |
| Google Ads | 4 | 3 | 5 | 5 | 3 | 20 |
| LinkedIn Ads | 3 | 2 | 4 | 4 | 2 | 15 |
| Email Marketing | 5 | 5 | 5 | 3 | 3 | 21 |
| Events/Webinars | 4 | 3 | 2 | 1 | 4 | 14 |
| Influencer/PR | 3 | 2 | 3 | 2 | 3 | 13 |
| Direct Sales | 5 | 1 | 1 | 4 | 5 | 16 |
| Social Organic | 3 | 5 | 3 | 3 | 2 | 16 |

**Selection rules:**
- Top 2–3 channels get 70% of budget (core channels)
- Next 2 channels get 25% (test channels)
- Remainder for experimental (5%)
- Re-score quarterly

### 4. Budget Allocation Model

#### 4.1 Zero-Based Budgeting Template

| Line Item | Monthly | Quarterly | Annual | % of Total |
|---|---|---|---|---|
| Paid Media (Ads) | $X | $X | $X | 40% |
| Content Production | $X | $X | $X | 20% |
| Tools & Software | $X | $X | $X | 10% |
| Events & Sponsorships | $X | $X | $X | 10% |
| Agency/Freelancers | $X | $X | $X | 10% |
| Contingency (10%) | $X | $X | $X | 10% |
| **Total** | **$X** | **$X** | **$X** | **100%** |

#### 4.2 Budget by Funnel Stage

| Stage | Allocation | Rationale |
|---|---|---|
| Top of Funnel (Awareness) | 40% | Build pipeline volume |
| Middle of Funnel (Consideration) | 30% | Convert interest to leads |
| Bottom of Funnel (Conversion) | 20% | Close deals, reduce friction |
| Retention & Advocacy | 10% | Maximize LTV |

### 5. Content Strategy

Map content types to funnel stages and personas:

| Funnel Stage | Content Type | Format | Frequency |
|---|---|---|---|
| Awareness | Blog posts, infographics, social | Written, Visual | 2–3x/week |
| Consideration | Whitepapers, case studies, webinars | Long-form, Video | 1x/week |
| Decision | Product demos, free trials, ROI calc | Interactive | Always available |
| Retention | Knowledge base, community, newsletter | Multi-format | 1–2x/week |

See also: [content-marketing-workflow](/skills/content-marketing-workflow)

### 6. KPI Dashboard

#### 6.1 North Star Metric

Define one metric that captures the core value delivered to customers:

- **E-commerce:** Orders per week
- **SaaS:** Weekly active users (WAU)
- **Marketplace:** Transactions per month
- **Lead Gen:** Qualified opportunities created

#### 6.2 Tiered KPI Structure

| Tier | Focus | Example KPIs | Review Cadence |
|---|---|---|---|
| Tier 1 (Executive) | Business health | Revenue, CAC, LTV, Gross Margin | Monthly |
| Tier 2 (Tactical) | Channel performance | CPA, ROAS, Conversion Rate, MQLs | Weekly |
| Tier 3 (Operational) | Daily execution | CTR, Open Rate, CPC, Bounce Rate | Daily |

#### 6.3 KPI Definitions

| KPI | Formula | Target | Benchmark |
|---|---|---|---|
| CAC (Customer Acquisition Cost) | Total Sales & Marketing Cost / New Customers | < $X | Varies by industry |
| LTV (Lifetime Value) | ARPU × Gross Margin × Avg. Months Retained | > 3× CAC | 3:1 LTV:CAC |
| ROAS (Return on Ad Spend) | Revenue from Ads / Ad Spend | > 4:1 | 4:1 (good), 8:1 (great) |
| Conversion Rate | Conversions / Visitors | > 3% | 2–5% avg |
| Churn Rate | Customers Lost / Total Customers (monthly) | < 5% | 5–7% SaaS avg |
| NPS (Net Promoter Score) | % Promoters − % Detractors | > 50 | 30+ is good |

See also: [marketing-analytics-dashboard](/skills/marketing-analytics-dashboard)

### 7. 90-Day Action Plan

#### Month 1: Foundation & Quick Wins

| Week | Focus | Actions | Deliverables |
|---|---|---|---|
| W1 | Strategy Finalization | Complete SWOT, personas, channel matrix | Strategy doc signed off |
| W2 | Infrastructure | Set up analytics, tracking, CRM integration | Tracking audit, dashboards |
| W3 | Content Engine | Publish 4 cornerstone pieces, set up editorial calendar | 4 articles, calendar template |
| W4 | Paid Launch | Launch top 2 paid channels, set up A/B tests | Campaigns live, baseline data |

#### Month 2: Build Momentum

| Week | Focus | Actions | Deliverables |
|---|---|---|---|
| W5 | Optimization | Review ad performance, double down on winners | Optimized campaigns |
| W6 | Content Expansion | Launch newsletter, 2 guest posts, 1 webinar | Newsletter active, leads |
| W7 | Conversion | A/B test landing pages, improve onboarding flow | Higher CVR |
| W8 | Trust Building | Publish 2 case studies, update social proof | Case studies live |

#### Month 3: Scale & Systematize

| Week | Focus | Actions | Deliverables |
|---|---|---|---|
| W9 | Automation | Set up email nurture sequences, lead scoring | Email flows live |
| W10 | Channel Expansion | Launch 1 new channel (test budget) | Test data collected |
| W11 | Performance Review | Full KPI review, retro, re-forecast | Q2 plan draft |
| W12 | Planning | Q3 strategy, budget reallocation, OKRs | Q3 plan approved |

### 8. Risk & Contingency Planning

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Channel saturation / rising CPC | Medium | High | Diversify channels early |
| Low conversion rates | Medium | High | Systematic CRO program |
| Competitor launches | Medium | Medium | Monitor via alerts, have counter-positioning ready |
| Budget cuts | Low | High | Build ROI case, identify non-essential spend |
| Team bandwidth crunch | High | Medium | Prioritize ruthlessly, use freelancers for overflow |

## Common Pitfalls

1. **Strategy without execution plan:** A SWOT analysis without a 90-day action plan is just a document. Always pair analysis with concrete owner, timelines, and resources.
2. **Too many channels:** Spreading budget thin across 8+ channels dilutes impact. Focus on 2–3 core channels, master them, then expand.
3. **Vanity metrics over actionable KPIs:** Impressions and traffic feel good but don't drive decisions. Lead with CAC, LTV, ROAS, and Conversion Rate.
4. **Ignoring customer acquisition cost trends:** CAC creeping up is the first sign of channel saturation. Monitor monthly and set escalation triggers.
5. **One-size-fits-all personas:** Generic personas lead to generic messaging. Validate personas with real customer interviews, not just team assumptions.
6. **No budget contingency:** Marketing always faces unexpected costs (platform changes, competitive response, new tools). Always reserve 10%.
7. **Overlooking retention:** Acquiring customers is 5–7× more expensive than retaining them. Allocate at least 10% of budget and energy to retention programs.
8. **Static strategy:** A strategy written in month 1 should not be identical in month 3. Schedule a monthly "strategy pulse" to adjust based on data.

## Verification Checklist

- [ ] SWOT analysis complete with top 3 items per quadrant
- [ ] Competitive landscape mapped with 5+ competitors
- [ ] 2–3 detailed buyer personas created and validated
- [ ] Value proposition canvas filled out for each segment
- [ ] Channel selection matrix scored and top channels selected
- [ ] Budget allocation by channel and funnel stage defined
- [ ] North Star Metric and Tier 1/2/3 KPIs documented
- [ ] 90-day action plan with weekly milestones and owners
- [ ] Risk register with mitigation strategies
- [ ] All assumptions documented for testing
- [ ] Stakeholder sign-off on strategy document
- [ ] Tracking and analytics infrastructure verified
- [ ] Baseline KPI values recorded for future comparison
- [ ] Monthly strategy review cadence scheduled
