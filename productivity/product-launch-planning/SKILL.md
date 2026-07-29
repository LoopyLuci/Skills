---
name: product-launch-planning
description: "Use when planning and executing product launches."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [product-launch, launch-planning, release, announcement, launch-day]
    related_skills: [go-to-market-strategy, product-management-roadmap, sales-enablement-playbooks, digital-marketing-strategy]
---

# Product Launch Planning

Planning and executing product launches — from alpha/beta programs through launch day execution and post-launch analysis.

## When to Use

- Launching a new product, feature, or major update
- Coordinating cross-functional launch teams
- Managing beta programs and early access
- Planning launch day activities and communications
- Measuring launch success and ROI

## Launch Tracks

```python
LAUNCH_TRACKS = {
    'product': ['Feature complete', 'QA/testing', 'Beta program', 'Bug fixes', 'GA release'],
    'marketing': ['Messaging', 'Landing page', 'Blog post', 'Email sequence', 'Social campaign', 'PR'],
    'sales': ['Playbook', 'Training', 'Demo environment', 'Collateral', 'Pricing approval'],
    'customer_success': ['Documentation', 'Support training', 'FAQ/KB', 'Onboarding flow'],
    'analytics': ['Tracking setup', 'Dashboards', 'Success metrics', 'Reporting'],
}

class LaunchCoordinator:
    """Coordinate cross-functional product launch."""
    
    def __init__(self, product: str, version: str, launch_date: str):
        self.product = product
        self.version = version
        self.launch_date = launch_date
        self.tasks = []
        self.beta_users = []
        self.risks = []
    
    def add_task(self, track: str, task: str, owner: str, 
                 due_date: str, dependency: str = None) -> 'LaunchCoordinator':
        import uuid
        self.tasks.append({
            'id': str(uuid.uuid4())[:8],
            'track': track, 'task': task, 'owner': owner,
            'due': due_date, 'dependency': dependency, 'status': 'pending',
        })
        return self
    
    def add_beta_user(self, name: str, email: str, 
                      company: str = '', feedback: str = '') -> 'LaunchCoordinator':
        self.beta_users.append({
            'name': name, 'email': email, 'company': company,
            'feedback': feedback, 'status': 'active',
        })
        return self
    
    def get_launch_readiness(self) -> Dict:
        total = len(self.tasks)
        if total == 0: return {'readiness': 0}
        done = sum(1 for t in self.tasks if t['status'] == 'done')
        blocked = sum(1 for t in self.tasks if t['status'] == 'blocked')
        
        return {
            'readiness_pct': round(done / total * 100, 1),
            'total_tasks': total,
            'completed': done,
            'blocked': blocked,
            'by_track': {track: sum(1 for t in self.tasks if t['track'] == track and t['status'] == 'done') 
                        for track in LAUNCH_TRACKS},
        }
    
    def generate_launch_day_timeline(self) -> str:
        timeline = f"📅 Launch Day Timeline: {self.product} {self.version}\n"
        timeline += "=" * 50 + "\n"
        
        # Standard launch day schedule
        events = [
            ('06:00', 'Final systems check and monitoring setup'),
            ('07:00', 'Release deployed to production'),
            ('07:30', 'Smoke tests pass verification'),
            ('08:00', 'Blog post published'),
            ('08:05', 'Social media announcements go live'),
            ('08:15', 'Email campaign sends'),
            ('08:30', 'Sales team activated for inbound'),
            ('09:00', 'Monitor support channels for issues'),
            ('12:00', 'Mid-day check-in (metrics review)'),
            ('17:00', 'End-of-day metrics snapshot'),
            ('Next day', 'Post-launch retrospective'),
        ]
        
        for time, event in events:
            timeline += f"\n{time} — {event}"
        
        return timeline
```

## Common Pitfalls

1. **Feature creep delaying launch** — adding "just one more feature" pushes dates indefinitely
2. **No internal launch** — employees should be the first to know; brief internally before public
3. **Unprepared support team** — first users hit support before launch is announced; train them
4. **No post-launch plan** — day after launch needs just as much attention as day of
5. **Measuring wrong things** — vanity metrics don't tell if the launch succeeded

## Verification Checklist

- [ ] Product complete and QA verified
- [ ] Beta program completed and feedback incorporated
- [ ] Launch day timeline with owner for each slot
- [ ] All cross-functional tracks on track (product, marketing, sales, CS, analytics)
- [ ] Internal team briefed
- [ ] Support team trained and ready
- [ ] Monitoring dashboards configured
- [ ] Rollback plan defined
- [ ] Post-launch retrospective scheduled

## See Also

- go-to-market-strategy — broader GTM context
- product-management-roadmap — product readiness
- sales-enablement-playbooks — sales readiness
- digital-marketing-strategy — marketing launch plan
