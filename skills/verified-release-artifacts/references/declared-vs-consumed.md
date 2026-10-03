# Declared versus consumed

A rendered control, a save method, or a passing test proves nothing if nothing
reads the value. Use this before calling any settings, agent-profile or
control surface done.

## Audit before you build, not after

Scan the surface **first**, then plan against what the scan found. A plan written
before the scan is a guess about which parts are already broken, and the guess is
usually wrong in the direction that wastes the most work.

Concretely: a parity assessment based on reading feature lists will claim a
client is "a few settings behind" when it has no consumer for most of them. The
audit costs an hour; rebuilding the wrong thing costs days. Re-read the code for
the specific claim before recommending it — a confidently-stated wrong premise
sends the user to build what already exists.

## A command that reports success while changing nothing is worse than a dead control

A visible, disabled control is honest. A control that accepts input, replies
`{"queued": true}`, and changes no observable state is a lie that costs the user
more time, because they will assume it worked and debug something else.

These cluster in the dispatch layer, and are the highest-value findings an audit
produces:

- The handler validates, enqueues, and returns — but the consumer of that queue is
  never wired.
- The handler mutates an in-memory status record while the real store is
  elsewhere, so the value neither persists nor arrives.
- The handler takes a parameter and never stores it at all.
- A reporter returns **hardcoded placeholder values** (a fixed `0.0` position, a
  fabricated `"none"` id) instead of reading live state, so no command is
  observable and an agent that moved something is told it stayed put.
- The reporter reads a different source than the writer mutates.

Check the read path and the write path of every command against each other. If a
response is meant to prove a change happened, it must be derived from the thing
that changed.

## Classify into three states, not two

| State | Meaning |
|---|---|
| Live | Read by code that changes behaviour |
| Read-only mirror | The app writes it at startup to mirror real state; changing it does nothing |
| Inert | Nothing reads it |

The middle state is the one people miss. Labelling it "not wired up" is simply
incorrect: the window is showing the truth.

## The two false passes

Both of these make an audit report a clean result while the feature is inert.
See "Parser output must be cross-checked" for why a clean result needs the full
set printed before it is believed.

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

## A correct command can still be invisible

The wire and the screen are two different consumers. A command that is handled
correctly at the backend can still show nothing, because the render layer caches
what it read under a key that never changes.

Symptoms to recognise: the IPC reply is correct, the engine state is correct, and
the screen shows the old value. The defect is in how the view is keyed or how
often it re-reads, not in the command.

- A frame counter or tick value **derived from the data being displayed** never
  changes, so the view never recomposes. It must increment monotonically on its
  own, from the thing that drives redraws.
- Caching a read inside an effect keyed by the same value it reads makes the
  cache permanent.
- Verify the display explicitly: after a command, confirm the rendered output
  changed, with a screenshot read back, not by trusting the reply.

This class is invisible to a passing backend test and to a green IPC probe. It
needs the render tier.

## Parser output must be cross-checked before it is believed

An audit that reports a clean result from a broken parser is worse than one that
fails. Two false passes recur:

- **Counting the plumbing layer as a consumer.** The store, view model and screen
  pass a value between each other; that is round-tripping, not behaviour. Exclude
  them explicitly or every setting reports live.
- **Reading the parser's own input wrong.** Slicing an enum to the next
  `pub enum` absorbs the following enum's variants; reading commands from the
  dispatcher that only forwards finds none.

Every audit must print the full classified set, not a verdict, so the numbers can
be eyeballed against the code. When an audit says "0 unreachable" and you know
the surface has commands, suspect the parser before you trust the result.

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

When a setting later gains a real consumer, remove its label in the same change.
A stale "not wired up" is its own lie.

## Two store bugs that look like working code

Both are one-line ordering mistakes that no amount of reading the happy path
catches, and both were caught only because the behaviour was asserted.

**Filtering before looking up.** `load().filterNot { it.id == id }` then searching
that filtered list for `id` always misses, so a lookup of a property belonging to
the row just removed silently returns the default. Look up first, then filter:

```kotlin
val existing = load().firstOrNull { it.id == saved.id }   // before the filter
write(load().filterNot { it.id == stored.id } + stored)
```

**Persisting a seed while claiming to store edits.** If built-ins are re-seeded
from code on load and the write path filters them out, a user's edit to one is
discarded on the next read - which looks like the save failing intermittently.
Write the user's version as an override rather than dropping it.

Both surface as an edit that saves, reports success, and is gone after a
restart - which is exactly the read-back trap above, one layer deeper. Assert the
round trip through a **fresh store instance**, since the same instance may hold a
cache that hides the loss.

## Non-Windows targets

`#[cfg(windows)]` on an implementation does not gate its tests or the imports it
uses: tests calling a platform-only function fail to compile elsewhere, and
`use x::{self, ...}` names `self` on every platform. A Windows-only dev loop
cannot see these; CI on a second target will.