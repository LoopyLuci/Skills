---
name: website-analytics-tracking
description: "Use when setting up website analytics and tracking systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [analytics, tracking, google-analytics, dashboards, metrics, GA4, event-tracking]
    related_skills: [seo-search-engine-optimization, cms-website-management, digital-marketing-strategy, conversion-rate-optimization]
---

# Website Analytics and Tracking

Setting up website analytics — from Google Analytics 4 implementation through event tracking, custom dashboards, conversion attribution, and data-driven decision making.

## When to Use

- Setting up analytics on a new website
- Implementing custom event tracking (clicks, form submissions, scrolls)
- Building performance dashboards and reports
- Configuring conversion tracking and attribution
- Analyzing user behavior to improve experience

## Analytics Setup

### GA4 Implementation

```python
import json
from typing import Dict, List, Optional

class GA4Setup:
    """Guide to implementing Google Analytics 4."""
    
    MEASUREMENT_IDS = {
        'web': 'G-XXXXXXXXXX',
        'firebase': 'Firebase project ID',
    }
    
    @staticmethod
    def generate_gtag_code(measurement_id: str) -> str:
        """Generate GA4 gtag.js snippet."""
        return f'''
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{measurement_id}', {{
    'cookie_flags': 'SameSite=None;Secure',
    'cookie_domain': 'auto',
    'send_page_view': true
  }});
</script>
'''
    
    @staticmethod
    def generate_gcm_config() -> str:
        """Google Consent Mode v2 configuration."""
        return '''
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  
  // Default consent state
  gtag('consent', 'default', {
    'ad_storage': 'denied',
    'analytics_storage': 'denied',
    'ad_user_data': 'denied',
    'ad_personalization': 'denied',
    'functionality_storage': 'granted',
    'personalization_storage': 'denied',
    'security_storage': 'granted',
    'wait_for_update': 500
  });
</script>
'''
```

### Custom Event Tracking

```python
class EventTracker:
    """Implement custom event tracking."""
    
    # Standard GA4 event categories
    EVENT_CATEGORIES = {
        'engagement': ['scroll_depth', 'time_on_page', 'video_view'],
        'conversion': ['form_submit', 'button_click', 'purchase', 'signup'],
        'navigation': ['internal_search', 'menu_click', 'outbound_click'],
        'ecommerce': ['add_to_cart', 'remove_from_cart', 'checkout_start', 'purchase'],
        'content': ['article_read', 'pdf_download', 'social_share'],
    }
    
    @staticmethod
    def generate_tracking_code(event_name: str, event_params: Dict = None) -> str:
        """Generate JavaScript for tracking a custom event."""
        params = json.dumps(event_params or {})
        return f'''
// Track event: {event_name}
gtag('event', '{event_name}', {params});

// Or for Google Tag Manager:
dataLayer.push({{
  'event': '{event_name}',
  ...{params}
}});
'''
    
    @staticmethod
    def track_form_submission(form_id: str, form_name: str) -> str:
        """Track form submissions."""
        return f'''
document.getElementById('{form_id}').addEventListener('submit', function() {{
  gtag('event', 'form_submit', {{
    'form_name': '{form_name}',
    'form_id': '{form_id}'
  }});
}});
'''
    
    @staticmethod
    def track_outbound_links() -> str:
        """Track all outbound link clicks automatically."""
        return '''
document.addEventListener('click', function(e) {
  var target = e.target.closest('a');
  if (target && target.hostname !== window.location.hostname) {
    gtag('event', 'click', {
      'link_url': target.href,
      'link_text': target.innerText.trim().substring(0, 100),
      'link_type': 'outbound'
    });
  }
});
'''
```

## Dashboard Builder

