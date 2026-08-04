---
name: email-marketing-automation
description: "Use when automating email. Sequences, flows, funnels."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [email, marketing, automation, sequences, funnels, drip]
    related_skills: [email-marketing-campaigns, lead-gen-optimization]
---

# Email Marketing Automation

## Overview
Design and deploy automated email sequences and drip campaigns: lead nurturing, customer onboarding, re-engagement, upsell/cross-sell, post-purchase, and abandoned cart recovery. Includes segmentation, deliverability, content strategy, and analytics.

## When to Use
- "Set up a lead nurturing sequence"
- "Automate my customer onboarding emails"
- "Create an abandoned cart flow"
- "Build an email funnel from scratch"

## Email Automation Types

| Type | Trigger | Goal | Typical Length |
|------|---------|------|----------------|
| Lead Nurture | Form submit, content download | Qualify leads, move to SQL | 7-14 days, 6-10 emails |
| Welcome Series | Account created | Activate new users | 7-14 days, 5-7 emails |
| Onboarding | Product signup | Drive first success | 14-30 days, 7-12 emails |
| Check-in | Inactive user | Re-engage, prevent churn | 7-14 days, 3-5 emails |
| Post-Purchase | Purchase confirmed | Upsell, reviews, loyalty | 30-90 days, 6-12 emails |
| Abandoned Cart | Cart not completed | Recover revenue | 4-24 hours, 3-4 emails |
| Win-back | Churned/lapsed | Reactivate customer | 30-60 days, 4-6 emails |
| Replenishment | Previous purchase + X days | Repeat purchase | Ongoing, automated |

## Email Automation Builder Framework

### Step 1: Define the Trigger
```yaml
Trigger: "User downloads e-book from landing page"
Segment: "New lead, hasn't purchased in 30 days"
Timing: "0 minutes (immediate send)"
```

### Step 2: Map the User Journey
| Email # | Timing | Goal | Content | CTA |
|---------|--------|------|---------|-----|
| 1 | +0 min | Deliver promise | E-book download link + thank you | Read now |
| 2 | +1 day | Build trust | Your story/why we made this | Meet the team |
| 3 | +3 days | Educate | Key insight from e-book | Deep dive article |
| 4 | +5 days | Social proof | Case study of results | See case study |
| 5 | +7 days | Address objections | Common concerns + solutions | Chat with us |
| 6 | +10 days | Offer | Special promo/different offer | Claim offer |
| 7 | +14 days | Final push | Last chance + bonus | Final call |

### Step 3: Segmentation Rules
Build segments using behavioral + demographic data:

**Leads:**
- Job title (decision maker vs individual contributor)
- Company size (SMB vs enterprise)
- Industry vertical
- Content interests (which topics they engaged with)
- Engagement level (email opens, link clicks)

**Customers:**
- Product tier (free vs paid)
- Usage frequency (active vs dormant)
- Purchase history (frequency, value)
- Support interactions (number of tickets)

## Email Sequence Templates

### Lead Nurture Sequence (7 emails, 8 days)
Use when a lead downloads content but doesn't convert:

**Email 1 — Immediate (0 hours)**
- Deliver the promised content
- Thank them for their interest
- CTA: Read the content / follow on social

**Email 2 — Next day (24 hours)**
- Share a related story or case study
- CTA: Read the case study

**Email 3 — Day 3 (72 hours)**
- Address a key objection or concern
- CTA: Schedule a call / live demo

**Email 4 — Day 5**
- Educational content (deeper dive into topic)
- CTA: Read the guide / watch the video

**Email 5 — Day 6**
- Social proof (testimonials, stats)
- CTA: Get a free consultation

**Email 6 — Day 7**
- Product-focused but soft sell
- CTA: Try free trial / request demo

**Email 7 — Day 8 (Final)**
- Last value-add content + gentle close
- CTA: Limited time offer / final consultation

### Abandoned Cart Recovery (4 emails, 48 hours)
**Email 1 — 1 hour after abandonment**
Subject: "Wait! Don't forget your cart"
- Show items in their cart
- CTA: Return to checkout

**Email 2 — 24 hours**
Subject: "Still thinking it over?"
- Add scarcity (items selling fast)
- Add a small discount (free shipping, 5% off)

**Email 3 — 36 hours**
Subject: "Your cart is expiring"
- Urgency (cart will be cleared)
- Stronger incentive (10% off)

**Email 4 — 48 hours**
Subject: "Last chance — items removed"
- Cart cleared
- Win-back offer

## Email Content Strategy

