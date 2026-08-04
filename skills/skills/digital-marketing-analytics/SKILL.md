---
name: digital-marketing-analytics
description: "Use when analyzing marketing data. ROI, attribution, CAC."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [marketing, analytics, roi, attribution, cac, ltv]
    related_skills: [marketing-analytics-dashboard, content-marketing-strategy]
---

# Digital Marketing Analytics Framework

## Overview
Measure, analyze, and optimize marketing performance across digital channels using data-driven attribution, lifetime value modeling, customer acquisition cost analysis, and ROI optimization. Covers UTM tagging, conversion tracking, cohort analysis, multi-touch attribution, and marketing mix modeling.

## When to Use
- "Calculate customer acquisition cost (CAC)"
- "Build attribution model for marketing channels"
- "Optimize marketing ROI across channels"
- "Analyze marketing funnel conversion rates"
- "Build customer lifetime value model"

## Core Metrics Framework

### Acquisition Metrics
| Metric | Formula | Target |
|--------|---------|--------|
| CAC | Marketing Spend / New Customers | < LTV/3 |
| Conversion Rate (Site) | Conversions / Visitors | 2-5% (varies by industry) |
| Conversion Rate (Lead) | Qualified Leads / MQLs | 20-30% |
| Cost Per Click (CPC) | Ad Spend / Clicks | Channel-dependent |
| Cost Per Acquisition (CPA) | Ad Spend / Conversions | Varies by value |

### Retention Metrics
| Metric | Formula | Target |
|--------|---------|--------|
| Churn Rate | (Customers Lost / Active Customers) | <5% monthly |
| Retention Rate | (Customers at End - New) / Customers at Start | >85% |
| Lifetime Value (LTV) | ARPU × Gross Margin / Churn Rate | >3x CAC |

### Revenue Metrics
| Metric | Formula | Target |
|--------|---------|--------|
| ROAS | Revenue / Ad Spend | >3:1 |
| ROI | (Revenue - Cost) / Cost | >300% |
| LTV:CAC Ratio | LTV / CAC | >3:1 |
| Payback Period | CAC / (ARPU - Variable Cost) | <12 months |

## UTM Tracking Implementation
```python
# Consistent UTM parameter structure
def generate_utm_url(base_url, source, medium, campaign, content="", term=""):
    """
    Generate UTM-tagged URLs for campaign tracking
    
    Args:
        base_url: Landing page URL
        source: google, facebook, newsletter, etc.
        medium: cpc, email, social, etc.
        campaign: product_launch_q3, retention_email, etc.
        content: Optional for A/B testing (banner_ad, text_link)
        term: Optional for paid search (keyword)
    
    Returns:
        Full URL with UTM parameters
    """
    params = {
        "utm_source": source,
        "utm_medium": medium,
        "utm_campaign": campaign,
    }
    if content:
        params["utm_content"] = content
    if term:
        params["utm_term"] = term
    
    from urllib.parse import urlencode, urlparse, urlunparse
    parsed = urlparse(base_url)
    query = urlencode(params)
    
    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        "",
        query,
        ""
    ))

# Example usage:
# https://yoursite.com/landing?utm_source=google&utm_medium=cpc&utm_campaign=...
```

## Multi-Touch Attribution Modeling

