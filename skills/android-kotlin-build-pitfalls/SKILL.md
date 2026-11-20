---
name: android-kotlin-build-pitfalls
description: Use when gradlew Kotlin compilation fails.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [android, kotlin, hilt, build-pitfalls]
    category: software-development
    related_skills: [android-toolchain-provisioning]
---

# Android/Kotlin Build Pitfalls

## Trigger

Use when `./gradlew assembleDebug` or `./gradlew compileDebugKotlin` fails with Kotlin compilation errors, or when adding new UI screens and AI SDK components.

## Procedure

### Kotlin language gotchas

1. `when (value) { is Enum.ENTRY -> ... }` is a compile error
   - The `is` keyword is for type checking, not enum entry matching
   - Fix: use `value == Enum.ENTRY` instead

2. Enum properties named `name` shadow `Enum.name` and cause compile errors
   - Fix: rename the property to `taxName` (or any non-reserved name)
   - Pattern: `enum class TaxType(code: String, taxName: String, ...)`

3. Box `contentAlignment` is not a valid parameter
   - Fix: Use nested Box with explicit sizing

### Activity result API

1. `rememberLauncherForActivityResult` requires three dependencies:
   - `androidx.activity:activity-compose:1.7.2`
   - `androidx.activity:activity:1.7.2`
   - `androidx.activity:activity-ktx:1.7.2`

### Hilt DI for new repositories

1. Add `@Provides` methods to `app/src/main/java/com/spendingsaver/di/AppModule.kt`
2. `@ApplicationContext` qualifier is REQUIRED for `Context` injection in `@Provides` methods

## Build commands

```bash
cd SpendingSaverAndroid
./gradlew clean assembleDebug --console=plain --no-daemon
```

Run `./gradlew clean` first if a compile error persists after fixing source.

## Project build & CI environment

