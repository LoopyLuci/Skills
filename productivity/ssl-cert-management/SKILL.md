---
name: ssl-cert-management
description: "Request and renew Let's Encrypt certs with certbot"
---

# SSL Certificate Management

## Certbot
```bash
# Install
sudo apt install certbot python3-certbot-nginx

# Get cert
sudo certbot --nginx -d example.com -d www.example.com

# Test renewal
sudo certbot renew --dry-run

# Auto-renewal (systemd)
sudo systemctl enable certbot.timer
```

## Manual DNS Challenge
```bash
certbot certonly --manual --preferred-challenges dns -d example.com
```
