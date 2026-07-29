---
name: social-media-strategy
description: "Use when building a social media strategy doc."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [social-media, strategy, content-planning, marketing]
    related_skills: [social-media-content-calendar, social-media-analytics]
---

# Social Media Strategy Framework

## Overview

A comprehensive methodology for building a complete social media strategy from the ground up. This framework covers the **full lifecycle** — audit → goals → platform selection → content pillars → tone/voice → posting cadence → hashtag strategy → KPIs → reporting. Produces a shareable markdown strategy document that aligns stakeholders and guides execution for 3–12 months.

## When to Use

- **Launching a brand's social presence** from scratch (new company, rebrand, entering a new market)
- **Auditing and refreshing** a stale or underperforming existing strategy
- **Preparing a investor/pitch deck** social section or a client proposal
- **Quarterly or annual strategy review** — identifying what to keep, drop, or experiment with

## Body

### Phase 1: Audit & Competitive Analysis

Begin by capturing the current state and landscape. Run these diagnostics:

```bash
# Create the strategy doc
touch social_strategy_$(date +%Y%m%d).md
```

Include these audit sections in the doc:

**Internal Audit**
- Platform presence (which platforms, how many followers, last post date on each)
- Top 5 performing posts (by engagement rate) — identify patterns
- Bottom 5 performing posts — identify what to stop doing
- Current posting cadence (times/week per platform)
- Content mix breakdown: % educational / % promotional / % entertaining / % community
- Audience demographics (age, location, gender, device) from platform analytics

**Competitive Audit (3–5 competitors)**
- Their platform presence and follower counts
- Their posting cadence and content themes
- Their engagement rate benchmarks
- Gaps they're not filling — your opportunity space
- Their hashtag strategy (number of hashtags, branded vs generic)

### Phase 2: Goals & KPIs (SMART Framework)

Define objectives mapped to the marketing funnel:

| Funnel Stage | Goal Example | Primary KPI | Secondary KPI |
|---|---|---|---|
| Awareness | Reach 50K impressions/mo | Reach / Impressions | Follower growth rate |
| Consideration | Drive 10K link clicks/mo | CTR | Save rate |
| Conversion | Generate 200 leads/mo | Conversion rate | Cost per lead |
| Loyalty | Achieve 5% engagement rate | Engagement rate | Repeat interaction rate |
| Advocacy | 50 UGC posts/mo | Share of voice | Brand mention sentiment |

Write goals as:
- **Specific**: "Grow LinkedIn followers from 2K → 5K"
- **Measurable**: "achieve 4% average engagement rate on Instagram"
- **Achievable**: based on current growth trajectory × 1.5x
- **Relevant**: ties to business revenue or brand objectives
- **Time-bound**: "by Q3 2025"

### Phase 3: Platform Selection & Prioritization

Score each candidate platform:

```markdown
| Platform | Audience Fit (1-5) | Content Fit (1-5) | Resource Need (1-5) | Goal Alignment (1-5) | Total |
|---|---|---|---|---|---|
| LinkedIn | 5 | 4 | 3 | 5 | 17 |
| Instagram | 4 | 5 | 4 | 3 | 16 |
| TikTok | 3 | 3 | 5 | 2 | 13 |
| X/Twitter | 4 | 3 | 2 | 4 | 13 |
| YouTube | 5 | 4 | 5 | 5 | 19 |
| Facebook | 3 | 2 | 3 | 2 | 10 |
```

**Decision rules:**
- Total ≥ 16: Primary platform (daily posting, heavy investment)
- Total 12–15: Secondary (3–5x/week, moderate investment)
- Total < 12: Tertiary (repurpose content, low investment) or skip

**Platform-specific guidance:**
- **LinkedIn**: B2B, professional audiences, thought leadership, long-form posts, PDF carousels
- **Instagram**: Visual-first, storytelling, Reels-heavy, community via Stories + DMs
- **TikTok**: Short-form entertainment, trends-driven, raw/authentic, its own search ecosystem
- **X/Twitter**: Real-time conversation, news, threads, community building via replies
- **YouTube**: Long-form educational, search-driven (2nd largest search engine), evergreen
- **Facebook**: Older demographics, community groups, events, marketplace

### Phase 4: Content Pillars

Define 3–5 content pillars. Each needs:

```markdown
### Pillar N: [Name]
- **Purpose**: [educate / inspire / entertain / convert / community]
- **% of Content Mix**: [15–35%]
- **Format(s)**: [e.g., video, carousel, text post, infographic]
- **Topics**: [3–5 specific topic areas]
- **Example Headlines**: [3 examples]
- **Success Metric**: [e.g., saves, shares, clicks, comments]
```

**Recommended mix for most brands:**
- Educational/How-to: 30%
- Entertaining/Relatable: 25%
- Community/Culture: 20%
- Promotional/Product: 15%
- Thought Leadership/Industry: 10%

