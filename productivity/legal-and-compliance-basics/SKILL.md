---
name: legal-and-compliance-basics
description: "Legal: GDPR, CCPA, FTC, ToS, privacy, consent."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [legal, compliance, gdpr, ccpa, privacy, terms-of-service]
    related_skills: [ecommerce-store-setup, freelance-business-operations, affiliate-marketing]
---

# Legal & Compliance Basics

## Overview
Core legal compliance for websites and online businesses: GDPR, CCPA, CAN-SPAM, FTC endorsement guidelines, cookie consent, DMCA, affiliate disclosure, Terms of Service, Privacy Policy. **⚠️ This is NOT legal advice — always consult an attorney for your specific situation.**

## When to Use
- Determining which regulations apply to your business
- Setting up GDPR-compliant cookie consent
- Drafting Privacy Policy and Terms of Service
- Ensuring CAN-SPAM compliance for email marketing
- Adding FTC-compliant affiliate disclosures
- Implementing DMCA takedown process
- Reviewing ADA/Section 508 accessibility requirements

## Body

### 1. GDPR (EU — General Data Protection Regulation)

**Applies to:** Any business processing data of EU residents, regardless of location.

**Requirements:**
- [ ] Privacy policy explaining what data you collect, why, and retention period
- [ ] Cookie consent banner with granular opt-in (pre-ticked checkboxes are ILLEGAL under GDPR)
- [ ] Right to access: users can request all data you hold
- [ ] Right to deletion: users can request permanent data deletion
- [ ] Data breach notification within 72 hours
- [ ] Data Processing Agreement (DPA) with third-party processors (Google Analytics, Mailchimp, etc.)

**Penalty:** Up to €20M or 4% of global annual revenue (whichever is higher).

### 2. CCPA (California Consumer Privacy Act)

**Applies to:** For-profit businesses with ≥$25M revenue OR data on 50,000+ Californians OR 50%+ revenue from data sales.

**Requirements:**
- [ ] "Do Not Sell My Personal Information" link on homepage
- [ ] Privacy policy with categories of data collected and sold
- [ ] Right to know what data is collected
- [ ] Right to delete
- [ ] Right to opt out of data sale

### 3. CAN-SPAM (US Commercial Email)

**Applies to:** Any commercial email to US recipients.

**Requirements:**
- [ ] Accurate subject line (not misleading)
- [ ] Physical mailing address in EVERY email
- [ ] Clear, working unsubscribe link in EVERY email
- [ ] Honor unsubscribe within 10 business days
- [ ] Identify message as ad if promotional

**Penalty:** Up to $50,120 per violation.

### 4. FTC Endorsement Guidelines

**Applies to:** Anyone receiving compensation (money, free product, affiliate commission) to endorse a product.

**Requirements:**
- [ ] Clear disclosure of material connection
- [ ] Disclosure must be "clear and conspicuous" — NOT hidden in footer or link
- [ ] Images: overlay text, not just in caption
- [ ] Video: spoken disclosure + on-screen text
- [ ] Social: "#ad" or "#sponsored" (NOT just "#collab" or "#partner")

### 5. Cookie Consent

| Solution | Cost | Features |
|----------|------|----------|
| Cookiebot | Free (limited), Paid | Auto-scan, granular consent, multi-language |
| Osano | Paid | Full compliance platform |
| Finsweet Cookie Consent | Free (Webflow) | Lightweight, customizable |
| Custom JS | Free | Build with cookies.js library |

**Implementation:** Scan site for all cookies/scripts → Categorize (necessary, preferences, statistics, marketing) → Implement consent banner with granular toggles → Block non-necessary scripts until consent → Log consent records.

### 6. DMCA (Digital Millennium Copyright Act)

**Safe harbor requirements (US):**
- Designate DMCA agent with Copyright Office
- Publish DMCA takedown policy
- Respond to takedown notices promptly
- Implement repeat infringer policy

### 7. ToS & Privacy Policy Templates

**Privacy Policy sections:**
1. What information we collect (personal + non-personal)
2. How we collect it (forms, cookies, analytics, third parties)
3. Why we collect it (legitimate interest, consent, contract fulfillment)
4. How we store and protect it
5. Who we share it with (processors, legal requirements)
6. Your rights (access, deletion, portability, objection)
7. Cookie policy (types, purpose, duration)
8. Contact information for privacy questions

**Terms of Service sections:**
1. Acceptance of terms
2. Description of service
3. User responsibilities (no misuse, account security)
4. Payment terms (if applicable)
5. Intellectual property rights
6. Limitation of liability
7. Termination clause
8. Dispute resolution / governing law
9. Changes to terms

### 8. ADA / Section 508 Accessibility

**Baseline requirements:**
- Alt text on all images
- Proper heading hierarchy (h1 → h2 → h3)
- Color contrast ratio ≥ 4.5:1 for normal text
- Keyboard-navigable interface
- Captions on video content
- Screen reader compatibility

**Tools:** WAVE (wave.webaim.org) for automated checks, axe DevTools browser extension, manual keyboard testing.

## Common Pitfalls

- **Copying another site's ToS**: Terms are specific to your business. Copying violates copyright and may not protect you.
- **No cookie banner**: GDPR fines issued for implied consent (pre-checked boxes).
- **Forgetting unsubscribe**: CAN-SPAM requires working unsubscribe in EVERY commercial email.
- **Vague affiliate disclosures**: "Some links are affiliate" buried in footer = NOT compliant.
- **Assuming US law only**: If you have international visitors, GDPR applies regardless of your location.
- **Skipping DPA**: Google Analytics, Mailchimp, and most SaaS tools require a signed DPA under GDPR.

## Verification Checklist

- [ ] Privacy policy covers all required sections
- [ ] Terms of Service drafted (NOT copied from another site)
- [ ] Cookie consent banner installed (granular opt-in for GDPR)
- [ ] CAN-SPAM compliance: unsubscribe + physical address in every email
- [ ] FTC disclosure on all affiliate/review content
- [ ] DMCA agent designated (if applicable)
- [ ] "Do Not Sell My Info" link (if subject to CCPA)
- [ ] Data Processing Agreements with third-party tools
- [ ] Accessibility: alt text, heading hierarchy, color contrast checked
- [ ] ⚠️ Disclaimer displayed: "Not legal advice — consult an attorney"