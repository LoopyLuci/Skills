---
name: real-estate-property-analysis
description: "Use when underwriting property. Cap rate, NOI, IRR, DSCR."
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [real-estate, investment, analysis, financial-modeling, underwriting]
    related_skills: [real-estate-rental-analysis, real-estate-cma-generator, real-estate-market-intel]
---

# Real Estate Property Analysis

Comprehensive financial underwriting for income-producing real estate investments. Calculate all key performance metrics, generate sensitivity tables, and produce professional PDF reports.

## When to Use

- Evaluating a potential acquisition (single-family, multi-family, commercial)
- Running the numbers on a deal presented by an agent or wholesaler
- Comparing multiple investment opportunities side-by-side
- Preparing a detailed investment memo for partners or lenders
- Stress-testing a deal under different assumptions (vacancy, rate, rent growth)

## Key Financial Metrics

| Metric | Formula | Target Range |
|---|---|---|
| **Cap Rate** | NOI ÷ Purchase Price | 4-12% (market-dependent) |
| **Cash-on-Cash Return** | Pre-Tax Cash Flow ÷ Total Cash Invested | 8%+ |
| **NOI** | Effective Gross Income - Total Operating Expenses | Positive |
| **GRM (Gross Rent Multiplier)** | Price ÷ Gross Annual Rent | 4-12 |
| **Debt Service Coverage Ratio (DSCR)** | NOI ÷ Annual Debt Service | 1.25+ (conventional) |
| **Break-Even Occupancy** | (OpEx + Debt Service) ÷ EGI at 100% occupancy | < 85% |
| **IRR** | Annualized total return (time-weighted) | 12-20% (target dependent) |
| **Equity Multiple** | Total Cash Returned ÷ Equity Invested | 2.0x+ over hold period |

## Workflow

### 1. Gather Property Data

Collect these inputs from the user, MLS, or public records:

```
Purchase Price:
Down Payment %:
Closing Costs:
Loan Amount:
Interest Rate:
Amortization (years):
Gross Annual Rent:
Other Income (laundry, parking, storage, etc.):
Vacancy Rate (%):
Property Management (% of EGI):
Property Taxes (annual):
Insurance (annual):
HOA/Condo Fees (annual):
Maintenance/Repairs (% of EGI or $ amount):
Utilities (annual):
CapEx Reserve (% of EGI or $ amount):
Other OpEx (legal, accounting, marketing):
Appreciation Rate (annual, projection):
Rent Growth Rate (annual, projection):
Selling Costs (% at exit):
Hold Period (years):
```

### 2. Calculate Base Case

Run the core calculations:

**Income:**
```
PGI (Potential Gross Income) = Gross Annual Rent + Other Income
V&C Allowance = PGI × Vacancy Rate
EGI (Effective Gross Income) = PGI - V&C Allowance
```

**Operating Expenses:**
```
Property Management = EGI × Mgmt %
Taxes (fixed annual)
Insurance (fixed annual)
HOA (fixed annual)
Maintenance = EGI × Maint %
Utilities (fixed annual)
CapEx Reserve = EGI × CapEx %
Other (fixed annual)
Total OpEx = sum of all above
```

**Net Operating Income:**
```
NOI = EGI - Total OpEx
```

**Debt Service:**
```
Monthly P&I = PMT(rate/12, term×12, -loan amount)
Annual Debt Service = Monthly P&I × 12
DSCR = NOI ÷ Annual Debt Service
```

**Cash Flow:**
```
Pre-Tax Cash Flow = NOI - Annual Debt Service
Total Cash Invested = (Down Payment + Closing Costs)
Cash-on-Cash Return = Pre-Tax Cash Flow ÷ Total Cash Invested × 100
```

**Valuation Metrics:**
```
Cap Rate = NOI ÷ Purchase Price × 100
GRM = Purchase Price ÷ Gross Annual Rent
Break-Even Occupancy = (OpEx + Debt Service) ÷ PGI × 100
```

### 3. Python Financial Model

Save as `analyze_deal.py`:

```python
#!/usr/bin/env python3
def pmt(rate, nper, pv):
    if rate == 0:
        return pv / nper
    r = rate / 12
    n = nper * 12
    return r * pv * (1 + r)**n / ((1 + r)**n - 1)

def analyze_property(**kwargs):
    p = {
        'purchase_price': 500000,
        'down_payment_pct': 20,
        'closing_costs': 10000,
        'interest_rate': 6.5,
        'amort_years': 30,
        'gross_annual_rent': 60000,
        'other_annual_income': 2400,
        'vacancy_rate': 5,
        'mgmt_pct': 8,
        'property_taxes': 6000,
        'insurance': 1800,
        'hoa_fees': 0,
        'maintenance_pct': 5,
        'utilities': 1200,
        'capex_pct': 5,
        'other_opex': 500,
        'appreciation_rate': 3,
        'rent_growth_rate': 2,
        'selling_costs_pct': 8,
        'hold_years': 5,
    }
    p.update(kwargs)

    pgi = p['gross_annual_rent'] + p['other_annual_income']
    vacancy_allowance = pgi * p['vacancy_rate'] / 100
    egi = pgi - vacancy_allowance

    mgmt = egi * p['mgmt_pct'] / 100
    maintenance = egi * p['maintenance_pct'] / 100
    capex = egi * p['capex_pct'] / 100
    total_opex = (mgmt + p['property_taxes'] + p['insurance'] +
                  p['hoa_fees'] + maintenance + p['utilities'] +
                  capex + p['other_opex'])

    noi = egi - total_opex
    loan_amount = p['purchase_price'] * (1 - p['down_payment_pct'] / 100)
    monthly_pmt = pmt(p['interest_rate'] / 100, p['amort_years'], loan_amount)
    annual_debt = monthly_pmt * 12
    pre_tax_cf = noi - annual_debt
    total_cash = (p['purchase_price'] * p['down_payment_pct'] / 100) + p['closing_costs']
    coc_return = (pre_tax_cf / total_cash) * 100 if total_cash else 0

    cap_rate = (noi / p['purchase_price']) * 100
    grm = p['purchase_price'] / p['gross_annual_rent'] if p['gross_annual_rent'] else 0
    dscr = noi / annual_debt if annual_debt else 0
    break_even = ((total_opex + annual_debt) / pgi) * 100 if pgi else 0

    # Pro-forma projection
    cash_flows = []
    current_rent = pgi
    current_value = p['purchase_price']
    total_returned = 0

    for year in range(1, p['hold_years'] + 1):
        vac = current_rent * p['vacancy_rate'] / 100
        egi_y = current_rent - vac
        mgmt_y = egi_y * p['mgmt_pct'] / 100
        maint_y = egi_y * p['maintenance_pct'] / 100
        capex_y = egi_y * p['capex_pct'] / 100
        opex_y = (mgmt_y + p['property_taxes'] + p['insurance'] +
                  p['hoa_fees'] + maint_y + p['utilities'] +
                  capex_y + p['other_opex'])
        noi_y = egi_y - opex_y
        cf_y = noi_y - annual_debt
        cash_flows.append(cf_y)
        total_returned += cf_y
        current_rent *= (1 + p['rent_growth_rate'] / 100)
        current_value *= (1 + p['appreciation_rate'] / 100)

    # Loan balance at exit
    remaining_balance = loan_amount
    for _ in range(p['hold_years'] * 12):
        interest = remaining_balance * (p['interest_rate'] / 100 / 12)
        principal = monthly_pmt - interest
        remaining_balance -= principal
    remaining_balance = max(0, remaining_balance)

    selling_costs = current_value * p['selling_costs_pct'] / 100
    net_sale_proceeds = current_value - selling_costs - remaining_balance
    total_returned += net_sale_proceeds

    # IRR via Newton-Raphson
    irr_guess = 0.10
    for _ in range(1000):
        npv = -total_cash
        cf_all = cash_flows + [net_sale_proceeds]
        for t, cf in enumerate(cf_all):
            npv += cf / (1 + irr_guess)**(t + 1)
        if abs(npv) < 0.001:
            break
        dnpv = 0
        for t, cf in enumerate(cf_all):
            dnpv += -cf * (t + 1) / (1 + irr_guess)**(t + 2)
        if dnpv == 0:
            break
        irr_guess -= npv / dnpv
        if irr_guess < -1:
            irr_guess = 0.5
            break

    irr = irr_guess * 100
    equity_multiple = total_returned / total_cash if total_cash else 0

    return {
        'pgi': round(pgi, 2),
        'egi': round(egi, 2),
        'total_opex': round(total_opex, 2),
        'noi': round(noi, 2),
        'annual_debt': round(annual_debt, 2),
        'pre_tax_cf': round(pre_tax_cf, 2),
        'total_cash_invested': round(total_cash, 2),
        'cap_rate': round(cap_rate, 2),
        'cash_on_cash': round(coc_return, 2),
        'grm': round(grm, 2),
        'dscr': round(dscr, 2),
        'break_even_occupancy': round(break_even, 2),
        'monthly_payment': round(monthly_pmt, 2),
        'loan_amount': round(loan_amount, 2),
        'projected_sale_value': round(current_value, 2),
        'net_sale_proceeds': round(net_sale_proceeds, 2),
        'irr': round(irr, 2),
        'equity_multiple': round(equity_multiple, 2),
        'cash_flows': [round(cf, 2) for cf in cash_flows],
        'remaining_balance': round(remaining_balance, 2),
    }

def print_report(r):
    print("=" * 60)
    print("INVESTMENT PROPERTY ANALYSIS REPORT")
    print("=" * 60)
    print(f"\nINCOME — PGI: ${r['pgi']:>10,.2f}  EGI: ${r['egi']:>10,.2f}")
    print(f"EXPENSES — Total OpEx: ${r['total_opex']:>10,.2f}")
    print(f"NOI: ${r['noi']:>10,.2f}")
    print(f"DEBT — Monthly: ${r['monthly_payment']:>10,.2f}  Annual: ${r['annual_debt']:>10,.2f}")
    print(f"CASH FLOW: ${r['pre_tax_cf']:>10,.2f}  Cash Invested: ${r['total_cash_invested']:>10,.2f}")
    print(f"\nMETRICS")
    print(f"  Cap Rate:          {r['cap_rate']:>8.2f}%")
    print(f"  Cash-on-Cash:      {r['cash_on_cash']:>8.2f}%")
    print(f"  GRM:               {r['grm']:>8.2f}")
    print(f"  DSCR:              {r['dscr']:>8.2f}")
    print(f"  Break-Even Occ:    {r['break_even_occupancy']:>8.2f}%")
    print(f"  IRR:               {r['irr']:>8.2f}%")
    print(f"  Equity Multiple:   {r['equity_multiple']:>8.2f}x")
    print(f"\nPROJECTION ({len(r['cash_flows'])} yrs)")
    for i, cf in enumerate(r['cash_flows']):
        print(f"  Year {i+1} CF: ${cf:>9,.2f}")
    print(f"  Sale Value:    ${r['projected_sale_value']:>10,.2f}")
    print(f"  Net Proceeds:  ${r['net_sale_proceeds']:>10,.2f}")

if __name__ == '__main__':
    import json
    result = analyze_property()
    print_report(result)
    print(f"\nJSON:\n{json.dumps(result, indent=2)}")
```

