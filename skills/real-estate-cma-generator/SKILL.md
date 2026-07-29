---
name: real-estate-cma-generator
description: "Comparative market analysis. Comps, adjustments, pricing."
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [real-estate, cma, pricing, comparative-market-analysis, valuation]
    related_skills: [real-estate-property-analysis, real-estate-market-intel]
---

# Comparative Market Analysis (CMA) Generator

Professional, data-driven Comparative Market Analysis for residential real estate. Find comparable sold listings, apply adjustments for differences, determine a recommended price range with confidence levels, and generate a CMA report.

## When to Use

- A seller asks "What's my home worth?"
- Preparing a listing presentation
- A buyer needs help determining a fair offer price
- Reviewing an appraisal for accuracy
- Repricing a stale listing

## Key CMA Concepts

| Term | Definition |
|---|---|
| **Comparable (Comp)** | A recently sold property similar to the subject property |
| **Active Listing** | A property currently on the market (competition, not comp) |
| **Pending/Under Contract** | A property under agreement but not yet closed (indicator of market direction) |
| **Expired/Withdrawn** | A property that didn't sell (pricing ceiling indicator) |
| **Adjustment** | Dollar value added or subtracted from a comp to account for differences vs. subject |
| **Price Range** | Low-to-high valuation based on adjusted comp values |
| **Confidence Level** | How reliable the CMA is (High/Medium/Low) based on comp proximity and quantity |

## Workflow

### 1. Gather Subject Property Data

```
Address:
Property Type:
Bedrooms:
Bathrooms:
Square Footage (above grade):
Lot Size (acres or sq ft):
Year Built:
Garage (# of cars):
Basement (finished/unfinished/none):
HVAC (central/radiant/window):
Roof (material, age):
Exterior (brick, siding, stucco, etc.):
Condition (Excellent/Good/Fair/Poor):
Special Features (pool, view, waterfront, fireplace, etc.):
Recent Updates/Remodeling (year, scope):
HOA (monthly fee, amenities):
Tax Assessed Value:
Last Sale Date (if known):
Last Sale Price (if known):
```

### 2. Find Comparable Sales

Search for 3-6 comparable sold properties within:
- **Radius**: 0.25 mi for dense urban, 0.5-1 mi for suburban, 1-3 mi for rural
- **Time frame**: Sold within last 6 months (extend to 12 months in slow markets)
- **Size range**: ±20% square footage ideally, ±30% acceptable
- **Bedrooms**: Same ± 1 bedroom
- **Property type**: Same type (never comp a condo to a single-family)
- **Age range**: ±10 years for similar construction era

```python
def search_comps(subject, max_results=6):
    """
    Search for comparable sold properties using web sources.
    subject: dict with address, beds, baths, sqft, type, zip, etc.
    """
    print(f"Searching for comps for: {subject.get('address')}")
    print(f"  Type: {subject.get('type')}  Beds: {subject.get('beds')}  SqFt: {subject.get('sqft')}")
    print()

    # Search local MLS/public data
    query = f"sold recently {subject.get('zip')} {subject.get('beds')} bedroom {subject.get('type', 'home')}"
    results = web_search(query, limit=5)

    comps = []
    for result in results:
        comp = {
            'source': result.url,
            'title': result.title,
            'description': result.description,
        }
        comps.append(comp)
        print(f"  Found: {result.title}")
        print(f"    {result.url}")

    return comps
```

### 3. Build Comp Adjustment Grid

Adjust each comp's sale price for differences from the subject:

