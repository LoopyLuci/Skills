---
name: banking-api-integration
description: "Use when integrating banking APIs. PSD2, Open Banking."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [banking, fintech, api-integration, open-banking, psd2]
    related_skills: [fintech-payment-systems, fraud-detection-ml]
---

# Banking API Integration

## Overview
Connect applications to banking systems using Open Banking (PSD2), Open Banking UK, FDX, or other regional banking data APIs. Covers OAuth2 authentication, consent flows, account information services (AIS), payment initiation (PIS), and webhook handling for real-time transaction data.

## When to Use
- "Integrate bank account data into my app"
- "Implement PSD2-compliant payment initiation"
- "Handle Open Banking OAuth consent flows"
- "Set up bank transaction webhooks"

## Authentication Flow (OAuth2 + Consent)
```python
import httpx, hmac, hashlib

class BankingAPIClient:
    def __init__(self, client_id, client_secret, base_url):
        self.cid = client_id; self.sep = client_secret
        self.base = base_url

    def get_access_token(self, auth_code):
        r = httpx.post(f"{self.base}/oauth/token", data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "client_id": self.cid,
            "client_secret": self.sep,
            "redirect_uri": os.environ["OAUTH_REDIRECT_URI"]
        })
        return r.json()["access_token"]

    def create_consent(self, token, permissions):
        r = httpx.post("https://api.openbanking.org.uk/aisp/account-requests",
            headers={"Authorization": f"Bearer {token}"}, json={"Permissions": permissions})
        return r.json()["AccountRequestId"]

# Consent flow:
# 1. Redirect user to bank auth page
# 2. Bank returns auth_code → exchange for access_token
# 3. Create consent with specific permissions
# 4. Listen for webhooks on transaction updates
```

## Webhook Handling (Signature Verification Required)
```python
@app.route("/banking/webhook", methods=["POST"])
def handle_webhook():
    sig = request.headers.get("x-signature-sha256")
    expected = hmac.new(os.environ["WEBHOOK_SECRET"].encode(),
        request.data, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(sig, expected):
        return "Unauthorized", 401
    process_banking_event(request.get_json())
    return "OK", 200
```

## Common Pitfalls
1. Consent expiration (90-day renewal required in Open Banking UK)
2. Rate limit exceeded — implement exponential backoff
3. Not handling consent revocation gracefully
4. Currency stored without currency code
5. Duplicate webhook deliveries not deduplicated
6. Not checking transaction data freshness
7. Missing idempotency keys on webhook processing

## Verification Checklist
- [ ] OAuth2 consent flow tested end-to-end
- [ ] Refresh token handling implemented
- [ ] Rate limit backoff logic deployed
- [ ] Webhook signature validation works
- [ ] Consent expiration reminders configured
- [ ] Account type filtering functional
- [ ] Currency codes stored with amounts
- [ ] Webhook deduplication by ID
- [ ] Data freshness checks active
- [ ] Bank API outage handling in place