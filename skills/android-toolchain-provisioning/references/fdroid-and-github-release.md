# Shipping an Android app to GitHub and F-Droid

F-Droid's inclusion policy forbids non-free dependencies. If your app uses Google Cast,
Firebase, Play Billing, Maps or ML Kit, that is the blocker — everything else is
paperwork. This is the product-flavor split that solves it without forking.

## Find the blockers first

```python
for f in glob.glob("**/build.gradle.kts", recursive=True):
    for m in re.finditer(r"^\s*(?:api|implementation)\((libs\.[\w.]+|\"[^\"]+\")\)", src, re.M):
        if re.search(r"cast|play.?services|gms|firebase|billing|mlkit", m.group(1), re.I):
            print(f, m.group(1))
```

## The flavor split

Two flavors on one dimension. Only the module with proprietary code needs per-flavor
SOURCE, but **every** library module needs the dimension declared or variant resolution
fails.

```kotlin
// app/build.gradle.kts
flavorDimensions += "distribution"
productFlavors {
    create("foss") { dimension = "distribution"; versionNameSuffix = "-foss" }
    create("full") { dimension = "distribution" }
}
```

```kotlin
// The proprietary dep is flavor-scoped — never plain implementation(...)
"fullImplementation"(libs.play.services.cast.framework)
```

Layout in the affected module:

```
src/main/…/CastStreamer.kt              interface + NoOpCastStreamer
src/full/…/cast/CastAudioStreamer.kt    real SDK implementation
src/foss/…/di/CastBindingModule.kt      binds the no-op
src/full/…/di/CastBindingModule.kt      binds the real one
app/src/full/AndroidManifest.xml        SDK meta-data (OPTIONS_PROVIDER etc.)
```

Same fully-qualified class name in both flavor source sets, different bodies. Everything
above the interface stays flavor-agnostic — `StreamingCoordinator` injects `CastStreamer`,
not `CastAudioStreamer`.

### Pitfall: the dimension must exist everywhere

A flavorless module consuming a flavored dependency fails with:

```
cannot choose between fossDebugRuntimeElements / fullDebugRuntimeElements
```

The tempting fix is `missingDimensionStrategy("distribution", "full", "foss")` — **do not
use it here.** It pins flavorless consumers to the `full` variant, so the FOSS app links
the Play-Services-carrying library and the whole exercise is defeated. Declare the
dimension in the library convention plugin instead, so all modules follow the app:

```kotlin
// AndroidLibraryConventionPlugin
flavorDimensions += "distribution"
productFlavors {
    create("foss") { dimension = "distribution" }
    create("full") { dimension = "distribution" }
}
```

### Pitfall: manifest entries for absent classes

An SDK `meta-data` block pointing at a class that isn't in the FOSS build is a latent
crash and a policy problem. Move it to `app/src/full/AndroidManifest.xml`; AGP merges it
per flavor.

### Make the no-op honest

Return a reason, don't silently do nothing:

```kotlin
override val unavailableReason =
    "Chromecast needs Google Play Services, which this build omits. " +
    "Use the GitHub release, or stream to an AirPlay speaker."
```

## Verify purity — in CI, not by eye

Config review is not proof; a transitive dependency can reintroduce the SDK. Check the
compiled dex:

```bash
./gradlew :app:assembleFossRelease
unzip -p app/build/outputs/apk/foss/release/*.apk classes.dex > /tmp/c.dex
grep -c 'com/google/android/gms' /tmp/c.dex     # MUST be 0
```

Real numbers from this project: full build 4,206 refs → FOSS build **0**.

Note: `grep -c` on a binary exits 1 with no matches, so `$(grep -c … || echo 0)` emits
`"0\n0"` and breaks `[ "$x" -eq 0 ]`. Use `tr -c '[:print:]' '\n' < dex | grep -c …`.

## F-Droid must build from source, unsigned

Signing config has to degrade gracefully when `keystore.properties` is absent, or
F-Droid's build fails:

```kotlin
val hasSigningConfig = keystoreProperties.containsKey("storeFile")
release { if (hasSigningConfig) signingConfig = signingConfigs.getByName("release") }
```

Test it the way F-Droid will:

```bash
mv keystore.properties keystore.properties.bak
./gradlew :app:assembleFossRelease     # must succeed, output is *-unsigned.apk
mv keystore.properties.bak keystore.properties
```

## Metadata layout

```
fastlane/metadata/android/en-US/
├── short_description.txt      ≤ 80 chars
├── full_description.txt       supports <b>, <i>, <ul>
├── changelogs/1.txt           filename == versionCode
├── icon.png                   512×512
└── phoneScreenshots/          2+ real device PNGs
```

Build recipe goes to `fdroiddata` as `metadata/<applicationId>.yml`:

```yaml
Builds:
  - versionName: 1.0.0-foss
    versionCode: 1
    commit: v1.0.0
    subdir: app
    gradle:
      - foss          # the FLAVOR name
UpdateCheckMode: Tags ^v[0-9.]+$
```

## Audit permissions before submitting

Read them from the manifest — do not write the table from memory:

```python
perms = sorted(set(re.findall(r'android:name="android\.permission\.([A-Z_]+)"', manifest)))
```

This project declared **20**, not the 8 I first assumed. Two drew scrutiny:

- **Signature-level permissions** (e.g. `BLUETOOTH_PRIVILEGED`) can never be granted to a
  normal app. Justify or remove — reviewers ask.
- **`READ_PHONE_STATE`** looks invasive and is usually unnecessary: audio focus and
  `AudioManager.mode` give you call state without it.

## GitHub side

- `LICENSE` at the root (F-Droid checks it too).
- CI must build **both** flavors — a change that only compiles with the proprietary SDK
  present breaks F-Droid silently — plus the dex purity check.
- Release job: keystore from base64 repo secrets, write `keystore.properties`, build,
  `sha256sum`, upload, then `rm -rf` the credentials in an `if: always()` step.
- Issue template asking for the diagnostic log export turns "doesn't work on my phone"
  into something fixable. A device-compatibility template is worth having when platform
  behaviour varies by OEM.
