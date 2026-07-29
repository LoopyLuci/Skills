---
name: docker-networking-troubleshoot
description: "Use when debugging Docker network connectivity issues."
category: docker
tags: [docker, networking, troubleshooting]
---
# Docker Networking Troubleshoot

Diagnosing and fixing Docker network issues.

## Diagnostics
```powershell
docker network inspect mynet
docker inspect myapp --format '{{json .NetworkSettings}}' | ConvertFrom-Json
docker exec myapp ping google.com
docker exec myapp nslookup db
docker port myapp
netstat -ano | Select-String ":8080"
```

## DNS Fix
User-defined bridge resolves by name:
```yaml
services:
  app: { networks: [mynet] }
  db: { networks: [mynet] }
networks: { mynet: { driver: bridge } }
```

## Port Conflicts
```powershell
netstat -ano | Select-String ":80"
docker run -p 8080:80 nginx  # different host port
```

## Custom DNS
```yaml
services:
  app:
    dns: [8.8.8.8, 1.1.1.1]
    dns_search: example.com
```

## Pitfalls
- Default bridge has no DNS by name -- use user-defined bridge
- --link is deprecated; use networks
- VPNs break Docker DNS -- set static DNS in daemon.json
