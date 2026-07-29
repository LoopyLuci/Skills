---
name: list-building-email-growth
description: "Use when growing email lists and lead generation strategies."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [email-list, lead-generation, opt-in, list-building, subscribers, growth]
    related_skills: [email-marketing-campaigns, marketing-funnel-design, content-writing-seo-copy, digital-marketing-strategy]
---

# List Building and Email Growth

Building and growing email subscriber lists through ethical lead generation — from opt-in strategies and lead magnets through landing pages, pop-ups, and list cleaning.

## When to Use

- Growing an email subscriber list from scratch
- Designing opt-in forms and landing pages
- Creating lead magnets that convert
- Implementing list cleaning and compliance
- Building lead generation funnels

## Opt-In Strategy

```python
from typing import Dict, List, Optional
from datetime import datetime

class OptInStrategist:
    """Design ethical opt-in strategies."""
    
    TYPES = {
        'single_optin': {
            'description': 'User submits email, immediately added to list',
            'pros': 'Higher conversion rate, simpler flow',
            'cons': 'Higher invalid/non-consensual emails',
            'compliance': 'GDPR: not sufficient alone',
        },
        'double_optin': {
            'description': 'User submits, receives confirmation email, must click to confirm',
            'pros': 'Higher quality list, better deliverability, GDPR compliant',
            'cons': '20-30% dropoff on confirmation step',
            'compliance': 'GDPR: best practice',
        },
        'confirmed_optin': {
            'description': 'User submits, receives single email to confirm, no second click',
            'pros': 'Better than single, verifies email exists',
            'cons': 'Still weaker than double opt-in legally',
            'compliance': 'GDPR: acceptable',
        },
    }
    
    @staticmethod
    def recommend(business_type: str, region: str) -> Dict:
        """Recommend opt-in strategy based on context."""
        if region in ('eu', 'uk', 'california'):
            return {
                'type': 'double_optin',
                'reasoning': 'Required for GDPR compliance in EU/UK',
                'recovery_flow': 'Send reminder email after 24h if not confirmed',
            }
        elif business_type in ('enterprise', 'finance', 'healthcare'):
            return {
                'type': 'double_optin',
                'reasoning': 'High trust requirement for sensitive industries',
            }
        return {
            'type': 'single_optin',
            'reasoning': 'Lower friction for content/newsletter lists',
            'note': 'Ensure clear privacy policy and unsubscribe option',
        }
```

## Pop-Up and Form Builder

```python
class OptInFormBuilder:
    """Design high-converting opt-in forms and pop-ups."""
    
    FORM_TEMPLATES = {
        'popup_timed': {
            'trigger': 'After 30 seconds on page',
            'headline': 'Never Miss an Update',
            'subheadline': 'Get the latest [topic] insights delivered to your inbox',
            'button': 'Subscribe',
            'design': 'Centered modal with overlay',
            'conversion_tip': 'Best for content sites and blogs',
        },
        'popup_exit': {
            'trigger': 'Mouse leaves the window (exit intent)',
            'headline': 'Wait! Don\'t Miss Out',
            'subheadline': 'Get our free [lead magnet] before you go',
            'button': 'Send Me the Free Guide',
            'design': 'Exit-intent triggered, large modal',
            'conversion_tip': 'Best for recovering abandoning visitors',
        },
        'inline_form': {
            'trigger': 'Embedded in content, after first scroll',
            'headline': 'Enjoying this? Get more delivered!',
            'subheadline': 'Subscribe for weekly insights',
            'button': 'Subscribe',
            'design': 'Inline with content, minimal styling',
            'conversion_tip': 'Best in blog posts and long-form content',
        },
        'slide_in': {
            'trigger': 'After 50% scroll or 60 seconds',
            'headline': 'Join [number] subscribers',
            'subheadline': 'Free weekly newsletter with [topic] tips',
            'button': 'Join Free',
            'design': 'Bottom-right slide, less intrusive',
            'conversion_tip': 'Best for mobile and non-intrusive capture',
        },
        'landing_page': {
            'trigger': 'Dedicated landing page from social/ad traffic',
            'headline': 'Get Your Free [Lead Magnet]',
            'subheadline': 'Join [number] people who already downloaded',
            'button': 'Download Now — It\'s Free',
            'design': 'Full landing page with hero image and form',
            'conversion_tip': 'Best for dedicated ad campaigns',
        },
    }
    
    @staticmethod
    def suggest_form(page_type: str, traffic_source: str) -> Dict:
        """Suggest optimal form type based on context."""
        if traffic_source == 'ad' or page_type == 'landing':
            return OptInFormBuilder.FORM_TEMPLATES['landing_page']
        elif page_type in ('blog', 'article'):
            return [OptInFormBuilder.FORM_TEMPLATES['inline_form'],
                    OptInFormBuilder.FORM_TEMPLATES['popup_exit']]
        elif traffic_source == 'social':
            return OptInFormBuilder.FORM_TEMPLATES['popup_timed']
        return OptInFormBuilder.FORM_TEMPLATES['slide_in']
```