### Attribution Model Comparison
```python
import pandas as pd
import numpy as np

class AttributionModel:
    def __init__(self, touchpoint_data):
        self.touchpoints = touchpoint_data  # DataFrame: customer_id, channel, timestamp, conversion
        
    def first_touch_attribution(self):
        """
        Credit first touchpoint with 100% of conversion
        """
        first_touches = self.touchpoints.groupby('customer_id').first()
        return first_touches.groupby('channel').size()
    
    def last_touch_attribution(self):
        """
        Credit last touchpoint with 100% of conversion
        """
        last_touches = self.touchpoints.groupby('customer_id').last()
        return last_touches.groupby('channel').size()
    
    def linear_attribution(self):
        """
        Equal credit to all touchpoints
        """
        touchpoint_counts = self.touchpoints.groupby(['customer_id', 'channel']).size()
        conversions = self.touchpoints[self.touchpoints['conversion']==True].groupby('customer_id').size()
        
        credit = touchpoint_counts / touchpoint_counts.groupby('customer_id').transform('count')
        channel_credit = credit.groupby('channel').sum() * conversions.mean()
        
        return channel_credit
    
    def time_decay_attribution(self, decay_lambda=0.5):
        """
        More weight to touchpoints closer to conversion
        """
        # Calculate time difference from conversion
        conversion_times = self.touchpoints[self.touchpoints['conversion']==True].groupby('customer_id')['timestamp'].min()
        
        # Apply exponential decay (closer to conversion = higher weight)
        credits = []
        for cust_id, touchpoints in self.touchpoints.groupby('customer_id'):
            conv_time = conversion_times.get(cust_id)
            if conv_time and len(touchpoints) > 0:
                time_diffs = (conv_time - touchpoints['timestamp']).dt.total_seconds()
                weights = np.exp(-decay_lambda * time_diffs)
                normalized = weights / weights.sum() * touchpoints['conversion'].iloc[-1]
                for i, idx in enumerate(touchpoints.index):
                    credits.append({
                        'channel': touchpoints.iloc[i]['channel'],
                        'credit': normalized.iloc[i]
                    })
        
        credits_df = pd.DataFrame(credits)
        return credits_df.groupby('channel')['credit'].sum()
    
    def data_driven_attribution(self):
        """
        Use Markov chains to determine channel influence
        """
        from collections import Counter
        
        # Build transition matrix
        transitions = []
        conversions = []
        
        for cust_id, touchpoints in self.touchpoints.groupby('customer_id'):
            channels = touchpoints['channel'].tolist()
            transitions.extend(list(zip(channels[:-1], channels[1:])))
            if touchpoints['conversion'].iloc[-1]:
                conversions.append(channels[-1])
        
        # Count transitions
        transition_counts = Counter(transitions)
        conversion_counts = Counter(conversions)
        
        # Calculate removal effect for each channel
        base_conversion_rate = len(conversions) / len(self.touchpoints['customer_id'].unique())
        
        channel_importance = {}
        for channel in set(t for _, t in transitions):
            # Remove channel and recalculate conversion rate
            filtered_transitions = [t for t in transitions if t[0] != channel and t[1] != channel]
            # Simplified — real implementation uses full Markov chain removal
            channel_importance[channel] = len([c for c in conversions if c != channel]) / max(1, len(filtered_transitions))
        
        return channel_importance

# Usage comparison
model = AttributionModel(touchpoint_data)
print("First Touch:", model.first_touch_attribution().to_dict())
print("Last Touch:", model.last_touch_attribution().to_dict())
print("Linear:", model.linear_attribution().to_dict())
print("Time Decay:", model.time_decay_attribution().to_dict())
```

## Cohort Analysis & LTV Modeling

### Customer Lifetime Value Calculation
```python
def calculate_ltv(cohort_data, discount_rate=0.1):
    """
    Calculate LTV by customer cohort
    
    Args:
        cohort_data: DataFrame with customer cohorts and revenue over time
        discount_rate: Annual discount rate for NPV calculation
    
    Returns:
        LTV metrics by cohort
    """
    # Group by cohort (first purchase month)
    cohort_data['cohort'] = cohort_data.groupby('customer_id')['first_purchase_date'].transform('min').dt.to_period('M')
    
    # Calculate cohort sizes
    cohorts = cohort_data.groupby(['cohort', 'order_number']).agg(
        customers=('customer_id', 'nunique'),
        total_revenue=('revenue', 'sum')
    ).reset_index()
    
    # Revenue per user per period
    cohorts['revenue_per_user'] = cohorts['total_revenue'] / cohorts['customers']
    
    # LTV by cohort with discounting
    ltv_by_cohort = {}
    
    for cohort, cohort_df in cohorts.groupby('cohort'):
        periods = cohort_df['order_number'].values
        revenues = cohort_df['revenue_per_user'].values
        
        # Discount future cash flows
        discounted_cash_flows = []
        cumulative_ltv = 0
        
        for i, (period, revenue) in enumerate(zip(periods, revenues)):
            discounted = revenue / ((1 + discount_rate) ** (period / 12))
            discounted_cash_flows.append(discounted)
            cumulative_ltv += discounted
        
        ltv_by_cohort[cohort] = {
            "cohort_size": int(cohort_df['customers'].iloc[0]),
            "ltv": round(cumulative_ltv, 2),
            "ltv_12_month": round(sum(discounted_cash_flows[:12]), 2),
            "ltv_24_month": round(sum(discounted_cash_flows[:24]), 2)
        }
    
    return ltv_by_cohort
```

