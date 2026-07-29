---
name: docker-swarm-orchestration
description: "Use when deploying/managing Docker Swarm services."
category: docker
tags: [docker, swarm, orchestration, cluster, service]
---
# Docker Swarm Orchestration

Deploying and managing Docker Swarm services and clusters.

## Initialize a Swarm

```powershell
# Manager node
docker swarm init --advertise-addr 192.168.1.10

# Get join token for workers
docker swarm join-token worker
docker swarm join-token manager

# Worker joins
docker swarm join --token SWMTKN-1-... 192.168.1.10:2377
```

## Node Management

```powershell
docker node ls
docker node inspect self
docker node promote node2
docker node demote node2
docker node update --availability drain node2
docker node update --label-add storage=ssd node3
```

## Service Lifecycle

```powershell
# Create service
docker service create --name web --replicas 3 -p 80:80 nginx:alpine

# With constraints and resources
docker service create --name api --replicas 5 \
    --constraint 'node.role == worker' \
    --limit-cpu 0.5 --limit-memory 512M \
    --env DB_HOST=db \
    --network my-overlay \
    --with-registry-auth \
    myregistry.com/api:latest

# Update
docker service update --image nginx:1.25 --rollback web
docker service update --replicas 10 web
docker service update --force web  # force re-deploy

# Rollback
docker service rollback web

# Scale
docker service scale web=5 api=10

# Remove
docker service rm web
```

## Stack Deploy (Compose → Swarm)

```yaml
# docker-stack.yml
version: "3.9"
services:
  web:
    image: nginx:alpine
    deploy:
      replicas: 3
      update_config:
        parallelism: 2
        delay: 10s
        order: start-first
      restart_policy:
        condition: on-failure
      placement:
        constraints: [node.role == worker]
      resources:
        limits: { cpus: "0.5", memory: 512M }
    ports: ["80:80"]
    networks: [frontend]
  api:
    image: myapi:latest
    deploy:
      replicas: 5
      resources:
        reservations: { cpus: "0.25", memory: 256M }
    networks: [frontend, backend]
  db:
    image: postgres:16-alpine
    deploy:
      mode: replicated
      replicas: 1
      placement:
        constraints: [node.labels.storage == ssd]
    volumes: ["pgdata:/var/lib/postgresql/data"]
    networks: [backend]
networks:
  frontend: { driver: overlay }
  backend: { driver: overlay, internal: true }
volumes:
  pgdata: { driver: local }
```

```powershell
# Deploy stack
docker stack deploy -c docker-stack.yml myapp

# List stacks
docker stack ls

# List services in stack
docker stack services myapp

# List tasks (containers) in stack
docker stack ps myapp

# Remove stack
docker stack rm myapp
```

## Secrets and Configs

```powershell
# Secrets (stored encrypted, only in Swarm)
echo "MySecretPassword" | docker secret create db_password -
docker service create --secret db_password postgres:16-alpine

# Configs (unencrypted, mounted as files)
docker config create nginx.conf ./nginx.conf
docker service create --config src=nginx.conf,target=/etc/nginx/nginx.conf nginx
```

## Rolling Updates

```powershell
# Update with parallelism and delay
docker service update --image myapp:2.0.0 \
    --update-parallelism 2 \
    --update-delay 30s \
    --update-order start-first \
    --update-monitor 60s \
    --update-failure-action rollback \
    web
```

## Pitfalls

- Swarm mode is NOT compatible with `docker compose up` (use `docker stack deploy`)
- Overlay networks need ports open (7946 TCP/UDP, 4789 UDP)
- Secrets are only available to Swarm services, not standalone containers
- Volume drivers must exist on all nodes
- `docker stack rm` does NOT remove named volumes
