# AI SDK Integration Procedure

Procedure for integrating the local AI engine (Cactus prisma-ml image-studio) into the SpendingSaver Android app.

## Architecture

```
Host Machine AI Engine (Python 3.14 + Cactus)
    ↓ HTTP (typed API)
Android AI SDK (Kotlin: AiClient, AiRepository, model classes)
    ↓
SpendingSaver App UI (Composables: AIChatScreen, AIImageDescriptionScreen, AITranscribeScreen)
```

## Verified Build Configuration (2026-11-19)

- **Kotlin**: 1.8.22
- **KSP**: 1.8.22-1.0.11
- **Hilt**: 2.51.1 (KSP, NOT kapt)
- **Android Gradle Plugin**: 8.1.0 (compileSdk 34)
- **Gradle**: 8.2 (system Gradle fallback; Hermes wrapper had CRLF issues)
- **Gradle memory**: `org.gradle.jvmargs=-Xmx4096m` in `gradle.properties`
- **Dependencies**: `androidx.room:room-runtime:2.5.2`, `com.google.gson:gson:2.10.1`, `com.squareup.okhttp3:okhttp:4.11.0`

## Build Commands

```bash
cd SpendingSaverAndroid
export GRADLE_HOME=/tmp/gradle-8.2/gradle-8.2
export PATH=$GRADLE_HOME/bin:$PATH
gradle clean assembleDebug --console=plain --no-daemon
```

Fallback: use system Gradle 8.2 at `/tmp/gradle-8.2` if the Hermes wrapper gradlew has CRLF or `DEFAULT_JVM_OPTS` quoting issues.

## Known Issues (Fixed)

- **Kotlin 1.8.22 EnumClassLowering**: Converting enum classes with default parameters and multiple entries causes `AssertionError: No such value argument slot`. Fix: convert enum to data class + object registry.
- **Dagger duplicate bindings**: Duplicate `@Provides @Singleton` for the same type in different modules causes build failure. Remove the duplicate.
- **Hilt stale stub**: After Hilt version changes, `rm -rf app/build/tmp/kapt3/stubs` may be needed, but KAPT is not used with Hilt 2.51.1 (KSP).
- **MediaType.parse extension**: In OkHttp 4.11.0, `MediaType.parse` is an extension function. Use `"application/json".parse()` or the full signature `RequestBody.create(content, null)`.
- **Room 2.5.2 DAO annotations**: `@Upsert`/`@Delete` not supported on DAO methods. Use `@Insert(onConflict = OnConflictStrategy.REPLACE)` + explicit `@Query("DELETE FROM ...")`.
