---
name: event-planning-management
description: "Use when planning and managing events and conferences."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [event-planning, conferences, webinars, venue, logistics, registration]
    related_skills: [marketing-funnel-design, email-marketing-campaigns, project-management-workflows, lead-generation-strategies]
---

# Event Planning and Management

Planning, organizing, and executing events — from conferences and webinars through product launches, trade shows, and corporate events.

## When to Use

- Planning a conference, summit, or trade show booth
- Running webinars and virtual events
- Organizing product launches or customer events
- Managing event logistics (venue, catering, AV)
- Tracking event budgets, timelines, and ROI

## Event Types

```python
EVENT_TYPES = {
    'conference': {
        'description': 'Multi-day in-person event with speakers, sessions, networking',
        'lead_time': '6-12 months',
        'budget_range': '$50K-$500K+',
        'team_size': '5-20 people',
        'key_metrics': ['Attendance', 'NPS', 'Leads generated', 'Sponsorship revenue'],
    },
    'webinar': {
        'description': 'Online educational session (live or on-demand)',
        'lead_time': '3-6 weeks',
        'budget_range': '$0-$5K',
        'team_size': '1-3 people',
        'key_metrics': ['Registrations', 'Attendance rate', 'Conversion rate'],
    },
    'product_launch': {
        'description': 'In-person or hybrid event unveiling a new product',
        'lead_time': '2-4 months',
        'budget_range': '$10K-$100K',
        'team_size': '3-8 people',
        'key_metrics': ['Media coverage', 'Social reach', 'Demo signups'],
    },
    'trade_show': {
        'description': 'Exhibiting at an industry trade show/conference',
        'lead_time': '3-6 months',
        'budget_range': '$10K-$100K',
        'team_size': '2-6 people',
        'key_metrics': ['Leads collected', 'Meetings booked', 'Brand impressions'],
    },
    'networking': {
        'description': 'Smaller gathering for relationship building',
        'lead_time': '2-6 weeks',
        'budget_range': '$1K-$10K',
        'team_size': '1-3 people',
        'key_metrics': ['Attendance', 'New contacts', 'Follow-up rate'],
    },
}
```

## Event Planner

```python
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class EventPlanner:
    """Plan and track event logistics."""
    
    def __init__(self, name: str, event_type: str, 
                 event_date: str, capacity: int = 100):
        self.name = name
        self.type = event_type
        self.date = event_date
        self.capacity = capacity
        self.budget = 0.0
        self.expenses = []
        self.tasks = []
        self.attendees = []
        self.sponsors = []
    
    def set_budget(self, total: float):
        self.budget = total
    
    def add_expense(self, category: str, description: str, 
                    amount: float, vendor: str = ''):
        self.expenses.append({
            'category': category, 'description': description,
            'amount': amount, 'vendor': vendor,
            'date': datetime.now().isoformat(),
        })
    
    def add_task(self, task: str, owner: str, due_date: str,
                 depends_on: List[str] = None) -> 'EventPlanner':
        import uuid
        tid = str(uuid.uuid4())[:8]
        self.tasks.append({
            'id': tid, 'task': task, 'owner': owner,
            'due': due_date, 'status': 'pending',
            'depends_on': depends_on or [],
        })
        return self
    
    def register_attendee(self, name: str, email: str, 
                          ticket_type: str = 'general',
                          company: str = '') -> str:
        import uuid
        aid = str(uuid.uuid4())[:8]
        self.attendees.append({
            'id': aid, 'name': name, 'email': email,
            'ticket_type': ticket_type, 'company': company,
            'checked_in': False, 'registered': datetime.now().isoformat(),
        })
        return aid
    
    def get_budget_report(self) -> Dict:
        total_spent = sum(e['amount'] for e in self.expenses)
        by_category = {}
        for e in self.expenses:
            by_category[e['category']] = by_category.get(e['category'], 0) + e['amount']
        
        return {
            'total_budget': self.budget,
            'total_spent': total_spent,
            'remaining': self.budget - total_spent,
            'pct_spent': round(total_spent / max(self.budget, 1) * 100, 1),
            'by_category': by_category,
        }
    
    def get_timeline(self) -> List[Dict]:
        return sorted(self.tasks, key=lambda t: t['due'])
    
    def get_attendance_summary(self) -> Dict:
        total_registered = len(self.attendees)
        checked_in = sum(1 for a in self.attendees if a['checked_in'])
        return {
            'capacity': self.capacity,
            'registered': total_registered,
            'checked_in': checked_in,
            'fill_rate': round(total_registered / max(self.capacity, 1) * 100, 1),
            'no_show_rate': round((total_registered - checked_in) / max(total_registered, 1) * 100, 1),
        }
```

