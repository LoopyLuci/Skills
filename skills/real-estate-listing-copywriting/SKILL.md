---
name: real-estate-listing-copywriting
description: "MLS listing copy. AIDA, feature-to-benefit, A/B variants."
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [real-estate, copywriting, mls, listings, marketing]
    related_skills: [real-estate-social-media-content, real-estate-cma-generator]
---

# Real Estate Listing Copywriting

Write MLS-optimized property listings that convert. Use the AIDA framework, convert features into benefits, produce 3 A/B variants per listing, and optimize for all major platforms (MLS, Zillow, Redfin, Realtor.com, social media).

## When to Use

- Writing a new listing description for the MLS
- Refreshing a stale listing that's been on market 30+ days
- Creating versioned copy for different platforms (MLS vs. social)
- Coaching a client on how their listing will be marketed
- Building a listing copy template library for your team

## The AIDA Framework

Every listing should follow the **AIDA** structure:

| Stage | Purpose | Example Headline |
|---|---|---|
| **A**ttention | Hook in 3-8 words | "Rooftop Views + Chef's Kitchen" |
| **I**nterest | Build desire with benefits | "Wake up to sweeping skyline views from your private terrace" |
| **D**esire | Paint the lifestyle picture | "Imagine hosting dinner parties in this renovated open-concept space" |
| **A**ction | Clear next step | "Schedule your private showing today — this one won't last" |

## Workflow

### 1. Gather Property Details

Collect from the user or MLS:

```
Address:
Property Type: [Single Family / Condo / Townhouse / Multi-Family]
Bedrooms:
Bathrooms:
Square Footage:
Lot Size:
Year Built:
List Price:
HOA Dues:
Garage/Parking:
Key Features (list 5-10):
Recent Upgrades (list 3-5):
Unique Selling Points (3):
School District:
Neighborhood/Subdivision:
Nearby Amenities:
```

### 2. Feature → Benefit Translation

Convert every feature into a buyer benefit:

| Feature | → Benefit |
|---|---|
| "Quartz countertops" | "Elegant, low-maintenance quartz countertops — no sealing required" |
| "New HVAC (2023)" | "Year-round comfort with a brand-new HVAC system — lower utility bills" |
| "Walk-in closet" | "His-and-hers walk-in closets with custom organizers" |
| "Hardwood floors" | "Gleaming hardwood floors throughout — no carpet to clean" |
| "Open floor plan" | "Seamless flow from kitchen to living — perfect for entertaining" |
| "Smart home features" | "Control lighting, thermostat, and security from your phone" |
| "South-facing backyard" | "Sun-drenched south-facing yard — all-day natural light" |
| "Dual vanity" | "Morning-ready dual vanity — no more fighting for counter space" |
| "Updated kitchen" | "Turn-key chef's kitchen with stainless steel appliances" |
| "Pool" | "Resort-style pool — your weekend escape without leaving home" |
| "Mountain views" | "Breathtaking mountain panoramas from every window" |
| "Walking distance to transit" | "5-min walk to the metro — skip the traffic" |
| "Corner lot" | "Extra privacy and landscaping on a coveted corner lot" |
| "New roof" | "Peace of mind with a new roof and 30-year transferable warranty" |

### 3. Generate 3 A/B Variants

Create three distinct tones for A/B testing:

