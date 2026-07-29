---
name: real-estate-transaction-coordination
description: "Closing checklists per state. Docs, disclaimers, compliance."
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [real-estate, transactions, closing, compliance, documentation]
    related_skills: [real-estate-cma-generator, real-estate-property-analysis]
---

# Real Estate Transaction Coordination

End-to-end transaction management from offer acceptance to post-closing. State-by-state checklists, required documents, mandatory disclosures, compliance checkpoints, and closing coordination workflows.

## When to Use

- Managing a residential real estate transaction from ratified contract to closing
- Ensuring compliance with state-specific disclosure requirements
- Preparing a transaction file for broker review or audit
- Training a new transaction coordinator on your process
- Coordinating with title, escrow, lender, and attorneys

## Transaction Phases Overview

| Phase | Timeline | Key Actions |
|---|---|---|
| **Under Contract** | Day 0-3 | Receipt of contract, earnest money deposit, deliver disclosures |
| **Due Diligence** | Day 3-30 | Inspections, appraisal, loan processing, survey, attorney review |
| **Contingency Removal** | Day 30-45 | Satisfy all contingencies, final walk-through prep |
| **Closing Prep** | Day 45-60 | CD review, funds confirmation, final walk-through, docs to title |
| **Closing Day** | Day 60 | Signing, funding, recording, keys released |
| **Post-Closing** | Day 60+ | Commission paid, final accounting, file audit |

## State-by-State Document Requirements

### Universal Documents (Every Transaction)

```
1. Purchase and Sale Agreement (executed)
2. Seller Property Disclosure Statement
3. Lead-Based Paint Disclosure (pre-1978)
4. Agency Disclosure (if applicable in state)
5. Earnest Money Receipt / Escrow Agreement
6. Financing Addendum / Loan Approval Letter
7. Appraisal Report
8. Home Inspection Report
9. Wood Destroying Insect Report (termite)
10. Title Commitment / Preliminary Report
11. Closing Disclosure (CD) / HUD-1
12. FIRPTA Documentation (foreign seller)
13. Certificate of Occupancy (if new construction)
14. Survey (if required)
15. Property Tax Certifications
```

### State-Specific Disclosures (Notable Examples)

| State | Key Disclosure Requirements |
|---|---|
| **California** | Natural Hazard Disclosure, Mello-Roos, TDS (Transfer Disclosure Statement), NHD Report, Megan's Law, Home Energy Rating |
| **Texas** | Seller's Disclosure Notice, TREC One-to-Four Family Contract, Third Party Financing Addendum, Lead-Based Paint, Condominium Addendum |
| **Florida** | Seller's Property Disclosure, Condominium/COA Documents, Flood Zone Disclosure, Radon Disclosure, Wind Mitigation (if applicable) |
| **New York** | Property Condition Disclosure Act (waivable), Lead Paint (pre-1960), Attorney Representation letters, Co-op Board Package (if co-op) |
| **Illinois** | Residential Real Property Disclosure, Radon Disclosure, Lead-Based Paint, Flood Hazard Disclosure, Resale Condo Docs |
| **Washington** | Form 17 Seller Disclosure, Lead-Based Paint, Condo/HOA Resale Certificate, Septic System (if applicable) |
| **Oregon** | Seller Disclosure Statement, Lead-Based Paint, Septic Disclosure, Home Energy Score (Portland area) |
| **Colorado** | Seller's Property Disclosure, Radon Disclosure, HOA Docs (if applicable), Lead-Based Paint, Methamphetamine Contamination |
| **Arizona** | Seller Property Disclosure Statement, Lead-Based Paint, Homeowners' Association Disclosure, Affidavit of Disclosure |
| **Georgia** | Seller's Property Disclosure, Lead-Based Paint, Radon Disclosure, Community Association Docs (if applicable) |
| **North Carolina** | Residential Property Disclosure Statement, Lead-Based Paint, Radon Disclosure, Well/Septic Disclosure |
| **Virginia** | Property Disclosure Statement, Lead-Based Paint, Radon Disclosure, Military Air Installation Disclosure |
| **Maryland** | Seller Disclosure Statement, Lead-Based Paint, Radon Disclosure, Well/Septic (if applicable), Water Quality |