## Lead Magnet Creator

```python
class LeadMagnetCreator:
    """Create lead magnets that drive opt-in conversions."""
    
    LEAD_MAGNET_TYPES = {
        'pdf_guide': {
            'effort': 'medium',
            'conversion': 'high',
            'best_for': 'Educational content, how-to, comprehensive guides',
            'example_titles': [
                "The Ultimate Guide to [topic]",
                "10 Ways to [benefit] Without [pain]",
                "[Topic] Checklist: Everything You Need",
            ],
        },
        'email_course': {
            'effort': 'high',
            'conversion': 'very_high',
            'best_for': 'Building relationships, multi-touch nurture',
            'format': '5-7 email sequence delivered over 7-14 days',
        },
        'template_kit': {
            'effort': 'medium',
            'conversion': 'high',
            'best_for': 'Action-oriented audiences who want ready-to-use resources',
            'example_titles': [
                "[Topic] Templates Pack",
                "The Ultimate [Topic] Spreadsheet",
                "[Number] Ready-to-Use [Resource] Templates",
            ],
        },
        'webinar': {
            'effort': 'very_high',
            'conversion': 'very_high',
            'best_for': 'High-ticket offers, B2B, complex topics',
            'format': '30-60 minute live or recorded video training',
        },
        'tool_calculator': {
            'effort': 'very_high',
            'conversion': 'extremely_high',
            'best_for': 'Interactive value, finance/health/marketing niches',
            'format': 'Interactive web tool requiring email to access results',
        },
        'cheatsheet': {
            'effort': 'low',
            'conversion': 'high',
            'best_for': 'Quick-reference content, low-commitment subscribers',
            'format': '1-page PDF, infographic, or reference card',
        },
    }
    
    @staticmethod
    def suggest(niche: str, audience: str, 
                effort_level: str = 'medium') -> List[Dict]:
        """Suggest lead magnet types for a niche."""
        suggestions = {
            'health_fitness': ['pdf_guide', 'cheatsheet', 'email_course'],
            'finance_investing': ['tool_calculator', 'pdf_guide', 'template_kit'],
            'marketing_business': ['template_kit', 'webinar', 'email_course'],
            'technology_saas': ['tool_calculator', 'webinar', 'template_kit'],
            'education_learning': ['email_course', 'pdf_guide', 'cheatsheet'],
            'lifestyle_personal': ['cheatsheet', 'pdf_guide', 'email_course'],
        }
        
        recommended_types = suggestions.get(niche, ['pdf_guide', 'cheatsheet'])
        
        results = []
        for lt in recommended_types:
            if lt in LeadMagnetCreator.LEAD_MAGNET_TYPES:
                magnet = LeadMagnetCreator.LEAD_MAGNET_TYPES[lt]
                if magnet['effort'] == effort_level or True:  # Include all, let user decide
                    results.append({
                        'type': lt,
                        'effort': magnet['effort'],
                        'conversion': magnet['conversion'],
                        'description': magnet.get('best_for', ''),
                    })
        
        return results[:3]
```

