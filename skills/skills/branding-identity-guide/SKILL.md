---
name: branding-identity-guide
description: "Use when developing brand identity and style guidelines."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [branding, identity, style-guide, visual-design, brand-strategy, logo]
    related_skills: [content-writing-seo-copy, digital-marketing-strategy, social-media-content-planning, marketing-funnel-design]
---

# Brand Identity and Style Guidelines

Developing and documenting brand identity — from brand strategy and visual identity through tone of voice, messaging frameworks, and comprehensive style guides.

## When to Use

- Building a brand from scratch for a new business
- Refreshing or rebranding an existing brand
- Creating brand guidelines for a team or agency
- Ensuring consistent brand expression across channels
- Defining brand values, personality, and positioning

## Brand Strategy

```python
from typing import Dict, List, Optional

class BrandStrategy:
    """Define core brand strategy elements."""
    
    @staticmethod
    def define_brand_pyramid(business: Dict) -> Dict:
        """Build the brand pyramid from foundation to expression."""
        return {
            'purpose': f"Why {business.get('name', 'we')} exists beyond profit",
            'vision': business.get('vision', 'The future we want to create'),
            'mission': business.get('mission', 'What we do every day'),
            'values': business.get('values', ['Value 1', 'Value 2']),
            'personality': BrandStrategy._personality_traits(business.get('industry', '')),
            'positioning': BrandStrategy._positioning_statement(business),
        }
    
    @staticmethod
    def _personality_traits(industry: str) -> List[str]:
        archetypes = {
            'technology': ['Innovative', 'Smart', 'Clean', 'Forward-thinking'],
            'healthcare': ['Caring', 'Trustworthy', 'Professional', 'Compassionate'],
            'finance': ['Reliable', 'Secure', 'Expert', 'Stable'],
            'ecommerce': ['Energetic', 'Approachable', 'Helpful', 'Trendy'],
            'education': ['Inspiring', 'Knowledgeable', 'Supportive', 'Clear'],
            'food': ['Warm', 'Authentic', 'Delicious', 'Welcoming'],
            'fashion': ['Creative', 'Bold', 'Elegant', 'Trendsetting'],
        }
        return archetypes.get(industry, ['Professional', 'Reliable', 'Trustworthy', 'Friendly'])
    
    @staticmethod
    def _positioning_statement(business: Dict) -> str:
        """Create a positioning statement."""
        return (
            f"For {business.get('target_audience', 'our audience')}, "
            f"{business.get('name', 'our brand')} is the "
            f"{business.get('category', 'solution')} that "
            f"{business.get('differentiator', 'solves your problem')}. "
            f"Unlike {business.get('competitors', 'competitors')}, "
            f"we {business.get('unique_value', 'provide unique value')}."
        )
```

## Visual Identity

```python
class VisualIdentity:
    """Define visual brand elements."""
    
    @staticmethod
    def define_color_palette(primary_hex: str, industry: str = None) -> Dict:
        """Build a complete color palette from a primary color."""
        # In practice: use color theory to generate harmonious palette
        suggested = {
            'technology': {'primary': '#2563EB', 'secondary': '#7C3AED', 'accent': '#06B6D4'},
            'healthcare': {'primary': '#0891B2', 'secondary': '#059669', 'accent': '#0284C7'},
            'finance': {'primary': '#1E3A5F', 'secondary': '#0F766E', 'accent': '#B45309'},
            'ecommerce': {'primary': '#E11D48', 'secondary': '#F59E0B', 'accent': '#10B981'},
            'food': {'primary': '#DC2626', 'secondary': '#EA580C', 'accent': '#65A30D'},
            'creative': {'primary': '#7C3AED', 'secondary': '#EC4899', 'accent': '#F59E0B'},
        }
        
        palette = suggested.get(industry, {
            'primary': primary_hex, 'secondary': '#6B7280', 'accent': '#3B82F6'
        })
        
        return {
            'primary': {'hex': palette['primary'], 'usage': 'Headlines, buttons, primary elements'},
            'secondary': {'hex': palette['secondary'], 'usage': 'Subheadlines, backgrounds'},
            'accent': {'hex': palette['accent'], 'usage': 'CTAs, highlights, emphasis'},
            'neutral': {'hex': '#6B7280', 'usage': 'Body text'},
            'background': {'hex': '#FFFFFF', 'usage': 'Page backgrounds'},
            'dark': {'hex': '#111827', 'usage': 'Dark mode backgrounds'},
        }
    
    @staticmethod
    def typography_guide(industry: str = None) -> Dict:
        """Recommend typefaces for brand."""
        suggestions = {
            'technology': {'heading': 'Inter', 'body': 'Inter', 'mono': 'JetBrains Mono'},
            'finance': {'heading': 'Playfair Display', 'body': 'Source Sans Pro', 'mono': 'IBM Plex Mono'},
            'creative': {'heading': 'Poppins', 'body': 'DM Sans', 'mono': 'Space Mono'},
            'editorial': {'heading': 'Merriweather', 'body': 'Source Serif Pro', 'mono': 'Fira Code'},
            'default': {'heading': 'Montserrat', 'body': 'Open Sans', 'mono': 'Fira Code'},
        }
        return suggestions.get(industry, suggestions['default'])
    
    @staticmethod
    def logo_usage_guidelines() -> List[str]:
        """Standard logo usage rules."""
        return [
            "Minimum clear space: height of the logo mark on all sides",
            "Minimum size: 24px digital, 0.5 inches print",
            "Never stretch, distort, rotate, or change logo colors",
            "Preferred placement: top-left or centered",
            "Don't place on busy backgrounds — use solid or gradient version",
            "Don't add effects (shadows, gradients, outlines)",
            "Use full-color logo on white/light backgrounds",
            "Use reversed (white) logo on dark backgrounds",
            "Never rearrange or modify logo elements",
        ]
```

