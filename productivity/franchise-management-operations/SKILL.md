---
name: franchise-management-operations
description: "Use when managing franchise operations and systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [franchise, operations, franchisor, franchisee, multi-location, expansion]
    related_skills: [retail-pos-systems, business-metrics-kpis, crm-sales-pipeline, project-management-workflows]
---

# Franchise Management and Operations

Managing franchise systems — from franchisor operations and franchisee support through multi-location standardization, training, compliance, and growth.

## When to Use

- Building franchise operations as a franchisor
- Opening and managing multiple franchise locations
- Standardizing operations across franchise units
- Creating franchise training and documentation
- Tracking franchise performance and compliance

## Franchise System Components

```python
from typing import Dict, List
from datetime import datetime, timedelta

class FranchiseSystem:
    """Manage a franchise network."""
    
    def __init__(self, brand_name: str, 
                 initial_fee: float = 35000,
                 royalty_pct: float = 0.06,
                 marketing_fund_pct: float = 0.02):
        self.brand = brand_name
        self.initial_fee = initial_fee
        self.royalty = royalty_pct
        self.marketing_fund = marketing_fund_pct
        self.franchisees = {}
        self.documents = {}
        self.standards = {}
    
    def add_franchisee(self, name: str, territory: str,
                       opened_date: str, initial_fee_paid: bool = False) -> str:
        import uuid
        fid = str(uuid.uuid4())[:8]
        self.franchisees[fid] = {
            'id': fid, 'name': name, 'territory': territory,
            'opened': opened_date, 'status': 'active',
            'initial_fee_paid': initial_fee_paid,
            'monthly_revenue': [], 'inspection_scores': [],
            'training_completed': [], 'compliance_issues': [],
        }
        return fid
    
    def record_monthly_revenue(self, fid: str, revenue: float, month: str):
        if fid in self.franchisees:
            royalty_due = revenue * self.royalty
            marketing_due = revenue * self.marketing_fund
            self.franchisees[fid]['monthly_revenue'].append({
                'month': month, 'revenue': revenue,
                'royalty_due': round(royalty_due, 2),
                'marketing_due': round(marketing_due, 2),
                'total_due': round(royalty_due + marketing_due, 2),
            })
    
    def add_inspection_score(self, fid: str, score: int, 
                              inspector: str, notes: str = ''):
        if fid in self.franchisees:
            self.franchisees[fid]['inspection_scores'].append({
                'date': datetime.now().isoformat(),
                'score': score, 'inspector': inspector,
                'passed': score >= 70, 'notes': notes,
            })
    
    def get_franchise_health(self) -> Dict:
        active = [f for f in self.franchisees.values() if f['status'] == 'active']
        if not active: return {}
        
        avg_inspection = []
        for f in active:
            scores = [s['score'] for s in f.get('inspection_scores', [])]
            if scores: avg_inspection.extend(scores)
        
        revenue_data = []
        for f in active:
            for m in f.get('monthly_revenue', []):
                revenue_data.append(m['revenue'])
        
        return {
            'total_franchisees': len(self.franchisees),
            'active': len(active),
            'avg_inspection_score': round(sum(avg_inspection)/len(avg_inspection), 1) if avg_inspection else 0,
            'avg_monthly_revenue': round(sum(revenue_data)/len(revenue_data), 2) if revenue_data else 0,
            'total_monthly_royalty': round(sum(m['royalty_due'] for f in active for m in f.get('monthly_revenue', [])), 2),
        }
```

## Operations Manual

```python
class OperationsManual:
    """Create and manage franchise operations documentation."""
    
    SECTIONS = [
        'Brand Standards', 'Opening Procedures', 'Daily Operations',
        'Staff Management', 'Customer Service', 'Inventory Management',
        'Marketing & Advertising', 'Financial Reporting', 'Health & Safety',
        'Technology Systems', 'Training Requirements', 'Compliance Checklist',
    ]
    
    @staticmethod
    def generate_toc() -> str:
        toc = "📋 Franchise Operations Manual\n" + "=" * 40 + "\n"
        for i, section in enumerate(OperationsManual.SECTIONS, 1):
            toc += f"\n{i:2d}. {section}"
        toc += "\n\n" + "-" * 40
        toc += "\nEach section includes: Purpose | Standards | Procedures | Checklists | Forms\n"
        return toc
    
    @staticmethod
    def create_section(section_name: str, brand: str) -> Dict:
        return {
            'section': section_name,
            'brand': brand,
            'last_updated': datetime.now().isoformat(),
            'version': '1.0',
            'content_structure': [
                {'type': 'purpose', 'label': 'Purpose of this section'},
                {'type': 'standards', 'label': 'Brand standards & minimum requirements'},
                {'type': 'procedures', 'label': 'Step-by-step procedures'},
                {'type': 'checklists', 'label': 'Daily/weekly/monthly checklists'},
                {'type': 'forms', 'label': 'Required forms and templates'},
                {'type': 'training', 'label': 'Training materials and videos'},
            ],
            'approval_required': True,
        }
```

## Franchise Recruitment

```python
class FranchiseRecruitment:
    """Manage franchise sales and recruitment pipeline."""
    
    QUALIFICATION_CRITERIA = {
        'net_worth_min': 250000,
        'liquid_assets_min': 100000,
        'industry_experience': 'preferred',
        'management_experience_years': 3,
        'credit_score_min': 680,
    }
    
    @staticmethod
    def qualify_candidate(financials: Dict) -> Dict:
        issues = []
        passed = True
        
        if financials.get('net_worth', 0) < 250000:
            issues.append(f"Net worth ${financials.get('net_worth', 0):,} below ${250000:,} minimum")
            passed = False
        
        if financials.get('liquid_assets', 0) < 100000:
            issues.append(f"Liquid assets ${financials.get('liquid_assets', 0):,} below ${100000:,} minimum")
            passed = False
        
        if financials.get('credit_score', 0) < 680:
            issues.append(f"Credit score {financials.get('credit_score', 0)} below 680 minimum")
            passed = False
        
        return {
            'qualified': passed,
            'issues': issues,
            'recommendation': 'Proceed to FDD review' if passed else 'Does not meet minimum requirements',
        }
```

## Common Pitfalls

1. **No standardized operations** — each franchisee runs differently; enforce SOPs
2. **Weak training program** — under-trained franchisees fail; invest in onboarding
3. **Inconsistent brand experience** — customers expect same experience at every location
4. **Not enforcing compliance** — brand standards degrade without inspections
5. **Poor franchisee selection** — selling to unqualified candidates creates failures
6. **Inadequate support** — franchisees need ongoing support beyond opening

## Verification Checklist

- [ ] Franchise Disclosure Document (FDD) current and compliant
- [ ] Operations manual written and maintained
- [ ] Training program (initial + ongoing) established
- [ ] Quality inspection program with scoring
- [ ] Royalty and marketing fund collection system in place
- [ ] Territory mapping completed
- [ ] Franchisee recruitment qualification criteria defined
- [ ] Legal compliance verified (state registrations)

## See Also

- retail-pos-systems — POS standardization across franchise
- business-metrics-kpis — franchisee performance metrics
- crm-sales-pipeline — franchise sales pipeline
- project-management-workflows — franchisee onboarding workflow
