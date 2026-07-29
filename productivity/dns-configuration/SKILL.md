---
name: dns-configuration
description: "Configure DNS records A CNAME MX TXT via API"
---

# DNS Configuration

## Common Records
| Type | Purpose | Example |
|------|---------|---------|
| A | IPv4 address | example.com -> 1.2.3.4 |
| CNAME | Alias | www -> example.com |
| MX | Mail server | @ -> mail.example.com |
| TXT | Verification | SPF, DKIM, domain verify |

## Via API (Cloudflare)
```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE/dns_records" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"A","name":"example.com","content":"1.2.3.4","ttl":120}'
```
