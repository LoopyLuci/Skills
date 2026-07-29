---
name: seo-search-engine-optimization
description: "Use when implementing SEO strategies and technical audits."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [seo, search-engine-optimization, keyword-research, technical-seo, content-optimization]
    related_skills: [website-analytics-tracking, content-writing-seo-copy, cms-website-management, digital-marketing-strategy]
---

# Search Engine Optimization (SEO)

Implementing comprehensive SEO strategies — keyword research, on-page optimization, technical SEO, link building, content strategy, and performance tracking.

## When to Use

- Improving organic search rankings for a website
- Conducting SEO audits and identifying issues
- Performing keyword research for content planning
- Implementing technical SEO (schema, core web vitals, sitemaps)
- Building an SEO content strategy aligned with business goals

## SEO Pillars

```
Technical SEO — site structure, speed, mobile, indexing, crawlability
On-Page SEO — content, keywords, meta tags, headings, internal links
Off-Page SEO — backlinks, social signals, brand mentions, PR
Content SEO — topical authority, content clusters, EEAT
```

## Keyword Research

```python
import json
from typing import List, Dict, Tuple

class KeywordResearch:
    """Keyword discovery, analysis, and clustering."""
    
    # Simulated keyword data (in practice, use Ahrefs/SEMRush/Google API)
    
    @staticmethod
    def analyze_keyword(keyword: str, volume: int = None, 
                        difficulty: int = None) -> Dict:
        """Analyze a keyword for SEO potential."""
        return {
            'keyword': keyword,
            'search_volume': volume or 0,
            'difficulty': difficulty or 50,  # 0-100
            'intent': KeywordResearch.classify_intent(keyword),
            'cpc': None,  # From keyword tool
            'trend': 'stable',
        }
    
    @staticmethod
    def classify_intent(keyword: str) -> str:
        """Classify search intent: informational, navigational, commercial, transactional."""
        keyword_lower = keyword.lower()
        
        transactional = ['buy', 'purchase', 'order', 'price', 'cost', 'discount', 
                        'coupon', 'deal', 'cheap', 'subscribe']
        commercial = ['best', 'top', 'review', 'comparison', 'vs', 'versus',
                     'alternative', 'rating', 'recommended', '2024', '2025']
        navigational = ['login', 'sign in', 'dashboard', 'homepage', 'official']
        
        if any(w in keyword_lower for w in transactional):
            return 'transactional'
        if any(w in keyword_lower for w in commercial):
            return 'commercial'
        if any(w in keyword_lower for w in navigational):
            return 'navigational'
        return 'informational'
    
    @staticmethod
    def cluster_keywords(keywords: List[str]) -> Dict[str, List[str]]:
        """Group keywords into topical clusters."""
        # Simple topic extraction: use the first 1-2 words as cluster key
        clusters = {}
        for kw in keywords:
            words = kw.lower().split()
            if len(words) >= 2:
                cluster_key = ' '.join(words[:2])
            else:
                cluster_key = words[0]
            clusters.setdefault(cluster_key, []).append(kw)
        return clusters
    
    @staticmethod
    def opportunity_score(keyword: Dict) -> float:
        """Score keywords by opportunity (high volume, low difficulty = high score)."""
        volume = keyword.get('search_volume', 0)
        difficulty = keyword.get('difficulty', 50)
        if difficulty == 0:
            return 0
        return round(volume / difficulty, 1)
```

## On-Page SEO Optimizer

```python
class OnPageSEO:
    """Optimize on-page SEO elements for a page."""
    
    TITLE_LENGTH_MAX = 60
    META_DESC_LENGTH = 160
    HEADING_HIERARCHY = ['h1', 'h2', 'h3', 'h4']
    
    @staticmethod
    def optimize_title(title: str, keyword: str, brand: str = "") -> Dict:
        """Create an SEO-optimized title tag."""
        
        # Patterns
        titles = [
            f"{keyword}: {title[:40]}",
            f"{keyword} — {title[:40]}",
            f"{title[:45]} | {brand}",
            f"{title[:50]} [{keyword}]",
        ]
        
        best = None
        for t in titles:
            if len(t) <= OnPageSEO.TITLE_LENGTH_MAX:
                best = t
                break
        
        return {
            'title': best or titles[0][:OnPageSEO.TITLE_LENGTH_MAX],
            'length': len(best) if best else len(titles[0]),
            'keyword_included': keyword.lower() in (best or titles[0]).lower(),
            'recommendation': 'Good' if best and len(best) <= OnPageSEO.TITLE_LENGTH_MAX else 'Truncate'
        }
    
    @staticmethod
    def optimize_meta_description(description: str, keyword: str) -> Dict:
        """Create an SEO-optimized meta description."""
        # Ensure keyword appears naturally
        if keyword.lower() not in description.lower():
            description = f"{description[:120]} — {keyword}"
        
        # Include call to action
        ctas = ["Learn more", "Get started", "Read the guide", "Discover how"]
        has_cta = any(cta.lower() in description.lower() for cta in ctas)
        if not has_cta:
            description += f" {ctas[0]} today."
        
        return {
            'description': description[:OnPageSEO.META_DESC_LENGTH],
            'length': min(len(description), OnPageSEO.META_DESC_LENGTH),
            'keyword_included': keyword.lower() in description.lower(),
            'has_cta': has_cta,
        }
    
    @staticmethod
    def analyze_content(content: str, keyword: str) -> Dict:
        """Analyze content for SEO best practices."""
        from collections import Counter
        import re
        
        words = re.findall(r'\w+', content.lower())
        word_count = len(words)
        
        # Keyword density
        keyword_words = keyword.lower().split()
        keyword_count = sum(1 for i in range(len(words) - len(keyword_words) + 1)
                          if words[i:i+len(keyword_words)] == keyword_words)
        
        # Heading structure
        h1s = len(re.findall(r'^# .+', content, re.MULTILINE))
        h2s = len(re.findall(r'^## .+', content, re.MULTILINE))
        h3s = len(re.findall(r'^### .+', content, re.MULTILINE))
        
        # Readability (simplified Flesch)
        sentences = len(re.findall(r'[.!?]+', content))
        avg_words_per_sentence = word_count / max(sentences, 1)
        
        recommendations = []
        if word_count < 300: recommendations.append("Content too short (<300 words)")
        if keyword_count == 0: recommendations.append("Keyword not found in content")
        if h1s != 1: recommendations.append(f"Expected 1 H1, found {h1s}")
        if h2s < 3: recommendations.append("Add more H2 subheadings")
        if avg_words_per_sentence > 25: recommendations.append("Sentences too long, break them up")
        
        return {
            'word_count': word_count,
            'keyword_occurrences': keyword_count,
            'keyword_density_pct': round(keyword_count / max(word_count, 1) * 100, 2),
            'headings': {'h1': h1s, 'h2': h2s, 'h3': h3s},
            'readability_score': round(max(0, 100 - avg_words_per_sentence * 2), 0),
            'recommendations': recommendations,
        }
```

