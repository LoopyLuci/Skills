---
name: real-estate-rental-analysis
description: "Rental cash flow analysis. 1% rule, 50% rule, cash-on-cash."
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [real-estate, rentals, cash-flow, roi, property-management]
    related_skills: [real-estate-property-analysis, real-estate-market-intel, real-estate-cma-generator]
---

# Real Estate Rental Analysis

Deep-dive rental property analysis for buy-and-hold investors. Compute cash flow, apply the 1% and 50% rules, project depreciation (cost segregation), calculate amortization schedules, and determine true ROI across different financing scenarios.

## When to Use

- Evaluating a property as a long-term rental investment
- Comparing short-term rental (Airbnb/VRBO) vs. long-term rental returns
- Analyzing a potential BRRRR (Buy-Rehab-Rent-Refinance-Repeat) deal
- Presenting a rental investment proposal to a client or partner
- Determining if a property meets your minimum cash flow thresholds

## Key Rental Metrics & Rules of Thumb

| Metric/Rule | What It Tells You | Formula | Target |
|---|---|---|---|
| **1% Rule** | Quick rent-to-price sanity check | Monthly Rent ÷ Purchase Price | ≥ 1% |
| **2% Rule** | Strong cash flow potential | Monthly Rent ÷ Purchase Price | ≥ 2% (multi-family) |
| **50% Rule** | Operating expense estimate | Total OpEx ≈ 50% of Gross Rent | 45-55% |
| **Cash-on-Cash Return** | Return on cash invested | Annual CF ÷ Total Cash In | 8-12%+ |
| **Cap Rate** | Unlevered return | NOI ÷ Purchase Price | 5-10% |
| **Gross Rent Multiplier** | Valuation multiple | Price ÷ Gross Annual Rent | 4-10 |
| **Debt Coverage Ratio** | Lender safety margin | NOI ÷ Annual Debt Service | 1.25+ |
| **Total ROI** | Full return including appreciation | (CF + Equity Growth) ÷ Total Cash | 15%+ annualized |
| **CapEx % of Rent** | Reserve for replacements | 5-15% of EGI | 10% (recommended) |
| **Cash Flow / Door** | Per-unit profitability | Net CF ÷ Units | $100-300+/door |

## Workflow

### 1. Gather Rental Property Data

```
Purchase Price:
After Repair Value (ARV, if BRRRR):
Number of Units:
Monthly Rent Per Unit:
Total Monthly Gross Rent:
Other Monthly Income (laundry, parking, storage, pet fees, vending):
Property Management (% of EGI or $):
Property Taxes (annual):
Insurance (annual):
HOA Dues (monthly, if applicable):
Maintenance/Repairs: ___ % of EGI or $____ / year
CapEx Reserve: ___ % of EGI or $____ / year
Vacancy Rate ___ %
Utilities Paid by Owner (annual):
Advertising/Marketing ($/year):
Legal/Accounting ($/year):
Pest Control ($/year):
Trash/Snow Removal ($/year):
Down Payment: ___ %
Closing Costs: $____ or ___ %
Interest Rate: ___ %
Loan Term: ___ years
Points / Origination Fees: $____
Renovation Costs (if BRRRR): $____
Refinance ARV (if BRRRR): $____
Appreciation Rate (annual): ___ %
Rent Growth Rate (annual): ___ %
Marginal Tax Rate: ___ %
```

### 2. Apply the 1% Rule (Quick Filter)

```python
def one_percent_rule(purchase_price, monthly_rent):
    ratio = monthly_rent / purchase_price * 100
    passes = ratio >= 1.0
    verdict = "PASSES ✅" if passes else "FAILS ❌"
    target_rent = purchase_price * 0.01
    target_price = monthly_rent * 100
    print("1% RULE ANALYSIS")
    print(f"  Purchase Price:   ${purchase_price:>10,}")
    print(f"  Monthly Rent:     ${monthly_rent:>10,}")
    print(f"  Ratio:            {ratio:>6.2f}%")
    print(f"  Verdict:          {verdict}")
    print(f"  Need ${target_rent:,.0f}/mo rent or ${target_price:,.0f} price")
    return {'ratio': round(ratio, 2), 'passes': passes}
```

### 3. Apply the 50% Rule (Expense Estimate)

