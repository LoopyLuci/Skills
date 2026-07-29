---
name: real-estate-social-media-content
description: "Social media content for real estate. 30-day calendar."
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [real-estate, social-media, content-planning, marketing]
    related_skills: [real-estate-listing-copywriting, real-estate-market-intel]
---

# Real Estate Social Media Content

Plan, create, and schedule 30 days of real estate social media content across Instagram, Facebook, LinkedIn, TikTok, and YouTube Shorts. Includes platform-specific formats, content pillars, hashtag strategies, and engagement tactics.

## When to Use

- Starting or refreshing a real estate social media presence
- Building a 30-day content calendar from scratch
- Repurposing a listing into multi-platform content
- A client asks how you'll market their property on social
- Driving leads from social platforms to your CRM

## Content Pillars (The Rule of Thirds)

| Pillar | % of Content | Purpose | Examples |
|---|---|---|---|
| **Listings** | 33% | Showcase inventory, drive showings | Tours, open houses, just-listed, price drops, just-sold |
| **Value/Education** | 33% | Build authority, answer buyer/seller questions | Market updates, tips, financing, renovations, process explainers |
| **Personal/Local** | 33% | Build trust, show personality, community connection | Behind-the-scenes, local businesses, team culture, client stories |

## Platform-Specific Formats

### Instagram

| Content Type | Best For | Frequency | Format Specs |
|---|---|---|---|
| Reel | Listing tours, tips, trends | 5-7x/week | 9:16 vertical, 15-60s, trending audio |
| Carousel | Market reports, tips, comparisons | 2-3x/week | 1080×1080, 5-10 slides |
| Story | Open houses, daily updates | Daily | 9:16, 15s per slide, interactive stickers |
| Post | Personal, client stories | 2-3x/week | 1080×1080 or 4:5 |

**Example Reel Script (15 seconds — Listing Tour):**
```
[0:00-0:03] Hook: "Stop scrolling — this is the one 🔥"
[0:03-0:07] Wide shot of kitchen/living: "4BR/3BA in Zilker — $675k"
[0:07-0:11] Fast cuts: primary bed → bath → backyard
[0:11-0:15] CTA: "Link in bio to tour. Your new home is waiting 🏡"
```

**Hashtag Strategy (30 tags per post):**
```
3 broad: #realestate #dreamhome #homesweethome
5 niche-local: #AustinRealEstate #ZilkerHomes #ATXRealtor #AustinLiving #TexasRealEstate
8 specific: #ModernFarmhouse #OpenFloorPlan #ChefsKitchen #MoveInReady
10-14 community: #AustinAgents #ATXRealEstateTeam #AustinHomeSearch
```

### Facebook

| Content Type | Best For | Frequency | Format Specs |
|---|---|---|---|
| Feed Post | Listings, market updates | Daily | 1200×628, text 80-250 chars |
| Facebook Live | Open houses, Q&As, tours | 1x/week | 16:9, min 10 min, stable camera |
| Reel (shared) | Listing videos, tips | 3-4x/week | 9:16, cross-post from IG |
| Event | Open house, webinar | Per event | Location, date, time, RSVP link |

**Post Templates:**

Open House:
```
🚪 OPEN HOUSE THIS WEEKEND
📍 123 Main St, Austin, TX
📅 Sun, July 30 • 1-4 PM

✨ 4BR/3BA • 2,400 sq ft • $675k
☕ Light refreshments served

Come see why Zilker is Austin's most sought-after neighborhood. Bring your clients — everyone welcome!

#OpenHouse #AustinRealEstate #Zilker
```

Just-Listed:
```
🎉 JUST LISTED — Zilker Modern Farmhouse
✨ 4 beds | 3 baths | 2,400 sq ft
💰 $675,000

Highlights:
✅ Chef's kitchen w/ Thermador appliances
✅ Smart home w/ Lutron lighting
✅ 5-min walk to Barton Springs

DM for a private tour or link in comments ↘️
```

