---
name: local-seo-google-business
description: "Use when optimizing local SEO and Google Business Profile."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [local-seo, google-business-profile, maps, GBP, local-search, citations]
    related_skills: [seo-search-engine-optimization, website-analytics-tracking, digital-marketing-strategy, cms-website-management]
---

# Local SEO and Google Business Profile

Optimizing local search presence and Google Business Profile (formerly Google My Business) for businesses with physical locations.

## When to Use

- Managing a business with a physical location
- Optimizing Google Business Profile for local search rankings
- Building local citations and NAP consistency
- Getting more customers from Google Maps and local search
- Managing reviews and local reputation

## GBP Optimization Checklist

```python
GBP_SETUP = {
    'business_name': 'Exact legal name (consistent everywhere)',
    'category': 'Primary category + up to 10 additional categories',
    'address': 'Physical address (no PO boxes for GBP)',
    'service_area': 'Service area if you don't serve at location',
    'phone': 'Local number (not call center / toll-free)',
    'website': 'Business website URL',
    'hours': 'Regular and special/holiday hours',
    'description': '750-character business description with keywords',
    'photos': 'Interior, exterior, team, products (100+ recommended)',
    'attributes': 'Black-owned, LGBTQ+ friendly, women-led, etc.',
    'services': 'List of services/products offered',
    'menus': 'For restaurants — online menu',
    'booking': 'Booking button if applicable (appointment types)',
    'questions': 'Q&A section — proactively answer common questions',
    'posts': 'Weekly GBP posts (offers, events, updates)',
    'reviews': 'Respond to every review (positive + negative)',
}

def gbp_audit_score(profile: Dict) -> Dict:
    """Score a GBP profile's completeness (100-point scale)."""
    score = 0
    missing = []
    
    checks = [
        ('name', 5), ('category', 10), ('address', 10),
        ('phone', 10), ('website', 5), ('hours', 10),
        ('description', 5), ('photos', 10), ('services', 5),
    ]
    
    for field, points in checks:
        if profile.get(field):
            score += points
        else:
            missing.append(field)
    
    # Review response rate bonus
    total_reviews = len(profile.get('reviews', []))
    responded = sum(1 for r in profile.get('reviews', []) if r.get('responded'))
    if total_reviews > 0 and responded / total_reviews >= 0.5:
        score += 10
    
    # Posting frequency bonus
    posts_last_30 = profile.get('posts_last_30_days', 0)
    if posts_last_30 >= 4:
        score += 10
    elif posts_last_30 >= 2:
        score += 5
    
    # Photo count bonus
    photo_count = profile.get('photo_count', 0)
    if photo_count >= 100: score += 10
    elif photo_count >= 50: score += 5
    
    return {
        'score': min(score, 100),
        'missing_elements': missing,
        'rating': 'Excellent' if score >= 80 else 'Good' if score >= 60 else 'Needs work',
        'recommendations': [f"Add: {m}" for m in missing],
    }
```

## Local Citation Building

```python
CITATION_SITES = {
    'tier_1': [
        'Google Business Profile', 'Bing Places', 'Apple Maps',
        'Facebook', 'Yelp', 'Yellow Pages',
    ],
    'tier_2': [
        'MapQuest', 'Superpages', 'Citysearch', 'Hotfrog',
        'Merchant Circle', 'Foursquare', 'Manta',
    ],
    'niche_specific': {
        'restaurant': ['TripAdvisor', 'OpenTable', 'Zomato', 'MenuPages'],
        'healthcare': ['Healthgrades', 'Zocdoc', 'Vitals', 'RateMDs'],
        'legal': ['Avvo', 'Martindale', 'FindLaw', 'Lawyers.com'],
        'home_services': ['Angi (Angies List)', 'HomeAdvisor', 'Houzz', 'Porch'],
        'real_estate': ['Zillow', 'Realtor.com', 'Trulia', 'Redfin'],
    },
}

class CitationBuilder:
    """Manage NAP consistency across citations."""
    
    def __init__(self, business_name: str, address: str, phone: str, website: str):
        self.nap = {
            'name': business_name,
            'address': address,
            'phone': phone,
            'website': website,
        }
        self.citations = []
    
    def add_citation(self, site: str, url: str, 
                     nap_match: str = 'exact', status: str = 'pending'):
        self.citations.append({
            'site': site, 'url': url,
            'nap_match': nap_match,  # exact, partial, mismatch
            'status': status,
            'last_verified': None,
        })
    
    def get_consistency_report(self) -> Dict:
        exact = sum(1 for c in self.citations if c['nap_match'] == 'exact')
        partial = sum(1 for c in self.citations if c['nap_match'] == 'partial')
        mismatched = sum(1 for c in self.citations if c['nap_match'] == 'mismatch')
        pending = sum(1 for c in self.citations if c['status'] == 'pending')
        
        return {
            'total_citations': len(self.citations),
            'exact_match': exact,
            'partial_match': partial,
            'mismatch': mismatched,
            'pending': pending,
            'consistency_score': round(exact / max(len(self.citations), 1) * 100, 1),
        }
```

