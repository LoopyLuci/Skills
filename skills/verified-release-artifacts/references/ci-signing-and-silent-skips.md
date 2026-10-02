# CI that reports success without doing the work

A CI job that **exits 0 when it cannot do its job** is worse than a red job: it
converts a missing prerequisite into a green checkmark, and every downstream
consumer trusts it. Audit release workflows for this before trusting any green
build.

## The silent skip

The classic shape:

```yaml
- name: Restore signing key
  run: |
    if [ -z "$KEYSTORE_B64" ]; then
      echo "::warning::No signing key configured; skipping."
      exit 0          # <-- the job now succeeds having produced nothing
    fi
```

This job went green while emitting no signed artifact. Confirm by reading the
log for the skip message, not the conclusion field:

```bash
gh run view <run-id> --log | grep -iE "skipping|no .* configured|::warning::"
```

Two fixes, both required:

1. **Fail instead of skipping.** `exit 1` and name the secrets to set. A job whose
   whole purpose is producing a signed artifact has no valid skip path.
2. **Verify the output, not the exit code.** Add a step that locates the tool and
   checks the artifact's actual property:

```yaml
- name: Verify the APK is signed by the release key
  run: |
    APK=$(ls app/build/outputs/apk/release/*.apk | head -1)
    test -f "$APK" || { echo "::error::No release APK produced"; exit 1; }
    APKSIGNER=$(ls -d "${ANDROID_HOME:-$ANDROID_SDK_ROOT}"/build-tools/*/apksigner \
                2>/dev/null | sort -V | tail -1)
    [ -n "$APKSIGNER" ] || { echo "::error::apksigner not found"; exit 1; }
    "$APKSIGNER" verify --print-certs "$APK" > verify.txt 2>&1 \
      || { echo "::error::signature did not verify"; cat verify.txt; exit 1; }
    # Catches the silent fallback to the debug key.
    if grep -q "Android Debug" verify.txt; then
      echo "::error::APK is debug-signed, not release-signed"; exit 1
    fi
    grep -E "certificate DN|SHA-256 digest" verify.txt
```

Locate `apksigner` by globbing `build-tools/*/` rather than hardcoding a version,
and fall back across `$ANDROID_HOME` / `$ANDROID_SDK_ROOT` — neither is reliably
set in every runner.

## Providing the secrets

Set them via stdin so values never reach shell history or logs:

```bash
gh secret set SCREENBUDDY_KEYSTORE_B64 --repo OWNER/REPO < keystore.b64
gh secret list --repo OWNER/REPO        # confirm names, never values
```

Verify the stored payload actually restores the key before trusting CI — decode
the base64 and open it with `keytool`, comparing the certificate SHA-256. Then
delete any plaintext scratch copy holding the secrets.

## Workflow triggers that hide their own breakage

A `paths:` filter that does not include the workflow's own file means **editing
the workflow never runs it**, so a broken edit sits unnoticed until an unrelated
change happens to match.

```yaml
on:
  push:
    paths:
      - 'ScreenBuddy-Android/**'
      - '.github/workflows/android.yml'   # <-- required
```

## Actions that ignore the job's working-directory

`reactivecircus/android-emulator-runner` runs its `script:` from the repository
root, not the job's `defaults.run.working-directory`. A relative `./gradlew` fails
with `sh: 1: ./gradlew: not found`. Put the directory in the script itself:

```yaml
script: cd ScreenBuddy-Android && ./gradlew connectedDebugAndroidTest
```

## Exec bit lost on Windows

`gradlew` committed as mode `100644` makes every `./gradlew` step die with exit
126 before Gradle starts, while local runs pass because Windows ignores the bit.

```bash
git update-index --chmod=+x ScreenBuddy-Android/gradlew
```

## A matrix entry that cannot possibly pass

If the app is platform-specific (Win32/Direct2D, Cocoa, …), a cross-platform
release matrix is guaranteed red. Replace the impossible entry with a real check
of whatever *is* portable — the core/library crate with `--all-targets` — which
also catches cfg-gating mistakes a single-platform build cannot surface. Do not
delete the job and do not fake it.
