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
surface has a consumer at all, see `references/declared-vs-consumed.md`.

## When to Use

- Before reporting any settings, toggle, provider, or endpoint change as working.
- When a value is stored and you need evidence it is also applied.
- When a unit test passes but the feature appears dead to a user.
- When the user has hardware connected and asked for proof, not a build.

Do not use it for pure logic with no runtime surface: that is ordinary unit
testing, and reaching for a device there is wasted time.

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

## Durable success signals

Prefer a check that is impossible to satisfy accidentally:

- The recorded request body contains the exact value that was configured,
  rather than merely a successful status code.
- The persisted file exists and reads back after a relaunch.
- The screenshot shows the working control enabled and the broken one visibly
  disabled, in the same frame.