```python
def fifty_percent_rule(gross_monthly_rent):
    estimated_opex = gross_monthly_rent * 0.50
    estimated_noi = gross_monthly_rent - estimated_opex
    print("\n50% RULE ESTIMATE")
    print(f"  Gross Monthly Rent:   ${gross_monthly_rent:>8,.2f}")
    print(f"  Est. OpEx (50%):      ${estimated_opex:>8,.2f}")
    print(f"  Est. NOI (pre-debt):  ${estimated_noi:>8,.2f}")
    print(f"  Est. Annual NOI:      ${estimated_noi*12:>8,.2f}")
    return {'gross_monthly': gross_monthly_rent, 'est_opex': estimated_opex,
            'est_noi': estimated_noi, 'annual_noi': estimated_noi * 12}
```

### 4. Full Cash Flow Analysis

```python
def rental_analysis(**kwargs):
    p = {
        'purchase_price': 300000, 'arv': 300000, 'down_payment_pct': 20,
        'closing_costs': 6000, 'units': 1, 'monthly_rent': 3500,
        'other_monthly_income': 100, 'mgmt_pct': 8, 'property_taxes': 3600,
        'insurance': 1500, 'hoa': 0, 'maintenance_pct': 5, 'capex_pct': 8,
        'vacancy_rate': 5, 'utilities': 600, 'advertising': 300,
        'legal_accounting': 500, 'pest_control': 300, 'trash_snow': 500,
        'interest_rate': 6.5, 'loan_term_years': 30, 'appreciation_rate': 3,
        'rent_growth_rate': 2, 'holding_period_years': 5, 'rehab_costs': 0,
        'marginal_tax_rate': 24,
    }
    p.update(kwargs)

    gross_monthly = p['monthly_rent'] + p['other_monthly_income']
    gross_annual = gross_monthly * 12
    vacancy = gross_annual * p['vacancy_rate'] / 100
    egi = gross_annual - vacancy

    mgmt = egi * p['mgmt_pct'] / 100
    maintenance = egi * p['maintenance_pct'] / 100
    capex = egi * p['capex_pct'] / 100
    total_opex = (mgmt + p['property_taxes'] + p['insurance'] + p['hoa']*12 +
                  maintenance + p['utilities'] + p['advertising'] +
                  p['legal_accounting'] + p['pest_control'] + p['trash_snow'] + capex)
    opex_ratio = total_opex / gross_annual * 100 if gross_annual else 0

    loan_amount = min(p['purchase_price'] + p['rehab_costs'], p['arv']) * (1 - p['down_payment_pct'] / 100)
    monthly_rate = p['interest_rate'] / 100 / 12
    n = p['loan_term_years'] * 12
    monthly_pmt = monthly_rate * loan_amount * (1 + monthly_rate)**n / ((1 + monthly_rate)**n - 1) if monthly_rate > 0 else loan_amount / n
    annual_debt = monthly_pmt * 12
    noi = egi - total_opex
    pre_tax_cf = noi - annual_debt
    total_cash = (p['purchase_price'] * p['down_payment_pct'] / 100 + p['closing_costs'] + p['rehab_costs'])
    coc_return = (pre_tax_cf / total_cash) * 100 if total_cash else 0
    cap_rate = (noi / p['arv']) * 100 if p['arv'] else 0
    one_pct_ratio = gross_monthly / p['purchase_price'] * 100

    # Depreciation
    building_value = p['purchase_price'] * 0.80
    annual_depreciation = building_value / 27.5
    tax_savings = annual_depreciation * p['marginal_tax_rate'] / 100

    # Projection
    cash_flows = []
    current_rent = gross_annual
    current_value = p['arv']
    for year in range(1, p['holding_period_years'] + 1):
        vac_y = current_rent * p['vacancy_rate'] / 100
        egi_y = current_rent - vac_y
        mgmt_y = egi_y * p['mgmt_pct'] / 100
        maint_y = egi_y * p['maintenance_pct'] / 100
        capex_y = egi_y * p['capex_pct'] / 100
        opex_fixed = (p['property_taxes'] + p['insurance'] + p['hoa']*12 +
                      p['utilities'] + p['advertising'] + p['legal_accounting'] +
                      p['pest_control'] + p['trash_snow'])
        noi_y = egi_y - (mgmt_y + opex_fixed + maint_y + capex_y)
        cf_y = noi_y - annual_debt
        cash_flows.append(cf_y)
        current_rent *= (1 + p['rent_growth_rate'] / 100)
        current_value *= (1 + p['appreciation_rate'] / 100)

    # Loan balance
    remaining = loan_amount
    for _ in range(p['holding_period_years'] * 12):
        interest = remaining * monthly_rate
        principal = monthly_pmt - interest
        remaining -= principal
    remaining = max(0, remaining)

    equity_gain = current_value - remaining - total_cash
    total_return = sum(cash_flows) + equity_gain
    total_roi_pct = (total_return / total_cash) * 100 if total_cash else 0

    print("\n" + "=" * 70)
    print("RENTAL PROPERTY ANALYSIS")
    print("=" * 70)
    print(f"\n📋 QUICK RULES")
    print(f"  1% Rule:         {one_pct_ratio:.2f}%  {'✅ PASS' if one_pct_ratio >= 1 else '❌ FAIL'}")
    print(f"  50% Rule OpEx:   {opex_ratio:.1f}%  {'✅' if 40 <= opex_ratio <= 60 else '⚠️'}")
    print(f"\n💰 INCOME — Gross: ${gross_annual:>8,.0f}  EGI: ${egi:>8,.0f}")
    print(f"\n📉 EXPENSES ({opex_ratio:.1f}%) — Total: ${total_opex:>8,.0f}")
    print(f"\n🏠 NOI: ${noi:>8,.0f}  |  Cap Rate: {cap_rate:.2f}%")
    print(f"\n🏦 DEBT — Loan: ${loan_amount:>8,.0f}  Monthly P&I: ${monthly_pmt:>8,.2f}")
    print(f"\n💵 CASH FLOW — Monthly: ${pre_tax_cf/12:>8,.0f}  Annual: ${pre_tax_cf:>8,.0f}  /door: ${(pre_tax_cf/12)/p['units']:>8,.0f}")
    print(f"\n📊 RETURNS")
    print(f"  Cash-on-Cash:        {coc_return:.2f}%")
    print(f"  Annual Depreciation: ${annual_depreciation:>8,.0f}")
    print(f"  Tax Savings:         ${tax_savings:>8,.0f}/yr")
    print(f"\n📈 PROJECTION ({p['holding_period_years']}yr)")
    print(f"  Projected Value:    ${current_value:>10,.0f}")
    print(f"  Equity Gain:        ${equity_gain:>10,.0f}")
    print(f"  Total Return:       ${total_return:>10,.0f}")
    print(f"  Total ROI:          {total_roi_pct:.1f}%")

    return {
        'one_pct_ratio': round(one_pct_ratio, 2), 'opex_ratio': round(opex_ratio, 1),
        'noi': round(noi, 2), 'cap_rate': round(cap_rate, 2),
        'dscr': round(noi/annual_debt, 2) if annual_debt else 0,
        'monthly_cf': round(pre_tax_cf/12, 2), 'annual_cf': round(pre_tax_cf, 2),
        'total_cash': round(total_cash, 2), 'coc_return': round(coc_return, 2),
        'tax_savings': round(tax_savings, 0), 'total_roi': round(total_roi_pct, 1),
    }
```

