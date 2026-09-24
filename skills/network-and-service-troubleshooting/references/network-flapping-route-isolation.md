# Network Flapping: Route-Isolation Diagnosis

## Pattern

When a bot/network service "works, then stops working right after" with errors like
`httpx.ReadError`, `Timed out`, `Connection reset`, or "polling restarted after network error",
the flapping is often a **transport-level route problem**, not an application bug.

### Key insight

Broken IPv6 (or a flaky network route) often passes **short** requests but fails on
**long-held connections**. If you only probe with quick `curl` or ping, everything looks
fine while the actual service — which holds connections open (e.g. Telegram's `getUpdates`
long-poll) — flaps constantly. This produces a maddening "works in testing, breaks in
production" picture.

The diagnostic: hold connections open to the target for as long as the real service does,
and compare routes (auto vs forced-IPv4 vs forced-IPv6).

## Procedure

1. **Measure, don't assume.** Build a probe that opens a TLS connection to the target
   host:port, sleeps for the real service's hold time (Telegram ≈8-10s), then does a
   minimal read. Run 8-12 rounds per route.
2. **Isolate routes.** Test `auto` (OS default), forced IPv4 (`curl -4`), and forced IPv6
   (`curl -6`) separately. The failing route will show timeouts; the working route will be clean.
3. **Scope the fix to the failing route.** Do not disable IPv6 globally unless it is broken
   to *all* hosts. If only specific hosts (e.g. `api.telegram.org`) fail, pin those hostnames
   to IPv4 only and leave everything else dual-stack.
4. **Verify continuously after fixing.** A short "it works now" is insufficient — the bug was
   intermittent. Confirm the new route holds connections cleanly across many rounds, and that
   the application's reconnect rate drops to zero.

## Common trap: your own diagnostic conflicts with the live service

Telegram (and similar long-poll APIs) allow **only one `getUpdates` consumer per bot token**.
If you probe `getUpdates` while the bot is running, you get `HTTP 409 Conflict` — which looks
like the bot is broken but is actually *proof your probe is colliding with the live poller*.

**Solutions:**
- Use a **transport-level probe** (raw TLS connect + hold + minimal HTTP) against the API
  host:port instead of calling `getUpdates`. Read-only, no conflict.
- If you must test the API method, stop the bot first. The conflict is expected and harmless.

## When to suspect this

- Logs show repeated reconnects, "network error (attempt N)", `ReadError`, `Timed out`
- The service works for seconds to minutes after each restart, then drops
- Quick curl/ping to the same host succeeds consistently
- The service uses long-polling, streaming, SSE, or WebSockets

## Example: Telegram bot flapping (2026-08-26)

```
auto   : 6/8 ok — 2x TimeoutError   ← resolver returns AAAA first; v6 long-polls die
forced v4: 8/8 ok — zero failures    ← the good route
forced v6: 6/8 ok — 2x TimeoutError  ← confirms v6 is the broken route
```

Fix: force IPv4 for `api.telegram.org` / `telegram.org` only, via a `sitecustomize.py`
that filters `socket.getaddrinfo` results for those suffixes. Fail-safe: if no A record
exists, return the original list unchanged.

See `scripts/_probe_transport.py` for a reusable, read-only transport probe.

---

## Windows-specific: BOM-less `.ps1` with non-ASCII chars

Windows PowerShell 5.1 reads BOM-less `.ps1` files as the system ANSI code page. If the
file contains UTF-8 characters outside ASCII (em-dashes, curly quotes, non-Latin letters),
PowerShell mis-decodes them and fails with a confusing parse error like:
`Missing argument in parameter list` or `The term '-X' is not recognized`.

**Fix:** prepend a UTF-8 BOM (`0xEF 0xBB 0xBF`) to the file. This is the *opposite* of the
usual "no BOM for UTF-8" rule — PowerShell 5.1 specifically needs it.

(Note: `config.yaml`, `.env`, and JSON files have the opposite rule — no BOM. Only `.ps1`
and other PowerShell 5.1-consumed scripts need the BOM.)

**Fix (Python):**
```python
from pathlib import Path
p = Path("script.ps1")
raw = p.read_bytes()
if not raw.startswith(b"\xef\xbb\xbf"):
    p.write_bytes(b"\xef\xbb\xbf" + raw)
```
