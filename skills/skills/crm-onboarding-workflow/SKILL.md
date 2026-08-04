---
name: crm-onboarding-workflow
description: "Use when setting up CRM. Data import, team onboarding."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [crm, sales, customer-management, onboarding, data-import]
    related_skills: [real-estate-property-analysis, marketing-strategy-framework]
---

# CRM Onboarding Workflow

## Overview
Systematically set up a CRM (HubSpot, Salesforce, Pipedrive, or ClickUp) for a new team or business: data migration strategy, field mapping, pipeline definition, team onboarding, user permissions, and go-live checklist.

## When to Use
- "Set up a CRM for my team"
- "Import customer data into CRM"
- "I need a sales pipeline defined"
- "Onboard my team to HubSpot"

## CRM Selection Guide

### Tier: Small Business (1-10 users)
| CRM | Price | Best For | Key Limits |
|-----|-------|----------|-----------|
| HubSpot Free | $0 | Startups, solopreneurs | 1,000,000 contacts, 1,000 emails/day |
| Freshsales Free | $0 | Sales teams, simple needs | 10 users, 100MB storage |
| Agile CRM | $8.99/user | All-in-one small biz | 1000 contacts, email + phone |

### Tier: Growth (10-100 users)
| CRM | Price | Best For | Key Limits |
|-----|-------|----------|-----------|
| Pipedrive | $14.90/user | Sales pipeline, deal management | Unlimited deals, no limits on records |
| ActiveCampaign | $21/user | Marketing + Sales automation | 15,000 contacts |
| HubSpot Starter | $45 | Sales + Marketing + Service | 1,000 contacts, limited features |

### Tier: Enterprise (100+ users)
| CRM | Price | Best For | Key Limits |
|-----|-------|----------|-----------|
| Salesforce Essentials | $25/user | Full enterprise features | All Salesforce capabilities |
| Salesforce Unlimited | $300+ | Custom enterprise workflows | Everything + support |
| Monday CRM | $22-25/user | Project-based selling | Unlimited boards, 5GB storage |

## Phase 1: Planning (Week 1)

### 1. Define Your Sales Process
Map your current sales workflow before touching the CRM:
```
Lead Source → Lead Capture → Qualification → Demo/Meet → Proposal → Negotiation → Closed Won/Lost
```

Document:
- Average deal size per stage
- Time spent in each stage
- Common objections by stage
- Key handoff points between team members

### 2. Data Migration Strategy
Inventory all data sources:
| Source | Type | Volume | Quality | Migration |
|--------|------|--------|---------|-----------|
| Excel/CSV | Contacts, deals | 1,200 rows | Low (duplicates) | Clean + Import |
| Email | Lead captures | Ongoing | Good | Auto-sync |
| LinkedIn | Prospects | 500 | Medium | Manual import |
| Previous CRM | All data | 5,000 records | Variable | API export |

**Critical Decision**: Start with clean data or bring everything?
- **Clean data only**: Import only contacts with valid emails and recent activity (last 12 months)
- **Full import**: All historical data, requires deduplication

### 3. Field Mapping Template
Use the `xlsx` tool to design your field mapping:

| Source Field | Target Field | Data Type | Required | Notes |
|-------------|-------------|-----------|----------|-------|
| `Contact Name` | `contact.name` | string | yes | Split into first/last |
| `Email` | `contact.email` | email | yes | Validate format |
| `Phone` | `contact.phone` | phone | no | Standardize to E.164 |
| `Company` | `account.name` | string | yes | Create if new |
| `Job Title` | `contact.title` | string | no | |
| `Source` | `lead.source` | picklist | no | Map to standard values |
| `Lead Status` | `lead.status` | picklist | yes | (new, working, closed) |
| `Last Contact` | `activity.date` | date | no | |

## Phase 2: Setup (Week 2)

### 1. Pipeline Configuration
Create deal stages with probability and quota:

