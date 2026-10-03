---
name: verified-release-artifacts
description: "Use when releasing built binaries (EXE, APK, archives)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [Release, Publishing, Artifacts, Signing, Verification, CI]
    related_skills: [github-repo-management, github-pr-workflow]
---

# Verified Release Artifacts

Turning a working local project into a published release whose binaries actually
install and run. The governing rule:

> A successful build command, a successful `git push`, and a successful
> `gh release create` are each necessary and none of them is evidence. Verify
> the artifact the user will download, not the command that produced it.

Every rule below exists because the plausible-looking signal said the job was
done while the deliverable was unusable.

## When to Use

- Publishing a GitHub Release that carries built binaries (`.exe`, `.apk`,
  `.aab`, `.dmg`, `.tar.gz`).
- A push rejected for exceeding the 100 MB file limit.
- Building an Android release APK, including signing and toolchain setup.
- Any "commit, push, and cut a release" request — the audit and verification
  steps apply even when the artifacts are small and seem obviously fine.

## Order of operations

Do these in order. Steps 3 and 7 are where a "successful" release is actually
caught, and both are routinely skipped.

1. Confirm the project's own gates are green (build, lint, tests) *before*
staging a release. A release snapshotting a red tree is a bad release.
2. Build the release artifact.
3. **Audit staged content** for oversized blobs and secrets — before the first
push, not after the rejection teaches you what to look for.
4. Push.
5. **Wait for CI on that exact commit to finish green.** Do not tag a commit
whose checks are still running — see below.
6. Tag.
7. Create the release with assets.
8. **Download the assets back and verify each one.**
9. Report URLs, sizes, and what was verified vs. assumed.

### Do not tag before CI has actually run

`git push` returning 0 means the workflows were *queued*, not that they passed.
Tagging immediately produces a release whose commit is still untested, and if CI
then goes red you must either re-cut the tag or ship a release known to have a
failing gate.

```bash
git push origin main
RID=$(gh run list --limit 1 --json databaseId -q '.[0].databaseId')
gh run watch "$RID" --exit-status --interval 25 >/dev/null   # wait, do not poll-and-hope
gh run view "$RID" --json jobs -q '.jobs[] | "\(.conclusion)\t\(.name)"'
```

Every job must read `success`. If one fails, fix and push first — then wait again
for the *new* head SHA.

Note that `gh run watch` can exceed your own command timeout; re-query
`gh run view <id> --json status,jobs` rather than assuming a timed-out watch means
failure.

### Local green says nothing about remote green

Check CI state at the moment you report, not only at the moment you last pushed.
A long local-green run can coexist with a remote failure you have not looked at,
and the gap widens with every commit since. Before reporting CI as green:

```bash
gh run list --limit 5 --json workflowName,status,conclusion,headSha \
  -q '.[] | "\(.conclusion // .status)\t\(.workflowName)"'
```

If several workflows run in parallel, all must be `success`, not just the one you
remember. When a claim of "green" turns out to be stale, correct the record
explicitly and name what was actually checked - an unverified claim reported as
verified is the failure, not the underlying CI break.

### A validation action that needs the network is a single point of failure

Third-party validation actions commonly fetch expected checksums or manifests
from a remote service. If the runner cannot reach it, the job fails before
anything is compiled, and every step behind it is silently skipped - so the
release artifact step never runs while the job looks like it was about to.

Treat a remote-dependent validation step as optional unless the remote is
guaranteed reachable. Prefer a local check with no network dependency; the build
itself already exercises whatever the validation was guarding. Verify locally
before pushing a replacement: a "fix" that fails on the runner costs another full
cycle, and two of the three attempts in this class died on details the local run
could not have told you (a tool absent from the runner image, a `cd` that
duplicated a `working-directory` already set by the job).

### Keep version metadata in one story

The manifest and the tag drift independently, and the drift is invisible until a
user reports the wrong version. Before tagging, confirm these agree and that the
tag matches:

- `[workspace.package] version` (and any per-crate version that is published)
- `versionName` / `versionCode` in the Android build
- the git tag

Where a version string is printed in the app (an About box, a `--version` flag),
read it from crate metadata (`env!("CARGO_PKG_VERSION")`) instead of hardcoding
it, so it cannot drift again. Bump `versionCode` on every release — Android
requires a strictly greater code for an update to install over a published one.

### If CI fails after you have already tagged

Do not silently move the tag. Fix forward on `main`, then either move the tag
deliberately (`git tag -f` + `--verify-tag` on re-create) or keep the tag and say
plainly in the release notes which commit the binaries came from and that the fix
landed after. When the post-tag fixes are test- or CI-only, state that
explicitly so nobody thinks the published binaries changed.

### Check remote state immediately before reporting, not just before pushing

The gap between the last push and the report is where a stale "green" claim
survives. A release cut while a workflow had been failing for several commits is
still a bad release, and the user finds out from CI rather than from you.