```python
def adjust_comp(comp_price, differences, subject):
    """
    Apply dollar adjustments to a comp to make it comparable to subject.
    differences: list of (feature, subject_value, comp_value, adjustment_per_unit)
    """
    adjusted_price = comp_price
    adjustments_log = []

    # Standard adjustment values (market-dependent — adjust for your area)
    standard_adjustments = {
        'sqft': 150,                 # $ per sq ft of above-grade living area
        'bedroom': 15000,            # $ per bedroom difference
        'bathroom': 10000,           # $ per bathroom difference
        'lot_size': 25000,           # $ per 0.25 acre difference
        'garage_car': 8000,          # $ per garage space
        'pool': 25000,               # $ for pool (vs. no pool)
        'fireplace': 3000,           # $ per fireplace
        'view': 30000,               # $ for premium view
        'waterfront': 75000,         # $ for waterfront
        'basement_finished': 20000,  # $ for finished basement
        'age_per_year': -1000,       # $ per year newer (subtract if comp is older)
        'condition_excellent': 20000, # $ for excellent condition
        'condition_good': 0,
        'condition_fair': -15000,
        'hoa_presence': 0,           # Already reflected in price
    }

    # Sq ft adjustment
    diff_sqft = subject.get('sqft', 0) - differences.get('sqft', 0)
    sqft_adj = diff_sqft * standard_adjustments['sqft']
    if abs(sqft_adj) > 500:
        adjusted_price += sqft_adj
        adjustments_log.append(f"SqFt: {'+' if sqft_adj > 0 else ''}${sqft_adj:,} (diff: {diff_sqft} sqft × ${standard_adjustments['sqft']})")

    # Bedroom adjustment
    diff_beds = subject.get('beds', 0) - differences.get('beds', 0)
    bed_adj = diff_beds * standard_adjustments['bedroom']
    if bed_adj != 0:
        adjusted_price += bed_adj
        adjustments_log.append(f"Beds: {'+' if bed_adj > 0 else ''}${bed_adj:,} ({diff_beds:+d} bed × ${standard_adjustments['bedroom']:,})")

    # Bathroom adjustment
    diff_baths = subject.get('baths', 0) - differences.get('baths', 0)
    bath_adj = diff_baths * standard_adjustments['bathroom']
    if bath_adj != 0:
        adjusted_price += bath_adj
        adjustments_log.append(f"Baths: {'+' if bath_adj > 0 else ''}${bath_adj:,} ({diff_baths:+d} bath × ${standard_adjustments['bathroom']:,})")

    # Garage adjustment
    diff_garage = subject.get('garage', 0) - differences.get('garage', 0)
    garage_adj = diff_garage * standard_adjustments['garage_car']
    if garage_adj != 0:
        adjusted_price += garage_adj
        adjustments_log.append(f"Garage: {'+' if garage_adj > 0 else ''}${garage_adj:,} ({diff_garage:+d} spaces)")

    # Age adjustment
    diff_age = subject.get('year_built', 2000) - differences.get('year_built', 2000)
    age_adj = diff_age * standard_adjustments['age_per_year']
    if abs(age_adj) > 1000:
        adjusted_price += age_adj
        adjustments_log.append(f"Age: {'+' if age_adj > 0 else ''}${age_adj:,} ({diff_age:+d} years)")

    return adjusted_price, adjustments_log
```

### 4. Complete CMA Calculation