### 4. Sensitivity Analysis

```python
def sensitivity_table(base_params, param_ranges):
    from itertools import product
    results = []
    keys, values = zip(*param_ranges.items())
    for combo in product(*values):
        params = dict(base_params)
        for k, v in zip(keys, combo):
            params[k] = v
        r = analyze_property(**params)
        combo_str = ', '.join(f'{k}={v}' for k, v in zip(keys, combo))
        results.append({
            'params': combo_str,
            'cap_rate': r['cap_rate'],
            'coc_return': r['cash_on_cash'],
            'dscr': r['dscr'],
            'irr': r['irr'],
        })
    return results

# Vary price, vacancy, and rate simultaneously
table = sensitivity_table(
    {'purchase_price': 500000, 'gross_annual_rent': 60000, 'vacancy_rate': 5, 'interest_rate': 6.5},
    {'purchase_price': [450000, 500000, 550000], 'vacancy_rate': [3, 5, 8], 'interest_rate': [5.5, 6.5, 7.5]}
)
for row in table:
    print(f"{row['params']:60s} | Cap: {row['cap_rate']:5.2f}% | CoC: {row['coc_return']:5.2f}% | DSCR: {row['dscr']:.2f} | IRR: {row['irr']:5.2f}%")
```

### 5. Generate PDF Report

