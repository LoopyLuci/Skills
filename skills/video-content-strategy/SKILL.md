---
name: video-content-strategy
description: "Use when planning and producing video content strategy."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [video, content-strategy, youtube, production, editing, short-form, long-form]
    related_skills: [podcast-production-management, content-repurposing-distribution, social-media-content-planning, digital-marketing-strategy]
---

# Video Content Strategy

Planning, producing, and distributing video content — from YouTube channels and short-form (TikTok, Reels, Shorts) through production workflows and performance analytics.

## When to Use

- Starting a YouTube channel for your brand
- Creating short-form video content (TikTok, Instagram Reels, YouTube Shorts)
- Building a video production workflow
- Optimizing videos for search and discovery
- Measuring video performance and ROI

## Platform Comparison

```python
VIDEO_PLATFORMS = {
    'youtube': {
        'format': 'Long-form (8-20 min) + Shorts (<60s)',
        'best_for': 'Tutorials, reviews, vlogs, educational content',
        'monetization': 'Ad revenue, memberships, Super Chat',
        'seo': 'YouTube search is #2 search engine after Google',
        'algorithm': 'Watch time, click-through rate, session time',
    },
    'tiktok': {
        'format': 'Short-form (15-60s)',
        'best_for': 'Trends, entertainment, quick tips, behind-the-scenes',
        'monetization': 'Creator Fund, brand deals, LIVE gifts',
        'seo': 'Hashtag and sound discovery',
        'algorithm': 'Completion rate, rewatches, shares',
    },
    'instagram_reels': {
        'format': 'Short-form (15-90s)',
        'best_for': 'Visual brands, products, lifestyle, creators',
        'monetization': 'Brand deals, affiliate, badges',
        'seo': 'Hashtag and explore page',
        'algorithm': 'Reels plays, shares, saves, completion rate',
    },
    'linkedin_video': {
        'format': 'Short to medium (1-15 min)',
        'best_for': 'B2B, thought leadership, professional education',
        'monetization': 'Brand deals, lead generation',
        'seo': 'LinkedIn feed algorithm, hashtags',
        'algorithm': 'Engagement (likes, comments, shares) by professional network',
    },
}

def recommend_platform(content_type: str, audience: str) -> str:
    if audience == 'b2b': return 'LinkedIn Video'
    if content_type in ('tutorial', 'educational', 'review'): return 'YouTube'
    if content_type in ('entertainment', 'trend'): return 'TikTok'
    if audience in ('visual', 'lifestyle'): return 'Instagram Reels'
    return 'YouTube'
```

## Video Production Workflow

```python
from typing import Dict, List, Optional
from datetime import datetime

class VideoProduction:
    """Plan and manage video production from concept to publish."""
    
    def __init__(self, title: str, platform: str, target_length_seconds: int):
        self.title = title
        self.platform = platform
        self.target_length = target_length_seconds
        self.status = 'concept'
        self.script = ''
        self.shots = []
        self.resources = []
        self.publish_date = None
    
    def add_shot(self, description: str, duration_seconds: int, 
                 type: str = 'b_roll', notes: str = '') -> 'VideoProduction':
        self.shots.append({
            'shot_num': len(self.shots) + 1,
            'description': description,
            'duration': duration_seconds,
            'type': type,  # A-roll (speaking), B-roll (supplemental), intro, outro
            'notes': notes,
        })
        return self
    
    def calculate_total_duration(self) -> int:
        return sum(s['duration'] for s in self.shots)
    
    def generate_shooting_script(self) -> str:
        script = f"🎬 {self.title}\n"
        script += f"Platform: {self.platform} | Target: {self.target_length}s\n"
        script += "=" * 50 + "\n"
        
        running_time = 0
        for shot in self.shots:
            script += f"\nShot {shot['shot_num']} ({shot['type']}) | {running_time}s"
            script += f"\n  {shot['description']}"
            if shot['notes']: script += f"\n  📝 {shot['notes']}"
            running_time += shot['duration']
        
        total = self.calculate_total_duration()
        script += f"\n\n⏱️ Total: {total}s (target: {self.target_length}s)"
        over_under = total - self.target_length
        if abs(over_under) > self.target_length * 0.1:
            script += f"\n⚠️ Off by {over_under}s ({'over' if over_under > 0 else 'under'})"
        return script
```

## YouTube SEO

