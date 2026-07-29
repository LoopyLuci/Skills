---
name: social-media-content-calendar
description: "Use when planning social media content calendars."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [social-media, content-calendar, planning, scheduling]
    related_skills: [social-media-strategy, social-media-analytics]
---

# Social Media Content Calendar

## Overview

A complete system for building month-long social media content calendars across platforms. Includes daily post ideas with suggested visuals, captions, hashtags, optimal posting times, and content pillar tracking. Outputs both markdown (readable plan) and CSV (importable into Google Sheets, Airtable, or scheduling tools like Buffer/Hootsuite/Later).

## When to Use

- **Monthly planning session** — before a new month begins, set up 4 weeks of content
- **Campaign planning** — product launches, events, seasonal promotions, or awareness months
- **Content gap analysis** — when analytics show certain pillars or formats are underrepresented
- **Client content planning** — deliverable for social media management clients
- **Team coordination** — align writers, designers, and video editors on what needs to be produced and when

## Body

### Template 1: Markdown Monthly Calendar

```bash
touch content_calendar_$(date +%Y_%m).md
```

**Structure:**

```markdown
# Content Calendar: [Month] [Year]
## Month Theme: [Theme]
## Campaign Focus: [Campaign name]
## Key Dates: [Holidays, launches, events]

## Week 1: [Theme]

### Monday — [Date]
| Field | Value |
|---|---|
| Platform | LinkedIn |
| Pillar | Educational |
| Format | Carousel (PDF) — 5 slides |
| Topic | "3 Signs Your [Problem] Is Costing You Revenue" |
| Visual Brief | Title → Sign 1 → Sign 2 → Sign 3 → CTA |
| Caption Hook | "Here's the uncomfortable truth about [problem]..." |
| CTA | "Drop a 🔥 if you've seen #2 happen in your org" |
| Hashtags | #[Industry]Tips, #B2B[Topic], #[Niche]Strategy |
| Best Time | 9:00 AM ET |
| Status | [ ] Draft [ ] Review [ ] Scheduled |

### Tuesday — Instagram Reel
| Field | Value |
|---|---|
| Format | Reel — 15–30s |
| Topic | "POV: Explaining [industry concept] to a non-tech friend" |
| Audio | Trending sound |
| Caption | Short + question. "Tag someone who needs this 😂" |
| Best Time | 11:00 AM ET |

### Wednesday — X/Twitter Thread
| Field | Value |
|---|---|
| Format | Thread — 5–7 tweets |
| Topic | "Why [trend] is overhyped (and what matters)" |
| Tweet 1 | Hot take + thesis |
| Tweets 2–5 | Numbered points |
| Tweet 6 (CTA) | "What'd I miss? Reply below 👇" |

### Thursday — TikTok
| Field | Value |
|---|---|
| Topic | "One hack that saved us $10K/month" |
| Style | Direct-to-camera, text overlay |
| Caption | "Save this for later 📌" |

### Friday — LinkedIn Community
| Field | Value |
|---|---|
| Topic | Team spotlight / behind-the-scenes |
| Caption | Personal, vulnerable, human |
```

### Template 2: CSV Calendar (Import-Ready)

```bash
cat << 'CALENDAR_HEADER' > content_calendar_$(date +%Y_%m).csv
Date,Day,Platform,Pillar,Format,Topic,CTA,Hashtags,Best Time,Status
"2025-04-01","Tuesday","LinkedIn","Educational","Carousel","3 Signs Your Strategy Is Failing","Save this","#Strategy","9:00 AM","Draft"
"2025-04-02","Wednesday","Instagram","Entertaining","Reel","POV: Explaining ROI","Tag someone","#MarketingHumor","11:00 AM","Idea"
CALENDAR_HEADER
```

### Platform-Aware Planning Templates

**LinkedIn-Focused Week:** Mon=Carousel, Tue=Text (hot take), Wed=Document (case study), Thu=Text (story), Fri=Image (culture)

**Instagram-Focused Week:** Mon=Carousel (tips) + Stories BTS, Tue=Image + Poll, Wed=Reel only, Thu=Carousel + Countdown, Fri=Image (aesthetic) + ThisOrThat, Sat=Reel (lifestyle)

**TikTok-Focused Week:** Mon=Educational 60s, Tue=Trend take 15s (Duet), Wed=Storytime 45s, Thu=List format 60s, Fri=Relatable 15s, Sat=UGC reshare 30s, Sun=Roundup 30s

### Content Mix Tracker

```markdown
| Week | Educational | Entertaining | Community | Promotional | Thought Leadership |
|---|---|---|---|---|---|
| W1 | 3 | 2 | 2 | 1 | 2 |
| W2 | 2 | 3 | 1 | 2 | 2 |
| Total | 5 (25%) | 5 (25%) | 3 (15%) | 3 (15%) | 4 (20%) |
```

### 12-Month Theme Calendar

| Month | Theme | Focus |
|---|---|---|
| Jan | Fresh Start | Educational, aspirational |
| Feb | Deep Connections | Community, culture |
| Mar | Growth & Strategy | Data-driven |
| Apr | Innovation | Thought leadership |
| May | Celebration | Culture, social proof |
| Jun | Mid-Year Pivot | Analytical |
| Jul | Behind the Scenes | Community |
| Aug | Deep Dives | Educational |
| Sep | Back to Basics | Educational |
| Oct | Case Studies | Social proof, conversion |
| Nov | Gratitude | Community |
| Dec | Year in Review | Thought leadership |

## Common Pitfalls

- **Overplanning, under-creating**: Leave 30% buffer for reactive/trending content.
- **No pillar tracking**: Check the tracker weekly or you'll skew 70% promotional.
- **Same content, every platform**: Adapt format, hook, and length per platform.
- **Ignoring seasonality**: Check holidays and events BEFORE scheduling.
- **Scheduling without engagement time**: Block 30 min/day for comment replies.
- **Caption-first trap**: Visuals drive engagement. Write caption last.
- **No repurposing plan**: Each long-form asset → 3–5 calendar entries.
- **CSV encoding**: Must be UTF-8 with BOM for Excel. `printf '\xef\xbb\xbf' > file.csv`
- **Static calendar**: Update every 2 weeks based on real performance.

## Verification Checklist

- [ ] Calendar file created (markdown or CSV) with date stamp
- [ ] Month theme defined
- [ ] Key dates (holidays, launches, events) noted
- [ ] Each week has posts for each active platform
- [ ] Content mix tracker shows balanced pillar distribution
- [ ] Every post has: platform, pillar, format, topic, caption hook, CTA, hashtags, best time
- [ ] Visual brief included for each post
- [ ] 30% buffer space for reactive/trending content
- [ ] Team roles assigned (writer, designer, reviewer, scheduler)
- [ ] Previous month's analytics reviewed before finalizing