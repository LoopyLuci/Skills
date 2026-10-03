---
name: declared-vs-consumed-audit
description: Use when a feature looks done but may have no consumer.
---

# Declared-versus-consumed audit

A rendered control, a save method, or a passing test proves nothing if nothing
reads the value. Before calling a feature done, check that a declared surface has
a real consumer.

## The pattern that keeps producing defects

The same shape appeared four times in one project: a list maintained by
inspection drifts away from the code, and the drift is invisible until something
reads the real behaviour.

1. Three settings were labelled "not wired up" when the app actually wrote them
   at startup. The label was wrong because it came from a per-setting grep
   rather than from reading who reads and who writes.
2. Wiring `ai_provider` exposed that its option list omitted providers the
   parser already supported - the control could not select what the engine used.
3. `set_setting` replied `success` even when the store rejected the key.
4. A CI gate failed on first run and revealed that Linux/macOS had not compiled
   for some time.

## What to do

1. **Classify into three states, not two.** Live (read and honoured), read-only
   (written by the app to mirror real state; changing it does nothing), and
   inert (nothing reads it). The middle state is the one people miss, and
   labelling it "not wired up" is simply incorrect.
2. **Derive the truth mechanically.** A scanner that finds readers and writers
   per name beats a hand-maintained list. It should also check the two derived
   lists against each other for overlap.
3. **Gate it.** The scan runs in CI and fails on drift. Failing cheaply beats
   noticing a fifth time.
4. **Print the full picture** - every classified name - not just a verdict. A
   clean result from a broken parser is worse than a failure.

## Parser bugs to expect

When auditing by parsing source:

- Slicing an enum to the next `pub enum` silently absorbs the following enum's
  variants.
- Wire formats are often snake_case (`serde` `rename_all`) while the enum is
  PascalCase, so the two never compare equal. Normalise both sides.
- A name appearing near an unrelated `.set(` is not evidence it is written.

Always print the parsed set and check it against reality before trusting a pass.

## Probing, not just unit testing

A unit test over a helper proves the helper works, not that it is called. For
"is this setting live?", assert the value reaches runtime state through the real
interface - over IPC, in the process, while the app runs. Expect the probe's own
assumptions to be wrong first: correct wrong field names, response envelopes and
clamp-versus-reject semantics before concluding the app is broken.

## cfg-gating

`#[cfg(windows)]` on an implementation does not gate its tests or the imports it
uses. Tests calling a platform-only function fail to compile elsewhere, and
`use x::{self, ...}` names `self` on every platform. Check non-Windows targets;
a Windows-only dev loop cannot see these.