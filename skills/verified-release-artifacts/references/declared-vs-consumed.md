# Declared versus consumed

A rendered control, a save method, or a passing test proves nothing if nothing
reads the value. Use this before calling any settings, agent-profile or
control surface done.

## Classify into three states, not two

| State | Meaning |
|---|---|
| Live | Read by code that changes behaviour |
| Read-only mirror | The app writes it at startup to mirror real state; changing it does nothing |
| Inert | Nothing reads it |

The middle state is the one people miss. Labelling it "not wired up" is simply
incorrect: the window is showing the truth.

## The two false passes

Both of these make an audit report a clean result while the feature is inert:

- **Counting the settings layer as its own consumer.** The store, the view model
  and the settings screen pass a value between each other; that is round-tripping,
  not behaviour. Exclude them explicitly or every setting reports live.
- **Treating a successful read-back as proof of storage.** A write into an
  in-memory map reports success and reads back correctly for the life of the
  process, then vanishes on restart. Verify the value survives a restart, and
  that the process reading it is the one that consumes it.

## Parser bugs to expect

- Slicing an enum to the next `pub enum` absorbs the following enum's variants.
- Wire formats are often snake_case while the enum is PascalCase, so the two never
  compare equal. Normalise both sides.
- A name appearing near an unrelated call is not evidence it is written.
- A dispatcher that merely forwards is not where commands are declared; find the
  registry the dispatcher calls into.

Always print the parsed set and check it against reality before trusting a pass.
A clean result from a broken parser is worse than a failure.

## Prove it on the wire

The only place a generation setting is observable is the request that leaves the
process. Point the app at a local stub that records the body, then assert on the
wire format - not on what the UI shows.

On a physical handset, `127.0.0.1` is the handset. Forward the port to the host:

```bash
adb -s <serial> reverse tcp:PORT tcp:PORT
```

Check the capability is actually the field that provider reads. An OpenAI-shaped
endpoint takes `max_tokens`; Ollama ignores it and reads `options.num_predict`.
Sending the field the app already had proves nothing if that provider never reads
it.

When a probe fails, add one log line to the app and read it. Guessing the cause
from a silent failure costs more than the log line, and a stale process will
happily report the previous build's behaviour - force-stop and relaunch before
believing a diagnostic.

Expect the probe's own assumptions to be wrong first: wrong field names, wrong
response envelopes, and clamp-versus-reject semantics.

## A gate must not fire on what the UI already discloses

If inert controls are already disabled and labelled with the missing capability,
a CI check that fails on them is noise, and noise trains people to ignore the
gate. Fail on what is *undisclosed*: a command advertised but unable to run, a
setting the UI presents as working. Report the rest as counts.

Note that a fresh CI runner has no built binary, so a probe that launches the app
fails for a reason unrelated to the audit. Build first in that job.

## Disabled-and-labelled is a legitimate end state

Before implementing a control whose backing feature does not exist, check
whether it is already honestly labelled. Each reason should name the missing
capability specifically ("no boot receiver is registered", "no animation system
in the UI"), not apologise generically - a reader can then tell whether it is
waiting on a permission, a service, or a feature nobody has built.

## Non-Windows targets

`#[cfg(windows)]` on an implementation does not gate its tests or the imports it
uses: tests calling a platform-only function fail to compile elsewhere, and
`use x::{self, ...}` names `self` on every platform. A Windows-only dev loop
cannot see these; CI on a second target will.