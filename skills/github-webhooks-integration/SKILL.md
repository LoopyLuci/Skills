---
name: github-webhooks-integration
description: Set up webhooks, handle events, and build integrations.
---

# GitHub Webhooks Integration

**Trigger**: Use when setting up GitHub webhooks, building integrations, or reacting to GitHub events programmatically.

## Webhook Events

| Event | When it fires | Payload includes |
|-------|--------------|------------------|
| `push` | Git push | commits, ref, before/after SHA |
| `pull_request` | PR opened/closed/sync | PR data, review status |
| `issues` | Issue created/edited/closed | Issue body, labels |
| `issue_comment` | Comment on issue/PR | Comment body, issue ref |
| `release` | Release published | Release data, assets |
| `workflow_run` | Workflow completed | Workflow status, conclusion |
| `star` | Repo starred/unstarred | Action (created/deleted) |
| `create`/`delete` | Branch/tag created/deleted | Ref type, ref name |

## Setting Up a Webhook

### Via API
```bash
gh api repos/:owner/:repo/hooks \
  --method POST \
  --input - << 'EOF'
{
  "name": "web",
  "active": true,
  "events": ["push", "pull_request", "issues"],
  "config": {
    "url": "https://example.com/github-webhook",
    "content_type": "json",
    "secret": "your-webhook-secret"
  }
}
EOF
```

### Via CLI
```bash
gh api repos/:owner/:repo/hooks --method POST \
  -f name=web \
  -f active=true \
  -f events[]=push \
  -f events[]=pull_request \
  -f config[url]=https://example.com/webhook \
  -f config[content_type]=json \
  -f config[secret]=my-secret
```

## Verifying Webhook Signatures

```python
# Python — verify HMAC-SHA256 signature
import hashlib, hmac

def verify_webhook(payload_body: bytes, signature_header: str, secret: str) -> bool:
    """Verify GitHub webhook signature."""
    signature = hmac.new(
        secret.encode(), payload_body, hashlib.sha256
    ).hexdigest()
    expected = f"sha256={signature}"
    return hmac.compare_digest(expected, signature_header)
```

```javascript
// Node.js
const crypto = require('crypto');

function verifyWebhook(payload, signature, secret) {
  const sig = 'sha256=' + crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');
  return crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(signature));
}
```

## Managing Webhooks

```bash
# List hooks
gh api repos/:owner/:repo/hooks --jq '.[].config.url'

# Get a specific hook
gh api repos/:owner/:repo/hooks/123456

# Update hook
gh api repos/:owner/:repo/hooks/123456 \
  --method PATCH \
  -f active=true \
  -f events[]=push

# Delete hook
gh api repos/:owner/:repo/hooks/123456 --method DELETE

# Test ping (sends test event)
gh api repos/:owner/:repo/hooks/123456/tests --method POST

# Recent deliveries
gh api repos/:owner/:repo/hooks/123456/deliveries --jq '.[].guid'
```

## Webhook Handler (FastAPI Example)

```python
from fastapi import FastAPI, Request, HTTPException
import hmac, hashlib

app = FastAPI()
WEBHOOK_SECRET = "your-webhook-secret"

@app.post("/github-webhook")
async def handle_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get("x-hub-signature-256", "")
    
    # Verify signature
    expected = "sha256=" + hmac.new(
        WEBHOOK_SECRET.encode(), payload, hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise HTTPException(403, "Invalid signature")
    
    event = request.headers.get("x-github-event", "push")
    data = await request.json()
    
    if event == "push":
        branch = data["ref"].split("/")[-1]
        print(f"Push to {branch}: {data['head_commit']['message']}")
    elif event == "pull_request":
        action = data["action"]
        print(f"PR {data['pull_request']['number']}: {action}")
    
    return {"status": "ok"}
```

## Re-delivery & Troubleshooting

```bash
# List recent deliveries
gh api repos/:owner/:repo/hooks/123456/deliveries --jq \
  '.[] | {guid, status_code, delivered_at}'

# Get delivery details
gh api repos/:owner/:repo/hooks/123456/deliveries/DELIVERY_GUID

# Re-deliver a failed delivery
gh api repos/:owner/:repo/hooks/123456/deliveries/DELIVERY_GUID/attempts \
  --method POST
```

## Pitfalls
- **Signature verification**: Always verify — without it, anyone can POST to your endpoint
- **Payload size limit**: GitHub caps payloads at 25 MB — larger events are dropped
- **Retry on failure**: GitHub retries 3 times with exponential backoff if endpoint returns 5xx
- **Secret rotation**: Update the secret in both GitHub and your server — use `gh api` to patch
- **Local testing**: Use `smee.io` or `ngrok http 8000` for forwarding webhooks to localhost

## Verification
```bash
# Test ping
gh api repos/:owner/:repo/hooks/123456/tests --method POST

# Check recent deliveries
gh api repos/:owner/:repo/hooks/123456/deliveries --jq '.[0]'
```
