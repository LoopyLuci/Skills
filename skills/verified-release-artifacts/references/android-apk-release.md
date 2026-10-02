# Android APK release: signing, toolchain, verification

Depth for the Android half of cutting a release. Every item here is a state that
looks healthy and produces a broken APK.

## JDK / AGP compatibility matrix

The Android Gradle Plugin pins the JDK it works with. Running a newer JDK fails
in `JdkImageTransform`, where `jlink` exits non-zero **with no diagnostic** — the
error names `jlink.exe` but prints nothing actionable.

| AGP | Use JDK | Wrong JDK symptom |
|-----|---------|-------------------|
| 8.2.x | **17** | JDK 21: `Execution failed for JdkImageTransform` / `jlink` exit 1, silent |
| 8.2.x | 17 | JDK 25: fails even earlier, in Gradle script/plugin resolution |

There is no diagnostic to iterate on here — check the AGP version against your
JDK before debugging anything else. Prefer downloading a JDK 17 over trying to
upgrade AGP, since the upgrade drags in a Gradle/Compose/Kotlin matrix change.

```bash
curl -sL -o jdk17.zip \
  "https://api.adoptium.net/v3/binary/latest/17/ga/windows/x64/jdk/hotspot/normal/eclipse"
unzip -q jdk17.zip -d <toolchain-dir>
export JAVA_HOME='C:\path\to\jdk-17'   # Windows-style, see apksigner note
```

**Document the JDK requirement in the README and pin it in CI** with a comment
explaining why, or the next session re-derives this from scratch.

## A corrupt gradle-wrapper.jar blocks everything

Symptom: `ClassNotFoundException: org.gradle.wrapper.GradleWrapperMain`.

A wrapper JAR saved over a browser download page (a GitHub HTML error page) has
the right size and the right filename but is not a ZIP. Check the magic bytes:

```bash
head -c 4 gradle/wrapper/gradle-wrapper.jar | xxd   # must be 504b = "PK"
file gradle/wrapper/gradle-wrapper.jar
```

Regenerate a real one from any locally cached Gradle distribution — this needs
no network for the wrapper itself:

```bash
export JAVA_HOME='C:\path\to\jdk-17'
G="C:/Users/<you>/.gradle/wrapper/dists/gradle-<ver>-bin/<hash>/gradle-<ver>"
"$JAVA_HOME/bin/java" -cp "$G/lib/gradle-launcher-<ver>.jar" \
  org.gradle.launcher.GradleMain wrapper --gradle-version <ver> --distribution-type bin
```

List candidates with `ls ~/.gradle/wrapper/dists`. A regenerated JAR is ~43 KB;
a several-hundred-KB "JAR" is suspicious.

## SDK path must be git-ignored

`local.properties` holds an absolute SDK path. It is machine-specific and often
points at a profile that does not exist on the current host (e.g. a different
Windows user name baked in at authoring time). Fix it locally and never commit
it:

```properties
sdk.dir=C:/Users/<you>/AppData/Local/Android/Sdk
```

Add `local.properties` and `keystore.properties` to `.gitignore`.

## Release signing: an unsigned APK is uninstallable

`assembleRelease` with no signing config emits `app-release-unsigned.apk`. It
builds cleanly and looks like success, but no user can install it.

Wire signing so it reads a git-ignored properties file or env vars, and warns
when absent:

```kotlin
import java.util.Properties   // explicit import: bare `java` resolves to Gradle's
                              // java extension inside the DSL and fails to compile

signingConfigs {
    create("release") {
        val props = Properties()
        val f = rootProject.file("keystore.properties")
        if (f.exists()) f.inputStream().use { props.load(it) }
        val storePath = props.getProperty("storeFile")
            ?: System.getenv("SCREENBUDDY_KEYSTORE")
        // Resolve against the ROOT project: file() inside a subproject module
        // resolves to that module's dir, so a root-relative path looks absent
        // and the build silently falls back to the debug key.
        val store = storePath?.let { p ->
            val direct = file(p)
            if (direct.exists()) direct else rootProject.file(p)
        }
        if (store != null && store.exists()) {
            storeFile = store
            storePassword = props.getProperty("storePassword")
                ?: System.getenv("SCREENBUDDY_STORE_PASSWORD")
            keyAlias = props.getProperty("keyAlias") ?: "screenbuddy"
            keyPassword = props.getProperty("keyPassword")
                ?: System.getenv("SCREENBUDDY_KEY_PASSWORD")
        }
    }
}

buildTypes {
    release {
        val rel = signingConfigs.getByName("release")
        signingConfig = if (rel.storeFile != null) rel else {
            logger.warn("No release keystore configured; signing with the debug key.")
            signingConfigs.getByName("debug")
        }
    }
}
```

Two silent-failure traps, both producing an installable-but-wrong artifact:
- `file(path)` inside the `app` module resolves to `app/`, not the root.
- `storeFile` is non-null even when unset, so test existence explicitly.

Generate a key:

```bash
keytool -genkeypair -v -keystore app-release.jks -alias screenbuddy \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -dname "CN=ScreenBuddy, O=ScreenBuddy, C=US"
```

R8/minification (`isMinifyEnabled = true`) can break Room, Retrofit, and Gson
reflective use. If release builds crash where debug works, add keep rules to
`proguard-rules.pro` before suspecting the signing setup.

## Verify the built APK

```bash
apksigner verify --verbose --print-certs app-release.apk
aapt2 dump badging app-release.apk | head -5
```

**Read the certificate DN.** `CN=Android Debug` on a release artifact means the
signing config fell back — the APK still installs, so no build step flags it.
Expect the project's own DN (e.g. `CN=ScreenBuddy`).

`aapt2 dump badging` confirms package name, `versionName`, minSdk, targetSdk —
cross-check these against the release tag.

`apksigner` and `aapt2` are `.bat` wrappers and require `JAVA_HOME` as a
**Windows-style** path (`C:\...`). An MSYS path (`/c/...`) aborts with
"JAVA_HOME is set to an invalid directory", which reads like a missing JDK but
is a path-format problem.

## Version alignment

`versionName` in `defaultConfig` and the release tag drift independently. The
APK being `1.0.0` while the desktop binary is `0.1.0` is a real release defect
even when both build fine — surface it rather than silently picking one.