---
name: email-marketing-campaigns
description: "Use when building and managing email marketing campaigns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [email-marketing, campaigns, newsletters, automation, deliverability]
    related_skills: [crm-sales-pipeline, marketing-funnel-design, social-media-content-planning, digital-marketing-strategy]
---

# Email Marketing Campaigns

Building and managing email marketing campaigns — from list building and segmentation through campaign creation, automation sequences, deliverability optimization, and analytics.

## When to Use

- Creating email newsletters and nurture sequences
- Building automated email flows (welcome, abandoned cart, re-engagement)
- Segmenting email lists for targeted campaigns
- Improving email deliverability (avoiding spam folders)
- Analyzing email performance (open rates, click rates, conversions)

## Campaign Types

```python
CAMPAIGN_TYPES = {
    'welcome_sequence': '5-7 email sequence for new subscribers',
    'nurture': 'Educational content to build trust over time',
    'promotional': 'Product launches, sales, offers',
    'newsletter': 'Regular content digest (weekly/monthly)',
    'abandoned_cart': 'Recovery sequence for ecommerce',
    're_engagement': 'Win-back inactive subscribers',
    'transactional': 'Order confirmations, receipts, shipping updates',
    'event': 'Webinar registrations, event reminders, follow-ups',
    'birthday': 'Personalized greetings and offers',
}
```

## Campaign Builder

```python
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import smtplib
from email.mime.text import MIMEText
import csv

class EmailCampaign:
    """Design and execute email marketing campaigns."""
    
    def __init__(self, name: str, campaign_type: str):
        self.name = name
        self.type = campaign_type
        self.emails = []  # Ordered sequence of emails
        self.segments = []
        self.created_at = datetime.now().isoformat()
    
    def add_email(self, subject: str, body_html: str,
                  delay_hours: int = 0, delay_days: int = 0,
                  goal: str = "", track_links: bool = True) -> 'EmailCampaign':
        """Add an email to the campaign sequence."""
        self.emails.append({
            'subject': subject,
            'body_html': body_html,
            'delay': f"{delay_days}d {delay_hours}h" if delay_days or delay_hours else "0h",
            'delay_hours': delay_hours + delay_days * 24,
            'goal': goal,
            'track_links': track_links,
            'metrics': {'sent': 0, 'opens': 0, 'clicks': 0, 'unsubscribes': 0},
        })
        return self  # Fluent API
    
    def set_segments(self, segments: List[str]):
        """Target specific list segments."""
        self.segments = segments
        return self
    
    def get_sequence_timeline(self) -> str:
        """Generate a timeline of the email sequence."""
        timeline = f"\n📧 Campaign: {self.name} ({self.type})\n"
        timeline += "=" * 50 + "\n"
        
        cumulative = 0
        for i, email in enumerate(self.emails, 1):
            cumulative += email['delay_hours']
            days = cumulative // 24
            hours = cumulative % 24
            timeline += f"\nEmail {i} | +{days}d {hours}h | {email['subject']}"
            timeline += f"\n  Goal: {email['goal']}"
            timeline += f"\n  {'─' * 40}"
        
        return timeline
    
    def estimate_delivery_window(self) -> Dict:
        """Calculate total campaign duration."""
        total_hours = sum(e['delay_hours'] for e in self.emails)
        return {
            'total_duration_hours': total_hours,
            'total_duration_days': round(total_hours / 24, 1),
            'email_count': len(self.emails),
        }
```

## Welcome Sequence Example

