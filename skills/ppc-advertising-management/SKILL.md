---
name: ppc-advertising-management
description: "Use when managing pay-per-click advertising campaigns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ppc, advertising, google-ads, paid-search, SEM, bidding, keywords]
    related_skills: [social-media-advertising, seo-search-engine-optimization, conversion-rate-optimization, digital-marketing-strategy]
---

# PPC Advertising Management

Managing pay-per-click advertising campaigns across search and display networks — from keyword research and ad copy through bidding strategies, quality score optimization, and performance analysis.

## When to Use

- Running Google Ads (formerly AdWords) campaigns
- Managing Bing Ads or other search engine marketing
- Building and optimizing keyword lists
- Writing ad copy for search and display ads
- Analyzing PPC performance and optimizing ROI

## Campaign Structure

```
Account
└── Campaigns (by product, location, funnel stage)
    ├── Ad Groups (by theme/keyword cluster)
    │   ├── Keywords (match types)
    │   └── Ads (variants for testing)
    ├── Ad Groups
    └── ...
```

## Keyword Research

```python
from typing import Dict, List, Optional
from datetime import datetime

class PPCKeywordResearch:
    """Research and organize PPC keywords."""
    
    MATCH_TYPES = {
        'exact': '[keyword] — Exact match, close variants only',
        'phrase': '"keyword" — Phrase match, words in order',
        'broad': 'keyword — Broad match, related searches',
        'broad_modified': '+keyword — Broad with mandatory terms',
    }
    
    @staticmethod
    def organize_into_themes(keywords: List[str]) -> Dict[str, List[str]]:
        """Group keywords into themed ad groups."""
        themes = {}
        for kw in keywords:
            words = kw.lower().split()
            # Use first 1-2 words as theme key
            key = ' '.join(words[:2]) if len(words) > 1 else words[0]
            themes.setdefault(key, []).append(kw)
        return themes
    
    @staticmethod
    def generate_negative_keywords(keywords: List[str]) -> List[str]:
        """Suggest negative keywords to exclude irrelevant traffic."""
        negatives = []
        for kw in keywords:
            parts = kw.lower().split()
            # Free/cheap variations
            if 'free' in parts: negatives.append('free')
            if 'cheap' in parts: negatives.append('cheap')
            if 'job' in parts: negatives.extend(['job', 'jobs', 'career', 'hiring'])
        return list(set(negatives))
```

## Ad Copy Generator

```python
class PPCAdCopy:
    """Generate and test PPC ad copy variants."""
    
    @staticmethod
    def generate(headline: str, keyword: str, url: str, 
                 benefits: List[str]) -> Dict:
        """Generate Responsive Search Ad variants."""
        headlines = [
            f"{headline} — {benefits[0]}" if benefits else headline,
            f"{keyword} — Get Started Today",
            f"Save on {keyword}",
            f"{keyword}: {benefits[0] if benefits else 'Learn More'}",
            f"Official {keyword} Site",
        ]
        
        descriptions = [
            f"{benefits[0] if benefits else 'Premium service'}. "
            f"{benefits[1] if len(benefits) > 1 else ''} Call us today!",
            f"Looking for {keyword}? We offer {benefits[0].lower() if benefits else 'competitive pricing'}."
            f" {benefits[2] if len(benefits) > 2 else 'Get a free quote'}",
        ]
        
        return {
            'final_url': url,
            'headlines': headlines[:5],
            'descriptions': descriptions,
            'suggested_path': keyword.lower().replace(' ', '-')[:15],
        }
    
    @staticmethod
    def generate_ad_extensions(business: Dict) -> Dict:
        """Generate ad extensions for better CTR."""
        return {
            'sitelink_extensions': [
                {'text': 'Products', 'url': f"{business.get('url')}/products"},
                {'text': 'About Us', 'url': f"{business.get('url')}/about"},
                {'text': 'Contact', 'url': f"{business.get('url')}/contact"},
            ],
            'call_extension': business.get('phone'),
            'location_extension': business.get('address'),
            'callout_extensions': business.get('callouts', []),
        }
```

