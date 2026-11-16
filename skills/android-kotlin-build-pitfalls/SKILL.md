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

11. **Duplicate top-level functions across files cause overload resolution ambiguity**
   - If two files define the same function name in the same package, Kotlin cannot resolve which to use
   - Detection: `Conflicting declarations: val backgroundGradient` or similar

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

### New learnings (2026-11-16) — SpendingSaver session

- **Clean build verification**: After any source change, run `./gradlew clean assembleDebug --console=plain --no-daemon` to catch incremental-build KSP cache staleness
- **Dex merging failures**: `DexArchiveMergerException` is a KSP cache issue; always `./gradlew clean` first
- **Kotlin compiler internal error**: Often a duplicate function in a DAO; grep for duplicate method names in the DAO file
- **Room migration**: If schema changes, Room requires a migration; validate before shipping
- **KSP version alignment**: `ksp` and `kotlin` versions must match exactly; mismatched versions cause internal compiler errors
- **Hilt @Provides**: Context injection in `@Provides` methods requires `@ApplicationContext`
- **Unit test verification**: Run `./gradlew :app:testDebugUnitTest` after `clean assembleDebug` — 12/12 tests passed in one session
- **Phased rollout**: Implement feature, verify clean build, then verify unit tests — do not skip steps
- **APK size**: Debug APK ~16.6 MB after AI SDK changes; clean-build APK path not yet confirmed

## References

- `build/gradle/gradle.properties` — project-wide Gradle options
- `ci/README.md` — CI/CD pipeline documentation
- `ai-service/README.md` — AI SDK architecture
- `ai-service/ai/backend` — Cactus engine server (Python 3.14)
- `ai-service/ai/sdk` — Android AI SDK (typed HTTP)
