---
name: consent-management-skills
description: "Use when managing user consent. GDPR, CCPA, opt-out."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [consent, gdpr, ccpa, privacy, opt-in, opt-out, data-processing]
    related_skills: [legal-and-compliance-basics, privacy-by-design-skill-authoring, data-leakage-prevention-in-skills]
---

# Consent Management for Skills

## Overview
Implement GDPR/CCPA-compliant consent management for Hermes skills: granular consent collection, consent withdrawal mechanisms, cookie consent integration, "Do Not Sell" handling, and audit trail maintenance for data-processing operations.

**⚠️ This skill provides a framework for consent workflows. When implementing consent in actual software, always consult with a privacy attorney for legal compliance in your jurisdiction.**

## When to Use
- "Add consent management to this skill"
- "Handle GDPR consent for user data processing"
- "Implement CCPA 'Do Not Sell' opt-out"
- "Track user consent for data processing operations"
- "Need a consent audit trail for compliance"

## Consent Categories (GDPR Article 7)

### Essential (Always Active)
These are required for core functionality and do not require explicit consent:
- Ephemeral input processing (process and discard, never stored)
- Error handling for skill execution (logs redacted of PII)
- Basic authentication to access skill features

### Performance (Optional — Requires Consent)
These improve experience but are not required:
- Anonymous usage analytics (aggregate, no PII)
- Performance benchmarking (no user-level data)
- Feature usage tracking (aggregated only)

### Functional (Optional — Requires Consent)
These enable enhanced features:
- Saving user preferences (theme, layout preferences)
- Custom configurations (saved templates, workspaces)
- Personalization features

### Marketing (Optional — Requires Consent)
- Promotional communications (email, in-app banners)
- Product update announcements with marketing
- Affiliate/partner program participation

## Consent Implementation Pattern

### Consent Object Structure
```json
{
  "user_id": "hashed_or_anonymized_identifier",
  "consents": {
    "essential": {"granted": true, "timestamp": "2024-01-15T10:30:00Z", "version": "1.0"},
    "performance": {"granted": false, "timestamp": null, "version": null},
    "functional": {"granted": true, "timestamp": "2024-01-15T10:30:00Z", "version": "1.0"},
    "marketing": {"granted": false, "timestamp": null, "version": null}
  },
  "metadata": {
    "ip_country": "US",
    "user_agent": "platform-version",
    "consent_language": "en"
  }
}
```

### Consent Check Pattern
```python
def check_consent(user_id: str, purpose: str) -> bool:
    """
    Check if user has given consent for a specific purpose.
    Default: deny if no record exists (GDPR-safe default).
    """
    consent = load_user_consent(user_id)
    if not consent:
        return False
    
    purpose_consent = consent.get("consents", {}).get(purpose, {})
    return purpose_consent.get("granted", False)

def request_consent(user_id: str, purpose: str, description: str) -> bool:
    """
    Present consent request to user before processing.
    GDPR requires consent to be: informed, specific, unambiguous, and freely given.
    """
    # Display consent dialog via the platform's native UI:
    # "[Purpose]: [Description]"
    # "This means we will [specific data use]"
    # "Learn more: [Privacy Policy]"
    # Buttons: [Accept] [Reject]
    
    user_choice = show_platform_consent_dialog(
        title=f"Permission Request: {purpose}",
        message=description,
        options=["Allow", "Don't Allow"]
    )
    
    # Record the consent decision with full audit trail
    record_consent(user_id, purpose, user_choice, version="1.0")
    return user_choice == "Allow"

# Usage in skill workflow:
def process_skill_with_analytics(user_data: str, user_id: str):
    # Essential processing is always allowed
    result = core_processing(user_data)
    
    # Check for optional analytics consent
    if check_consent(user_id, "performance"):
        # Safe to collect anonymous analytics
        collect_anonymous_metrics({
            "input_length": len(user_data),
            "output_type": type(result).__name__,
            "processing_time_ms": measure_duration()
        })
    
    return result
```

### Consent Withdrawal (GDPR Article 21)
Users must be able to withdraw consent as easily as giving it:

