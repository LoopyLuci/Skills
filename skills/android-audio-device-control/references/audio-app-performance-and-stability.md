# Android audio app: polish, performance, stability

Measured findings from hardening a production audio app. Every number here came from a
real device (Nokia 7.2 / Android 11), not an estimate.

## 1. Audio focus is not optional

An app that produces or captures audio MUST negotiate focus. Without it the app talks
over phone calls, alarms and navigation prompts, never ducks, and never pauses. That is
a Play policy problem, not just bad manners.

Audit any audio codebase with:

```bash
grep -rc "requestAudioFocus\|OnAudioFocusChangeListener" --include=*.kt .
```

Zero hits on an audio app is the single highest-severity finding available.

The decision table that matters:

| System callback | App behaviour |
|---|---|
| `AUDIOFOCUS_GAIN` | resume, full gain |
| `AUDIOFOCUS_LOSS_TRANSIENT_CAN_DUCK` | keep playing, attenuate (~-12 dB) |
| `AUDIOFOCUS_LOSS_TRANSIENT` | pause, KEEP the session (call ending → resume) |
| `AUDIOFOCUS_LOSS` | stop AND abandon focus (another player took over) |
| `AUDIOFOCUS_REQUEST_DELAYED` | do NOT start yet — focus arrives later |

Implementation notes learned the hard way:

- **Duck yourself.** `setWillPauseWhenDucked(false)` and apply your own gain multiplier
  AFTER the DSP chain. Letting the platform duck stacks its attenuation on top of your
  processing and changes how compressors/limiters behave.
- **Gate `start()` on the focus result.** Returning `false` when focus is refused is
  what prevents playing during a call.
- **Always `abandon()` in `stop()`/`release()`.** Holding focus after stopping keeps
  other apps silent — the most common focus bug in the wild.
- Capture wants `GAIN_TRANSIENT_MAY_DUCK` (let music keep playing quietly), playback
  wants `GAIN`.

## 2. ERROR_DEAD_OBJECT: the unplug crash

`AudioTrack.write()` / `AudioRecord.read()` return `ERROR_DEAD_OBJECT` when the device
disappears mid-stream (USB DAC pulled, Bluetooth dropped). Code that only checks
`if (written < 0) break` silently kills audio; code that ignores the return value spins
on a dead handle.

```kotlin
when {
    written == AudioTrack.ERROR_DEAD_OBJECT -> {
        // Rebuild against the new default route; do not reuse the dead track.
        if (!recreateTrack()) break
        continue
    }
    written == AudioTrack.ERROR_INVALID_OPERATION -> break
    written < 0 -> break
    written < buffer.size -> underruns++
}
```

Extract the track/record builder into its own function so the recovery path cannot
drift from the initial configuration. Count recoveries in your state object — a rising
count is a real diagnostic signal.

## 3. `runCatching` without logging is a debugging dead end

OEM audio stacks routinely refuse operations the public API advertises (codec
selection, battery reporting, routing), so `runCatching` is the right tool. But:

```bash
# The tell: many catches, no logging.
grep -rc "runCatching" --include=*.kt . | awk -F: '{s+=$2} END {print s" catches"}'
grep -rc "Log\.\|Timber\." --include=*.kt . | awk -F: '{s+=$2} END {print s" logs"}'
```

149 catches against 1 log call meant "codec switching doesn't work on my phone" was
unactionable. Fix with a bounded in-memory ring buffer (no file I/O on the audio path,
no unbounded growth) plus an inline helper that replaces the bare pattern:

```kotlin
inline fun <T> platformCall(tag: String, operation: String = "", default: T, block: () -> T): T =
    try { block() } catch (e: Throwable) { w(tag, "platform call failed ($operation)", e); default }
```

Catch `Throwable`, not `Exception`: reflective access to hidden APIs throws
`NoSuchMethodError` on some OEM builds.

Store only `"${type.simpleName}: ${message}"` per event, never a full stack trace —
4,000 events with stacks will not fit in a sane memory budget.

