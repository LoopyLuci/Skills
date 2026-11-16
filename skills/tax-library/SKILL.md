---
name: tax-library
description: Build tax model and Room database with search.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [tax, android, room, room-dao, search, navigation]
    category: data-model
    related_skills: [android-kotlin-build-pitfalls]
---

# Taxes Library Feature

## Trigger

Use when building the Taxes Library feature in SpendingSaver Android:
- Adding tax data model (country/state/town/level tax details)
- Creating Room DAO, database, and repository for tax data
- Adding navigation routes from settings or main screen to tax features
- Integrating search and detailed tax breakdowns

## Scope (exhaustive)

The Taxes Library must include:
1. **Data model** — `TaxType` enum (20+ types), `TaxCountry`, `TaxState`, `TaxTown`, `TaxDetail`, `TaxRecord`, `TaxFiling`, `TaxAudit`
2. **Room persistence** — `TaxDao` (CRUD + flows), `TaxDatabase` (sqlite db + migrations)
3. **Repository** — `TaxRepository` interface + implementation with factory methods
4. **Search** — `SearchableTax` projection with category-based filtering
5. **UI** — Country browser, jurisdiction detail, town detail, tax detail viewer, search screen
6. **Navigation** — Routes from settings or main screen to tax features

## Data Model

### TaxType (enum)
- Categories: `income`, `consumption`, `property`, `payroll`, `corporate`, `capital_gains`, `inheritance`, `vat`, `sales`, `other`
- Fields: `code`, `taxName` (display name), `category`, `appliesTo` (individuals/businesses/both), `filingFrequency`, `declarationRequired`
- DO NOT name a property `name` on an enum — it shadows `Enum.name` and causes compile errors. Use `taxName` instead.

### Entity types
- `TaxCountry`: isoCode, name, taxAuthority, taxYearStart, currency, isManaged
- `TaxState`: countryId, name, code
- `TaxTown`: stateId, name
- `TaxDetail`: countryId, stateId, townId, taxType, rate, threshold, filingRequirements, deductions, credits, notes
- `TaxRecord`: countryId, stateId, townId, transactionId, taxType, taxAmount, rateApplied, taxPeriod
- `TaxFiling`: countryId, stateId, taxYear, filingStatus, filingDate, totalIncome, totalTax, totalDeductions, totalCredits, refundDue, balanceDue, status
- `TaxAudit`: countryId, taxType, action, oldData, newData, changedBy, changedAt

## Room Setup

### Package structure rule (CRITICAL)

**ALL files must live in the SAME package as the entity types** (`com.spendingsaver.tax`).
- `TaxLibrary.kt` (entities)
- `TaxDao.kt` (Room DAO)
- `TaxDatabase.kt` (@Database class)
- `TaxRepository.kt` (Repository interface + impl)

If `@Dao` is in a different package from `@Database`, KSP validates against the wrong schema and fails with `SQLITE_ERROR: no such table` or `[ksp] MissingType`.
- The generated `TaxDao_Impl.java` must be in the same package as the source files — KSP cache must be flushed with `./gradlew clean` before every build.

### DAO structure

1. Start with `@Dao` interface in the same package as the entity types
2. Each entity gets CRUD methods:
   - `insert(item): Long` (single insert, `@Insert(onConflict = REPLACE)`)
   - Query methods returning Flow for reactive UI
   - Query methods returning List for sync access in suspend functions
3. **DO NOT add `insertAll(List<T>)` methods** to the DAO — KSP generates `insertAll(List<T>)` with a `$completion: Continuation<Unit>` parameter, causing `Conflicting declarations` or `Type mismatch` errors
4. Separate `insertAll` from the Repository — only the DAO defines it; the Repository only defines individual `insert(item)`

### DAO pitfalls

