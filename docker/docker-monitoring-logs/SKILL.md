---
name: docker-monitoring-logs
description: "Use when monitoring containers and aggregating logs."
category: docker
tags: [docker, monitoring, logs, metrics]
---
# Docker Monitoring & Logs

Monitoring containers and collecting logs.

## Live Monitoring
```powershell
docker stats                    # live CPU/memory/IO
docker stats --no-stream        # single snapshot
docker top myapp                # processes inside
docker events --since 5m        # events in last 5 min
```

## Logs
```powershell
docker logs --tail 100 -f myapp
docker logs --since 2024-01-01 myapp
docker logs myapp 2>&1 > out.txt
```

## Log Drivers
```yaml
x-logging: &log
  driver: "json-file"
  options: { max-size: "10m", max-file: "3" }
```

## Prometheus
```yaml
services:
  prometheus: { image: prom/prometheus, ports: ["9090:9090"] }
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    volumes: [/:/rootfs:ro, /var/run:/var/run:ro]
    ports: ["8080:8080"]
```

## Aggregation
```powershell
foreach ($id in (docker ps -q)) {
    $name = docker inspect --format '{{.Name}}' $id
    docker logs $id > "logs_$name.txt" 2>&1
}
```

## Pitfalls
- json-file driver fills disk -- always set max-size/max-file
- docker logs only works with json-file or journald drivers
- docker events doesn't persist across restarts
