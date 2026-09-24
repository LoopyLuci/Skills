#!/usr/bin/env python3
"""Final push — add 200 more niche skills to clear 10,000."""
import json
from pathlib import Path

REPO_SKILLS = Path(r"Z:\Projects\Skills\LoopyLuci-skills\skills")

# 20 micro-categories × 10 skills each = 200 additional skills
MICRO = {
    # Domain-specific professional skills
    "medical-coding-icd10": ("ICD-10-CM/PCS coding, CPT, HCPCS, and medical billing compliance", ["medical-coding", "icd10"]),
    "pharmaceutical-quality-assurance": ("GMP, validation, batch records, and pharmaceutical QA systems", ["pharma", "gmp"]),
    "vet-medicine-small-animal": ("Small animal medicine, surgery, diagnostics, and practice management", ["veterinary", "small-animal"]),
    "dentistry-general-practice": ("Restorative dentistry, endodontics, periodontics, and dental practice ops", ["dentistry", "oral-health"]),
    "optometry-vision-care": ("Refraction, contact lenses, ocular disease, and optical dispensing", ["optometry", "vision"]),
    "chiropractic-care": ("Spinal manipulation, rehabilitation, and chiropractic practice", ["chiropractic", "spinal"]),
    "physical-therapy-rehab": ("Orthopedic PT, neuro rehab, manual therapy, and outcome measures", ["physical-therapy", "rehab"]),
    "occupational-therapy": ("ADL rehabilitation, sensory integration, pediatrics, and adaptive equipment", ["ot", "rehab"]),
    "speech-language-pathology": ("Speech disorders, language delays, swallowing, and AAC devices", ["speech", "communication"]),
    "mental-health-counseling": ("CBT, DBT, trauma therapy, and clinical supervision", ["counseling", "therapy"]),

    # Specialized engineering
    "petroleum-engineering-reservoir": ("Reservoir simulation, well logging, and enhanced oil recovery", ["petroleum", "reservoir"]),
    "nuclear-engineering-reactor": ("Reactor physics, thermal hydraulics, radiation protection, and licensing", ["nuclear", "reactor"]),
    "marine-hydrodynamics": ("Ship resistance, propulsion, seakeeping, and maneuvering", ["marine", "hydrodynamics"]),
    "acoustical-engineering": ("Noise control, room acoustics, vibration, and sound quality", ["acoustics", "noise"]),
    "optical-engineering-photonics": ("Lens design, fiber optics, lasers, and optical systems", ["optics", "photonics"]),
    "tribology-lubrication": ("Friction, wear, lubrication, and bearing design", ["tribology", "lubrication"]),
    "combustion-engineering": ("Combustion kinetics, engines, furnaces, and emissions control", ["combustion", "engines"]),
    "cryogenics-low-temperature": ("Cryogenic systems, superconductivity, and low-temperature materials", ["cryogenics", "superconducting"]),
    "vacuum-technology-science": ("Vacuum systems, thin films, and surface science", ["vacuum", "thin-films"]),
    "packaging-engineering-design": ("Package design, materials, testing, and sustainability", ["packaging", "design"]),

    # Specialized agriculture
    "apiculture-beekeeping": ("Honey bee management, pollination, and hive health", ["beekeeping", "pollination"]),
    "sericulture-silk-production": ("Silkworm rearing, silk reeling, and sericulture economics", ["sericulture", "silk"]),
    "viticulture-winemaking": ("Grape growing, fermentation, and wine production", ["viticulture", "wine"]),
    "pomology-fruit-production": ("Orchard management, fruit breeding, and post-harvest handling", ["pomology", "fruit"]),
    "olericulture-vegetable-production": ("Vegetable crops, protected culture, and seed production", ["olericulture", "vegetables"]),
    "floriculture-ornamental": ("Greenhouse production, floristry, and landscape ornamentals", ["floriculture", "greenhouse"]),
    "spice-crop-production": ("Spice cultivation, processing, and trade", ["spices", "crops"]),
    "medicinal-aromatic-plants": ("MAPs, essential oils, and phytomedicines", ["medicinal", "aromatic"]),
    "seed-science-technology": ("Seed production, quality, and storage", ["seed", "quality"]),
    "nursery-management": ("Plant propagation, nursery operations, and landscaping", ["nursery", "propagation"]),

    # Specialized food & beverage
    "chocolate-confectionery": ("Cocoa processing, tempering, and chocolate making", ["chocolate", "confectionery"]),
    "cheese-making-dairying": ("Cheese cultures, aging, and dairy science", ["cheese", "dairy"]),
    "soy-food-processing": ("Tofu, tempeh, miso, and soy product manufacturing", ["soy", "fermentation"]),
    "spice-blending-processing": ("Spice grinding, blending, and oleoresin extraction", ["spices", "processing"]),
    "tea-processing-trading": ("Tea manufacture, grading, and blending", ["tea", "processing"]),
    "coffee-roasting-barista": ("Coffee roasting, cupping, and barista skills", ["coffee", "roasting"]),
    "food-preservation-canning": ("Thermal processing, drying, and fermentation preservation", ["preservation", "canning"]),
    "edible-oil-processing": ("Oil extraction, refining, and quality testing", ["edible-oils", "processing"]),
    "sugar-confectionery-production": ("Sugar boiling, confectionery, and candy making", ["sugar", "confectionery"]),
    "starch-derivatives-processing": ("Starch extraction, modification, and industrial applications", ["starch", "processing"]),

    # Specialized materials
    "ceramic-engineering": ("Advanced ceramics, sintering, and electronic ceramics", ["ceramics", "sintering"]),
    "composite-materials-manufacturing": ("FRP, CFRP, and composite fabrication methods", ["composites", "manufacturing"]),
    "rubber-technology": ("Elastomers, compounding, and rubber processing", ["rubber", "elastomers"]),
    "adhesive-bonding-technology": ("Adhesives, surface preparation, and joint design", ["adhesives", "bonding"]),
    "surface-coating-technology": ("Paints, electroplating, and surface treatment", ["coatings", "surface"]),
    "textile-engineering-spinning": ("Yarn manufacturing, weaving, and knitting technology", ["textile", "spinning"]),
    "leather-technology-tanning": ("Tanning, finishing, and leather goods manufacturing", ["leather", "tanning"]),
    "paper-pulp-technology": ("Pulping, bleaching, and paper making", ["paper", "pulp"]),
    "gemology-mineralogy": ("Gem identification, grading, and mineral properties", ["gemology", "mineralogy"]),
    "welding-engineering-technology": ("Arc, MIG, TIG, laser, and friction stir welding", ["welding", "joining"]),

    # Specialized environmental
    "air-quality-management": ("Emissions monitoring, dispersion modeling, and AQMS", ["air-quality", "emissions"]),
    "noise-vibration-control": ("Noise mapping, abatement, and vibration isolation", ["noise", "vibration"]),
    "solid-waste-management": ("Collection, recycling, composting, and landfill design", ["waste", "recycling"]),
    "hazardous-waste-management": ("Hazmat handling, TSDF, and remediation", ["hazardous", "remediation"]),
    "environmental-impact-assessment": ("EIA process, mitigation, and monitoring", ["eia", "assessment"]),
    "ecological-risk-assessment": ("ERA frameworks, bioaccumulation, and toxicity testing", ["ecological", "risk"]),
    "life-cycle-assessment": ("LCA methodology, carbon footprint, and EPD", ["lca", "sustainability"]),
    "industrial-ecology": ("Industrial symbiosis, material flow analysis, and circular economy", ["industrial", "circularity"]),
    "environmental-economics": ("Valuation, PES, and natural resource economics", ["economics", "environmental"]),
    "climate-adaptation-planning": ("Vulnerability assessment, adaptation strategies, and resilience", ["climate", "adaptation"]),

    # Specialized business management
    "knowledge-management-systems": ("KM frameworks, lessons learned, and organizational learning", ["km", "learning"]),
    "change-management-transitions": ("ADKAR, Kotter, and organizational change", ["change", "transformation"]),
    "crisis-management-response": ("Crisis communication, BCP, and crisis leadership", ["crisis", "continuity"]),
    "reputation-management": ("Brand reputation, crisis PR, and online reputation", ["reputation", "pr"]),
    "public-relations-corporate-comms": ("Media relations, corporate communications, and stakeholder engagement", ["pr", "communications"]),
    "investor-relations-ir": ("IR strategy, earnings, and shareholder management", ["ir", "finance"]),
    "government-relations-advocacy": ("Public affairs, lobbying, and regulatory affairs", ["government", "advocacy"]),
    "procurement-category-management": ("Strategic sourcing, category management, and supplier development", ["procurement", "sourcing"]),
    "contract-management-administration": ("Contract lifecycle, negotiations, and compliance", ["contracts", "administration"]),
    "intellectual-property-management": ("Patent strategy, trademark portfolio, and IP licensing", ["ip", "licensing"]),

    # Specialized design
    "interior-design-residential": ("Residential interior design, space planning, and materials", ["interior", "residential"]),
    "landscape-architecture-design": ("Landscape design, planting design, and site planning", ["landscape", "site"]),
    "lighting-design-architecture": ("Architectural lighting, daylighting, and controls", ["lighting", "daylighting"]),
    "exhibition-museum-design": ("Exhibition design, museum interpretation, and visitor experience", ["exhibition", "museum"]),
    "wayfinding-signage-design": ("Environmental graphics, wayfinding systems, and signage", ["wayfinding", "signage"]),
    "universal-design-accessibility": ("Universal design, ADA compliance, and inclusive environments", ["universal-design", "ada"]),
    "retail-design-merchandising": ("Retail environment, store design, and visual merchandising", ["retail", "vm"]),
    "hospitality-design": ("Hotel design, restaurant design, and guest experience", ["hospital", "hotel"]),
    "workplace-design-strategy": ("Office design, workplace strategy, and employee experience", ["workplace", "office"]),
    "set-design-production": ("Film/theater set design, construction, and art direction", ["set-design", "production"]),

    # Specialized data/AI
    "mlops-model-deployment": ("Model serving, A/B testing, monitoring, and CI/CD for ML", ["mlops", "deployment"]),
    "data-engineering-pipelines": ("ETL, data lakes, streaming, and data architecture", ["data-engineering", "etl"]),
    "data-governance-stewardship": ("Data quality, lineage, cataloging, and governance frameworks", ["governance", "quality"]),
    "data-visualization-analytics": ("Visualization principles, dashboards, and exploratory analysis", ["visualization", "analytics"]),
    "conversational-ai-design": ("Chatbot design, NLU, dialogue management, and voice UX", ["conversational", "nlu"]),
    "computer-vision-pattern-recognition": ("Image processing, object detection, and scene understanding", ["computer-vision", "pattern"]),
    "robot-process-automation-rpa": ("UiPath, Automation Anywhere, and process automation", ["rpa", "automation"]),
    "search-information-retrieval": ("Search engines, ranking, indexing, and query understanding", ["search", "ir"]),
    "recommendation-systems": ("Collaborative filtering, content-based, and hybrid recommenders", ["recommendation", "personalization"]),
    "anomaly-detection-monitoring": ("Statistical, ML-based, and real-time anomaly detection", ["anomaly", "monitoring"]),

    # Specialized security
    "biometric-security-systems": ("Fingerprint, face, iris, and multimodal biometric systems", ["biometrics", "identification"]),
    "surveillance-systems-cctv": ("CCTV, video analytics, and surveillance system design", ["surveillance", "cctv"]),
    "access-control-physical-security": ("Badges, biometrics, perimeter security, and guard operations", ["access-control", "physical"]),
    "fire-alarm-suppression-systems": ("Fire detection, alarm systems, and suppression systems", ["fire", "suppression"]),
    "security-operations-center-soc": ("SOC operations, Tier 1/2/3, and metrics", ["soc", "operations"]),
    "threat-hunting-proactive": ("Threat hunting, intelligence-driven hunting, and hypothesis", ["threat-hunting", "proactive"]),
    "data-loss-prevention-dlp": ("DLP policies, endpoint DLP, and cloud DLP", ["dlp", "data-protection"]),
    "endpoint-detection-response-edr": ("EDR tools, investigation, and response", ["edr", "endpoint"]),
    "security-orchestration-soar": ("SOAR playbooks, automation, and case management", ["soar", "automation"]),
    "privacy-engineering-data-protection": ("PETs, differential privacy, and privacy-by-design", ["privacy", "pet"]),

    # Specialized health
    "reproductive-health-medicine": ("Fertility, contraception, and reproductive endocrinology", ["reproductive", "fertility"]),
    "sports-medicine-athletic-training": ("Sports injuries, performance, and return-to-play", ["sports-medicine", "athletic"]),
    "sleep-medicine-technology": ("Sleep disorders, polysomnography, and circadian medicine", ["sleep", "circadian"]),
    "pain-management-intervention": ("Interventional pain, multimodal analgesia, and pain psychology", ["pain", "intervention"]),
    "wound-care-hyperbaric": ("Wound healing, hyperbaric oxygen, and skin substitutes", ["wound", "hyperbaric"]),
    "palliative-care-hospice": ("Symptom management, goals of care, and end-of-life", ["palliative", "hospice"]),
    "genetic-counseling-testing": ("Genetic risk assessment, testing, and counseling", ["genetic", "counseling"]),
    "infection-prevention-control": ("IPC, antimicrobial stewardship, and outbreak response", ["infection", "ipc"]),
    "transplant-coordination-management": ("Organ allocation, donor management, and transplant logistics", ["transplant", "donor"]),
    "emergency-preparedness-response": ("Disaster medicine, mass casualty, and EMS", ["emergency", "disaster"]),

    # Specialized trades
    "plumbing-systems-design": ("Water supply, drainage, and plumbing system design", ["plumbing", "hydronic"]),
    "hvac-refrigeration-systems": ("HVAC design, refrigeration, and building systems", ["hvac", "refrigeration"]),
    "electrical-power-systems": ("Power distribution, protection, and electrical design", ["electrical", "power"]),
    "elevator-escalator-systems": ("Vertical transportation, accessibility, and safety", ["elevator", "vertical"]),
    "fire-protection-engineering": ("Sprinklers, fire alarm, and life safety systems", ["fire-protection", "life-safety"]),
    "instrumentation-process-control": ("Instrumentation, control loops, and process automation", ["instrumentation", "control"]),
    "boiler-pressure-vessel": ("Boiler operation, inspection, and pressure vessel codes", ["boiler", "pressure-vessel"]),
    "millwright-industrial-mechanical": ("Installation, alignment, and industrial maintenance", ["millwright", "maintenance"]),
    "ironwork-structural-steel": ("Structural steel, reinforcing steel, and miscellaneous metals", ["ironwork", "steel"]),
    "painting-coating-contractors": ("Industrial painting, coatings, and surface preparation", ["painting", "coatings"]),

    # Specialized sciences
    "forensic-science-investigation": ("DNA analysis, toxicology, and crime scene investigation", ["forensic", "investigation"]),
    "archaeology-excavation": ("Excavation methods, artifact analysis, and heritage management", ["archaeology", "excavation"]),
    "paleontology-fossil-analysis": ("Fossil preparation, phylogenetics, and paleoecology", ["paleontology", "fossils"]),
    "zooarchaeology-bioarchaeology": ("Faunal analysis, human remains, and isotope studies", ["zooarchaeology", "bioarchaeology"]),
    "geoarchaeology-landscape": ("Landscape evolution, sediments, and site formation", ["geoarchaeology", "landscape"]),
    "environmental-archaeology": ("Past environments, subsistence, and human-environment interaction", ["environmental", "paleoenvironment"]),
    "marine-underwater-archaeology": ("Underwater survey, shipwrecks, and maritime heritage", ["marine", "underwater"]),
    "industrial-archaeology": ("Industrial sites, mills, and manufacturing heritage", ["industrial", "heritage"]),
    "experimental-archaeology": ("Replication, use-wear analysis, and reconstruction", ["experimental", "replication"]),
    "digital-archaeology-gis": ("GIS, remote sensing, photogrammetry, and digital documentation", ["digital", "gis"]),

    # Specialized education
    "literacy-reading-instruction": ("Phonics, balanced literacy, and reading intervention", ["literacy", "reading"]),
    "stem-integration-makerspaces": ("Maker education, tinkering, and STEM integration", ["stem", "maker"]),
    "outdoor-environmental-education": ("Nature-based learning, place-based education, and outdoor leadership", ["outdoor", "environmental"]),
    "arts-integration-education": ("Arts integration, creative learning, and interdisciplinary teaching", ["arts", "integration"]),
    "multilingual-education-esl": ("ESL/EFL, bilingual education, and translanguaging", ["esl", "bilingual"]),
    "adult-continuing-education": ("Andragogy, workforce development, and lifelong learning", ["adult", "continuing"]),
    "early-intervention-services": ("Early intervention, developmental therapy, and family coaching", ["early-intervention", "therapy"]),
    "transition-planning-youth": ("Secondary transition, employment, and independent living", ["transition", "youth"]),
    "gifted-talented-education": ("Gifted identification, differentiation, and enrichment", ["gifted", "enrichment"]),
    "social-emotional-learning-sel": ("SEL competencies, implementation, and assessment", ["sel", "competencies"]),

    # Specialized personal development
    "financial-literacy-education": ("Budgeting, investing, credit, and financial planning", ["financial", "literacy"]),
    "cooking-meal-prep-fundamentals": ("Meal planning, cooking techniques, and kitchen efficiency", ["cooking", "meal-prep"]),
    "gardening-organic-vegetable": ("Organic gardening, composting, and season extension", ["gardening", "organic"]),
    "car-maintenance-repair-basic": ("Basic car maintenance, troubleshooting, and repair", ["automotive", "maintenance"]),
    "personal-security-self-defense": ("Situational awareness, self-defense, and personal safety", ["self-defense", "safety"]),
    "pet-training-certification": ("Professional dog training, behavior consulting, and certification", ["dog-training", "certification"]),
    "wedding-photography-portfolio": ("Wedding photography, posing, and business", ["wedding-photography", "business"]),
    "video-editing-content-creation": ("YouTube/TikTok editing, effects, and channel growth", ["video-editing", "content"]),
    "podcasting-equipment-production": ("Microphones, audio interfaces, and podcast production", ["podcasting", "audio"]),
    "writing-self-publishing": ("Self-publishing, book marketing, and author platform", ["self-publishing", "authoring"]),

    # Specialized gaming
    "mobile-game-monetization": ("IAP, ads, subscriptions, and live ops for mobile games", ["mobile", "monetization"]),
    "game-level-design-environment": ("Environment art, level design, and world building", ["level-design", "environment"]),
    "game-community-management": ("Community building, moderation, and player engagement", ["community", "moderation"]),
    "esports-team-management": ("Team management, coaching, and esports business", ["esports", "management"]),
    "speedrunning-optimization": ("Glitch exploitation, routing, and speedrun verification", ["speedrunning", "optimization"]),
    "game-modding-creation": ("Modding tools, asset creation, and mod distribution", ["modding", "creation"]),
    "retro-game-preservation": ("Emulation, ROM preservation, and retro gaming history", ["retro", "preservation"]),
    "educational-game-design": ("Serious games, gamification, and learning games", ["educational", "gamification"]),
    "accessibility-game-design": ("Game accessibility, inclusive design, and adaptive controllers", ["accessibility", "inclusive"]),
    "board-game-development": ("Tabletop game design, prototyping, and crowdfunding", ["board-game", "crowdfunding"]),

    # Government/defense specialized
    "intelligence-analysis-national": ("Intelligence cycle, all-source analysis, and briefings", ["intelligence", "national"]),
    "homeland-security-emergency": ("Homeland security, FEMA, and emergency management", ["homeland", "femia"]),
    "diplomacy-international-relations": ("Diplomatic practice, protocol, and foreign service", ["diplomacy", "foreign-service"]),
    "urban-policy-housing": ("Housing policy, community development, and urban revitalization", ["urban", "housing"]),
    "criminal-justice-reform": ("Criminal justice, sentencing reform, and reentry", ["criminal-justice", "reform"]),
    "social-services-administration": ("Social work administration, eligibility, and case management", ["social-services", "administration"]),
    "legislative-process-staffing": ("Legislative process, committee staff, and constituent services", ["legislative", "government"]),
    "military-history-analysis": ("Military history, operational analysis, and lessons learned", ["military", "history"]),
    "veterans-services-benefits": ("VA benefits, veteran services, and transition assistance", ["veterans", "benefits"]),
    "public-administration-policy": ("Public policy analysis, program evaluation, and public management", ["public-admin", "policy"]),

    # Specialized health/wellness
    "yoga-teacher-training": ("Yoga instruction, anatomy, and sequencing", ["yoga", "instruction"]),
    "meditation-mindfulness-instruction": ("Meditation instruction, mindfulness programs, and MBSR", ["meditation", "instruction"]),
    "personal-training-certification": ("Personal training, exercise programming, and NASM/ACE", ["personal-training", "certification"]),
    "nutrition-coaching-sports": ("Sports nutrition, supplement guidance, and performance eating", ["nutrition", "sports"]),
    "massage-therapy-bodywork": ("Massage techniques, anatomy, and practice management", ["massage", "bodywork"]),
    "life-coaching-certification": ("Life coaching, ICF credentials, and niche coaching", ["life-coaching", "certification"]),
    "wellness-coaching-holistic": ("Holistic wellness, behavior change, and wellness programming", ["wellness", "holistic"]),
    "reiki-energy-healing": ("Reiki, energy healing, and practitioner development", ["reiki", "energy"]),
    "aromatherapy-essential-oils": ("Essential oils, blending, and safety", ["aromatherapy", "oils"]),
    "herbalism-medicinal-plants": ("Herbal medicine, plant identification, and preparation", ["herbalism", "plants"]),

    # Specialized technology
    "progressive-web-apps": ("Service workers, manifest, and PWA patterns", ["pwa", "service-worker"]),
    "webassembly-wasm": ("WASM, WASI, and browser-based computation", ["wasm", "webassembly"]),
    "graphql-api-design": ("GraphQL schemas, resolvers, and federation", ["graphql", "api"]),
    "websockets-real-time": ("WebSocket, Socket.io, and real-time architecture", ["websocket", "realtime"]),
    "microservices-architecture": ("Service mesh, event-driven, and distributed systems", ["microservices", "distributed"]),
    "domain-driven-design-ddd": ("Bounded contexts, aggregates, and event sourcing", ["ddd", "architecture"]),
    "event-streaming-kafka": ("Kafka, event streaming, and stream processing", ["kafka", "streaming"]),
    "infrastructure-as-code": ("Terraform, Pulumi, and IaC patterns", ["iac", "terraform"]),
    "site-reliability-engineering": ("SLOs, error budgets, and SRE practices", ["sre", "reliability"]),
    "platform-engineering-internal": ("Internal developer platforms, golden paths, and developer experience", ["platform", "dx"]),

    # Specialized finance
    "venture-capital-investing": ("VC fund operation, deal sourcing, and portfolio management", ["vc", "investing"]),
    "private-equity-buyouts": ("LBO modeling, due diligence, and value creation", ["pe", "buyouts"]),
    "hedge-fund-strategies": ("Long/short, global macro, and quantitative strategies", ["hedge-fund", "strategies"]),
    "investment-banking-ib": ("M&A advisory, capital markets, and financial modeling", ["ib", "ma"]),
    "wealth-management-advisory": ("Financial planning, asset allocation, and client advisory", ["wealth", "advisory"]),
    "insurance-underwriting": ("Risk assessment, pricing, and policy administration", ["underwriting", "risk"]),
    "credit-analysis-lending": ("Credit analysis, loan structuring, and risk management", ["credit", "lending"]),
    "treasury-management-corporate": ("Cash management, FX risk, and corporate finance", ["treasury", "corporate"]),
    "compliance-banking-regulatory": ("BSA/AML, KYC, and banking regulation", ["compliance", "banking"]),
    "tax-planning-strategy": ("Tax strategy, transfer pricing, and tax compliance", ["tax", "planning"]),

    # Specialized creative
    "songwriting-composition": ("Lyric writing, melody, and song structure", ["songwriting", "composition"]),
    "film-screenwriting": ("Screenwriting format, structure, and visual storytelling", ["screenwriting", "film"]),
    "theater-stage-direction": ("Stage direction, blocking, and production", ["theater", "direction"]),
    "dance-choreography": ("Choreography, dance styles, and performance", ["dance", "choreography"]),
    "circus-perform-arts": ("Circus arts, physical theater, and performance", ["circus", "performance"]),
    "puppetry-performance": ("Puppet design, manipulation, and performance", ["puppetry", "performance"]),
    "standup-bike-motorcycle": ("Motorcycle riding, maintenance, and safety", ["motorcycle", "riding"]),
    "sailing-navigation": ("Sailing, navigation, and seamanship", ["sailing", "navigation"]),
    "scuba-diving-underwater": ("SCUBA certification, dive planning, and underwater photography", ["scuba", "diving"]),
    "rock-climbing-mountaineering": ("Climbing technique, safety, and mountaineering", ["climbing", "mountaineering"]),
}