The ordering matters: check `gh run list` *after* the last commit lands and
*before* writing the report. A workflow that failed on an earlier commit of the
same work is the same defect as one failing now - it was never green, so the
claim was never true.

Where a workflow failed for an infrastructure reason rather than a code defect,
say that explicitly and separately from code health, and say whether the fix is
verified or only attempted. Both Android runs here failed on a network timeout in
a third-party validation action while every local test passed; reporting that as
"all green" would have been false in the way that matters.

## Gate the project the way CI does

Run the exact commands the CI workflow runs, at the same strictness. Locally
permissive checks hide CI failures until after you've pushed.

```bash
cargo fmt --all -- --check          # if Rust
cargo clippy --all-targets -- -D warnings
cargo test --workspace
```

When you fix lint warnings, prefer real fixes over blanket suppression. For
code that is genuinely reserved-but-unwired, mark it with an explicit reason
(`#[allow(dead_code)] // Win32 hwnd handle; wired up when the window is shown`)
rather than deleting API surface or leaving the gate red.

## Oversized blobs block the push, and untracking is not the fix

GitHub hard-rejects any blob over 100 MB. Local commits succeed silently.

```bash
git rev-list --objects --all \
  | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
  | awk '$1=="blob" && $3>50000000 {print $3/1024/1024" MB "$4}' | sort -u
```

`git rm --cached` + `.gitignore` removes the file from HEAD but **leaves the blob
in the commit graph**, so the next push fails with the identical message. Fixing
the working tree and re-committing is the trap that costs the most time here.

```bash
pip install git-filter-repo
git filter-repo --path <oversized-file> --invert-paths --force
```

- Check `git ls-remote origin` is empty **before** rewriting. If refs exist,
  rewriting invalidates other clones — stop and tell the user.
- `filter-repo` **deletes the `origin` remote** as a side effect. Re-add it, or
  the next push fails with no upstream:
  ```bash
  git remote add origin git@github.com:OWNER/REPO.git
  git push -u origin main
  ```
- Re-run the audit afterward to confirm.

Third-party engine/toolchain downloads are the usual culprit. Prefer not
vendoring them at all: honour an existing env-var override (`GODOT_BIN`) and
document the install step in the README.

## Secrets and build output must never enter the index

Audit additions and deletions separately — a filename in the diff may be its
intended removal from tracking:

```bash
git add -A
git diff --cached --name-only | grep -iE '\.jks$|keystore\.properties|local\.properties'  # expect nothing
git diff --cached --diff-filter=A --name-only | grep -iE '\.exe$|\.apk$|\.jks$'             # expect nothing
git diff --cached --diff-filter=D --name-only | wc -l                                        # intended removals
```

Always git-ignore: keystores, `keystore.properties`, `local.properties` (leaks an
absolute local path), `dist/` staging dirs, and build output. Committed build
dirs can be thousands of files — `git rm -r --cached <build-dir>`.

Read signing credentials from a git-ignored properties file or env vars so
builds still sign without secrets in history, and **warn explicitly when no
keystore is found** — a silent fallback to a debug key produces an installable
APK that nobody flags.

In CI, a missing keystore must **fail the job, not skip it**. A step that
`exit 0`s when its secret is absent turns a missing prerequisite into a green
checkmark, and the release ships unsigned or absent while every status reads
success. Then verify the produced artifact is release-signed rather than trusting
the exit code. See `references/ci-signing-and-silent-skips.md`.

The same "green but did nothing" class of bug has other members worth auditing
for: a workflow whose `paths:` filter excludes its own file (so edits to it never
trigger it), an action that ignores the job's `working-directory` (so relative
paths 404), and `gradlew` committed without the exec bit (exit 126 on every
step). All are listed in that reference.

## Default branch must match what CI triggers on

If workflows trigger on `main` and the branch is `master`, CI silently never
runs. Rename before the first push, then set it on the remote:

```bash
git branch -m master main
gh repo edit OWNER/REPO --default-branch main
gh workflow list     # expect: active
```

## Verify by downloading the artifact back

`gh release view` showing an asset proves a row exists. Download it and verify
integrity claims, not just bytes.

```bash
gh release view v1.0.0 --json tagName,isDraft,isPrerelease,assets,url
curl -sL -o verify.apk "https://github.com/O/R/releases/download/v1.0.0/app.apk" \
  -w "HTTP %{http_code} bytes %{size_download}\n"
sha256sum verify.apk ./dist/app.apk     # must match
```

Then check the artifact's specific claims — see
`references/android-apk-release.md` for APK signature/version verification, and
run downloaded binaries rather than trusting `file` alone.

Tag before releasing and pass `--verify-tag` so a release can't silently tag the
wrong commit. Confirm the release version matches the build manifest
(`[workspace.package] version`, `versionName`); these drift independently and a
mismatched tag is a real release defect.

## Reporting

State the URL, asset names and sizes, and what was **verified** (checksums,
signature identity, binary actually running) separately from what was assumed.