```python
from datetime import datetime, timedelta
import json

def generate_cma(subject, comp_data_list):
    """
    Full CMA calculation.
    subject: dict of subject property details
    comp_data_list: list of comp data dicts
    """
    print("=" * 70)
    print(f"COMPARATIVE MARKET ANALYSIS")
    print(f"Subject: {subject.get('address', 'N/A')}")
    print(f"{'='*70}")

    # Subject summary
    print(f"\nSUBJECT PROPERTY")
    print(f"  {subject.get('beds', '?')}BR / {subject.get('baths', '?')}BA")
    print(f"  {subject.get('sqft', '?')} sq ft  |  Built {subject.get('year_built', '?')}")
    print(f"  Lot: {subject.get('lot_size', '?')}  |  Garage: {subject.get('garage', '?')}-car")
    print(f"  Condition: {subject.get('condition', 'N/A')}")
    if subject.get('features'):
        print(f"  Features: {', '.join(subject['features'][:5])}")
    print(f"\nADJUSTED COMPARABLES")

    # Process each comp
    adjusted_values = []
    for i, comp in enumerate(comp_data_list):
        differences = comp.get('differences', {})
        sale_price = comp.get('sale_price', 0)
        sale_date = comp.get('sale_date', 'N/A')

        adjusted_price, adjustments = adjust_comp(sale_price, differences, subject)
        adjusted_values.append(adjusted_price)
        net_adj = adjusted_price - sale_price

        print(f"\n  Comp {i+1}: {comp.get('address', 'N/A')}")
        print(f"  Sale Price: ${sale_price:>10,}  |  Sold: {sale_date}")
        print(f"  Stats: {differences.get('beds', '?')}BR / {differences.get('baths', '?')}BA  |  {differences.get('sqft', '?')} sq ft  |  Built {differences.get('year_built', '?')}")
        if adjustments:
            for adj in adjustments:
                print(f"    {adj}")
        print(f"  Adjusted Value: ${adjusted_price:>10,}")
        print(f"  Net Adjustment: {'+' if net_adj >= 0 else ''}${net_adj:,} ({net_adj/sale_price*100:.1f}%)")

    # Price range calculation
    if len(adjusted_values) >= 2:
        adj_sorted = sorted(adjusted_values)
        low = int(adj_sorted[len(adj_sorted)//4] if len(adj_sorted) >= 4 else adj_sorted[0])
        high = int(adj_sorted[-(len(adj_sorted)//4 or 1)-1] if len(adj_sorted) >= 4 else adj_sorted[-1])
        median = int(sorted(adjusted_values)[len(adjusted_values)//2])
        avg_val = int(sum(adjusted_values) / len(adjusted_values))
    else:
        low = int(min(adjusted_values))
        high = int(max(adjusted_values))
        median = int(adjusted_values[0])
        avg_val = median

    # Price per sq ft analysis
    subject_ppsf = subject.get('price_target', median) / subject.get('sqft', 1)
    comp_ppsfs = [v / c.get('sqft', 1) for v, c in zip(adjusted_values, comp_data_list) if c.get('sqft', 0) > 0]
    avg_ppsf = sum(comp_ppsfs) / len(comp_ppsfs) if comp_ppsfs else 0

    print(f"\n{'='*70}")
    print(f"PRICE RECOMMENDATION")
    print(f"{'='*70}")
    print(f"  Adjusted Range:      ${low:,} – ${high:,}")
    print(f"  Median Adjusted:     ${median:,}")
    print(f"  Average Adjusted:    ${avg_val:,}")
    print(f"  Avg Price/Sq Ft:     ${avg_ppsf:,.0f}")
    print(f"  Subject Est PPSF:    ${subject_ppsf:,.0f}")

    # Confidence assessment
    comp_count = len(comp_data_list)
    comp_spread = high - low
    spread_pct = comp_spread / avg_val * 100 if avg_val else 0

    if comp_count >= 5 and spread_pct < 10:
        confidence = "High"
    elif comp_count >= 3 and spread_pct < 15:
        confidence = "Medium"
    else:
        confidence = "Low"

    print(f"\n  Confidence Level:    {confidence}")
    print(f"  # of Comps:          {comp_count}")
    print(f"  Value Spread:        {spread_pct:.1f}%")

    # Suggested list price if selling
    if subject.get('purpose') == 'listing':
        list_price = int(median * 1.02)  # Price 2% above median for negotiation room
        print(f"\n  Suggested List Price: ${list_price:,}")
        print(f"  Price per Sq Ft:     ${list_price/subject.get('sqft', 1):,.0f}")

    return {
        'range': (low, high),
        'median': median,
        'average': avg_val,
        'avg_ppsf': round(avg_ppsf, 0),
        'confidence': confidence,
        'adjusted_comps': adjusted_values,
        'suggested_list': int(median * 1.02) if subject.get('purpose') == 'listing' else None,
    }
```

### 5. CMA Report Template

Generate a professional CMA PDF:

```python
def print_cma_report(subject, comp_data_list, cma_result):
    """Print a formatted CMA report to display or export."""
    print("\n")
    print("=" * 70)
    print("  PROFESSIONAL COMPARATIVE MARKET ANALYSIS")
    print("=" * 70)
    print(f"  Date: {datetime.now().strftime('%B %d, %Y')}")
    print(f"  Subject: {subject.get('address')}")
    print(f"  Prepared for: {subject.get('client_name', 'Client')}")
    print(f"  Prepared by: {subject.get('agent_name', 'Your Agent')}")
    print("-" * 70)
    print(f"  SUBJECT PROPERTY")
    print(f"    {subject.get('beds')} bd / {subject.get('baths')} ba / {subject.get('sqft')} sq ft")
    print(f"    Built: {subject.get('year_built')}  |  Lot: {subject.get('lot_size')}")
    print(f"    Condition: {subject.get('condition')}")
    print()
    print(f"  VALUE CONCLUSION")
    print(f"    Estimated Value:            ${cma_result['median']:,}")
    print(f"    Value Range:               ${cma_result['range'][0]:,} – ${cma_result['range'][1]:,}")
    print(f"    Average Price per Sq Ft:    ${cma_result['avg_ppsf']:.0f}")
    print(f"    Confidence:                 {cma_result['confidence']}")
    print()
    print(f"  COMP SUMMARY")
    print(f"    {'#':>3} {'Address':<30} {'Price':>12} {'Adj Value':>12} {'%Adj':>7}")
    print(f"    {'-'*63}")
    for i, (comp, adj_val) in enumerate(zip(comp_data_list, cma_result['adjusted_comps'])):
        pct = (adj_val - comp['sale_price']) / comp['sale_price'] * 100
        addr_short = comp.get('address', 'N/A')[:28]
        print(f"    {i+1:>3} {addr_short:<30} ${comp['sale_price']:>8,} ${adj_val:>8,} {pct:>+6.1f}%")
    print("-" * 70)
```

### 6. Quick CMA from Web Data

For a rapid CMA without manual comp entry:

```bash
# Use web search to find comps for a subject address
# Then extract key data points from Redfin or Zillow
curl -s "https://www.redfin.com/zipcode/78701" | python3 -c "
import sys
html = sys.stdin.read()
# Parse for recent sales data
print('Redfin data fetched. Extract comps from the page.')
"
```

## Common Pitfalls

- **Using only active listings as comps**: Active listings are competition, not comps. They set the ceiling. Use closed sales first, pendings second, actives third.
- **Not adjusting for market date**: If comps sold 6-12 months ago in an appreciating market, apply an upward time adjustment (0.5-1% per month).
- **Adjusting beyond 15% total**: If a comp needs >15% net adjustment, it's probably not a good comp. Find a closer one.
- **Ignoring condition differences**: A comp in "Excellent" condition vs. subject in "Fair" condition needs a significant downward adjustment ($10-30k+).
- **Relying on Zestimates**: Zillow's AVM is a starting point, not a CMA. It can be off by 5-15% in volatile markets.
- **Including distressed sales**: Short sales, foreclosures, and REOs are not comps for a standard retail sale unless the subject is also distressed.
- **Mismatching property types**: Never comp a single-family detached to a townhouse, condo, or duplex.
- **Overlooking concessions**: If the seller gave $10k in closing cost credits, the true sales price is the prices minus the concession value.
- **Failing to consider location within location**: A street facing a highway is not comparable to a cul-de-sac in the same subdivision.
- **Using list price instead of sold price**: List price is asking price. Only closed prices matter for comps.

## Verification Checklist

- [ ] 3-6 comparable closed sales found within recommended radius/timeframe
- [ ] All comps are same property type (SFH ↔ SFH, condo ↔ condo)
- [ ] Bedroom count within ±1 of subject
- [ ] Square footage within ±30% of subject (ideally ±20%)
- [ ] Age within ±15 years of subject
- [ ] Net adjustment per comp does not exceed 15%
- [ ] Time adjustment applied for comps older than 3 months (if market changing)
- [ ] Distressed sales excluded (short sale, foreclosure, REO)
- [ ] Price per square foot calculated and cross-checked
- [ ] Confidence level assessed (High/Medium/Low) with explanation
- [ ] Suggested list price includes negotiation room (2-5% above target)
- [ ] Recommended price range has bottom (seller's minimum) and top (overpriced ceiling)
- [ ] All sources and sale dates documented
- [ ] Seller concessions (if any) accounted for in comp prices
- [ ] CMA report formatted and ready for client presentation