**IMPORTANT**: Requirements change frequently. Always verify with:
- State Real Estate Commission website
- Local Association of Realtors legal hotline
- Title company / closing attorney
- Broker managing broker

### Transaction File Checklist Template

```python
def transaction_checklist(state, transaction_type):
    """
    Return a transaction checklist specific to state and transaction type.
    transaction_type: 'resale', 'new_construction', 'short_sale', 'foreclosure'
    """
    universal = [
        "Executed Purchase Agreement",
        "All addenda and counter-offers",
        "Seller Property Disclosure",
        "Lead-Based Paint Disclosure (if pre-1978)",
        "Agency Disclosure Form",
        "Earnest Money Deposit Receipt",
        "Proof of Funds / Pre-Approval Letter",
        "Home Inspection Report",
        "Termite/WDO Report",
        "Roof Certification (if applicable)",
        "HVAC Certification (if applicable)",
        "Appraisal Report",
        "Title Commitment",
        "Survey (if ordered)",
        "Homeowners Insurance Binder",
        "Flood Certification",
        "Closing Disclosure (3 days before closing)",
        "Final Walk-Through Form",
        "Settlement Statement",
        "Wiring Instructions (buyer & seller)",
        "Commission Agreement",
        "Property Tax Proration Worksheet",
    ]

    state_specific = {
        'CA': [
            "Transfer Disclosure Statement (TDS)",
            "Natural Hazard Disclosure (NHD) Report",
            "Mello-Roos / CFD Disclosure",
            "Megan's Law Database Disclosure",
            "Real Estate Transfer Disclosure Statement",
            "Smoke Alarm and Carbon Monoxide Device Compliance",
            "Home Energy Rating System (HERS) Disclosure",
            "Water Heater Bracing Compliance",
        ],
        'TX': [
            "TREC Seller's Disclosure Notice",
            "TREC Third Party Financing Addendum",
            "TREC Lead-Based Paint Addendum",
            "TREC Condominium Addendum (if condo)",
            "TREC Notice of Buyer Termination",
            "Property Tax Certificate",
            "HOA Resale Certificate",
            "MUD/Special Assessment District Disclosure",
        ],
        'FL': [
            "Seller's Property Disclosure (not mandatory but recommended)",
            "Condo Association Documents (if condo)",
            "HOA Covenants and Restrictions",
            "Flood Zone Determination",
            "Wind Mitigation Inspection Report",
            "Radon Disclosure",
            "Property Tax Disclosure Summary",
            "CLUE Report (insurance claims history)",
        ],
        'NY': [
            "Property Condition Disclosure Act Statement",
            "Lead-Based Paint Disclosure",
            "Attorney Representation Letter",
            "Co-op Board Application Package (co-op only)",
            "Right of First Refusal Waiver",
            "Flip Tax Disclosure (co-op)",
            "Property Tax Abatement Documents (421a, J-51)",
            "Certificate of Occupancy (if new construction)",
        ],
    }

    checklist = {
        'universal': universal,
        'state_specific': state_specific.get(state, []),
        'additional': [],
    }

    if transaction_type == 'new_construction':
        checklist['additional'] = [
            "Certificate of Occupancy",
            "Builder's Warranty",
            "Spec Sheet / Floor Plan",
            "Upgrade Selection Sheet",
            "Permit Closings",
            "Warranty of Habitability",
        ]
    elif transaction_type == 'short_sale':
        checklist['additional'] = [
            "Short Sale Approval Letter",
            "Third Party Authorization",
            "Hardship Letter",
            "Financial Statement (seller)",
            "Tax Returns (2 years)",
            "Broker Price Opinion (BPO)",
            "Negotiation Log",
        ]

    return checklist

def print_checklist(state='TX', transaction_type='resale'):
    checklist = transaction_checklist(state, transaction_type)

    print("=" * 70)
    print(f"TRANSACTION CHECKLIST: {state.upper()} | {transaction_type.replace('_', ' ').title()}")
    print("=" * 70)

    print(f"\n📋 UNIVERSAL DOCUMENTS ({len(checklist['universal'])} items)")
    for i, item in enumerate(checklist['universal'], 1):
        print(f"  [ ] {i:2d}. {item}")

    if checklist['state_specific']:
        print(f"\n📍 {state.upper()}-SPECIFIC ({len(checklist['state_specific'])} items)")
        for i, item in enumerate(checklist['state_specific'], 1):
            print(f"  [ ] {i:2d}. {item}")

    if checklist['additional']:
        print(f"\n📎 ADDITIONAL ({transaction_type.replace('_', ' ').title()}) ({len(checklist['additional'])} items)")
        for i, item in enumerate(checklist['additional'], 1):
            print(f"  [ ] {i:2d}. {item}")

    print(f"\n{'='*70}")
    print(f"Total: {len(checklist['universal']) + len(checklist['state_specific']) + len(checklist['additional'])} items")
    return checklist

checklist = print_checklist('CA', 'resale')
```

