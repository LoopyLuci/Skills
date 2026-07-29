---
name: seo-strategy
description: "Use when building SEO. Keywords, on-page, technical."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [seo, search-engine-optimization, content, keywords, technical-seo]
    related_skills: [content-marketing-workflow, marketing-analytics-dashboard, competitor-analysis]
---

# SEO Strategy

## Overview

A comprehensive search engine optimization (SEO) methodology covering the full spectrum: keyword research (head terms, long-tail, search intent, difficulty analysis), on-page optimization (title tags, meta descriptions, headers, internal linking, content structure), technical SEO audit (Crawlability, Core Web Vitals, XML sitemaps, robots.txt, canonical tags, structured data), local SEO (Google Business Profile, local citations, review management), and competitor backlink analysis. This skill provides a systematic, data-driven approach to improving organic search visibility.

## When to Use

- Building an SEO strategy from scratch for a new website or product
- Conducting a technical SEO audit and identifying quick wins
- Performing keyword research and content gap analysis for a content plan
- Optimizing existing content for higher search rankings
- Setting up local SEO for a brick-and-mortar or service-area business
- Analyzing competitor backlink profiles to inform link building
- Diagnosing a drop in organic traffic or rankings
- Preparing for a site migration or redesign from an SEO perspective

## Body

### 1. Keyword Research

#### 1.1 Keyword Taxonomy

| Type | Example | Search Volume | Competition | Conversion Potential | Strategy |
|---|---|---|---|---|---|
| **Head Terms (1–2 words)** | "CRM software" | High (10K–100K+/mo) | Very high | Low (informational) | Build brand authority, not ranking for these initially |
| **Body Terms (2–3 words)** | "small business CRM" | Medium (1K–10K/mo) | High | Medium | Target with pillar content |
| **Long-Tail (3+ words)** | "best CRM for real estate agents with 5 employees" | Low (100–1K/mo) | Low-Medium | High (purchase intent) | Target with specific landing pages / blog posts |
| **Question-Based** | "how to choose a CRM" | Medium | Medium | Medium | Target with how-to guides |

#### 1.2 Search Intent Classification

| Intent | Goal | Content Type | Landing Page Type |
|---|---|---|---|
| **Informational** | Learn something | Blog posts, guides, tutorials, videos | Educational content |
| **Commercial** | Research before buying | Comparison posts, reviews, best-of lists | Category / roundup pages |
| **Transactional** | Buy / sign up | Product pages, pricing, free trial | Product / sales pages |
| **Navigational** | Find a specific site | Brand pages | Homepage / brand page |

**Intent mapping rule:** Match content type to search intent exactly. An informational query needs a guide, not a product page. A transactional query needs pricing, not a blog post.

#### 1.3 Keyword Difficulty & Opportunity Scoring

Build a weighted score for each keyword candidate:

```
Keyword Score = (SV × 0.20) + (Intent Fit × 0.25) + (Business Value × 0.25) + (Difficulty^-1 × 0.20) + (CTR Potential × 0.10)
```

| Factor | Source | Scoring |
|---|---|---|
| Search Volume (SV) | Ahrefs, SEMrush, GSC, KW Finder | 0 = <100, 25 = 100–500, 50 = 500–2K, 75 = 2K–10K, 100 = 10K+ |
| Intent Fit | Manual assessment | 0 = poor match, 50 = moderate, 100 = exact match |
| Business Value | Revenue potential estimation | 0 = low purchase intent, 50 = medium, 100 = high purchase intent |
| Difficulty | Ahrefs KD, SEMrush KD, Moz DA of top 10 | 0 = KD 80+, 25 = KD 60–79, 50 = KD 40–59, 75 = KD 20–39, 100 = KD 0–19 |
| CTR Potential | SERP feature presence (featured snippet, People Also Ask) | 0 = no features, 50 = some, 100 = featured snippet opportunity |

**Target:** Score 60+ → strong opportunity. Score 40–59 → consider only if strategically important. Score < 40 → deprioritize.

#### 1.4 Keyword Clustering

Group keywords into topical clusters for content planning:

1. Identify the "head" keyword per cluster (highest volume, most general)
2. Map all long-tail and related keywords to that head term
3. Build one pillar page for the head keyword
4. Create supporting cluster content for each long-tail variation