- **Orphaned `@Insert` annotations** — After deleting a method, also delete the corresponding annotation line. Orphaned annotations cause `An abstract DAO method must be annotated with one and only one of the following annotations`.
- **Flow<List<T>> in suspend functions** — Calling `.first()` or `.toList()` on a `Flow<List<T>>` receiver in a suspend function causes `Unresolved reference` or receiver type mismatch. Use `collect { list.addAll(it) }` inside a suspend function.
- **Class naming collision** — Do NOT name the Repository class `TaxRepository` — the compiler confuses a `class TaxRepository(private val dao: TaxDao)` with `interface TaxDao`. Name the impl `TaxRepositoryImpl`.
- **KSP cache** — After any DAO or `@Database` edit, run `./gradlew clean` before `assembleDebug`. Incremental builds do NOT clear the KSP cache.

## Database

### TaxDatabase
- `@Database` annotation with all 7 entity types
- `abstract fun taxDao(): TaxDao`
- Singleton pattern with `getInstance(context: Context)`
- Database name: `taxes.db`

## Repository

### Structure

1. `TaxRepository` interface defines all data access methods
2. `TaxRepositoryImpl` class implements the interface
3. Factory function: `fun createTaxRepository(context: Context): TaxRepository` (or `extension fun Context.createTaxRepository()`)

### Method patterns

- `observeCountries()`: Flow<List<TaxCountry>>
- `getCountryByCode(isoCode)`: suspend fun → TaxCountry?
- `getAllCountries()`: suspend fun → List<TaxCountry> (use collect, not first/toList)
- `insertCountry(country)`: suspend fun → Long

## Search

### SearchableTax projection

- Data class for searchable tax items
- Fields: `id`, `country`, `state`, `town`, `taxType`, `rate`, `threshold`, `description`, `category`
- Used by UI for search results and category filtering

### Query patterns

- Search by countryId with LIKE query on filingRequirements, deductions, credits, notes
- Search across all countries with `observeAllCountries()` + map to `SearchableTax`

## UI

### Screen flow

1. `TaxCountryBrowserScreen` — list of countries (filter by isManaged)
2. `TaxStateListScreen` — list of states for selected country
3. `TaxTownDetailScreen` — list of towns for selected state
4. `TaxDetailDetailScreen` — detailed breakdown of tax types for selected jurisdiction
5. `TaxSearchScreen` — search across all jurisdictions and tax types

### Navigation

- Add routes to `MainActivity` NavHost:
  - `tax-countries`
  - `tax-stats` (country detail)
  - `tax-states/{countryId}` (state detail — extract via `backStackEntry.arguments`)
  - `tax-towns` (town detail)
  - `tax-search`

### Screen composable pitfalls

- **Screen composable signature must match navigation argument extraction.** When using `{param}` routes, the composable lambda receives `backStackEntry` — extract params from `backStackEntry.arguments`, not as function parameters.
- **Do NOT use `CenterAlignedTopAppBar`** — it is not a valid composable for a screen top bar. Use `TopAppBar` with a `title` lambda.
- **Place composable invocations inside `@Composable` functions only.** A `Column { ... }` must not be placed outside a composable context (e.g., inside a `when` branch as a raw statement).
- **Import `androidx.compose.foundation.background`** — the `.background()` modifier is NOT available from `androidx.compose.ui.Modifier` alone.

## Integration

### Settings integration
- Add `aiServiceUrl` to `AppSettings` data class
- Add `setAiServiceUrl` to `SettingsRepository`
- Display AI service status in AI settings screen (READY / FAILED)

### AppModule DI
- Add `@Provides` methods:
  - `provideOkHttpClient(): OkHttpClient`
  - `provideAiClient(OkHttpClient): AiClient`
  - `provideAiRepository(AiClient): AiRepository`

## Testing (unit tests for taxes)

