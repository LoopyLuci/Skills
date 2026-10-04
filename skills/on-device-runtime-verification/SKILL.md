---
name: on-device-runtime-verification
description: Use when a change must be proven on real hardware.
version: 1
author: hermes-curator
license: MIT
metadata:
  hermes:
    tags: [verification, testing, android, instrumentation, end-to-end]
    related_skills: [systematic-debugging, test-driven-development]
---

# On-device runtime verification

A build that compiles, and a unit test over a helper, both pass while the change
does nothing. To prove a change reaches runtime you have to observe the effect
at the far end: bytes on a socket, an entry in a device log, a pixel in a
screenshot.

This skill covers setting up that observation harness. For auditing whether a
surface has a consumer at all, see `references/declared-vs-consumed.md` - which
also covers the permission-declared-but-never-requested class and the rule that a
repeated "what next?" means build the top item, not re-rank. For pointing a
handset at a recorder and reading replies back, see
`references/device-recorder-harness.md`. For wiring that audit into CI so drift
fails a build, see `references/audits-as-ci-gates.md`. For checking and trusting
what the remote pipeline actually did, see `references/remote-ci-state.md`. For
the Kotlin/Compose compile errors that cost a build cycle each, see
`references/kotlin-compose-api-errors.md`.

## When to Use

- Before reporting any settings, toggle, provider, or endpoint change as working.
- When a value is stored and you need evidence it is also applied.
- When a unit test passes but the feature appears dead to a user.
- When the user has hardware connected and asked for proof, not a build.

Do not use it for pure logic with no runtime surface: that is ordinary unit
testing, and reaching for a device there is wasted time.

## Reporting

Lead with what changed and what was verified. State limits plainly, including
anything the check could not cover, rather than letting a clean count imply more
than it does. A "0 unconsumed" result means no surface is lying to the user, not
that the product is finished - say so, because the distinction is the honest one.
The same applies to a green audit generally: it is evidence about declared
surfaces, not a completeness claim, and an engine with no sound files or a
permission prompt that was never written still satisfies it.

**A repeated "what next?" means build, not re-rank.** Answering that question
with another prioritised list reads as not having listened, and the user asking
again is the correction. After the first list, the correct shape is one sentence
naming the single highest-value item, then doing it and reporting what changed -
no ranking, no options, no closing question. Offering alternatives and waiting
hands back a decision the user has already made by asking again. Once the
pattern is established, keep going without waiting for a "go": each cycle should
carry something that could not have been said before - a number that moved, a
defect class found, a control that was hollow. If a cycle produces no such thing,
the item chosen was wrong, not the format of the reply.

When the autonomous work is genuinely exhausted, that is the real answer: say
what is blocked on the user specifically - credentials, a signing key, a scope
decision - and stop. Repeating a list as filler once there is nothing left to
build is exactly what the repetition is complaining about.

## Procedure

1. **Pick the observation point closest to the effect.** A control change is
   proven by what the code under it emits, not by what the UI shows. Assert on
   the request body the app actually sends, the file it actually writes, or the
   value it actually logs.
2. **Redirect the app's traffic to something you control.** Point the app at a
   local stub that records its input. A static fixture proves less than a
   recorder.
3. **Force-stop and relaunch before every assertion.** A reinstall leaves the old
   process running; probing it tests the previous build and yields a confident
   wrong answer.
4. **Drive the app through its real interface**, not by calling internals.
5. **Assert, then read the whole reply.** A partial match against a status field
   is how an error path passes as success.
6. **Capture the screen and look at it** when the claim is about presentation.

## Pitfalls

- **Assert on the wire format, not on storage.** A value that persisted is not a
  value that was honoured; a setting can save perfectly and never be read.
- **Restart before diagnosing.** Stale processes serve stale code. When a value
  appears not to propagate, confirm the running process is the one you just
  built before hunting the cause.
- **Log the resolved value at the boundary** when a value seems lost. One log
  line naming the layer that dropped it replaces a build cycle per hypothesis.
  Guessing which layer failed is the slowest possible path.
- **Expect the probe's own mismatches first.** Wrong field names, wrong response
  envelopes, wrong control coordinates, and a clamp-versus-reject semantic
  difference are all common and all masquerade as product defects. Fix the probe
  before you "fix" working code.
- **Tap coordinates are guesses.** Derive them from the layout or dump the view
  hierarchy; a mis-landed tap can look like a missing screen.
- **Read the log per-tag, and match the response line specifically.** A stack
  trace follows a successful reply, so "the last tagged line" picks up noise and
  turns a pass into a fail.
- **Resolve platform tools from the SDK, not `PATH`.** A tool that works in a
  terminal you configured is not available to a script you run later.
- **`10.0.2.2` is the emulator loopback, not the host.** On a physical handset use
  `adb reverse` to forward a host port, or the request simply never arrives.
- **Audit each client separately.** A desktop and a mobile client in one codebase
  can have completely different consumers, so one platform's audit says nothing
  about the other.
- **Finish the job in the same pass.** An audit that ends in a list of next steps
  reads as stalling. Fix what it found, then report what is fixed and what is not
  - and when the answer to "what is next?" is already known, build the top item
  rather than re-prioritising it. A repeated question is a stronger signal than
  the first: after the second, stop ranking entirely and ship, and lead the reply
  with what you did rather than the list you did not need to give.
- **Silence from a device is evidence about the harness first.** Confirm logcat
  works, the app launches, and the component is registered before concluding the
  code is at fault. `am start -W` reports a misleading component error even for
  a registered, launchable activity, so read the whole output rather than its
  first line.
- **A protected broadcast cannot be simulated.** `am broadcast` will not deliver
  a system action such as boot, and a real reboot that produces no log says
  nothing about the receiver. Test the decision instead: instantiate the
  component directly in an instrumented test and assert the branch it takes.
- **A framework handle can be absent.** `goAsync()` returns null when nothing is
  driving a receiver, and the resulting null dereference lands on a worker thread
  where no log will ever show it. Guard the handle and run the work inline when
  it is missing, which also makes the component directly testable.
- **A recomposition key derived from what it renders never changes.** An overlay
  keyed on a value computed from the data it displays never re-reads, so the
  command reports success and the screen shows the old state. Drive rendering
  from a real monotonic counter, and confirm the change by reading the captured
  screen back.
- **Every record looking the same is an identity problem, not a rendering one.**
  When a feature is wired correctly yet the data never changes what appears,
  suspect a lookup that misses and falls back: generated ids against referenced
  names, or a default that swallows the miss. Compare two records that should
  differ; if they render identically, fix the data layer, not the view.

## Durable success signals

Prefer a check that is impossible to satisfy accidentally:

- The recorded request body contains the exact value that was configured,
  rather than merely a successful status code.
- The persisted file exists and reads back after a relaunch.
- The screenshot shows the working control enabled and the broken one visibly
  disabled, in the same frame.