---
name: blog-idea-generator
description: "Use when generating blog ideas. Multi-framework."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [blog, ideas, content-planning, keyword-research, topics]
    related_skills: [blog-post-outliner, blog-seo-post-optimizer, blog-analytics-interpreter]
---

# Blog Idea Generator

## Overview

A systematic, multi-framework approach to generating blog post ideas. Combines keyword gap analysis, competitor audits, customer Q&A mining (Reddit, Quora, Amazon reviews), seasonal/trending topics, and content upgrade strategies. Outputs a scored, prioritized list with difficulty, traffic potential, and angle for each idea.

## When to Use

- You're starting a new blog and need 20–50 content ideas
- Your content calendar is running dry
- You're entering a new niche or category
- You want to outperform competitors' existing content
- You need data-backed justification for editorial decisions

## Frameworks

### 1. Keyword Gap Analysis

Compare your current ranking keywords against competitors to find opportunities your site misses.

**Process:**
1. Identify 3–5 top competitors in your niche
2. Collect their ranking keywords via Ahrefs / Semrush / Ubersuggest / Google Search Console
3. Cross-reference against your own keyword portfolio
4. Find keywords where competitors rank 4–15 and you don't rank at all
5. Prioritize by: search volume × relevance × (15 - competitor rank position)

**Tools:**
| Tool | Purpose |
|------|---------|
| Ahrefs Content Gap | Side-by-side competitor keyword overlap |
| Semrush Keyword Gap | Compare up to 5 domains |
| Google Search Console | Your actual ranking terms + impressions |
| Ubersuggest | Free keyword data with volume estimates |

### 2. Competitor Content Audit

Systematically analyze what worked for competitors and build a better version.

**Process:**
1. Pull the top 10 highest-traffic posts from each competitor (Ahrefs Site Explorer or Similarweb)
2. For each post, evaluate:
   - Headline format (listicle, how-to, pillar, controversy)
   - Word count and depth
   - Visual assets (screenshots, diagrams, videos)
   - Internal/external links
   - Social proof (comments, shares, backlinks)
3. Identify the "content gap": what does their post skip or handle poorly?
4. Build a "10x" angle: deeper research, better formatting, fresh data, expert quotes, interactive elements

**Scoring Matrix:**
| Factor | Weight |
|--------|--------|
| Competitor traffic | 25% |
| Current backlink count | 20% |
| Content freshness (last update) | 15% |
| Keyword difficulty (KD) | 15% |
| Our authority in niche | 15% |
| Seasonal relevance | 10% |

### 3. Customer Q&A Mining

Find real questions your audience is asking and answer them directly.

**Sources:**
- **Reddit:** `site:reddit.com/r/{subreddit} {topic}"` — search for questions with high upvotes (500+)
- **Quora:** `site:quora.com {topic} "what" OR "how" OR "why"` — find top-viewed questions
- **Amazon Reviews:** Scrape reviews of popular books/products in niche; extract complaints, desired outcomes, questions
- **YouTube Comments:** Filter high-view videos on your topic; look for "question" comments left by viewers
- **AnswerThePublic:** Visualizes search questions by question word (what, why, how, which)
- **AlsoAsked.com:** Shows "people also ask" follow-up chains in a visual tree
- **Support Tickets / Customer Emails:** Internal feedback is gold — what do customers ask support?

**Idea Template:**
```
Q: [Exact question from source]
Angle: [Unique take — personal experience, data-driven, contrarian]
Search Volume: [Monthly searches estimated via keyword tool]
Potential: [High / Medium / Low based on combo of volume + competition]
```

### 4. Seasonal & Trending Topics

Ride existing search patterns with timely content.

**Checklist:**
- [ ] Google Trends for topic over 12 months — note peaks
- [ ] Google Alerts set up for 5 core keywords
- [ ] Upcoming holidays / events / awareness days in your niche
- [ ] Industry conference schedules (talk titles = content ideas)
- [ ] Product launch calendar (yours and competitors')
- [ ] Exploding Topics / SparkToro trending reports
- [ ] "Year in Review" / "Year Ahead" content for Q4

**Seasonal Planning Table:**
```
Season/Event      | Prep Content | Curated Content | Promotion Strategy
------------------|-------------|----------------|--------------------
Q1 New Year       | Resolutions  | Best-of lists  | Social + email
Mid-year          | Half-year review | Trend roundups | LinkedIn
Industry event    | Pre-event blog | Live coverage | Outreach to attendees
Product launch    | Teaser posts | Launch announcement | PR + paid
```

### 5. Content Upgrade Strategy

Turn existing ideas into multiple formats or stack them into pillar pages.

**Upgrade Paths:**
| Original | Upgrade |
|----------|---------|
| Listicle (10 tips) | In-depth pillar page (50 tips) |
| Single case study | Case study roundup (5–10 studies) |
| How-to post | Video + transcript + downloadable checklist |
| Interview | Multi-interview roundup with analysis |
| Data post | Updated version with new data yearly |
| Beginner guide | Advanced guide + tools directory |

## The Scored Idea List

Output format — generate 15–50 rows like this:

| # | Idea Title | Keyword | Vol | KD | Angle | Priority |
|---|-----------|---------|-----|-----|-------|----------|
| 1 | "X for Beginners: Complete Guide" | how to X | 2.4K | 12 | Beginner-focused with checklist | A |
| 2 | "Why [Common Belief] Is Wrong" | [common belief] myth | 800 | 8 | Contrarian w/ data | A |
| 3 | "10 [Topic] Tools Under $50" | best tools for X | 1.2K | 22 | Budget angle | B |

**Priority Tiers:**
- **A (Publish ASAP):** High volume + low difficulty + high relevance
- **B (Calendar within 30 days):** Good combo of factors
- **C (Backlog / fill later):** Low volume or high difficulty but brand-building
- **D (Revisit seasonally):** Timing-dependent

## Common Pitfalls

- **Keyword cannibalization:** Don't write the same angle twice — consolidate or differentiate
- **Too broad, not specific enough:** "Content marketing" vs "Content marketing for SaaS startups with <50 employees"
- **Ignoring search intent:** "Best coffee makers" = commercial intent (affiliate); "How to make pour-over coffee" = informational
- **Vanity keywords:** High volume but zero conversion potential — prioritize buyer-intent terms
- **No differentiation:** If 20 posts already cover the same angle, yours needs a real hook
- **Over-relying on AI idea generation without real source mining:** Tools hallucinate demand — verify with actual search data

## Verification Checklist

- [ ] Keyword gap analysis run against 3 competitors
- [ ] At least 3 real customer questions mined (Reddit / Quora / reviews / support)
- [ ] Seasonal trend data checked (Google Trends)
- [ ] Each idea has search volume + KD estimate
- [ ] No duplicate angles across ideas
- [ ] At least 5 priority-A ideas identified
- [ ] Content upgrade path noted for at least 2 ideas
- [ ] Ideas exported to a ranked spreadsheet or Notion database