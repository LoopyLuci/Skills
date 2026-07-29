---
name: project-management-workflows
description: "Use when setting up project management systems and flows."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [project-management, workflows, agile, scrum, kanban, task-management, jira]
    related_skills: [crm-sales-pipeline, business-metrics-kpis, cms-website-management, digital-marketing-strategy]
---

# Project Management Workflows

Setting up project management systems, workflows, and processes — from methodology selection through task management, sprint planning, and team collaboration.

## When to Use

- Setting up PM for a new team or project
- Implementing Agile/Scrum or Kanban workflows
- Designing task management workflows
- Running sprint planning, standups, retrospectives
- Tracking project progress and reporting

## Methodology Selection

```python
METHODOLOGIES = {
    'scrum': {'best_for': 'Software teams', 'cadence': '2-week sprints'},
    'kanban': {'best_for': 'Support, maintenance', 'cadence': 'Continuous'},
    'waterfall': {'best_for': 'Construction, regulated', 'cadence': 'Phase-based'},
    'hybrid': {'best_for': 'Marketing, creative', 'cadence': 'Weekly'},
}

def recommend(team_size: int, work_type: str) -> Dict:
    if team_size > 10 and work_type == 'software': return METHODOLOGIES['scrum']
    elif work_type in ('support', 'maintenance'): return METHODOLOGIES['kanban']
    return METHODOLOGIES['hybrid']
```

## Task and Sprint Management

```python
from datetime import datetime
import uuid

class ProjectManager:
    def __init__(self, name: str):
        self.name = name
        self.tasks = {}
        self.sprints = {}
    
    def add_task(self, title: str, assignee: str = None,
                 priority: str = 'medium') -> str:
        task_id = str(uuid.uuid4())[:8]
        self.tasks[task_id] = {
            'id': task_id, 'title': title, 'assignee': assignee,
            'status': 'backlog', 'priority': priority,
            'created_at': datetime.now().isoformat(),
        }
        return task_id
    
    def create_sprint(self, name: str, goal: str, start: str, end: str) -> str:
        sid = str(uuid.uuid4())[:8]
        self.sprints[sid] = {'id': sid, 'name': name, 'goal': goal,
            'start': start, 'end': end, 'tasks': [], 'status': 'planning'}
        return sid
    
    def get_sprint_burndown(self, sid: str) -> Dict:
        sprint = self.sprints.get(sid, {})
        tasks = sprint.get('tasks', [])
        done = sum(1 for t in tasks if self.tasks.get(t, {}).get('status') == 'done')
        return {'total': len(tasks), 'completed': done, 'remaining': len(tasks) - done}
```

## Workflow Templates

```python
WORKFLOWS = {
    'content': {'stages': ['Idea', 'Writing', 'Editing', 'Review', 'Published']},
    'software': {'stages': ['Backlog', 'In Progress', 'Review', 'Testing', 'Done']},
    'sales': {'stages': ['Lead', 'Contacted', 'Demo', 'Proposal', 'Closed']},
}
```

## Common Pitfalls

1. **Tool over process** — buying Jira won't fix broken workflows
2. **Too many statuses** — keep to 5-7; more creates confusion
3. **No WIP limits** — everything "in progress" means nothing finishes
4. **Sprint overload** — commit to less than full capacity
5. **No retros** — teams repeat mistakes without reflection

## Verification Checklist

- [ ] Methodology selected and documented
- [ ] Workflow statuses defined (5-7)
- [ ] WIP limits set per stage
- [ ] Meeting cadence established
- [ ] Velocity tracked over 3+ sprints

## See Also

- crm-sales-pipeline — project management for sales
- business-metrics-kpis — delivery metrics
- cms-website-management — website projects
