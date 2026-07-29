---
name: competitive-intelligence-analysis
description: "Use when researching competitors and market positioning."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [competitive-intelligence, market-research, competitor-analysis, positioning, SWOT]
    related_skills: [pricing-strategy-optimization, product-management-roadmap, digital-marketing-strategy, saas-metrics-reporting]
---

# Competitive Intelligence Analysis

Researching, tracking, and analyzing competitors to inform product, marketing, and business strategy.

## When to Use

- Analyzing the competitive landscape before entering a market
- Tracking competitor product, pricing, and positioning changes
- Preparing competitive battle cards for sales teams
- Identifying market gaps and differentiation opportunities
- Informing product roadmap and strategic decisions

## Competitive Analysis Frameworks

```python
from typing import Dict, List, Optional
from datetime import datetime

class CompetitiveAnalysis:
    """Framework for competitive research and analysis."""
    
    @staticmethod
    def swot(company: Dict) -> Dict:
        """SWOT Analysis: Strengths, Weaknesses, Opportunities, Threats."""
        return {
            'strengths': company.get('strengths', []),
            'weaknesses': company.get('weaknesses', []),
            'opportunities': company.get('opportunities', []),
            'threats': company.get('threats', []),
        }
    
    @staticmethod
    def porter_five_forces(industry: str) -> Dict:
        """Porter's Five Forces analysis template."""
        return {
            'threat_of_new_entrants': {
                'score': None,  # 1-5 (5 = high threat)
                'factors': ['Capital requirements', 'Brand loyalty', 'Regulatory barriers'],
            },
            'bargaining_power_of_suppliers': {
                'score': None,
                'factors': ['Number of suppliers', 'Switching costs', 'Substitute inputs'],
            },
            'bargaining_power_of_buyers': {
                'score': None,
                'factors': ['Number of buyers', 'Price sensitivity', 'Product differentiation'],
            },
            'threat_of_substitutes': {
                'score': None,
                'factors': ['Availability of substitutes', 'Price-performance tradeoff'],
            },
            'competitive_rivalry': {
                'score': None,
                'factors': ['Number of competitors', 'Industry growth rate', 'Exit barriers'],
            },
        }
```

## Competitor Tracking

```python
class CompetitorTracker:
    """Track competitor activities and changes over time."""
    
    def __init__(self):
        self.competitors = {}
        self.signals = []
    
    def add_competitor(self, name: str, website: str, 
                       category: str, description: str = '') -> str:
        import uuid
        cid = str(uuid.uuid4())[:8]
        self.competitors[cid] = {
            'id': cid, 'name': name, 'website': website,
            'category': category, 'description': description,
            'signals': [], 'products': [], 'market_share': None,
        }
        return cid
    
    def record_signal(self, competitor_id: str, signal_type: str,
                      description: str, source_url: str = '',
                      severity: str = 'info'):
        """Record a competitive signal (product launch, funding, hire, etc.)."""
        signal = {
            'date': datetime.now().isoformat(),
            'type': signal_type,  # product_launch, pricing_change, funding, hire, partnership, etc.
            'description': description,
            'source': source_url,
            'severity': severity,
        }
        if competitor_id in self.competitors:
            self.competitors[competitor_id]['signals'].append(signal)
        self.signals.append({'competitor_id': competitor_id, **signal})
    
    def get_recent_signals(self, days: int = 30) -> List[Dict]:
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=days)
        recent = []
        for s in self.signals:
            if datetime.fromisoformat(s['date']) >= cutoff:
                recent.append(s)
        return sorted(recent, key=lambda x: x['date'], reverse=True)
    
    def generate_newsletter(self) -> str:
        """Generate competitive intelligence digest."""
        report = "🔍 Competitive Intelligence Digest\n"
        report += f"Date: {datetime.now().strftime('%B %d, %Y')}\n"
        report += "=" * 50 + "\n"
        
        for cid, comp in self.competitors.items():
            recent = [s for s in comp['signals'] 
                     if (datetime.now() - datetime.fromisoformat(s['date'])).days <= 30]
            if recent:
                report += f"\n**{comp['name']}**\n"
                for s in recent:
                    report += f"  {s['severity'].upper()}: {s['description']}\n"
        
        return report
```

