# Cron-Based Autonomous Watcher Pattern

A generalizable pattern for running a background monitor on a Hermes cron schedule that autonomously handles a domain and reports results back to the chat. Silent when there's nothing to do; produces a report only when action was taken.

## Architecture

```
Hermes Cron Scheduler (every 6h)
        │
        ▼
  watcher_script.py  (no_agent=True — watchdog mode)
        │
        ├── 1. Check domain health (audit, coverage, metrics)
        ├── 2. If action needed → take it (create, fix, update)
        ├── 3. If no action → exit silently (empty stdout)
        └── 4. If action taken → print report to stdout
                │
                ▼
        Delivered back to origin chat
```

## Key Design Decisions

### Why no_agent=True?
The script runs deterministically without LLM overhead. The cron scheduler runs the script directly, captures stdout, and delivers it verbatim. If the script produces no stdout, nothing is delivered — the watcher is silent when healthy.

### Silent-on-healthy pattern
```python
def main():
    if all_healthy():
        return  # No output → no delivery → no noise
    print(f"🤖 **Report**\n...")  # Only prints when action taken
```

### Cron Configuration
```bash
cronjob(action='create', name='My Watcher', schedule='every 6h',
        script='watcher.py', no_agent=True, deliver='origin')
```

### Report Format
When action is taken, output a markdown report:
```
🤖 **Watcher Report**
━━━━━━━━━━━━━━━━━━━━━
**Domain:** kubernetes
**Action:** 5 skills created
**Status:** 12 gaps remaining
**Total inventory:** 1,038 skills
_Next check in 6 hours._
```

## When to Use This Pattern

- Monitoring ecosystem health (skill gaps, package updates, security CVEs)
- Scheduled maintenance tasks (cleanup, deduplication, reindexing)
- Data collection agents that only report when thresholds are breached
- Any autonomous process that should be silent when things are fine

## Implementation Template

```python
#!/usr/bin/env python3
"""watcher.py — Silent-until-action background monitor."""

def check_health() -> dict:
    """Return domain health metrics. Used to decide if action needed."""
    ...

def take_action() -> int:
    """Perform the maintenance/creation action. Return count of items affected."""
    ...

def main():
    health = check_health()
    if health["status"] == "healthy":
        return  # Silent exit — nothing to report
    
    count = take_action()
    print(f"🤖 **Watcher Report**")
    print(f"━━━━━━━━━━━━━━━━━━━━━")
    print(f"**Domain:** {health['domain']}")
    print(f"**Action:** {count} items processed")
    print(f"**Status:** {health['remaining']} remaining")

if __name__ == "__main__":
    main()
```

## Pitfalls

- **no_agent=True is REQUIRED** for the silent-on-healthy pattern
- **deliver='origin'** sends back to the current chat
- **Script in ~/.hermes/scripts/** — cron job requires relative path
- **Empty stdout = silent** — the cron scheduler only delivers non-empty stdout
- **Non-zero exit** sends an error alert — use try/except
- **Test with cronjob(action='run', job_id='...')** before scheduled run