### LinkedIn

| Content Type | Best For | Frequency | Format Specs |
|---|---|---|---|
| Long-form post | Market insights, thought leadership | 2-3x/week | 1,200-2,100 chars, no hashtags in body |
| PDF carousel | Market reports, data | 1x/week | Add to post as document |
| Article | Deep dives, neighborhood guides | 1-2x/month | 2,000+ words |

**LinkedIn Post Template:**
```
The Austin market just shifted. Here's what I'm seeing in Q3.

🏡 Days on Market: Up 15% YoY (now 42 days avg)
💰 Median Price: $567k (flat vs Q2 — first time no growth in 3 years)
📊 Inventory: 3.2 months (up from 1.8 months last year)

What does this mean for sellers?
→ Price it right on day 1. Overpricing now leads to DOM creep.
→ Condition matters more than ever. Staging and minor renovations pay off.

What does this mean for buyers?
→ You have negotiating power for the first time since 2020.
→ Rate buydowns and closing credits are back on the table.

Curious about your specific neighborhood? Drop a comment or DM me. I'm running free market reviews all week.

#AustinRealEstate #MarketUpdate #RealEstateTrends
```

### TikTok / YouTube Shorts

| Element | Best Practice |
|---|---|
| Hook (0-3s) | Question or bold statement: "The #1 mistake home sellers make in 2025" |
| Body (3-45s) | Quick cuts, on-screen text, trending sound, show don't tell |
| CTA (last 5s) | "Follow for more Austin real estate tips" or "Link in bio" |
| Caption | 100-150 chars, 3-5 hashtags, emoji in first line |

**TikTok Video Ideas (30-day batch):**
```
1. "You're overpaying if you don't check this one thing" (hidden costs)
2. "Never skip the home inspection" (horror story)
3. "What $500k gets you in Austin vs. Dallas" (comparison)
4. "5 things I'd change about my house" (reno tips)
5. "Reality of being a real estate agent" (BTS)
6. "The worst neighborhoods for investors right now" (hot take)
7. "How to read a CMA" (education)
8. "Open house prep in under 2 minutes" (timelapse)
9. "My favorite paint colors for resale" (tips)
10. "Rate environment explained in 60 seconds" (education)
```

## 30-Day Content Calendar

Generate a complete month of content:

```python
from datetime import datetime, timedelta
import random

def generate_content_calendar(month, year, agent_name, market_city, listings):
    """
    Generate 30 days of social media content.
    listings: list of active listing dicts (address, price, beds, baths, highlights)
    """
    # Content themes by day of week
    themes = {
        'Monday': 'Market Monday 📊',      # Data, stats, market reports
        'Tuesday': 'Tip Tuesday 💡',        # Education, how-to, advice
        'Wednesday': "What's New 🔑",       # Listings, just-listed, new tours
        'Thursday': 'Throwback 🏘️',         # Just-sold, client stories, past deals
        'Friday': 'Feature Friday 🏡',       # Featured listing deep dive
        'Saturday': 'Local Love ❤️',         # Neighborhood, restaurants, spots
        'Sunday': 'Sell the Dream ✨',        # Lifestyle, inspiration, aspirational
    }

    # Content type mix
    content_types = ['reel', 'carousel', 'static', 'story']

    start_date = datetime(year, month, 1)
    num_days = 30
    calendar = []

    for day_offset in range(num_days):
        date = start_date + timedelta(days=day_offset)
        day_name = date.strftime('%A')
        theme = themes.get(day_name, 'Daily Update')

        # Alternate content types
        ctype = content_types[day_offset % len(content_types)]

        # Generate a content plan for the day
        post = {
            'date': date.strftime('%Y-%m-%d'),
            'day': day_name,
            'theme': theme,
            'content_type': ctype,
            'pillar': random.choice(['listings', 'value', 'personal']),
            'suggested_caption': '',
        }

        # Generate caption based on theme
        if day_name == 'Monday':
            post['suggested_caption'] = f"{theme}\n\n{market_city} Market Update - {date.strftime('%B %Y')}\n📈 Median Price: TBD\n📊 Inventory: TBD\n⏱ DOM: TBD\n\nWhat questions do you have about the market? Drop them below! 👇"
        elif day_name == 'Tuesday':
            tip = random.choice([
                "3 things every home inspector wishes you knew before buying",
                "The hidden costs of homeownership (budget for this!)",
                "Why pre-approval matters more than your dream home search",
                "Credit score hacks for future homeowners",
                "Renovations that actually add value to your home",
            ])
            post['suggested_caption'] = f"{theme}\n\n{tip}\n\nSave this for later 📌\nFollow @{agent_name.replace(' ', '_')} for more real estate tips!"
        elif day_name == 'Wednesday':
            if listings:
                listing = listings[day_offset % len(listings)]
                post['suggested_caption'] = f"{theme}\n\n✨ JUST LISTED ✨\n{listing.get('address')}\n{listing.get('beds')}BR/{listing.get('baths')}BA | {listing.get('sqft')} sq ft\n💰 ${listing.get('price', 0):,}\n\nDM for a private tour! 📲"
        elif day_name == 'Thursday':
            post['suggested_caption'] = f"{theme}\n\n🏡 Client highlight: Another happy homeowner found their dream home in {market_city}!\n\nTheir secret? Getting pre-approved before they started looking.\n\nYour story could be next — let's find your perfect home ✨"
        elif day_name == 'Friday':
            if listings:
                listing = listings[(day_offset + 1) % len(listings)]
                post['suggested_caption'] = f"{theme} — Detailed Tour 🎥\n\nSwipe through to see every inch of this stunning {listing.get('beds')}BR home in {market_city}!\n\n📍 {listing.get('address')}\n💵 ${listing.get('price', 0):,}\n\nTap the link in bio for full details 🔗"
        elif day_name == 'Saturday':
            post['suggested_caption'] = f"{theme}\n\nShowing some love for {random.choice(['South Congress', 'Downtown', 'Zilker Park', 'East Austin', 'Mueller', 'The Domain'])}\n\n{random.choice(['Best coffee in town ☕', 'Farmers market finds 🥑', 'Hidden gem alert 💎', 'Weekend brunch spot 🥞', 'Best hiking trail near 🥾'])}\n\nTag your favorite {market_city} spot below! 👇"
        else:  # Sunday
            quote = random.choice([
                "Home is not a place, it's a feeling 🏡",
                "Your home should tell the story of who you are ✨",
                "Every home has a story — let us help you write yours 📖",
                "Dream big, start small, act now 🚀",
            ])
            post['suggested_caption'] = f"{quote}\n\nWhat does home mean to you? Share your thoughts below 💭\n\n#RealEstate {market_city.replace(' ', '')}RealEstate"

        calendar.append(post)

    return calendar

# Example: generate a calendar
listings_sample = [
    {'address': '123 Main St', 'beds': 4, 'baths': 3, 'sqft': 2400, 'price': 675000},
    {'address': '456 Oak Ave', 'beds': 3, 'baths': 2, 'sqft': 1800, 'price': 525000},
]

cal = generate_content_calendar(8, 2026, "Sarah Johnson", "Austin", listings_sample)

print("=" * 80)
print("30-DAY SOCIAL MEDIA CONTENT CALENDAR")
print("=" * 80)
for post in cal[:7]:  # First week preview
    print(f"\n📅 {post['date']} ({post['day']})")
    print(f"📌 Theme: {post['theme']}")
    print(f"🎬 Type: {post['content_type']} | Pillar: {post['pillar']}")
    print(f"✏️ {post['suggested_caption'][:100]}...")
```

## Batch Content Workflow

