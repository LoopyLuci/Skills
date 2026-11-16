---
name: ai-integration-architecture
description: Use when adding AI engines to the SpendingSaver app.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [ai, android, hilt, http-sdk]
    category: software-development
    related_skills: [android-kotlin-build-pitfalls]
---

# AI/Multimodal Integration Architecture

## Trigger

Use when adding AI/multimodal capabilities to the SpendingSaver Android app:
- Integrating Cactus text generation, Mirage vision, or Whistle ASR
- Adding prism-ml Bonsai for text/image generation
- Adding image-studio for image generation
- Exposing AI features through UI (chat, image description, voice input)

## Architecture (mandatory)

```
Host Machine AI Engine (Python 3.14 + Cactus + prism-ml + image-studio)
    down-arrow HTTP (typed API with capability registry)
Android AI SDK (Kotlin: capability registry + intents + client + repository)
    down-arrow
SpendingSaver App UI (Composables: chat, image description, voice, image gen)
```

**Rule: Always use HTTP SDK as the bridge between the local AI engine and the Android app.**
- Native JNI/Ndk bindings are NOT viable because the Android SDK has no NDK installed.
- The host Python AI engine runs locally on the machine; Android SDK calls it via typed HTTP endpoints.
- The AI capability registry defines typed endpoints for each capability.

## Capability Mapping

| Capability | Source |
|---|---|
| Text generation / tool use | Cactus engine (cactus) |
| Vision / image-to-text / OCR | Cactus Mirage |
| Speech recognition (ASR) | Cactus Whistle |
| Text-to-speech | Not in Cactus stack — TODO: Jetpack TextToSpeech |
| Image generation | prism-ml bonsai-image + image-studio/FLUX.2 klein |
| Object detection / segmentation | Cactus Mirage |
| Zero-shot classification / VQA / document QA | Cactus Mirage |

## Key Files

| File | Purpose |
|---|---|
| SpendingSaverAndroid/app/src/main/java/com/spendingsaver/ai/AiCapabilities.kt | Capability registry with typed endpoints |
| SpendingSaverAndroid/app/src/main/java/com/spendingsaver/ai/AiIntent.kt | Typed sealed-intent hierarchy |
| SpendingSaverAndroid/app/src/main/java/com/spendingsaver/ai/AiClient.kt | OkHttp 4.11.0 + Gson HTTP client |
| SpendingSaverAndroid/app/src/main/java/com/spendingsaver/ai/AiRepository.kt | Repository with ping/generateText/describeImage/transcribeAudio/generateImage |
| SpendingSaverAndroid/app/src/main/java/com/spendingsaver/ai/AiHiltModule.kt | DI module |
| SpendingSaverAndroid/app/src/main/java/com/spendingsaver/di/AppModule.kt | Hilt DI: @Provides for OkHttpClient, AiClient, AiRepository |
| SpendingSaverAndroid/app/src/main/java/com/spendingsaver/ui/screens/AISettingsScreen.kt | Settings screen with service URL configuration |
| SpendingSaverAndroid/app/src/main/java/com/spendingsaver/ui/screens/AIComponents.kt | UI components (Chat, Image description, Voice input) |
| SpendingSaverAndroid/app/src/main/java/com/spendingsaver/ui/viewmodel/MainViewModel.kt | ViewModel with aiRepository StateFlow |

## Build & KSP Workflow (AI SDK)

### Build requirements

1. `./gradlew clean assembleDebug --console=plain --no-daemon` — always run `clean` first.
2. `org.gradle.jvmargs=-Xmx4096m` in `SpendingSaverAndroid/gradle.properties`.
3. `GRADLE_OPTS="-Xmx4096m -XX:MaxMetaspaceSize=512m"` in `ci/config.sh`.
4. `okhttp 4.11.0` + `kotlinx-serialization-json 1.5.1` in `app/build.gradle.kts`.

### KSP & Room DAO pitfalls discovered during AI SDK integration

1. **MOVE DAO, DATABASE, AND REPOSITORY INTO ONE PACKAGE** — All three files (`TaxDao.kt`, `TaxDatabase.kt`, `TaxRepository.kt`) must live in the same package as the entity types (`com.spendingsaver.tax`). If the `@Dao` is in a different package from the `@Database` class, KSP validates the DAO queries against the wrong schema and fails with `SQLITE_ERROR: no such table` or `[ksp] MissingType`.
2. **REMOVE `insertAll(List<T>)` methods from DAOs** — KSP generates `insertAll(List<T>)` as a suspend function with a `$completion: Continuation<Unit>` parameter, causing `Conflicting declarations` or `Type mismatch` errors. Use individual `insert(item)` calls instead.
3. **Remove orphaned annotations when deleting methods** — If a method is deleted from a DAO but its `@Insert`/`@Query` annotation is left behind, KSP fails with `An abstract DAO method must be annotated with one and only one of the following annotations`.
4. **Use `collect { it.toList() }` (not `.first()` or `toList()`) on `Flow<List<T>>`** — In suspend functions, calling `.first()` or `.toList()` on a `Flow<List<T>>` receiver causes `Unresolved reference` or receiver type mismatch. Use `collect { list.addAll(it) }` inside a suspend function to materialize the list.
5. **KSP cache invalidation** — After any DAO or `@Database` edit, run `./gradlew clean` before `assembleDebug`. The KSP cache holds stale bindings that incremental builds do not clear.
6. **Do NOT duplicate `insertAll` in both DAO and Repository** — Only the DAO defines `insertAll(List<T>)`; the Repository only defines individual `insert(item)` methods. Cluttered the Repository with `insertAll` methods causes duplicate variable declarations.

## Priority & scope (user preference)

1. **Mobile app first, Nokia 7.2 test target** — Verify on `com.spendingsaver` process via `adb`.
2. **No Kindle device/package** — Verify `pm list packages | grep -i kindle` returns empty.
3. **CI/CD green gate is a precondition** — `./ci/run.sh all` must be green before shipping feature work.
4. **Full AI/multimodal integration** — Host engine (Cactus + prism-ml + image-studio) → Android AI SDK (typed HTTP) → app.
5. **Local AI engine** — Host Python 3.14.9+202**1021 venv has `cactus-compute` installed.
6. **No NDK** — Native JNI/Cactus build is blocked; use HTTP SDK.
7. **Exhaustive scope, not minimal** — Complete every roadmap item, do not trim.
8. **Credential handling** — API keys, tokens, passwords, secrets must NEVER appear in summaries; replaced with `[REDACTED]`.
9. **Gradle `GRADLE_OPTS` must supply ONLY JVM memory options** — `-Xmx4096m -XX:MaxMetaspaceSize=512m` — not CLI flags (`-x -no-daemon --console=plain --build-cache` crash JVM with `Unrecognized option: -x`).
10. **Do not commit credentials, local configuration, private account data, generated build output, or local logs.**

## Testing

1. Unit tests for AI SDK (`AiClientTest.kt`, `AiRepositoryTest.kt`) run via `./gradlew :app:testDebugUnitTest`.
2. Integration tests: start the local Python AI engine host, then call Android SDK endpoints via device network.
3. Mock `OkHttpClient` when testing repository layer.

## References

- `ai-integration-procedure.md` — detailed AI SDK implementation procedure (if exists)
- `android-kotlin-build-pitfalls` — Kotlin language and build pitfalls
- `ai-service/README.md` — AI SDK architecture
- `ci/README.md` — CI/CD pipeline documentation