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

1. **`when (value) { is Enum.ENTRY -> ... }` is a Kotlin compile error**
   - The `is` keyword is for type checking, not enum entry matching
   - Fix: use `value == Enum.ENTRY` instead

2. **Enum property named `name` shadows `Enum.name` and causes compile error**
   - The Kotlin compiler rejects enum classes with a property named `name` because it shadows the `name` member of the `Enum` superinterface
   - Fix: rename the property to `taxName` (or any non-reserved name)
   - Example: `enum class TaxType(code: String, taxName: String, ...)`

3. **Room DAO in separate package fails KSP validation against wrong schema**
   - When a `@Dao` interface is in a separate package (e.g., `com.spendingsaver.tax`) from its `@Database` class, KSP validates the DAO queries against the main app's `AppDatabase` schema instead of the correct `@Database` class
   - Result: `SQLITE_ERROR: no such table: tax_detail` despite the `@Database` annotations being correct
   - Fix: (a) move the DAO into the main app's `com.spendingsaver.data` package, or (b) create a separate Android library module for the feature
   - Detection: `./gradlew assembleDebug` fails with `SQLITE_ERROR: no such table` and `[ksp] MissingType` errors
   - Alternative: use a dedicated module with its own `build.gradle.kts` and `settings.gradle.kts`

4. **Activity result API needs ALL three dependencies**
   - `activity-compose`, `activity`, AND `activity-ktx` must all be present
   - Missing any one causes `rememberLauncherForActivityResult` to be unresolved

5. **Hilt Context injection requires `@ApplicationContext`**
   - `Context` injected into `@Provides` methods must use `@ApplicationContext`

6. **Duplicate top-level functions across files cause overload resolution ambiguity**
   - If two files define the same function name in the same package, Kotlin cannot resolve which to use
   - Detection: `Conflicting declarations: val backgroundGradient` or similar

7. **MSYS paths do not work with native Windows tools**

8. **Kotlin source file must have `package` declaration**

9. **Gradle builds that fail can leave stale intermediate files**
   - After fixing source files, always run `./gradlew clean` to remove stale KSP and intermediate artifacts
   - The `clean` task deletes the `build/` directory, which contains KSP-generated stubs and cached annotations

10. **Build memory exhaustion**
   - Kotlin compilation can fail with `Insufficient memory` or `malloc failed` for large projects
   - Fix: increase JVM heap in `gradle.properties`: `org.gradle.jvmargs=-Xmx4096m`
   - Also set `GRADLE_OPTS="-Xmx4096m -XX:MaxMetaspaceSize=512m"` in `ci/config.sh`
   - Pattern: `Insufficient memory for the Java Runtime Environment to continue`

## References

- `build/gradle/gradle.properties` — project-wide Gradle options
- `ci/README.md` — CI/CD pipeline documentation
- `ai-service/README.md` — AI SDK architecture

## How this skill was built

This skill was created from a session that integrated a new AI SDK into the SpendingSaver Android app. The session hit repeated Kotlin compilation errors (Kotlin `when` expressions with `is` over enum entries, Box `contentAlignment`, duplicate function definitions, MSYS path resolution, Hilt DI binding issues). These errors were resolved through iterative build+fix cycles, and the successful pattern is encoded here as standing workflow rules for future sessions.
