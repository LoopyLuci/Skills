---
name: hermes-gateway-messaging-operations
description: "Use when the Hermes gateway or a messaging platform is down."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [hermes, gateway, messaging, telegram, discord, slack, env, credentials, windows]
    related_skills: [hermes-agent]
---

# Hermes gateway & messaging-platform operations

Bringing a messaging surface up is a diagnosis task, not a config-writing task: the
credential is usually present and merely disabled. Prove the channel end-to-end
before declaring success — a connected poller that cannot deliver is still broken.

`hermes-agent` (bundled) covers the feature surface. This skill covers the
operational procedure on this host.

## When to Use

- `hermes gateway status` reports no process, or a previous unclean exit.
- `logs/gateway.log` says `No messaging platforms enabled.`
- A platform (Telegram, Discord, Slack, Signal, WhatsApp) is not receiving
  replies, or `Channel directory built: 0 target(s)`.
- A platform credential in `.env` must be enabled, replaced, or added.
- The gateway dies repeatedly and the Windows login item needs checking.

Not for choosing which platform to use or writing platform adapters — that is
the bundled `hermes-agent` skill's territory.

## Order of work

1. **Read the three state sources before touching anything.** They answer
   "is it running", "what did it think", and "what did it do":
   ```bash
   hermes gateway status                      # process + login item
   tail -40 "$HERMES_HOME/logs/gateway.log"   # per-platform connect lines
   cat "$HERMES_HOME/gateway_state.json"      # pid, state, per-platform error_code
   ```
   Note `HERMES_HOME` here is `C:/Users/Server/AppData/Local/hermes`, not `~/.hermes`.
   Resolve it from the environment or the `hermes --version` install line; never
   hardcode `~/.hermes` on this host.

2. **Diagnose from the log line, not from config.** The decisive strings:
   - `No messaging platforms enabled.` → no platform has an active token.
   - `✓ telegram connected` / `Connected to X (polling mode)` → platform is up.
   - `Channel directory built: 0 target(s)` → connected but no authorized users,
     so every inbound is unauthorized and no cron delivery target exists.
   - `polling confirmed healthy: getUpdates progressing (generation N)` → the
     poller is genuinely advancing, not wedged on a stale connection.

3. **Only then edit credentials** — see the .env rules below, which are the
   highest-risk step in this workflow.

4. **Restart and re-verify from the log, not from the exit code.**
   `hermes gateway start` printing `✓ Gateway started (PID: N)` proves only that
   a process spawned. The platform connects asynchronously ~20-40s later.

5. **Prove delivery with a real API call**, not by inspecting state. See
   `references/platform-verification.md`.

## Reading state.db without hurting the gateway

`state.db` grows fast (hundreds of MB here) and the gateway is writing to it
continuously. Any tool that inspects it must open it read-only:

```python
conn = sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True, timeout=5)
```

Three traps specific to this store:

- **`PRAGMA quick_check` is a full scan — seconds, not milliseconds.** On a 500 MB
  store it measured ~5s. Never call it from a UI thread, a timer tick, or an
  interactive probe path; run it on a worker or on demand only. `count(*)` on
  `messages` is ~7ms by contrast, so measure before assuming a query is cheap.
- **Use the FTS index for message search, not `LIKE`.** `messages_fts` exists
  alongside `messages`; `MATCH` + `bm25()` measured ~10ms where `LIKE '%term%'`
  took ~420ms and matched fewer rows. Quote each user token (`"a" AND "b"`) so
  FTS operators in the input (`"`, `-`, `*`, `(`) cannot raise a syntax error,
  and fall back to `LIKE` on `sqlite3.Error`.
- **Filter superseded rows.** `messages.active = 0` and `messages.compacted = 1`
  mark content that context compaction replaced. Querying without those filters
  returns the same turn twice and shows blanks; both flags are large here
  (~90k inactive, ~73k compacted).

Other tables worth knowing for triage: `sessions` (per-session token/tool
counters, `end_reason`, `estimated_cost_usd`), `session_model_usage` (per-model
token totals), `delivery_obligations` (outbound queue with `state`/`attempts`),
`async_delegations` (background sub-agents), `gateway_heartbeats`.

`cron/jobs.json` stores `schedule` as a **nested dict** (`{"kind": "interval",
"minutes": 30, "display": "every 30m"}`), so `str(job["schedule"])` prints a
Python repr. Read `.display`, fall back to deriving from `kind`+`minutes`, and
show `state` / `last_status` / `failure_streak` / `next_run_at` alongside it.

## Not every timestamp in gateway_state.json is an epoch time

`gateway_state.json` mixes clock domains in one small file, and the mismatched
ones fail silently rather than raising:

- `start_time` is a **monotonic** clock, not epoch seconds. Subtracting it from
  `time.time()` yields a negative delta, so any uptime display becomes a large
  negative duration instead of an error. Derive real uptime from the OS process
  instead (`psutil.Process(pid).create_time()`, or `wmic`/`Get-Process` on
  Windows); `tasklist` has no start-time column, so it cannot substitute.
- `platforms.<name>.updated_at` is an ISO-8601 **string** with a UTC offset,
  while `sessions.started_at` and `gateway_heartbeats.last_heartbeat` in
  `state.db` are epoch **seconds**.