```python
def generate_listing_variants(property_info):
    """
    Generate 3 tone variants for a property listing.
    property_info: dict with beds, baths, sqft, price, features, etc.
    """
    addr = property_info.get('address', '')
    beds = property_info.get('beds', 3)
    baths = property_info.get('baths', 2)
    sqft = property_info.get('sqft', 1500)
    price = property_info.get('price', 500000)
    features = property_info.get('features', [])
    usp = property_info.get('usp', [])
    agent = property_info.get('agent_name', 'Your Agent')
    agency = property_info.get('agency', 'Realty Co.')
    phone = property_info.get('phone', '555-0100')

    variants = {}

    # Variant A: Luxury / aspirational
    headline_a = f"Sophisticated Living in the Heart of {property_info.get('neighborhood', 'Town')}"
    body_a = f"""
Price: ${price:,}

{headline_a}

Step into a world of refined elegance at {addr}. This {beds}-bedroom, {baths}-bathroom residence spans {sqft:,} sq ft of meticulously designed living space.

{usp[0] if len(usp) > 0 else 'Every detail has been thoughtfully curated to elevate your daily life.'}

FEATURES YOU'LL LOVE:
"""
    for f in features[:5]:
        body_a += f"\n• {f}"

    body_a += f"""

DON'T MISS THIS OPPORTUNITY

Schedule your private tour today. Homes of this caliber don't stay on the market long.

{agent} | {agency} | {phone}
"""
    variants['luxury'] = {'headline': headline_a, 'body': body_a.strip()}

    # Variant B: Warm / lifestyle
    headline_b = f"Welcome Home — {beds} Beds, {baths} Baths, Endless Charm"
    body_b = f"""
Price: ${price:,}

{headline_b}

{addr} isn't just a house — it's where memories are made. Picture yourself sipping morning coffee on the sunlit deck, hosting friends in the open-concept living room, and tucking the kids into cozy bedrooms upstairs.

This inviting {beds}-bed, {baths}-bath home offers {sqft:,} sq ft of comfortable living space, including:
"""
    for f in features[:5]:
        body_b += f"\n• {f}"
    body_b += f"""

Come see for yourself why {property_info.get('neighborhood', 'this neighborhood')} is one of the most sought-after communities in the area.

Schedule your showing today — your new home is waiting.

{agent} | {agency} | {phone}
"""
    variants['warm'] = {'headline': headline_b, 'body': body_b.strip()}

    # Variant C: Short / data-driven (Zillow-optimized)
    headline_c = f"{beds}BR/{baths}BA | {sqft:,} sq ft | ${price:,} | {property_info.get('neighborhood', 'Prime Location')}"
    body_c = f"""
{headline_c}

The Numbers:
• {beds} Bedrooms | {baths} Bathrooms | {sqft:,} Sq Ft
• Built: {property_info.get('year_built', 'N/A')} | Lot: {property_info.get('lot_size', 'N/A')}
• HOA: ${property_info.get('hoa', 'N/A')}/mo
• Price/Sq Ft: ${price // sqft:,}

Key Facts:
"""
    for f in features[:5]:
        body_c += f"\n• {f}"
    body_c += f"""
{usp[0] if len(usp) > 0 else ''}

Available for showings starting immediately. Ask about our preferred lender incentives.

{agent} | {agency} | {phone}
"""
    variants['data'] = {'headline': headline_c, 'body': body_c.strip()}

    return variants

# Example usage
property_info = {
    'address': '123 Main St, Austin, TX 78701',
    'beds': 4,
    'baths': 3,
    'sqft': 2400,
    'price': 675000,
    'year_built': 2019,
    'lot_size': '0.25 acres',
    'hoa': 150,
    'neighborhood': 'Zilker',
    'features': [
        'Chef's kitchen with quartz counters and Thermador appliances',
        'Engineered hardwood floors throughout main level',
        'Primary suite with spa-like ensuite and walk-in closet',
        'Covered patio with built-in grill — perfect for entertaining',
        'Smart home system: Nest thermostat, Ring doorbell, Lutron lighting',
        'EV charger in two-car garage',
        'Walking distance to Barton Springs, Zilker Park, and South Congress',
    ],
    'usp': [
        'Rarely available end-unit with extra windows and private yard',
        'Top-rated Austin ISD schools — Zilker Elementary',
        'Low-maintenance living with HOA-covered lawn care',
    ],
    'agent_name': 'Sarah Johnson',
    'agency': 'Austin Realty Collective',
    'phone': '512-555-0142',
}

variants = generate_listing_variants(property_info)
for tone, content in variants.items():
    print(f"\n{'='*70}")
    print(f"VARIANT: {tone.upper()}")
    print(f"{'='*70}")
    print(content['headline'])
    print(content['body'])
```

### 4. Platform-Specific Optimization

| Platform | Character Limit | Style | Key Rules |
|---|---|---|---|
| **MLS** | Usually unlimited, but first 250-500 chars shown | Professional, complete sentences | Include all room names, school district, property condition |
| **Zillow** | 500 chars for description | Benefit-forward, scannable | Lead with best feature, bullet points help |
| **Redfin** | 500 chars | Conversational, warm | Write like a local — mention nearby coffee shops, parks |
| **Realtor.com** | 500 chars | Balanced | Blend MLS professionalism with lifestyle language |
| **Instagram** | 2,200 chars caption | Emotional, visual-first | Start with the view/photo description, emojis OK |
| **Facebook** | 5,000 chars | Storytelling | Longer format, ask questions, encourage comments |
| **TikTok/Reels** | Caption: ~150 chars | Punchy, hashtag-heavy | Hook in first 3 words, 5-10 relevant hashtags |

### 5. SEO Keyword Strategy

Include these high-value keywords naturally in your copy:

