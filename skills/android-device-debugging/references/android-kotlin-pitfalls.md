# Android Kotlin Compilation & Runtime Pitfalls

Surfaces during `:app:compileDebugKotlin` / `:app:assembleDebug`. Each costs 1-3 build cycles if unknown.

## @Inject + module-provided classes → KAPT failure

When a class has `@Inject constructor` AND is also provided by a `@Module` `@Provides` method, KAPT sees two sources of the same binding and fails with "unresolved reference" or ambiguous dependency errors.

**Fix:** Remove `@Inject` from module-provided classes. Keep `@Inject` on consumers (ViewModels, UseCases, repositories resolved from the module).

## @Contextual Any in @Serializable → IR lowering crash

Using `Map<String, @Contextual Any>` in a `@Serializable` data class causes `BackendException: Internal compiler error: Exception during IR lowering` at `AnnotationSerializer.getAnnotationClassId`.

**Fix:** Replace with `Map<String, JsonElement>` from `kotlinx.serialization.json.JsonElement`.

## Size import conflict with CameraX

`androidx.compose.ui.geometry.*` brings in `androidx.compose.ui.geometry.Size`, which shadows `android.util.Size` (used by CameraX `ImageAnalysis.Builder.setTargetResolution()`).

**Fix:** Alias-import the Android Size and do NOT import both unqualified:
```kotlin
import android.util.Size as AndroidSize
.setTargetResolution(AndroidSize(1280, 720))
```

## Icons.Default.AlertCircle does not exist

Material Icons does not include `AlertCircle`. Using it produces "Unresolved reference: AlertCircle".

**Fix:** Use `Icons.Default.Warning` instead.

## kotlinx.coroutines.launch from non-suspend function

`kotlinx.coroutines.launch` is an extension on `CoroutineScope`. Calling it from a regular (non-suspend) function without a scope receiver fails with "Unresolved reference: launch".

**Fix:** Use the scope property (e.g., `viewModelScope.launch`). `kotlinx.coroutines.delay` is fine inside `launch` since it's within the coroutine.

## val refreshJob with reassignment

Declaring `private val refreshJob = kotlinx.coroutines.Job()` prevents reassignment (`refreshJob = viewModelScope.launch { ... }` fails with "Val cannot be reassigned").

**Fix:** Use `var` with nullable type and safe-call cancel:
```kotlin
private var refreshJob: Job? = null
fun startAutoRefresh() {
    refreshJob?.cancel()
    refreshJob = viewModelScope.launch { ... }
}
```

## Deep link handling in @AndroidEntryPoint Activity

When an `@AndroidEntryPoint` Activity receives a deep link via `intent.data`, process it in `onCreate` AND `onNewIntent` (for single-top launches). Extract the query parameter and store it in `PairingStore` or a holder object, then consume from the composable via `LaunchedEffect`.

## Pairing token format (QEMU-MCP)

Tokens are `signature.payload` format — two base64url parts separated by `.`. The desktop generates them with `qrcode.make("qmcmcp://pair?key={token}")`. The Android `PairingTokenVerifier.verify()` splits on `.`, decodes both parts, validates Ed25519 signature, then parses compact JSON. `uriToToken()` extracts the key from `qmcmcp://pair?key=...` URIs.

## EncryptedSharedPreferences constructor

`PairingStore` uses `@ApplicationContext Context` constructor (NOT `@Inject`) because Hilt cannot provide `ApplicationContext` to an `@Inject`-annotated constructor without a module. The class is provided by the module instead.

## @Provides method receiver

When a `@Provides` method receives parameters, those parameters must themselves be resolvable by Hilt (either `@Inject` constructors or other `@Provides` methods). The receiver itself should NOT have `@Inject` if it's provided by the module.

## Ed25519 verification on Android 10–12 (API 29–31)

`java.security.KeyFactory.getInstance("Ed25519")` throws `NoSuchAlgorithmException: no such algorithm: Ed25519` on Android 10–12 because Ed25519 isn't natively supported until Android 13 (API 33).

