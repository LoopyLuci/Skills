# Auditing surfaces that may be inert

A surface can look finished — it renders, it saves, it reports success — and be
read by nothing. When three defects in a row turn out to share that shape, stop
implementing and measure the whole class.

## What to scan

| Surface | Reader to find | Writer to find |
|---|---|---|
| Settings / config keys | code reading the key | code calling `.set()` on it |
| MCP tools | the IPC command the tool sends | the loop that handles it |
| IPC commands | the loop arm that acts on it | the socket arm that answers inline |
| Profiles / agents | the accessor that turns one into runtime config (`to_agent_config`) | `apply_profile` and its callers |

A declared item with no reader is inert. A declared item the app *writes* but
never reads is a **read-only mirror** — a third state that a one-list "inert"
predicate cannot express (see `settings-editor-model.md`).

## Make the parser prove itself

An audit that reports `PASS` while its parser is broken is worse than one that
fails, because it gets promoted to a CI gate and then enforces nothing. Two traps
that produced total false passes:

- **Slicing an enum to the next `pub enum`.** Between `GodotCommand` and the next
  enum declaration sits `ControlRequest`; slicing to the next declaration folds
  its variants into the first enum's list, so the real commands disappear and
  unrelated ones take their place. Slice to the enum's **own** closing brace.
- **Comparing a wire name to a variant name.** `#[serde(rename_all =
  "snake_case")]` means `nine_router_status` arrives on the wire while the variant
  is `NineRouterStatus`. These never string-equal, so every item reads as unknown.
  Normalise both sides before comparing.

Have the audit print what it derived, not just its verdict:

```
Reachable commands: 39/39
  queued to the loop: ActivateAgent, DeleteAgent, ...
  answered by the socket: Ping, GetStatus, ...
  handled by the loop: ActivateAgent, DeleteAgent, ...
```

Then check the numbers against something you already know. If you have eleven
agents and the audit says zero, the parser is wrong.

Also prefer the *strictest* interpretation that still works: a loose window of
characters around a `.set(` call marks every setting as a mirror and hides the
real findings.

## Turn the scan into a gate

Hand-maintained lists rot as soon as one item gains a consumer. Have the scan
derive the truth from code and fail when the UI's lists disagree with it or with
each other, then run it in CI. The gate is the point: three successive defects
came from a list drifting away from the code, and each was caught by an audit
rather than by reading.

## A clean audit is not a licence to skip the probe

An audit proves declarations are wired to handlers. It does not prove the
*behaviour* works. It found no defects on the MCP/IPC surfaces in one session
while the runtime behind them still had an inert settings path — keep the
end-to-end probes that exercise real state alongside the static gate.