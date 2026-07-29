---
name: social-engineering-phishing
description: "Use when performing social engineering and phishing tests."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [social-engineering, phishing, pretexting, spear-phishing, Gophish, SET]
    related_skills: [osint-reconnaissance-techniques, red-team-operations, evasion-techniques-av-bypass, bug-bounty-methodology]
---

# Social Engineering and Phishing

Performing social engineering assessments — from phishing campaign setup through pretexting, vishing, physical security testing, and awareness training.

## When to Use

- Testing employee security awareness
- Simulating phishing attacks for assessments
- Pretexting for physical access tests
- Building security awareness training
- Measuring organizational resilience to social engineering

## Social Engineering Techniques

```python
SOCIAL_ENG_TYPES = {
    'phishing': 'Email-based — malicious link or attachment, credential harvesting, malware delivery',
    'spear_phishing': 'Targeted phishing with OSINT-gathered personalization (name, role, interests)',
    'whaling': 'Executive-targeted phishing (CEO, CFO, board) — high-value, careful pretext',
    'vishing': 'Voice phishing — phone calls impersonating IT support, vendor, or executive',
    'smishing': 'SMS phishing — text messages with urgent requests, fake package delivery',
    'pretexting': 'Create fabricated scenario to extract information or gain access',
    'tailgating': 'Follow authorized person through secured door (social compliance)',
}

class PhishingCampaign:
    """Manage phishing simulation campaigns."""
    def __init__(self, name: str, target_list: List[str]):
        self.name = name
        self.targets = target_list
        self.emails_sent = 0
        self.clicks = 0
        self.credentials_submitted = 0
    
    def calculate_risk_score(self) -> Dict:
        click_rate = self.clicks / max(self.emails_sent, 1) * 100
        cred_rate = self.credentials_submitted / max(self.emails_sent, 1) * 100
        return {
            'click_rate': round(click_rate, 1),
            'credential_rate': round(cred_rate, 1),
            'risk_level': 'high' if click_rate > 20 else 'medium' if click_rate > 10 else 'low',
        }
```

## Verification Checklist

- [ ] Written authorization from target organization
- [ ] Phishing framework chosen (Gophish, SET, Modlishka)
- [ ] Landing page mirrors legitimate login (credential harvesting)
- [ ] Email headers configured (SPF, DKIM to improve deliverability)
- [ ] Tracking pixel/redirect for click measurement
- [ ] Campaign targets defined with opt-out list
- [ ] Pretexting scenario documented
- [ ] Vishing script prepared (if voice calls in scope)
- [ ] Physical testing methods defined (tailgating, badge cloning)
- [ ] Debrief with client after campaign (findings, recommendations)
- [ ] Sensitive data discarded after engagement