```python
class DashboardBuilder:
    """Build analytics dashboards with key metrics."""
    
    METRIC_DEFINITIONS = {
        'users': 'Number of unique visitors',
        'sessions': 'Number of visits',
        'pageviews': 'Total pages viewed',
        'bounce_rate': '% of single-page sessions',
        'avg_session_duration': 'Average time per visit (seconds)',
        'pages_per_session': 'Average pages per visit',
        'conversion_rate': '% of sessions with goal completion',
        'goal_completions': 'Total completed goals',
        'revenue': 'Total attributed revenue',
    }
    
    @staticmethod
    def kpi_dashboard(metrics: List[str], period: str = '30d') -> Dict:
        """Define a KPI dashboard layout."""
        return {
            'title': f'Performance Dashboard ({period})',
            'period': period,
            'kpis': [
                {
                    'metric': m,
                    'definition': DashboardBuilder.METRIC_DEFINITIONS.get(m, m),
                    'visualization': 'number' if m in ('users', 'sessions', 'pageviews', 'goal_completions') else 'percentage',
                    'comparison': 'previous_period',
                }
                for m in metrics
            ],
            'charts': [
                {'type': 'line', 'title': 'Users Over Time', 'metric': 'users'},
                {'type': 'line', 'title': 'Conversion Rate Trend', 'metric': 'conversion_rate'},
                {'type': 'bar', 'title': 'Top Pages', 'metric': 'pageviews', 'dimension': 'page'},
                {'type': 'pie', 'title': 'Traffic Sources', 'metric': 'sessions', 'dimension': 'source'},
                {'type': 'bar', 'title': 'Device Breakdown', 'metric': 'sessions', 'dimension': 'device_category'},
            ],
            'segments': [
                {'name': 'All Traffic', 'filter': ''},
                {'name': 'Organic Search', 'filter': 'source == "organic"'},
                {'name': 'Direct', 'filter': 'source == "direct"'},
                {'name': 'Social', 'filter': 'source ~ "social"'},
                {'name': 'Email', 'filter': 'source == "email"'},
            ],
        }
    
    @staticmethod
    def executive_report(metrics: Dict) -> str:
        """Generate an executive summary from metrics."""
        report = "📊 Executive Dashboard Summary\n"
        report += "=" * 40 + "\n"
        
        report += f"\n👥 Users: {metrics.get('users', 'N/A')} "
        report += f"(+{metrics.get('users_growth', 'N/A')}% vs previous period)\n"
        
        report += f"\n📈 Traffic: {metrics.get('sessions', 'N/A')} sessions\n"
        report += f"   Pages/Session: {metrics.get('pages_per_session', 'N/A')}\n"
        report += f"   Avg Duration: {metrics.get('avg_session_duration', 'N/A')}s\n"
        report += f"   Bounce Rate: {metrics.get('bounce_rate', 'N/A')}%\n"
        
        report += f"\n🎯 Conversions: {metrics.get('goal_completions', 'N/A')}\n"
        report += f"   Conversion Rate: {metrics.get('conversion_rate', 'N/A')}%\n"
        
        report += f"\n💰 Revenue: ${metrics.get('revenue', 'N/A')}\n"
        report += f"   ROAS: {metrics.get('roas', 'N/A')}x\n"
        
        return report
```

## Conversion Tracking

```python
class ConversionTracking:
    """Set up conversion tracking and attribution."""
    
    @staticmethod
    def track_purchase(transaction_id: str, value: float, 
                       currency: str = 'USD', items: List[Dict] = None) -> str:
        """GA4 purchase event tracking."""
        items_json = json.dumps(items or [])
        return f'''
gtag('event', 'purchase', {{
  'transaction_id': '{transaction_id}',
  'value': {value},
  'currency': '{currency}',
  'items': {items_json}
}});
'''
    
    @staticmethod
    def generate_utm_builder() -> Dict:
        """UTM parameter builder for campaign tracking."""
        return {
            'utm_source': 'google, facebook, linkedin, twitter, newsletter',
            'utm_medium': 'cpc, social, email, banner, referral',
            'utm_campaign': 'campaign_name (e.g., spring_sale_2024)',
            'utm_term': 'paid_keyword (for PPC)',
            'utm_content': 'specific_ad_variant (for A/B testing)',
            'example': '?utm_source=google&utm_medium=cpc&utm_campaign=spring_sale&utm_term=shoes'
        }
    
    @staticmethod
    def validate_utm(url: str) -> List[str]:
        """Validate that UTM parameters are properly formatted."""
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        issues = []
        if 'utm_source' in params and not params['utm_source'][0]:
            issues.append("utm_source is empty")
        if 'utm_source' in params and params['utm_source'][0] == '':
            issues.append("utm_source is required")
        if 'utm_medium' in params and params['utm_medium'][0] == '':
            issues.append("utm_medium should not be empty")
        if 'utm_campaign' not in params:
            issues.append("Consider adding utm_campaign for better tracking")
        
        return issues
```

## Common Pitfalls

1. **Not tracking conversions** — traffic without conversion tracking is vanity; set up goals
2. **Data sampling** — GA4 samples data above certain thresholds; use 360 or BigQuery
3. **Over-tracking** — tracking every click creates noise; track what drives decisions
4. **No UTM parameters** — can't distinguish campaign performance; always use UTM
5. **Ignoring attribution** — last-click attribution overvalues bottom-of-funnel; consider data-driven
6. **Cookieless future** — third-party cookies are being deprecated; prepare with first-party data

## Verification Checklist

- [ ] GA4 or analytics tool installed on all pages
- [ ] Key events tracked (form submissions, purchases, signups)
- [ ] Goals/conversions configured in analytics
- [ ] UTM parameters used for all campaigns
- [ ] Dashboard built with key business metrics
- [ ] Data layer implemented for enhanced ecommerce (if applicable)
- [ ] Consent mode configured for GDPR compliance
- [ ] Regular audit: verify tracking is working (Real-Time report)
- [ ] Exclusion filters for internal traffic

## See Also

- seo-search-engine-optimization — tracking SEO performance
- conversion-rate-optimization — using analytics for CRO
- digital-marketing-strategy — data-driven marketing decisions
- cms-website-management — ensuring analytics on all pages
