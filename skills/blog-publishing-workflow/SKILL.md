---
name: blog-publishing-workflow
description: "Use when managing blog publishing. Draft to publish."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [blog, publishing, editorial, workflow, content-management]
    related_skills: [blog-post-outliner, blog-seo-post-optimizer, content-repurposing]
---

# Blog Publishing Workflow

## Overview

A complete editorial pipeline from draft to post-mortem. Covers every stage: drafting, reviewing, editing, approving, scheduling, publishing, and promoting. Integrates grammar/style checking, image optimization, internal linking, SEO metadata, social excerpts, scheduling, and a 30-day post-mortem analysis. Works with SSGs (Hugo, Jekyll, Astro), WordPress, Ghost, Medium, and any CMS.

## When to Use

- You're setting up a one-person or team editorial process
- You need to enforce quality gates before publishing
- You're migrating to a new CMS or static site generator
- You want to eliminate "publish and pray" by adding promotion automation
- You need a repeatable checklist for every post

## Full Pipeline

### Stage 1: Draft

**Goal:** Get raw content onto the page. Imperfect is fine — the next stages polish it.

**Workflow:**
```
Idea → Outline (blog-post-outliner) → First draft → Draft label applied
```

**Check:**
- [ ] Outline approved by editor/self before writing
- [ ] Target word count noted (don't exceed ±20%)
- [ ] Primary + secondary keywords listed at the top of the file
- [ ] Draft saved with version: `draft-v1` or branch name
- [ ] All source URLs / research notes included
- [ ] Placeholder `[IMAGE: description]` markers where visuals go

**File Naming Convention:**
```
posts/{yyyy}-{mm}-{dd}-{slug}.md       # Single file
posts/{yyyy}/{mm}/{slug}/index.md      # Hugo/Jekyll style with assets folder
```

### Stage 2: Review

**Goal:** Structural integrity, argument flow, fact-checking, tone alignment.

**Reviewer Checklist:**
- [ ] Headline matches post content (no clickbait mismatch)
- [ ] Intro hook is engaging and accurate
- [ ] H2/H3 structure logical and scannable
- [ ] Facts/statistics checked against source
- [ ] Quotes attributed correctly
- [ ] No logical gaps or missing context
- [ ] Tone and voice consistent with brand guidelines
- [ ] Internal links point to relevant posts (not orphaned)
- [ ] External links point to authoritative, live URLs
- [ ] Plagiarism check passed (Copyscape / Grammarly / originality.ai)

**Tools:**
- Grammarly / Hemingway — tone, clarity, readability
- Copyscape / Originality.ai — plagiarism detection
- Ahrefs Site Audit (for linking internal candidates)

### Stage 3: Edit

**Goal:** Polish language, fix grammar, optimize readability, finalize formatting.

**Edit Passes (do in order):**

**Pass A — Line Edit:** Fix grammar, spelling, punctuation, syntax. Eliminate passive voice where active is stronger. Shorten long sentences. Remove filler words (very, really, just, actually, that).

**Pass B — Readability Edit:** Apply formatting rules from blog-post-outliner. Break long paragraphs. Add subheadings. Insert bullet lists. Check Flesch-Kincaid grade level (target: 6th–8th grade for broad audience, 9th–12th grade for technical/professional).

**Pass C — SEO Edit:** Run blog-seo-post-optimizer checks — keyword placement, meta description, alt text, schema markup.

**Pass D — Visual Edit:** Place actual images/media, write captions, add alt text. Run image compression. Check mobile layout (screenshots if needed).

**Checklist:**
- [ ] Spelling and grammar check passed
- [ ] Flesch-Kincaid grade level within target range
- [ ] Active voice on >80% of sentences
- [ ] Filler words removed
- [ ] All `[IMAGE:]` placeholders replaced with real media
- [ ] Images compressed (< 200 KB for inline, < 1 MB for hero)
- [ ] Alt text written for all images
- [ ] Social sharing image created (1200×630 px)
- [ ] Mobile preview checked

### Stage 4: Approve

**Goal:** Final sign-off — no more content changes after this.

**Decision Matrix:**
| Gate | Pass | Fail → Action |
|------|------|--------------|
| Content accuracy | All claims verified | Return to review with comments |
| SEO optimization | Keyword placement, meta, schema | Return to edit Pass B |
| Formatting | All elements rendered properly | Return to edit Pass D |
| Brand alignment | Tone, voice, positioning | Return to Stage 2 review |
| Legal/Compliance | No liability or regulatory issues | Consult legal team |

**Sign-off methods:**
- **Git-based:** PR approval via GitHub/GitLab (squash merge to main)
- **CMS-based:** Set post status to "Pending Review" → editor approves → status to "Scheduled"
- **Notion-based:** Status field: `Draft → In Review → Approved → Scheduled`

### Stage 5: Schedule

**Goal:** Right time, right frequency, right promotion lead time.

**Scheduling Rules:**
- **Frequency:** At most 1 post per day, at least 1 post per week
- **Best publish days** (general B2B): Tuesday 8–10 AM, Thursday 8–10 AM (US ET)
- **Best publish days** (general B2C): Saturday 9–11 AM, Sunday 10 AM–12 PM
- **Lead time for promotion assets:** 48 hours before publish
- **Inter-post spacing:** No two posts targeting the same keyword within 30 days
- **Time zone:** Set in CMS/scheduler (recommend: ET for US audience, UTC for global)

**Pre-Publish Promotion Checklist (48h before):**
- [ ] Social graphics queued in Buffer/Hootsuite/Sprout
- [ ] Email draft written (subject, preview text, excerpt)
- [ ] Outreach list started (relevant influencers/tools mentioned in post)
- [ ] Internal team notified (Slack/Teams)

### Stage 6: Publish

**Goal:** Flawless launch — every detail correct on the live post.

**Publish Day Checklist:**
- [ ] URL slug correct (no trailing dates unless standard)
- [ ] Meta title and description rendered correctly
- [ ] Canonical URL set (no self-duplicate issues)
- [ ] Open Graph tags set (og:title, og:description, og:image, og:url)
- [ ] Twitter Card tags set (twitter:card, twitter:title, twitter:description, twitter:image)
- [ ] Featured image / hero image displays correctly
- [ ] All images load and aren't broken
- [ ] Table of contents renders (if used)
- [ ] Internal links point to live URLs (not draft URLs)
- [ ] Schema markup valid (test with Google Rich Results Test)
- [ ] RSS feed updated (check feed reader)
- [ ] Sitemap pinged (Google Search Console, Bing Webmaster Tools)
- [ ] 301 redirect from old slug if slug changed during editing

### Stage 7: Promote

**Goal:** Amplify reach through owned, earned, and paid channels.

**Day 0 (Publish day):**
- [ ] Post shared on Twitter/X, LinkedIn, Facebook, Bluesky (or relevant platforms)
- [ ] Newsletter sent to list (if news post or high-value)
- [ ] Shortened link (bit.ly / uhoh) used for trackable sharing
- [ ] Relevant Slack/Discord communities pinged (if allowed)
- [ ] Author bio/link updated on profile

**Day 1–3:**
- [ ] Cross-post to Medium (canonical link back to original)
- [ ] Cross-post to dev.to (tech content) or LinkedIn Articles
- [ ] Reply to comments on all social posts
- [ ] Tag any people/brands mentioned in the post
- [ ] Submit to relevant aggregators (Inbound.org, GrowthHackers, Sphinn, etc.)

**Day 4–14:**
- [ ] Guest post pitching — reference this post as credential
- [ ] Outreach to blogs that link to similar content
- [ ] Repurpose into one other format (see content-repurposing)
- [ ] Pinterest pin (if visual niche)
- [ ] HARO/Help a Reporter response with post as reference

**Day 14–30:**
- [ ] Check social analytics — double down on best-performing platform
- [ ] Check Google Search Console — impressions, clicks, avg position
- [ ] Update post with new data if stale
- [ ] Add internal links from 2–3 older posts pointing to this one
- [ ] 30-day post-mortem (see below)

### 30-Day Post-Mortem

Analyze every published post 30 days after publication.

**Post-Mortem Template:**
```
Post Title:
Slug:
Publish Date:
Type: [Pillar / Guide / List / News / Opinion]

Metrics (30 days):
  Pageviews: ___
  Unique Visitors: ___
  Avg Time on Page: ___
  Bounce Rate: __%
  Social Shares: ___
  Backlinks: ___
  Email Clicks: ___
  Comments: ___
  Search Impressions: ___
  Search Avg Position: ___

Grade: [A / B / C / D]
  A: > 75th percentile → Repurpose, update quarterly
  B: > 50th → Promote more, check for small fixes
  C: > 25th → Find bottleneck (title, distribution, topic)
  D: Bottom quartile → Investigate (bad keyword, timing, or content)

Lessons:
- What worked? ___
- What would you change? ___
- Should a follow-up be written? (Yes/No) ___
- Score for Editorial Calendar: [Keep / Cluster / Archive]
```

## Integration Notes

### Static Site Generators (Hugo, Jekyll, Astro, 11ty)
```yaml
---
title: "Post Title"
date: 2025-01-15T08:00:00-05:00
draft: true
tags: ["tag1", "tag2"]
categories: ["category"]
description: "Meta description here"
featured_image: "/images/post-hero.webp"
canonical: "https://example.com/post"
toc: true
---
```
- Use `draft: true` until publish day
- CI/CD handles minification and image optimization
- Git hooks can run link-checking before merge

### WordPress / Ghost / Medium
- Use the respective REST API for scheduling
- WordPress: Yoast / RankMath for SEO metadata
- Ghost: built-in meta editor (OG, Twitter, Schema)
- Medium: import with canonical URL set in Advanced Settings

## Common Pitfalls

- **Publishing without a review gate:** Typos, broken links, factual errors erode trust — enforce at least one reviewer
- **Skipping image optimization:** Large images kill page speed and Core Web Vitals — always compress before uploading
- **Publishing then forgetting:** Without a promotion plan, great posts get zero traffic — schedule promo before publishing
- **Inconsistent scheduling:** Three posts one week and none the next hurts SEO trust signals — maintain rhythm
- **Ignoring the post-mortem:** Without tracking what worked, you repeat mistakes. Run the 30-day check on every post
- **No RSS ping:** New posts won't appear in news readers fast enough without sitemap ping

## Verification Checklist

- [ ] All 7 stages checklist executed (draft → review → edit → approve → schedule → publish → promote)
- [ ] 48-hour pre-publish promo assets prepared
- [ ] Publish-day checklist fully completed (broken links checked, schema tested, OG tags valid)
- [ ] 7-day promotion schedule executed
- [ ] 30-day post-mortem recorded in analytics tracker
- [ ] Post categorized and tagged for future clustering