```python
class YouTubeSEO:
    """Optimize videos for YouTube search and discovery."""
    
    @staticmethod
    def optimize_title(title: str, keyword: str) -> Dict:
        patterns = [
            f"{keyword}: {title[:40]}",
            f"{title[:50]} — {keyword}",
            f"{keyword} — {title[:45]}",
        ]
        
        best = None
        for t in patterns:
            if len(t) <= 60 and keyword.lower() in t.lower():
                best = t
                break
        
        if not best: best = patterns[0][:60]
        
        return {
            'title': best,
            'length': len(best),
            'keyword_included': keyword.lower() in best.lower(),
            'tips': 'Include keyword early, keep under 60 chars, create curiosity',
        }
    
    @staticmethod
    def optimize_description(video_summary: str, keyword: str, 
                             timestamps: List[str] = None,
                             links: List[str] = None) -> str:
        desc = f"{video_summary[:200]}\n\n"
        desc += f"{' '.join(['#' + k.replace(' ', '') for k in keyword.split()])}\n\n"
        
        if timestamps:
            desc += "📋 Timestamps:\n"
            for t in timestamps:
                desc += f"{t}\n"
            desc += "\n"
        
        if links:
            desc += "🔗 Links:\n"
            for l in links:
                desc += f"- {l}\n"
        
        return desc
    
    @staticmethod
    def tags_from_content(title: str, keyword: str, topics: List[str]) -> List[str]:
        """Generate YouTube tags."""
        tags = [keyword, title]
        for t in topics:
            tags.append(t)
            tags.append(f"{keyword} {t}")
        return list(set(tags))[:10]
```

## Content Funnel

```python
class VideoContentStrategy:
    """Plan video content across the marketing funnel."""
    
    CONTENT_MIX = {
        'top_of_funnel': {
            'ratio': '30%',
            'purpose': 'Attract new viewers, build awareness',
            'video_types': ['Trend topics', 'Industry news', 'Quick tips', 'Viral formats'],
            'kpi': 'Views, reach, new subscribers',
        },
        'middle_of_funnel': {
            'ratio': '40%',
            'purpose': 'Educate and build authority',
            'video_types': ['Tutorials', 'How-tos', 'Case studies', 'Comparison videos'],
            'kpi': 'Watch time, engagement, comments',
        },
        'bottom_of_funnel': {
            'ratio': '20%',
            'purpose': 'Convert viewers into customers',
            'video_types': ['Product demos', 'Testimonials', 'Pricing explainers', 'Webinars'],
            'kpi': 'Click-through rate, conversions',
        },
        'retention': {
            'ratio': '10%',
            'purpose': 'Keep subscribers engaged and coming back',
            'video_types': ['Behind the scenes', 'Q&A', 'Community spotlights', 'Updates'],
            'kpi': 'Return viewers, subscriber growth',
        },
    }
    
    @staticmethod
    def monthly_plan(niche: str, videos_per_week: int = 2) -> List[Dict]:
        """Generate a monthly video content plan."""
        import random
        formats = {
            'top_of_funnel': ['Trend explanation', 'News reaction', 'Quick tip', 'Industry myth'],
            'middle_of_funnel': ['Tutorial', 'Case study', 'Comparison', 'Deep dive'],
            'bottom_of_funnel': ['Demo', 'Testimonial', 'Pricing breakdown'],
            'retention': ['Behind the scenes', 'Q&A', 'Community spotlight'],
        }
        
        plan = []
        week = 1
        for i in range(videos_per_week * 4):
            stage = random.choice(list(formats.keys()))
            fmt = random.choice(formats[stage])
            plan.append({
                'week': week,
                'day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'][i % 5] if i % 5 < 5 else 'Mon',
                'format': fmt,
                'funnel_stage': stage,
                'topic_hint': f"[{niche}] {fmt} video idea",
            })
            if (i + 1) % videos_per_week == 0: week += 1
        
        return plan
```

## Common Pitfalls

1. **No hook** — you have 3 seconds to grab attention; start with a strong hook
2. **Ignoring audio** — bad audio = viewers leave, even with great video; invest in a mic
3. **No thumbnail strategy** — thumbnails drive 90% of CTR; design custom thumbnails
4. **Inconsistent posting** — YouTube rewards consistency; set a schedule and stick to it
5. **Not repurposing** — one long-form video can be 10+ short-form clips; plan repurposing
6. **No CTA** — viewers won't naturally subscribe, like, or comment unless asked

## Verification Checklist

- [ ] Channel/platform set up with complete branding
- [ ] Content strategy defined (TOF/MOF/BOF mix)
- [ ] Recording equipment tested (camera, audio, lighting)
- [ ] Video editing workflow established
- [ ] Thumbnail design template created
- [ ] Title and description SEO optimized per video
- [ ] Upload schedule defined (weekly, bi-weekly)
- [ ] Repurposing workflow (long form → short clips)
- [ ] Analytics dashboard set up (views, watch time, subs, CTR)
- [ ] Community engagement plan (comments, community tab)

## See Also

- podcast-production-management — audio production crossover
- content-repurposing-distribution — repurposing video content
- social-media-content-planning — promoting video on social
- digital-marketing-strategy — video in marketing strategy
