---
name: customer-marketing-social-proof
description: "Use when building customer marketing and social proof."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [customer-marketing, social-proof, testimonials, case-studies, reviews, G2]
    related_skills: [customer-advocacy-program, product-marketing-strategy, content-marketing-workflow, influencer-affiliate-programs]
---

# Customer Marketing and Social Proof

Building customer marketing programs — from collecting testimonials and case studies through review generation, social proof placement, and ROI measurement.

## When to Use

- Collecting and promoting customer testimonials
- Building case studies with quantifiable results
- Generating reviews on G2, Capterra, Trustpilot
- Placing social proof on website and in sales

## Social Proof Types

```python
SOCIAL_PROOF_TYPES = {
    'testimonials': 'Short quotes from satisfied customers (text or video)',
    'case_studies': 'Deep dive with problem, solution, results (pages)',
    'reviews': 'G2, Capterra, Google Reviews — star ratings + text',
    'logos': 'Customer logo sliders on website (builds trust instantly)',
    'metrics': '"10K+ customers", "99.9% uptime", "4.8★ rating" — quantified',
    'social_mentions': 'Twitter, LinkedIn praise — embed on site',
}

class SocialProofManager:
    """Manage and deploy social proof assets."""
    def __init__(self):
        self.testimonials = []
        self.case_studies = []
        self.reviews = []
    
    def add_testimonial(self, quote: str, customer: str, title: str,
                         company: str, metric: str = ''):
        self.testimonials.append({
            'quote': quote, 'customer': customer, 'title': title,
            'company': company, 'metric': metric,
        })
    
    def rotation(self, page_context: str) -> List[Dict]:
        """Get relevant testimonials for a specific page."""
        return self.testimonials[:3]  # Simplified rotation
```

## Verification Checklist

- [ ] Testimonials collected from key customer segments
- [ ] Case studies with quantified results (X% improvement, $Y saved)
- [ ] Review generation campaign (G2, Capterra, Google)
- [ ] Social proof placed on homepage, pricing, and sales pages
- [ ] Customer logos visible on website
- [ ] Video testimonials (short, authentic, diverse customers)
- [ ] Social proof ROI measured (conversion lift from proof elements)
- [ ] Permission obtained for all customer quotes and logos
