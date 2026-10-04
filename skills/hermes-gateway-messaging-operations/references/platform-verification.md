# Verifying a messaging platform end-to-end

Goal: real proof that a message can leave Hermes and reach the user's chat, and
that the allowlist authorizes their user ID. Three independent checks, cheapest
first.

## 1. The token is real (no gateway involved)

Telegram's `getMe` answers instantly and needs no polling slot, so it validates
the token without competing with the running gateway:

```python
import json, re, urllib.request
s = open('.env', encoding='utf-8').read()
tok = re.search(r'^TELEGRAM_BOT_TOKEN=(.+)$', s, re.M).group(1).strip()
r = json.load(urllib.request.urlopen(f'https://api.telegram.org/bot{tok}/getMe', timeout=20))
print(r['ok'], r['result']['username'], r['result']['id'])
```

`ok: False` here means a wrong/revoked token, not a Hermes problem.

## 2. The gateway's own view

After a restart, poll the log rather than sleeping a fixed amount:

```bash
tail -40 "$HERMES_HOME/logs/gateway.log" | grep -E "connected|polling|Channel directory"
```

Success looks like all three of: `telegram connected`,
`polling confirmed healthy: getUpdates progressing`, and
`Channel directory built: 1 target(s)`. A `0 target(s)` line with a connected
platform means the allowlist parsed to nothing — the usual cause is a value
line carrying a trailing inline comment.

## 3. A real delivery (the only conclusive check)

Send to the configured home channel and read the response, rather than trusting
any local state file:

```python
def api(method, **params):
    body = urllib.parse.urlencode(params).encode()      # bytes, not str
    return json.load(urllib.request.urlopen(
        f'https://api.telegram.org/bot{tok}/{method}', body, timeout=20))

r = api('sendMessage', chat_id=home, text='...')
print(r['ok'], r['result']['message_id'], r['result']['chat'].get('username'))
```

Gotchas that look like failures but are not:

- `TypeError: POST data should be bytes, an iterable of bytes, or a file
  object` — `urlencode(...).encode()` is missing. `urlopen` rejects a `str`
  body.
- Do not pass `parse_mode=None`; omit the parameter entirely.
- `chat_id` must be the numeric user/channel ID. Resolving a `@handle`
  yourself is unnecessary — `sendMessage` accepts a `@channelusername`
  directly.

Run this once before the restart and once after it. Identical success both
times is what separates "the gateway is running" from "the gateway works".

## Interpreting `gateway_state.json`

`platforms.<name>` is written by a separate writer PID, so `state: "connected"`
can be weeks stale. Always sanity-check `updated_at` and `writer_pid` against
the live process before believing it:

```python
import json
d = json.load(open('gateway_state.json'))
print(d['pid'], d['gateway_state'], json.dumps(d.get('platforms'), indent=1))
```

`updated_at` older than the current `pid`'s start time means the entry is
leftover, not live.

## Gateway death without a shutdown record

`hermes gateway status` warns when the previous process died with no clean
shutdown. The usual cause on this host is that the shell which ran
`hermes gateway start` sat inside a Windows Job Object that killed the child on
exit. The fix is the Startup-folder VBS login item, which
`hermes gateway status` confirms is installed:

```
C:\Users\Server\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Hermes_Gateway.vbs
```

Start the gateway from a normal interactive prompt or a detached spawn, not
from inside a job-bound tool shell, or it will be reaped again.
