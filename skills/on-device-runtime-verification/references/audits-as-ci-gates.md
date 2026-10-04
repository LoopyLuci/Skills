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
- **Read the job's `working-directory` and available tools before writing a step
  into it.** Two mistakes in one replacement step: it assumed `unzip` existed on
  the runner, and it `cd`-ed into a directory that did not exist relative to the
  job's own working directory. Both fail on first run for reasons unrelated to
  what the gate checks. Run the new command locally with the same shell before
  committing it.
- **A gate that fails on something already disclosed elsewhere is noise.** A
  scanner that exits non-zero because a setting has no consumer, when every such
  setting is already shown to the user as disabled with the reason named, turns
  the job red for a finding that has already been handled. Narrow the exit
  condition to the part that is genuinely undeliverable - a command advertised
  but unable to run, because an agent would be told it is available and it would
  do nothing - and keep the rest as reported output.
- **Prefer a local check over a remote-fetching action.** The official
  `gradle/actions/wrapper-validation` downloads the expected checksum from
  services.gradle.org, so a runner without access to it fails before anything
  compiles and takes the signed-release step with it. That is a supply-chain
  nicety that became a single point of failure; a local archive listing over the
  committed JAR is enough, because the build itself exercises the wrapper.
- **Do not trust a green gate on the run that added it.** Read the step list to
  confirm each check actually executed rather than being skipped.
- **Count from the raw declared list, not a deduplicated set.** A duplicate entry
  and a missing handler produce the same count mismatch, and deduplicating first
  hides the discrepancy from the check meant to expose it. Report duplicates
  explicitly: harmless at runtime, fatal as drift.
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