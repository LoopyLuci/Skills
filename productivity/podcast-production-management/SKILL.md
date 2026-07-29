---
name: podcast-production-management
description: "Use when producing and managing podcast episodes."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [podcast, production, audio, editing, distribution, show-notes]
    related_skills: [content-repurposing-distribution, content-writing-seo-copy, blog-building-content-strategy, digital-marketing-strategy]
---

# Podcast Production and Management

Producing, publishing, and growing a podcast — from concept and equipment through recording, editing, distribution, and audience growth.

## When to Use

- Launching a new podcast for your brand or business
- Planning podcast episodes and guest scheduling
- Managing production workflow (recording, editing, publishing)
- Writing show notes and optimizing for discoverability
- Growing podcast audience and measuring performance

## Podcast Setup

```python
PODCAST_SETUP = {
    'naming': {
        'tips': [
            'Include a keyword related to your topic',
            'Keep it memorable and searchable',
            'Check for existing podcasts with the same name',
        ],
    },
    'cover_art': {
        'specs': '3000×3000 pixels, JPG or PNG, <500KB',
        'tips': ['Readable at thumbnail size', 'High contrast', 'Include podcast name'],
    },
    'recording_equipment': {
        'beginner': {'mic': 'USB: Blue Yeti, Audio-Technica ATR2100', 'cost': '$50-150'},
        'intermediate': {'mic': 'XLR: Shure SM58, Rode PodMic', 'interface': 'Focusrite Scarlett 2i2', 'cost': '$200-400'},
        'advanced': {'mic': 'Shure SM7B, Electro-Voice RE20', 'interface': 'Rodecaster Pro, Mixer', 'cost': '$500-1500'},
    },
    'recording_software': {
        'free': ['Audacity', 'OBS Studio', 'GarageBand (Mac)'],
        'paid': ['Descript', 'Adobe Audition', 'Hindenburg Journalist', 'Logic Pro (Mac)'],
        'remote_recording': ['Zencastr', 'Riverside.fm', 'SquadCast', 'Cleanfeed'],
    },
    'hosting': {
        'anchor_spotify': {'cost': 'Free', 'distribution': 'Spotify + all major platforms'},
        'buzzsprout': {'cost': '$12-24/mo', 'distribution': 'All major platforms'},
        'transistor': {'cost': '$19-99/mo', 'distribution': 'All platforms, analytics'},
        'simplecast': {'cost': '$15-85/mo', 'distribution': 'All platforms, advanced analytics'},
    },
}

def recommend_setup(budget: str, remote_guests: bool) -> Dict:
    rec = {}
    if budget == 'low':
        rec['mic'] = "Blue Yeti USB"
        rec['software'] = 'Audacity + Zencastr' if remote_guests else 'Audacity'
        rec['hosting'] = 'Anchor (free)'
    elif budget == 'medium':
        rec['mic'] = 'Shure SM58 + Focusrite Scarlett'
        rec['software'] = 'Descript + Riverside.fm'
        rec['hosting'] = 'Buzzsprout'
    else:
        rec['mic'] = 'Shure SM7B + Rodecaster Pro'
        rec['software'] = 'Adobe Audition + Riverside.fm'
        rec['hosting'] = 'Transistor'
    return rec
```

## Episode Production

```python
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class PodcastEpisode:
    """Plan and produce a podcast episode."""
    
    def __init__(self, title: str, podcast_name: str, episode_num: int):
        self.title = title
        self.podcast = podcast_name
        self.number = episode_num
        self.guests = []
        self.segments = []
        self.links = []
        self.sponsors = []
        self.status = 'planned'
    
    def add_guest(self, name: str, title: str, bio: str = '',
                  social_links: Dict = None) -> 'PodcastEpisode':
        self.guests.append({
            'name': name, 'title': title, 'bio': bio,
            'social': social_links or {},
        })
        return self
    
    def add_segment(self, name: str, duration_minutes: int, 
                    description: str, questions: List[str] = None) -> 'PodcastEpisode':
        self.segments.append({
            'name': name, 'duration': duration_minutes,
            'description': description, 'questions': questions or [],
        })
        return self
    
    def generate_run_sheet(self) -> str:
        total_duration = sum(s['duration'] for s in self.segments)
        
        sheet = f"🎙️ Episode {self.number}: {self.title}\n"
        sheet += f"Duration: ~{total_duration} min\n"
        sheet += "=" * 50 + "\n"
        
        if self.guests:
            sheet += "\n👤 Guest" + ("s" if len(self.guests) > 1 else "") + ":\n"
            for g in self.guests:
                sheet += f"  {g['name']} — {g['title']}\n"
                if g['bio']: sheet += f"  Bio: {g['bio'][:100]}\n"
        
        sheet += "\n📋 Segments:\n"
        running_time = 0
        for seg in self.segments:
            sheet += f"\n  {running_time}:00 — {seg['name']} ({seg['duration']} min)"
            sheet += f"\n    {seg['description']}"
            if seg['questions']:
                for q in seg['questions']:
                    sheet += f"\n    • {q}"
            running_time += seg['duration']
        
        if self.sponsors:
            sheet += f"\n\n📢 Sponsors: {', '.join(s for s in self.sponsors)}"
        
        return sheet
    
    def generate_show_notes(self) -> str:
        notes = f"# {self.title}\n\n"
        notes += f"Episode {self.number} of {self.podcast}\n\n"
        
        if self.guests:
            notes += "## About the Guest\n"
            for g in self.guests:
                notes += f"\n**{g['name']}** — {g['title']}\n"
                if g['bio']: notes += f"{g['bio']}\n"
        
        notes += "\n## What We Cover\n"
        for seg in self.segments:
            notes += f"\n- **{seg['name']}**: {seg['description']}\n"
        
        notes += "\n## Key Takeaways\n1. \n2. \n3. \n"
        
        if self.links:
            notes += "\n## Links & Resources\n"
            for link in self.links:
                notes += f"- {link.get('label', '')}: {link.get('url', '')}\n"
        
        return notes
```