**Fix:** Use Google Tink's `Ed25519Verify` instead of JCA. Add `implementation("com.google.crypto.tink:tink-android:1.7.0")` and:
```kotlin
val verifier = Ed25519Verify(publicKeyBytes)
verifier.verify(sigBytes, payBytes)
```

## Tink Ed25519Verify expects raw 32-byte key, not DER

Tink's `Ed25519Verify` constructor expects the raw 32-byte Ed25519 public key. PEM X509/DER encoding has a ~12-byte ASN.1 header (total 44 bytes for a 32-byte key). Passing DER bytes throws `Given public key's length is not 32`.

**Fix:** Extract the last 32 bytes from the DER-decoded key:
```kotlin
if (derBytes.size > 32) {
    return derBytes.copyOfRange(derBytes.size - 32, derBytes.size)
}
```

## PEM key parsing with `\r` line endings

PEM keys with `\r\n` (Windows) line endings break `removeSuffix("-----END PUBLIC KEY-----")` because `\r` remains after the footer. After `replace(Regex("\\s"), "")`, the footer text gets concatenated with the base64 payload, producing `...Ai+A=---ENDPUBLICKEY-----` which fails base64 decoding.

**Fix:** Always `.trim()` the PEM string before stripping the header/footer:
```kotlin
val cleaned = pem
    .trim()
    .removePrefix(KEY_HEADER)
    .removeSuffix(KEY_FOOTER)
    .replace(Regex("\\s"), "")
```

## Compose BOM 2024.01.00 breaks CircularProgressIndicator at runtime

`implementation(platform("androidx.compose:compose-bom:2024.01.00"))` compiles fine but crashes on any screen showing an indeterminate `CircularProgressIndicator` with `NoSuchMethodError: KeyframesSpec$KeyframesSpecConfig.at()`. The crash is in Material3's animation spec, not your code.

**Fix:** Upgrade to `2024.02.02` or later. The error is a runtime crash, not a compile error, so `assembleDebug` succeeds but the app crashes on the loading screen.

## NavHost startDestination doesn't update after creation

Setting `startDestination` on a `NavHost` after the host has been created does NOT recreate the host with the new destination. The host captures the destination at first composition.

**Fix:** Use `key(dest)` around the NavHost so it recreates when `dest` changes:
```kotlin
key(dest) {
    AppNavHost(startDestination = dest, ...)
}
```

## PairingViewModel instance isolation across NavBackStackEntries

When `MainScreen` and `PairingScreen` are separate composable destinations, each NavBackStackEntry gets its own `PairingViewModel` instance via `hiltViewModel()`. State changes in one screen's ViewModel are not visible to the other.

**Fix:** Read the ViewModel state reactively in `MainScreen` via `collectAsState()` and trigger navigation with `LaunchedEffect(state.status)` (NOT `LaunchedEffect(Unit)` — that only runs once):
```kotlin
val pairingState by pairingViewModel.state.collectAsState()
LaunchedEffect(pairingState.status) {
    if (pairingState.status is UiState.Success) {
        startDestination = Screen.Dashboard.route
    }
}
```

## BouncyCastle bcprov + bcpkix META-INF conflict

Adding both `org.bouncycastle:bcprov-jdk18on` and `org.bouncycastle:bcpkix-jdk18on` causes `mergeDebugJavaResource` to fail with "3 files found with path `META-INF/versions/9/OSGI-INF/MANIFEST.MF`".

**Fix:** Use only one, or add `packagingOptions { resources.pickFirsts += "META-INF/**" }`. For Ed25519, prefer Tink (`com.google.crypto.tink:tink-android`) over BouncyCastle to avoid this conflict entirely.

## serverUrl for adb reverse connections

When connecting to a local server via `adb reverse tcp:8443 tcp:8443`, `PairingStore.serverUrl` should use `127.0.0.1` instead of the Tailscale hostname, or the IP directly if it's a Tailscale IP (`100.x.y.z`).

**Fix:**
```kotlin
val serverUrl: String
    get() {
        val targetIp = ip?.let { if (it.startsWith("100.")) it else host } ?: host
        return "http://$targetIp:$port"
    }
```