1. Unit tests run via `./gradlew :app:testDebugUnitTest` from `SpendingSaverAndroid`.
2. **Test data**: `AiResponse` (in `AiIntent.kt`) requires `success: Boolean` — always provide it.
3. **Test dependencies**: Ensure `app/build.gradle.kts` has `testImplementation("junit:junit:4.13.2")`, `testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.6.4")`, and `testImplementation("io.mockk:mockk:1.13.7")`.
4. **Test context**: If testing classes that need `Context`, provide a mock `Context` with mocked `SharedPreferences` (implement the full `Context` abstract class or use a stub).
5. **Test assertions**: Use `assertEquals(expected, actual)` — order matters for error messages.
6. **Run tests with `./gradlew clean :app:testDebugUnitTest`** after test file changes.

## AI Engine Host Setup (updated from session learnings)

- Use HermESC-managed Python 3.14.9+202**1021 venv at `/c/Users/Server/AppData/Local/hermes/tools/python-3.14.9+202**1021-win32-x64/python3`.
- The venv has `cactus-compute` installed (cactus, Mirage, Whistle confirmed accessible via HTTP).
- Default `HERMES_PYTHON` env override for alternative Python paths.

## Priority & scope (user preference)

1. **Mobile app first, Nokia 7.2 test target** — Verify on `com.spendingsaver` process via `adb`.
2. **No Kindle device/package** — Verify `pm list packages | grep -i kindle` returns empty.
3. **CI/CD green gate is a precondition** — `./ci/run.sh all` must be green before shipping feature work.
4. **Full AI/multimodal integration** — Host engine (Cactus + prism-ml + image-studio) → Android AI SDK (typed HTTP) → app.
5. **Local AI engine** — Host Python 3.14.9+202**1021 venv has `cactus-compute` installed.
6. **No NDK** — Native JNI/Cactus build is blocked; use HTTP SDK.
7. **Exhaustive scope, not minimal** — Complete every roadmap item, do not trim.
8. **Credential handling** — API keys, tokens, passwords, secrets must NEVER appear in summaries; replaced with `[REDACTED]`.
9. **Gradle `GRADLE_OPTS` must supply ONLY JVM memory options** — `-Xmx4096m -XX:MaxMetaspaceSize=512m` — not CLI flags (`-x -no-daemon --console=plain --build-cache` crash JVM with `Unrecognized option: -x`).
10. **Do not commit credentials, local configuration, private account data, generated build output, or local logs.**

## Testing

1. Unit tests for AI SDK (`AiClientTest.kt`, `AiRepositoryTest.kt`) run via `./gradlew :app:testDebugUnitTest`.
2. Integration tests: start the local Python AI engine host, then call Android SDK endpoints via device network.
3. Mock `OkHttpClient` when testing repository layer.

## References

- `ai-integration-procedure.md` — detailed AI SDK implementation procedure
- `android-kotlin-build-pitfalls` — Kotlin language and build pitfalls
- `ai-service/README.md` — AI SDK architecture
- `ci/README.md` — CI/CD pipeline documentation
- `ai-integration-procedure.md` — implementation procedure for AI SDK (cactus, mirage, whistle, prism-ml, image-studio)

## New learnings (2026-11-16)

- **Taxes Library is fully delivered** — clean `assembleDebug` PASSED (40 tasks, 1m 40s, exit 0); 12/12 unit tests green
- **AI SDK in-app integration complete** — MainViewModel wired, AISettingsScreen, AIComponents, DI module done
- **Build verification pattern**: `./gradlew clean assembleDebug` then `./gradlew :app:testDebugUnitTest` after any file change
- **Room+DAO package rule**: ALL DAO and @Database files must be in the same package as entity types (com.spendingsaver.tax) — KSP validates against the wrong schema if not
- **KSP + insertAll pitfall**: Never add `insertAll(List<T>)` to a DAO; KSP generates `insertAll(List<T>, Continuation<Unit>)` causing conflicts
- **Orphaned annotations**: After deleting a DAO method, also delete its annotation line
- **Flow<List<T>> in suspend**: Use `collect { list.addAll(it) }` inside suspend functions
- **Gradle memory**: GRADLE_OPTS must supply ONLY JVM memory options (`-Xmx4096m -XX:MaxMetaspaceSize=512m`); never add CLI flags