### Subject Line Frameworks
| Framework | Example | Best For |
|-----------|---------|----------|
| Curiosity | "You won't believe what we found..." | Cold, curiosity-driven |
| Direct | "Your cart is waiting" | Clear, transactional |
| Numbers | "5 mistakes killing your [metric]" | Educational |
| Benefit | "Save 3 hours per week" | Value-focused |
| Urgency | "24 hours left" | Time-sensitive |
| Personalization | "[Name], about your [product] cart..." | Relationship-based |

### Preheader Text (the text after the subject line)
- Acts as a "second subject line"
- Keep under 120 characters
- Reinforce the subject or add new angle
- Often determines open decision alongside subject

### Email Copy Structure
1. **Above the fold (preview)**: Subject + preheader must compel opening
2. **Opening sentence**: Deliver on the promise, immediately useful
3. **Body**: 1-3 short paragraphs, scannable
4. **CTA block**: Button above the fold AND at the bottom
5. **P.S.**: Highest-read section — add urgency or bonus

## Deliverability Optimization

### Sender Reputation Factors
| Factor | Best Practice |
|--------|--------------|
| Sender domain | Use a subdomain (email.yourdomain.com) |
| SPF record | Set up SPF for your sending domain |
| DKIM | Enable DKIM to sign emails |
| DMARC | Configure with quarantine or reject |
| Engagement | High open/click rates = better deliverability |
| Complaints | Keep under 0.1% complaint rate |
| Bounces | Keep under 2% bounce rate |

### Spam Trigger Words (avoid)
- "Free," "Guarantee," "Act now," "100%," "No obligation," "Cash," "Winner," "Urgent," "Risk-free," "Limited time," "Click below"

Use these instead: "Try," "Get started," "Offer ends," "Last chance," "Explore," "See how"

### Frequency & Timing
- **Lead nurture**: 2-3 emails per week max
- **Welcome/onboarding**: Every 2-3 days
- **Abandoned cart**: Spaced out (1h, 24h, 36h, 48h)
- **General marketing**: Weekly at most
- **Time**: 10 AM - 12 PM local time, Tuesday-Thursday

## Automation Analytics & Optimization

### Key Metrics by Automation Type
| Metric | Lead Nurture | Welcome | Onboarding | Cart Recovery |
|--------|-------------|---------|------------|---------------|
| Open Rate | >35% | >60% | >50% | >50% |
| Click Rate | >8% | >25% | >15% | >10% |
| Conversion Rate | >5% | >20% | >15% | >20% |
| Unsubscribe Rate | <0.1% | <0.05% | <0.1% | <0.2% |
| Bounce Rate | <2% | <1% | <2% | <1% |

### A/B Testing Opportunities
1. **Subject line**: Test 2-3 variants per email
2. **Send time**: Test 9am vs 1pm vs 4pm
3. **CTA text**: "Get Started" vs "Try Free" vs "Learn More"
4. **CTA color**: Green vs orange vs blue
5. **Hero image**: With vs without
6. **Personalization**: Name in subject line yes/no
7. **Email length**: Short vs long format
8. **Value prop**: Benefit-focused vs feature-focused

### Iterative Optimization Process
1. Week 1: Launch with best practices
2. Week 2-3: Identify lowest-performing emails
3. Week 4: A/B test subject lines on weakest email
4. Week 5: A/B test CTA on weakest email
5. Month 2: A/B test the strongest email for incremental gains
6. Monthly: Review all metrics, refresh content, adjust timing

## Common Pitfalls
1. **No clear goal per email** — each email should have one CTA, not five
2. **Ignoring unsubscribes** — high unsubs mean content isn't wanted; respect that preference
3. **Sending too frequently** — 7 emails in 3 days = list damage
4. **Generic content** — email should reference known context (what they downloaded, where they dropped off)
5. **No segmentation** — sending the same sequence to leads and existing customers
6. **Broken links** — test every link before scheduling
7. **Mobile-unfriendly** — 65%+ of email opens are mobile; preview on phone
8. **Forgetting the preview text** — it's as important as the subject line

## Verification Checklist
- [ ] Automation type defined with clear goal
- [ ] Trigger event identified (form submit, purchase, inactivity)
- [ ] User journey mapped (email → timing → goal → CTA)
- [ ] Segmentation rules defined (behavioral + demographic)
- [ ] 5-7 email templates written with subject + preheader
- [ ] CTA strategy per email (button text, placement)
- [ ] Deliverability setup checked (SPF/DKIM/DMARC)
- [ ] Content reviewed for spam triggers
- [ ] Send frequency and timing decided
- [ ] Key metrics defined for each email in sequence