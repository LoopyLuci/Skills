---
name: google-mobile-ads-android-migrate-to-next-gen
description: Use when migrating Android apps from legacy GMA SDK to GMA Next-Gen SDK.
tags: [android, google-mobile-ads, migration, gma-sdk, kotlin]
related_skills: [google-mobile-ads-get-started, android-native-dev]
---

# Google Mobile Ads SDK — Migration to GMA Next-Gen

Provides comprehensive mapping tables for migrating Android applications from the legacy `com.google.android.gms:play-services-ads` SDK to the new `com.google.android.libraries.ads.mobile.sdk:ads-mobile-sdk`.

## Migration Workflow

1. **Configure Gradle**: Replace dependency, update `minSdk` (24+) and `compileSdk` (34+)
2. **Per-file migration**: Refactor imports, class names, and method signatures
3. **Verify and build**: Run `gradle build -x test` to confirm clean build

## Code Example: Gradle Dependency

```kotlin
// Old (legacy)
// implementation("com.google.android.gms:play-services-ads:23.0.0")

// New (Next-Gen)
implementation("com.google.android.libraries.ads.mobile.sdk:ads-mobile-sdk:LATEST_VERSION")
```

## Key Migration Rules

- **App ID**: Preserve `com.google.android.gms.ads.APPLICATION_ID` meta-data in manifest
- **UI Threading**: Callbacks invoke on background thread — wrap UI operations in `runOnUiThread{}`
- **Initialization**: Call `MobileAds.initialize()` on background thread; bundle `RequestConfiguration` into `InitializationConfig`
- **Banner ads**: Use `com.google.android.libraries.ads.mobile.sdk.banner.AdView`
- **Response info**: Use `ad.getResponseInfo()` (not `.responseInfo`)

## Common Pitfalls

- **Missing dependency exclusion**: Exclude `play-services-ads` and `play-services-ads-lite` globally to avoid duplicate symbol errors
- **UI thread crashes**: All UI operations in GMA callbacks MUST use `runOnUiThread{}` or `Dispatchers.Main`
- **AdSize mismatch**: AdSize is now declared in `BannerAdRequest`, not on `AdView`
- **MediaView removed**: Use `registerNativeAd(nativeAd, mediaView)` instead of `nativeAd.mediaView`

## Verification Checklist

- [ ] Gradle dependency updated to `ads-mobile-sdk`
- [ ] `minSdk` >= 24, `compileSdk` >= 34
- [ ] Legacy SDK excluded from all transitive dependencies
- [ ] Build succeeds: `gradle build -x test`
- [ ] All imports refactored per API mapping table