## Battle Card Builder

```python
class BattleCard:
    """Create competitive battle cards for sales teams."""
    
    @staticmethod
    def create(our_product: Dict, competitor: Dict) -> Dict:
        return {
            'our_company': our_product.get('company', ''),
            'competitor': competitor.get('name', ''),
            'overview': competitor.get('description', ''),
            'head_to_head': BattleCard._compare_features(our_product, competitor),
            'our_advantages': our_product.get('advantages', []),
            'their_weaknesses': competitor.get('weaknesses', []),
            'common_objections': BattleCard._objection_handling(our_product, competitor),
            'win_stories': [],
        }
    
    @staticmethod
    def _compare_features(us: Dict, them: Dict) -> List[Dict]:
        comparison = []
        our_features = us.get('features', {})
        their_features = them.get('features', {})
        all_keys = set(list(our_features.keys()) + list(their_features.keys()))
        
        for key in sorted(all_keys):
            our_val = our_features.get(key, '—')
            their_val = their_features.get(key, '—')
            winner = 'us' if our_val != '—' and their_val == '—' else (
                'them' if their_val != '—' and our_val == '—' else 'tie')
            comparison.append({
                'feature': key, 'us': our_val, 'them': their_val, 'winner': winner,
            })
        
        return comparison
    
    @staticmethod
    def _objection_handling(us: Dict, them: Dict) -> List[Dict]:
        return [
            {
                'objection': f"Their product is cheaper",
                'response': f"While {them.get('name')} has a lower entry price, {us.get('company')} offers [specific advantage] that delivers [specific value] justifying the investment.",
            },
            {
                'objection': f"They have more features",
                'response': f"{them.get('name')} may have more features, but {us.get('company')} focuses on doing [core value] better than anyone else, with [specific metric] results.",
            },
        ]
```

## Market Positioning

```python
class MarketPositioning:
    """Analyze market positioning and differentiation."""
    
    @staticmethod
    def perceptual_map(competitors: List[Dict], dim1: str, dim2: str) -> Dict:
        """Position competitors on a 2D perceptual map."""
        return {
            'x_axis': dim1,
            'y_axis': dim2,
            'positions': {
                c['name']: {'x': c.get(dim1, 5), 'y': c.get(dim2, 5)}
                for c in competitors
            },
            'analysis': "Position yourself where competitors aren't concentrated",
        }
    
    @staticmethod
    def differentiation_matrix(features: List[str], 
                               competitors: List[Dict]) -> str:
        """Create a feature comparison matrix."""
        table = "Feature".ljust(25) + " | US"
        for c in competitors:
            table += f" | {c.get('name', '')[:10]}".ljust(14)
        table += "\n" + "-" * (25 + 14 * (len(competitors) + 1)) + "\n"
        
        for feature in features:
            table += feature.ljust(25) + " | ✅"
            for c in competitors:
                has = c.get('features', {}).get(feature, False)
                table += f" | {'✅' if has else '❌'}".ljust(14)
            table += "\n"
        
        return table
```

## Common Pitfalls

1. **Paralysis by analysis** — spending too much time on analysis, not enough on action
2. **Only tracking direct competitors** — indirect competitors and substitutes can disrupt you
3. **Copying competitors** — competitive analysis should find gaps, not tell you what to build
4. **Outdated intelligence** — competitor landscape changes fast; update signals weekly
5. **Confirmation bias** — looking for data that confirms you're better; be objective
6. **Not sharing with teams** — CI is useless if sales and product don't know about it

## Verification Checklist

- [ ] Top 3-5 competitors identified and tracked
- [ ] Competitive signals monitored (weekly)
- [ ] SWOT analysis completed
- [ ] Battle cards created for sales team
- [ ] Feature comparison matrix maintained
- [ ] Market positioning mapped
- [ ] CI digest shared with relevant teams
- [ ] Pricing and packaging compared regularly

## See Also

- pricing-strategy-optimization — competitive pricing analysis
- product-management-roadmap — features from competitive gaps
- digital-marketing-strategy — positioning in the market
- saas-metrics-reporting — benchmarking against competitors