## 4. Baseline Profile — the biggest free win

**Rigorously measured: 712 ms → 517 ms median cold start (27% faster).**

Macrobenchmark, 10 iterations per mode, `timeToInitialDisplay` on a Nokia 7.2 / Android 11:

| Mode | Median | Range |
|---|---|---|
| `None` (JIT) | 712 ms | 693–833 |
| `Partial` (Baseline Profile) | **517 ms** | 500–529 |
| `Full` (AOT) | 524 ms | 492–556 |

Two findings worth internalising:

- The profile **matches full AOT** (within 7 ms) at a fraction of the install cost.
- It also **cuts variance**: a 29 ms spread versus 139 ms. Consistency matters as much as
  the median for perceived responsiveness.

**Do not trust ad-hoc `am start -W` timings.** A quick loop of
`adb shell cmd package compile -m speed-profile` + `am start` suggested 42% on this same
app — a 15-point overstatement versus macrobenchmark, because it does not control for
page cache, background work, or measurement warmup. Use `am start` to sanity-check that
the app launches; use macrobenchmark for any number you intend to publish.

Steps:

1. `implementation(libs.androidx.profileinstaller)` in the app module.
2. `app/src/main/baseline-prof.txt` listing startup classes/methods (`HSPL` prefixes).
3. Verify it actually shipped — do not assume:
   ```python
   z = zipfile.ZipFile("app-release.aab")
   [n for n in z.namelist() if n.endswith((".prof", ".profm"))]
   # BUNDLE-METADATA/com.android.tools.build.profiles/baseline.prof
   ```
4. Reproduce the on-device effect for measurement:
   ```bash
   adb shell cmd package compile -m speed-profile -f <pkg>
   adb shell am start -W -n <pkg>/.MainActivity | grep TotalTime
   ```

Always `force-stop` between runs and discard the first measurement — it includes
page-cache warming.

## 5. Compose: find unstable parameters mechanically

A `List`/`Map`/`Set` parameter on a `@Composable` is UNSTABLE, so the composable
recomposes whenever its parent does. On a Canvas that redraws during a drag gesture,
that is visible jank.

```python
for m in re.finditer(r"@Composable\s*(?:private\s+)?fun\s+(\w+)\s*\(([^)]{0,700})\)", src, re.S):
    unstable = re.findall(r"(\w+):\s*(List<|Map<|Set<)", m.group(2))
```

Fix with `kotlinx.collections.immutable.ImmutableList` and `.toImmutableList()` at the
call site. Export it as `api` (not `implementation`) from the module that owns the
composable, or callers cannot construct one.

Check what is ALREADY right before changing it: `Path()` objects wrapped in `remember`,
`drawWithCache`, and FFT callers passing a reusable output buffer were all fine here —
only the parameter types needed work.

## 6. Hot-path allocation audit

Anything called per audio frame or per animation frame must not allocate:

```python
alloc = re.compile(r"\b(listOf|mutableListOf|arrayOf|FloatArray\(|ArrayList|mapOf)\b|\.map \{|\.filter \{|\.toList\(\)")
```

Real hit: `if (listOf(b0,b1,b2,a1,a2).any { it.isNaN() })` inside biquad coefficient
updates — allocated a List on every EQ band drag. Explicit `||` checks are uglier and
correct.

Ignore constructor/`init`-time allocations (FFT tables, delay buffers): those run once.
Read the surrounding function before "fixing" anything.

## 7. Macrobenchmark module

`com.android.test` module, `targetProjectPath = ":app"`, and a `benchmark` build type on
the app that `initWith(release)` so you measure a release-like binary. Benchmarking a
debug build produces numbers that mean nothing.

Compare `CompilationMode.None()` vs `Partial(BaselineProfileMode.Require)` vs `Full()`
— the None→Partial delta is exactly what the Baseline Profile buys real users.

Wait for real content, not just the window, or you are timing a splash screen:

```kotlin
startActivityAndWait()
device.wait(Until.hasObject(By.textContains("Dashboard")), 5_000)
```