### 5. BRRRR Analysis

```python
def brrrr_analysis(**kwargs):
    p = {
        'purchase_price': 200000, 'rehab_costs': 50000, 'closing_costs_buy': 5000,
        'arv': 320000, 'monthly_rent_arv': 3500, 'refi_interest_rate': 7.0,
        'refi_lvr': 75, 'refi_closing_costs': 4000, 'vacancy_rate': 5,
        'mgmt_pct': 8, 'property_taxes': 4000, 'insurance': 1800,
    }
    p.update(kwargs)

    total_cash_in = p['purchase_price'] + p['rehab_costs'] + p['closing_costs_buy']
    refi_loan = p['arv'] * p['refi_lvr'] / 100
    cash_recouped = refi_loan - p['refi_closing_costs']
    cash_left_in = total_cash_in - cash_recouped

    monthly_rate = p['refi_interest_rate'] / 100 / 12
    n = 30 * 12
    monthly_pmt = monthly_rate * refi_loan * (1 + monthly_rate)**n / ((1 + monthly_rate)**n - 1)
    annual_debt = monthly_pmt * 12
    gross_annual = p['monthly_rent_arv'] * 12
    egi = gross_annual - gross_annual * p['vacancy_rate'] / 100
    mgmt = egi * p['mgmt_pct'] / 100
    noi = egi - (mgmt + p['property_taxes'] + p['insurance'])
    cf = noi - annual_debt
    coc = (cf / cash_left_in) * 100 if cash_left_in > 0 else float('inf')

    print("\n" + "=" * 70)
    print("BRRRR ANALYSIS")
    print("=" * 70)
    print(f"\nBUY+REHAB: ${total_cash_in:>8,} total cash in")
    print(f"REFI: ARV ${p['arv']:>8,} → Loan ${refi_loan:>8,} → Recoup ${cash_recouped:>8,}")
    print(f"CASH LEFT IN: ${cash_left_in:>8,}")
    print(f"RENT: ${p['monthly_rent_arv']:>8,}/mo → CF ${cf:>8,}/yr → CoC {coc:.1f}%")
    print(f"Cash Out > All-In? {'✅ YES' if cash_recouped > total_cash_in else '❌ NO'}")
    return {'cash_left_in': round(cash_left_in, 0), 'coc': round(coc, 1)}
```