## Production Workflow

```python
PRODUCTION_WORKFLOW = [
    ('Planning', [
        'Topic selection and research',
        'Guest outreach and confirmation',
        'Episode outline and questions',
        'Record intro/outro if applicable',
    ]),
    ('Pre-production', [
        'Send guest prep email (topics, equipment check, recording link)',
        'Set up recording session (Zencastr/Riverside)',
        'Test audio levels and internet connection',
        'Prepare intro music and segments',
    ]),
    ('Recording', [
        'Record local backup (each person records locally)',
        'Record intros and transitions',
        'Take notes during recording for show notes',
    ]),
    ('Post-production', [
        'Edit audio (remove umms, pauses, mistakes, background noise)',
        'Mix levels (normalize volume across speakers)',
        'Add intro/outro music',
        'Export as MP3 (128-192kbps, mono or stereo)',
        'Write show notes and title',
        'Design episode artwork (if needed)',
    ]),
    ('Publishing', [
        'Upload to hosting platform',
        'Write SEO-optimized title and description',
        'Add timestamps and links',
        'Schedule publish date/time',
        'Create promotional assets (audiogram, quote card)',
    ]),
    ('Promotion', [
        'Post on social media (clip + link)',
        'Send to email list',
        'Notify guest (they will share with their audience)',
        'Submit to podcast directories (Spotify, Apple)',
        'Repurpose: blog post, social clips, newsletter',
    ]),
]

def production_checklist(episode: PodcastEpisode) -> str:
    checklist = f"✅ Production Checklist: Episode {episode.number}\n"
    checklist += "=" * 50 + "\n"
    for phase, items in PRODUCTION_WORKFLOW:
        checklist += f"\n**{phase}**\n"
        for item in items:
            checklist += f"  ☐ {item}\n"
    return checklist
```

## Podcast Analytics

```python
PODCAST_METRICS = {
    'downloads': 'Total downloads per episode (within 30/60/90 days)',
    'unique_listeners': 'Estimated unique listeners',
    'listener_retention': 'Average % of episode listened to',
    'subscribers': 'Total subscribers across all platforms',
    'downloads_per_episode': 'Average downloads in first 30 days',
    'growth_rate': 'Month-over-month download growth',
    'top_episodes': 'Episodes with highest downloads',
    'top_sources': 'Where listeners find the show (Spotify, Apple, etc.)',
    'reviews_rating': 'Number of reviews and average star rating',
}

def episode_performance(episode_data: Dict) -> str:
    report = f"📈 Performance: Episode {episode_data.get('number', '?')}\n"
    report += "=" * 40 + "\n"
    report += f"Downloads (30d): {episode_data.get('downloads_30d', 'pending')}\n"
    report += f"Downloads (60d): {episode_data.get('downloads_60d', 'pending')}\n"
    report += f"Retention Rate: {episode_data.get('retention_pct', 'N/A')}%\n"
    report += f"Top Source: {episode_data.get('top_source', 'N/A')}\n"
    return report
```

## Common Pitfalls

1. **Bad audio quality** — listeners forgive content but not audio; invest in a decent mic
2. **No editing** — 45 minutes of umms and rambling loses listeners; edit tightly
3. **Inconsistent publishing** — listeners won't subscribe if schedule is unpredictable
4. **No show notes** — show notes drive SEO and help listeners decide to listen
5. **Not promoting** — podcasting is 20% production, 80% promotion; have a promo plan
6. **No call to action** — listeners won't know to subscribe/review/share unless asked

## Verification Checklist

- [ ] Podcast concept and name defined
- [ ] Cover art designed (3000×3000)
- [ ] Recording equipment secured
- [ ] Hosting platform selected and set up
- [ ] First 3 episodes recorded and edited
- [ ] RSS feed submitted to Apple, Spotify, etc.
- [ ] Show notes template created
- [ ] Intro/outro recorded with music
- [ ] Publishing schedule defined (weekly, bi-weekly)
- [ ] Promotion plan for each episode

## See Also

- content-repurposing-distribution — repurposing podcast content
- content-writing-seo-copy — writing show notes
- blog-building-content-strategy — podcast as content pillar
- digital-marketing-strategy — podcast marketing strategy
