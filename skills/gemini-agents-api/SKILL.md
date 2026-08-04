---
name: gemini-agents-api
description: Use when programmatically managing custom Agent resources on Gemini Enterprise Agent Platform.
tags: [gemini, agents, api, google-cloud, vertex-ai, ai-platform]
related_skills: [gemini-api, gemini-interactions-api, google-cloud-recipe-auth]
---

# Gemini Enterprise Agent Platform — Managed Agents API

Provides REST endpoints and JSON payload structures to programmatically manage custom Agent resources on the Gemini Enterprise Agent Platform.

## Authentication

```bash
export PROJECT_ID="your-project-id"
export LOCATION="global"
export ACCESS_TOKEN=$(gcloud auth print-access-token)
```

## Endpoint

```
https://aiplatform.googleapis.com/v1beta1/projects/{PROJECT_ID}/locations/{LOCATION}/agents
```

## Code Example: Create Agent

```bash
curl -X POST "https://aiplatform.googleapis.com/v1beta1/projects/${PROJECT_ID}/locations/global/agents" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "my-custom-agent",
    "base_agent": "antigravity-preview-05-2026",
    "description": "A custom support agent.",
    "system_instruction": "You are a helpful assistant.",
    "tools": [
      {"type": "code_execution"},
      {"type": "google_search"}
    ]
  }'
```

## CRUD Operations

- **Create**: POST — Long-Running Operation (poll with operation name)
- **Get**: GET `/agents/{AGENT_ID}`
- **List**: GET `/agents`
- **Update**: PATCH with `update_mask` query parameter
- **Delete**: DELETE `/agents/{AGENT_ID}`

## Common Pitfalls

- **Update mask required**: Always include `update_mask` when patching agents
- **Location support**: Not all regions support the Managed Agents API — verify regional availability
- **LRO polling**: Agent creation is async — poll the returned operation URL until `done: true`

## Verification Checklist

- [ ] Cloud SDK authenticated: `gcloud auth print-access-token`
- [ ] Agent created and `done: true` from LRO
- [ ] Agent can be retrieved with GET
- [ ] Agent responds to interactions via `gemini-interactions-api`
