---
name: blog-building-content-strategy
description: "Use when building blogs and planning editorial strategy."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [blogging, content-strategy, editorial, CMS, writing, publishing]
    related_skills: [content-writing-seo-copy, seo-search-engine-optimization, cms-website-management, digital-marketing-strategy]
---

# Blog Building and Content Strategy

Building, managing, and growing a blog — from platform selection and editorial planning through content creation, publishing workflows, and growth strategies.

## When to Use

- Starting a new blog (personal, business, or niche)
- Planning an editorial calendar and content strategy
- Building a blog on a CMS (WordPress, Ghost, Hugo, static site)
- Growing blog traffic through content marketing and SEO
- Repurposing blog content for social, email, and other channels

## Platform Selection

```python
class BlogPlatformSelector:
    """Compare blog platforms and suggest the best fit."""
    
    PLATFORMS = {
        'wordpress': {
            'type': 'cms',
            'cost': 'free + hosting ($5-30/mo)',
            'difficulty': 'medium',
            'customization': 'very_high',
            'seo': 'excellent',
            'best_for': 'Content marketing, business blogs, large sites',
            'hosting': 'self-managed or WordPress.com',
        },
        'ghost': {
            'type': 'cms',
            'cost': 'free + hosting ($9-30/mo)',
            'difficulty': 'medium',
            'customization': 'medium',
            'seo': 'excellent',
            'best_for': 'Subscription/newsletter blogs, publications',
            'hosting': 'Ghost(Pro) or self-hosted',
        },
        'hugo': {
            'type': 'static_site_generator',
            'cost': 'free ($0-10/mo for hosting)',
            'difficulty': 'high',
            'customization': 'very_high',
            'seo': 'excellent',
            'best_for': 'Developer blogs, performance-focused, technical content',
            'hosting': 'Netlify, Vercel, GitHub Pages',
        },
        'medium': {
            'type': 'platform',
            'cost': 'free',
            'difficulty': 'low',
            'customization': 'very_low',
            'seo': 'good',
            'best_for': 'Building audience, thought leadership, no technical setup',
            'hosting': 'built-in',
        },
        'substack': {
            'type': 'newsletter',
            'cost': 'free',
            'difficulty': 'low',
            'customization': 'low',
            'seo': 'low',
            'best_for': 'Newsletter-first, paid subscriptions, personal essays',
            'hosting': 'built-in',
        },
    }
    
    @staticmethod
    def recommend(technical_skill: str, budget: str, 
                  primary_goal: str) -> Dict:
        """Recommend a blog platform based on needs."""
        if primary_goal == 'newsletter':
            return BlogPlatformSelector.PLATFORMS['substack']
        if primary_goal == 'reach':
            return BlogPlatformSelector.PLATFORMS['medium']
        if technical_skill == 'high' and budget == 'low':
            return BlogPlatformSelector.PLATFORMS['hugo']
        if budget == 'medium' and primary_goal == 'monetization':
            return BlogPlatformSelector.PLATFORMS['ghost']
        return BlogPlatformSelector.PLATFORMS['wordpress']
```

## Editorial Calendar

```python
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import csv

class EditorialCalendar:
    """Plan, track, and manage editorial content."""
    
    CONTENT_FORMATS = [
        'how_to_guide', 'list_post', 'comparison', 'case_study',
        'opinion_editorial', 'interview', 'resource_roundup',
        'news_analysis', 'tutorial', 'thought_leadership',
        'beginner_guide', 'advanced_guide', 'checklist', 'template',
    ]
    
    def __init__(self, blog_name: str, content_focus: str):
        self.blog = blog_name
        self.focus = content_focus  # Primary topic/niche
        self.articles = {}  # article_id -> Article
    
    def plan_article(self, title: str, topic: str, format: str,
                     publish_date: str, keywords: List[str] = None,
                     target_word_count: int = 1500,
                     series: str = None) -> str:
        """Plan a new article for the editorial calendar."""
        import uuid
        article_id = str(uuid.uuid4())[:8]
        
        self.articles[article_id] = {
            'id': article_id,
            'title': title,
            'topic': topic,
            'format': format,
            'keywords': keywords or [],
            'target_word_count': target_word_count,
            'publish_date': publish_date,
            'series': series,
            'status': 'planned',  # planned, writing, editing, scheduled, published
            'author': None,
            'seo_score': None,
            'promotion_channels': [],
            'created_at': datetime.now().isoformat(),
        }
        
        return article_id
    
    def generate_monthly_plan(self, year: int, month: int, 
                              posts_per_week: int = 2) -> List[Dict]:
        """Generate a suggested monthly posting plan."""
        import calendar
        
        plan = []
        _, days_in_month = calendar.monthrange(year, month)
        
        post_count = 0
        for day in range(1, days_in_month + 1):
            date = datetime(year, month, day)
            if date.weekday() < 5 and post_count % (7 // posts_per_week) == 0:
                if post_count < posts_per_week * 4:
                    formats = self.CONTENT_FORMATS
                    plan.append({
                        'date': date.isoformat(),
                        'suggested_format': formats[post_count % len(formats)],
                        'week_number': date.isocalendar()[1],
                        'day_name': date.strftime('%A'),
                    })
                    post_count += 1
        
        return plan
    
    def get_publishing_schedule(self, upcoming_days: int = 30) -> List[Dict]:
        """Get all upcoming scheduled articles."""
        now = datetime.now()
        deadline = now + timedelta(days=upcoming_days)
        
        upcoming = []
        for article in self.articles.values():
            pub_date = datetime.fromisoformat(article['publish_date'])
            if now <= pub_date <= deadline:
                upcoming.append(article)
        
        return sorted(upcoming, key=lambda a: a['publish_date'])
    
    def get_content_gaps(self) -> List[Dict]:
        """Identify topics that need coverage."""
        # Simplified: check which formats haven't been used recently
        used_formats = set(a['format'] for a in self.articles.values())
        unused_formats = [f for f in self.CONTENT_FORMATS if f not in used_formats]
        
        return [{'gap_area': 'format_missing', 'format': f} for f in unused_formats]
```