## Technical SEO Audit

```python
class TechnicalSEO:
    """Technical SEO audit and recommendations."""
    
    @staticmethod
    def audit_url(url: str) -> Dict:
        """Basic technical SEO audit for a URL."""
        import re
        
        issues = []
        
        # URL structure
        if len(url) > 100:
            issues.append("URL too long")
        if re.search(r'[A-Z]', url):
            issues.append("URL contains uppercase characters")
        if '_' in url:
            issues.append("URL contains underscores (use hyphens)")
        if re.search(r'\d{8,}', url):
            issues.append("URL contains date (duplicate content risk)")
        
        # Check for common patterns
        checks = {
            'has_www': 'www.' in url,
            'has_https': url.startswith('https://'),
            'has_trailing_slash': url.endswith('/') if not url.endswith('.html') else True,
            'url_length': len(url),
            'parameters': '?' in url,
        }
        
        if not checks['has_https']:
            issues.append("Not using HTTPS")
        if checks['parameters']:
            issues.append("URL contains query parameters (canonicalize)")
        
        return {
            'url': url,
            'checks': checks,
            'issues': issues,
            'score': max(0, 100 - len(issues) * 15),
        }
    
    @staticmethod
    def generate_sitemap(urls: List[str], base_url: str) -> str:
        """Generate an XML sitemap."""
        from datetime import datetime
        
        sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        for url in urls:
            sitemap += '  <url>\n'
            sitemap += f'    <loc>{url}</loc>\n'
            sitemap += f'    <lastmod>{datetime.now().date().isoformat()}</lastmod>\n'
            sitemap += '    <changefreq>monthly</changefreq>\n'
            sitemap += '    <priority>0.8</priority>\n'
            sitemap += '  </url>\n'
        
        sitemap += '</urlset>'
        return sitemap
    
    @staticmethod
    def generate_robots_txt(allow_all: bool = True, sitemap_url: str = None) -> str:
        """Generate robots.txt content."""
        lines = []
        if allow_all:
            lines.append("User-agent: *")
            lines.append("Disallow:")
        else:
            lines.append("User-agent: *")
            lines.append("Disallow: /admin/")
            lines.append("Disallow: /private/")
            lines.append("Disallow: /temp/")
        
        if sitemap_url:
            lines.append(f"\nSitemap: {sitemap_url}")
        
        return '\n'.join(lines)
```

## Common Pitfalls

1. **Keyword cannibalization** — multiple pages targeting the same keyword; consolidate or differentiate
2. **Content thinness** — 200-word pages won't rank; aim for comprehensive coverage (1,500+ words)
3. **Ignoring search intent** — ranking for "best coffee maker" with a product page when users want comparisons
4. **Over-optimization** — keyword stuffing and unnatural links trigger penalties; focus on user value
5. **Technical debt** — slow pages, broken links, missing alt text compound; run monthly audits
6. **Ranking ≠ revenue** — ranking for high-volume keywords that don't convert; align SEO with business goals

## Verification Checklist

- [ ] Keyword research completed with intent classification
- [ ] Title tags optimized (≤60 chars, includes keyword)
- [ ] Meta descriptions written (≤160 chars, includes CTA)
- [ ] URL structure clean (hyphens, lowercase, short)
- [ ] Heading hierarchy (h1 → h2 → h3) logical
- [ ] Core Web Vitals meet Google thresholds
- [ ] XML sitemap submitted to Google Search Console
- [ ] robots.txt configured correctly
- [ ] Canonical tags set to avoid duplicate content
- [ ] Mobile responsive verified
- [ ] Schema markup added (where applicable)
- [ ] Internal linking structure reviewed

## See Also

- website-analytics-tracking — measuring SEO impact
- content-writing-seo-copy — writing optimized content
- cms-website-management — implementing SEO in CMS
- digital-marketing-strategy — integrating SEO with broader strategy
