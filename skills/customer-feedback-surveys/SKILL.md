---
name: customer-feedback-surveys
description: "Use when designing surveys and managing customer feedback."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [customer-feedback, surveys, NPS, CSAT, CES, VOC, voice-of-customer]
    related_skills: [customer-success-retention, product-management-roadmap, saas-metrics-reporting, business-metrics-kpis]
---

# Customer Feedback and Surveys

Designing, deploying, and analyzing customer feedback programs — from NPS and CSAT surveys through qualitative research and Voice of Customer (VoC) programs.

## When to Use

- Measuring customer satisfaction and loyalty (NPS, CSAT)
- Gathering product feedback for roadmap decisions
- Running customer interviews and user research
- Building a Voice of Customer program
- Analyzing feedback at scale to find patterns

## Survey Types

```python
SURVEY_TYPES = {
    'nps': {
        'name': 'Net Promoter Score',
        'question': 'How likely are you to recommend [company] to a friend or colleague?',
        'scale': '0-10',
        'scoring': '9-10: Promoters, 7-8: Passives, 0-6: Detractors',
        'formula': 'NPS = %Promoters - %Detractors',
        'cadence': 'Quarterly or after key milestones',
        'follow_up': 'Why did you give that score? (open text)',
    },
    'csat': {
        'name': 'Customer Satisfaction Score',
        'question': 'How satisfied were you with [experience]?',
        'scale': '1-5 (Very Dissatisfied → Very Satisfied)',
        'scoring': '4-5: Satisfied, 1-3: Not Satisfied',
        'formula': 'CSAT = % of respondents scoring 4-5',
        'cadence': 'After each interaction (support, purchase)',
    },
    'ces': {
        'name': 'Customer Effort Score',
        'question': 'How easy was it to [resolve issue / complete task]?',
        'scale': '1-5 (Very Difficult → Very Easy)',
        'scoring': 'Higher is better (less effort)',
        'cadence': 'After support interactions, onboarding',
    },
}
```

## Survey Builder

```python
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class SurveyBuilder:
    """Design and deploy customer surveys."""
    
    def __init__(self, name: str, survey_type: str):
        self.name = name
        self.type = survey_type
        self.questions = []
        self.target_audience = []
        self.triggers = []
    
    def add_question(self, text: str, question_type: str,
                     required: bool = True, options: List[str] = None,
                     scale_min: int = None, scale_max: int = None) -> 'SurveyBuilder':
        self.questions.append({
            'id': len(self.questions) + 1,
            'text': text,
            'type': question_type,  # rating, multiple_choice, open_text, yes_no
            'required': required,
            'options': options,
            'scale': {'min': scale_min, 'max': scale_max} if scale_min else None,
        })
        return self
    
    def set_triggers(self, events: List[str], delay_hours: int = 0):
        """Set when survey is sent (e.g., after purchase, after support ticket)."""
        self.triggers = [{'event': e, 'delay_hours': delay_hours} for e in events]
        return self
    
    def build_nps(self) -> 'SurveyBuilder':
        """Build standard NPS survey."""
        self.add_question(
            "How likely are you to recommend us to a friend or colleague?",
            'rating', scale_min=0, scale_max=10
        )
        self.add_question("What's the primary reason for your score?", 'open_text')
        self.add_question("What could we do better?", 'open_text', required=False)
        return self
    
    def build_csat(self, interaction: str = 'experience') -> 'SurveyBuilder':
        """Build CSAT survey after an interaction."""
        self.add_question(
            f"How satisfied were you with your {interaction}?",
            'rating', scale_min=1, scale_max=5
        )
        self.add_question("What worked well?", 'open_text', required=False)
        self.add_question("What could be improved?", 'open_text', required=False)
        return self
```

## Feedback Analyzer

