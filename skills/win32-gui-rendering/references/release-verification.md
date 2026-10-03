# Shipping a release and proving the artifact

A green build proves the code compiles. It does not prove the published artifact
is the one you tested, is signed, or runs.

## Order

1. **Run every gate against the release binary, not a debug build.** Probes that
   pick the newest binary by mtime will do this for you once you `cargo build
   --release` last — check that ordering explicitly rather than assuming it.
2. **Stage assets and checksums together.** One `sha256sum *.exe *.apk >
   <tag>-checksums.txt` in the asset directory, so the checksum file cannot
   drift from the files it describes.
3. **Commit the version bump, then tag that commit.** A tag pointing at an
   untagged version bump publishes a release whose source is not the tag.
4. **Confirm no secret is tracked** before publishing:
   `git ls-files | grep -iE 'keystore|\.jks|\.env$'` must come back empty. Build
   signing material at a git-ignored path and confirm with `git check-ignore -v`
   rather than trusting the ignore rule.
5. **Download the published artifacts back** and verify those bytes:
   ```bash
   gh release download <tag> --repo <owner>/<repo>
   sha256sum -c <tag>-checksums.txt
   ```
6. **Run the downloaded binary.** This is the check that catches a wrong-tag or
   stale-asset mistake, and it costs one command.

## Android signing

- Keep the key at a git-ignored path beside its `keystore.properties`, which is
  where the Gradle config resolves both from.
- `apksigner.bat` needs a **native Windows** `JAVA_HOME` (`C:\...`); an MSYS
  `/c/...` path fails.
- A debug-signed release is the silent failure to defend against — `assembleRelease`
  falls back to the debug key and still succeeds. Always read the certificate DN
  and SHA-256 back and compare with the expected release key:
  ```bash
  "$ANDROID_HOME/build-tools/36.0.0/apksigner.bat" verify --print-certs app-release.apk
  ```
  The same SHA-256 across releases is the evidence the *same* key signed them.
- In CI, missing signing secrets must **fail the job**. Accepting a debug-signed
  or absent artifact turns a release pipeline into a warning generator.

## Release notes: state what is still broken

The notes are read by people deciding whether to install, so the limitations
section is load-bearing, not a disclaimer. Include:

- the headline defect this release fixes, stated plainly (not a feature list)
- what is verified and how (test count, which probes ran against which binary)
- what remains inert or unimplemented, **with the reason** — a setting that
  cannot be wired should say why in the notes too, or a reader assumes it was
  forgotten
- platform scope, so nobody installs a Windows-only binary expecting a Mac build

Correct the previous release's notes in the new ones when they were wrong. A
release that quietly drops an earlier overstatement leaves the reader with a
belief that was never true.

## When a release is due

Unreleased work compounds: each session adds to a pile nobody can review. Cut a
release when a coherent unit of work is verified, not when the next idea arrives.
State plainly what is and is not in it rather than letting the gap grow.