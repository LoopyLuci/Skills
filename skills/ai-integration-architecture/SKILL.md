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

## AI Engine Host Setup

- Use HermESC-managed Python 3.14.9+202**1021 venv at `/c/Users/Server/AppData/Local/hermes/tools/python-3.14.9+202**1021-win32-x64/python3`.
- The venv has `cactus-compute` installed (cactus, Mirage, Whistle confirmed accessible via HTTP).
- Default `HERMES_PYTHON` env override for alternative Python paths.

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

1. **Test dependencies**: Add `testImplementation("io.mockk:mockk:1.13.7")` to `app/build.gradle.kts`.
2. **MockK setup**: Use `mockkObject(AiClient)` to mock the client, then `every { AiClient(any(), any(), any()) } returns mockClient` to inject the mock.
3. **Constructor access**: `AiRepository` takes `Context` in constructor; provide a mock `Context` with mocked `SharedPreferences`.
4. **Test data**: `AiResponse` constructor requires `success: Boolean` (no default value) — always provide it.

## References

- `ai-integration-procedure.md` — detailed AI SDK implementation procedure (if exists)
- `android-kotlin-build-pitfalls` — Kotlin language and build pitfalls
- `ai-service/README.md` — AI SDK architecture
- `ci/README.md` — CI/CD pipeline documentation