## Key Compliance Deadlines

| Milestone | Days Before/After Contract | Responsible Party |
|---|---|---|
| Deliver disclosures | Within 3-7 days of contract acceptance | Seller/Agent |
| Earnest money deposited | Within 3 business days of contract | Buyer/Agent |
| Inspection period ends | Per contract (typically 10-14 days) | Buyer |
| Loan application submitted | Within 5 days of contract | Buyer/Lender |
| Appraisal ordered | Within 5 days of application | Lender |
| Appraisal received | 14-21 days before closing | Lender |
| Title commitment received | 10-14 days before closing | Title Company |
| Homeowners insurance bound | 7 days before closing | Buyer |
| Closing Disclosure sent | 3 business days before closing | Lender |
| Final walk-through | 1-2 days before closing | Buyer/Agent |
| Funds wired to title | 1 day before closing | Buyer |
| Sign closing docs | Closing day | All parties |
| Deed recorded | Closing day + 0-3 days | Title/County |
| Commission paid | At recording | Broker/Title |

## Key Disclaimers & Required Language

### Fair Housing (Mandatory on All Marketing Materials)
```
"This property is available for equal housing opportunity. We do not discriminate on the 
basis of race, color, religion, sex, handicap, familial status, national origin, or any 
other protected class."
```

### Brokerage Disclosure
```
"[Broker Name] represents the [seller/buyer/transaction] in this transaction. Commission 
paid by [seller/buyer/both] as agreed in the listing/buyer representation agreement."
```

### Agency Disclosure
```
- Seller's Agent: Represents the seller and owes fiduciary duties to the seller
- Buyer's Agent: Represents the buyer and owes fiduciary duties to the buyer
- Dual Agent: Represents both buyer and seller (where permitted by law)
- Transaction Broker: Facilitates the transaction without representing either party (CO, FL, etc.)
```

## Transaction Communication Log

```python
from datetime import datetime, timedelta

class TransactionTracker:
    def __init__(self, address, contract_date, closing_date):
        self.address = address
        self.contract_date = contract_date
        self.closing_date = closing_date
        self.milestones = []
        self.contacts = []

    def add_milestone(self, name, due_date, completed=False, notes=''):
        self.milestones.append({
            'name': name,
            'due_date': due_date,
            'completed': completed,
            'notes': notes,
        })

    def log_contact(self, party, method, summary):
        self.contacts.append({
            'timestamp': datetime.now(),
            'party': party,
            'method': method,
            'summary': summary,
        })

    def days_to_closing(self):
        return (self.closing_date - datetime.now().date()).days

    def status_report(self):
        total = len(self.milestones)
        done = sum(1 for m in self.milestones if m['completed'])
        overdue = [m for m in self.milestones if not m['completed'] and m['due_date'] < datetime.now().date()]

        print(f"\n{'='*60}")
        print(f"TRANSACTION STATUS: {self.address}")
        print(f"{'='*60}")
        print(f"Contract: {self.contract_date}")
        print(f"Closing:  {self.closing_date} ({self.days_to_closing()} days away)")
        print(f"Progress: {done}/{total} milestones ({int(done/total*100)}%)" if total else "Progress: 0/0")
        if overdue:
            print(f"⚠️ OVERDUE ({len(overdue)}):")
            for m in overdue:
                print(f"  - {m['name']} (due {m['due_date']})")
        print()
        for m in self.milestones:
            status = '✅' if m['completed'] else '⏳' if m['due_date'] >= datetime.now().date() else '⚠️'
            print(f"  {status} {m['name']:40s} Due: {m['due_date']}  {m['notes'][:30]}")
        print(f"\n📞 Recent Contacts:")
        for c in self.contacts[-5:]:
            print(f"  {c['timestamp'].strftime('%m/%d %H:%M')} | {c['party']:15s} | {c['method']:6s} | {c['summary'][:50]}")

# Example
tracker = TransactionTracker(
    address="123 Main St, Austin, TX 78701",
    contract_date=datetime(2026, 8, 1).date(),
    closing_date=datetime(2026, 9, 15).date(),
)
tracker.add_milestone("Deliver disclosures", datetime(2026, 8, 4).date(), True)
tracker.add_milestone("Earnest money deposited", datetime(2026, 8, 5).date(), True)
tracker.add_milestone("Inspection completed", datetime(2026, 8, 14).date(), False)
tracker.add_milestone("Loan application submitted", datetime(2026, 8, 7).date(), True)
tracker.add_milestone("Appraisal ordered", datetime(2026, 8, 10).date(), True)
tracker.add_milestone("Appraisal received", datetime(2026, 9, 1).date(), False)
tracker.add_milestone("Title commitment received", datetime(2026, 9, 5).date(), False)
tracker.add_milestone("Closing Disclosure sent", datetime(2026, 9, 12).date(), False)
tracker.add_milestone("Final walk-through", datetime(2026, 9, 14).date(), False)
tracker.add_milestone("Funds wired", datetime(2026, 9, 14).date(), False)
tracker.log_contact("Buyer", "Email", "Sent inspection report summary")
tracker.log_contact("Lender", "Phone", "Confirmed appraisal ordered")
tracker.log_contact("Title Co", "Email", "Received draft title commitment")
tracker.status_report()
```

