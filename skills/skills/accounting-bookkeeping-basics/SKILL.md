---
name: accounting-bookkeeping-basics
description: "Use when managing accounting and bookkeeping processes."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [accounting, bookkeeping, financial-statements, GAAP, tax, cash-basis, accrual]
    related_skills: [financial-modeling-budgeting, business-metrics-kpis, tax-planning-small-business, business-insurance-guide]
---

# Accounting and Bookkeeping Basics

Managing accounting and bookkeeping processes — from financial statements and chart of accounts through accrual vs cash accounting, reconciliations, and closing the books.

## When to Use

- Setting up accounting for a new business
- Understanding financial statements (P&L, Balance Sheet, Cash Flow)
- Managing accounts payable and receivable
- Preparing for tax filing or audits
- Building financial reporting processes

## Accounting Framework

```python
ACCOUNTING_CONCEPTS = {
    'double_entry': 'Every transaction affects at least two accounts (debit = credit)',
    'accrual': 'Revenue recognized when earned, expenses when incurred (not when cash moves)',
    'cash_basis': 'Revenue recognized when cash received, expenses when paid',
    'gaap': 'Generally Accepted Accounting Principles — standard framework',
}

class ChartOfAccounts:
    """Standard chart of accounts categories."""
    def __init__(self):
        self.accounts = {
            'assets': ['Cash', 'Accounts Receivable', 'Inventory', 'Equipment'],
            'liabilities': ['Accounts Payable', 'Accrued Expenses', 'Deferred Revenue', 'Loans'],
            'equity': ['Common Stock', 'Retained Earnings', 'Paid-in Capital'],
            'revenue': ['Product Revenue', 'Service Revenue', 'Interest Income'],
            'expenses': ['COGS', 'Salaries', 'Rent', 'Marketing', 'Software', 'Professional Fees'],
        }
    
    def add_account(self, category: str, name: str):
        if category in self.accounts:
            self.accounts[category].append(name)
```

## Common Pitfalls

1. **Mixing personal and business finances** — separate bank accounts and credit cards
2. **No chart of accounts** — without structure, categories become inconsistent
3. **Not reconciling monthly** — bank rec catches errors; do it monthly
4. **Misclassifying expenses** — CAPEX vs OPEX matters for tax and financial reporting
5. **Forgetting deferred revenue** — cash received for not-yet-delivered services is a liability

## Verification Checklist

- [ ] Chart of accounts established
- [ ] Separate business bank account and credit card
- [ ] Accounting software configured (QBO, Xero, FreshBooks)
- [ ] Bank accounts reconciled monthly
- [ ] Accounts payable and receivable tracked
- [ ] Invoicing system set up with payment terms
- [ ] Sales tax registration (if applicable)
- [ ] CPA/tax advisor engaged for tax planning
- [ ] Financial statements reviewed monthly (P&L, Balance Sheet, Cash Flow)
