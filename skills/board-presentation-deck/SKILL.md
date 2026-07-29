---
name: board-presentation-deck
description: "Use when preparing board presentations and materials."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [board-deck, board-meeting, investor-reporting, governance, presentation]
    related_skills: [fundraising-investor-pitch, business-metrics-kpis, saas-metrics-reporting, financial-modeling-budgeting]
---

# Board Presentation and Governance

Preparing board meeting presentations and governance materials — from executive summaries and KPI dashboards through strategic discussions and board packs.

## When to Use

- Preparing quarterly board meeting presentations
- Building board packs with financial and operational KPIs
- Communicating strategy, risks, and milestones to the board
- Preparing for board committee meetings (audit, compensation)
- Creating board-level strategic updates

## Board Deck Structure

```python
BOARD_DECK_SLIDES = {
    'executive_summary': 'High-level highlights and lowlights (1 page)',
    'financials': 'Revenue, P&L, cash flow, balance sheet, burn rate',
    'kpi_dashboard': 'ARR, MRR, Churn, CAC, LTV, NPS, headcount',
    'operational_metrics': 'Usage, customers, pipeline, product adoption',
    'strategic_business': 'Key initiatives, milestones, competitive landscape',
    'risks_and_mitigations': 'Top risks and mitigation plans',
    'ask': 'Decisions needed from the board',
    'appendix': 'Detailed back-up slides for reference',
}

class BoardDeck:
    """Generate board meeting materials."""
    def __init__(self, period: str, company: str):
        self.period = period
        self.company = company
    
    def executive_summary(self, highlights: List[str], 
                          lowlights: List[str], cash: float) -> str:
        summary = f"📊 {self.company} — Board Summary ({self.period})\n"
        summary += "=" * 50 + "\n\n✅ Highlights:\n"
        for h in highlights: summary += f"  • {h}\n"
        summary += "\n⚠️ Lowlights:\n"
        for l in lowlights: summary += f"  • {l}\n"
        summary += f"\n💰 Cash: ${cash:,.0f}"
        return summary
```

## Common Pitfalls

1. **Too much detail** — board wants strategy, decisions, not operational minutiae
2. **No bad news** — hiding problems from the board erodes trust; share risks early
3. **No ask** — board meetings should result in decisions; have clear asks
4. **Inconsistent metrics** — defining metrics differently each quarter confuses comparison
5. **No competitive context** — board needs to know how you're performing vs market

## Verification Checklist

- [ ] Executive summary (1-2 pages max)
- [ ] Financial metrics consistent with prior reporting
- [ ] KPI dashboard with targets and comparison to prior periods
- [ ] Strategic initiatives with milestones
- [ ] Risk register with mitigation plans
- [ ] Clear "asks" for board decisions
- [ ] Board pack distributed 5+ days before meeting
- [ ] Appendix available for deep-dive questions
- [ ] CEO/CFO scripts aligned on key messages
