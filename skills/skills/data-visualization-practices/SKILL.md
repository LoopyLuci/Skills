---
name: data-visualization-practices
description: "Use when implementing data visualization and dashboards."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [data-visualization, charts, D3, dashboards, BI, dashboard-design, storytelling]
    related_skills: [website-analytics-tracking, business-metrics-kpis, saas-metrics-reporting, marketing-analytics-dashboard]
---

# Data Visualization Practices

Implementing effective data visualization — from chart selection and dashboard design through D3/Plotly implementation, accessibility, and data storytelling.

## When to Use

- Building dashboards for business metrics
- Choosing the right chart type for your data
- Implementing custom visualizations with D3.js or Plotly
- Designing accessible and responsive visualizations
- Telling stories with data through visualization

## Chart Selection

```python
CHART_SELECTION = {
    'trend_over_time': 'Line chart with time on x-axis, metric on y-axis',
    'comparison': 'Bar chart (horizontal for many categories, vertical for few)',
    'composition': 'Stacked bar chart (static) or area chart (over time)',
    'distribution': 'Histogram (frequency) or box plot (quartiles, outliers)',
    'correlation': 'Scatter plot with optional trend line',
    'part_to_whole': 'Pie chart (≤5 categories) or treemap (many categories)',
    'geospatial': 'Choropleth map or bubble map on geographic data',
}

class DashboardBuilder:
    """Design dashboard layouts with effective chart usage."""
    def __init__(self, title: str, theme: str = 'light'):
        self.title = title
        self.charts = []
    
    def add_chart(self, chart_type: str, title: str, data, 
                  width: int = 1, height: int = 1):
        self.charts.append({
            'type': chart_type, 'title': title,
            'data': data, 'width': width, 'height': height
        })
    
    def layout(self) -> List[Dict]:
        """Arrange charts in a grid layout."""
        # Simple grid: width 1 = half row, width 2 = full row
        return sorted(self.charts, key=lambda c: c['width'], reverse=True)
```

## Common Pitfalls

1. **Chart junk** — 3D effects, excessive gradients, gridlines, and decorations obscure data
2. **Wrong chart type** — pie chart for 15 categories, bar chart for time series, etc.
3. **Misleading axis** — truncated y-axis exaggerates differences; always start at 0 for bar charts
4. **Color blindness ignored** — 8% of men are color-blind; use patterns + accessible palettes
5. **Dashboard without context** — a number without comparison (vs target, vs prior period) is meaningless
6. **Too much information** — one dashboard with 20 charts overwhelms; group by theme

## Verification Checklist

- [ ] Chart type matches data (trend, comparison, distribution, composition)
- [ ] Axes labeled and truthful (y-axis starts at 0 for bar charts)
- [ ] Color palette is accessible (color-blind friendly)
- [ ] Dashboard has clear hierarchy (most important metric first)
- [ ] Context provided (target, prior period, benchmark)
- [ ] Responsive design (works on mobile/different screen sizes)
- [ ] Interactivity (tooltips, filtering, drill-down)
- [ ] Performance optimized (data aggregation, lazy loading)
