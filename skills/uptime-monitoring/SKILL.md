---
name: uptime-monitoring
description: "Ping endpoints check SSL expiry monitor via Telegram cron"
---

# Uptime Monitoring

## Simple Health Check
```bash
#!/bin/bash
URL="https://example.com"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" $URL)
if [ "$STATUS" != "200" ]; then
    echo "DOWN: $URL returned $STATUS"
fi
```

## SSL Expiry Check
```bash
#!/bin/bash
EXPIRY=$(echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null | openssl x509 -noout -enddate)
echo "SSL: $EXPIRY"
```

## Cron + Telegram
```bash
hermes cron create --schedule "*/5 * * * *" --script scripts/uptime.sh --no-agent --deliver telegram
```
