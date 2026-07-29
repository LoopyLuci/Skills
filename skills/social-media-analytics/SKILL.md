---
name: social-media-analytics
description: "Use when analyzing social media performance data."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [social-media, analytics, metrics, reporting, kpi]
    related_skills: [social-media-strategy, social-media-content-calendar]
---

# Social Media Analytics & Reporting

## Overview

A structured methodology for analyzing social media performance across platforms. Covers engagement rate vs benchmarks, reach/follower ratio, best-performing content pattern identification, audience growth analysis, sentiment analysis, and data-driven recommendations. Produces actionable reports that connect metrics to business outcomes.

## When to Use

- **Monthly/quarterly reporting** — stakeholder or client performance reviews
- **Content audit** — identifying what's working and what to stop
- **Strategy pivots** — data-driven decisions on platform investment, content mix, and budget
- **Competitive benchmarking** — comparing performance against peers
- **Campaign post-mortem** — measuring effectiveness of specific campaigns
- **ROI analysis** — connecting social metrics to business results

## Body

### Part 1: Data Collection

#### 1.1 Where to Get Data

| Platform | Native Analytics | Schedule |
|---|---|---|
| LinkedIn | LinkedIn Analytics (creator mode) | Weekly |
| Instagram | Insights (business/creator account) | Weekly |
| TikTok | TikTok Analytics (pro account) | Weekly |
| X/Twitter | X Analytics | Weekly |
| YouTube | YouTube Studio Analytics | Weekly |
| Facebook | Meta Business Suite | Weekly |

**Tooling:** Google Data Studio / Looker Studio (multi-platform dashboards), Sprout Social / Hootsuite Analytics / Later (cross-platform), Brand24 / Brandwatch (sentiment), Excel / Google Sheets (custom tracking).

### Part 2: Core Metrics Framework

#### 2.1 Metric Definitions

**Reach & Awareness:**
| Metric | Definition | Benchmark |
|---|---|---|
| Impressions | Total times content was displayed | ≥50K/mo (small), ≥5M (large) |
| Reach | Unique users who saw content | 40–70% of impressions |
| Follower growth rate | (New / total followers) × 100 | 2–5%/mo (good), 10%+ (excellent) |
| Share of voice | Brand mentions / industry mentions × 100 | ≥10% (strong) |
| Viral coefficient | Shares / impressions × 100 | ≥1% (viral) |

**Engagement:**
| Metric | Definition | Benchmark |
|---|---|---|
| Engagement rate | (Likes+comments+shares+saves) / impressions × 100 | 1–3% (good), 5%+ (excellent) |
| Save rate | Saves / impressions × 100 | ≥1% (good), ≥3% (excellent) |
| Share rate | Shares / impressions × 100 | ≥0.5% (good), ≥2% (excellent) |
| CTR | Link clicks / impressions × 100 | 1–3% (standard), 5%+ (strong) |

**Conversion:**
| Metric | Benchmark |
|---|---|
| Conversion rate | 2–5% (B2B), 5–10% (B2C) |
| CPC | $0.20–$5 (varies by platform) |
| CPL | $5–$200 (varies by industry) |
| ROAS | 3×+ (good), 5×+ (excellent) |

#### 2.2 Platform-Specific Benchmarks

| Platform | Avg ER | Best Format |
|---|---|---|
| LinkedIn | 1.5–3.5% | PDF carousels, document posts |
| Instagram | 0.5–2% (feed), 1–4% (Reels) | Reels, carousels |
| TikTok | 3–9% | Trending sounds, educational |
| X/Twitter | 0.5–2% | Threads, visual tweets |
| YouTube | 4–8% (Shorts), 2–5% (long-form) | How-to, reviews |
| Facebook | 0.1–0.5% | Video, link posts |

### Part 3: Analysis Framework

#### 3.1 Step 1 — Aggregate + Clean Data

```markdown
## Monthly Data Summary: [Month] [Year]

| Metric | Platform A | Platform B | Total |
|---|---|---|---|
| Total Posts | 20 | 25 | 45 |
| Total Impressions | 50,000 | 80,000 | 130,000 |
| Avg Engagement Rate | 3.0% | 4.0% | 3.6% |
| Follower Growth | +250 | +400 | +650 |
| Link Clicks | 500 | 200 | 700 |
| Conversions | 25 | 10 | 35 |
| Estimated Value | $5,000 | $2,000 | $7,000 |
```

#### 3.2 Step 2 — Content Pattern Analysis

```markdown
## Best Performing (Top 5 by ER)

| Post | Platform | Format | Topic | ER | Saves | Shares |
|---|---|---|---|---|---|---|
| [Link] | LinkedIn | Carousel | "5 Strategies" | 6.2% | 120 | 45 |
| [Link] | TikTok | Educational | "How to [X]" | 11.4% | 890 | 230 |
| [Link] | Instagram | Reel | "POV" | 5.1% | 450 | 180 |

**Patterns:**
→ Carousels outperform single images 3:1 on LinkedIn
→ Educational content gets 2× more saves than entertainment
→ Thread hooks with data outperform opinion hooks 60:40
```

