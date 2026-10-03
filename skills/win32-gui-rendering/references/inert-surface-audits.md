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

## Classify into three states, never two

The two-way live/inert split is wrong for every setting the app seeds from
runtime state. Three states, each needing different wording in the UI:

| State | Test | UI must say |
|---|---|---|
| Live | read and honoured | nothing — editable |
| Read-only mirror | written by the app, never read | "set by the app - read only" |
| Inert | never read, never written | "not wired up yet" |

Labelling a mirror "not wired up" is simply incorrect: the window shows the truth
there, it just cannot be edited. Deriving the lists from a per-item grep
produces exactly this wrong answer, because a grep cannot tell a reader from a
writer.

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
real findings. Scope the search to the `set(` call expression itself.

## A gate that cannot reach its subject fails for the wrong reason

A probe that launches the binary needs one built. On a fresh CI runner there is
none, so the job reports "the app did not start" — which says nothing about the
audit and gets misread as an audit failure. Add an explicit build step ahead of
every live probe, and keep static checks (the scan, the parser audit) runnable
without one so a tooling failure is distinguishable from a product failure.

## Turn the scan into a gate

Hand-maintained lists rot as soon as one item gains a consumer. Have the scan
derive the truth from code and fail when the UI's lists disagree with it or with
each other, then run it in CI. The gate is the point: three successive defects
came from a list drifting away from the code, and each was caught by an audit
rather than by reading.

Expect the gate to fail the moment you fix something — that is it working. Wiring
six settings to real consumers made the window's inert list wrong within the
same change, because the derived truth moved and the hand-maintained list did
not. Fix the list in the same commit, and add a test naming the newly-wired
items so a regression fails a test rather than needing a new audit.

## A clean audit is not a licence to skip the probe

An audit proves declarations are wired to handlers. It does not prove the
*behaviour* works. It found no defects on the MCP/IPC surfaces in one session
while the runtime behind them still had an inert settings path — keep the
end-to-end probes that exercise real state alongside the static gate.

## Probes lie about their own assumptions first

A new probe will usually fail for reasons that are not product defects. Before
concluding the app is broken, check the probe's model of the interface:

- the wire field name (`key` vs `name`) — a parse error on every call reads as
  "the write was refused"
- the response envelope (`{"data": {...}}` nesting) and which command actually
  carries the data you are reading
- **clamp vs reject semantics.** A validating store refuses an out-of-range write
  and keeps the previous value; a clamping one stores the bound. Assert the real
  behaviour, and treat "rejected write leaves the old value intact" as its own
  positive check.
- whether the value is read from the live store or a per-frame snapshot mirror,
  which may not contain the field you are asserting on

Correct those, then re-run. Only what survives is a real finding.