- **Location**: neighborhood, zip code, school district, nearby landmarks
- **Property type**: single-family, condo, townhouse, loft, ranch, colonial
- **Lifestyle**: "starter home," "move-in ready," "turnkey," "income property"
- **Condition**: "newly renovated," "updated kitchen," "fresh paint"
- **Amenities**: "hardwood floors," "open floor plan," "granite counters"
- **Market cues**: "priced to sell," "rare opportunity," "motivated seller"

### 6. MLS Bullet Optimization

Keep MLS bullets punchy and benefit-driven:

```
❌ BAD: "New kitchen with quartz countertops"
✅ GOOD: "Gorgeous chef's kitchen w/ quartz counters & stainless appliances"

❌ BAD: "Large backyard"
✅ GOOD: "Expansive private backyard — perfect for summer BBQs and play"

❌ BAD: "Close to shopping"
✅ GOOD: "Walk to Trader Joe's, Starbucks, and the farmers market"

❌ BAD: "3 bedrooms"
✅ GOOD: "3 generously sized bedrooms with ceiling fans and walk-in closets"
```

### 7. Listing Refresh Strategy

For stale listings (30+ days on market):

1. **Change the headline** completely — new angle, new hook
2. **Update 3+ photos** — different angles, different lighting, different season
3. **Add a price improvement note** if applicable: "New Price! Originally $525k — now $499k"
4. **Emphasize different features** — if you led with kitchen, now lead with location
5. **Change the tone** — switch from luxury to warm, or from data to lifestyle
6. **Add a seller incentive**: "Closing cost credit offered," "Rate buydown available"

### 8. Listing Photo Caption Templates

**Living Room:** "Sun-drenched living room with 10-ft ceilings and gas fireplace — the heart of the home"

**Kitchen:** "Chef-worthy kitchen with waterfall island, Bosch appliances, and walk-in pantry"

**Primary Bedroom:** "Primary retreat with spa ensuite, dual vanities, and custom walk-in closet"

**Backyard:** "Resort-inspired backyard with saltwater pool, pergola, and outdoor kitchen"

**View:** "Unobstructed sunset views from the rooftop terrace — every evening is a show"

**Entryway:** "A grand welcome: marble foyer sets the tone for this meticulously maintained home"

## Common Pitfalls

- **Writing for agents, not buyers**: Avoid jargon like "3/2 SFD w/ 2CG" — write for humans, not the MLS grid.
- **Feature dumps with no benefits**: A list of features without "what this means for you" doesn't motivate a showing.
- **Hyperbole that triggers skepticism**: "Best house ever" and "one of a kind" are trust-killers. Be specific instead.
- **Ignoring the listing photos**: Copy that contradicts photos (mentions "city views" when no windows face the skyline) creates cognitive dissonance.
- **Overwriting the first 250 characters**: MLS and Zillow truncate. Put the strongest selling point in the first sentence.
- **Forgetting the call to action**: Every listing needs an explicit next step — "Schedule your showing" not "Contact us for more info."
- **Neglecting mobile formatting**: Buyers read on phones. Short paragraphs, bullet points, and frequent line breaks.
- **Missing key MLS compliance**: Every market has required disclaimers (brokerage name, fair housing, EHO). Check your local MLS rules.
- **Using stale templates**: Buyers have seen every real estate cliché. Fresh, authentic copy stands out.
- **Not localizing**: Generic copy that could describe any house in any city doesn't sell. Name the coffee shop, the park, the farmers market.

## Verification Checklist

- [ ] AIDA framework present (Attention hook in headline, Interest/Desire in body, Action in closing)
- [ ] Every feature translated to a buyer benefit (no naked feature lists)
- [ ] 3 A/B variants generated (luxury/aspirational, warm/lifestyle, data-driven)
- [ ] Strongest selling point in the first 250 characters
- [ ] Active voice throughout (not passive: "You'll love" not "It is loved by")
- [ ] MLS compliance checked (Fair Housing disclaimer, broker info, required disclosures)
- [ ] Mobile-friendly formatting (short paragraphs, bullets, line breaks)
- [ ] Platform-specific optimization applied (MLS vs Zillow vs social)
- [ ] SEO keywords included naturally (location, type, amenities)
- [ ] No hyperbole, clichés, or industry jargon for consumers
- [ ] Call to action is explicit and time-sensitive
- [ ] Photo captions written for each key space (living, kitchen, primary, outdoor)
- [ ] Spelling and grammar checked (use a tool — no exceptions)
- [ ] For stale listings: headline changed, photos updated, incentive added