## List Cleaning and Maintenance

```python
class ListHealthManager:
    """Maintain list health through cleaning and monitoring."""
    
    @staticmethod
    def audit_list(emails: List[Dict]) -> Dict:
        """Audit an email list for health issues."""
        total = len(emails)
        issues = {'invalid_format': 0, 'disposable': 0, 'duplicates': 0, 'bounced': 0}
        
        seen = set()
        for email in emails:
            addr = email.get('email', '')
            
            # Check format
            if '@' not in addr or '.' not in addr.split('@')[-1]:
                issues['invalid_format'] += 1
                continue
            
            # Check duplicates
            if addr.lower() in seen:
                issues['duplicates'] += 1
            seen.add(addr.lower())
            
            # Check for disposable email domains
            domain = addr.split('@')[-1].lower()
            disposable = ['mailinator.com', 'guerrillamail.com', 'tempmail.com',
                         '10minutemail.com', 'throwaway.email']
            if domain in disposable:
                issues['disposable'] += 1
            
            if email.get('bounced', False):
                issues['bounced'] += 1
        
        health_score = round((1 - sum(issues.values()) / max(total, 1)) * 100, 1)
        
        return {
            'total_subscribers': total,
            'active_subscribers': total - sum(issues.values()),
            'health_score': health_score,
            'health_rating': 'good' if health_score >= 90 else 'fair' if health_score >= 70 else 'needs_cleaning',
            'issues': issues,
            'recommendations': ListHealthManager._recommendations(issues, total),
        }
    
    @staticmethod
    def _recommendations(issues: Dict, total: int) -> List[str]:
        recs = []
        if issues['bounced'] > total * 0.05:
            recs.append(f"Remove {issues['bounced']} bounced emails immediately")
        if issues['invalid_format'] > 0:
            recs.append(f"Review {issues['invalid_format']} invalid-format emails")
        if issues['disposable'] > 10:
            recs.append("Block disposable email domains at signup")
        if not recs:
            recs.append("List is healthy — no immediate cleaning needed")
        return recs
```

## Common Pitfalls

1. **Buying lists** — violates CAN-SPAM/GDPR, destroys sender reputation; always use opt-in
2. **Single opt-in for critical lists** — lower list quality; use double opt-in for important segments
3. **Ignoring deliverability** — list growth matters little if emails go to spam; monitor inbox placement
4. **No re-engagement** — inactive subscribers hurt deliverability; re-engage or remove after 6 months
5. **Topping up without cleaning** — adding new subscribers but never removing bounces/inactive kills health
6. **No preference center** — subscribers who can choose frequency/content stay longer

## Verification Checklist

- [ ] Opt-in method chosen (single, double, or confirmed)
- [ ] GDPR/CAN-SPAM compliance (privacy policy, consent records, unsubscribe link)
- [ ] Lead magnet designed and connected to welcome sequence
- [ ] Opt-in forms placed in optimal locations (pop-up, inline, slide-in, landing page)
- [ ] Double opt-in confirmation email set up
- [ ] Welcome sequence (3-7 emails) connected to signup
- [ ] List cleaning schedule established (monthly removal of bounces/inactive)
- [ ] Preference center offered (frequency, content topics)
- [ ] Re-engagement campaign set for 6-month inactive subscribers
- [ ] Deliverability monitoring (inbox placement rate, spam complaints)

## See Also

- email-marketing-campaigns — what to send to the list
- marketing-funnel-design — list building as funnel top
- content-writing-seo-copy — writing lead magnet content
- digital-marketing-strategy — list growth strategy
