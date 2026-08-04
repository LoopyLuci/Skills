---
name: google-mobile-ads-interstitial
description: Use when implementing Google Mobile Ads interstitial ads in Android/iOS apps.
tags: [android, ios, google-mobile-ads, interstitial-ads, monetization]
related_skills: [google-mobile-ads-get-started, google-mobile-ads-banner, google-mobile-ads-rewarded]
---

# Google Mobile Ads SDK — Interstitial Ads

Interstitial ads are full-page ads that cover the interface of an app. They are typically displayed at natural transition points in an app's flow.

## Ad Placement Guidelines

- Place at natural app transition points (between levels, after completing a task)
- Identify target file and parent context before implementing

## Implementation Steps

1. Determine the platform (Android / iOS)
2. Load the ad
3. Register for ad event callbacks
4. Show the ad
5. Verify the implementation

## Code Example (Android — Kotlin)

```kotlin
import com.google.android.gms.ads.interstitial.InterstitialAd
import com.google.android.gms.ads.AdRequest

class MainActivity : AppCompatActivity() {
    private var interstitialAd: InterstitialAd? = null

    fun loadInterstitial() {
        val adRequest = AdRequest.Builder().build()
        InterstitialAd.load(this, "ca-app-pub-3940256099942544/1033173712", adRequest,
            object : InterstitialAdLoadCallback() {
                override fun onAdLoaded(ad: InterstitialAd) {
                    interstitialAd = ad
                }
                override fun onAdFailedToLoad(loadAdError: LoadAdError) {
                    interstitialAd = null
                }
            })
    }

    fun showInterstitial() {
        interstitialAd?.show(this)
    }
}
```

## Common Pitfalls

- **Ad not loaded before show**: Always check that the ad is loaded before calling `show()`
- **Showing too frequently**: Respect user experience — don't show interstitials too often
- **Missing ad unit ID**: Use test ad IDs during development

## Verification Checklist

- [ ] Test ad unit ID used during development
- [ ] Ad loads successfully
- [ ] Ad displays at appropriate transition points
- [ ] Production ad unit ID configured before release
