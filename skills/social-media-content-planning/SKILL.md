---
name: social-media-content-planning
description: "Use when planning and scheduling social media content."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [social-media, content, scheduling, calendar, strategy, platforms]
    related_skills: [social-media-analytics, content-writing-seo-copy, email-marketing-campaigns, digital-marketing-strategy]
---

# Social Media Content Planning

Planning, creating, scheduling, and managing social media content across platforms — from content calendars and post templates through platform-specific optimization and scheduling.

## When to Use

- Building a social media content strategy
- Creating and managing a content calendar
- Optimizing posts for different platforms (LinkedIn, Twitter, Instagram, TikTok, Facebook)
- Scheduling content across multiple accounts
- Analyzing what content performs best

## Content Calendar

```python
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import csv

class ContentCalendar:
    """Plan and manage social media content schedule."""
    
    PLATFORMS = ['linkedin', 'twitter', 'instagram', 'facebook', 'tiktok', 'youtube']
    
    CONTENT_CATEGORIES = [
        'educational', 'promotional', 'entertainment', 'behind_the_scenes',
        'user_generated', 'industry_news', 'thought_leadership', 'case_study',
        'tip_trick', 'question_poll', 'storytelling', 'event',
    ]
    
    def __init__(self, brand_name: str, start_date: str = None):
        self.brand = brand_name
        self.start = datetime.fromisoformat(start_date) if start_date else datetime.now()
        self.posts = {}  # post_id -> Post
    
    def plan_post(self, platform: str, content: str, publish_date: str,
                  category: str = 'educational', media_urls: List[str] = None,
                  hashtags: List[str] = None, ctas: str = None) -> str:
        """Schedule a social media post."""
        import uuid
        post_id = str(uuid.uuid4())[:8]
        
        self.posts[post_id] = {
            'id': post_id,
            'platform': platform,
            'content': content,
            'publish_date': publish_date,
            'category': category,
            'media_urls': media_urls or [],
            'hashtags': hashtags or [],
            'cta': ctas,
            'status': 'planned',
            'created_at': datetime.now().isoformat(),
            'performance': None,
        }
        
        return post_id
    
    def generate_weekly_plan(self, week_offset: int = 0) -> List[Dict]:
        """Generate a suggested weekly posting schedule."""
        week_start = self.start + timedelta(weeks=week_offset)
        
        # Recommended posting frequency per platform
        platform_frequency = {
            'linkedin': {'posts_per_week': 3, 'best_times': ['tue 8am', 'wed 10am', 'thu 9am']},
            'twitter': {'posts_per_week': 14, 'best_times': ['daily 8am', '12pm', '5pm']},
            'instagram': {'posts_per_week': 4, 'best_times': ['mon 11am', 'thu 1pm', 'fri 10am']},
            'facebook': {'posts_per_week': 3, 'best_times': ['wed 12pm', 'thu 1pm', 'sat 9am']},
            'tiktok': {'posts_per_week': 5, 'best_times': ['daily 7pm', '9pm']},
        }
        
        plan = []
        for platform, config in platform_frequency.items():
            for i in range(config['posts_per_week']):
                day_offset = (i * 7 // config['posts_per_week'])
                post_date = week_start + timedelta(days=day_offset)
                plan.append({
                    'platform': platform,
                    'suggested_date': post_date.isoformat(),
                    'best_time': config['best_times'][i % len(config['best_times'])],
                    'suggested_categories': random.sample(self.CONTENT_CATEGORIES, 2),
                })
        
        return sorted(plan, key=lambda p: p['suggested_date'])
    
    def export_csv(self, filepath: str):
        """Export calendar to CSV."""
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Platform', 'Content', 'Category', 'Status'])
            for post in sorted(self.posts.values(), key=lambda p: p['publish_date']):
                writer.writerow([
                    post['publish_date'], post['platform'],
                    post['content'][:100], post['category'], post['status']
                ])
```

## Platform-Specific Optimization

