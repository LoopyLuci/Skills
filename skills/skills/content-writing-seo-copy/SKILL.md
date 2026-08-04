---
name: content-writing-seo-copy
description: "Use when writing SEO content and marketing copy."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [content-writing, copywriting, seo-copy, marketing, content-creation]
    related_skills: [blog-building-content-strategy, seo-search-engine-optimization, social-media-content-planning, digital-marketing-strategy]
---

# Content Writing and SEO Copywriting

Writing compelling content and marketing copy that ranks in search engines and converts readers — from headlines and body copy through CTAs, landing pages, and content structures.

## When to Use

- Writing blog posts, articles, and guides
- Crafting website copy (homepage, about, product pages)
- Creating marketing copy (emails, landing pages, ads)
- Optimizing existing content for better SEO and conversions
- Developing brand voice and content guidelines

## Copywriting Frameworks

```python
FRAMEWORKS = {
    'AIDA': {
        'name': 'Attention → Interest → Desire → Action',
        'use_for': 'Landing pages, ads, sales pages',
    },
    'PAS': {
        'name': 'Problem → Agitate → Solve',
        'use_for': 'Problem-focused content, product pages',
    },
    'BAB': {
        'name': 'Before → After → Bridge',
        'use_for': 'Case studies, transformations',
    },
    '4Cs': {
        'name': 'Clear → Concise → Compelling → Credible',
        'use_for': 'Website copy, about pages',
    },
    'FAB': {
        'name': 'Features → Advantages → Benefits',
        'use_for': 'Product descriptions, comparisons',
    },
}

class CopyFramework:
    """Apply copywriting frameworks."""
    
    @staticmethod
    def write_aida(headline: str, problem: str, solution: str, 
                   offer: str, cta: str) -> Dict:
        """AIDA framework: Attention → Interest → Desire → Action."""
        return {
            'framework': 'AIDA',
            'attention': f"**{headline}** — {problem[:80]}",
            'interest': f"**Here's how it works:** {solution[:200]}",
            'desire': f"**Imagine if you could:** {offer[:200]}",
            'action': f"**{cta}** — Limited time offer.",
            'full_copy': f"# {headline}\n\n{problem}\n\n{solution}\n\n{offer}\n\n**{cta}**"
        }
    
    @staticmethod
    def write_pas(problem: str, agitate: str, solution: str) -> Dict:
        """PAS framework: Problem → Agitate → Solve."""
        return {
            'framework': 'PAS',
            'problem': f"**Struggling with** {problem}? You're not alone.",
            'agitate': f"This isn't just inconvenient — {agitate}",
            'solution': f"**Here's the solution:** {solution}",
            'full_copy': f"# {problem}\n\n{agitate}\n\n{solution}"
        }
```

## Headline Generation

```python
class HeadlineGenerator:
    """Generate compelling headlines for content."""
    
    FORMULAS = [
        "How to [achieve_desire] in [time_period] (Without [pain_point])",
        "[Number] [topic] Strategies That Actually Work in [year]",
        "The Ultimate Guide to [topic]: Everything You Need to Know",
        "Why [common_belief] Is Wrong (And What Really Works)",
        "[Number] [topic] Mistakes That Are Killing Your [result]",
        "The [adjective] [noun] That Will Transform Your [area]",
        "[Number] Signs You Need [solution] (And What to Do About It)",
        "What Nobody Tells You About [topic]",
        "The [adjective] Guide to [topic] for [audience]",
        "[Number] [topic] Tips From [authority]",
    ]
    
    @staticmethod
    def generate_headlines(topic: str, audience: str, 
                           count: int = 5) -> List[Dict]:
        """Generate headline variations from formulas."""
        import random
        
        headlines = []
        formulas = random.sample(HeadlineGenerator.FORMULAS, min(count, len(HeadlineGenerator.FORMULAS)))
        
        fillers = {
            '[topic]': topic,
            '[audience]': audience,
            '[year]': '2024',
            '[adjective]': random.choice(['Complete', 'Essential', 'Definitive', 'Practical', 'Proven']),
            '[result]': 'Results',
            '[area]': 'Success',
            '[authority]': random.choice(['Experts', 'Top Performers', 'Industry Leaders']),
        }
        
        for formula in formulas:
            headline = formula
            for placeholder, value in fillers.items():
                headline = headline.replace(placeholder, value)
            # Keep remaining brackets as prompts
            if '[' in headline:
                headline += ' [Customize]'
            
            headlines.append({
                'headline': headline,
                'formula': formula,
                'length': len(headline),
                'type': 'how_to' if 'How to' in headline else 'list' if headline[0].isdigit() else 'other',
            })
        
        return headlines
    
    @staticmethod
    def score_headline(headline: str) -> Dict:
        """Score headline effectiveness."""
        score = 0
        tips = []
        
        # Length check (ideal: 30-60 chars for SEO, 6-12 words)
        words = headline.split()
        if 6 <= len(words) <= 12:
            score += 20
        else:
            tips.append(f"Optimal word count: 6-12 words (currently {len(words)})")
        
        if 30 <= len(headline) <= 60:
            score += 20
        elif len(headline) > 60:
            tips.append(f"Truncated in search results (>60 chars)")
        
        # Power words
        power_words = ['ultimate', 'essential', 'proven', 'complete', 'definitive', 
                      'guaranteed', 'secret', 'simple', 'effective', 'powerful']
        has_power = any(w in headline.lower() for w in power_words)
        if has_power: score += 10
        
        # Number
        has_number = any(w.isdigit() for w in words)
        if has_number: score += 15
        else: tips.append("Add a number for 36% more clicks")
        
        # Emotional trigger
        emotional = ['you', 'your', 'because', 'without', 'why', 'what']
        has_emotion = any(w in headline.lower() for w in emotional)
        if has_emotion: score += 15
        
        # Curiosity gap
        if 'that' in headline.lower() or 'why' in headline.lower():
            score += 10
        
        return {
            'headline': headline,
            'score': score,
            'rating': 'Excellent' if score >= 80 else 'Good' if score >= 60 else 'Needs work',
            'word_count': len(words),
            'char_count': len(headline),
            'tips': tips,
        }
```