## Writing Workflow

```python
class BloggingWorkflow:
    """End-to-end blog writing and publishing workflow."""
    
    STAGES = [
        'topic_research', 'keyword_research', 'outline',
        'first_draft', 'self_edit', 'peer_review', 'seo_optimize',
        'final_draft', 'add_media', 'schedule', 'publish',
        'promote', 'track_performance'
    ]
    
    @staticmethod
    def create_brief(topic: str, target_keyword: str, 
                     searcher_intent: str) -> Dict:
        """Create a content brief for writers."""
        return {
            'working_title': topic,
            'target_keyword': target_keyword,
            'searcher_intent': searcher_intent,
            'target_audience': self._define_audience(topic),
            'key_points': [
                f"Define what {target_keyword} means",
                f"Explain why it matters",
                f"Step-by-step guide or actionable tips",
                f"Common mistakes or challenges",
                f"Expert insights or data points",
            ],
            'questions_to_answer': [
                f"What is {target_keyword}?",
                f"Why is {target_keyword} important?",
                f"How do I implement {target_keyword}?",
                f"What are best practices for {target_keyword}?",
            ],
            'suggested_structure': [
                'H1: Title with keyword',
                'H2: What is [topic]?',
                'H2: Why [topic] matters',
                'H2: How to [implement/use] (step-by-step)',
                'H2: Best practices',
                'H2: Common mistakes to avoid',
                'H2: Frequently asked questions',
                'H2: Conclusion with CTA',
            ],
            'competitor_urls': [],
            'word_count_target': 1500,
        }
    
    @staticmethod
    def _define_audience(topic: str) -> Dict:
        """Define target audience for a topic."""
        return {
            'primary': {
                'role': 'Professionals in relevant field',
                'pain_point': f'Needs to understand {topic} quickly',
                'knowledge_level': 'Intermediate',
            },
            'secondary': {
                'role': 'Decision-makers',
                'pain_point': 'Evaluating solutions related to topic',
                'knowledge_level': 'Beginner',
            }
        }
```

## Content Repurposing

```python
class ContentRepurposer:
    """Repurpose blog content for multiple channels."""
    
    @staticmethod
    def repurpose_for_social(blog_content: str, title: str) -> Dict:
        """Convert a blog post into social media content."""
        import re
        
        # Extract key points
        paragraphs = [p for p in blog_content.split('\n\n') if len(p) > 50]
        
        # Social posts for different platforms
        return {
            'twitter_thread': ContentRepurposer._to_twitter_thread(paragraphs[:8]),
            'linkedin_post': {
                'content': f"📝 New: {title}\n\n{paragraphs[0][:200]}...\n\nLink in comments ↓",
                'length': 'medium',
            },
            'instagram_carousel': {
                'slides': [
                    f"Slide 1: {title}",
                    *[f"Slide {i+2}: {p[:150]}" for i, p in enumerate(paragraphs[:4])],
                    "Swipe up for the full guide!",
                ],
                'count': min(len(paragraphs) + 2, 10),
            },
            'email_newsletter': {
                'subject': title,
                'preview': paragraphs[0][:150] if paragraphs else title,
                'content_blocks': [
                    {'type': 'heading', 'text': title},
                    {'type': 'paragraph', 'text': paragraphs[0][:300]},
                    {'type': 'cta', 'text': 'Read the full article →', 'url': '[link]'},
                ],
            },
        }
    
    @staticmethod
    def _to_twitter_thread(paragraphs: List[str]) -> List[str]:
        """Convert paragraphs to Twitter thread."""
        thread = []
        for i, p in enumerate(paragraphs):
            tweet = f"{i+1}/{len(paragraphs)}: {p[:250]}"
            thread.append(tweet)
        thread.append(f"{len(paragraphs)+1}/{len(paragraphs)+1}: 👆 Full guide at [link]")
        return thread
```

## Common Pitfalls

1. **Inconsistent publishing** — readers don't return if posts are unpredictable; stick to a schedule
2. **Writing for search engines first** — readers come first, SEO second; great content naturally attracts links
3. **No content upgrade** — every post should have a related lead magnet (checklist, PDF, template)
4. **Ignoring promotion** — publishing is 20%, promoting is 80%; have a distribution plan for every post
5. **No internal linking** — link to your own relevant content; keeps readers on site longer
6. **Not repurposing** — one blog post can be 10+ social posts, an email, a video, and a podcast

## Verification Checklist

- [ ] Blog platform selected and configured
- [ ] Editorial calendar covers 4+ weeks ahead
- [ ] Content briefs created for upcoming posts
- [ ] Publishing workflow defined (draft → review → edit → schedule → publish)
- [ ] Promotion plan for each post (social, email, syndication)
- [ ] Lead magnet/content upgrade per post
- [ ] Analytics tracking (page views, time on page, conversions)
- [ ] Repurposing workflow established (blog → social → email)

## See Also

- content-writing-seo-copy — writing optimized blog content
- seo-search-engine-optimization — ranking blog content
- cms-website-management — managing the blog platform
- digital-marketing-strategy — blog as part of marketing strategy