## Tone of Voice

```python
class ToneOfVoice:
    """Define brand tone of voice and messaging guidelines."""
    
    DIMENSIONS = [
        ('formal', 'casual'),
        ('serious', 'humorous'),
        ('respectful', 'irreverent'),
        ('enthusiastic', 'matter-of-fact'),
        ('detailed', 'concise'),
    ]
    
    @staticmethod
    def define(dimension_scores: Dict[str, int]) -> Dict:
        """Define tone of voice on each dimension (1-5 scale)."""
        return {
            dimension: {
                'score': score,
                'leaning': f"More {pair[1] if score > 3 else pair[0]}"
                           f"{' (neutral)' if score == 3 else ''}",
                'guidelines': ToneOfVoice._guidelines(dimension, score),
            }
            for dimension, score in dimension_scores.items()
            for pair in ToneOfVoice.DIMENSIONS if pair[0] in dimension or pair[1] in dimension
        }
    
    @staticmethod
    def _guidelines(dimension: str, score: int) -> str:
        if score <= 2:
            return f"Lean {dimension.split('-')[0]}. Use traditional formats, avoid slang."
        elif score >= 4:
            return f"Lean {dimension.split('-')[1]}. Use conversational language, be approachable."
        return "Balanced approach. Adapt to context."
    
    @staticmethod
    def do_dont_examples(brand_name: str, industry: str) -> Dict:
        """Examples of brand-appropriate and inappropriate copy."""
        return {
            'do': [
                f"Hi there! {brand_name} is here to help you [benefit].",
                f"Ready to get started with {brand_name}? Let's go.",
                f"See why [number] customers trust {brand_name}.",
            ],
            'dont': [
                f"Buy now or miss out forever!!!",
                f"Click here to claim your FREE prize!!!",
                f"We're the best (trust us).",
            ],
        }
```

## Brand Guidelines Document

```python
class BrandGuidelines:
    """Assemble a complete brand guidelines document."""
    
    @staticmethod
    def generate(brand: Dict) -> str:
        """Generate a brand guidelines document."""
        name = brand.get('name', 'Brand')
        
        doc = f"""
# {name} Brand Guidelines v1.0

## 1. Brand Strategy
- **Purpose**: {brand.get('purpose', 'TBD')}
- **Vision**: {brand.get('vision', 'TBD')}
- **Mission**: {brand.get('mission', 'TBD')}
- **Values**: {', '.join(brand.get('values', []))}
- **Personality**: {', '.join(brand.get('personality', []))}

## 2. Positioning
{brand.get('positioning', 'TBD')}

## 3. Visual Identity

### Color Palette
- Primary: {brand.get('colors', {}).get('primary', {}).get('hex', 'TBD')}
- Secondary: {brand.get('colors', {}).get('secondary', {}).get('hex', 'TBD')}
- Accent: {brand.get('colors', {}).get('accent', {}).get('hex', 'TBD')}

### Typography
- Headings: {brand.get('typography', {}).get('heading', 'TBD')}
- Body: {brand.get('typography', {}).get('body', 'TBD')}

### Logo
See logo_usage_guidelines section.

## 4. Tone of Voice
{brand.get('tone_of_voice', 'TBD')}

## 5. Applications
- Website and digital
- Social media
- Print and collateral
- Advertising
- Packaging (if applicable)

## 6. Review
These guidelines should be reviewed annually.
"""
        return doc
```

## Common Pitfalls

1. **Inconsistent application** — brand guidelines that nobody follows; train the team and enforce
2. **Generic branding** — "innovative, reliable, customer-focused" describes every company
3. **Style guide without substance** — colors and fonts without strategy miss the point
4. **Every decision is subjective** — guidelines remove subjectivity; document the reasoning
5. **Not evolving** — brands must evolve; review guidelines annually
6. **Internal focus only** — brand is what customers experience; test externally

## Verification Checklist

- [ ] Brand purpose, vision, mission, and values defined
- [ ] Positioning statement created
- [ ] Color palette with hex codes and usage rules
- [ ] Typography selected (heading, body, accent)
- [ ] Logo usage guidelines documented
- [ ] Tone of voice defined along key dimensions
- [ ] Do/don't examples for copywriting
- [ ] Brand guidelines document compiled and shared
- [ ] Team trained on brand standards
- [ ] Annual review process established

## See Also

- content-writing-seo-copy — applying brand voice to content
- digital-marketing-strategy — brand positioning in strategy
- social-media-content-planning — expressing brand on social
- marketing-funnel-design — brand consistency across funnel