## Local Ranking Factors

```python
LOCAL_RANKING_FACTORS = {
    'proximity': {
        'weight': 'High',
        'description': 'Distance between searcher and business location',
        'influence': 'You can\'t change proximity, but can target specific areas',
    },
    'gbp_signals': {
        'weight': 'Very High',
        'description': 'Category, attributes, verification, completeness',
        'influence': 'Optimize every GBP field; post weekly; respond to reviews',
    },
    'reviews': {
        'weight': 'High',
        'description': 'Quantity, recency, diversity, and sentiment of reviews',
        'influence': 'Encourage reviews, respond to all, never buy fake reviews',
    },
    'citations': {
        'weight': 'Medium',
        'description': 'Number and consistency of NAP across the web',
        'influence': 'Build tier 1 citations first; audit consistency quarterly',
    },
    'backlinks': {
        'weight': 'Medium',
        'description': 'Quality and relevance of backlinks to your site',
        'influence': 'Local backlinks (chambers, sponsors, partners) are most valuable',
    },
    'website_signals': {
        'weight': 'Medium',
        'description': 'On-page local SEO (title, H1, schema, content)',
        'influence': 'Include city/region in title, headings, and content',
    },
    'social_signals': {
        'weight': 'Low',
        'description': 'Social media presence and engagement',
        'influence': 'Active social profiles with consistent NAP',
    },
}

def local_seo_audit(business: Dict) -> List[str]:
    """Generate local SEO recommendations."""
    recs = []
    
    if not business.get('gbp_claimed'):
        recs.append("Claim and verify your Google Business Profile")
    if business.get('gbp_category_count', 0) < 3:
        recs.append("Add more relevant categories to GBP (up to 10)")
    if business.get('gbp_photos', 0) < 50:
        recs.append(f"Add more photos to GBP (currently {business.get('gbp_photos', 0)}, target 100+)")
    if business.get('gbp_posts_30d', 0) < 4:
        recs.append("Post to GBP at least once per week (services, offers, events)")
    if business.get('review_count', 0) < 10:
        recs.append("Implement a review generation strategy (target 10+ reviews)")
    if business.get('review_response_rate', 0) < 0.5:
        recs.append("Respond to ALL reviews — positive and negative")
    
    return recs
```

## Common Pitfalls

1. **NAP inconsistency** — different address formats across citations confuse Google
2. **Unclaimed GBP** — Google populates unclaimed profiles with unreliable data; claim yours
3. **Buying fake reviews** — Google detects and penalizes; legitimate review generation only
4. **Abandoned profile** — old posts, unresponded reviews, outdated hours hurt rankings
5. **Wrong category** — primary category is the #1 ranking signal; choose carefully
6. **No review strategy** — customers need to be asked; make it easy to leave a review

## Verification Checklist

- [ ] Google Business Profile claimed and verified
- [ ] All NAP fields complete and accurate
- [ ] Primary + secondary categories selected
- [ ] 100+ high-quality photos uploaded
- [ ] Business description written (750 chars, keyword-rich)
- [ ] Products/services listed
- [ ] Weekly GBP posts published
- [ ] All reviews responded to within 48 hours
- [ ] Top 10 citation sites checked for NAP consistency
- [ ] Local schema markup on website

## See Also

- seo-search-engine-optimization — broader SEO strategy
- website-analytics-tracking — tracking local search performance
- digital-marketing-strategy — local SEO in marketing mix
- cms-website-management — local SEO on website