Always surface what the user must act on, even mid-session:
- a signing key generated during the session that exists nowhere else
- version skew between components released together
- rewritten history, so other clones now diverge

A verified claim and an inferred one must read differently. If something could
not be verified, say so plainly instead of implying it was checked.

**Label the strength of a fix honestly.** If a defect reproduced only in CI and
your local runs stayed clean, say the local evidence did not reproduce it and
that CI is the authority — do not present a plausible fix as confirmed. If you
verified a regression test by reverting the fix and watching it fail, that is
strong evidence and worth stating as such. Distinguish *verified*, *probable
cause, unconfirmed locally*, and *assumed*.

**Never report a check as passed when it errored, was skipped, or never ran.**
Say which check did not run and why.

## Answering "what is next?"

When the user asks what to do next and there is a clear highest-priority item
with the evidence already gathered, **do that item** rather than returning a
ranked list. A repeated question is not a request for a re-brief; it is a signal
that the previous answer was not an action.

**The second identical ask is the deadline.** The first one may deserve an
answer. If the user asks the same thing again having received a list, the list
was the wrong output — stop explaining and start the top item. Answering the
same question three times is not thoroughness; it is refusing to act.

### Acting beats asking for permission on the same thing twice

Once you have named the top item and the user has asked again, asking "shall I
do X?" a second time is the same mistake one level up: you have the answer and
are spending a turn on ceremony. If the work needs no credentials, no scope
decision, and no irreversible action, treat the repeat as consent and start.

Reserve a question for work that genuinely cannot proceed without the user:
credentials only they hold, a managed signing key, or a scope trade-off between
options they must weigh. Ask for exactly that, in one short paragraph. Do not
pad it with a re-ranked list of items already agreed.

### Say the answer, then do the work, in that order

Do not withhold the judgement. Give the ranked answer in a sentence or two, then
begin the top item in the same turn. The user gets the reasoning *and* the
progress, and a wrong premise can still be corrected before much is built on it.

### When you have drained the work you can do alone, say so

Repeatedly inventing adjacent tasks to avoid saying "this needs you" is its own
failure. If everything remaining needs credentials, a managed key, or a scope
decision, name that plainly and stop. Distinguish *nothing left to do* from
*nothing left that I can do unaided* — the second is a real and useful status,
and padding it with speculative work helps nobody.

### Separate "complete" from "not lying"

Report counts and verdicts with their scope attached. "Every declared setting has
a consumer" means nothing is lying to the user; it does not mean the feature is
finished. State the remaining gaps in the same breath — no bundled sound files, a
permission prompt not yet requested, sprites not drawn — because a bare
completeness number reads as "done" and gets acted on.

### Verify the premise of your own recommendation first

Before recommending work, check that the gap is real. A recommendation built on
an unverified premise sends the user to build something that already exists, and
costs more than checking would have.

Re-read the code for the specific claim rather than carrying forward a summary
from earlier in the session or from your own prior message. Stated confidently
and wrong, a wrong premise is worse than an admitted uncertainty — the user acts
on it. When a check contradicts something you asserted earlier, say so plainly
and immediately, and correct the record before proceeding.

Ask "what did I assert, and have I read the code since?" for every item in a
recommended list.

## A green suite is not proof the artifact works

A release can pass every gate and still be broken on the user's machine. Cheap
test tiers miss whole classes of defect:

| Defect class | Tier that can catch it |
|---|---|
| Plain logic, parsing, data transforms | Unit / JVM tests |
| Concurrency, resource lifetime, native crashes | Stress at high thread counts, then CI |
| UI composition, layout, lifecycle, rendering | Instrumented tests on device/emulator |
| Anything the user touches | A real device, real install |

When a whole unit suite is green and the app still misbehaves on hardware, the
gap is the **tier**, not the tests. Install the built artifact on a real device,
drive it, and read the crash log — then add the missing test tier to CI so the
class cannot ship again. See `references/device-verification-and-test-tiers.md`.

## A settings screen that stores and nothing reads is the same class of bug

A UI control that renders, saves and persists, while no code ever reads the
value, passes every gate in this document and is still a lie the user has to
discover. Before shipping any settings, agent-profile or control surface, audit
declared-versus-consumed, and prove the value on the wire rather than in the UI.
See `references/declared-vs-consumed.md`.

## References

- `references/android-apk-release.md` — APK signing, JDK/AGP version matrix,
  verifying a built APK, and recovering from wrapper/SDK misconfiguration.
- `references/release-preflight-checklist.md` — condensed pre-push audit
  commands and the exact verification steps per artifact type.
- `references/ci-signing-and-silent-skips.md` — CI jobs that go green without
  doing their work: skipped signing, self-excluding path filters, actions that
  ignore `working-directory`, lost exec bits, impossible matrix entries.
- `references/device-verification-and-test-tiers.md` — installing and driving a
  real device, reading crash logs, and which test tier catches which bug class.
- `references/declared-vs-consumed.md` — auditing a settings or control surface
  for values nothing reads, proving it on the wire, and gating it in CI.