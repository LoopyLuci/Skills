---
name: apexlang-deploy
description: Deploys the application specified in APEXLang to a provided database.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [oracle, apex, apexlang]
    source: oracle/skills
---

Use `scripts/deploy-apex-app.sh <app-directory>` to import an APEX application directory into a database. Set `SQLCL_BIN` to the absolute path of the SQLcl executable and `SQLCL_CONNECTION_STRING` to the SQLcl connection string before running it.