---
name: community-management-engagement
description: "Use when building and managing online communities."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [community-management, engagement, moderation, forums, discord, slack, membership]
    related_skills: [customer-success-retention, social-media-content-planning, customer-feedback-surveys, event-planning-management]
---

# Community Management and Engagement

Building, growing, and managing online communities — from strategy and platform selection through moderation, engagement programs, and community analytics.

## When to Use

- Starting a community (Slack, Discord, Circle, forum)
- Growing engagement and reducing churn in an existing community
- Building a customer community for support and advocacy
- Running member programs (AMA, events, challenges)
- Measuring community health and ROI

## Platform Selection

```python
COMMUNITY_PLATFORMS = {
    'discord': {
        'best_for': 'Gaming, tech, real-time chat, younger demographics',
        'structure': 'Channels (text + voice), roles, threads',
        'moderation': 'Built-in, bots (MEE6, Dyno), auto-mod',
        'monetization': 'Nitro, server subscriptions',
        'limits': 'Unlimited members, 25MB upload (free)',
    },
    'slack': {
        'best_for': 'Professional communities, B2B, work-aligned groups',
        'structure': 'Channels, threads, huddles',
        'moderation': 'Built-in, Workflow Builder, apps',
        'monetization': 'Paid plans for history/unlimited',
        'limits': 'Free: 90-day history, 10 apps',
    },
    'circle': {
        'best_for': 'Paid membership communities, courses, content',
        'structure': 'Spaces, posts, comments, live streams',
        'moderation': 'Built-in, member management',
        'monetization': 'Native subscriptions, Stripe integration',
        'limits': 'Pricing based on members',
    },
    'facebook_group': {
        'best_for': 'Consumer brands, local communities, broad reach',
        'structure': 'Posts, comments, polls, events, live',
        'moderation': 'Auto-mod, keyword filters, admin tools',
        'monetization': 'Sub-only posts, badges',
        'limits': 'Unlimited (algorithm-controlled reach)',
    },
}

def recommend_platform(audience_type: str, monetize: bool, 
                       realtime: bool) -> str:
    if audience_type in ('b2b', 'professional'):
        return 'Slack' if not monetize else 'Circle'
    if realtime:
        return 'Discord'
    if monetize:
        return 'Circle'
    return 'Discord'
```

## Community Manager

```python
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

class CommunityManager:
    """Manage community members, content, and engagement."""
    
    def __init__(self, name: str, platform: str):
        self.name = name
        self.platform = platform
        self.members = {}
        self.posts = []
        self.events = []
        self.engagement_log = []
    
    def add_member(self, username: str, email: str = '',
                   source: str = 'organic', role: str = 'member') -> str:
        import uuid
        mid = str(uuid.uuid4())[:8]
        self.members[mid] = {
            'id': mid, 'username': username, 'email': email,
            'source': source, 'role': role,  # member, moderator, admin
            'joined': datetime.now().isoformat(),
            'last_active': datetime.now().isoformat(),
            'post_count': 0, 'comment_count': 0, 'reactions_given': 0,
            'badges': [],
        }
        return mid
    
    def log_activity(self, member_id: str, activity_type: str):
        if member_id in self.members:
            self.members[member_id]['last_active'] = datetime.now().isoformat()
            if activity_type == 'post':
                self.members[member_id]['post_count'] += 1
            elif activity_type == 'comment':
                self.members[member_id]['comment_count'] += 1
            
            self.engagement_log.append({
                'member_id': member_id, 'type': activity_type,
                'timestamp': datetime.now().isoformat(),
            })
    
    def get_active_members(self, days: int = 30) -> List[Dict]:
        """Get members active within N days."""
        cutoff = datetime.now() - timedelta(days=days)
        active = []
        for m in self.members.values():
            if datetime.fromisoformat(m['last_active']) >= cutoff:
                active.append(m)
        return active
    
    def get_inactive_members(self, days: int = 30) -> List[Dict]:
        """Get members who haven't been active."""
        cutoff = datetime.now() - timedelta(days=days)
        return [m for m in self.members.values() 
                if datetime.fromisoformat(m['last_active']) < cutoff]
    
    def get_community_health(self) -> Dict:
        total = len(self.members)
        if total == 0: return {}
        active_30d = len(self.get_active_members(30))
        active_7d = len(self.get_active_members(7))
        
        return {
            'total_members': total,
            'active_30d': active_30d,
            'active_7d': active_7d,
            'engagement_rate_30d': round(active_30d / total * 100, 1),
            'engagement_rate_7d': round(active_7d / total * 100, 1),
            'new_members_30d': sum(1 for m in self.members.values()
                if (datetime.now() - datetime.fromisoformat(m['joined'])).days <= 30),
            'total_posts': len(self.posts),
            'members_at_risk': len(self.get_inactive_members(60)),
        }
```