Adjust based on brand stage:
- **New brand** (0–1 yr): skew educational (40%) and entertaining (30%) — build trust + awareness
- **Growth brand** (1–3 yr): balanced across all 5 pillars
- **Established brand** (3+ yr): community (25%) + thought leadership (20%) — deepen loyalty

### Phase 5: Tone & Voice Guide

```markdown
| Dimension | Our Approach | Avoid |
|---|---|---|
| Formality | Conversational but informed | Jargon-heavy, corporate speak |
| Humor | Witty, situational | Sarcasm, dark humor |
| Authority | Data-backed claims | Absolutes, false certainty |
| Empathy | Acknowledge pain before solutions | Toxic optimism |
| Inclusivity | Gender-neutral, diverse | Assumptions about audience |
| CTA | Clear, low-friction | Desperate sales language |
```

**Platform-specific tone adaptations:**
- **LinkedIn**: Professional warmth, data-rich
- **TikTok**: Casual, trend-aware, embraces imperfection
- **Instagram**: Aspirational yet accessible, community-first
- **X/Twitter**: Sharp, timely, quick wit

### Phase 6: Posting Cadence & Optimal Timing

```markdown
| Platform | Min/Week | Ideal/Week | Max |
|---|---|---|---|
| LinkedIn | 3 | 5 | 7 |
| Instagram Feed | 3 | 4 | 7 |
| Instagram Stories | 5 | 7+ | 14+ |
| TikTok | 3 | 5 | 10 |
| X/Twitter | 7 | 14 | 28 |
| YouTube | 1 | 2 | 4 |
| Facebook | 3 | 5 | 7 |
```

**Optimal posting times (general — verify in analytics):**
- **LinkedIn**: Tue–Thu 8–10 AM, 12–1 PM, 5–6 PM
- **Instagram**: Mon–Fri 9–11 AM, Tue 11 AM (best day)
- **TikTok**: Tue–Thu 7–9 AM, 11 AM–2 PM, 7–10 PM
- **X/Twitter**: Mon–Fri 8–10 AM, 1–3 PM, 5–6 PM
- **YouTube**: Sat–Sun 9–11 AM (publish 2–4 hours before prime viewing)

### Phase 7: Hashtag Strategy

```
TIER 1 — Broad reach (500K–1M+ posts): 3–5 hashtags
  → High visibility, low conversion
TIER 2 — Niche community (10K–500K posts): 5–8 hashtags
  → Sweet spot — high reach with relevant audience
TIER 3 — Branded + Hyper-specific (<10K posts): 2–3 hashtags
  → Low reach, highest conversion, owned space

Per post: 10–15 (Instagram), 2–5 (LinkedIn), 0–2 (TikTok)
```

### Phase 8: KPI Dashboard

```markdown
| Metric | Target | Last Month | This Month | % Change | On Track? |
|---|---|---|---|---|---|
| Follower count | +1,000 | 8,420 | 9,150 | +8.7% | ✅ |
| Engagement rate | 4.0% | 3.2% | 3.8% | +18.8% | ✅ |
| Reach | 50,000 | 42,000 | 51,200 | +21.9% | ✅ |
| Link clicks | 1,500 | 1,200 | 1,450 | +20.8% | ⚠️ |
| Conversion rate | 2.5% | 1.8% | 2.1% | +16.7% | ⚠️ |
| Cost per click | $0.50 | $0.62 | $0.55 | +11.3% | ✅ |
```

### Phase 9: Content Production Workflow

```
Monday (Strategy): Review analytics, update calendar, brief team
Tuesday/Wednesday (Production): Write copy, design visuals, edit video, source audio
Thursday (Review & Schedule): Internal review, approve, schedule in Buffer/Hootsuite/Later
Friday (Engagement): Reply to all comments/DMs, engage 15–20 industry accounts, retrospective
```

## Common Pitfalls

- **Too many platforms at once**: Start with 2–3 and master them.
- **Vanity metrics focus**: Tie everything to business outcomes (leads, sales, traffic).
- **No pillar guardrails**: Without content pillar %s, brands drift 70% promotional.
- **Cross-posting verbatim**: Adapt format and tone per platform.
- **Hashtag stuffing**: 30 irrelevant hashtags hurt reach.
- **Static strategy**: Review and update quarterly. Platforms change algorithms 4–6×/year.
- **No repurposing workflow**: Each long-form piece should yield 5–10 social posts.

## Verification Checklist

- [ ] Strategy doc saved as markdown with date stamp
- [ ] Internal audit completed with top/bottom 5 posts identified
- [ ] Competitive audit (3–5 competitors) documented
- [ ] 3–5 SMART goals defined mapped to funnel stage
- [ ] Platform scoring matrix filled with ≥6 platforms scored
- [ ] 3–5 content pillars defined with %, topics, example headlines
- [ ] Tone & voice matrix completed with platform adaptations
- [ ] Posting cadence table populated for selected platforms
- [ ] Hashtag tier strategy documented
- [ ] KPI dashboard structure with targets and tracking columns
- [ ] Content production workflow (weekly cycle) documented
- [ ] Stakeholder review completed with sign-off