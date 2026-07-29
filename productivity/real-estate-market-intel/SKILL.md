---
name: real-estate-market-intel
description: "Use when researching markets. Demographics, comps, schools."
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [real-estate, market-research, neighborhood-analysis, demographics]
    related_skills: [real-estate-cma-generator, real-estate-property-analysis]
---

# Real Estate Market Intelligence

Multi-source market research for real estate agents, investors, and analysts. Gather property data, Census demographics, school ratings, crime statistics, employment trends, and compile everything into professional neighborhood profile sheets.

## When to Use

- Advising a client on which neighborhood to buy in
- Pricing a listing and needing market context
- Writing a market report or blog post on local conditions
- Evaluating an out-of-state or unfamiliar market
- Preparing for a listing appointment with hyperlocal data
- Deciding between two comparable neighborhoods

## Workflow

### 1. Data Sources & Query Strategy

| Data Domain | Best Sources | How to Access |
|---|---|---|
| Property Values & Comps | Zillow Research, Redfin Data Center, local MLS | `web_extract` on public data pages |
| Demographics | US Census Bureau (ACS), Census Reporter | API + `web_extract` |
| Schools | GreatSchools.org, Niche, Schooldigger | `web_extract` |
| Crime | AreaVibes, NeighborhoodScout, local PD reports | `web_search` + `web_extract` |
| Employment / Economy | BLS, FRED, local EDD | API or `web_extract` |
| Walkability / Transit | Walk Score, Redfin Walk Score API | `web_extract` |
| Zillow Home Value Index | fred.stlouisfed.org (ZHVI series) | `web_extract` CSV data |
| Neighborhood Reviews | Niche, Nextdoor, City-Data, Reddit | `web_search` + `web_extract` |

### 2. Property & Market Data Scrape

Use `web_extract` to pull key market indicators:

```python
def fetch_market_data(zip_code, city, state):
    """Gather market-level indicators for an area."""
    data = {}

    # Zillow home value data via web extraction
    zillow_url = f"https://www.zillow.com/home-values/{zip_code}/"
    # Redfin data center
    redfin_url = f"https://www.redfin.com/zip/{zip_code}"

    return data

# Example usage
market_data = fetch_market_data("90210", "Beverly Hills", "CA")
```

### 3. Demographic Profile

Use the Census Bureau's American Community Survey (ACS) via API:

```bash
# Get median household income, population, age distribution, housing data
# Census API endpoints:
# ACS 5-year estimates: https://api.census.gov/data/2023/acs/acs5
# Key variable groups:
#   B19013_001E - Median household income
#   B01003_001E - Total population
#   B25077_001E - Median home value
#   B25064_001E - Median gross rent
#   B25002_001E - Occupied housing units
#   B23025_005E - Unemployment count

curl "https://api.census.gov/data/2023/acs/acs5?get=NAME,B19013_001E,B01003_001E,B25077_001E,B25064_001E&for=zip%20code%20tabulation%20area:90210" | python -m json.tool
```

Build a demographic profile function:

```python
import urllib.request
import json

def census_demographics(zip_code):
    """Fetch key demographics for a ZIP code from Census ACS."""
    vars_list = [
        "NAME",
        "B19013_001E",   # Median household income
        "B01003_001E",   # Total population
        "B25077_001E",   # Median home value
        "B25064_001E",   # Median gross rent
        "B25002_001E",   # Occupied housing units
        "B23025_005E",   # Unemployed
        "B23025_002E",   # In labor force
    ]
    vars_str = ",".join(vars_list)
    url = f"https://api.census.gov/data/2023/acs/acs5?get={vars_str}&for=zip%20code%20tabulation%20area:{zip_code}"
    try:
        req = urllib.request.urlopen(url)
        rows = json.loads(req.read())
        if len(rows) > 1:
            col_names = rows[0]
            values = rows[1]
            demo = dict(zip(col_names, values))
            # Compute unemployment rate
            labor_force = int(demo.get('B23025_002E', 0))
            unemployed = int(demo.get('B23025_005E', 0))
            demo['unemployment_rate'] = round(unemployed / labor_force * 100, 1) if labor_force else 0
            return demo
    except Exception as e:
        return {"error": str(e)}
    return None

# Usage
demo = census_demographics("90210")
print(json.dumps(demo, indent=2))
```

### 4. School Ratings

Pull school data from GreatSchools.org:

```python
def fetch_school_ratings(zip_code):
    """Search for school ratings in a ZIP code area."""
    # Example using web extraction
    # In practice, GreatSchools requires scraping their public pages
    search_results = web_search(f"greatschools.org {zip_code} elementary school ratings")
    # Then extract ratings from the linked pages
    print(f"School data for {zip_code}:")
    for result in search_results:
        print(f"  - {result.title}")
    return search_results
```

Build an organized school summary:

| School Name | Type | Rating (1-10) | Enrollment | Student/Teacher Ratio |
|---|---|---|---|---|
| Lincoln Elementary | Public | 8 | 520 | 18:1 |
| Washington Middle | Public | 7 | 680 | 20:1 |
| Jefferson High | Public | 9 | 1200 | 22:1 |

### 5. Crime Statistics

Research crime data for the area:

```python
def crime_profile(city, state, zip_code):
    """Assemble crime statistics from multiple public sources."""
    print(f"\n=== CRIME PROFILE: {zip_code} ===")

    # AreaVibes crime data
    url = f"https://www.areavibes.com/{city.lower()}-{state.lower()}/crime/"
    print(f"1. AreaVibes: {url}")
    print("   - Overall crime grade (A-F)")
    print("   - Violent crime rate per 100k")
    print("   - Property crime rate per 100k")
    print("   - Compare to national average")

    # NeighborhoodScout
    ns_url = f"https://www.neighborhoodscout.com/{state.lower()}/{city.lower()}/crime"
    print(f"2. NeighborhoodScout: {ns_url}")
    print("   - Crime per 100k residents")
    print("   - Annual crime count by type")
    print("   - Safety percentile rank")

    # FBI UCR data
    print("3. FBI Uniform Crime Reporting (national level)")
    print("   - https://ucr.fbi.gov/crime-in-the-u.s")
    return {"city": city, "state": state, "zip": zip_code}
```

### 6. Employment & Economic Trends

Pull employment data from the Bureau of Labor Statistics:

```bash
# BLS API for local area unemployment statistics (LAUS)
# Series ID format: LAUCN<area_code>0000000003 (unemployment rate)
# Area codes available at: https://www.bls.gov/cew/classifications/areas/area-titles.csv

# FRED API - Federal Reserve Economic Data
# ZHVI (Zillow Home Value Index) series
# Payroll employment by MSA
curl "https://api.stlouisfed.org/fred/series/observations?series_id=MSANB906URN&api_key=YOUR_API_KEY&file_type=json"
```

### 7. Build Neighborhood Profile Sheet

Compile all data into a readable sheet:

```python
def neighborhood_profile(zip_code, city, state):
    """Generate a comprehensive neighborhood profile."""
    print("=" * 70)
    print(f"NEIGHBORHOOD PROFILE: {city.upper()}, {state}  {zip_code}")
    print("=" * 70)

    # Demographics
    demo = census_demographics(zip_code)
    if demo and 'error' not in demo:
        print(f"\nDEMOGRAPHICS")
        print(f"  Population:               {demo.get('B01003_001E', 'N/A')}")
        print(f"  Median Household Income:  ${int(demo.get('B19013_001E', 0)):,}")
        print(f"  Median Home Value:        ${int(demo.get('B25077_001E', 0)):,}")
        print(f"  Median Gross Rent:        ${int(demo.get('B25064_001E', 0)):,}")
        print(f"  Unemployment Rate:        {demo.get('unemployment_rate', 'N/A')}%")

    # Market conditions
    print(f"\nMARKET CONDITIONS")
    print(f"  Walk Score:               TBD (web search)")
    print(f"  Transit Score:            TBD (web search)")
    print(f"  Bike Score:               TBD (web search)")
    print(f"  Avg Days on Market:       TBD (local MLS)")
    print(f"  Price per Sq Ft:          TBD (local MLS)")

    # Run web searches for walkability
    search_walk = web_search(f"walk score maps {zip_code} walkability")
    if search_walk:
        print(f"  Walk Score Ref:           {search_walk[0].url}")

    print(f"\nSCHOOLS")
    print(f"  TBD — run fetch_school_ratings({zip_code})")

    print(f"\nCRIME")
    print(f"  TBD — run crime_profile('{city}', '{state}', '{zip_code}')")

    print("\n" + "=" * 70)
    return {"zip": zip_code, "city": city, "state": state}
```