```python
# 7-email welcome sequence
welcome = EmailCampaign("New Subscriber Welcome", "welcome_sequence")
welcome.add_email(
    "Welcome to [Brand]! Here's your [lead magnet]",
    "<h1>Thanks for joining!</h1><p>As promised, here's your free resource...</p>",
    delay_hours=0, goal="Deliver lead magnet"
).add_email(
    "Meet the team behind [Brand]",
    "<p>We thought you'd like to know who we are...</p>",
    delay_days=1, goal="Build connection and trust"
).add_email(
    "How to get the most out of [product/service]",
    "<p>A quick-start guide to get results fast...</p>",
    delay_days=2, goal="Onboard and educate"
).add_email(
    "[Customer] achieved [result] — here's how",
    "<p>See how someone like you used [product] to get [result]...</p>",
    delay_days=4, goal="Social proof"
).add_email(
    "Your [product] checklist for [specific outcome]",
    "<p>A practical checklist to get started...</p>",
    delay_days=5, goal="Provide value, increase engagement"
).add_email(
    "Quick question about your experience",
    "<p>We'd love to hear how things are going...</p>",
    delay_days=7, goal="Gather feedback, qualify interest"
).add_email(
    "Ready to take the next step?",
    "<p>Here's a special offer just for you...</p>",
    delay_days=10, goal="Conversion/purchase"
)
```

## Deliverability Optimization

```python
class DeliverabilityOptimizer:
    """Optimize email deliverability (avoid spam folder)."""
    
    SPAM_TRIGGER_WORDS = [
        'free', 'guaranteed', 'act now', 'limited time', 'click here',
        'buy now', 'discount', 'earn money', 'congratulations',
        'winner', 'prize', 'cash', 'bonus', 'no cost', 'call now',
        'double your', 'instant', 'once in a lifetime',
    ]
    
    @staticmethod
    def check_spam_score(email_body: str) -> Dict:
        """Check email for spam triggers and score it."""
        body_lower = email_body.lower()
        
        # Check spam trigger words
        found_triggers = [w for w in DeliverabilityOptimizer.SPAM_TRIGGER_WORDS 
                         if w in body_lower]
        
        # Check formatting issues
        issues = []
        if 'ALL CAPS' in email_body or any(w.isupper() for w in email_body.split() if len(w) > 4):
            issues.append("Excessive use of ALL CAPS")
        
        # Count images vs text ratio
        import re
        images = len(re.findall(r'<img', email_body))
        text = len(re.sub(r'<[^>]+>', '', email_body))
        if images > 3 and text < 100:
            issues.append("Too many images, too little text")
        
        # Exclamation marks
        exclamation_count = email_body.count('!')
        if exclamation_count > 3:
            issues.append(f"Too many exclamation marks ({exclamation_count})")
        
        # Red flags
        has_red_flags = len(found_triggers) > 2 or len(issues) > 0
        
        return {
            'score': max(0, 100 - len(found_triggers) * 10 - len(issues) * 15),
            'spam_triggers_found': found_triggers,
            'formatting_issues': issues,
            'is_red_flag': has_red_flags,
            'recommendations': [
                f"Remove '{w}'" for w in found_triggers
            ] + issues,
        }
    
    @staticmethod
    def optimize_subject_line(subject: str) -> Dict:
        """Optimize email subject line for opens."""
        # Length check
        if len(subject) > 60:
            return {'subject': subject[:57] + '...', 'truncated': True}
        
        # Personalization
        if '{name}' not in subject.lower() and '{first_name}' not in subject.lower():
            return {'subject': subject, 'suggestion': 'Add personalization tag for +20% opens'}
        
        return {'subject': subject, 'suggestion': None}
    
    @staticmethod
    def dkim_spf_setup(domain: str) -> List[str]:
        """Instructions for email authentication setup."""
        return [
            f"1. Add SPF record: v=spf1 include:_spf.your-email-service.com ~all",
            f"2. Add DKIM record from your email service provider",
            f"3. Add DMARC record: v=DMARC1; p=quarantine; rua=mailto:dmarc@{domain}",
            f"4. Verify: dig TXT {domain} | grep 'v=spf1'",
            f"5. Verify: dig TXT _dmarc.{domain} | grep 'v=DMARC1'",
        ]
```

## Analytics and Metrics

