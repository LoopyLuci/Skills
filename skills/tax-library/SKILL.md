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

### Package structure rule

**MOVE DAO, DATABASE, AND REPOSITORY INTO ONE PACKAGE.** All three files must live in the same package as the entity types (`com.spendingsaver.tax`).

If the `@Dao` is in a different package from the `@Database` class, KSP validates the DAO queries against the wrong schema and fails with `SQLITE_ERROR: no such table` or `[ksp] MissingType`.

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
- **KSP cache** — After any DAO or `@Database` edit, run `./gradlew clean` before `assembleDebug`. Incremental builds do not clear the KSP cache.

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
  - `tax-states` (state detail)
  - `tax-towns` (town detail)
  - `tax-search`

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

## Testing

1. Unit tests for TaxRepository (in-memory DAO mock)
2. `./gradlew :app:testDebugUnitTest` to run all unit tests
3. Verify `./gradlew clean assembleDebug` build succeeds

## Priority & scope (user preference)

1. **Mobile app first, Nokia 7.2 test target** — verify via `adb`
2. **CI/CD green gate is a precondition** — `./ci/run.sh all` must be green
3. **Exhaustive scope, not minimal** — complete every roadmap item
4. **Credential handling** — never include API keys, tokens, passwords, or secrets in summaries; replace with `[REDACTED]`
5. **Build memory** — `org.gradle.jvmargs=-Xmx4096m` in gradle.properties; `GRADLE_OPTS="-Xmx4096m -XX:MaxMetaspaceSize=512m"` in ci/config.sh
6. **Gradle GRADLE_OPTS only JVM memory options** — not CLI flags
