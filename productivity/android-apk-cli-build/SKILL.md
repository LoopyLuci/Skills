---
name: android-apk-cli-build
description: "Build Android APK from CLI on Windows without Android Studio"
---

# Android APK CLI Build on Windows

Build a debug APK without Android Studio using portable JDK + SDK tools.

## Quick Start

```bash
# 1. JDK (portable)
curl -L -o "C:\Users\%USERNAME%\Downloads\jdk17.zip" \
  "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.14%2B7/OpenJDK17U-jdk_x64_windows_hotspot_17.0.14_7.zip"
unzip -q /c/Users/YourName/Downloads/jdk17.zip -d /c/Users/YourName/Downloads/jdk_extract
export JAVA_HOME="C:\\Users\\YourName\\Downloads\\jdk_extract\\jdk-17.0.14+7"
export PATH="$JAVA_HOME/bin:$PATH"

# 2. Android cmdline-tools
curl -L -o "C:\Users\%USERNAME%\Downloads\cmdline-tools.zip" \
  "https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip"
unzip -q /c/Users/YourName/Downloads/cmdline-tools.zip -d /c/Users/YourName/Downloads/cmd_extract
mkdir -p /c/Users/YourName/Android/Sdk/cmdline-tools
mv /c/Users/YourName/Downloads/cmd_extract/cmdline-tools /c/Users/YourName/Android/Sdk/cmdline-tools/latest

# 3. Install SDK
export ANDROID_SDK_ROOT="C:\\Users\\YourName\\Android\\Sdk"
export PATH="$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$PATH"
yes | sdkmanager --sdk_root="$ANDROID_SDK_ROOT" "platforms;android-34" "build-tools;34.0.0"

# 4. Generate wrapper
curl -L -o gradle-8.2-bin.zip "https://services.gradle.org/distributions/gradle-8.2-bin.zip"
unzip -q gradle-8.2-bin.zip
export PATH="/c/Users/YourName/Downloads/gradle-8.2/bin:$PATH"
cd /path/to/android && gradle wrapper --gradle-version=8.2

# 5. Build
echo "sdk.dir=C:/Users/YourName/Android/Sdk" > local.properties
export JAVA_HOME="C:\\Users\\YourName\\Downloads\\jdk_extract\\jdk-17.0.14+7"
export ANDROID_SDK_ROOT="C:\\Users\\YourName\\Android\\Sdk"
./gradlew assembleDebug --no-daemon
```

APK output: `app/build/outputs/apk/debug/app-debug.apk`

## Path Rules

| Variable | Format | Example |
|----------|--------|---------|
| JAVA_HOME | Windows `\\` | `C:\\Users\\Name\\jdk` |
| ANDROID_SDK_ROOT | Windows `\\` | `C:\\Users\\Name\\Android\\Sdk` |
| local.properties | Forward `/` | `sdk.dir=C:/Users/Name/Android/Sdk` |
| curl -o | Windows `\` quoted | `"C:\Users\Name\file.zip"` |

## Common Errors

| Error | Fix |
|-------|-----|
| `sdkmanager not found` | cmdline-tools/latest/bin in PATH |
| `JAVA_HOME invalid` | Use Windows-style path with double backslashes |
| `ic_launcher not found` | Create PNG icons with PIL or XML drawables |
| `Unresolved reference` | Use fully-qualified names: `android.content.Intent` |
