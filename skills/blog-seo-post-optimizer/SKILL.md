---
name: blog-seo-post-optimizer
description: "Use when optimizing blog posts for SEO. Keyword checks."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [blog, seo, on-page, optimization, search]
    related_skills: [blog-post-outliner, blog-analytics-interpreter, blog-idea-generator]
---

# Blog SEO Post Optimizer

## Overview

A comprehensive on-page SEO optimization framework for individual blog posts. Covers keyword placement (title, H1, H2s, first 100 words, image filenames, alt text), readability (Flesch-Kincaid, sentence length, paragraph breaks), internal/external linking strategy, schema markup (Article, FAQ, HowTo), and meta optimization. Run this on every post before publishing.

## When to Use

- You've finished a draft and need SEO optimization before publishing
- You're auditing existing posts for SEO improvement
- You're preparing a post targeting a specific keyword for the first time
- You need to validate that schema markup is correct

## Keyword Placement

### Primary Keyword Checklist

| Location | Required? | Best Practice |
|----------|-----------|---------------|
| **URL slug** | ✓ Required | Exact match or close variant, lowercase, hyphens |
| **H1 title** | ✓ Required | Near the beginning of the title |
| **First 100 words** | ✓ Required | Appear naturally in first paragraph |
| **Meta title** | ✓ Required | Exact match preferred, near start of title tag |
| **Meta description** | ✓ Required | Include keyword, make sound natural |
| **At least one H2** | ✓ Required | Ideally the first H2 after the intro |
| **Image alt text** | ✓ Required (1+ image) | Describe the image naturally |
| **Image filename** | Recommended | `keyword-phrase.jpg` not `IMG_4923.jpg` |
| **Open Graph title** | Recommended | Include keyword for social share impact |
| **Body (2–3 more times)** | Recommended | Natural use at 2–3 additional spots |
| **Conclusion paragraph** | Optional | Tie it back in the final summary |

### Secondary Keyword Placement

- 2–3 related H2s should contain secondary keywords
- 1–2 image alt text entries per secondary keyword
- Spread across the post body (1 mention per ~500 words)

### Keyword Stuffing Warning Signs

- Same keyword repeated in 3+ consecutive sentences
- Keywords in places they don't make sense (unnatural alt text)
- Keyword density > 3% of total word count
- The post feels like it was written for search engines, not humans

## Readability Optimization

### Target Metrics

| Metric | Target Range | Tool |
|--------|-------------|------|
| Flesch-Kincaid Grade Level | 6–9 (broad), 9–12 (technical) | Hemingway, Yoast, Grammarly |
| Avg Sentence Length | 14–20 words | Readable.com, Hemingway |
| Paragraph Length | 2–4 sentences (3–5 lines max) | Visual scan |
| Passive Voice | < 10% of sentences | Hemingway |
| Transition Words | 1 per paragraph | Yoast SEO readability check |

### Readability Rules

1. **One idea per sentence.** Split compound sentences at every "and" or "but" when the halves can stand alone.
2. **Vary sentence length.** After a long sentence (20+ words), follow with a short one (5–10 words).
3. **Use subheadings (H3s) every 300–400 words** in long sections.
4. **Keep paragraphs short.** On mobile, no paragraph should exceed 3 lines.
5. **Use transitions between H2 sections:** "Beyond [prior point], there's another factor to consider: [next point]."
6. **Prefer active voice.** "Google ranks this higher" instead of "This is ranked higher by Google."

## Internal & External Linking

### Internal Links

**Count:** 2–5 internal links per 1,000 words.

**Strategy:**
| Link Type | Purpose | Anchor Text |
|-----------|---------|-------------|
| **Contextual** | Link to related deep dive mid-article | Keyword-rich ("See our complete guide on keyword research") |
| **Supporting** | Link to a case study or data source | Descriptive ("According to our 2024 study...") |
| **Pillar** | Link to the pillar page covering broader topic | Broad match ("Learn more about content marketing") |
| **Hub** | Link to category/tag page | Navigational ("Explore all SEO guides") |

**Rules:**
- Link to pages with 500+ words of content (no thin pages)
- No orphan posts — every post should have incoming internal links from at least 2 others
- Use `nofollow` only on login pages, privacy policies, and paid links
- Update at least 2 older posts to link to this new post at publish time

### External Links

**Count:** 1–5 external links (authority citations or data sources).

**Strategy:**
- Link to authoritative sources (Google, academic papers, industry studies, .gov/.edu domains)
- Link to tools/resources you're recommending
- Open in same tab (default) — no `target="_blank"` for editorial links unless it's a tool/page the reader needs to use separately
- Use `rel="noopener"` on all external links for security

## Schema Markup

### Article Schema (Required)

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Your Post Title",
  "description": "Meta description",
  "image": "https://example.com/images/post-hero.jpg",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "url": "https://example.com/author/name"
  },
  "datePublished": "2025-01-15T08:00:00-05:00",
  "dateModified": "2025-01-15T08:00:00-05:00",
  "publisher": {
    "@type": "Organization",
    "name": "Your Site",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://example.com/post"
  }
}
```

### FAQ Schema (Use When Post Has 3+ Q&A Pairs)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Question 1",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Answer text."
    }
  }]
}
```

