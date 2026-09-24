---
name: android-audio-dsp-equalizer
version: 1.0.0
author: Hermes Agent
license: MIT
description: Build EQ/DSP engines and spectrum visualizers on Android.
metadata:
  hermes:
    tags: [android, dsp, equalizer, biquad, fft, kotlin]
    related_skills: [android-audio-device-control]
---

# Android Audio DSP: Equalizers & Visualization

## When to Use

Implementing a graphic or parametric equalizer, biquad filter chain, FFT spectrum
analyzer, loudness meter, compressor/limiter, or crossfeed on Android in Kotlin.

## Two paths — pick deliberately

| | Platform `Equalizer` effect | Own biquad chain |
|---|---|---|
| Bands | 5 (typically), fixed centers | Unlimited, arbitrary |
| Applies to | Any session, incl. global | Only audio you process |
| Latency cost | None (in HAL) | Your buffer size |
| Q / filter type | Not adjustable | Full control |

Real apps use **both**: platform `Equalizer`/`BassBoost`/`Virtualizer`/`LoudnessEnhancer`
to affect other apps' playback, and an in-process biquad chain for your own pipeline and
for computing/previewing the response curve. Be explicit in the UI about which is active.

```kotlin
Equalizer(0 /*priority*/, sessionId).apply {
    enabled = true
    (0 until numberOfBands).forEach { b ->
        val (lo, hi) = getBandFreqRange(b.toShort()).let { it[0] to it[1] }
        setBandLevel(b.toShort(), millibels)   // bandLevelRange in mB, e.g. -1500..1500
    }
}
```
Levels are **millibels** (dB × 100). `getBandFreqRange` returns **milliHertz**.

## Biquad (RBJ cookbook) — the core primitive

Direct-form-1 transposed, coefficients normalized by `a0`. This is the whole engine:

```kotlin
class Biquad {
    private var b0=1.0; private var b1=0.0; private var b2=0.0
    private var a1=0.0; private var a2=0.0
    private var x1=0.0; private var x2=0.0; private var y1=0.0; private var y2=0.0

    fun configure(type: FilterType, freq: Double, sampleRate: Int, q: Double, gainDb: Double) {
        val a = 10.0.pow(gainDb / 40.0)              // amplitude for peaking/shelf
        val w0 = 2.0 * PI * freq / sampleRate
        val cw = cos(w0); val sw = sin(w0)
        val alpha = sw / (2.0 * q)
        var B0: Double; var B1: Double; var B2: Double
        var A0: Double; var A1: Double; var A2: Double
        when (type) {
            PEAK -> {
                B0 = 1 + alpha*a;  B1 = -2*cw;      B2 = 1 - alpha*a
                A0 = 1 + alpha/a;  A1 = -2*cw;      A2 = 1 - alpha/a
            }
            LOW_SHELF -> {
                val s = 2*sqrt(a)*alpha
                B0 = a*((a+1) - (a-1)*cw + s);  B1 = 2*a*((a-1) - (a+1)*cw); B2 = a*((a+1) - (a-1)*cw - s)
                A0 = (a+1) + (a-1)*cw + s;      A1 = -2*((a-1) + (a+1)*cw);  A2 = (a+1) + (a-1)*cw - s
            }
            HIGH_SHELF -> {
                val s = 2*sqrt(a)*alpha
                B0 = a*((a+1) + (a-1)*cw + s);  B1 = -2*a*((a-1) + (a+1)*cw); B2 = a*((a+1) + (a-1)*cw - s)
                A0 = (a+1) - (a-1)*cw + s;      A1 = 2*((a-1) - (a+1)*cw);    A2 = (a+1) - (a-1)*cw - s
            }
            LOW_PASS -> { B0=(1-cw)/2; B1=1-cw; B2=(1-cw)/2; A0=1+alpha; A1=-2*cw; A2=1-alpha }
            HIGH_PASS -> { B0=(1+cw)/2; B1=-(1+cw); B2=(1+cw)/2; A0=1+alpha; A1=-2*cw; A2=1-alpha }
            NOTCH -> { B0=1; B1=-2*cw; B2=1; A0=1+alpha; A1=-2*cw; A2=1-alpha }
            BAND_PASS -> { B0=alpha; B1=0.0; B2=-alpha; A0=1+alpha; A1=-2*cw; A2=1-alpha }
            ALL_PASS -> { B0=1-alpha; B1=-2*cw; B2=1+alpha; A0=1+alpha; A1=-2*cw; A2=1-alpha }
        }
        b0=B0/A0; b1=B1/A0; b2=B2/A0; a1=A1/A0; a2=A2/A0
    }

    fun process(x: Double): Double {
        val y = b0*x + b1*x1 + b2*x2 - a1*y1 - a2*y2
        x2=x1; x1=x; y2=y1; y1=y
        return y
    }

    /** Magnitude response in dB at [freq] — for drawing the curve without audio. */
    fun magnitudeDb(freq: Double, sampleRate: Int): Double {
        val w = 2.0*PI*freq/sampleRate
        val cw1 = cos(w); val cw2 = cos(2*w); val sw1 = sin(w); val sw2 = sin(2*w)
        val numRe = b0 + b1*cw1 + b2*cw2; val numIm = -(b1*sw1 + b2*sw2)
        val denRe = 1.0 + a1*cw1 + a2*cw2; val denIm = -(a1*sw1 + a2*sw2)
        val num = hypot(numRe, numIm); val den = hypot(denRe, denIm)
        return 20.0 * log10((num / den).coerceAtLeast(1e-12))
    }
}
```