## SEO Content Optimizer

```python
class SEOContentOptimizer:
    """Optimize content for search engines while maintaining readability."""
    
    @staticmethod
    def analyze_keyword_density(content: str, target_keyword: str) -> Dict:
        """Analyze and suggest keyword usage improvements."""
        import re
        
        content_lower = content.lower()
        keyword_lower = target_keyword.lower()
        words = len(re.findall(r'\w+', content))
        
        # Count exact and partial keyword matches
        exact_count = content_lower.count(keyword_lower)
        
        # Count LSI (latent semantic indexing) variations
        lsi_variations = [keyword_lower, keyword_lower + 's', 
                         keyword_lower.replace(' ', '-'),
                         keyword_lower.replace(' ', '')]
        
        total_keyword_uses = sum(content_lower.count(v) for v in lsi_variations)
        
        density = round(total_keyword_uses / max(words, 1) * 100, 2)
        ideal_density = (1.0, 2.5)  # Ideal range
        
        suggestions = []
        if density < ideal_density[0]:
            suggestions.append(f"Keyword density {density}% is too low. Target 1-2.5%")
        elif density > ideal_density[1]:
            suggestions.append(f"Keyword density {density}% may be keyword stuffing. Reduce usage.")
        
        # Check placement
        first_100_words = content_lower.split()[:100]
        if keyword_lower not in ' '.join(first_100_words):
            suggestions.append("Use keyword in the first 100 words")
        
        return {
            'keyword': target_keyword,
            'word_count': words,
            'exact_matches': exact_count,
            'total_uses': total_keyword_uses,
            'density_pct': density,
            'density_status': 'good' if ideal_density[0] <= density <= ideal_density[1] else 'adjust',
            'suggestions': suggestions,
        }
    
    @staticmethod
    def suggest_related_terms(seed_keyword: str) -> List[str]:
        """Suggest related terms to include for topical authority."""
        # In practice, use SEMRush/Ahrefs API or NLP similarity
        return [
            f"{seed_keyword} guide",
            f"{seed_keyword} best practices",
            f"{seed_keyword} examples",
            f"{seed_keyword} vs [competitor]",
            f"{seed_keyword} pricing",
            f"{seed_keyword} review",
            f"what is {seed_keyword}",
            f"how to use {seed_keyword}",
        ]
```

## Landing Page Copy

```python
class LandingPageCopy:
    """Write high-converting landing page copy."""
    
    @staticmethod
    def create(value_proposition: str, target_audience: str,
               key_benefits: List[str], social_proof: str,
               objection: str, cta: str) -> Dict:
        """Generate a complete landing page structure."""
        return {
            'hero_section': {
                'headline': f"{value_proposition[:60]}",
                'subheadline': f"Designed for {target_audience}",
                'cta_button': cta,
            },
            'problem_section': {
                'headline': "The Challenge",
                'body': f"Are you {target_audience} struggling with...",
            },
            'solution_section': {
                'headline': "Our Solution",
                'benefits': [f"✅ {b}" for b in key_benefits],
            },
            'social_proof': {
                'headline': "Trusted by [Number] [Audience]",
                'testimonial': f'"{social_proof[:200]}"',
            },
            'objection_handling': {
                'headline': "Common Concerns",
                'body': f"We understand you might think {objection}, but here's the truth...",
            },
            'cta_section': {
                'headline': "Ready to Get Started?",
                'cta': cta,
                'urgency': "Limited time offer — act now!",
            },
        }
```

## Common Pitfalls

1. **Writing for SEO first** — keywords matter, but readers need to enjoy the content first
2. **Weak headlines** — 80% of people read the headline, only 20% read the rest; invest in headlines
3. **No clear CTA** — readers don't know what to do next; always include a specific call-to-action
4. **Burying the lead** — putting the most important point at the end; lead with value
5. **Generic content** — "content for everyone" resonates with no one; write for a specific person
6. **No skimmable structure** — readers scan before they read; use headings, bullets, bold text

## Verification Checklist

- [ ] Headline scored ≥ 60 (power words, numbers, emotional triggers)
- [ ] Keyword density 1-2.5%, keyword in first 100 words
- [ ] H1 + H2 + H3 structure with keywords in headings
- [ ] Clear CTA in every piece of content
- [ ] Readability: short paragraphs, active voice, simple language
- [ ] Social proof or statistics included
- [ ] Related internal links to other content
- [ ] Meta title (<60 chars) and description (<160 chars)
- [ ] Alt text for all images

## See Also

- blog-building-content-strategy — content planning and editorial calendar
- seo-search-engine-optimization — technical and on-page SEO
- social-media-content-planning — repurposing content for social
- digital-marketing-strategy — content's role in the marketing mix