| Stage | Probability | Quota % | Description |
|-------|-------------|---------|-------------|
| Qualify to Buy | 10% | 0 | Initial interest confirmed |
| Meeting Scheduled | 20% | 0 | Demo or call booked |
| Demo Given | 35% | 0 | Product shown, questions answered |
| Proposal Sent | 55% | 0 | Custom quote sent |
| Negotiation | 75% | 0 | Back-and-forth on terms |
| Contract Sent | 90% | 0 | Final agreement for e-signature |
| Closed Won | 100% | 100 | Payment received |
| Closed Lost | 0% | 0 | Lost to competitor/price/no fit |

### 2. Team Onboarding
Each user gets:
- Login credentials (set up by admin)
- Role-based access level (see Permissions matrix below)
- 30-min platform walkthrough
- Assigned territory/segments
- Test record in each pipeline stage (practice only)

### 3. Automation Rules
Set up 3 essential automations for day one:

**Automation 1: New Lead Assignment**
- Trigger: New lead created
- Action: Assign to sales rep (round-robin)
- Action: Send notification email to rep

**Automation 2: Deal Stage Alerts**
- Trigger: Deal stage change to "Demo Given" or later
- Action: Notify sales manager
- Action: Add to weekly forecast report

**Automation 3: Stale Lead Reminder**
- Trigger: Lead not contacted within 2 hours
- Action: Send reminder to assigned rep
- Action: Escalate to manager after 24 hours

### 4. Email Templates
Pre-build these templates so reps can send immediately:
1. **Initial outreach** (from lead assignment workflow)
2. **Meeting follow-up** (with calendar link and deck)
3. **Proposal delivery** (with pricing tiers)
4. **Win announcement** (internal: notify ops, sales ops, success)
5. **Loss follow-up** (with feedback request)

## Phase 3: Go-Live (Week 3)

### 1. Permissions Matrix
| Role | Records Access | Features |
|------|----------------|----------|
| Sales Rep | Own + team leads | Create/edit deals, contacts, activities |
| Sales Manager | All team + own | Forecasting, reports, team management |
| Operations | All records | Import/export, field management, workflows |
| Admin | Everything | User management, billing, integrations |
| Read-Only | Assigned accounts | Viewing only |

### 2. Reporting Dashboard
Set up the 4 essential dashboards everyone needs:
- **Pipeline Health**: Deals by stage, weighted pipeline value
- **Activity Volume**: Calls, emails, meetings booked (per rep)
- **Conversion Rates**: Lead→MQL→SQL→Win rates
- **Forecast**: Projected revenue by quarter (weighted deals)

### 3. Integration Checklist
- [ ] Email syncing (Gmail/Office 365) — sync sent/received emails as activities
- [ ] Calendar sync — meetings appear in CRM, auto-log
- [ ] Phone system (if using) — log calls automatically with recordings
- [ ] Email marketing tool (Mailchimp, HubSpot, ActiveCampaign)
- [ ] Website forms → CRM lead capture
- [ ] Payment processor → deal won trigger

## Common Pitfalls

1. **Data migration chaos** — importing everything including duplicates, invalid emails, and outdated records. Clean first, migrate second.

2. **Over-configuration** — building every possible field and view upfront. Start minimal (5-7 key fields) and expand based on usage patterns.

3. **Skipping user training** — reps won't use the CRM if they don't know how. Schedule 1-on-1 walkthroughs for each user.

4. **No ownership of cleanup** — without an admin, the CRM becomes a data graveyard. Assign a CRM admin (rotates monthly).

5. **Wrong access levels** — giving everyone full access to everything creates privacy risk and data chaos. Use territory/role-based access.

6. **Too many pipelines** — one pipeline with clear stages. Multiple pipelines confuse reporting and forecasting.

7. **No data hygiene rules** — without clear rules for required fields, data quality degrades rapidly. Make email required on all contacts.

## Verification Checklist

- [ ] Sales process documented (5-7 stages with clear definitions)
- [ ] Data sources inventoried (3-5 sources mapped)
- [ ] Field mapping completed (core fields + custom fields)
- [ ] Pipeline configured with stages, probabilities, quotas
- [ ] 3 automations set up (lead assignment, stage alerts, stale reminders)
- [ ] Email templates pre-built (5 core templates)
- [ ] User roles defined with permissions matrix
- [ ] 4 reporting dashboards configured
- [ ] 5 core integrations verified
- [ ] CRM admin assigned with monthly cleanup schedule