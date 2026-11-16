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

## Key Files

| File | Purpose |
|------|---------|
| `SpendingSaverAndroid/app/src/main/java/com/spendingsaver/ai/AiCapabilities.kt` | Capability registry with typed endpoints |
| `SpendingSaverAndroid/app/src/main/java/com/spendingsaver/ai/AiIntent.kt` | Typed sealed-intent hierarchy |
| `SpendingSaverAndroid/app/src/main/java/com/spendingsaver/ai/AiClient.kt` | OkHttp 4.11.0 + Gson HTTP client |
| `SpendingSaverAndroid/app/src/main/java/com/spendingsaver/ai/AiRepository.kt` | Repository with ping/generateText/describeImage/transcribeAudio/generateImage |
| `SpendingSaverAndroid/app/src/main/java/com/spendingsaver/ai/AiHiltModule.kt` | DI module |
| `SpendingSaverAndroid/app/src/main/java/com/spendingsaver/di/AppModule.kt` | Hilt DI: @Provides for OkHttpClient, AiClient, AiRepository |
| `SpendingSaverAndroid/app/src/main/java/com/spendingsaver/ui/screens/AISettingsScreen.kt` | Settings screen with service URL configuration |
| `SpendingSaverAndroid/app/src/main/java/com/spendingsaver/ui/screens/AIComponents.kt` | UI components (Chat, Image description, Voice input) |
| `SpendingSaverAndroid/app/src/main/java/com/spendingsaver/ui/viewmodel/MainViewModel.kt` | ViewModel with aiRepository StateFlow |

## Capability Mapping

| Capability | Source |
|-------------|--------|
| Text generation / tool use | Cactus engine (cactus) |
| Vision / image-to-text / OCR | Cactus Mirage |
| Speech recognition (ASR) | Cactus Whistle |
| Text-to-speech | Not in Cactus stack (TODO — Jetpack TextToSpeech) |
| Image generation | prism-ml bonsai-image + image-studio/FLUX.2 klein |

## Known Limitations

- **No NDK in Android SDK**: Native JNI integration of Cactus engine is not possible. Viable path is host engine + HTTP SDK.
- **Voice input is a simulated placeholder**: No real MediaRecorder/AudioRecord yet. UI has a recording dialog.
- **AI features not yet wired into existing app screens**: Chat/Image/Voice screens exist but not integrated into main app navigation yet.
