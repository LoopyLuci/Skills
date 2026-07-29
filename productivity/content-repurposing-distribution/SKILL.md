---
name: content-repurposing-distribution
description: "Use when repurposing content across multiple channels."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [content-repurposing, distribution, content-marketing, multi-channel, content-strategy]
    related_skills: [content-writing-seo-copy, blog-building-content-strategy, social-media-content-planning, digital-marketing-strategy]
---

# Content Repurposing and Distribution

Turning one piece of content into many — repurposing strategies, distribution channels, syndication, and maximizing the ROI of every content asset.

## When to Use

- Getting more mileage from existing content assets
- Building a content distribution plan
- Repurposing long-form content into multiple formats
- Distributing content across owned, earned, and paid channels
- Maximizing content ROI (one piece, many formats, many channels)

## Repurposing Framework

```
Core Asset (e.g., 2000-word blog post)
├── Social Media (5-10 posts across platforms)
├── Email (2-3 email sequence)
├── Visual (infographic, carousel, video)
├── Audio (podcast episode)
├── Short-form (Twitter thread, LinkedIn post)
├── Derivative (checklist, cheatsheet, template)
└── Updated/Refreshed (republish with updates)
```

## Content Repurposer

```python
from typing import Dict, List, Optional
import re

class ContentRepurposer:
    """Repurpose content into multiple formats."""
    
    @staticmethod
    def analyze_content(content: str) -> Dict:
        """Analyze content to find repurposing opportunities."""
        paragraphs = [p for p in content.split('\n\n') if len(p) > 40]
        
        # Extract key elements
        stats = re.findall(r'\d+%|\$\d+|\d+x|\d+ [a-z]+', content)
        quotes = re.findall(r'"([^"]*)"', content)
        headings = re.findall(r'^#{1,3}\s(.+)$', content, re.MULTILINE)
        
        return {
            'paragraph_count': len(paragraphs),
            'key_stats': stats[:5],
            'quotable_moments': quotes[:3],
            'headings': headings,
            'estimated_read_time': max(1, len(content.split()) // 200),
            'repurpose_opportunities': ContentRepurposer._suggest_formats(paragraphs, stats, quotes),
        }
    
    @staticmethod
    def _suggest_formats(paragraphs, stats, quotes) -> List[Dict]:
        formats = []
        
        if len(paragraphs) >= 7:
            formats.append({'format': 'twitter_thread', 'items': len(paragraphs)})
            formats.append({'format': 'email_sequence', 'items': min(len(paragraphs) // 3 + 1, 5)})
        
        if stats:
            formats.append({'format': 'infographic', 'key_stat_count': len(stats)})
            formats.append({'format': 'linkedin_carousel', 'slides': min(len(paragraphs) // 2 + 1, 10)})
        
        if quotes:
            formats.append({'format': 'quote_graphics', 'count': len(quotes)})
        
        formats.append({'format': 'summary_post'})
        formats.append({'format': 'podcast_script', 'estimated_minutes': max(5, len(paragraphs))})
        
        return formats
    
    @staticmethod
    def to_twitter_thread(paragraphs: List[str], max_tweets: int = 15) -> List[str]:
        """Convert paragraphs into a Twitter thread."""
        thread = []
        for i, p in enumerate(paragraphs[:max_tweets - 1], 1):
            tweet = f"{i}/{len(paragraphs)}: {p[:240]}"
            thread.append(tweet)
        thread.append(f"{len(paragraphs)}/{len(paragraphs)}: 👆 Full article at [link]")
        return thread
    
    @staticmethod
    def to_email_sequence(paragraphs: List[str], title: str) -> List[Dict]:
        """Convert content into a multi-email sequence."""
        chunk_size = max(1, len(paragraphs) // 5)
        emails = []
        
        for i in range(0, min(len(paragraphs), chunk_size * 5), chunk_size):
            chunk = paragraphs[i:i + chunk_size]
            emails.append({
                'subject': f"{title} — Part {len(emails) + 1}",
                'preview': chunk[0][:100] if chunk else '',
                'content': '\n\n'.join(chunk),
                'position': len(emails) + 1,
            })
        
        return emails
    
    @staticmethod
    def create_linkedin_carousel(paragraphs: List[str], title: str) -> List[Dict]:
        """Create LinkedIn carousel slides from content."""
        slides = [{'title': title, 'type': 'cover'}]
        
        for p in paragraphs[:8]:
            slides.append({
                'title': '',
                'body': p[:200],
                'type': 'content',
            })
        
        slides.append({'title': 'Want the full guide?', 'body': 'Link in comments ↓', 'type': 'cta'})
        return slides
```

