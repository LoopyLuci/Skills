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

## Build Requirements

1. SpendingSaverAndroid/app/build.gradle.kts must include:
   - implementation(com.squareup.okhttp3:okhttp:4.11.0)
   - implementation(com.google.code.gson:gson:2.10.1)
2. Use ./gradlew clean assembleDebug --console=plain --no-daemon — incremental builds mask compile errors.
3. If assemblyDebug fails with KSP MissingType errors about Room tables, ensure the DAO is in the same package as its @Database class.

## Testing

1. Unit tests for the AI SDK (AiClientTest.kt, AiRepositoryTest.kt) run via ./gradlew :app:testDebugUnitTest.
2. Integration tests: start the local Python AI engine host, then call the Android SDK endpoints via the device's network.
3. Mock the OkHttpClient when testing the repository layer.

## Pitfalls

1. **No NDK in the Android SDK** – native libcactus.so/JNI bindings cannot be compiled. Use HTTP SDK instead.
2. **Incremental builds mask compile errors** – always use ./gradlew clean before assembleDebug.
3. **HttpUrl parsing requires a context** – HttpUrl.parse() returns null for malformed URLs; always guard with a null check or fallback.
4. **Gson fromJson type mismatches** – ensure Kotlin types match JSON structure exactly.
5. **Box contentAlignment is not a valid parameter** – use nested Box with explicit sizing.
6. **Activity result API needs ALL three dependencies** – activity-compose, activity, AND activity-ktx must all be present.
7. **Hilt Context injection requires @ApplicationContext** – Context injected into @Provides methods must use @ApplicationContext.
8. **Enum property named name shadows Enum.name** – rename to taxName or similar non-reserved name.
9. **Duplicate top-level functions across files cause overload resolution ambiguity** – avoid naming collisions.
10. **Room DAO in separate package fails KSP validation against wrong schema** – DAO must be in the same package as its @Database class.
11. **Build memory exhaustion** – Kotlin compilation can fail with Insufficient memory. Increase JVM heap: org.gradle.jvmargs=-Xmx4096m in gradle.properties.

## References

- ai-integration-procedure.md — detailed AI SDK implementation procedure.
- android-kotlin-build-pitfalls — Kotlin language and build pitfalls.