```bash
pip install fpdf2
```

```python
from fpdf import FPDF

class InvestmentReport(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, 'Property Investment Analysis', ln=True, align='C')
        self.ln(5)

    def section(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(230, 230, 240)
        self.cell(0, 8, title, ln=True, fill=True)
        self.ln(2)

    def metric_line(self, label, value):
        self.set_font('Helvetica', '', 10)
        self.cell(120, 7, label)
        self.cell(0, 7, str(value), ln=True)

def generate_summary_pdf(result, filename='investment_report.pdf'):
    pdf = InvestmentReport()
    pdf.add_page()
    pdf.section('Income & Expenses')
    pdf.metric_line('Potential Gross Income:', f"${result['pgi']:,.2f}")
    pdf.metric_line('Effective Gross Income:', f"${result['egi']:,.2f}")
    pdf.metric_line('Total OpEx:', f"${result['total_opex']:,.2f}")
    pdf.metric_line('Net Operating Income:', f"${result['noi']:,.2f}")
    pdf.section('Financing')
    pdf.metric_line('Loan Amount:', f"${result['loan_amount']:,.2f}")
    pdf.metric_line('Monthly P&I:', f"${result['monthly_payment']:,.2f}")
    pdf.section('Returns')
    pdf.metric_line('Cap Rate:', f"{result['cap_rate']:.2f}%")
    pdf.metric_line('Cash-on-Cash:', f"{result['cash_on_cash']:.2f}%")
    pdf.metric_line('DSCR:', f"{result['dscr']:.2f}")
    pdf.metric_line('IRR:', f"{result['irr']:.2f}%")
    pdf.metric_line('Equity Multiple:', f"{result['equity_multiple']:.2f}x")
    pdf.section('Projection')
    for i, cf in enumerate(result['cash_flows']):
        pdf.metric_line(f'Year {i+1} CF:', f"${cf:,.2f}")
    pdf.metric_line('Sale Value:', f"${result['projected_sale_value']:,.2f}")
    pdf.metric_line('Net Proceeds:', f"${result['net_sale_proceeds']:,.2f}")
    pdf.output(filename)
    print(f"Report: {filename}")
```

## Common Pitfalls

- **Ignoring CapEx reserves**: Always budget 5-15% of EGI for long-term replacements (roof, HVAC, parking lot).
- **Using pro forma NOI instead of trailing NOI**: Sellers' pro formas are optimistic. Verify actual T12 operating statements.
- **Overlooking management costs**: Include 8-10% management fee even if self-managing to reflect market cost.
- **Forgetting vacancy between tenants**: Use market vacancy (5-10%), not current occupancy. Account for lease-up time.
- **Skipping sensitivity analysis**: A single-point estimate is dangerous. Stress-test across vacancy, rate, and rent growth.
- **Misapplying cap rate**: Cap rate does not account for leverage, financing, or appreciation. Never use as sole decision metric.
- **Underestimating insurance**: Property insurance has risen 15-30% annually in many markets. Get actual quotes.
- **Assuming linear rent growth**: Check local rent control ordinances before projecting growth.
- **Using tax assessment instead of market value**: Tax-assessed value often lags market. Use appraised/purchase price.
- **Ignoring loan prepayment penalties**: Confirm whether the loan has yield maintenance, defeasance, or prepayment lockout.

## Verification Checklist

- [ ] GRM calculated and cross-checked against market comps
- [ ] Cap rate computed and compared to market average for property type/class
- [ ] Cash-on-cash with correct total cash invested (down payment + closing costs + immediate repairs)
- [ ] DSCR confirmed ≥ 1.25 for conventional financing
- [ ] Break-even occupancy confirmed below 85%
- [ ] Sensitivity table run with at least 3 variables (price, vacancy, interest rate)
- [ ] Pro-forma projections checked against trailing 12-month actuals
- [ ] CapEx reserve included (minimum 5% of EGI)
- [ ] Property management fee included (even if self-managing)
- [ ] All income/expense figures in annual amounts
- [ ] Loan amortization verified (correct term, rate, payment)
- [ ] IRR and equity multiple computed for full hold period
- [ ] Selling costs included in exit proceeds
- [ ] At least one downside scenario modeled
- [ ] Report exported and reviewed for numerical consistency