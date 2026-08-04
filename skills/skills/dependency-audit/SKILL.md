---
name: dependency-audit
description: "Audit Python deps for vulnerabilities updates and licenses"
---

# Dependency Audit

## Check for Vulnerabilities

```bash
# pip-audit
pip install pip-audit
pip-audit

# Safety
pip install safety
safety check

# pip freeze comparison
pip freeze | safety check --stdin
```

## Check for Outdated Packages

```bash
pip list --outdated

# pip-upgrader
pip install pip-upgrader
pip-upgrade
```

## License Checking

```bash
pip install pip-licenses
pip-licenses
pip-licenses --summary
pip-licenses --allow-only "MIT;Apache-2.0"
```

## requirements.txt Hygiene

```bash
# Generate from installed
pip freeze > requirements.txt

# Generate with hashes (secure)
pip freeze --require-hashes > requirements.txt

# Compile from setup.cfg/pyproject.toml
pip install pip-tools
pip-compile pyproject.toml
```

## Automated Audit (Cron)

```bash
hermes cron create \
  --schedule "0 9 * * 1" \
  --script "scripts/dep-audit.sh" \
  --no-agent \
  --deliver telegram
```

Script outputs only when issues found (empty = silent).