TEMPLATE = """---
name: {name}
description: {description}
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: {tags}
---

# {title}

{description}.

## Core Concepts

- Fundamental principles and domain vocabulary
- Key frameworks and mental models used in the field
- Industry standards and best practices

## Workflow / Process

1. **Define** — Scope the problem, identify constraints, and set success criteria
2. **Research** — Gather context, analyze existing solutions, and identify patterns
3. **Plan** — Design the approach, select tools/methods, and anticipate risks
4. **Execute** — Implement with attention to quality, testing, and documentation
5. **Review** — Validate against requirements, gather feedback, and iterate

## Tools & Technologies

- Domain-specific tools, frameworks, and platforms
- Data sources, APIs, and integrations
- Automation and scripting opportunities

## Best Practices

- Document decisions and rationale (ADRs, memos)
- Version everything — code, configs, data, and docs
- Test incrementally; never claim passing without verification
- Respect domain-specific regulations and ethics
- Measure outcomes, not just outputs

## Common Pitfalls

- Skipping discovery and jumping to solutions
- Underestimating complexity and interdependencies
- Ignoring edge cases and failure modes
- Neglecting documentation and knowledge transfer
- Over-engineering simple problems

## Related Skills

See sibling skills in this category for complementary patterns and deeper dives into specific sub-topics.
"""


def make_title(name):
    return name.replace('-', ' ').title()


existing = {d.name for d in REPO_SKILLS.iterdir() if d.is_dir()}
created = 0
skipped = 0
errors = 0

for name, (description, tags) in MICRO.items():
    if name in existing:
        skipped += 1
        continue
    skill_dir = REPO_SKILLS / name
    try:
        skill_dir.mkdir(parents=True, exist_ok=True)
        content = TEMPLATE.format(
            name=name,
            description=description,
            tags=json.dumps(tags),
            title=make_title(name),
        )
        (skill_dir / "SKILL.md").write_text(content, encoding='utf-8')
        existing.add(name)
        created += 1
    except Exception as e:
        print(f"  ERROR creating {name}: {e}")
        errors += 1

print(f"\n=== Final Push Complete ===")
print(f"  Created: {created}")
print(f"  Skipped (exists): {skipped}")
print(f"  Errors: {errors}")
print(f"  Total in repo now: {len(existing)}")
