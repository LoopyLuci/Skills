# SEO Tools: Meta Tags, Sitemap, Structured Data

## Pattern

A `SEOMetadata` dataclass for page-level SEO, plus generators for sitemap, robots.txt, and an analyzer for scoring.

## Architecture

```python
@dataclass
class SEOMetadata:
    title: str = ""
    description: str = ""
    keywords: list[str] = field(default_factory=list)
    og_title: str = ""
    og_description: str = ""
    og_image: str = ""
    og_type: str = "website"
    twitter_card: str = "summary_large_image"
    canonical_url: str = ""
    robots: str = "index, follow"
    structured_data: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[str]: ...
    def to_meta_tags(self) -> str: ...
    def to_structured_data(self) -> str: ...

class SitemapGenerator:
    def __init__(self, base_url: str = "https://example.com"): ...
    def add_url(self, path: str, lastmod: str = "", changefreq: str = "monthly", priority: float = 0.5): ...
    def generate(self) -> str: ...
    def save(self, path: Path): ...

class RobotsTxtGenerator:
    def add_rule(self, user_agent: str, allow: list[str] = None, disallow: list[str] = None): ...
    def add_sitemap(self, url: str): ...
    def generate(self) -> str: ...

class SEOAnalyzer:
    def analyze(self, html_content: str, metadata: SEOMetadata) -> dict[str, Any]:
        # Checks title length, description length, H1 count, image alt text, links
        # Returns {"score": int, "issues": [...], "recommendations": [...]}
```

## GUI Integration

```python
class SEODialog(QDialog):
    def __init__(self, project: Project, parent: Optional[QWidget] = None):
        self.analyzer = SEOAnalyzer()
        # ... score display, issues list, recommendations list

    def _run_analysis(self):
        exporter = HTMLExporter()
        html = exporter.generate(self.project)
        result = self.analyzer.analyze(html, SEOMetadata(title=self.project.name))
        self.score_label.setText(f"SEO Score: {result['score']}/100")
        # ... populate issues and recommendations

# In WebBuilderWindow.menu:
seo_action = QAction("SEO Analysis...", self)
seo_action.triggered.connect(self.open_seo_analysis)
```

## SEO Checks

| Check | Severity | Points |
|-------|----------|--------|
| Missing title | Critical | -20 |
| Title > 60 chars | Warning | -10 |
| Missing description | Warning | -10 |
| Description > 160 chars | Warning | -10 |
| Missing H1 | Critical | -20 |
| Multiple H1s | Warning | -10 |
| Images without alt | Warning | -10/image |
| No structured data | Info | -5 |
| No links | Info | -5 |

## Key Decisions

1. **Score-based** — 100 points, deduct for issues, clamp at 0
2. **Severity levels** — critical (-20), warning (-10), info (-5)
3. **Open Graph + Twitter** — Standard social media meta tags
4. **JSON-LD** — Structured data as dict, serialized to script tag
5. **Recommendations** — Static list of best practices
