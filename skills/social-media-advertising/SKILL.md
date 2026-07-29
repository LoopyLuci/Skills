---
name: social-media-advertising
description: "Use when creating and managing social media ad campaigns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [social-media, advertising, paid-social, facebook-ads, linkedin-ads, targeting]
    related_skills: [social-media-content-planning, ppc-advertising-management, digital-marketing-strategy, conversion-rate-optimization]
---

# Social Media Advertising

Creating, managing, and optimizing paid social media campaigns across platforms — from audience targeting and creative strategy through budget management and performance analysis.

## When to Use

- Running paid campaigns on Facebook, Instagram, LinkedIn, Twitter/X, TikTok
- Building and testing social ad audiences
- Designing ad creative and copy for social platforms
- Managing ad budgets and bids across platforms
- Analyzing and optimizing social ad performance

## Platform Comparison

```python
PLATFORM_COMPARISON = {
    'facebook_instagram': {
        'best_for': 'B2C, ecommerce, brand awareness, retargeting',
        'audience_size': '2.9B+ monthly active',
        'ad_formats': 'Image, Video, Carousel, Collection, Stories, Reels',
        'targeting': 'Demographic, interest, behavioral, custom audiences, lookalikes',
        'min_budget': '$5/day',
        'cost_benchmark_cpc': '$0.50-1.50',
    },
    'linkedin': {
        'best_for': 'B2B, professional services, recruitment, thought leadership',
        'audience_size': '900M+ members',
        'ad_formats': 'Sponsored Content, Message Ads, Text Ads, Dynamic Ads',
        'targeting': 'Job title, company, industry, skills, seniority, groups',
        'min_budget': '$10/day',
        'cost_benchmark_cpc': '$5-8',
    },
    'twitter_x': {
        'best_for': 'News, events, app installs, trending topics',
        'audience_size': '350M+ monthly active',
        'ad_formats': 'Promoted Tweets, Trends, Accounts, Amplify',
        'targeting': 'Keyword, interest, follower lookalikes, conversation targeting',
        'min_budget': '$5/day',
        'cost_benchmark_cpc': '$0.50-2.00',
    },
    'tiktok': {
        'best_for': 'Gen Z, viral content, app installs, brand awareness',
        'audience_size': '1B+ monthly active',
        'ad_formats': 'In-Feed, Spark Ads, Brand Takeover, Hashtag Challenge',
        'targeting': 'Demographic, interest, behavior, custom audiences',
        'min_budget': '$10/day',
        'cost_benchmark_cpc': '$1-2',
    },
}
```

## Campaign Builder

```python
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class SocialAdCampaign:
    """Design and manage social media advertising campaigns."""
    
    CAMPAIGN_OBJECTIVES = {
        'awareness': ['brand_awareness', 'reach'],
        'consideration': ['traffic', 'engagement', 'video_views', 'lead_generation'],
        'conversion': ['conversions', 'catalog_sales', 'store_visits'],
    }
    
    def __init__(self, name: str, platform: str, objective: str,
                 daily_budget: float, start_date: str, end_date: str = None):
        self.name = name
        self.platform = platform
        self.objective = objective
        self.daily_budget = daily_budget
        self.start = start_date
        self.end = end_date
        self.ad_sets = []
        self.total_budget = self._calculate_total_budget()
    
    def add_ad_set(self, name: str, targeting: Dict, 
                   placements: List[str], bid_strategy: str = 'lowest_cost') -> 'SocialAdCampaign':
        """Add an ad set (targeting group) to the campaign."""
        self.ad_sets.append({
            'name': name,
            'targeting': targeting,
            'placements': placements,
            'bid_strategy': bid_strategy,
            'budget_percentage': 100 // max(len(self.ad_sets) + 1, 1),
            'status': 'draft',
        })
        return self
    
    def _calculate_total_budget(self) -> float:
        if not self.end: return None
        start = datetime.fromisoformat(self.start)
        end = datetime.fromisoformat(self.end)
        days = (end - start).days
        return self.daily_budget * max(days, 1)
    
    def get_campaign_summary(self) -> str:
        summary = f"\n📢 Campaign: {self.name}\n"
        summary += f"Platform: {self.platform} | Objective: {self.objective}\n"
        summary += f"Budget: ${self.daily_budget}/day"
        if self.total_budget: summary += f" (total: ${self.total_budget})"
        summary += f"\nDuration: {self.start} to {self.end or 'ongoing'}"
        summary += f"\nAd Sets: {len(self.ad_sets)}\n"
        for i, ads in enumerate(self.ad_sets, 1):
            summary += f"\n  {i}. {ads['name']}"
            summary += f"\n     Targeting: {ads['targeting']}"
            summary += f"\n     Placements: {', '.join(ads['placements'][:3])}"
        return summary
```

## Audience Builder

