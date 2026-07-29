---
name: remote-team-management
description: "Use when managing remote and distributed teams."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [remote-work, distributed-teams, async-communication, remote-culture, hybrid]
    related_skills: [project-management-workflows, performance-review-systems, community-management-engagement, async-communication-patterns]
---

# Remote Team Management

Managing remote and distributed teams — from async communication and meeting rhythms through remote culture, performance management, and collaboration tools.

## When to Use

- Managing a fully remote or hybrid team
- Building remote-first communication practices
- Creating async-first workflows
- Maintaining team culture across time zones
- Onboarding and developing remote employees

## Remote Work Practices

```python
REMOTE_BEST_PRACTICES = {
    'async_first': 'Default to async (docs, recorded video, chat), meeting as last resort',
    'over_communicate': 'Share context generously — remote teams lack hallway conversations',
    'written_culture': 'Decisions documented, not discussed away; write things down',
    'time_zone_aware': 'Rotate meeting times; respect core hours with overlap',
    'results_oriented': 'Measure output, not hours (but beware burnout)',
}

class RemoteTeam:
    """Manage remote team rhythms."""
    def __init__(self, name: str, timezones: List[str]):
        self.name = name
        self.timezones = timezones
    
    def find_overlap(self, meeting_duration: int = 60) -> str:
        """Find best meeting time across time zones."""
        import pytz
        from datetime import datetime, timedelta
        
        local_now = datetime.now()
        overlap_hours = []
        
        # Simplified: find 2-hour window with most team members available
        # Real implementation would check calendar availability
        return "Suggest alternating between 9am ET/3pm CET and 3pm ET/9pm CET"
    
    def communication_rhythm(self) -> Dict:
        return {
            'daily': 'Async stand-up (Slack/bot, not video call)',
            'weekly': 'Team meeting (45 min, recorded, agenda first)',
            'biweekly': '1:1s with manager (30 min, no status update; coaching)',
            'quarterly': 'Team offsite (in-person if possible)',
        }
```

## Common Pitfalls

1. **Meeting overload** — synchronous meetings dominate remote; shift to async by default
2. **Out of sight, out of mind** — remote team members get overlooked for promotions; be intentional
3. **Time zone tyranny** — always scheduling at the same time penalizes some; rotate
4. **No water cooler** — serendipitous interactions need intentional replacement; virtual coffee
5. **Over-documentation** — process for process's sake; document what matters, not everything
6. **Burnout** — remote workers have trouble disconnecting; model healthy boundaries

## Verification Checklist

- [ ] Async-first communication culture established
- [ ] Core overlap hours defined for the team
- [ ] Written culture (decisions documented, meeting notes shared)
- [ ] 1:1s scheduled with every team member
- [ ] Team meeting rotation considers all time zones
- [ ] Career development and visibility for remote members
- [ ] Virtual social events (coffee, games, celebrations)
- [ ] Burnout signals monitored (after-hours messages, vacation usage)
- [ ] Clear expectations on availability and response times