```python
class FeedbackAnalyzer:
    """Analyze survey responses and feedback at scale."""
    
    @staticmethod
    def analyze_nps(responses: List[Dict]) -> Dict:
        """Analyze NPS survey results."""
        total = len(responses)
        if total == 0: return {}
        
        promoters = sum(1 for r in responses if r.get('score', 0) >= 9)
        passives = sum(1 for r in responses if 7 <= r.get('score', 0) <= 8)
        detractors = sum(1 for r in responses if r.get('score', 0) <= 6)
        
        nps_score = round((promoters - detractors) / total * 100, 1)
        
        return {
            'responses': total,
            'nps_score': nps_score,
            'promoters': {'count': promoters, 'pct': round(promoters/total*100, 1)},
            'passives': {'count': passives, 'pct': round(passives/total*100, 1)},
            'detractors': {'count': detractors, 'pct': round(detractors/total*100, 1)},
            'rating': 'Excellent' if nps_score >= 50 else 'Great' if nps_score >= 30 else 'Good' if nps_score >= 0 else 'Needs improvement',
        }
    
    @staticmethod
    def analyze_csat(responses: List[Dict]) -> Dict:
        """Analyze CSAT survey results."""
        scores = [r.get('score', 0) for r in responses]
        total = len(scores)
        if total == 0: return {}
        
        satisfied = sum(1 for s in scores if s >= 4)
        csat_score = round(satisfied / total * 100, 1)
        
        return {
            'responses': total,
            'csat_score': csat_score,
            'avg_score': round(sum(scores)/total, 2),
            'distribution': {i: scores.count(i) for i in range(1, 6)},
        }
    
    @staticmethod
    def extract_themes(open_ended: List[str]) -> Dict[str, int]:
        """Extract common themes from open-ended feedback."""
        # Simple keyword-based theme extraction
        themes = {
            'pricing': ['price', 'cost', 'expensive', 'cheap', 'value', 'pricing', 'bill'],
            'support': ['support', 'help', 'customer service', 'response', 'agent', 'cs'],
            'features': ['feature', 'missing', 'would like', 'need', 'wish', 'functionality'],
            'usability': ['easy', 'difficult', 'confusing', 'intuitive', 'interface', 'UI', 'UX'],
            'performance': ['slow', 'fast', 'speed', 'lag', 'performance', 'crash', 'bug'],
            'onboarding': ['setup', 'onboarding', 'getting started', 'first time', 'tutorial'],
        }
        
        results = {}
        for theme, keywords in themes.items():
            count = sum(1 for text in open_ended 
                       if any(kw in text.lower() for kw in keywords))
            if count > 0:
                results[theme] = count
        
        return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
```

## VoC Program

```python
class VoiceOfCustomer:
    """Build a Voice of Customer program."""
    
    SOURCES = {
        'surveys': ['NPS', 'CSAT', 'CES', 'Product-specific'],
        'support': ['Tickets', 'Chat logs', 'Call transcripts'],
        'reviews': ['G2/Capterra', 'App Store', 'Google Play'],
        'social': ['Twitter mentions', 'Reddit', 'LinkedIn'],
        'sales': ['Lost deal reasons', 'Objections', 'Competitive mentions'],
        'product': ['Usage data', 'Feature requests', 'User testing'],
    }
    
    @staticmethod
    def quarterly_report(feedback_data: Dict) -> str:
        report = "🗣️ Voice of Customer Report — Quarterly\n"
        report += "=" * 50 + "\n"
        
        report += f"\n📊 NPS: {feedback_data.get('nps', 'N/A')} "
        report += f"(Responses: {feedback_data.get('nps_responses', 0)})\n"
        report += f"😊 CSAT: {feedback_data.get('csat', 'N/A')}%\n"
        
        report += "\n📈 Top Themes from Feedback:\n"
        themes = feedback_data.get('themes', {})
        for theme, count in sorted(themes.items(), key=lambda x: x[1], reverse=True)[:5]:
            report += f"  {theme}: {count} mentions\n"
        
        report += "\n🎯 Action Items:\n"
        for item in feedback_data.get('action_items', []):
            report += f"  ☐ {item}\n"
        
        return report
```

## Common Pitfalls

1. **Survey fatigue** — asking too often reduces response rates; limit to key touchpoints
2. **Leading questions** — "How great was your experience?" biases responses; stay neutral
3. **Not closing the loop** — collecting feedback without acting on it erodes trust
4. **Only quantitative** — numbers tell what, not why; pair with open-ended questions
5. **Ignoring detractors** — detractors give the most actionable feedback; follow up
6. **No benchmark** — NPS of 30 means nothing without industry context; compare

## Verification Checklist

- [ ] NPS program established (quarterly cadence)
- [ ] CSAT surveys triggered after key interactions
- [ ] Open-ended feedback analyzed for themes
- [ ] Feedback loop closed (respond to feedback, share actions taken)
- [ ] VoC data shared with product, support, and leadership
- [ ] Response rate targets set and monitored
- [ ] Industry benchmarks identified for comparison

## See Also

- customer-success-retention — acting on feedback for retention
- product-management-roadmap — feedback-driven roadmapping
- saas-metrics-reporting — NPS as a leading indicator
- business-metrics-kpis — customer satisfaction KPIs