```
Cluster: "CRM software for small business"
├── Pillar: "The Complete Guide to CRM Software for Small Business"       ← Head keyword
├── Cluster 1: "Benefits of CRM for small business"                       ← Long-tail
├── Cluster 2: "How to choose a CRM for your small business"              ← Long-tail / question
├── Cluster 3: "Best affordable CRM software under $50/month"             ← Commercial
├── Cluster 4: "CRM implementation guide for small teams"                 ← Informational
└── Cluster 5: "CRM vs spreadsheets: why you need to switch"              ← Comparison
```

### 2. On-Page Optimization

#### 2.1 Title Tag Formula

```
Primary Keyword - Secondary Keyword | Brand Name
```

**Rules:**
- Length: 50–60 characters (Google typically displays ~580px — ~60 chars)
- Primary keyword as close to the beginning as possible
- Unique per page (no duplicate titles)
- Include brand name at the end (separated by pipe or dash)
- Match search intent (don't mislead)

**Examples:**
- ✅ "CRM for Real Estate Agents: Features, Pricing & Reviews | BrandName"
- ❌ "Software | BrandName" (too generic)
- ❌ "Welcome to our website" (no keywords)

#### 2.2 Meta Description Formula

```
[Action verb] [keyword] to [benefit]. Learn about [feature/benefit 1], [feature/benefit 2], and [feature/benefit 3]. [Brand] helps [audience] [outcome].
```

**Rules:**
- Length: 150–160 characters (Google truncates around 160)
- Include primary keyword naturally
- Include a CTA (Learn, Discover, Find, Get)
- Don't duplicate across pages
- Can influence CTR even though not a direct ranking factor

#### 2.3 Heading Structure (H1–H4)

```
H1: Primary Keyword (must be unique, one per page)
├── H2: Key subtopic 1 (includes related keyword)
│   ├── H3: Specific point within subtopic 1
│   └── H3: Another point
├── H2: Key subtopic 2
│   ├── H3: Detail
│   │   └── H4: Sub-detail
│   └── H3: Detail
├── H2: FAQ Section (or related question)
└── H2: Conclusion / Next steps
```

**Rules:**
- One H1 per page (matching the main topic / target keyword)
- H2s for major sections, H3s for subsections, H4s for details
- Include keywords naturally — don't keyword-stuff
- Headings should form a logical outline of the page content

#### 2.4 Content Optimization Checklist

- [ ] Keyword appears in: Title tag, H1, first 100 words, at least one H2, meta description, URL slug
- [ ] Content length: Comprehensive coverage (match or exceed top 3 competitors' word count)
- [ ] Readability score: Target 60–70+ (Flesch Reading Ease) / Grade 8–9 or simpler
- [ ] Internal links: 3–5 relevant links to other pages on your site per 1,000 words
- [ ] External links: 1–3 high-authority references
- [ ] Image alt text: Descriptive, includes keyword where natural
- [ ] Multimedia: At least one image, video, or infographic per 500 words
- [ ] Snippet optimization: Use bullet lists, tables, numbered steps for featured snippet chance
- [ ] Freshness: Update content every 6–12 months (add new data, examples, screenshots)

#### 2.5 Internal Linking Strategy

| Link Type | Purpose | How Often | Anchor Text |
|---|---|---|---|
| Navigational | Main menu, breadcrumbs | Every page | Generic ("Products", "About") |
| Contextual (in-body) | Connect related content | 3–5 per 1K words | Descriptive ("read our complete CRM guide") |
| Hub & Spoke | Cluster pages → Pillar page | Each cluster page links to pillar | Pillar keyword |
| Related posts | Bottom of blog posts | Automatic | Post title |
| Breadcrumbs | Site structure | All pages | Hierarchical category names |
| Footer links | Important pages | Footer on all pages | Short, generic |

### 3. Technical SEO Audit

#### 3.1 Crawlability & Indexability

| Check | Tool(s) | Pass Criteria | Fix if Failing |
|---|---|---|---|
| XML Sitemap | GSC, Screaming Frog, site.com/sitemap.xml | Valid XML, submitted to GSC, < 50K URLs, includes only canonical/indexable pages | Generate proper sitemap, remove noindex/redirect pages |
| robots.txt | site.com/robots.txt, GSC | Allows important pages, disallows admin/dev, references sitemap URL | Add `Allow: /`, `Disallow: /admin/*`, `Sitemap: https://site.com/sitemap.xml` |
| Crawl budget | GSC Crawl Stats | Google crawls new pages within 1–7 days | Remove low-value pages, fix 4xx/5xx errors |
| JavaScript rendering | GSC URL Inspection, Searchie.io | Content renders correctly without JS (or renders via Google's crawler) | Use SSR, pre-rendering, or dynamic rendering for JS-heavy sites |
| Page depth | Screaming Frog | Important pages within 3 clicks of homepage | Flatten site architecture, add breadcrumbs |
| Orphan pages | Screaming Frog, Analytics | No important pages without internal links | Add internal links to orphaned but valuable pages |

#### 3.2 Core Web Vitals

| Metric | What It Measures | Good (<) | Needs Improvement | Poor (>) |
|---|---|---|---|---|
| **LCP** (Largest Contentful Paint) | Loading speed — how fast main content appears | 2.5s | 2.5s–4.0s | 4.0s |
| **FID** (First Input Delay) | Interactivity — how fast page responds to user input | 100ms | 100ms–300ms | 300ms |
| **CLS** (Cumulative Layout Shift) | Visual stability — how much content jumps around | 0.1 | 0.1–0.25 | 0.25 |

**Optimization checklist:**
- [ ] LCP: Optimize images (WebP, compress), lazy-load below-fold images, preload hero image, minimize render-blocking resources, use a CDN
- [ ] FID: Eliminate long tasks (>50ms), defer non-critical JS, code-split large bundles, use web workers for heavy computation
- [ ] CLS: Set explicit width/height on all images/embeds, avoid inserting content above existing content after load, use `aspect-ratio` CSS, reserve space for ads/embeds

#### 3.3 Canonical Tags

| Scenario | Canonical URL | Notes |
|---|---|---|
| Same page, multiple URLs | Set to the preferred version | E.g., `site.com/page/` canonical to `site.com/page` |
| WWW vs. non-WWW | Pick one and 301 the other | Or use canonical consistently |
| HTTP vs. HTTPS | Always the HTTPS version | 301 HTTP → HTTPS |
| Paginated pages | Self-referencing canonical on each page | Or rel="next"/"prev" (Google mostly ignores these now) |
| Filtered / sorted pages | Canonical to the unfiltered page | E.g., `?color=red` canonical to the main category page |
| Syndicated content | Canonical to the original source | Use rel="canonical" on syndicated copies |

#### 3.4 Structured Data (Schema.org)

| Schema Type | Page Type | Benefits |
|---|---|---|
| Article / BlogPosting | Blog posts | May show headline, image, date in SERP |
| Product | Product pages | Price, availability, reviews in SERP (rich results) |
| FAQ | FAQ content | Expandable FAQ in SERP (limited to 2–4 questions per page now) |
| HowTo | Tutorial / guide | Steps, time, tools in SERP |
| BreadcrumbList | Navigation | Breadcrumb trail in SERP |
| Review / AggregateRating | Review pages, products | Star ratings in SERP |
| LocalBusiness | Local landing pages | Address, hours, phone in SERP |
| Organization | About / contact pages | Logo, social profiles, contact info |
| Event | Event pages | Date, location, ticket info in SERP |
| VideoObject | Video content | Thumbnail, duration, publish date in SERP |

**Implementation:** Use JSON-LD format (Google's preferred), validate with [Google Rich Results Test](https://search.google.com/test/rich-results).

#### 3.5 Technical SEO Audit Command Line Tools

```bash
# Crawl a site (Screaming Frog CLI alternative)
# Using curl to check HTTP headers
curl -I https://example.com/page/

# Check robots.txt
curl https://example.com/robots.txt

# Check sitemap
curl https://example.com/sitemap.xml

# Check for redirect chains
curl -IL https://example.com/page 2>&1 | grep -E "HTTP/|location:"

# Core Web Vitals via PageSpeed Insights API
# (requires API key)
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com&key=YOUR_API_KEY"

# Check HTTPS cert expiry
echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null | openssl x509 -noout -dates
```

### 4. Local SEO

#### 4.1 Google Business Profile (GBP) Optimization

| Element | Requirement | Impact |
|---|---|---|
| Business name | Exact legal name (no keyword stuffing) | High — name consistency is critical |
| Address | Exact, verifiable (or service area for SABs) | High — must match citations |
| Phone number | Local number (not call tracking initially) | High — NAP consistency |
| Categories | Primary + up to 10 secondary (be specific) | Very high — defines relevance |
| Description | 750 chars max, include keywords naturally | Medium |
| Hours | Accurate, including holiday/special hours | High — incorrect hours = poor UX |
| Photos | Minimum: 3 interior, 3 exterior, 3 product/service, 3 team — upload 100+ for best results | Medium-High — photos increase engagement |
| Posts | 1+ per week (offers, events, updates) | Medium — engagement signal |
| Q&A | Monitor and answer all questions promptly | Medium |
| Reviews | Respond to ALL reviews (positive AND negative) within 24 hours | Very high — review engagement is a key signal |

#### 4.2 Local Citation Building

| Citation Tier | Platforms | Priority |
|---|---|---|
| Tier 1 (Major) | Google, Bing, Apple Maps, Yelp, Facebook, Nextdoor | Essential |
| Tier 2 (Data Aggregators) | Infogroup, Neustar/Localeze, Factual, Foursquare | Essential for distribution |
| Tier 3 (Industry) | Yelp, Angi (for home services), TripAdvisor (for hospitality), Healthgrades (for medical), Zocdoc (for healthcare) | Industry-dependent |
| Tier 4 (Local) | Chamber of Commerce, local directories, local news, local blogs | Boost local relevance |

**NAP Consistency Rules:**
- Name, Address, Phone must be EXACTLY identical across every citation
- Same abbreviation patterns (e.g., "Street" vs "St." — pick one)
- Same formatting (suite number style, zip code punctuation)
- Use a citation tracking tool (Moz Local, BrightLocal, Yext) to audit

#### 4.3 Local Link Building

| Tactic | Difficulty | Impact |
|---|---|---|
| Sponsor local events or charities | Medium | High — .org links from community orgs |
| Join local Chamber of Commerce | Easy | Medium — typically includes directory listing |
| Partner with local businesses | Medium | High — cross-promotion + links |
| Host local workshops/events | Medium | High — event coverage + links |
| Local press releases (newsworthy only) | Medium | Medium — can generate citations + links |
| Local blog/PR outreach | Hard | High — local media links are powerful |

### 5. Competitor Backlink Analysis

#### 5.1 Backlink Quality Assessment

| Metric | Good | Moderate | Poor |
|---|---|---|---|
| Domain Rating (DR) / Authority | 50+ | 30–49 | < 30 |
| Referring Domains | 100+ (for competitive niches) | 20–99 | < 20 |
| Do-follow ratio | 60%+ | 40–59% | < 40% |
| Link context | Editorial, relevant, within content | Sidebar, footer, directory | Comment spam, paid links, PBNs |
| Anchor text diversity | < 30% exact match | 30–50% exact match | > 50% exact match |
| IP diversity (C-class) | 50+ unique C-blocks | 10–49 | < 10 |

#### 5.2 Backlink Gap Analysis

Use Ahrefs, SEMrush, or Moz to find competitor backlinks that you don't have:

1. Export top 100 referring domains for each of your top 3 competitors
2. Remove domains you already have links from
3. Filter by Domain Rating (DR 40+)
4. Filter by relevance (topically related to your niche)
5. Prioritize by: DR × Relevance × Link Type (editorial > directory)

**Outreach workflow:**
```
Identify link opportunity → Find contact (Hunter.io, Apollo) → 
Craft personalized email → Mention why you like their content → 
Suggest your resource as an addition → Follow up (day 7, day 14) → 
Track in a CRM / spreadsheet
```

#### 5.3 Common Link Building Tactics

| Tactic | Effort | Results Timeline | Risk |
|---|---|---|---|
| Guest posting | High | 1–3 months | Low (if high-quality sites) |
| Skyscraper technique (better content + outreach) | High | 2–4 months | Low |
| Broken link building (find broken links, suggest replacement) | Medium | 1–3 months | Low |
| Ego bait (interview experts, feature influencers) | Medium | 1–3 months | Low |
| Linkable assets (original research, infographics, tools) | Very high | 3–6 months | Low |
| Resource page link building | Medium | 1–2 months | Medium (if low-quality pages) |
| HARO / Qwoted / Featured (journalist requests) | Medium | Varies (daily pitches) | Low |
| PR / digital PR (newsworthy stories) | High | 3–6 months | Low |
| Unlinked brand mentions | Low | 2–4 weeks | Very low |
| Forum / Q&A links | Low | Immediate | High (if spammy) |

### 6. SEO Performance Tracking

#### 6.1 KPI Dashboard

| KPI | Tool | Frequency | Target |
|---|---|---|---|
| Organic Traffic | Google Analytics / GSC | Weekly | +10–20% MoM (growth phase) |
| Keyword Rankings | Ahrefs / SEMrush / GSC | Weekly | Page 1 for target terms |
| Click-Through Rate (CTR) | GSC | Monthly | Improve 1–2% per quarter |
| Impressions | GSC | Weekly | Track volume trend |
| Conversion Rate (Organic) | GA4 | Monthly | Match or exceed site average |
| Bounce Rate (Organic) | GA4 | Monthly | < 55% (content) / < 40% (product) |
| Core Web Vitals Pass Rate | GSC (Core Web Vitals report) | Monthly | 75%+ of URLs pass |
| Indexed Pages | GSC | Weekly | Growing, stable, no sudden drops |
| Backlinks (Referring Domains) | Ahrefs / SEMrush | Monthly | +5–10% MoM |
| Domain Authority / Rating | Moz / Ahrefs | Monthly | +1–3 per quarter |
| Page Load Time | PageSpeed Insights | Monthly | < 2.5s on mobile |

#### 6.2 Traffic Impact Equation

```
Organic Revenue = (Impressions × CTR × CVR × AOV)

Where:
- Impressions ∝ Number of indexed pages × Keyword difficulty coverage
- CTR ∝ Title/meta optimization × Rich result presence × Brand recognition
- CVR ∝ Content intent alignment × Page load speed × Trust signals
- AOV ∝ Product/offer quality × Cross-sell effectiveness
```

## Common Pitfalls

1. **Targeting keywords that are too competitive:** A new site should not target "CRM software" (KD 90+) in year one. Start with long-tail terms (KD < 40) and build domain authority.
2. **Keyword cannibalization:** Multiple pages targeting the same keyword compete against each other. Use a keyword → page mapping spreadsheet. Redirect or merge cannibalizing pages.
3. **Ignoring search intent:** Ranking #1 for an informational query won't generate revenue if your page tries to sell instead of teach. Match content type to intent.
4. **Thin content:** Pages under 300 words rarely rank for competitive terms. Most top-10 results have 1,500+ words. Go deep or go home.
5. **Over-optimizing anchor text:** If 40%+ of your backlinks use exact-match anchor text, you risk a Penguin penalty. Vary anchors naturally.
6. **Neglecting mobile SEO:** Google is mobile-first indexed. If your mobile site is slow or has poor UX, desktop rankings suffer too.
7. **No redirect plan for site migrations:** A site migration without proper 301 mapping can lose 50–90% of organic traffic. Map every old URL → new URL before the move.
8. **Buying links or using PBNs:** This violates Google's guidelines. When caught (and you will be), the penalty is manual action, traffic collapse, and recovery taking 6–12 months.
9. **Only creating content, never updating:** The SEO landscape changes constantly. Pages written in 2022 need 2025 updates. Set a 6-month refresh cadence for cornerstone content.
10. **No local NAP audit:** If your NAP is inconsistent across even two major directories, local rankings suffer significantly. Audit quarterly.

## Verification Checklist

- [ ] Keyword research completed: 50+ keywords mapped to intent and difficulty
- [ ] Keyword-page mapping prevents cannibalization (one keyword per page)
- [ ] Title tags optimized for all key pages (50–60 chars, keyword-forward)
- [ ] Meta descriptions written for all pages (150–160 chars, includes CTA)
- [ ] Heading structure correct: one H1 per page, logical H2/H3 hierarchy
- [ ] XML sitemap generated, submitted to Google Search Console
- [ ] robots.txt configured correctly (allows Google, blocks admin)
- [ ] Canonical tags set correctly across all pages
- [ ] Structured data (JSON-LD) implemented on key page types
- [ ] Core Web Vitals pass for 75%+ of URLs (LCP < 2.5s, FID < 100ms, CLS < 0.1)
- [ ] HTTPS enforced with 301 redirect from HTTP
- [ ] Mobile responsive test passed (Google Mobile-Friendly Test)
- [ ] Page speed optimized: < 2.5s on mobile, < 1.5s on desktop
- [ ] Internal linking strategy mapped (pillar pages connected to cluster content)
- [ ] Google Business Profile claimed and fully optimized
- [ ] NAP consistent across top 10+ local citations
- [ ] Competitor backlink analysis completed (top 3 competitors)
- [ ] Link building plan documented (3+ tactics, outreach templates ready)
- [ ] Google Search Console and GA4 set up with SEO dashboard
- [ ] Baseline rankings recorded for target keywords
- [ ] Content freshness schedule set (6-month review for cornerstone content)
- [ ] Crawl budget audit completed (Screaming Frog or equivalent)
