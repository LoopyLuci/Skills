---
name: data-minimization-framework
description: "Use when handling data. Collect only what's needed."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [privacy, data-minimization, gdpr-compliance, pii, data-governance]
    related_skills: [privacy-by-design-skill-authoring, secure-data-handling]
---

# Data Minimization Framework

## Overview
Apply data minimization principles to Hermes skill creation and usage: collect, process, and store only the minimum amount of data necessary for each specific purpose. Aligns with GDPR Article 5(1)(c) and CCPA data minimization requirements.

## When to Use
- When designing a skill that handles any input
- Reviewing what data a skill actually needs versus what it asks for
- Auditing data flow through skill workflows
- Planning logging and storage for skills

## Core Principle
**Ask for less, keep less, need less.** Every piece of data collected creates risk — storage, processing, transmission, and potential leakage. If data isn't strictly necessary, don't collect it.

## The Data Minimization Checklist

### Step 1: Define the Explicit Purpose
For each data point a skill would collect, complete this sentence:
> "This skill needs [data type] to achieve [specific purpose]. Without it, the skill cannot [specific function]."

If you can't complete the sentence specifically and honestly, the data is not needed.

### Step 2: Data Inventory — What Does the Skill Handle?

| Data Element | Is It Necessary? | Why | Legal Basis | Retention |
|-------------|------------------|-----|-------------|-----------|
| User's free-text input | | | Contractual necessity | Ephemeral (process & discard) |
| User's email address | | | | Session only |
| File paths | | | | Never stored |
| IP addresses (if logged) | | | | Not logged |
| Names/titles | | | | Not collected |

### Step 3: Input Validation with Purpose Limitation
```python
# BAD — collects everything:
def process_user_data(**kwargs):
    # Processes all keyword arguments
    return analyze(**kwargs)

# GOOD — only accepts necessary fields:
def process_project_description(
    project_name: str,  # Required: identifies the project to analyze
    description: str,    # Required: text to analyze
    # No extra fields accepted — they're not needed
):
    # Input validation
    if not project_name or len(project_name) > 100:
        raise ValueError("project_name is required (max 100 chars)")
    if not description or len(description) > 10000:
        raise ValueError("description is required (max 10000 chars)")
    
    result = analyze(description)
    # project_name used only for logging (redacted), never stored
    log_redacted(project_name)
    return result
```

### Step 4: Storage Minimization

| Data Type | Storage Policy |
|-----------|----------------|
| Raw user input | Never stored — process and discard |
| Processed results | Ephemeral or explicitly requested |
| Logs | Redact PII — never log raw input content |
| API responses | Ephemeral — use immediately, discard |
| Credentials/secrets | Environment variables only — never in code |

### Step 5: Processing Scope
```python
# Only process data within a clearly defined boundary:

class SkillProcessor:
    def __init__(self):
        # Maximum input sizes — prevents data hoarding
        self.max_input_length = 10000  # characters
        self.max_name_length = 100     # characters
        
    def process(self, user_input: str) -> str:
        # Validate size
        if len(user_input) > self.max_input_length:
            raise ValueError(f"Input exceeds {self.max_input_length} characters")
        
        # Process immediately — never cache raw input
        result = self._internal_process(user_input)
        
        # Input is discarded after processing
        return result
```

### Step 6: Output Sanitization
Never echo back raw input:
```python
# BAD:
def summarize(text):
    return f"Summary of: {text}"

# GOOD:
def summarize(text):
    result = generate_summary(text)
    return result  # No raw input echoed
```

## Logging and Debug Data

### What to Log (Safe)
```python
# Safe logging:
logger.info("Processing started", extra={
    "project_id": "[REDACTED]",     # Never log real names
    "input_length": len(text),     # Size only — never content
    "processing_time_ms": elapsed,
})
```

### What NOT to Log
- Raw user input text/content
- Email addresses, names, any PII
- File paths with personal identifiers
- API keys, tokens, credentials
- Stack traces that include variable values

## Data Retention Policy for Skills
| Data Category | Retention | Reason |
|---------------|-----------|--------|
| User input | 0 seconds (ephemeral) | GDPR: purpose fulfilled immediately |
| Processing output | User's session | Discarded on tab close |
| Logs | 7 days max | Debug only, PII-stripped |
| Configuration | As needed (persistent) | Non-personal, app settings |
| Cache | 24 hours max | Performance optimization only |

## The "Need-to-Know" Test
Before adding any field, feature, or logging to a skill, pass it through this test:

1. **Is it necessary** for the stated purpose? If the skill works without it, remove it.
2. **Is it proportional** to the benefit? Does the value of collecting this data outweigh privacy risk?
3. **Is it temporary**? Can the data be processed and discarded?
4. **Is it visible**? Can the user see and control what's collected?
5. **Is it documented**? Does the Privacy Impact section explain this data use?

If any test fails, the data handling doesn't meet minimization standards.

## Common Pitfalls
1. **"We might need it later"** — storing data "just in case" violates GDPR's purpose limitation principle
2. **Default max inputs** — accepting unlimited input when 1000 words is sufficient
3. **Logging for debugging** — debug logs often accidentally capture PII
4. **Caching raw input** — Redis/Memcached with raw user text creates retention liabilities
5. **Feature creep** — adding fields/features that need additional data not justified by core purpose
6. **Example data bloat** — templates with elaborate personal scenarios increase leakage risk

## Verification Checklist
- [ ] Explicit purpose defined for every data element
- [ ] Data inventory completed (element, necessity, legal basis, retention)
- [ ] Input validation with max lengths and purpose limitation
- [ ] No raw user input stored or cached beyond processing
- [ ] Logs redacted — PII stripped from all log entries
- [ ] Output never echoes raw sensitive input
- [ ] Maximum input sizes defined and enforced
- [ ] Retention policies documented per data type
- [ ] "Need-to-know" test passed for each field/feature