# Audits as CI gates

A one-off audit is a report. An audit wired into CI is a guarantee. The
difference is what happens the next time a list drifts away from the code.

## Why gate it

Manual audits catch what exists at the moment they run and nothing else. Drift is
the normal state of a hand-maintained list, and drift is invisible until something
reads real behaviour. A gate converts a silent defect into a red build at the
moment it is introduced.

The evidence that gates earn their cost: every one added so far failed on its
first run, and each failure was a real defect rather than a gate bug - including
a portability break that had been sitting undetected because development
happens on one platform.

## Procedure

1. **Make the scanner exit non-zero on drift**, not merely print a report. A gate
   that always passes is documentation.
2. **Fail on both directions.** A list claiming something is dead when the code
   honours it, and a list omitting something that is dead. One direction is a
   warning; both are the point.
3. **Check derived lists against each other** for overlap, so a name cannot be
   both live and inert.
4. **Print the full classified set** in the log, so a reviewer can see what the
   parser found without re-running it.
5. **Add the build the gate needs.** A gate that launches the app and probes it
   requires a binary; on a fresh runner there is none, and the gate fails on "the
   app did not start" - which says nothing about what it was checking.

## Pitfalls

- **A gate that needs a binary must build one first.** Otherwise it fails on
  first contact and gets ignored.
- **Do not trust a green gate on the run that added it.** Read the step list to
  confirm each check actually executed rather than being skipped.
- **A single-platform dev loop cannot see portability breakage.** Cross-target
  compile and test belong in CI, or cfg-gated code rots unchecked.
- **Do not weaken a gate to make it pass.** When a gate starts failing, the first
  hypothesis is that it found something real. Relaxing the assertion is the one
  move that destroys the value of having written it.
- **If a hand-maintained list is unavoidable, gate its agreement with the code
  rather than trusting it.** The gate's job is to fail the moment a human is
  wrong, not to be correct itself.

## Reporting

State what the gate caught and when. A gate's value is only legible from the
defects it prevented, and reporting "added a CI check" without the failure it
caught reads as process rather than progress.