```python
def withdraw_consent(user_id: str, purpose: str):
    """
    Withdraw consent — MUST be as easy as granting it.
    Immediately stops processing and deletes data collected under that consent.
    """
    consent_record = load_user_consent(user_id)
    consent_record["consents"][purpose] = {
        "granted": False,
        "timestamp": get_current_iso_timestamp(),
        "version": consent_record["consents"][purpose]["version"]
    }
    save_user_consent(user_id, consent_record)
    
    # Immediately purge any data collected under this consent
    purge_user_data_by_purpose(user_id, purpose)
    log_audit_event("consent_withdrawn", user_id, purpose)

def list_user_consents(user_id: str) -> dict:
    """Return all consent decisions for transparency"""
    consent = load_user_consent(user_id)
    return {
        purpose: {
            "granted": details.get("granted", False),
            "since": details.get("timestamp"),
            "can_withdraw": not details.get("granted", False)  # Essential stays on
        }
        for purpose, details in consent.get("consents", {}).items()
    }
```

## CCPA "Do Not Sell My Personal Information"

### When CCPA Applies to Skills
CCPA considers a "sale" any transfer of personal information to a third party for valuable consideration. This includes:
- Sending data to analytics services (Google Analytics, Mixpanel)
- Using third-party AI APIs with user data
- Affiliate/referral program data sharing
- Advertising pixels or tracking scripts

If your skill sends user data to any third party (including AI model providers), you likely need a "Do Not Sell" option.

### Implementation Pattern for CCPA
```python
# CCPA consent states
CCPA_CONSENT_STATES = {
    "opted_in": True,    # Explicit permission to share/sell data
    "opted_out": False,   # Explicit request to not sell data
    "pending": True      # Default — not explicitly opted out
}

def check_ccpa_status(user_id: str) -> bool:
    """
    Returns True if data sale is permitted (not opted out).
    CCPA requires honoring opt-out requests within 15 days.
    """
    consent = load_user_consent(user_id)
    ccpa_status = consent.get("metadata", {}).get("ccpa_status", "pending")
    
    if ccpa_status == "opted_out":
        return False  # Do not sell
    else:
        return True  # Sell permitted (pending or opted in)

def process_with_ccpa_compliance(user_id: str, user_data: str):
    """Full GDPR + CCPA compliant processing"""
    # GDPR consent check (for analytics, features, etc.)
    has_gdpr_consent = check_consent(user_id, "performance")
    
    # CCPA check (for data sales to third parties)
    can_share_data = check_ccpa_status(user_id)
    
    # Process essential function (always allowed)
    result = core_processing(user_data)
    
    # Optional processing (GDPR consent required)
    if has_gdpr_consent:
        collect_analytics(result)
    
    # Third-party sharing (CCPA compliance)
    if can_share_data:
        # Safe to send anonymized result to third party
        share_with_partner(anonymize(result))
    else:
        # CCPA opt-out — only local processing
        log_audit_event("ccpa_opt_out_honored", user_id)
        # Local-only processing, no external transmission
    
    return result
```

## Consent Interface Design

### Skill-Level Consent Prompt
When a skill first needs non-essential data access:

```
Permission Request: Performance Analytics

This skill would like to collect anonymous usage data to improve performance:
• Processing time per request
• Error occurrence rates
• Feature usage statistics

No personal data or inputs will be transmitted. Data is aggregated and anonymized.

[Allow] [Don't Allow] [Manage Settings]

You can change these any time in Settings → Privacy.
```

### Consent Settings Panel (Pattern)
Allow users to manage all consent preferences:

```
Privacy Settings
─────────────────────────────────────────────────
[✓] Essential (required for operation)
[✕] Performance (anonymous usage analytics)     [Change]
[✓] Functional (save preferences, themes)       [Change]  
[✕] Marketing (product updates, tips)           [Change]
─────────────────────────────────────────────────
California Resident Rights:
[Do Not Sell My Personal Information]

Your consent history: [View Record] | [Download JSON] | [Withdraw All]
```

## Consent Audit Trail

### Logging Consent Events
Every consent action must be logged for compliance:

