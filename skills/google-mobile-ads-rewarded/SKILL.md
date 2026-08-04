---
name: google-mobile-ads-rewarded
description: Use when implementing Google Mobile Ads rewarded ads in Android/iOS apps.
tags: [android, ios, google-mobile-ads, rewarded-ads, monetization]
related_skills: [google-mobile-ads-get-started, google-mobile-ads-banner, google-mobile-ads-interstitial]
---

# Google Mobile Ads SDK — Rewarded Ads

Rewarded ads reward users with in-app items for interacting with full-screen ads. Users must explicitly opt in to view a rewarded ad.

## Ad Placement Guidelines

- Identify target file where the ad should be placed
- Add an opt-in UI element that users can tap to start the rewarded ad

## Implementation Steps

1. Determine the platform (Android / iOS)
2. Load the ad
3. Register for ad event callbacks
4. Add an opt-in UI element
5. Show the ad
6. Grant the reward to the user
7. Verify the implementation

## Code Example (Android — Kotlin)

```kotlin
import com.google.android.gms.ads.rewarded.RewardedAd
import com.google.android.gms.ads.AdRequest

class MainActivity : AppCompatActivity() {
    private var rewardedAd: RewardedAd? = null

    fun loadRewardedAd() {
        val adRequest = AdRequest.Builder().build()
        RewardedAd.load(this, "ca-app-pub-3940256099942544/5224354917",
            adRequest, object : RewardedAdLoadCallback() {
                override fun onAdLoaded(ad: RewardedAd) {
                    rewardedAd = ad
                }
                override fun onAdFailedToLoad(loadAdError: LoadAdError) {
                    rewardedAd = null
                }
            })
    }

    fun showRewardedAd() {
        rewardedAd?.show(this, OnUserEarnedRewardListener { rewardItem ->
            val rewardAmount = rewardItem.amount
            val rewardType = rewardItem.type
            // Grant reward to user
        })
    }
}
```

## Common Pitfalls

- **No opt-in UI**: Users must explicitly choose to watch a rewarded ad
- **Missing reward grant**: Always grant the reward after successful ad completion
- **Ad not ready**: Preload the ad before showing the opt-in button

## Verification Checklist

- [ ] Opt-in UI element added for user consent
- [ ] Test ad unit ID used during development
- [ ] Ad loads successfully
- [ ] Reward granted after ad completion
- [ ] Production ad unit ID configured before release
