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

2. Box `contentAlignment` is not a valid parameter
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

2. **Activity result API needs ALL three dependencies**
   - `activity-compose`, `activity`, AND `activity-ktx` must all be present
   - Missing any one causes `rememberLauncherForActivityResult` to be unresolved

3. **Hilt Context injection requires `@ApplicationContext`**
   - `Context` injected into `@Provides` methods must use `@ApplicationContext`

4. **Duplicate top-level functions across files cause overload resolution ambiguity**
   - If two files define the same function name in the same package, Kotlin cannot resolve which to use

5. **MSYS paths do not work with native Windows tools**

6. **Kotlin source file must have `package` declaration**

7. **Gradle builds that fail can leave stale intermediate files**

## References

- `build/gradle/gradle.properties` — project-wide Gradle options
- `ci/README.md` — CI/CD pipeline documentation
- `ai-service/README.md` — AI SDK architecture

## How this skill was built

This skill was created from a session that integrated a new AI SDK into the SpendingSaver Android app. The session hit repeated Kotlin compilation errors (Kotlin `when` expressions with `is` over enum entries, Box `contentAlignment`, duplicate function definitions, MSYS path resolution, Hilt DI binding issues). These errors were resolved through iterative build+fix cycles, and the successful pattern is encoded here as standing workflow rules for future sessions.