### 6. Short-Term vs. Long-Term Comparison

```python
def str_vs_ltr_analysis(**kwargs):
    p = {
        'purchase_price': 350000, 'monthly_rent_ltr': 3500,
        'str_daily_rate': 250, 'str_occupancy_rate': 65, 'str_management_pct': 20,
        'str_cleaning_fee': 85, 'str_avg_stay_nights': 3.5,
        'down_payment_pct': 25, 'closing_costs': 7000, 'interest_rate': 6.5,
        'property_taxes': 4200, 'insurance': 2000, 'hoa': 0, 'utilities': 2400,
        'maintenance_pct': 5, 'capex_pct': 8, 'vacancy_rate_ltr': 5,
    }
    p.update(kwargs)

    gross_annual_ltr = p['monthly_rent_ltr'] * 12
    vac_ltr = gross_annual_ltr * p['vacancy_rate_ltr'] / 100
    egi_ltr = gross_annual_ltr - vac_ltr
    fixed_opex = p['property_taxes'] + p['insurance'] + p['hoa']*12 + p['utilities']
    total_opex_ltr = (egi_ltr * 8/100 + fixed_opex + egi_ltr * p['maintenance_pct']/100 + egi_ltr * p['capex_pct']/100)
    noi_ltr = egi_ltr - total_opex_ltr

    str_gross_nights = 365 * p['str_occupancy_rate'] / 100
    str_gross_rev = str_gross_nights * p['str_daily_rate']
    str_cleaning_rev = (str_gross_nights / p['str_avg_stay_nights']) * p['str_cleaning_fee']
    str_total_rev = str_gross_rev + str_cleaning_rev
    str_total_opex = (str_total_rev * p['str_management_pct']/100 + fixed_opex +
                      str_total_rev * p['maintenance_pct']/100 + str_total_rev * p['capex_pct']/100)
    str_noi = str_total_rev - str_total_opex

    loan_amount = p['purchase_price'] * (1 - p['down_payment_pct'] / 100)
    monthly_rate = p['interest_rate'] / 100 / 12
    n = 30 * 12
    monthly_pmt = monthly_rate * loan_amount * (1 + monthly_rate)**n / ((1 + monthly_rate)**n - 1)
    annual_debt = monthly_pmt * 12
    total_cash = p['purchase_price'] * p['down_payment_pct'] / 100 + p['closing_costs']

    cf_ltr = noi_ltr - annual_debt
    cf_str = str_noi - annual_debt
    coc_ltr = (cf_ltr / total_cash) * 100
    coc_str = (cf_str / total_cash) * 100

    print("\n" + "=" * 70)
    print("SHORT-TERM vs. LONG-TERM RENTAL COMPARISON")
    print("=" * 70)
    print(f"\n{'Metric':<35} {'Long-Term':>15} {'Short-Term':>15}")
    print(f"{'-'*65}")
    print(f"{'Gross Revenue':<35} ${gross_annual_ltr:>10,.0f}  ${str_total_rev:>10,.0f}")
    print(f"{'Net Income':<35} ${noi_ltr:>10,.0f}  ${str_noi:>10,.0f}")
    print(f"{'Cash Flow/yr':<35} ${cf_ltr:>10,.0f}  ${cf_str:>10,.0f}")
    print(f"{'Cash Flow/mo':<35} ${cf_ltr/12:>10,.0f}  ${cf_str/12:>10,.0f}")
    print(f"{'Cash-on-Cash':<35} {coc_ltr:>10.1f}%  {coc_str:>10.1f}%")
    print(f"\n{'✅ STR wins' if cf_str > cf_ltr else '✅ LTR wins'} by ${abs(cf_str-cf_ltr):,.0f}/yr")
    return {'ltr_coc': round(coc_ltr, 1), 'str_coc': round(coc_str, 1)}
```