## Distribution Channels

```python
class DistributionPlanner:
    """Plan content distribution across channels."""
    
    CHANNELS = {
        'owned': {
            'website_blog': 'High', 'email_newsletter': 'High',
            'podcast': 'Medium', 'knowledge_base': 'Medium',
        },
        'earned': {
            'medium': 'High', 'linkedin_posts': 'High',
            'quora': 'Medium', 'industry_publications': 'Medium',
            'podcast_interviews': 'Medium', 'guest_posts': 'High',
        },
        'paid': {
            'social_ads': 'High', 'google_ads': 'Medium',
            'sponsored_content': 'Medium', 'retargeting': 'High',
        },
        'social': {
            'linkedin': 'High', 'twitter': 'High',
            'facebook': 'Medium', 'instagram': 'Medium',
            'youtube': 'High', 'tiktok': 'Medium',
        },
    }
    
    @staticmethod
    def build_plan(content_title: str, content_type: str,
                   target_audience: str, budget: str = 'low') -> List[Dict]:
        """Build a distribution plan for a piece of content."""
        plan = []
        
        # Owned channels (always)
        plan.append({'channel': 'blog', 'action': 'Publish on website', 'timing': 'Day 0'})
        plan.append({'channel': 'email', 'action': 'Send to email list', 'timing': 'Day 0'})
        
        # Social
        plan.append({'channel': 'linkedin', 'action': 'Native article/post', 'timing': 'Day 0'})
        plan.append({'channel': 'twitter', 'action': 'Thread or tweet with image', 'timing': 'Day 0'})
        
        # Earned
        if budget != 'low':
            plan.append({'channel': 'medium', 'action': 'Republish on Medium (canonical URL)', 'timing': 'Day 3'})
            plan.append({'channel': 'outreach', 'action': 'Share with industry influencers', 'timing': 'Day 3'})
        
        # Paid (if budget allows)
        if budget == 'high':
            plan.append({'channel': 'social_ads', 'action': 'Boost top-performing post', 'timing': 'Day 7'})
            plan.append({'channel': 'retargeting', 'action': 'Retarget content visitors', 'timing': 'Day 14'})
        
        # Repurpose
        plan.append({'channel': 'repurpose', 'action': 'Create derivative formats', 'timing': 'Days 7-14'})
        plan.append({'channel': 'update', 'action': 'Update and republish after 3 months', 'timing': 'Month 3'})
        
        return plan
```

## Common Pitfalls

1. **No canonical URL** — republishing without canonical tags creates duplicate content issues
2. **Same content, same format** — turning a blog post into... another blog post isn't repurposing
3. **Not adapting to platform** — reposting the same text on LinkedIn, Twitter, and Instagram ignores platform norms
4. **Forgetting distribution** — creating content is 20%, distributing is 80%; plan both
5. **One-and-done** — posting once and never sharing again wastes potential; re-share evergreen content quarterly
6. **No tracking** — many distribution channels, no way to know what works; use UTM parameters

## Verification Checklist

- [ ] Core content analyzed for repurposing opportunities
- [ ] At least 5 derivative formats planned (social posts, email, visual, audio, short-form)
- [ ] Distribution plan covers owned, earned, and social channels
- [ ] UTM parameters on all distribution links
- [ ] Canonical URL set when republishing on third-party platforms
- [ ] Re-sharing schedule planned (evergreen content reshared quarterly)
- [ ] Performance tracked per channel

## See Also

- content-writing-seo-copy — writing the original content
- blog-building-content-strategy — planning the content
- social-media-content-planning — distributing on social
- digital-marketing-strategy — content marketing strategy
