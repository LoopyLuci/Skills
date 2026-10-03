# Remote CI state is its own evidence

Local gates pass, remote gates are a separate system with separate inputs, and
"green locally" is not a claim about CI. Checking the remote run is a separate
step, and skipping it produces a confident false report.

## Why this needs its own rule

A session can end reporting "all green" while the remote pipeline has been red
for several runs. The local evidence is entirely true: the tests pass, clippy
passes, the probes pass. What is missing is the only thing that would have caught
it.

The tell is that the release step and the CI step come from the same claim. If
you say "all gates green, releasing", the green refers to what you ran, and the
release assumes more than you checked.

## Procedure

1. **Query the remote run after pushing**, every time: list the runs, then read
   the job and step conclusions, not just the workflow conclusion. A workflow
   marked success with a job skipped is not a green pipeline.
2. **Read the step list on the run that added a gate.** Confirm each new check
   executed rather than being skipped, which is the only way to know the gate ran
   at all.
3. **Distinguish infrastructure failure from defect before touching code.** A
   timeout contacting a third-party service from a hosted runner is not a bug in
   the repository. Read the failing step's actual output rather than its name.
4. **Fix, then watch the replacement run to completion.** Committing a workflow
   fix and reporting it as done is the same false claim in a new coat.
5. **Verify any replacement step locally first.** A shell step added to a
   workflow is code; run it before pushing and burn a cycle on it locally
   instead of in CI.

## Pitfalls

- **A third-party validation action is a single point of failure.** Wrapper
  checksum validation that fetches an expected value from a remote service fails
  the whole job before anything compiles when that service is unreachable, and
  silently skips every step behind it. Prefer a local check, or accept that the
  gate can block the build on someone else's uptime.
- **Do not add a step you have not executed.** Tools absent on the runner image
  (`unzip`, platform-specific utilities) and a `cd` that contradicts the job's
  configured `working-directory` are the two most common self-inflicted failures.
  Both read as infrastructure noise and cost a full CI round trip.
- **A transient local failure is not a remote one, and vice versa.** A local
  error you retried past says nothing about the runner, and a green local run
  says nothing about a remote gate.
- **Job-level "skipped" hides behind a red sibling.** When one step fails, every
  later step reports skipped, which reads like scope reduction rather than
  breakage. Name the first failing step.
- **Report the honest state when a gate cannot be reached.** "The Android job is
  red for a reason I have identified but not yet fixed" is useful; "all green" is
  worse than no report, because it stops the next session from looking.