## Webinar Production

```python
class WebinarProducer:
    """Plan and produce webinars."""
    
    PRODUCTION_CHECKLIST = [
        'Define topic and learning objectives',
        'Identify and confirm speaker(s)',
        'Create registration page',
        'Set up email confirmation and reminder sequence',
        'Prepare slide deck and visuals',
        'Set up webinar platform (Zoom, GoToWebinar, etc.)',
        'Conduct tech rehearsal (audio, video, screen share, Q&A)',
        'Record backup (local recording in case of streaming issues)',
        'Prepare Q&A moderation plan',
        'Send reminder emails (24h before, 1h before)',
        'Go live! Welcome, housekeeping, intro speaker',
        'Monitor chat and Q&A during event',
        'Post-event: send recording, survey, CTA',
        'Follow-up sequence for no-shows',
    ]
    
    @staticmethod
    def run_sheet(start_time: str, duration_minutes: int = 60) -> str:
        sheet = "🎥 Webinar Run Sheet\n" + "=" * 40 + "\n"
        start = datetime.strptime(start_time, '%H:%M')
        segments = [
            ('Pre-show', 10, 'Tech check, admit attendees, play waiting music'),
            ('Welcome', 5, 'Host intro, housekeeping, poll'),
            ('Presentation', 30, 'Main content delivery'),
            ('Q&A', 15, 'Moderated audience questions'),
            ('CTA & Close', 5, 'Call to action, upcoming events'),
        ]
        
        current = start
        for seg_name, seg_dur, desc in segments:
            sheet += f"\n{current.strftime('%H:%M')} — {seg_name} ({seg_dur}min)"
            sheet += f"\n  {desc}"
            current += timedelta(minutes=seg_dur)
        
        return sheet
```

## Post-Event Analysis

```python
def post_event_report(event: EventPlanner, feedback: List[Dict]) -> str:
    report = f"📋 Post-Event Report: {event.name}\n"
    report += f"Date: {event.date} | Type: {event.type}\n"
    report += "=" * 50 + "\n"
    
    attendance = event.get_attendance_summary()
    report += f"\n📊 Attendance: {attendance['registered']} registered"
    report += f" ({attendance['checked_in']} attended, {attendance['no_show_rate']}% no-show)\n"
    
    budget = event.get_budget_report()
    report += f"\n💰 Budget: ${budget['total_spent']:,.2f} spent of ${budget['total_budget']:,.2f}\n"
    
    if feedback:
        nps_scores = [f.get('nps', 0) for f in feedback if f.get('nps')]
        if nps_scores:
            avg_nps = sum(nps_scores) / len(nps_scores)
            report += f"\n😊 Avg NPS: {avg_nps:.0f}\n"
        
        report += "\n📝 Top Feedback Themes:\n"
        themes = {}
        for f in feedback:
            for theme in f.get('themes', []):
                themes[theme] = themes.get(theme, 0) + 1
        for theme, count in sorted(themes.items(), key=lambda x: x[1], reverse=True)[:3]:
            report += f"  • {theme}: {count}\n"
    
    report += "\n📈 Leads Generated: TBD (post-event follow-up)\n"
    return report
```

## Common Pitfalls

1. **Underestimating lead time** — venues, speakers, and vendors book months in advance
2. **No tech rehearsal** — AV failures are the #1 event problem; always rehearse
3. **Forgetting post-event follow-up** — leads go cold within 48 hours; follow up immediately
4. **Poor WiFi** — for in-person events, bad WiFi is the top complaint; test bandwidth
5. **Over-scheduling** — too many sessions leaves no time for networking; build in breaks
6. **No contingency plan** — speaker cancels, venue floods, internet dies; have backup plans

## Verification Checklist

- [ ] Event type selected and goals defined
- [ ] Budget approved with contingency (10-20%)
- [ ] Venue or platform booked and confirmed
- [ ] Speakers/panelists confirmed
- [ ] Marketing campaign launched (email, social, ads)
- [ ] Registration page live with tracking
- [ ] Production checklist completed (AV, slides, run sheet)
- [ ] Tech rehearsal completed
- [ ] Post-event follow-up sequence set up
- [ ] ROI/attribution plan defined

## See Also

- marketing-funnel-design — event as a funnel stage
- email-marketing-campaigns — event promotion and follow-up
- project-management-workflows — event project plan
- lead-generation-strategies — events as lead source
