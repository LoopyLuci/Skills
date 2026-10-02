---
name: windows-rust-android-build-env
description: Fix odd Rust/Android build failures on this Windows host.
---

# Windows build-environment repairs (this host)

Three failure modes here look like project bugs but are broken local installs.
Diagnose before editing any code.

Triggers: `rustdoc.exe ... not applicable`, `JdkImageTransform` failures,
`ClassNotFoundException: GradleWrapperMain` despite the wrapper jar existing.

## 1. `cargo test` fails on the doctest step

Symptom: `the 'rustdoc.exe' binary ... is not applicable to the
stable-x86_64-pc-windows-msvc toolchain`. The toolchain has only `rustdoc.pdb`,
no `rustdoc.exe`.

- `rustup component add rustdoc` **fails** (component not available for the target).
- `rustup update stable` **rolls back** with
  `failure removing component 'rustc-...', directory does not exist: bin\rustdoc.exe`
  — that message is the confirmation, not a red herring.

Fix:

```bash
rustup toolchain uninstall stable
rustup toolchain install stable --profile default
```

Check: `ls "$(rustc --print sysroot)/bin" | grep rustdoc` must show `rustdoc.exe`.

Side effect: swapping the toolchain mid-build can produce
`linking with link.exe failed: exit code: 1181`. That is a stale artifact — just
rebuild; it is not a code error.

## 2. Android build fails in JdkImageTransform

Symptom: `Failed to transform core-for-system-modules.jar` /
`Execution failed for JdkImageTransform`, with `jlink.exe` exiting 1 and **no
diagnostic**.

AGP 8.2.0 is built and tested against **JDK 17**. JDK 21 triggers this; JDK 25
is rejected outright (`25.0.2` as the whole error message). Install a 17 JDK and
pin it:

```bash
JAVA_HOME=/c/Users/Server/soniccore-toolchain/jdk-17.0.20.1+1 ./gradlew assembleRelease
```

Pin `java-version: '17'` in CI with a comment, or the next person will "upgrade"
it and rediscover this.

## 3. `gradle-wrapper.jar` is not a JAR

Symptom: `ClassNotFoundException: org.gradle.wrapper.GradleWrapperMain`, while the
file exists and is the right size.

Check the magic bytes — it must start with `PK` (0x50 0x4b). A saved HTML error
page (starts with `<!DOCTYPE html>`) is the usual culprit; someone saved a
download page over it.

Regenerate from any cached distribution rather than re-downloading:

```bash
G=/c/Users/Server/.gradle/wrapper/dists/gradle-8.11.1-bin/*/gradle-8.11.1
"$JAVA_HOME/bin/java" -cp "$G/lib/gradle-launcher-8.11.1.jar" \
  org.gradle.launcher.GradleMain wrapper --gradle-version 8.11.1 --distribution-type bin
```

Cached dists live under `~/.gradle/wrapper/dists/`. `gradle` is not on PATH here.

## Android SDK paths

`~/AppData/Local/Android/Sdk` is the real SDK. `local.properties` is git-ignored;
if it points elsewhere, nothing builds. Required env for any Gradle command:

```bash
export ANDROID_HOME="$HOME/AppData/Local/Android/Sdk"
export ANDROID_SDK_ROOT="$ANDROID_HOME"
```

Verify an APK rather than trusting the build:

```bash
"$ANDROID_HOME/build-tools/36.0.0/apksigner.bat" verify --print-certs app.apk
```

The `.bat` needs a **native Windows** `JAVA_HOME` (`C:\...`); an MSYS `/c/...` path
fails with "JAVA_HOME is set to an invalid directory".

## 4. Verifying an IPC/control surface that only exists at runtime

Compiling clean proves nothing here. ScreenBuddy's control server compiled for
weeks while being dead code: never started, and its two sides held separate
handles so every query returned defaults forever.

Checklist when wiring one of these:

- **Start the process for real**, then probe it over the wire. Two suites are
  worth having: one at the protocol level and one at the adapter level (e.g. MCP).
- **Prove a mutation actually mutated.** `{"queued": true}` only proves the
  request was accepted. Read the state back and assert the value changed, then
  restore it.
- **Watch for overwrite ordering.** A render/simulation loop that runs *after*
  your handler will undo it. Move the drain earlier, or pin the value.
- **Ensure both sides share one handle.** Two `Arc<Mutex<State>>` that look
  related but are constructed separately read as permanent defaults with no
  error. Make the API force a single instance, e.g.
  `Server::with_status(config, status.clone())`.
- **`tokio::spawn` panics outside a runtime.** A plain `fn main` has no reactor;
  build a `Runtime` and run it on a dedicated thread.
- **Suspect the shared-state bug before the loop.** If frames tick but the
  snapshot stays at zero, the loop is fine and the publisher is writing to a
  different object.

## Kotlin/Android testing on the JVM

`androidx.test.core`'s `ApplicationProvider` needs a registered instrumentation,
which fails in plain JVM unit tests with "No instrumentation registered!". Either
add Robolectric, or — cheaper here — write fakes implementing the DAO interfaces
and test the repository against those. Keep in-memory Room for instrumented
tests under `src/androidTest`.