```python
class EmailAnalytics:
    """Track and analyze email campaign performance."""
    
    INDUSTRY_BENCHMARKS = {
        'saas': {'open_rate': 25, 'click_rate': 3.5, 'unsub_rate': 0.3},
        'ecommerce': {'open_rate': 20, 'click_rate': 3.0, 'unsub_rate': 0.4},
        'publishing': {'open_rate': 30, 'click_rate': 4.0, 'unsub_rate': 0.2},
        'real_estate': {'open_rate': 28, 'click_rate': 4.5, 'unsub_rate': 0.2},
        'education': {'open_rate': 32, 'click_rate': 5.0, 'unsub_rate': 0.1},
    }
    
    @staticmethod
    def analyze_campaign(campaign: EmailCampaign, 
                         industry: str = 'saas') -> Dict:
        """Analyze campaign performance vs benchmarks."""
        benchmarks = EmailAnalytics.INDUSTRY_BENCHMARKS.get(industry, 
                     EmailAnalytics.INDUSTRY_BENCHMARKS['saas'])
        
        results = []
        for email in campaign.emails:
            m = email['metrics']
            sent = max(m['sent'], 1)
            open_rate = round(m['opens'] / sent * 100, 1)
            click_rate = round(m['clicks'] / sent * 100, 1)
            unsub_rate = round(m['unsubscribes'] / sent * 100, 2)
            
            results.append({
                'subject': email['subject'],
                'open_rate': open_rate,
                'click_rate': click_rate,
                'unsub_rate': unsub_rate,
                'open_vs_benchmark': round(open_rate - benchmarks['open_rate'], 1),
                'click_vs_benchmark': round(click_rate - benchmarks['click_rate'], 1),
            })
        
        return {
            'campaign': campaign.name,
            'industry': industry,
            'benchmarks': benchmarks,
            'email_results': results,
            'overall_open_rate': round(
                sum(m['opens'] for m in campaign.emails) / 
                max(sum(m['sent'] for m in campaign.emails), 1) * 100, 1
            ),
            'overall_click_rate': round(
                sum(m['clicks'] for m in campaign.emails) / 
                max(sum(m['sent'] for m in campaign.emails), 1) * 100, 1
            ),
        }
    
    @staticmethod
    def suggest_improvements(analysis: Dict) -> List[str]:
        """Suggest improvements based on performance data."""
        suggestions = []
        
        for email in analysis.get('email_results', []):
            if email['open_rate'] < analysis['benchmarks']['open_rate']:
                suggestions.append(
                    f"Improve subject line: '{email['subject'][:50]}...' "
                    f"is below benchmark ({email['open_rate']}% vs {analysis['benchmarks']['open_rate']}%)"
                )
            if email['click_rate'] < analysis['benchmarks']['click_rate']:
                suggestions.append(f"Add clearer CTA to email. CTR below benchmark.")
        
        return suggestions[:5]
```

## Common Pitfalls

1. **Buying email lists** — illegal in most jurisdictions (GDPR, CAN-SPAM); always use opt-in
2. **No segmentation** — sending the same email to everyone causes unsubscribes; segment by behavior
3. **Ignoring mobile** — 60%+ of emails are opened on mobile; design responsive emails
4. **Too many emails** — frequency fatigue; let subscribers choose their preferred cadence
5. **No A/B testing** — guess what works vs test subject lines, CTAs, send times, offers
6. **Weak CTAs** — "click here" gets fewer clicks than specific, benefit-driven CTAs

## Verification Checklist

- [ ] Email list collected via opt-in (not purchased)
- [ ] Segmentation strategy defined (by behavior, interests, engagement)
- [ ] Welcome sequence set up (first touch within 24 hours)
- [ ] SPF, DKIM, DMARC configured
- [ ] Spam score checked before every send
- [ ] Mobile-responsive template used
- [ ] A/B testing plan for subject lines
- [ ] Unsubscribe link prominently placed
- [ ] Analytics tracking (opens, clicks, conversions) configured
- [ ] GDPR/CAN-SPAM compliance (opt-in, privacy policy, unsubscribe)

## See Also

- crm-sales-pipeline — integrating email with sales
- marketing-funnel-design — email sequences for funnels
- social-media-content-planning — cross-promoting email and social
- digital-marketing-strategy — role of email in marketing mix