## Bid Management

```python
class BidManager:
    """Manage PPC bids and bidding strategies."""
    
    STRATEGIES = {
        'manual_cpc': 'Full control over individual bids',
        'enhanced_cpc': 'Auto-adjusts bids for higher conversions',
        'target_cpa': 'Auto-bids to hit target cost per acquisition',
        'target_roas': 'Auto-bids to hit target return on ad spend',
        'maximize_clicks': 'Get the most clicks within budget',
        'maximize_conversions': 'Get the most conversions within budget',
        'target_impression_share': 'Show ads on a specific % of eligible impressions',
    }
    
    @staticmethod
    def suggest_bid(keyword: str, avg_cpc: float, conversion_rate: float,
                    target_cpa: float, max_bid: float = None) -> Dict:
        """Suggest optimal bid for a keyword."""
        # Calculate max bid from target CPA
        cpa_based_bid = target_cpa * conversion_rate if conversion_rate > 0 else avg_cpc
        
        # Position-based adjustment
        first_page_bid = avg_cpc * 1.5
        top_of_page_bid = avg_cpc * 2.5
        
        recommended = min(cpa_based_bid, max_bid or float('inf'))
        
        return {
            'keyword': keyword,
            'avg_cpc_reference': round(avg_cpc, 2),
            'cpa_based_bid': round(cpa_based_bid, 2),
            'first_page_bid': round(first_page_bid, 2),
            'top_of_page_bid': round(top_of_page_bid, 2),
            'recommended_bid': round(recommended, 2),
            'max_bid_set': max_bid,
        }
```

## Quality Score Optimization

```python
class QualityScoreOptimizer:
    """Optimize Google Ads Quality Score."""
    
    FACTORS = {
        'expected_ctr': 'How likely your ad is to be clicked (relative to others)',
        'ad_relevance': 'How closely your ad matches the search intent',
        'landing_page_exp': 'How relevant and useful your landing page is',
    }
    
    @staticmethod
    def analyze(keyword: str, ad: Dict, landing_page_url: str) -> List[str]:
        """Analyze and suggest Quality Score improvements."""
        recommendations = []
        
        # Ad relevance check
        keyword_words = set(keyword.lower().split())
        ad_text = f"{ad.get('headline', '')} {ad.get('description', '')}".lower()
        if not any(kw in ad_text for kw in keyword_words):
            recommendations.append("Add keyword to ad copy for better relevance")
        
        # Landing page relevance
        if not landing_page_url:
            recommendations.append("Ensure landing page directly relates to keyword and ad")
        
        if not recommendations:
            recommendations.append("Keyword in ad copy ✓ — good relevance")
        
        return recommendations
```

## Common Pitfalls

1. **Not using negative keywords** — Google matches to irrelevant searches; add negatives from search term reports
2. **Broad match without controls** — broad match without modifiers or smart bidding wastes budget
3. **Poor landing page match** — highest Quality Score factor; ad group should match landing page exactly
4. **Not tracking conversions** — impossible to optimize without conversion tracking
5. **Set-and-forget** — PPC needs ongoing optimization; review at least weekly
6. **Ignoring search term reports** — the data on what people actually searched reveals optimization opportunities

## Verification Checklist

- [ ] Keywords organized into themed ad groups (not one ad group for everything)
- [ ] All match types used strategically (exact, phrase, broad modified)
- [ ] Negative keywords list built and applied
- [ ] Ad copy written with keyword insertion where appropriate
- [ ] Ad extensions configured (site links, callouts, structured snippets)
- [ ] Conversion tracking implemented and verified
- [ ] Landing pages match ad copy and keywords
- [ ] Bidding strategy selected based on campaign goals
- [ ] Search term report reviewed for negatives and keyword additions
- [ ] Quality Score tracked and optimized

## See Also

- social-media-advertising — paid social campaigns
- seo-search-engine-optimization — organic search complement
- conversion-rate-optimization — optimizing landing pages
- digital-marketing-strategy — PPC role in marketing mix