Normalise through one guarded helper that rejects values outside a plausible
epoch window (2001-09-09 to 2286-11-20) rather than formatting them. Rendering
`1.79e11` as a date silently yields a date ~55,000 years off, which looks like
a data bug rather than a clock bug. When a duration field is monotonic, show an
explicit dash instead of a fabricated number.

## Credentials live in .env — editing it is the dangerous step

`$HERMES_HOME/.env` is the credential store for every provider and platform.
It is deliberately unreadable through the normal file tools:

- `read_file` (and `read_file` inside `execute_code`) refuses it with
  "is a Hermes credential store and cannot be read directly". The `terminal`
  tool can still read it. This is expected, not a fault to work around loudly.

**Never rewrite the whole file from a parsed copy.** Read it as lines *with*
endings, mutate the single line, and write the exact same line list back:

```python
s = open(path, encoding='utf-8').read().splitlines(True)   # keepends=True
out = []
for line in s:
    if line.startswith('#TELEGRAM_BOT_TOKEN='):            # exact-prefix match
        line = 'TELEGRAM_BOT_TOKEN=' + line.split('=', 1)[1]
    out.append(line)
open(path, 'w', encoding='utf-8').writelines(out)
```

Pitfalls that corrupt the file, all of which leave it looking plausible:

- `rstrip('\n')` on every line while re-adding `'\n'` only on the lines you
  changed collapses the rest of the file into one enormous line. Every key
  except the edited ones stops parsing, and the gateway comes up with no
  providers at all. Match with an exact `startswith` prefix, never a substring
  test — a substring match on `TELEGRAM_BOT_TOKEN` also rewrites
  `TELEGRAM_CRON_THREAD_ID` style neighbours.
- `split()` / `'=' in line` / a substring search across a joined blob will match
  the wrong key or run a value into the next line. Split on `('=', 1)` and only
  index the value.
- Check the line endings the file actually uses before writing
  (`open(path,'rb').read().count(b'\r\n')`); writing LF into a CRLF file
  rewrites every line.

**Recovery is cheap if you never destroyed line structure.** If the file has
been collapsed, the sibling backups (`$HERMES_HOME/.env.bak.*`) are intact.
Restore from the newest backup, then verify nothing else was lost by diffing
line-by-line and confirming the key sets match — expect only the intentional
edits to differ:

```python
new = open('.env', encoding='utf-8').read().splitlines()
bak = open('.env.bak.<stamp>', encoding='utf-8').read().splitlines()
assert len(new) == len(bak)
print([(a, b) for a, b in zip(new, bak) if a != b])   # should be only your edits
```

That diff is the only acceptable evidence that credentials are intact. Say so
in the report rather than quietly proceeding.

**A backup can be too old, and a key-set diff will not catch it.** The newest
`.env.bak.*` may predate a credential rotation, so restoring it hands back a
revoked key under a correct-looking name — the key sets match, so the
line-by-line diff above passes while the gateway silently loses that provider.
Before restoring, harvest every `KEY=value` pair from the collapsed file and
diff the *values*, not just the key names, then re-apply any value that differs
from the backup:

```python
def kv(text):
    out = {}
    for m in re.finditer(r'([A-Za-z_][A-Za-z0-9_]*)=([^\n]*)', text):
        out.setdefault(m.group(1), m.group(2))
    return out

collapsed = kv(open('.env.broken', encoding='utf-8').read())
backup = kv(open(bak, encoding='utf-8').read())
print({k: v for k, v in collapsed.items() if backup.get(k) != v})   # rotate these back in
```

Save a copy of the collapsed file under a distinct name before restoring. If a
recovered value is empty or comment-like (the collapse swallowed it), the
credential is unrecoverable from the file and must be reissued — say that
plainly rather than shipping a half-restored `.env`.

## A disabled token usually has a comment explaining who took it

A commented-out platform token is deliberate, and the comment names the other
consumer. Before re-enabling it, confirm that consumer is gone — two processes
polling one bot token fight over `getUpdates` and starve each other:

```bash
grep -n 'PLATFORM_BOT_TOKEN\|_TOKEN' "$HERMES_HOME/.env" | head
ls -d <path-named-in-the-comment>          # does the other poller still exist?
```

If the other project still exists, do not enable the token here — coordinate or
move the credential instead. Report the conflict instead of silently winning it.

## Allowlist values must be bare

Trailing inline comments in a value line (`KEY=123   # note`) are only stripped
if the loader does it; do not rely on that for an allowlist, because a parsed
value of `123   # note` silently authorizes nobody. Strip the comment yourself
when normalizing, or put the note on its own comment line above the key.

## Always-on rules

- Report the incident plainly, including any file you damaged and how you
  restored it. This user's standing expectation is honest evidence over a clean
  summary; a silent self-inflicted regression is the worst possible outcome.
- Prefer the real API probe for proof. State files can be stale — a
  `platforms.telegram.state: "connected"` entry can carry an `updated_at`
  timestamp from weeks earlier while the process is long dead, because it is
  written by a separate writer process.
- Long polling is the default transport. That is correct for a desktop; if the
  user needs the bot up while the machine is off, say so explicitly rather than
  implying the gateway covers it.