### HowTo Schema (Use When Post Has Step-by-Step Instructions)

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to [Task]",
  "description": "Brief description.",
  "step": [
    {
      "@type": "HowToStep",
      "position": 1,
      "name": "Step 1",
      "text": "Step description."
    }
  ],
  "totalTime": "PT30M"
}
```

**Validation Tools:**
- Google Rich Results Test: `https://search.google.com/test/rich-results`
- Schema.org Validator: `https://validator.schema.org/`
- Yoast/WordPress plugin has built-in schema validation

## Meta Optimization

### Meta Title
| Element | Rule |
|---------|------|
| Length | 50–60 characters |
| Keyword | Include primary keyword, ideally near the beginning |
| Brand | Add brand name after pipe or dash if room |
| Click-Through Hook | Include a benefit, number, or power word |
| No duplication | Every meta title must be unique |

**Patterns:**
```
[Primary Keyword]: [Benefit/Subtitle] | [Brand]
[Number] [Power Word] [Keyword] [CTA] | [Brand]
[Question Keyword]? Here's [Answer] | [Brand]
```

### Meta Description
| Element | Rule |
|---------|------|
| Length | 150–160 characters |
| Keyword | Include primary keyword once naturally |
| Action | Include a CTA or what the reader will learn |
| Uniqueness | Every meta description must be unique |
| Format | Complete sentence, compelling, not just a summary |

**Pattern:**
```
[Primary Keyword] — [benefit/value statement]. [CTA: Learn/Discover/Find out] [what they get].
```

### Open Graph Tags
```html
<meta property="og:title" content="Post Title for Social (under 60 chars)" />
<meta property="og:description" content="Compelling description for social feeds" />
<meta property="og:image" content="https://example.com/images/social-share-1200x630.jpg" />
<meta property="og:url" content="https://example.com/post" />
<meta property="og:type" content="article" />
```

### Twitter Card Tags
```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Post Title" />
<meta name="twitter:description" content="Description for Twitter feed" />
<meta name="twitter:image" content="https://example.com/images/social-share-1200x630.jpg" />
```

**Image spec:** 1200×630 px, < 1 MB, JPEG or PNG, text overlay optional.

## Quick Audit Script (Python)

```python
#!/usr/bin/env python3
"""Basic on-page SEO audit from a markdown file."""
import re, sys
from pathlib import Path

def audit(filepath):
    content = Path(filepath).read_text()
    words = content.split()
    sentences = re.split(r'[.!?]+', content)
    word_count = len(words)
    avg_sentence = round(word_count / max(len(sentences), 1))
    h1s = re.findall(r'^# (.+)$', content, re.MULTILINE)
    h2s = re.findall(r'^## (.+)$', content, re.MULTILINE)
    images = re.findall(r'!\[.*?\]\((.+?)\)', content)
    
    report = f"=== SEO Audit: {filepath} ===\n"
    report += f"Word Count: {word_count}\n"
    report += f"Avg Sentence Length: {avg_sentence} words\n"
    report += f"H1 Tags: {len(h1s)} {'✓' if len(h1s)==1 else '✗ (need exactly 1)'}\n"
    report += f"H2 Tags: {len(h2s)} {'✓' if len(h2s)>=3 else '✗ (aim for 3+)'}\n"
    report += f"Images: {len(images)} {'✓' if len(images)>=1 else '✗ (add at least 1)'}\n"
    report += f"Internal Links: {len(re.findall(r'\[.*?\]\(/.*?\)', content))}\n"
    report += f"External Links: {len(re.findall(r'\[.*?\]\(https?://.*?\)', content))}\n"
    
    if h1s:
        report += f"Primary keyword in H1: CHECK MANUALLY\n"
    
    print(report)

if __name__ == "__main__":
    audit(sys.argv[1]) if len(sys.argv) > 1 else print("Usage: python audit.py post.md")
```

## Common Pitfalls

- **Targeting impossible keywords:** If DR < 30, don't target KD > 30 keywords
- **Over-optimization (keyword stuffing):** Google's NLP understands synonyms — you don't need exact keyword 15 times
- **Meta description not unique:** Every page needs distinct meta
- **Missing alt text:** Screen readers and Google Images rely on it
- **All internal links are navigational:** Deep contextual links pass authority — add mid-content links
- **No FAQ section:** FAQ schema often doubles featured snippet capture rate
- **Ignoring Core Web Vitals:** On-page text SEO doesn't matter if the page is slow
- **Canonical issues:** Wrong or missing canonical URL causes split ranking signals
- **Duplicate title/description:** A CMS that fills both from same field kills unique ranking

## Verification Checklist

- [ ] Primary keyword present in URL slug, H1, first 100 words, meta title, meta description, and 1+ H2
- [ ] Secondary keywords appear in 2–3 H2s and 1–2 image alt texts
- [ ] Keyword density < 3%
- [ ] Flesch-Kincaid grade level within target range
- [ ] Avg sentence length 14–20 words
- [ ] Passive voice < 10%
- [ ] 2–5 internal links per 1,000 words
- [ ] 1–5 external links to authoritative sources
- [ ] Article schema markup present and passes Google Rich Results Test
- [ ] FAQ or HowTo schema applied if content matches type
- [ ] Meta title: 50–60 chars, keyword near start, unique per page
- [ ] Meta description: 150–160 chars, keyword included, unique per page
- [ ] OG tags: title, description, image (1200×630), url all set
- [ ] Twitter card tags: summary_large_image set with image URL
- [ ] Canonical URL set correctly
- [ ] Post passes Core Web Vitals (test with PageSpeed Insights)