### 8. Market Trend Analysis

Track year-over-year trends:

```python
def market_trends(zip_code, months_back=12):
    """Analyze price trends, inventory, and days on market."""
    print(f"\n=== MARKET TRENDS: {zip_code} ===")
    print(f"Period: Past {months_back} months")

    # Key data points to gather:
    # 1. Median sale price (current vs 12 months ago)
    # 2. Number of sales (current vs 12 months ago)
    # 3. Average days on market
    # 4. Sale-to-list price ratio
    # 5. Inventory levels (active listings)
    # 6. Months of supply
    # 7. Price reductions (% of listings)

    # Web search for recent market reports
    results = web_search(f"{zip_code} real estate market report 2025 2026")
    print("Recent market reports:")
    for r in results:
        print(f"  - {r.title}")
        print(f"    {r.url}")

    return {"zip": zip_code, "search_results": results}
```

### 9. Investment Suitability Score

Score a neighborhood across key investment dimensions:

```python
def investment_score(demographics, school_ratings, crime_data, market_trends):
    """
    Score a neighborhood 1-10 on each dimension and return composite.
    10 = best for investment, 1 = worst.
    """
    scores = {}

    # Income score: higher median income = stronger rental pool
    med_income = int(demographics.get('B19013_001E', 0))
    scores['income'] = min(10, max(1, med_income / 15000))

    # Home value appreciation
    # Placeholder — needs year-over-year comparison
    scores['appreciation'] = 5

    # School score
    # Placeholder — needs GreatSchools data
    scores['schools'] = 5

    # Crime score (inverted: lower crime = higher score)
    scores['safety'] = 7

    # Employment score
    unemp = demographics.get('unemployment_rate', 5)
    scores['employment'] = max(1, 10 - unemp * 2)

    # Composite
    weights = {'income': 0.20, 'appreciation': 0.25, 'schools': 0.20,
               'safety': 0.20, 'employment': 0.15}
    composite = sum(scores[k] * weights[k] for k in weights)
    scores['composite'] = round(composite, 1)

    print("\nINVESTMENT SUITABILITY SCORE")
    for dim in ['income', 'appreciation', 'schools', 'safety', 'employment']:
        print(f"  {dim.capitalize():15s}: {scores[dim]}/10")
    print(f"  {'Composite':15s}: {scores['composite']}/10")

    return scores
```

## Common Pitfalls

- **Relying on a single data source**: Cross-validate property values, crime, and schools from at least 2 sources. Zillow Zestimates can be off by 5-15%.
- **Using outdated Census data**: ACS 5-year estimates lag by 2-3 years. Always check the survey year. Use ACS 1-year estimates for large metro areas (more current).
- **Confusing ZIP code with neighborhood**: ZIP code boundaries don't align with neighborhood boundaries. Pull data at the tract or block group level for precision.
- **Ignoring school boundaries**: GreatSchools ratings may not match actual attendance zones. Verify with the school district's boundary map.
- **Overweighting crime stats**: Crime data has reporting bias. Compare per-capita rates, not raw counts. Check trend data (2-3 years), not just a single year.
- **Forgetting seasonality**: Housing market data is seasonal. Compare same-month year-over-year, not month-over-month.
- **Neglecting supply-side data**: New construction permits, zoning changes, and development pipelines affect future values. Check city planning department websites.
- **Not verifying walk scores**: Walk Score can be inaccurate in suburban areas. Verify by looking at actual amenities within 1 mile.
- **Blending MSAs incorrectly**: Large metros have vastly different submarkets. A downtown zip and exurb zip in the same MSA are not comparable.

## Verification Checklist

- [ ] Median household income, population, and median home value pulled from Census ACS
- [ ] School ratings gathered from GreatSchools or Niche for at least top-3 schools
- [ ] Crime data collected (violent + property crime rates, vs. national average)
- [ ] Walk/transit/bike scores checked and noted
- [ ] Median sale price and price/sq ft from MLS or Redfin Data Center
- [ ] Year-over-year appreciation trend confirmed
- [ ] Average days on market and sale-to-list ratio checked
- [ ] Unemployment rate and major employers identified
- [ ] New construction / development pipeline researched
- [ ] Neighborhood profile sheet compiled and formatted
- [ ] Data sources documented with timestamps
- [ ] At least 2 independent sources cross-referenced per data point