#### 3.3 Step 3 — Audience Growth Analysis

```markdown
| Platform | Start | End | Growth | Rate | Top Source |
|---|---|---|---|---|---|
| LinkedIn | 2,000 | 2,250 | +250 | 12.5% | Carousels |
| Instagram | 5,000 | 5,400 | +400 | 8.0% | Reels, Explore |
| TikTok | 8,000 | 8,600 | +600 | 7.5% | FYP, trending audio |
| X/Twitter | 3,000 | 3,150 | +150 | 5.0% | Threads + replies |
```

#### 3.4 Step 4 — Sentiment Analysis

```markdown
| Platform | Positive | Neutral | Negative | Net Sentiment | Top Keywords |
|---|---|---|---|---|---|
| LinkedIn | 72% | 25% | 3% | +69 | "helpful", "bookmarked" |
| Instagram | 68% | 28% | 4% | +64 | "needed this", "saved" |
| TikTok | 80% | 16% | 4% | +76 | "facts", "finally" |

**Drivers:** Positive = educational carousels, relatable humor. Negative = promotional posts.
```

#### 3.5 Step 5 — Recommendations

```markdown
### Keep Doing (Double Down)
1. [Activity] driving [metric]. Increase from X to Y/week.

### Stop Doing (Cut)
1. [Activity] at 0.2% engagement. Remove from rotation.

### Test (Experiment)
1. [New format] — hypothesis based on [observation].
2. [New angle] — data suggests untapped segment.

### Forecast
- At current trajectory: [number]. With recommendations: [number].
- Risks: [algorithm changes, seasonal dips, competitive moves]
```

### Part 4: Reporting Templates

#### 4.1 Quick Weekly Dashboard

```markdown
## Weekly Snapshot: [Date Range]

| Platform | Posts | Impressions | ER | Followers | Top Post |
|---|---|---|---|---|---|
| LinkedIn | 5 | 12K | 3.4% | +80 | [Link] |
| Instagram | 7 | 25K | 2.1% | +150 | [Link] |
| TikTok | 10 | 60K | 7.2% | +200 | [Link] |

⚠️ **Flag:** TikTok engagement dropped 40% on Wednesday. Cause: news cycle.
🎯 **Win:** LinkedIn carousel reached 8K — highest all month.
📌 **Action:** Increase carousel output to 2x/week.
```

#### 4.2 Monthly Executive Report (1-Page)

```markdown
# [Brand] Social Report: [Month] [Year]

**Executive Summary:** Overall [up/down/flat]. Key driver: [win]. Key risk: [concern].

**Headline Numbers:**
- Total reach: [number] (+/-%)
- Avg engagement rate: [%] (+/- bps)
- Follower growth: [+/-] (+/-%)
- Total conversions: [+/-] (+/-%)
- Estimated value: [$] (impressions × CPM)

**Top 3 Wins:** [1. Win with metric, 2. Win with metric, 3. Win with metric]
**Top 3 Opportunities:** [1. Opportunity with plan, 2. Opportunity with plan, 3. Opportunity with plan]
**Next Month Focus:** [Single priority]
```

### Part 5: Competitive Benchmarking

```markdown
| Brand | Followers | Growth Rate | ER | Top Format | Share of Voice |
|---|---|---|---|---|---|
| Us | 15,000 | 8% | 3.5% | Carousels | 15% |
| Competitor A | 22,000 | 3% | 2.1% | Video | 22% |
| Competitor B | 8,000 | 12% | 4.2% | Threads | 8% |

**Gaps:** Competitor B growing faster from daily threads + community replies.
**Opportunity:** No competitors use carousels effectively — ownership potential.
```

## Common Pitfalls

- **Vanity metrics**: Likes and followers don't pay bills. Tie metrics to outcomes.
- **Wrong benchmarks**: 5% ER on TikTok is average; 5% on Facebook is exceptional.
- **Ignoring sample size**: One viral post skews averages. Report median + range.
- **No context**: "Impressions down 10%" is meaningless without knowing why.
- **Data without insight**: A 50-page report with every metric is noise. Lead with 3–5 actions.
- **No recommendations**: Data without "what to do next" is academic.
- **Not tracking trends**: Single-month snapshots are misleading. Use rolling 3-month trends.
- **Attribution errors**: Last-click attribution on social is usually wrong. Use multi-touch.

## Verification Checklist

- [ ] Data collected from all active platforms (native analytics exports)
- [ ] Core metrics calculated: impressions, reach, engagement rate, save rate, CTR
- [ ] Platform-specific benchmarks referenced for rate interpretation
- [ ] Top 5 and bottom 5 performing posts identified with pattern analysis
- [ ] Follower growth rate calculated with attribution analysis
- [ ] Sentiment analysis completed (positive/neutral/negative)
- [ ] Competitive benchmarks (3+ competitors) collected
- [ ] Recommendations written (keep / stop / test)
- [ ] Weekly dashboard or monthly executive report created
- [ ] Period-over-period comparison included (MoM or QoQ)
- [ ] Recommendations prioritized by expected impact
- [ ] Stakeholder review scheduled with top 3 insights highlighted