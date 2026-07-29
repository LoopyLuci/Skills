---
name: docker-volume-backup-restore
description: "Use when backing up or restoring Docker volumes."
category: docker
tags: [docker, volumes, backup, restore, data]
---

# Docker Volume Backup & Restore

Backing up and restoring Docker named volumes.

## Backup

```powershell
docker run --rm -v myvolume:/source -v C:\backups:/backup alpine `
    tar czf /backup/myvolume.tar.gz -C /source .
```

## Restore

```powershell
docker run --rm -v myvolume:/target -v C:\backups:/backup alpine `
    tar xzf /backup/myvolume.tar.gz -C /target
```

## Backup All

```powershell
$dir = "C:\backups\docker-volumes"
New-Item -ItemType Directory -Path $dir -Force
foreach ($vol in (docker volume ls -q)) {
    docker run --rm -v ${vol}:/source -v ${dir}:/backup alpine `
        tar czf "/backup/${vol}.tar.gz" -C /source .
}
```

## Cloud

```powershell
docker run --rm -v myvolume:/source alpine tar czf - -C /source . |
    aws s3 cp - s3://bucket/myvolume-$(date +%F).tar.gz
```

## Pitfalls

- **Stop container** before backup for consistency
- **Named volumes** only — anonymous can't be targeted
- **Databases** — use pg_dump/mysqldump, not file-level backup