```python
class PlatformOptimizer:
    """Optimize content for each social platform."""
    
    @staticmethod
    def optimize_for_linkedin(content: str) -> Dict:
        """LinkedIn: professional, thought leadership."""
        tips = (
            "• Keep it professional but conversational\n"
            "• Start with a hook (question or bold statement)\n"
            "• Use short paragraphs (1-3 sentences each)\n"
            "• Include a clear CTA (comment, share, or link)\n"
            "• Add 3-5 relevant hashtags\n"
            "• Best length: 1,200-1,500 characters\n"
            "• Tag relevant people/companies with @"
        )
        return {'content': content, 'platform': 'linkedin', 'tips': tips}
    
    @staticmethod
    def optimize_for_twitter(content: str) -> Dict:
        """X/Twitter: concise, timely, engaging."""
        if len(content) > 280:
            # Suggest thread
            words = content.split()
            threads = []
            current = ""
            for word in words:
                if len(current) + len(word) + 1 <= 260:
                    current += " " + word if current else word
                else:
                    threads.append(current.strip())
                    current = word
            if current:
                threads.append(current.strip())
            
            thread_text = "\n\n".join(
                f"{i+1}/{len(threads)}: {t}" for i, t in enumerate(threads)
            )
            return {
                'content': content,
                'platform': 'twitter',
                'type': 'thread',
                'tweets': threads,
                'tips': "Posted as a thread for better engagement"
            }
        
        return {
            'content': content,
            'platform': 'twitter',
            'type': 'single',
            'tips': "Add 1-2 relevant hashtags, consider a poll or question"
        }
    
    @staticmethod
    def optimize_for_instagram(content: str, has_image: bool = True) -> Dict:
        """Instagram: visual-first, storytelling."""
        return {
            'content': content,
            'platform': 'instagram',
            'requires_image': not has_image,
            'tips': (
                "• Caption: story + value + CTA\n"
                "• First 125 characters appear in feed — hook there\n"
                "• Add line breaks between paragraphs\n"
                "• Use 3-5 relevant hashtags + 5-10 niche hashtags\n"
                "• Include location tag\n"
                "• Best formats: Carousel > Video > Image\n"
                "• CTA examples: 'Double tap if...', 'Save for later', 'Share with...'"
            )
        }
```

## Content Idea Generator

```python
class ContentIdeaGenerator:
    """Generate content ideas based on topic and format."""
    
    IDEA_TEMPLATES = {
        'educational': [
            "The ultimate guide to [topic]",
            "[Number] [topic] tips that actually work",
            "What nobody tells you about [topic]",
            "[Topic] explained in simple terms",
            "Common [topic] mistakes and how to avoid them",
        ],
        'engagement': [
            "We asked [audience] about [topic]. Here's what they said",
            "Debate: [statement]. What's your take?",
            "Fill in the blank: [topic] is _____",
            "What's your [topic] hot take?",
            "Tag someone who needs to see this",
        ],
        'promotional': [
            "New [product/feature] alert! Here's what it does",
            "Behind the scenes: how we built [thing]",
            "Customer success story: [name] achieved [result] using [product]",
            "Limited time: [offer] — here's how to get it",
            "We're hiring! Join our [team] team",
        ],
        'storytelling': [
            "The day we almost [failure] but then [success]",
            "How [person] went from [start] to [result]",
            "Our founder's journey: from [idea] to [company]",
            "The hardest lesson we learned about [topic]",
            "What [event] taught us about [topic]",
        ],
    }
    
    @staticmethod
    def generate_ideas(topic: str, format: str = 'educational', count: int = 5) -> List[str]:
        """Generate content ideas from templates."""
        templates = ContentIdeaGenerator.IDEA_TEMPLATES.get(format, 
                     ContentIdeaGenerator.IDEA_TEMPLATES['educational'])
        ideas = []
        for template in templates[:count]:
            ideas.append(template.replace('[topic]', topic))
        return ideas
    
    @staticmethod
    def generate_hashtags(topic: str, count: int = 10) -> List[str]:
        """Generate relevant hashtags."""
        topic_words = topic.lower().split()
        base_tags = [
            f"#{topic_words[0]}",
            f"#{topic.replace(' ', '')}",
            f"#{topic_words[0]}Tips",
            f"#{topic_words[0]}Strategy",
        ]
        general_tags = [
            '#SocialMedia', '#ContentStrategy', '#DigitalMarketing',
            '#GrowthHacking', '#MarketingTips', '#BrandBuilding',
        ]
        import random
        random.shuffle(general_tags)
        return (base_tags + general_tags)[:count]
```

## Common Pitfalls

1. **Posting without a strategy** — random posting gets random results; use a content calendar
2. **Same content on every platform** — each platform has different audience expectations
3. **Ignoring engagement** — social media is two-way; respond to comments and messages
4. **Inconsistent posting** — followers lose interest; maintain a consistent schedule
5. **No CTA** — people don't know what to do; always include a call-to-action
6. **Vanity metrics** — likes don't pay the bills; track engagement rate and conversions

## Verification Checklist

- [ ] Content calendar covers at least 2 weeks ahead
- [ ] Platform-specific optimization applied per post
- [ ] Content mix balanced (educational, promotional, engagement, entertaining)
- [ ] Hashtags researched and relevant per platform
- [ ] Visual assets planned alongside copy
- [ ] Scheduling/batching tool configured (Buffer, Hootsuite, or custom)
- [ ] Engagement monitoring and response process defined
- [ ] Analytics tracking (UTM parameters for link clicks)

## See Also

- social-media-analytics — measuring content performance
- content-writing-seo-copy — writing engaging social copy
- digital-marketing-strategy — integrating social into broader strategy
- email-marketing-campaigns — cross-promoting social and email
