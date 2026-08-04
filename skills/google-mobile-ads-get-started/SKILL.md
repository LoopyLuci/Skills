---
name: google-mobile-ads-get-started
description: Use when integrating Google Mobile Ads SDK into Android, iOS, or Unity apps.
tags: [android, ios, unity, google-mobile-ads, sdk-setup, admob]
related_skills: [google-mobile-ads-banner, google-mobile-ads-interstitial, google-mobile-ads-rewarded]
---

# Google Mobile Ads SDK — Getting Started

Provides instructions for integrating the Google Mobile Ads (GMA) SDK for AdMob or Ad Manager in Android, iOS, or Unity applications.

## Implementation Steps

1. Determine platform (Android / iOS / Unity)
2. Add the SDK dependency
3. Set the application identifier
4. Initialize the SDK
5. Verify the integration
6. Select an ad format to continue

## Code Example (Android — build.gradle.kts)

```kotlin
dependencies {
    implementation("com.google.android.gms:play-services-ads:23.0.0")
}
```

## Code Example (iOS — CocoaPods)

```ruby
pod 'Google-Mobile-Ads-SDK'
```

## Code Example (Initialization — Android)

```kotlin
import com.google.android.gms.ads.MobileAds

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        MobileAds.initialize(this) { }
    }
}
```

## Common Pitfalls

- **Missing app ID**: Add `com.google.android.gms.ads.APPLICATION_ID` meta-data in AndroidManifest.xml
- **SDK not initialized**: Call `MobileAds.initialize()` before loading any ads
- **Wrong platform guide**: Android, iOS, and Unity have different setup steps — follow the correct one

## Verification Checklist

- [ ] SDK dependency added to build file
- [ ] Application ID configured in manifest / Info.plist
- [ ] SDK initialization code added
- [ ] Build succeeds without errors
- [ ] Ad format selected for next steps