### Gradle build path
- System Gradle 8.2 at /tmp/gradle-8.2/gradle-8.2 is the reliable build path for this project.
- Fallback only: use ./gradlew if the Hermes wrapper gradlew works (distributionUrl=https://services.gradle.org/distributions/gradle-8.2-bin.zip); the wrapper jar was missing/corrupted and had CRLF issues.
- CI uses $GRADLE_CMD (system Gradle) instead of ./gradlew.

### Gradle memory
- GRADLE_OPTS must supply ONLY JVM memory options (e.g. -Xmx4096m -XX:MaxMetaspaceSize=512m), never CLI flags like -x/-no-daemon.
- org.gradle.jvmargs=-Xmax4096m in gradle.properties.
- Verify $JAVA_HOME/bin/java -version first; JAVA_HOME must be a valid JDK install dir (not /).

### CI/CD pipeline
- Driver: ci/run.sh all|preflight|test|build|verify|report (set -u; sources config.sh + lib.sh).
- Report: ci/reports/summary.txt with Build/Test/Verify/Overall PASSED.
- Run ./ci/run.sh all after any source change; all stages green = CI passed.

## Pitfalls

### Kotlin language

1. **`when (value) { is Enum.ENTRY -> ... }` is a Kotlin compile error**
   - The `is` keyword is for type checking, not enum entry matching
   - Fix: use `value == Enum.ENTRY` instead

2. **Enum property named `name` shadows `Enum.name` and causes compile error**
   - The Kotlin compiler rejects enum classes with a property named `name` because it shadows the `name` member of the `Enum` superinterface
   - Fix: rename the property to `taxName` (or any non-reserved name)
   - Example: `enum class TaxType(code: String, taxName: String, ...)`

3. **Box `contentAlignment` is not a valid parameter**
   - Fix: Use nested Box with explicit sizing

### Activity result API

4. **Activity result API needs ALL three dependencies**
   - `activity-compose`, `activity`, AND `activity-ktx` must all be present
   - Missing any one causes `rememberLauncherForActivityResult` to be unresolved

### Hilt DI

5. **Hilt Context injection requires `@ApplicationContext`**
   - `Context` injected into `@Provides` methods must use `@ApplicationContext`

### Gradle Kotlin DSL script cache

**`metadata.bin` loss after repeated `build.gradle.kts` edits.** When `gradlew <task>` fails with `Could not read workspace metadata from .../kotlin-dsl/scripts/<hash>/metadata.bin`, the kotlin-dsl script plugin's on-disk cache is stale, not the source. Kill the daemon and clear the script cache:

- `./gradlew --stop`
- `rm -rf ~/.gradle/caches/8.7/kotlin-dsl/scripts/<script-hash>/`
- re-run `./gradlew <task>`

Do not fix this by editing more build files; the stale cache, not the source, is the failure.

### Room + KSP + Room DAO

6. **Room DAO must be in the same package as its `@Database` class**
   - When a `@Dao` interface is in a separate package (e.g., `com.spendingsaver.tax`) from its `@Database` class, KSP validates the DAO queries against the main app's `AppDatabase` schema instead of the correct `@Database` class
   - Result: `SQLITE_ERROR: no such table: tax_detail` despite the `@Database` annotations being correct
   - Fix: (a) move the DAO into the main app's `com.spendingsaver.data` package, or (b) create a separate Android library module for the feature, or (c) move BOTH the DAO AND the @Database class into the same package as the entity types
   - Detection: `./gradlew assembleDebug` fails with `SQLITE_ERROR: no such table` and `[ksp] MissingType` errors
   - Alternative: use a dedicated module with its own `build.gradle.kts` and `settings.gradle.kts`

7. **KSP generates `insertAll(List<T>)` with a `$completion: Continuation<Unit>` parameter**
   - When a DAO declares `insertAll(List<T>)`, KSP generates `insertAll(List<T>, Continuation<Unit>)` in the implementation class
   - This causes `Conflicting declarations` or `Type mismatch` errors because the source interface declares a different signature
   - Fix: Remove `insertAll(List<T>)` methods from the DAO; use individual `insert(item)` calls instead
   - In the Repository, only define `insert(item)` methods; do NOT redefine `insertAll` in the Repository

8. **Orphaned annotations cause KSP validation errors**
   - If a method is deleted from a DAO but its `@Insert`/`@Query` annotation is left behind, KSP fails with `An abstract DAO method must be annotated with one and only one of the following annotations`
   - Fix: After deleting a method, also delete the corresponding annotation line

9. **`Flow<List<T>>` in suspend functions needs `collect` or `toList()`**
   - Calling `.first()` or `.toList()` directly on a `Flow<List<T>>` receiver in a suspend function causes `Unresolved reference` or receiver type mismatch errors
   - Fix: Use `collect { list.addAll(it) }` inside a suspend function to accumulate values into a local list
   - Alternative: Materialize the flow upstream (e.g., `@Query` returning `List<T>` directly instead of `Flow<List<T>>`)

10. **KSP cache invalidation**
   - After any DAO or `@Database` edit, always run `./gradlew clean` to remove stale KSP and intermediate artifacts
   - The `clean` task deletes the `build/` directory, which contains KSP-generated stubs and cached annotations
   - Incremental builds DO NOT clear the KSP cache between builds

### Hilt & dependency injection

11. **Hilt version alignment**: Hilt 2.51.1 requires KSP (not kapt) — `com.google.devtools.ksp` must be applied with `ksp` for `hilt-compiler`. Correct import is `import dagger.hilt.InstallIn` (NOT `dagger.hilt.components.InstallIn`). Detected when KAPT/KSP mixes cause: `@InstallIn` cannot resolve symbols, or `dagger.hilt.compile-only-searcher is not a recognized Hilt option`.

12. **Dagger duplicate bindings**: If two `@Module` objects provide the same type via `@Provides @Singleton`, Dagger fails with `Dagger/DuplicateBindings`. Fix: remove the duplicate `@Provides` method from one of the modules (usually AppModule) and inject the provided dependency into every consumer.

### Kotlin 1.8.22 compiler bug (EnumClassLowering)
13. **Enum classes with default parameters cause compiler crash**: Kotlin 1.8.22's `EnumClassLowering` phase throws `AssertionError: No such value argument slot: N` when compiling enum classes with default parameters and multiple entries. Fix: convert the enum class to a `data class` + `object` for the registry:
   - `enum class AiStatus` → `data class AiStatus(val label: String, ...)`
   - `object AiCapabilities` → `class AiCapabilities(private val context: Context) { val ALL = listOf(...) }`
   - Do NOT use default parameters on enum entries
   - Detection: `AssertionError: No such value argument slot` during `compileDebugKotlin`

### Kotlin stdlib API changes (2026-11-19)
14. **`MediaType.parse` is an extension function, not a static method**: In OkHttp 4.11.0, `MediaType.parse` is an extension function and cannot be called as `okhttp3.MediaType.parse(...)`. Fix: use `...parse()` as an extension or use the full signature `RequestBody.create(content, null)`.
15. **`RequestBody.create` signature**: All overloads require a `MediaType?` as the first parameter. Detection: `None of the following functions can be called with the arguments supplied`. Fix: pass all parameters explicitly, including the `MediaType?` (even null).

### MSYS paths

12. **MSYS paths do not work with native Windows tools**
   - When calling native Windows binaries from terminal, use forward-slash paths (`C:/path/to/file`), not MSYS paths (`/c/path/to/file`)
   - The `terminal` tool runs through bash (git-bash/MSYS), but native tools like `gradlew` do not accept MSYS paths

13. **Kotlin source file must have `package` declaration**
   - Every Kotlin file must declare a `package` at the top, or the build fails with `Package not found` or `Unresolved reference` errors

14. **Build memory exhaustion**
   - Kotlin compilation can fail with `Insufficient memory` or `malloc failed` for large projects
   - Fix: increase JVM heap in `gradle.properties`: `org.gradle.jvmargs=-Xmx4096m`
   - Also set `GRADLE_OPTS="-Xmx4096m -XX:MaxMetaspaceSize=512m"` in `ci/config.sh`
   - Pattern: `Insufficient memory for the Java Runtime Environment to continue`

### New learnings (2026-11-16 through 2026-11-19) — SpendingSaver session

- **Clean build verification**: After any source change, run `./gradlew clean assembleDebug --console=plain --no-daemon` to catch incremental-build KSP cache staleness
- **Dex merging failures**: `DexArchiveMergerException` is a KSP cache issue; always `./gradlew clean` first
- **Room DAO in separate package**: When a `@Dao` is in a different package from its `@Database`, KSP validates against the main app's schema — result `SQLITE_ERROR: no such table`. Fix: move DAO into the same package as `@Database`, or use a separate Android library module
- **KSP cache invalidation**: After any DAO or `@Database` edit, always run `./gradlew clean` — incremental builds DO NOT clear the KSP cache between builds
- **Kotlin 1.8.22 EnumClassLowering bug**: Converting enum classes with default parameters and multiple entries causes `AssertionError: No such value argument slot` during `compileDebugKotlin`. Fix: convert enum to data class + object registry
- **Hilt 2.51.1 requires KSP**: Hilt 2.51.1 (ksp) needs `com.google.devtools.ksp` applied with `ksp` for `hilt-compiler`. Correct import is `import dagger.hilt.InstallIn` (NOT `dagger.hilt.components.InstallIn`)
- **Dagger duplicate bindings**: Duplicate `@Provides @Singleton` for the same type in different modules causes `Dagger/DuplicateBindings` build failure. Remove the duplicate `@Provides` from one module
- **Room migration**: If schema changes, Room requires a migration; validate before shipping
- **Room 2.5.2 DAO annotations**: `@Upsert`/`@Delete` on DAO methods is not supported. Use `@Insert(onConflict = OnConflictStrategy.REPLACE)` + explicit `@Query("DELETE FROM ...")` instead
- **Unit test verification**: Run `./gradlew :app:testDebugUnitTest` after `clean assembleDebug` — 12/12 tests passed in one session
- **Phased rollout**: Implement feature, verify clean build, then verify unit tests — do not skip steps
- **AI SDK integration**: Host machine Python engine (Cactus + prism-ml + image-studio) via typed HTTP API. No NDK in Android SDK. Hilt 2.51.1 + KSP 1.8.22-1.0.11 + Kotlin 1.8.22 is the verified combination
- **APK size**: Debug APK ~16.6 MB after AI SDK changes; clean-build APK path is the CI verification gate
- **MediaType.parse extension function**: In OkHttp 4.11.0, `MediaType.parse` is an extension function. Fix: use `"application/json".parse()` extension syntax


### On-device CI/CD pipeline development

**Device detection with ADB.** When a pre-set `ADB` path points to the adb binary but `command -v adb` fails (ADB not on PATH), the device detection must check `[[ -n "${ADB}" ]]` rather than `command -v adb`. This is the failure mode that blocked device targeting in the LumenSplat pipeline: `detect()` used `command -v adb` which returned empty because adb lived at `$ANDROID_HOME/platform-tools/adb` (not on PATH). Fix: test the pre-set ADB variable first.

**Preflight check for AndroidManifest.xml.** When a manifest attribute spans multiple lines, a single-line `grep -q` pattern fails. Use `grep -oE 'pattern[^<]*'` to capture the feature declaration and then check for the attribute in the captured line. Or use line-break-agnostic `grep -qPz` on the whole file.

**FOSS license allowlist key matching.** The 06_licenses check extracts catalog IDs from `app/build.gradle.kts` by replacing dots with hyphens. `libs.androidx.navigationCompose` becomes `androidx-navigationCompose` (the `Compose` suffix is preserved). The ALLOWED map must contain the exact extracted key — `“androidx-navigation-compose”` (hyphenated Compose token) will NOT match `androidx-navigationCompose` (no hyphen). Always run the check twice: once to see the missing keys, once to confirm they are added correctly.

**Preflight results file format.** `ci/audits/preflight_results.json` is NDJSON (one JSON object per line), not a JSON array. Each line is a separate object. When parsing with Python, do not use `json.load()` on the whole file — read line by line:

```python
import json, sys
with open('ci/audits/preflight_results.json') as f:
    for line in f:
        if line.strip():
            d = json.loads(line)
            print(d.get('name'), d.get('status'))
```

**Patch tool exact-string mismatches.** The `patch` tool can fail with “Could not find a match for old_string” when the file content differs from the intended patch target (whitespace, tabs vs spaces, line endings). When this happens, read the exact file content with `read_file` (or `cat`), then use a Python one-liner with precise string replacement instead of `patch`:

```bash
python3 -c "
import sys
p = 'path/to/file'
s = open(p).read()
s = s.replace(old_string, new_string)
open(p, 'w').write(s)
"
```

Then verify with `bash -n` for shell scripts or a build command.

## Unit test verification (Room + MockK + JUnit 5)

1. **Run tests**: `./gradlew :app:testDebugUnitTest` from `SpendingSaverAndroid`.
2. **Test template for Room DAO tests**:

   ```kotlin
   internal class TaxRepositoryTest {
       @Test
       fun testName() = runTest {
           // IMPORTANT: coEvery must be INSIDE each test method, never top-level.
           // Top-level coEvery causes: "Expecting a top level declaration" compile error.
           coEvery { TaxDatabase.getInstance(any()) } returns mockk<TaxDatabase>()

           val dao = mockk<TaxDao>(relaxed = true)
           every { dao.someMethod() } returns flowOf(...)   // non-suspend: use `every`
           // coEvery is for suspend functions only; use `every` for non-suspend

           val context = mockk<android.content.Context>(relaxed = true)
           val repository = TaxRepository(context, dao)

           // assertions
       }
   }
   ```

3. **Missing imports that cause `Unresolved reference` errors:**
   - `import kotlinx.coroutines.test.runTest` — `runTest { }` block
   - `import androidx.annotation.RuntimeEnvironment` — `RuntimeEnvironment.application` for a real Context (Room needs a non-null Context)
   - `import io.mockk.every` — `every { ... }` for non-suspend DAO method stubs
   - `import io.mockk.coEvery`, `import io.mockk.coVerify` — coroutine-aware stubs for suspend functions

4. **Gradle `clean` deadlock workaround**: `gradle clean` can fail with `New files were found` / \"New files were found\" (locked build files). Workaround: run `gradle clean` alone until it succeeds, then run `gradle assembleDebug` fresh.

5. **Read test results for failure diagnostics**: Check `app/build/test-results/testDebugUnitTest/TEST-*.xml` for detailed failure messages and stack traces.

6. **Seed data consistency**: `coVerify(exactly = N)` counts must match the actual seed data insertions. After changing `seedTaxData()`, review every `coVerify(exactly = N)` and recount the insertions:
   - 1 `insertCountry` call → 1 `coVerify(exactly = 1) { taxDao.insertCountry(any()) }`
   - `insertState` calls accumulate all states (each call is one state)
   - `insertTown` calls accumulate all towns
   - `insertDetails` (bulk) → 1 call → 1 `coVerify(exactly = 1) { taxDao.insertDetails(any()) }`
   - `insertRecord` calls accumulate records
   - `insertFiling` calls accumulate filings
   - `insertAudit` calls accumulate audits

7. **`insertDetails` (bulk) vs `insertDetail` (single)**: The `TaxRepository` uses `insertDetails(details: List<TaxDetail>)` which calls `taxDao.insertDetails(details)` — NOT `insertDetail` called repeatedly. When verifying, expect `coVerify(exactly = 1) { taxDao.insertDetails(any()) }` for bulk inserts, not `coVerify(exactly = N) { taxDao.insertDetail(any()) }`.

8. **`TaxTown` constructor has NO `country_code` parameter** — only `state_id`, `town_code`, `town_name`, `county`, `is_city`, `is_town`, `id`. Do NOT pass `country_code` to `TaxTown`.

9. **`TaxRepository` constructor**: `@Inject constructor(private val context: Context, private val taxDao: TaxDao)` — a field `private val taxDatabase = TaxDatabase.getInstance(context)` in the constructor is NOT used by repository methods (all methods use `taxDao`). For unit tests, intercept `TaxDatabase.getInstance(any())` with `coEvery { TaxDatabase.getInstance(any()) } returns mockk<TaxDatabase>()` so the constructor does not create a real database.

## References

- `ci/README.md` — local on-device CI/CD pipeline documentation
- `ci/preflight/checks/` — preflight check scripts (00_toolchain, 01_gradle_wrapper, 02_version_catalog, 03_manifest, 04_native_sources, 05_shaders, 06_licenses, 07_device, 99_notary)
- `ci/scripts/run_pipeline.sh` — pipeline orchestrator
- `ci/config.sh` — device detection and toolchain config
- `ci/matrix/device-matrix.md` — supported device matrix
