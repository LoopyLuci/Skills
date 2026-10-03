# Release preflight checklist

Condensed audit and verification steps. Run the pre-push audit before the first
push; run the verification block after creating the release.

## Pre-push audit

### 1. Oversized blobs anywhere in history

```bash
git rev-list --objects --all \
  | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
  | awk '$1=="blob" && $3>50000000 {print $3/1024/1024" MB "$4}' | sort -u
```

Anything listed will be rejected (100 MB limit). Untracking is not enough — the
blob stays in history. Rewrite with `git-filter-repo`, confirm nothing was pushed
first (`git ls-remote origin` empty), and re-add `origin` afterward because
filter-repo deletes it.

### 2. Secrets and build output in the index

```bash
git ls-files | grep -iE '\.jks$|\.keystore$|keystore\.properties|local\.properties|\.apk$|\.exe$'
```

Expect no output. Build dirs committed by a careless initial commit:

```bash
git ls-files | grep -cE '(^|/)(build|target|\.gradle)/'   # count them first
git rm -r --cached --quiet <build-dir>
```

### 3. Staged additions vs deletions

Distinguish intent before committing:

```bash
git add -A
git diff --cached --diff-filter=A --name-only | grep -iE '\.exe$|\.apk$|\.jks$|\.properties$'
git diff --cached --diff-filter=D --name-only | wc -l
```

### 4. Branch and gates

```bash
git branch -m master main     # if CI triggers on main
gh workflow list              # expect: active
```

### 5. Confirm gates ran against the artifact you are shipping

A green run before a rebuild proves the *previous* binary. Probes and tests that
launch a built executable resolve a path, and if both `debug` and `release`
exist the wrong one may be picked — so a handler added since the last
`--release` build looks like it never ran. Confirm the timestamp order, or
delete the stale artifact before running the probes:

```bash
ls -la --time-style=+%s target/release/app.exe target/debug/app.exe   # newest first wins
```

Rebuild `--release` *before* the final probe run, not just before packing, so the
live probe exercises the exact bytes that get uploaded.

## Post-release verification

### Confirm what exists

```bash
gh release view v0.1.0 --json tagName,name,isDraft,isPrerelease,assets,url
gh repo view OWNER/REPO --json defaultBranchRef,visibility
git ls-remote --heads --tags origin
```

### Download each asset back and compare checksums

```bash
curl -sL -o verify.bin "https://github.com/OWNER/REPO/releases/download/v0.1.0/ASSET" \
  -w "HTTP %{http_code} bytes %{size_download}\n"
sha256sum verify.bin ./dist/ASSET      # must match
```

A non-200 or a size mismatch means the upload is truncated or absent.

### Shipping one checksums file for a multi-asset release

When a release carries several artifacts, publish a `checksums.txt` next to them
(`sha256sum asset1 asset2 > checksums.txt`) and verify with one command:

```bash
gh release download vX.Y.Z -p '*.exe' -p '*.apk' -p '*checksums.txt'
sha256sum -c *checksums.txt          # expect every listed file: OK
```

Downloading assets with **selective `-p` patterns** is the trap here:
`sha256sum -c` reads every line of the file, so an entry you did not download
reports `FAILED open or read`. That reads like a corrupt published artifact when
it only means the file is absent from the directory. Download the whole set, or
grep the checksum file down to the names you actually fetched, before drawing any
conclusion about upload integrity.

### Artifact-specific verification

| Artifact | Command | What must hold |
|---|---|---|
| Android APK | `apksigner verify --print-certs A.apk` | Verifies; DN is the project's, not `CN=Android Debug` |
| Android APK | `aapt2 dump badging A.apk` | package, versionName, minSdk, targetSdk match the tag |
| Windows EXE | `file A.exe` | `PE32+ executable ... x86-64` |
| Windows EXE | run it | reaches steady state without crashing |
| Archive | extract | payload intact, not just the container |
| Native lib | `--print-certs` / ELF header | ABI and arch match the release target |

### Housekeeping

```bash
rm -f verify.bin        # remove temp verification copies
git status --short      # working tree clean, nothing unintended left
```

## Report template

State plainly:

- repo URL, default branch, visibility
- release URL, tag, draft/prerelease state
- each asset: name, size, **and what was verified about it**
- anything the user must act on: unrecoverable signing key, version skew
  between components, rewritten history diverging other clones

Keep "verified" and "assumed" visibly distinct. If a check could not run, say
which one and why rather than letting it read as passed.