### 7. Amortization Schedule

```python
def amortization_schedule(loan_amount, annual_rate, term_years):
    monthly_rate = annual_rate / 100 / 12
    n = term_years * 12
    monthly_pmt = monthly_rate * loan_amount * (1 + monthly_rate)**n / ((1 + monthly_rate)**n - 1)
    balance = loan_amount
    total_interest = 0

    print(f"\nAMORTIZATION — ${loan_amount:>8,} @ {annual_rate}% / {term_years}yr")
    print(f"  Payment: ${monthly_pmt:>8,.2f}/mo")
    print(f"\n  {'Year':>5} {'Payment':>10} {'Principal':>10} {'Interest':>10} {'Balance':>12}")
    for year in range(1, term_years + 1):
        ap, ai = 0, 0
        for _ in range(12):
            i = balance * monthly_rate
            pr = monthly_pmt - i
            balance -= pr
            ap += pr; ai += i
            total_interest += i
        print(f"  {year:>5} ${monthly_pmt*12:>8,.0f} ${ap:>8,.0f} ${ai:>8,.0f} ${max(0,balance):>10,.0f}")
    print(f"\n  Total Interest: ${total_interest:>10,.0f}")

amortization_schedule(200000, 6.5, 30)
```

## Common Pitfalls

- **Over-relying on the 1% rule**: Market conditions vary. In HCOL areas, 0.5-0.7% may be the norm. Use it as a filter, not a decision metric.
- **Ignoring the 50% rule**: Actual expenses vary, but the 50% rule is remarkably accurate over time. Budgeting <45% for OpEx likely means underestimating.
- **Forgetting vacancy between tenants**: Even 5% vacancy budgeted, a 3-week turnover costs ~6% annually. Budget for both vacancy AND turnover.
- **Neglecting payroll taxes on self-management**: Self-managing means active income for IRS. LLC structure matters.
- **Not accounting for STR regulations**: Many cities ban/restrict STRs (NY, LA, Austin, SF). Verify local laws before projecting STR returns.
- **Underestimating STR costs**: STRs have 20-30% management fees, higher utilities, supplies, licensing. Expect 60-70% expense ratios.
- **Skipping cost segregation**: Can accelerate depreciation from 27.5yr to 5-15yr on personal property. Saves $5-10k/yr on typical rental.
- **Ignoring self-management labor value**: Your time has economic value. At $50/hr, 5 hrs/week = $13k/yr opportunity cost.
- **Not running rent comps**: Projected rent must be based on actual market comps, not optimistic assumptions. Pull current listings.
- **Forgetting the 3.8% NIIT**: Net Investment Income Tax applies over $200k/$250k MAGI. Rental income may trigger this.
- **Overleveraging in rising rate environments**: CoC looks great at 5% rates but can go negative at 8%. Model at current rates.

## Verification Checklist

- [ ] 1% rule calculated: monthly rent ≥ 1% of purchase price
- [ ] 50% rule checked: operating expenses within 45-55% of gross rent
- [ ] Cash-on-cash return ≥ 8% (or personal minimum)
- [ ] Cap rate compared to market average for property type
- [ ] DSCR ≥ 1.25 for conventional financing
- [ ] Monthly cash flow per door documented (target $100+/door)
- [ ] All operating expenses itemized (management, taxes, insurance, HOA, maintenance, CapEx, utilities, advertising, legal)
- [ ] CapEx reserve included (minimum 8% of EGI)
- [ ] Vacancy rate reflects local market (not ideal 0%)
- [ ] Depreciation calculated (residential 27.5 years, land excluded)
- [ ] Tax savings from depreciation estimated
- [ ] Financing terms verified with actual lender quote
- [ ] Rent projections based on actual market comps
- [ ] Appreciation and rent growth rates conservative (2-3%)
- [ ] For BRRRR: cash-out refi covers all-in costs
- [ ] For STR vs LTR: local STR regulations verified
- [ ] Amortization schedule confirmed for loan term
- [ ] Equity growth and total ROI projected over hold period
- [ ] At least one downside scenario modeled