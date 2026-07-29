# Android CLI APK Build on Windows (No Android Studio)

Complete zero-to-APK process for building a Kotlin/Compose Android app from the
command line on a bare Windows 10/11 machine with no Android Studio, no Java,
and no Android SDK pre-installed.

## Full Toolchain Install

### 1. Portable JDK 17+

Download from Adoptium (Temurin) — no installer needed, just a zip:

```bash
curl -L -o "C:\\Users\\<user>\\Downloads\\jdk17.zip" \
  "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.14%2B7/OpenJDK17U-jdk_x64_windows_hotspot_17.0.14_7.zip"
unzip jdk17.zip -d "C:\\Users\\<user>\\Downloads\\jdk_extract"
```

Set `JAVA_HOME` to the extracted directory, **Windows-style path**:
```bash
export JAVA_HOME="C:\\Users\\<user>\\Downloads\\jdk_extract\\jdk-17.0.14+7"
export PATH="$JAVA_HOME/bin:$PATH"
```

### 2. Android Command-Line Tools

```bash
curl -L -o "C:\\Users\\<user>\\Downloads\\cmdline-tools.zip" \
  "https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip"
unzip cmdline-tools.zip -d cmdline_extract
mkdir -p "C:\\Users\\<user>\\Android\\Sdk\\cmdline-tools\\latest"
mv cmdline_extract/cmdline-tools/* "C:\\Users\\<user>\\Android\\Sdk\\cmdline-tools\\latest/"
```

### 3. SDK Components

```bash
export ANDROID_SDK_ROOT="C:\\Users\\<user>\\Android\\Sdk"
yes | cmdline-tools/latest/bin/sdkmanager.bat \
  --sdk_root="$ANDROID_SDK_ROOT" \
  "platforms;android-34" \
  "build-tools;34.0.0"
```

### 4. Gradle Wrapper

From within the Android project directory, if Gradle is available:
```bash
gradle wrapper --gradle-version=8.2
```

Or copy `gradlew`, `gradlew.bat`, `gradle/wrapper/gradle-wrapper.jar`, and
`gradle/wrapper/gradle-wrapper.properties` from another project.

### 5. local.properties

```bash
echo "sdk.dir=C:/Users/<user>/Android/Sdk" > android/local.properties
```

**Forward slashes are required.** `C:\\...` backslash format will cause
`Could not determine the dependencies of null` errors.

## Build the APK

```bash
cd android
export JAVA_HOME="C:\\Users\\<user>\\Downloads\\jdk_extract\\jdk-17.0.14+7"
export ANDROID_SDK_ROOT="C:\\Users\\<user>\\Android\\Sdk"
./gradlew assembleDebug --no-daemon
```

The APK lands at:
```
android/app/build/outputs/apk/debug/app-debug.apk
```

## Project Configuration (Minimum Viable)

### AndroidManifest.xml essentials for a P2P transfer app

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
<uses-permission android:name="android.permission.CHANGE_WIFI_MULTICAST_STATE" />
<uses-permission android:name="android.permission.NEARBY_WIFI_DEVICES" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />

<service
    android:name=".service.TransferService"
    android:foregroundServiceType="dataSync"
    android:exported="false" />
```

### app/build.gradle.kts minimum

```kotlin
android {
    namespace = "com.instanttransfer"
    compileSdk = 34
    defaultConfig {
        applicationId = "com.instanttransfer"
        minSdk = 26
        targetSdk = 34
    }
    buildFeatures { compose = true }
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.5"
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
}

dependencies {
    val composeBom = platform("androidx.compose:compose-bom:2024.01.00")
    implementation(composeBom)
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.activity:activity-compose:1.8.2")
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    implementation("androidx.navigation:navigation-compose:2.7.6")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
}
```

## Error Patterns Encountered

### `AAPT: error: resource mipmap/ic_launcher not found`

The manifest references `@mipmap/ic_launcher` but no icon exists in the project.
**Fix**: Create adaptive icon XML for API 26+ and PNG fallbacks:

```
res/
  mipmap-anydpi-v26/ic_launcher.xml  ← adaptive icon
  mipmap-mdpi/ic_launcher.png
  mipmap-hdpi/ic_launcher.png
  mipmap-xhdpi/ic_launcher.png
  mipmap-xxhdpi/ic_launcher.png
  values/colors.xml                   ← ic_launcher_background color
```

Minimal adaptive icon XML:
```xml
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@drawable/ic_launcher_foreground"/>
</adaptive-icon>
```

### `Unresolved reference: HorizontalDivider`

Material3 renamed `Divider` to `HorizontalDivider` in version 1.2.0.
- **BOM < 2024.02** (e.g. 2024.01.00): use `Divider`
- **BOM >= 2024.02**: use `HorizontalDivider`
- Use the version that matches your BOM — don't guess.

### `LinearProgressIndicator` wrong overload

Before Material3 1.2.0, the function took a raw `progress: Float`. After 1.2.0,
it takes a `progress: () -> Float` lambda (for animation support).
- **BOM 2024.01.00**: `LinearProgressIndicator(progress = 0.5f, ...)`
- **BOM 2024.03.00+**: `LinearProgressIndicator(progress = { 0.5f }, ...)`

### `Could not determine the dependencies of null` + `IOException: path syntax incorrect`

The `local.properties` `sdk.dir` had `C:\\...` backslashes. **Fix**: use
forward slashes: `sdk.dir=C:/Users/.../Sdk`.

### `sdkmanager: command not found`

The file is `sdkmanager.bat`, not `sdkmanager`. In git-bash, the `.bat`
extension is not automatically resolved. Call it with the full name:
```bash
sdkmanager.bat --version
```

### `JAVA_HOME is set to an invalid directory`

The `sdkmanager.bat` and `gradlew.bat` scripts read `JAVA_HOME` as a Windows
path. In git-bash, `JAVA_HOME=/c/Users/.../jdk-17` is a valid MSYS path for
bash commands, but `.bat` files don't understand it.

**Fix**: Always use `C:\\...` or `C:/...` format for JAVA_HOME when running
.bat tools in git-bash:
```bash
export JAVA_HOME="C:\\Users\\dubem\\Downloads\\jdk_extract\\jdk-17.0.14+7"
```

### `Val cannot be reassigned` in TransferJob

If you have a `data class TransferJob` and try to assign `job.state = X`, the
compiler will error if the field is declared as `val`. Change the field to `var`.

This is a common gotcha when converting a data class from immutable to mutable
as the app evolves.

## Caching and Build Speed

- First `./gradlew assembleDebug` downloads Gradle distribution + all deps — ~2-3 min
- Subsequent builds with no changes: ~15s (after `--no-daemon`)
- Incremental Kotlin-only change: ~10s
- Use `compileDebugKotlin` instead of `assembleDebug` to just check Kotlin
  compilation without building the full APK.

## Windows-Specific Notes

- **curl path format**: In git-bash, `curl -o /c/Users/.../file.zip` may fail
  with "Failed to open file". Use `curl -o "C:\\Users\\...\\file.zip"` (Windows
  format) instead. This is a known MSYS2 quirk where some tools interpret the
  path differently than bash.
- **All tools run in git-bash**: Everything in this guide was tested in git-bash
  on Windows 10. PowerShell was NOT used for any step.
- **Avoid mixing path formats**: Pick either MSYS (`/c/Users/...`) or Windows
  (`C:\\...`) and use it consistently. Mixing them within the same toolchain
  (e.g. `sdkmanager.bat` called from bash with MSYS `JAVA_HOME`) causes failures.