## Engagement Programs

```python
ENGAGEMENT_PROGRAMS = {
    'weekly_prompt': {
        'type': 'recurring',
        'frequency': 'Weekly',
        'description': 'Ask a question or prompt to spark discussion',
        'example': '✨ Weekly Wins: What\'s one thing you accomplished this week?',
    },
    'ama': {
        'type': 'event',
        'frequency': 'Monthly',
        'description': 'Ask Me Anything with founder, expert, or power user',
        'planning': 'Book guest 3 weeks ahead, collect questions 1 week ahead',
    },
    'member_spotlight': {
        'type': 'content',
        'frequency': 'Weekly',
        'description': 'Feature a community member and their work/story',
        'format': 'Q&A style post + share across social',
    },
    'challenge': {
        'type': 'event',
        'frequency': 'Monthly/Quarterly',
        'description': 'Themed challenge with prizes or recognition',
        'example': '30-day writing challenge, build week, design jam',
    },
    'virtual_coffee': {
        'type': 'event',
        'frequency': 'Weekly',
        'description': 'Casual video chat for members to connect',
        'format': '30-min unstructured Zoom/Discord',
    },
    'resource_library': {
        'type': 'content',
        'frequency': 'Ongoing',
        'description': 'Curated resources contributed by members',
        'format': 'Pinned thread or wiki with templates, guides, tools',
    },
}

def plan_monthly_calendar() -> str:
    cal = "📅 Community Calendar\n" + "=" * 40 + "\n"
    for name, program in ENGAGEMENT_PROGRAMS.items():
        cal += f"\n{name.replace('_', ' ').title()}"
        cal += f"\n  {program['description']}"
        cal += f" ({program['frequency']})"
    return cal
```

## Moderation Guidelines

```python
MODERATION_POLICY = {
    'allowed': [
        'Constructive discussion and debate',
        'Sharing work for feedback',
        'Asking for help (support)',
        'Sharing relevant resources',
        'Job postings (designated channel)',
    ],
    'not_allowed': [
        'Spam or self-promotion (outside designated channels)',
        'Harassment, hate speech, or personal attacks',
        'Sharing others\' private information (doxxing)',
        'Illegal content or activities',
        'NSFW content',
    ],
    'enforcement': {
        'first_offense': 'Warning (private message)',
        'second_offense': '24-hour mute',
        'third_offense': '7-day suspension',
        'egregious': 'Immediate permanent ban',
    },
}

def community_guidelines(community_name: str) -> str:
    guidelines = f"📜 {community_name} Community Guidelines\n"
    guidelines += "=" * 50 + "\n"
    guidelines += "\n**Be Respectful** — Treat others as you'd like to be treated.\n"
    guidelines += "\n**Stay On Topic** — Keep discussions relevant to the community focus.\n"
    guidelines += "\n**No Spam** — Self-promotion only in designated channels.\n"
    guidelines += "\n**Help Others** — The best communities are built on generosity.\n"
    guidelines += "\n**Report Issues** — See something? @mod or DM an admin.\n"
    return guidelines
```

## Common Pitfalls

1. **Build it and they won't come** — communities need active seeding and content; launch with 50+ warm members
2. **No moderation early** — bad behavior unchecked drives good members away; set tone from day 1
3. **Founder doesn't participate** — if leadership isn't active, community won't be
4. **Over-moderation** — deleting every off-topic post stifles conversation; allow some organic flow
5. **Measuring vanity metrics** — member count doesn't equal healthy community; track engagement rate
6. **No value for members** — if members don't get value, they leave; keep content-to-promotion ratio high

## Verification Checklist

- [ ] Platform selected based on audience and goals
- [ ] Community guidelines posted and enforced
- [ ] Moderation team trained
- [ ] Welcoming/onboarding sequence for new members
- [ ] Weekly engagement programs planned
- [ ] Member recognition program (spotlight, badges, roles)
- [ ] Community health metrics tracked (engagement rate, active, retention)
- [ ] Feedback loop established (members influence community direction)

## See Also

- customer-success-retention — community as retention driver
- social-media-content-planning — cross-promoting community content
- customer-feedback-surveys — community insights
- event-planning-management — community events