**Curve drawing = product of magnitudes**, i.e. sum of dB across bands. Compute on a
log-spaced frequency grid (~200 points, 20Hz–20kHz) — never per-pixel-linear, the bass end
will look wrong.

## Graphic EQ band centers

ISO 1/3-octave, 31 bands: 20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400,
500, 630, 800, 1k, 1.25k, 1.6k, 2k, 2.5k, 3.15k, 4k, 5k, 6.3k, 8k, 10k, 12.5k, 16k, 20k.
10-band (1-octave): 31.5, 63, 125, 250, 500, 1k, 2k, 4k, 8k, 16k.
Graphic bands are peaking filters with fixed Q ≈ `sqrt(2^n)/(2^n - 1)` per n-octave spacing
(≈4.32 for 1/3-octave, ≈1.41 for 1-octave).

## Preamp / clipping — mandatory, not optional

Any positive gain can clip. Auto-preamp:
`preampDb = -max(0, peak of summed response)`. Apply as a scalar before the chain and
show a clip indicator driven by actual sample peaks (`abs(sample) >= 1.0`).

## FFT for the analyzer

Two sources:
1. `Visualizer` (platform) — `setCaptureSize(1024)`, `getFft(ByteArray)` returns
   interleaved real/imag pairs in a *signed byte* packed format; requires `RECORD_AUDIO`
   even though you're capturing output. Cheap, coarse.
2. Your own radix-2 FFT over the PCM you process — full control, needed for
   spectrogram/LUFS.

Iterative in-place radix-2 Cooley–Tukey (no recursion, no allocation per frame):

```kotlin
class Fft(private val n: Int) {                     // n must be a power of 2
    private val cos = DoubleArray(n/2) { cos(-2.0*PI*it/n) }
    private val sin = DoubleArray(n/2) { sin(-2.0*PI*it/n) }
    fun transform(re: DoubleArray, im: DoubleArray) {
        var j = 0
        for (i in 1 until n) {                       // bit-reversal permutation
            var bit = n shr 1
            while (j and bit != 0) { j = j xor bit; bit = bit shr 1 }
            j = j or bit
            if (i < j) { re.swap(i,j); im.swap(i,j) }
        }
        var size = 2
        while (size <= n) {
            val half = size/2; val step = n/size
            var i = 0
            while (i < n) {
                var k = 0
                for (m in i until i+half) {
                    val l = m + half
                    val tre = re[l]*cos[k] - im[l]*sin[k]
                    val tim = re[l]*sin[k] + im[l]*cos[k]
                    re[l] = re[m]-tre; im[l] = im[m]-tim
                    re[m] += tre;      im[m] += tim
                    k += step
                }
                i += size
            }
            size = size shl 1
        }
    }
}
```
Window with Hann (`0.5*(1-cos(2πn/(N-1)))`), correct for window gain (×2 for Hann),
convert to dBFS (`20*log10(mag/N)`), then map to log-spaced display bins.

Smoothing that looks right: fast attack / slow release per bin
(`if (new > cur) cur = new else cur += (new-cur)*0.2`) plus a peak-hold with decay.

## Loudness (LUFS, ITU-R BS.1770-4)

K-weighting = high-shelf (+4dB @ ~1681Hz) → high-pass (~38Hz), then mean square over
400ms blocks with 75% overlap; `LUFS = -0.691 + 10*log10(sum of channel-weighted means)`.
Momentary = 400ms, short-term = 3s, integrated = gated (-70 LUFS absolute, -10 LU relative).

## Rendering the visualizer in Compose

Use `Canvas` with a `Path` for the curve and drive it from a `conflate()`d flow.
Non-negotiables for 60fps:
- Hoist all `Path`/`Paint` objects outside the draw lambda (`remember`).
- Feed the UI at ~30–60Hz max; `sample(16)` the DSP flow.
- Use `drawWithCache` for gradients/brushes.
- `graphicsLayer` + `CompositingStrategy.Offscreen` only when you actually need blend modes.
- Prefer `withFrameNanos`-driven interpolation over `animate*AsState` per bin (31–1024
  animations will jank).
- Only reach for `AndroidView` + OpenGL/`GLSurfaceView` for 3D waterfalls/particles.

## Pitfalls

- **Filter state must be per-channel.** One `Biquad` instance per channel per band, or
  stereo collapses/artifacts.
- Reconfiguring coefficients mid-stream clicks — crossfade the gain or ramp coefficients
  over a few ms.
- Q ≤ 0 or freq ≥ Nyquist/2 produces NaN that poisons the whole chain forever. Clamp:
  `q in 0.05..40`, `freq in 10.0..(sampleRate/2 * 0.98)`.
- Never allocate inside the audio callback — pre-size every buffer.
- `Visualizer.getFft` scaling is device-dependent; normalize against observed max, don't
  assume absolute dBFS.
- Store EQ presets as frequency/gain/Q triples, not band *indices* — band counts differ
  across devices and EQ types.
- AutoEQ community presets are ParametricEQ text (`Filter 1: ON PK Fc 105 Hz Gain -2.1 dB Q 0.70`);
  a simple line regex imports them, which is a big feature for free.
