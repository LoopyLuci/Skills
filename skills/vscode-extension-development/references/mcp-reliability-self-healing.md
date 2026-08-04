# MCP Server Reliability (VS Code Extension)

Patterns for making an MCP-over-HTTP server hosted by a VS Code extension
self-healing and crash-resilient.

## 1. Port fallback on EADDRINUSE

When the configured port is already taken (another instance, stale process),
don't just crash — retry on the next port. Use an error listener + recursive
`listen` rather than a fixed loop, so the retry fires on the async `error`
event (the `EADDRINUSE` is *not* thrown synchronously from `listen`).

```ts
let actualPort = port;
let attempt = 0;
const maxAttempts = 50;

function bind(p: number): void {
  server.on('error', (err) => {
    if (err.code === 'EADDRINUSE' && attempt < maxAttempts) {
      attempt++;
      actualPort = p + 1;
      server.close();      // release the failed listener
      bind(p + 1);          // retry
    } else {
      console.error('Failed to bind:', err.message);
    }
  });
  server.listen(p, '127.0.0.1', () => {
    console.log(`listening on ${actualPort}`);
  });
}
bind(port);
```

Expose the *resolved* port via a getter so callers (status bar, config
registration) use the real port, not the configured one:

```ts
Object.defineProperty(server, 'port', { get: () => actualPort });
// caller: const actual = (server as any).port;
```

When the watchdog triggers a restart, wrap the stop→start cycle in a
`restartMcpTransport` helper that also re-renders the status bar with the
resolved port. Guard the whole thing in try/catch so a failed restart
does not crash the extension host:

```ts
function restartMcpTransport(): void {
  try {
    stopHttpTransport();      // clears health timer too
    startHttpTransport(createServer());
    renderStatusBar();        // picks up resolved .port getter
  } catch (err) {
    console.error('[Hermes MCP] Watchdog restart failed:', err);
  }
}
```

### Test (real, not mocked)
Bind a throwaway `http.Server` to port 0, read its port, then start your
MCP server on that same port and assert it falls over to `port+1` and
`/health` answers on the new port.

## 2. Health-check watchdog (auto-restart)

A 15s `setInterval` polls `/health` with a 5s timeout. Three consecutive
failures → stop + restart the transport. Reset the counter on success.

```ts
let watchdogFailCount = 0;
const WATCHDOG_MAX_FAILURES = 3;

healthTimer = setInterval(async () => {
  try {
    const res = await fetch(`http://127.0.0.1:${port}/health`, {
      signal: AbortSignal.timeout(5_000),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = (await res.json()) as { status?: string };
    if (data.status !== 'ok') throw new Error('unhealthy');
    watchdogFailCount = 0;
  } catch {
    if (++watchdogFailCount >= WATCHDOG_MAX_FAILURES) {
      watchdogFailCount = 0;
      stopHttpTransport();
      startHttpTransport(createServer());
    }
  }
}, 15_000);
```

Clear the timer in `deactivate` / `stopHttpTransport` to avoid leaks.

## 3. SecretStorage for API keys (never settings.json)

Do **not** persist `llm.apiKey` to `vscode.workspace.getConfiguration().update(...)`
— that writes plaintext into `settings.json`. Use the extension context's
`SecretStorage` instead:

```ts
// store
await context.secrets.store('hermes.llm.apiKey', apiKey);
// read (e.g. before _sendConfig)
const key = await context.secrets.get('hermes.llm.apiKey');
// delete (key cleared)
await context.secrets.delete('hermes.llm.apiKey');
```

The extension-context-secrets object is available wherever you hold the
`ExtensionContext` (panel provider constructor, etc.).