### Weekly Production Sprint

**Monday (Planning)**
- Finalize 7 posts for upcoming week
- Check for listing changes, events, holidays
- Pre-write all captions

**Tuesday (Visuals)**
- Create/curate all images and videos
- Edit Reels, add captions, trending audio
- Design carousel graphics (Canva, Figma, or Python + Pillow)

**Wednesday (Scheduling)**
- Upload all content to scheduler (Later, Buffer, Meta Business Suite)
- Set optimal posting times (e.g., IG: 11AM or 6PM weekdays)
- Write all comments, replies, and engagement scripts

**Thursday-Friday (Engagement)**
- Spend 30 min/day replying to comments and DMs
- Engage with 10-15 local accounts (like, comment, share)
- Save all UGC and tagged posts for resharing

**Weekend (Capture)**
- Shoot open house video and photos
- Gather testimonials from clients
- Document local events and neighborhood highlights

## Engagement & Growth Tactics

- **Respond within 1 hour**: Meta's algorithm favors quick reply rates. Set up auto-replies for DMs with listing links.
- **Sticker engagement in Stories**: Use polls, Q&A, and quiz stickers to boost reach. Example: "Which kitchen finish? 🖤 Gold vs Matte Black"
- **Comment-to-DM flow**: Reply to comments with "DM me for the full list!" to move leads to DM.
- **Cross-promote with local businesses**: Tag coffee shops, restaurants, gyms. They'll often reshare, getting your account in front of their audience.
- **Post when your audience is online**: 11AM-1PM weekdays for Instagram, 7-9AM for Facebook, 7-8AM and 5-6PM for LinkedIn.
- **Use all 30 hashtags on Instagram**: Mix broad (realestate), local (AustinRealtor), niche (ModernFarmhouse), and trending.
- **Repurpose top-performing content**: If a Reel got 10k views, turn it into a carousel, a LinkedIn post, and a blog post.

## Common Pitfalls

- **Posting without a calendar**: Random posting kills algorithmic consistency. Batch and schedule everything.
- **Over-selling listings**: A feed of nothing but listings looks like a billboard, not a relationship. Follow the 33/33/33 rule.
- **Ignoring video**: Reels and Shorts get 10x the reach of static posts. Every listing needs a video component.
- **No call to action**: Every post should make the audience do something: save, share, comment, DM, click.
- **Inconsistent visual branding**: Different fonts, colors, and filters on every post looks unprofessional. Use brand templates.
- **Not engaging back**: Social media is a two-way street. Posting without replying doesn't build community.
- **Hashtag stuffing in comments**: Instagram now favors hashtags in the caption, not the first comment.
- **Ignoring analytics**: Post what works. If Reels with face-to-camera get 5x views, do more of them.
- **Posting at wrong times**: Late-night posts get buried by morning. Use platform analytics to find your audience's peak hours.
- **No lead capture mechanism**: Every bio should have a link (Linktree, Leadpages, or direct to IDX search). Every DM reply should end with an offer to help.

## Verification Checklist

- [ ] 30-day content calendar generated with daily posts
- [ ] Content pillars balanced (33% listings / 33% value / 33% personal)
- [ ] Platform-specific formats defined for each intended platform
- [ ] Hashtag strategy documented (broad / local / niche / community mix)
- [ ] 5-10 Reel/Shorts video ideas scripted
- [ ] Open house promotion templates ready (IG, FB, LinkedIn)
- [ ] Just-listed and just-sold templates ready
- [ ] Market update carousel template designed
- [ ] Bio optimized with lead capture link
- [ ] Weekly production schedule documented
- [ ] Engagement/response time SLA defined
- [ ] At least one cross-promotion tactic planned
- [ ] Visual brand templates created (Canva or similar)
- [ ] Analytics review scheduled (weekly or monthly)
- [ ] Lead capture flow defined (comment → DM → email/phone → CRM)