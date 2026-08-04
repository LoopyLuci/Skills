---
name: google-mobile-ads-banner
description: Use when implementing Google Mobile Ads banner ads in Android/iOS apps.
tags: [android, ios, google-mobile-ads, banner-ads, monetization]
related_skills: [google-mobile-ads-get-started, google-mobile-ads-interstitial, google-mobile-ads-rewarded]
---

# Google Mobile Ads SDK — Banner Ads

Banner ads are rectangular image or text ads that occupy a spot within an app's layout. They remain on screen during user interaction and can refresh automatically.

## Ad Placement Guidelines

- **Scrollable content** (ListView, ScrollView, RecyclerView): Use **Inline Adaptive Banner**
- **Non-scrollable content**: Use **Large Anchored Adaptive Banner** anchored to top or bottom

## Implementation Steps

1. Determine platform: Android or iOS
2. Define the ad view
3. Set the ad size
4. Register for ad load events
5. Load the banner ad
6. Replace test ad unit ID with production ID

## Code Example (Android — Kotlin)

```kotlin
val adView = AdView(context)
val adRequest = BannerAdRequest.Builder("ca-app-pub-3940256099942544/6300978111", AdSize.BANNER).build()
adView.loadAd(adRequest, object : AdLoadCallback<BannerAd> {
    override fun onAdLoaded(ad: BannerAd) {
        // Ad loaded successfully
    }
    override fun onAdFailedToLoad(adError: LoadAdError) {
        // Handle error
    }
})
```

## Common Pitfalls

- **Missing ad unit ID**: Always use test ad IDs during development, replace before release
- **Scrollable vs static**: Using anchored banner in a scrollable view causes poor UX
- **Ad size mismatch**: Ensure ad size matches the container dimensions

## Verification Checklist

- [ ] Correct banner type chosen (inline vs anchored)
- [ ] Test ad unit ID used during development
- [ ] Ad loads and displays correctly
- [ ] Production ad unit ID configured before release
