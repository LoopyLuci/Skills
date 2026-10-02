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
5. Tag.
6. Create the release with assets.
7. **Download the assets back and verify each one.**
8. Report URLs, sizes, and what was verified vs. assumed.

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

## References

- `references/android-apk-release.md` — APK signing, JDK/AGP version matrix,
  verifying a built APK, and recovering from wrapper/SDK misconfiguration.
- `references/release-preflight-checklist.md` — condensed pre-push audit
  commands and the exact verification steps per artifact type.