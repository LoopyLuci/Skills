---
name: reverse-proxy-setup
description: "Configure Nginx Caddy Traefik for SSL and routing"
---

# Reverse Proxy Setup

## Nginx
```nginx
server {
    listen 443 ssl;
    server_name example.com;
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Caddy (Auto SSL)
```caddy
example.com {
    reverse_proxy localhost:8000
}
```

## Traefik (Docker)
```yaml
labels:
  - "traefik.http.routers.myapp.rule=Host(`example.com`)"
  - "traefik.http.services.myapp.loadbalancer.server.port=8000"
```
