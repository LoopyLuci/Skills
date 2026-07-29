---
name: sms-marketing-messaging
description: "Use when implementing SMS marketing and messaging campaigns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sms, messaging, text-marketing, SMS-campaigns, compliance, TCPA]
    related_skills: [email-marketing-campaigns, marketing-automation-workflows, list-building-email-growth, digital-marketing-strategy]
---

# SMS Marketing and Messaging

Implementing SMS marketing campaigns — from opt-in and compliance through campaign types, automation sequences, and performance tracking.

## When to Use

- Launching SMS marketing for ecommerce or retail
- Building automated SMS sequences (abandoned cart, order updates)
- Ensuring TCPA/CTIA compliance for text marketing
- Segmenting audiences for targeted SMS campaigns
- Measuring SMS ROI and conversion rates

## Compliance Essentials

```python
COMPLIANCE_REQUIREMENTS = {
    'opt_in': [
        'Express written consent required (no pre-checked boxes)',
        'Disclosure: "Msg & data rates may apply, Reply STOP to cancel"',
        'Consent must be recorded and stored',
        'Single-opt-in acceptable for SMS (unlike email)',
    ],
    'opt_out': [
        'Reply STOP to opt out (mandatory)',
        'HELP for help information',
        'Opt-out must be processed immediately',
        'Cannot send after opt-out (even transactional)',
    ],
    'content': [
        'Identify yourself in every message',
        'Include opt-out instructions in every campaign message',
        'No texting before 8am or after 9pm local time',
        'Transaction messages cannot include marketing content',
    ],
    'record_keeping': [
        'Store consent records for 4+ years',
        'Log all sent messages with timestamps',
        'Track opt-outs with permanent suppression lists',
    ],
}

def check_sms_compliance(campaign: Dict) -> List[str]:
    issues = []
    if not campaign.get('opt_in_method'):
        issues.append("No express written consent collected")
    if 'STOP' not in campaign.get('message', '').upper():
        issues.append("Missing opt-out instructions (Reply STOP)")
    if campaign.get('hour') and (campaign['hour'] < 8 or campaign['hour'] > 21):
        issues.append("Sending outside 8am-9pm window")
    return issues or ["Compliant"]
```

## SMS Campaign Builder

```python
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class SMSCampaign:
    """Build and manage SMS marketing campaigns."""
    
    def __init__(self, name: str, business_name: str):
        self.name = name
        self.business = business_name
        self.messages = []
        self.segments = []
        self.schedule = None
    
    def add_message(self, text: str, delay: str = '0h',
                    trigger: str = None) -> 'SMSCampaign':
        """Add a message to the sequence."""
        self.messages.append({
            'text': text[:160],  # Standard SMS: 160 chars
            'delay': delay,
            'trigger': trigger,
        })
        return self
    
    def set_schedule(self, start: str, end: str = None,
                     send_hour: int = 10) -> 'SMSCampaign':
        self.schedule = {'start': start, 'end': end, 'hour': send_hour}
        return self
    
    def generate_campaign_preview(self) -> str:
        preview = f"📱 SMS Campaign: {self.name}\n"
        preview += f"Business: {self.business}\n" + "=" * 40 + "\n"
        
        for i, msg in enumerate(self.messages, 1):
            preview += f"\nSMS {i} ({msg['delay']}):"
            preview += f"\n  {msg['text']}"
            preview += f"\n  [STOP to opt out]"
        
        return preview
```

## Common Pitfalls

1. **Non-compliance** — TCPA violations cost $500-$1500 per text; get express consent
2. **Too many texts** — SMS is intrusive; 2-4 texts per month max for marketing
3. **No segmentation** — blasting everyone with the same message causes opt-outs
4. **Long messages** — over 160 chars = 2 credits; keep concise
5. **No opt-out processing** — delayed STOP processing violates regulations
6. **Ignoring time zones** — sending at 7am in their time = instant opt-out

## Verification Checklist

- [ ] Express written consent collected and stored
- [ ] Privacy policy includes SMS terms
- [ ] Opt-out (STOP) keyword active and tested
- [ ] Help (HELP) keyword active
- [ ] Sending window set to 8am-9pm local time
- [ ] Message includes business identification
- [ ] Campaign messages include opt-out instruction
- [ ] Opt-out suppression list maintained
- [ ] Consent records retained

## See Also

- email-marketing-campaigns — multi-channel strategy
- marketing-automation-workflows — SMS automation triggers
- list-building-email-growth — growing SMS opt-in list
- digital-marketing-strategy — SMS role in marketing mix
