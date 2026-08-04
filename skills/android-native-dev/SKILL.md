---
name: android-native-dev
description: Use when developing Android native apps with Kotlin, Compose, and Material Design 3.
tags: [android, kotlin, jetpack-compose, material-design, mobile-development]
related_skills: [fullstack-dev-api-design, fullstack-dev-db-schema, google-mobile-ads-get-started]
---

# Android Native Development

Comprehensive guide for Android native application development covering Material Design 3, Kotlin/Compose, project configuration, and build troubleshooting.

## Required Files Checklist

```
MyApp/
├── gradle.properties
├── settings.gradle.kts
├── build.gradle.kts
├── gradle/wrapper/gradle-wrapper.properties
├── app/
│   ├── build.gradle.kts
│   └── src/main/
│       ├── AndroidManifest.xml
│       ├── java/com/example/myapp/MainActivity.kt
│       └── res/values/{strings,colors,themes}.xml
```

## Code Example: Build Configuration (app/build.gradle.kts)

```kotlin
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.example.myapp"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.myapp"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }

    buildFeatures {
        compose = true
    }
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.8"
    }
}

dependencies {
    implementation(platform("androidx.compose:compose-bom:2024.02.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.activity:activity-compose:1.8.2")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
}
```

## Code Example: Compose UI with ViewModel

```kotlin
class MyViewModel : ViewModel() {
    private val _uiState = MutableStateFlow("Loading...")
    val uiState: StateFlow<String> = _uiState.asStateFlow()

    init {
        viewModelScope.launch {
            val data = withContext(Dispatchers.IO) { fetchData() }
            _uiState.value = data
        }
    }
}

@Composable
fun MyScreen(viewModel: MyViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()
    Text(text = uiState, fontSize = 18.sp)
}
```

## Common Pitfalls

- **UI updates on IO thread**: Always use `withContext(Dispatchers.IO)` for network/file, update UI on Main
- **Non-null assertions**: Use `?.` and `?:` instead of `!!` to avoid crashes
- **Missing lifecycle cleanup**: Always pair `addObserver` with `removeObserver`
- **BuildConfig disabled**: AGP 8.0+ requires `buildFeatures { buildConfig = true }`
- **Leaking ViewModel in composable**: Use `viewModel()` in Composable, not manual instantiation

## Verification Checklist

- [ ] `./gradlew assembleDebug` succeeds
- [ ] AndroidX enabled in `gradle.properties`
- [ ] Compose BOM manages UI dependency versions
- [ ] Coroutines use correct dispatchers (Main for UI, IO for network/file)
- [ ] Data class response fields are nullable (server may omit fields)
- [ ] Super.onCreate() called in Activity/Fragment lifecycle