## Common Pitfalls

- **Missing state-specific deadlines**: Each state has unique timelines for delivering disclosure, right to cancel, and attorney review periods.
- **Using outdated forms**: State real estate commissions update forms regularly. Always download current forms from your association before each transaction.
- **Forgetting the 3-day CD rule**: Closing Disclosure must be received by buyer at least 3 business days before closing. Count business days correctly.
- **Neglecting TRID compliance**: Late CD delivery = automatic 3-day closing delay. No exceptions.
- **Assuming all states are similar**: California's 17-day inspection contingency, Texas's option period, and New York's attorney review are fundamentally different.
- **Not verifying earnest money**: Confirm the earnest money was deposited into escrow and provide receipt within 3 days.
- **Skipping final walk-through**: Even in "as-is" transactions, document condition with time-stamped photos.
- **Ignoring FIRPTA**: Foreign seller = 15% withholding. File IRS Form 8288 within 20 days of closing.
- **Overlooking HOA estoppel**: Condo/townhouse transactions need an estoppel certificate showing current assessments and transfer fees.
- **Not documenting wire instructions securely**: Wire fraud is rampant. Always verify wiring instructions in person or by phone, never by email.
- **Missing tax proration errors**: Property tax prorations are commonly miscalculated. Verify the tax year, rate, and exemptions.

## Verification Checklist

- [ ] State-specific disclosure checklist compiled and cross-referenced with state RE commission
- [ ] All mandatory disclosures delivered within statutory timeline
- [ ] Earnest money receipt confirmed and filed
- [ ] Lead-Based Paint disclosure delivered (if property built pre-1978)
- [ ] Agency disclosure signed by all parties
- [ ] Home inspection completed, report delivered to buyer
- [ ] Termite/WDO inspection received and reviewed
- [ ] Appraisal received and value confirmed
- [ ] Title commitment reviewed for encumbrances, easements, exceptions
- [ ] Survey reviewed (if ordered) — property boundaries, encroachments
- [ ] HOI binder received and coverage adequate (replacement cost)
- [ ] Closing Disclosure received by buyer 3+ business days before closing
- [ ] Final walk-through completed and documented (photos + signed form)
- [ ] Funds confirmed wired (title company verification number)
- [ ] FIRPTA reviewed (foreign seller = withholding required)
- [ ] Commission agreement signed and amounts verified
- [ ] Property tax proration calculated and agreed
- [ ] HOA/condo estoppel obtained (if applicable)
- [ ] Post-closing: deed recording confirmed, commission paid, file archived
- [ ] All disclaimers and required fair housing language included