```python
class AudienceBuilder:
    """Build and estimate social media ad audiences."""
    
    @staticmethod
    def build_custom_audience(source: str, value: str, 
                              retention_days: int = 30) -> Dict:
        """Define a custom audience for retargeting."""
        return {
            'name': f'{value} ({retention_days}d)',
            'source': source,  # website, customer_list, app, engagement
            'value': value,
            'retention_days': retention_days,
            'type': 'custom',
        }
    
    @staticmethod
    def build_lookalike(source_audience_id: str, 
                        lookalike_pct: float = 1.0) -> Dict:
        """Build a lookalike audience from a source.
        
        lookalike_pct: 1% (most similar) to 10% (broadest)
        """
        return {
            'name': f'Lookalike ({lookalike_pct}%)',
            'source_audience': source_audience_id,
            'lookalike_percentage': lookalike_pct,
            'type': 'lookalike',
        }
    
    @staticmethod
    def estimate_reach(targeting: Dict, platform: str) -> Dict:
        """Estimate potential reach for targeting criteria."""
        # Simplified estimation (platform APIs provide actual estimates)
        base_reach = {
            'facebook_instagram': 1000000,
            'linkedin': 500000,
            'twitter_x': 300000,
            'tiktok': 800000,
        }
        
        # Reduce reach based on targeting specificity
        factors = 1.0
        if targeting.get('age_range'): factors *= 0.4
        if targeting.get('interests'): factors *= 0.3
        if targeting.get('job_titles'): factors *= 0.1
        if targeting.get('custom_audiences'): factors *= 0.5
        
        base = base_reach.get(platform, 500000)
        estimated_reach = int(base * factors)
        
        return {
            'platform': platform,
            'estimated_reach': estimated_reach,
            'targeting_specificity': 'high' if factors < 0.3 else 'medium' if factors < 0.6 else 'broad',
        }
```

## Performance Analysis

```python
class SocialAdAnalyzer:
    """Analyze social media ad performance."""
    
    METRICS = {
        'ctr': 'Click-through rate (%)',
        'cpc': 'Cost per click ($)',
        'cpm': 'Cost per 1000 impressions ($)',
        'cpa': 'Cost per acquisition ($)',
        'roas': 'Return on ad spend ($)',
        'frequency': 'Avg times person saw ad',
        'reach': 'Unique people reached',
        'impressions': 'Total times ad shown',
        'engagement_rate': 'Engagements / impressions (%)',
    }
    
    @staticmethod
    def analyze(results: Dict) -> Dict:
        """Analyze campaign performance across metrics."""
        analysis = {}
        
        spend = results.get('spend', 0)
        impressions = results.get('impressions', 0)
        clicks = results.get('clicks', 0)
        conversions = results.get('conversions', 0)
        revenue = results.get('revenue', 0)
        
        analysis['ctr'] = round(clicks / max(impressions, 1) * 100, 2)
        analysis['cpc'] = round(spend / max(clicks, 1), 2)
        analysis['cpm'] = round(spend / max(impressions, 1) * 1000, 2)
        analysis['cpa'] = round(spend / max(conversions, 1), 2)
        analysis['roas'] = round(revenue / max(spend, 1), 2)
        analysis['conversion_rate'] = round(conversions / max(clicks, 1) * 100, 2)
        
        return analysis
    
    @staticmethod
    def benchmark_check(platform: str, metrics: Dict) -> List[str]:
        """Compare metrics against platform benchmarks."""
        benchmarks = {
            'facebook_instagram': {'ctr': 0.90, 'cpc': 0.80, 'cpa': 18.00},
            'linkedin': {'ctr': 0.50, 'cpc': 6.00, 'cpa': 80.00},
            'twitter_x': {'ctr': 0.90, 'cpc': 1.50, 'cpa': 30.00},
            'tiktok': {'ctr': 1.50, 'cpc': 1.00, 'cpa': 25.00},
        }
        
        bm = benchmarks.get(platform, benchmarks['facebook_instagram'])
        alerts = []
        
        for metric, benchmark_value in bm.items():
            if metric in metrics:
                value = metrics[metric]
                if metric in ('cpc', 'cpa') and value > benchmark_value * 1.5:
                    alerts.append(f"⚠️ {metric.upper()} ${value} is 50%+ above benchmark ${benchmark_value}")
                elif metric in ('ctr',) and value < benchmark_value * 0.5:
                    alerts.append(f"⚠️ {metric.upper()} {value}% is 50%+ below benchmark {benchmark_value}%")
        
        if not alerts:
            alerts.append("✅ All metrics within healthy range")
        
        return alerts
```

## Common Pitfalls

1. **Wrong objective** — using "brand awareness" when you want conversions; match objective to funnel stage
2. **Audience overlap** — running multiple ad sets with overlapping audiences causes auction competition
3. **Creative fatigue** — same ad seen 5+ times drops CTR dramatically; refresh creative every 1-2 weeks
4. **Ignoring placement** — automatic placements can waste budget on low-performing spots; review placement reports
5. **Mobile-unfriendly creative** — most social traffic is mobile; design for small screens first
6. **No pixel/events** — can't optimize without conversion tracking; install platform pixel

## Verification Checklist

- [ ] Campaign objective matches funnel stage
- [ ] Audience targeting defined (demographics + interests + behaviors)
- [ ] Custom audiences created (website visitors, customer list)
- [ ] Lookalike audiences built from top segments
- [ ] Ad creative designed for mobile-first
- [ ] Tracking pixel/events installed and verified
- [ ] Budget and schedule configured
- [ ] Performance benchmarks identified per platform
- [ ] Testing plan (creative, audience, placement variants)

## See Also

- social-media-content-planning — organic social strategy
- ppc-advertising-management — cross-platform PPC management
- digital-marketing-strategy — role of paid social in strategy
- conversion-rate-optimization — optimizing ad landing pages
