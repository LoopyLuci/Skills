---
name: customer-education-programs
description: "Use when building customer education and enablement."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [customer-education, enablement, training, certification, knowledge-base, academy]
    related_skills: [customer-onboarding-automation, customer-success-retention, product-led-growth, customer-advocacy-program]
---

# Customer Education Programs

Building customer education and enablement programs — from training content and certification through LMS setup, knowledge bases, and education ROI measurement.

## When to Use

- Reducing time-to-value through customer training
- Building a certification program for power users
- Creating self-service education resources (academy)
- Reducing support tickets through enablement
- Driving product adoption through training

## Education Program Types

```python
EDUCATION_PROGRAMS = {
    'product_training': 'How-to guides, video tutorials, webinars on product usage',
    'certification': 'Structured curriculum with assessments and credentials',
    'knowledge_base': 'Searchable help articles, FAQs, troubleshooting guides',
    'academy': 'On-demand learning platform with courses and progress tracking',
    'community_learning': 'Peer learning, forums, AMAs, user groups',
    'on_demand': 'Self-paced video courses available anytime',
}

class EducationProgram:
    """Design and manage customer education."""
    def __init__(self, name: str):
        self.name = name
        self.courses = []
        self.enrollments = {}  # customer_id -> [course_ids]
    
    def add_course(self, title: str, modules: List[str], 
                   duration_hours: float, certification: bool = False):
        self.courses.append({
            'title': title, 'modules': modules,
            'duration': duration_hours, 'certification': certification,
            'completion_rate': 0,
        })
    
    def enroll(self, customer_id: str, course_id: int) -> bool:
        if course_id < len(self.courses):
            self.enrollments.setdefault(customer_id, []).append(course_id)
            return True
        return False
    
    def program_health(self) -> Dict:
        total = sum(len(e) for e in self.enrollments.values())
        return {
            'total_enrollments': total,
            'total_courses': len(self.courses),
            'active_students': len(self.enrollments),
            'avg_completion': sum(c['completion_rate'] for c in self.courses) / max(len(self.courses), 1),
        }
```

## Common Pitfalls

1. **Content without context** — training that doesn't tie to customer use cases and jobs-to-be-done
2. **No certification value** — certs that no one cares about; align with industry recognition
3. **Static content** — product changes and training becomes outdated; maintain content regularly
4. **Not measuring impact** — education should reduce support tickets and increase adoption; measure it
5. **Text-heavy training** — people learn better with video, interactive exercises, and hands-on labs

## Verification Checklist

- [ ] Training content maps to customer journey stages
- [ ] Content formats varied (video, written, interactive, live)
- [ ] Certification program with assessments
- [ ] Knowledge base searchable and well-organized
- [ ] Customer education platform selected (LMS or academy tool)
- [ ] Content refresh cadence (quarterly for product training)
- [ ] ROI metrics: ticket deflection, adoption increase, NPS improvement
- [ ] Customer feedback collected on training effectiveness
