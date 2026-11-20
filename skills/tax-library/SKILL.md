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
2. **Test template for Room + MockK + JUnit 5** (use for all repository DAO tests):

   ```kotlin
   internal class TaxRepositoryTest {
       @Test
       fun testName() = runTest {
           // IMPORTANT: coEvery must be INSIDE each test method, never top-level
           coEvery { TaxDatabase.getInstance(any()) } returns mockk<TaxDatabase>()
           
           val dao = mockk<TaxDao>(relaxed = true)
           every { dao.someMethod() } returns flowOf(...)   // non-suspend, use `every`
           // coEvery is for suspend functions only; use `every` for non-suspend
           
           val context = mockk<android.content.Context>(relaxed = true)
           val repository = TaxRepository(context, dao)
           
           // assertions
       }
   }
   ```

3. **Missing imports that cause `Unresolved reference` errors:**
   - `import kotlinx.coroutines.test.runTest` — `runTest { }` block
   - `import androidx.annotation.RuntimeEnvironment` — `RuntimeEnvironment.application` for a real Context (Room needs a non-null Context)
   - `import io.mockk.every` — `every { ... }` for non-suspend DAO method stubs
   - `import io.mockk.coEvery`, `import io.mockk.coVerify` — coroutine-aware stubs for suspend functions

4. **Gradle `clean` deadlock workaround**: `gradle clean` can fail with `New files were found` / "New files were found" (locked build files). Workaround: run `gradle clean` alone until it succeeds, then run `gradle assembleDebug` fresh.
5. **Read test results for failure diagnostics**: Check `app/build/test-results/testDebugUnitTest/TEST-*.xml` for detailed failure messages and stack traces.
6. **Seed data consistency**: `coVerify(exactly = N)` counts must match the actual seed data insertions. After changing `seedTaxData()`, review every `coVerify(exactly = N)` and recount the insertions:
   - 1 `insertCountry` call → 1 `coVerify(exactly = 1) { taxDao.insertCountry(any()) }`
   - `insertState` calls accumulate all states (each call is one state)
   - `insertTown` calls accumulate all towns
   - `insertDetails` (bulk) → 1 call → 1 `coVerify(exactly = 1) { taxDao.insertDetails(any()) }`
   - `insertRecord` calls accumulate records
   - `insertFiling` calls accumulate filings
   - `insertAudit` calls accumulate audits
7. **`TaxTown` constructor has NO `country_code` parameter** — only `state_id`, `town_code`, `town_name`, `county`, `is_city`, `is_town`, `id`. Do NOT pass `country_code` to `TaxTown`.
8. **`TaxRepository` constructor**: `@Inject constructor(private val context: Context, private val taxDao: TaxDao)` — a field `private val taxDatabase = TaxDatabase.getInstance(context)` in the constructor is NOT used by repository methods (all methods use `taxDao`). For unit tests, intercept `TaxDatabase.getInstance(any())` with `coEvery { TaxDatabase.getInstance(any()) } returns mockk<TaxDatabase>()` so the constructor does not create a real database.