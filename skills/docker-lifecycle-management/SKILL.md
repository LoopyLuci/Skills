---
name: docker-lifecycle-management
description: "Use when managing container/image/volume/network lifecycles."
category: docker
tags: [docker, containers, images, volumes, networks, cli]
---
# Docker Lifecycle Management

Complete reference for Docker container, image, volume, and network operations.

## Container Lifecycle

```powershell
docker create --name myapp nginx:alpine
docker start myapp
docker run --rm -it ubuntu:22.04 bash
docker run -d --name web -p 8080:80 nginx:alpine
docker stop myapp; docker kill myapp
docker restart myapp
docker rm -f myapp; docker container prune

# Inspect
docker ps -a --format '{{.Names}}\t{{.Status}}'
docker inspect myapp | ConvertFrom-Json | Select-Object NetworkSettings
docker logs --tail 100 -f myapp
docker stats --no-stream; docker top myapp
docker cp myapp:/app/logs.txt ./logs/
docker exec -it myapp bash
```

## Image Lifecycle

```powershell
docker build -t myapp:latest .
docker build -t myapp:1.0.0 -f Dockerfile.prod --no-cache .
docker images; docker rmi -f $(docker images -q)
docker tag myapp:latest myrepo/myapp:latest
docker push myrepo/myapp:latest; docker pull nginx:alpine
docker save myapp:latest -o myapp.tar; docker load -i myapp.tar
docker image prune; docker image prune -a
```

## Volume & Network Lifecycle

```powershell
docker volume create app-data
docker run --mount source=app-data,target=/data myapp
docker volume rm app-data; docker volume prune
docker network create --driver bridge mynet
docker run --network mynet --name app2 myapp
docker network connect mynet myapp
docker run -p 8080:80 nginx
docker network prune
```

## Pitfalls

- docker stop sends SIGTERM; docker rm -f sends SIGKILL
- Named volumes persist; anonymous volumes pruned
- Use user-defined bridge networks for DNS by name