```python
def log_consent_event(event_type: str, user_id: str, purpose: str, additional_data: dict = None):
    """
    Audit events for GDPR/CCPA compliance — never include raw PII
    """
    audit_entry = {
        "event_id": generate_uuid_v4(),
        "user_id_hash": hash_user_identifier(user_id),  # Never store raw ID
        "event_type": event_type,  # consent_granted, consent_withdrawn, consent_updated
        "purpose": purpose,  # The specific consent category
        "timestamp": get_current_iso_timestamp(),
        "ip_country": get_request_country(),  # Country only, never full IP
        "user_agent_info": get_browser_platform_info(),
        "consent_version": "1.0",
        "additional": additional_data or {}  # No PII allowed here either
    }
    
    # Store in append-only consent audit log
    write_to_audit_trail(audit_entry)

def generate_audit_report(user_id: str, date_range: tuple) -> list:
    """Generate consent audit trail for a user (for Right of Access requests)"""
    entries = query_audit_trail(
        user_hash=hash_user_identifier(user_id),
        start_date=date_range[0],
        end_date=date_range[1]
    )
    return [
        {
            "event_type": e["event_type"],
            "purpose": e["purpose"],
            "timestamp": e["timestamp"],
            "consent_version": e.get("consent_version", "1.0")
        }
        for e in entries
    ]
```

### Consent Record Retention
| Record Type | Retention Period | Reason |
|-------------|------------------|--------|
| Consent decisions (granted/withdrawn) | 3 years | GDPR audit trail requirement |
| Consent presentation versions | Indefinitely | Legal defense |
| Anonymized aggregate analytics | 2 years | Business intelligence |
| Raw audit entries with IDs | 3 years | Compliance audit trail |

## Cookie Consent for Web-Based Skills

### Consent Banner Template (GDPR-compliant)
```
We use cookies to make our services work and to understand how you use them.
By clicking "Accept selected", you consent to the use of cookies in the 
selected categories. You can manage your choices at any time.

Essential cookies (always active): Authentication, security, basic functionality
├── Performance cookies: Analytics, crash reports, performance
└── Marketing cookies: Ads, cross-site tracking, retargeting

[Accept selected] [Reject all] [Manage settings]
```

### Cookie Categories Mapping
| Cookie Type | Purpose | Strictly Necessary? | Consent Required? |
|-------------|---------|---------------------|-------------------|
| Authentication session | Keep users logged in | Yes | No |
| Security tokens | Prevent CSRF, session fixation | Yes | No |
| Load balancer stickiness | Distribute traffic | Yes | No |
| Analytics cookies | Usage statistics | No | Yes (GDPR) |
| Functional preferences | Theme, language settings | No | Yes (GDPR) |
| Advertising cookies | Targeted ads, retargeting | No | Yes (GDPR + CCPA) |

## Common Pitfalls
1. **Pre-checked checkboxes** — GDPR requires explicit opt-in; never default to "on"
2. **Bundled consent** — "Accept all cookies" is not valid; must allow granular choice
3. **No withdrawal path** — withdrawal must be as easy as giving consent
4. **No audit trail** — must prove when/where/how consent was given
5. **CCPA "Do Not Sell" buried** — link must be clearly visible on homepage
6. **Same consent for everything** — GDPR requires separate consent for different purposes
7. **No versioning** — when consent text changes, must re-request consent
8. **Forgetting CCPA** — CCPA applies to California residents regardless of cookie choice
9. **Consent as a wall** — cannot deny service for essential-only consent choice
10. **Treating consent as a one-time event** — must allow ongoing changes

## Verification Checklist
- [ ] Consent categories defined (essential, performance, functional, marketing)
- [ ] Granular consent required for non-essential processing
- [ ] Consent check implemented before each optional data processing operation
- [ ] Consent withdrawal mechanism (as easy as granting consent)
- [ ] Consent audit trail (who, when, what, how recorded for 3 years)
- [ ] CCPA "Do Not Sell My Info" mechanism implemented (if applicable)
- [ ] Cookie consent banner for web-integrated skills (if applicable)
- [ ] Consent preferences page accessible to users
- [ ] Consent record retention policy defined
- [ ] Consent interface tested with real users for clarity