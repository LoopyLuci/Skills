---
name: ai-agent-integration-workflow
description: "AI agents: use cases, deployment, analytics."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ai, agents, chatbot, integration, automation]
    related_skills: [workflow-automation-skill, community-building, ecommerce-store-setup]
---

# AI Agent Integration Workflow

## Overview
Design and deploy AI agents into websites, apps, and communication platforms. Covers use case identification, platform selection, conversation design (flow, persona, fallback), knowledge base setup, deployment options (embed widget, API, webhook, Slack/Discord bot), analytics and improvement loop, and cost estimation.

## When to Use
- Adding an AI chatbot to a website
- Creating a customer support AI agent
- Integrating an AI assistant into an app
- Building a Slack/Discord bot with AI capabilities
- Estimating cost and analyzing ROI for an AI agent

## Body

### 1. Use Case Identification

| Use Case | Description | Best Platform |
|----------|-------------|---------------|
| Customer support | Answer FAQs, triage tickets, escalate | Website widget + helpdesk |
| Lead qualification | Pre-screen visitors, book demos | Widget + CRM integration |
| User onboarding | Guide new users through setup | In-app assistant, email |
| Content assistant | Help users find content | Search + AI, Slack bot |
| Internal tool | Employee HR/IT support, knowledge retrieval | Slack/Teams bot |
| Ecommerce | Product recommendations, order status | Widget + Shopify/API |

### 2. Conversation Design

**Persona definition:**
- **Name**: [Assistant name]
- **Role**: Support agent / guide / sales assistant
- **Tone**: Professional, friendly, concise, or casual
- **Knowledge scope**: What it knows and doesn't know
- **Limits**: "I can help with account issues but can't process refunds"

**Intent flow:**
```
User message → Classify intent
  ├── FAQ → Answer from knowledge base
  ├── Support → Collect info → Create ticket → Confirm
  ├── Lead gen → Qualify → Book calendar → Confirm
  ├── Off-topic → Acknowledge limit → Redirect options
  └── Escalate → Handoff to human agent with full context
```

**Fallback handling (3 attempts):**
1. "I'm not sure I understand. Could you rephrase that?"
2. "Let me connect you with someone who can help." → Escalate
3. "Here are topics I can help with: [list]"

**Feedback loop:** "Was this helpful? 👍👎" → Analyze No responses → Update knowledge base → Redeploy.

### 3. Knowledge Base Setup

**Sources to include:** Website pages (FAQ, docs, pricing, about), product documentation, support tickets (anonymized), internal wikis/runbooks, policy documents.

**Formatting best practices:**
- Break into Q&A pairs for FAQ-style responses
- Keep each answer under 200 words
- Include "learn more" links
- Tag with categories and intent labels
- Update quarterly with new features and common issues

### 4. Deployment Options

**Website embed widget:**
- Add `<script>` tag to site header
- Customize: colors, position, greeting, proactive triggers
- Platforms: Tidio, Crisp, Intercom, or custom React/Vue component

**API integration:**
- REST or WebSocket endpoints
- POST user message → receive AI response
- Session tracking via conversation_id for context
- Rate limiting for burst handling

**Slack/Discord bot:**
- Slash commands (`/ask [question]`)
- Channel-based Q&A
- DM for private conversations
- SDKs: Bolt (Slack), discord.py (Discord)

### 5. Analytics & Improvement

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| Resolution rate | % resolved without handoff | >70% |
| CSAT | User satisfaction (1–5) | >4.0 |
| Avg conversation length | Messages per conversation | 3–6 |
| Handoff rate | % escalated to human | <30% |
| Response time | Time to first response | <5s |

**Improvement loop:** Collect fallback conversations → Analyze patterns → Update knowledge base → Deploy → Measure.

### 6. Cost Estimation

| Component | Small Scale | Medium Scale |
|-----------|-------------|-------------|
| LLM API (per 1K conversations) | $5–50/mo (GPT-4o mini) | $50–500/mo (GPT-4o) |
| Embedding storage | $0–20/mo | $20–100/mo |
| Hosting (widget/API) | $0–50/mo | $50–200/mo |
| Platform subscription | $0–200/mo | $200–500/mo |
| **Total** | **$10–100/mo** | **$100–500/mo** |

## Common Pitfalls

- **No clear scope**: AI that tries to do everything does nothing well. Define boundaries.
- **Bad knowledge base**: Garbage in, garbage out. Clean structured content is essential.
- **No human handoff**: Users need a path to a human when AI fails.
- **No feedback loop**: Without measurement, quality degrades over time.
- **Ignoring latency**: Responses over 5s feel broken. Optimize prompt size and model choice.
- **No rate limiting**: Burst traffic can spike costs exponentially.

## Verification Checklist

- [ ] Use case defined (support/lead gen/onboarding/internal)
- [ ] Persona documented (name, role, tone, scope, limits)
- [ ] Conversation flow designed (intent → response → fallback → escalate)
- [ ] Knowledge base built from 3+ sources
- [ ] Deployment method selected (widget/API/bot)
- [ ] Analytics tracking configured (resolution rate, CSAT, handoff rate)
- [ ] Cost estimation calculated for current scale
- [ ] Human handoff process defined
- [ ] Feedback loop implemented (was this helpful? → improve)