## Marketing Mix Modeling (MMM)

### Channel Contribution Analysis
```python
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

def marketing_mix_model(channel_data, target='sales'):
    """
    Attribution across marketing channels with diminishing returns
    
    Args:
        channel_data: DataFrame with channel spend and control variables
    """
    # Apply diminishing returns transformation (Hill function)
    channels = ['tv_spend', 'digital_spend', 'radio_spend', 'print_spend']
    
    # Hill function: y = x^n / (k^n + x^n)
    def hill_transform(spend, k=100000, n=0.5):
        return spend**n / (k**n + spend**n)
    
    # Transform spend data
    transformed_channels = pd.DataFrame()
    for ch in channels:
        if ch in channel_data.columns:
            transformed_channels[ch] = hill_transform(channel_data[ch])
    
    # Add control variables
    X = pd.concat([
        transformed_channels,
        channel_data[['seasonality_index', 'competitor_spend', 'economic_indicator']]
    ], axis=1)
    
    y = channel_data[target]
    
    # Fit model
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = LinearRegression()
    model.fit(X_scaled, y)
    
    # Feature importance (channels ranked)
    importance = dict(zip(X.columns, model.coef_))
    
    # Calculate ROI per channel
    roi = {}
    for i, channel in enumerate(channels):
        if channel in channel_data.columns:
            total_spend = channel_data[channel].sum()
            predicted_contribution = model.coef_[i] * transformed_channels[channel].sum()
            roi[channel] = round((predicted_contribution - total_spend) / total_spend * 100, 1)
    
    return {
        "model_coefficients": dict(zip(X.columns, model.coef_)),
        "r2_score": model.score(X_scaled, y),
        "channel_roi": roi,
        "baseline_sales": model.intercept_
    }
```

## Dashboard KPI Framework

### Marketing Funnel Tracking
```python
def marketing_funnel_kpis(traffic_data, conversion_data):
    """
    Calculate funnel metrics from traffic to conversion
    """
    funnel = {
        "Awareness": traffic_data['impressions'],
        "Interest": traffic_data['clicks'],
        "Consideration": traffic_data['visits'],
        "Intent": conversion_data['add_to_cart'],
        "Purchase": conversion_data['conversions']
    }
    
    rates = {}
    stages = list(funnel.keys())
    
    for i in range(len(stages)-1):
        rate = funnel[stages[i+1]] / funnel[stages[i]] * 100 if funnel[stages[i]] > 0 else 0
        rates[f"{stages[i]} → {stages[i+1]}"] = round(rate, 2)
    
    return {
        "funnel_counts": funnel,
        "conversion_rates": rates,
        "overall_conversion": round(funnel["Purchase"] / funnel["Awareness"] * 100, 2)
    }
```

## Common Pitfalls
1. **Attribution model bias** — last-click overvalues bottom-of-funnel channels
2. **Not tracking offline conversions** — missing phone calls, store visits
3. **Wrong attribution window** — 1-day vs 30-day changes credit allocation
4. **Ignoring seasonality and trends** — holiday effects, macroeconomic shifts
5. **Not deduplicating users across devices** — same person on mobile+desktop
6. **Missing data sources** — offline ads, brand awareness not captured
7. **Over-reliance on vanity metrics** — likes/followers instead of business impact
8. **Not calculating true LTV:CAC ratio** — leading to unsustainable growth
9. **Wrong attribution lookback windows** — 7-day vs 90-day windows dramatically change results
10. **No cohort analysis** — aggregate metrics hide retention differences

## Verification Checklist
- [ ] UTM parameters consistently applied across all campaigns
- [ ] Conversion tracking pixel installed and firing correctly
- [ ] At least 2 attribution models compared (last-click vs data-driven)
- [ ] LTV:CAC ratio >3:1 for target segments
- [ ] Marketing funnel drop-off points identified
- [ ] Cohort retention curves analyzed
- [ ] Channel ROI calculated with proper cost attribution
- [ ] Seasonality and trend effects controlled
- [ ] Offline conversions tracked and integrated
- [ ] Dashboard updated daily with reliable data sources