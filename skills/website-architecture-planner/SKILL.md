---
name: website-architecture-planner
description: "Use when planning site structure. IA, sitemaps."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [website, information-architecture, sitemap, wireframe, planning]
    related_skills: [static-site-generator-workflow, wordpress-development]
---

# Website Architecture Planner

## Overview
Plan complete website information architecture: sitemap generation, content hierarchy, navigation design, URL strategy, page type definitions, and wireframe outlines. Produces a full website blueprint document.

## When to Use
- "Plan the structure for my new website"
- "Design an information architecture"
- "Help me organize my site's content"

## Sitemap Generation
Build a hierarchical sitemap:

```
Home
├── About
│   ├── Our Story
│   ├── Team
│   └── Careers
├── Services
│   ├── Service A
│   ├── Service B
│   └── Service C
├── Resources
│   ├── Blog
│   ├── Case Studies
│   ├── Whitepapers
│   └── FAQ
└── Contact
    ├── Locations
    └── Support
```

### Flat vs Deep Architecture
- **Flat (<3 levels)**: Better for SEO, user experience. Limit to 2-3 clicks to any page.
- **Deep (>3 levels)**: Only for massive sites (500+ pages) with clear navigation paths.

## Navigation Design
| Navigation Type | Purpose | Best For |
|----------------|---------|----------|
| Primary nav | Main pages visitors need | Top 5-7 pages |
| Secondary nav | Supporting content | Resources, legal, about |
| Footer nav | Everything else in groups | Policies, contact, social |
| Breadcrumbs | Show location + SEO | Every inner page |
| Sidebar nav | Sub-page navigation | Documentation, courses |

Apply the "three-click rule": any page should be reachable in ≤3 clicks from any other page.

## URL Structure Strategy
- Use descriptive, keyword-rich slugs: `example.com/services/web-design` not `example.com/services/?p=123`
- Keep under 5 segments: `domain/category/post-name` ideal
- Use hyphens, not underscores: `web-design` not `web_design`
- Lowercase only: `/Services/Web-Design/` → `/services/web-design/`
- Avoid dates in URLs unless time-sensitive content

## Page Type Definitions
| Page Type | Purpose | Content Required |
|-----------|---------|-----------------|
| Homepage | Orientation, top conversions | H1, hero, social proof, top CTAs, value prop |
| Landing Page | Single conversion goal | Target headline, benefit bullets, form/CTA, trust signals |
| Blog Post | SEO, education, authority | Headline, body, featured image, meta, author |
| Product/Service | Sell an offering | Features, benefits, pricing, testimonials, FAQ |
| About | Trust-building | Story, team, mission, values, press mentions |
| Contact | Lead generation | Form, map, phone, email, hours |
| FAQ | Reduce support, SEO | Questions as H2s, answers below |
| Resource/Library | Content hub | Filtered grid/search, categories, featured items |

## Wireframe Outlines
Use the `sketch` tool or describe layout in markdown tables:
```
[Hero: Headline + Subheading + CTA Button]
[Social Proof: Logo bar of 3-5 companies]
[Features: 3-column grid with icons]
[Testimonials: Carousel of 3 quotes]
[FAQ: Accordion of top 5 questions]
[CTA: Final bold section]
[Footer: Links, social, legal]
```

## Common Pitfalls
1. **Ignoring mobile navigation** — hamburger menus on desktop are lazy; use responsive navigation
2. **Content-first, structure-second** — structure must follow content needs, not the other way around
3. **Orphan pages** — every page needs a link from at least one other page
4. **Overloaded primary nav** — 7+ items overwhelms users; group and stack
5. **No 404 strategy** — plan a helpful 404 page with search and popular links

## Verification Checklist
- [ ] Full hierarchical sitemap created  
- [ ] Navigation design (primary/secondary/footer/breadcrumb) planned
- [ ] URL structure strategy defined
- [ ] All page types documented (homepage, landing, blog, etc.)
- [ ] Wireframe outline for each top-level page type
- [ ] Mobile navigation plan included
- [ ] Every page has an inbound link path