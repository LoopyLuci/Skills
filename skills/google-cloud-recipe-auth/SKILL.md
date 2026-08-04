---
name: google-cloud-recipe-auth
description: Use when authenticating and authorizing to Google Cloud services and APIs.
tags: [google-cloud, authentication, iam, service-accounts, security, adc]
related_skills: [gke-productionize, gemini-api, firebase-basics]
---

# Authenticating to Google Cloud

Authentication is the process of proving who you are. Google Cloud supports multiple identity types and authentication methods for different scenarios.

## Clarifying Questions

Before providing a solution, determine:
1. **Who/what is authenticating?** (Human developer, local script, or production app?)
2. **Where is the code running?** (Local laptop, Compute Engine, GKE, Cloud Run, or external cloud?)
3. **What is the target?** (Google Cloud API or custom application?)
4. **Are you using a client library?** (Libraries handle ADC automatically)

## Human Authentication

```bash
# CLI authentication
gcloud auth login

# Local development (Application Default Credentials)
gcloud auth application-default login
```

## Service-to-Service Authentication

```bash
# Attach a custom service account (GKE example)
# 1. Create service account
gcloud iam service-accounts create my-app-sa --project=PROJECT_ID

# 2. Grant permissions
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:my-app-sa@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"

# 3. Use Workload Identity on GKE  
kubectl annotate serviceaccount APP_SA \
  iam.gke.io/gcp-service-account=my-app-sa@PROJECT_ID.iam.gserviceaccount.com
```

## Code Example: Using ADC (Python)

```python
from google.cloud import storage

# ADC automatically finds credentials
client = storage.Client()

# List buckets
buckets = list(client.list_buckets())
```

## Common Pitfalls

- **Service account keys**: Avoid downloading JSON keys — use impersonation or Workload Identity instead
- **Default service account**: Create custom service accounts rather than using the Compute Engine default
- **Access scopes**: Legacy VMs still use access scopes — check these if attached SA fails
- **API keys**: Restrict to specific APIs and projects; store in Secret Manager

## Verification Checklist

- [ ] Identity type determined (human vs service)
- [ ] auth method matches execution environment
- [ ] Least-privilege IAM roles applied
- [ ] No service account keys committed to code
- [ ] ADC configured for local development
