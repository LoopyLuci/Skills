---
name: database-backup-strategies
description: "Automated backup and restore for PostgreSQL MySQL SQLite"
---

# Database Backup Strategies

## PostgreSQL
```bash
pg_dump -Fc mydb > mydb.dump
pg_restore -d mydb mydb.dump
```

## MySQL
```bash
mysqldump -u root mydb > mydb.sql
mysql -u root mydb < mydb.sql
```

## SQLite
```bash
sqlite3 mydb.db ".backup mydb.backup"
sqlite3 mydb.db ".restore mydb.backup"
```

## Automated (Cron)
```bash
0 2 * * * pg_dump -Fc mydb > /backups/mydb_$(date +%Y%m%d).dump
# Keep 7 days, remove older
0 4 * * * find /backups -name "*.dump" -mtime +7 -delete
```
