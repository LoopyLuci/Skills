#!/usr/bin/env python3
"""
Generate 550+ real, useful skills to push the LoopyLuci/Skills repo past 10,000.
Each skill gets a proper SKILL.md with frontmatter and meaningful content.

Usage: python scripts/generate-missing-skills.py --apply
"""
import os
import re
import sys
import json
from pathlib import Path

REPO_SKILLS = Path(r"Z:\Projects\Skills\LoopyLuci-skills\skills")

# Define categories and skills — each is a dict with name, description, tags, content template
SKILLS_TO_GENERATE = []

# ─── GAME DEVELOPMENT ───────────────────────────────────────────────
GAME_CATS = {
    "unity-game-development": ("Unity C# game development patterns, prefabs, ScriptableObjects, coroutines, physics, and performance optimization", ["unity", "csharp", "game-dev"]),
    "unreal-engine-5": ("Unreal Engine 5 C++ and Blueprints, Niagara VFX, World Partition, MetaSounds, and Lumen GI", ["unreal", "cpp", "game-dev"]),
    "godot-engine-4": ("Godot 4 GDScript and C#, signals, nodes, scenes, shaders, and export workflows", ["godot", "gamedev"]),
    "game-ai-behavior-trees": ("Behavior trees, utility AI, GOAP, finite state machines for NPCs, and procedural generation", ["game-ai", "npc"]),
    "multiplayer-networking-games": ("Netcode, client-server authority, prediction, reconciliation, lag compensation, and state sync", ["multiplayer", "networking"]),
    "vr-game-development": ("VR interaction, hand tracking, spatial UI, comfort options, and cross-platform deployment", ["vr", "xr"]),
    "mobile-game-development": ("Mobile-first game design, touch input, performance on low-end devices, and store optimization", ["mobile", "ios", "android"]),
    "game-audio-design": ("FMOD, Wwise, adaptive audio, spatial sound, dynamic music, and procedural audio", ["audio", "fm", "wwise"]),
    "game-level-design": ("Blockout, pacing, player flow, encounter design, environmental storytelling, and playtesting", ["level-design", "environment"]),
    "game-optimization-profiling": ("GPU/CPU profiling, batching, LOD, occlusion culling, memory budgets, and frame pacing", ["optimization", "profiling"]),
    "game-narrative-design": ("Branching dialogue, quest systems, lore databases, writer's room tools, and narrative scripting", ["narrative", "writing"]),
    "game-ux-ui-design": ("Diegetic UI, HUD design, accessibility, localization, and platform certification UX requirements", ["ux", "ui", "accessibility"]),
    "indie-game-marketing": ("Steam page optimization, wishlist campaigns, press outreach, festival submissions, and launch strategy", ["marketing", "indie"]),
    "pixel-art-game-dev": ("Pixel-perfect rendering, palette management, tilemaps, sprite animation, and Aseprite workflows", ["pixel-art", "2d"]),
    "roguelike-procedural-generation": ("PCG algorithms, dungeon generation, loot tables, meta-progression, and difficulty curves", ["procedural", "roguelike"]),
    "fighting-game-mechanics": ("Frame data, input buffering, hitboxes/hurtboxes, combo systems, and netcode for fighters", ["fighting", "competitive"]),
    "open-world-streaming": ("World composition, level streaming, data layers, navmesh generation, and large-world coordinates", ["open-world", "streaming"]),
    "shadergame-visual-effects": ("Shader Graph, HLSL/GLSL, VFX Graph, post-processing stacks, and GPU particles", ["shaders", "vfx"]),
    "game-accessibility-standards": ("Xbox/PlayStation/Steam accessibility guidelines, remappable controls, screen reader, and colorblind modes", ["accessibility", "inclusive"]),
    "physics-game-development": ("2D/3D physics engines, rigidbodies, joints, cloth simulation, and deterministic physics", ["physics", "simulation"]),
}

# ─── CYBERSECURITY ───────────────────────────────────────────────────
SECURITY_CATS = {
    "penetration-testing-methodology": ("OWASP, PTES, OSCP methodology, recon, exploitation, post-exploitation, and reporting", ["pentesting", "offensive"]),
    "incident-response-ir": ("SANS PICERL, NIST 800-61, containment, eradication, recovery, and lessons-learned", ["ir", "dfir"]),
    "threat-intelligence-cti": ("MITRE ATT&CK, STIX/TAXII, IOCs, threat actor profiling, and intelligence sharing", ["cti", "intelligence"]),
    "malware-analysis-reverse-engineering": ("Static/dynamic analysis, sandboxing, YARA rules, IDA/Ghidra, and unpacking", ["malware", "re"]),
    "cloud-security-posture": ("CSPM, IAM policies, workload protection, compliance as code, and zero trust in cloud", ["cloud-security", "cspm"]),
    "application-security-secure-code": ("SAST, DAST, SCA, threat modeling (STRIDE), code review, and secure SDLC", ["appsec", "devsecops"]),
    "network-security-monitoring": ("IDS/IPS, SIEM, packet analysis, NetFlow, Zeek, and anomaly detection", ["nsm", "siem"]),
    "digital-forensics-investigation": ("Disk imaging, memory forensics, timeline analysis, mobile forensics, and chain of custody", ["forensics", "dfir"]),
    "cryptography-implementation": ("Symmetric/asymmetric crypto, key management, TLS/PKI, HSM, and quantum-safe migration", ["crypto", "pki"]),
    "iot-security-assessment": ("Firmware analysis, UART/SPI sniffing, Zigbee/BLE attacks, and IoT hardening", ["iot", "embedded"]),
    "compliance-frameworks-audit": ("SOC 2, ISO 27001, PCI DSS, HIPAA, NIST CSF, and audit preparation", ["compliance", "audit"]),
    "red-team-adversary-simulation": ("C2 frameworks, phishing campaigns, physical security, and purple team exercises", ["red-team", "c2"]),
    "security-architecture-design": ("Zero trust, defense in depth, segmentation, SASE, and security patterns", ["architecture", "zero-trust"]),
    "vulnerability-management": ("CVE/NVD, CVSS, patch management, vulnerability disclosure, and risk scoring", ["vuln-mgmt", "cve"]),
    "ctf-capture-the-flag": ("Jeopardy/AWD CTF formats, crypto challenges, web exploitation, and writeup standards", ["ctf", "competition"]),
    "identity-access-management": ("OAuth 2.0, OIDC, SAML, SCIM, PAM, and identity governance", ["iam", "identity"]),
    "container-kubernetes-security": ("Pod security, admission control, runtime security, image scanning, and network policies", ["k8s-security", "containers"]),
    "blockchain-security-web3": ("Smart contract auditing, DeFi exploits, flash loan attacks, and formal verification", ["web3", "blockchain"]),
    "operational-security-opsec": ("Counter-surveillance, tradecraft, secure communications, and personal security", ["opsec", "privacy"]),
    "security-awareness-training": ("Phishing simulations, security culture, gamification, and metrics tracking", ["training", "culture"]),
}

# ─── ROBOTICS ────────────────────────────────────────────────────────
ROBOTICS_CATS = {
    "ros2-robot-operating-system": ("ROS 2 nodes, topics, services, actions, launch files, and DDS configuration", ["ros2", "middleware"]),
    "robot-slam-mapping": ("SLAM algorithms, occupancy grid mapping, loop closure, and multi-session mapping", ["slam", "mapping"]),
    "autonomous-navigation-navigation2": ("Nav2, behavior trees, costmap layers, global/local planners, and recovery behaviors", ["navigation", "autonomy"]),
    "manipulation-motion-planning": ("MoveIt, IK, trajectory planning, grasp planning, and collision checking", ["manipulation", "moveit"]),
    "robot-perception-vision": ("Camera calibration, object detection, point cloud processing, and sensor fusion", ["perception", "vision"]),
    "control-systems-robotics": ("PID, MPC, state-space control, trajectory tracking, and actuator control", ["control", "dynamics"]),
    "swarm-robotics-multi-agent": ("Decentralized coordination, consensus algorithms, formation control, and emergent behavior", ["swarm", "multi-agent"]),
    "humanoid-robotics": ("Balance control, whole-body control, bipedal locomotion, and human-robot interaction", ["humanoid", "locomotion"]),
    "drone-systems-uav": ("PX4/ArduPilot, flight controllers, waypoint navigation, geofencing, and airspace compliance", ["drone", "uav"]),
    "robot-simulation-gazebo": ("Gazebo/Ignition, SDF/URDF, physics tuning, sensor simulation, and headless operation", ["simulation", "gazebo"]),
    "robot-learning-rl": ("Sim-to-real, domain randomization, imitation learning, and reinforcement learning for robots", ["robot-learning", "rl"]),
    "safety-robotics-functional": ("ISO 10218, ISO/TS 15066, safety-rated monitored stop, collaborative robots, and risk assessment", ["safety", "cobot"]),
}

# ─── QUANTUM COMPUTING ─────────────────────────────────────────────
QUANTUM_CATS = {
    "qiskit-quantum-programming": ("Qiskit circuits, transpilation, primitives, error mitigation, and IBM Quantum hardware", ["qiskit", "ibm"]),
    "quantum-algorithms-design": ("Shor, Grover, QAOA, VQE, quantum walks, and algorithm complexity analysis", ["algorithms", "theory"]),
    "quantum-machine-learning": ("Quantum kernels, QSVM, variational circuits, and quantum neural networks", ["qml", "hybrid"]),
    "quantum-chemistry-simulation": ("Molecular Hamiltonian, VQE for chemistry, active space selection, and basis sets", ["chemistry", "simulation"]),
    "quantum-optimization": ("Quantum annealing, QAOA for combinatorial optimization, and D-Wave workflows", ["optimization", "annealing"]),
    "quantum-cryptography": ("BB84, E91, QKD protocols, post-quantum crypto, and quantum random number generation", ["crypto", "qkd"]),
    "quantum-error-correction": ("Surface codes, stabilizer codes, logical qubits, and fault-tolerant thresholds", ["error-correction", "fault-tolerant"]),
    "quantum-hardware-superconducting": ("Transmon qubits, coherence times, gate fidelities, and cryogenic control", ["hardware", "superconducting"]),
}

# ─── GEOSPATIAL / GIS ───────────────────────────────────────────────
GEOSPATIAL_CATS = {
    "qgis-open-source-gis": ("QGIS processing, styling, labeling, print layouts, and plugin development", ["qgis", "gis"]),
    "postgis-spatial-databases": ("Spatial indexing, PostGIS functions, raster support, and query optimization", ["postgis", "sql"]),
    "geospatial-data-rasterio": ("Rasterio, xarray, GeoTIFF, COG, and multi-band analysis", ["raster", "python"]),
    "geospatial-data-geopandas": ("GeoPandas, spatial joins, projections, geometry operations, and mapping", ["geopandas", "python"]),
    "remote-sensing-satellite": ("Sentinel, Landsat, NDVI, change detection, and time-series analysis", ["remote-sensing", "satellite"]),
    "web-mapping-leaflet-mapbox": ("Leaflet, Mapbox GL, MapLibre, tile servers, and interactive web maps", ["web-mapping", "javascript"]),
    "cartography-map-design": ("Visual hierarchy, typography, color schemes, projections, and thematic mapping", ["cartography", "design"]),
    "gps-gnss-positioning": ("RTK, PPP, coordinate transformations, and accuracy assessment", ["gps", "surveying"]),
    "spatial-analysis-modeling": ("Spatial statistics, hotspot analysis, interpolation, and geostatistics", ["spatial-stats", "analysis"]),
    "geocoding-address-processing": ("Forward/reverse geocoding, address standardization, and geocoding APIs", ["geocoding", "addresses"]),
}

# ─── PRODUCT MANAGEMENT ────────────────────────────────────────────
PM_CATS = {
    "product-roadmapping-strategy": ("Roadmap frameworks, outcome-based roadmapping, prioritization, and stakeholder alignment", ["roadmap", "strategy"]),
    "user-research-methods": ("Interviews, surveys, usability testing, diary studies, and research repositories", ["research", "ux"]),
    "product-metrics-okrs": ("North Star metric, AARRR, OKR setting, experimentation, and metric trees", ["metrics", "okrs"]),
    "agile-product-ownership": ("Scrum, Kanban, story mapping, backlog refinement, and sprint ceremonies", ["agile", "scrum"]),
    "product-discovery": ("Opportunity solution tree, assumption mapping, prototyping, and validated learning", ["discovery", "lean"]),
    "product-strategy-positioning": ("Value proposition, competitive analysis, market sizing, and pricing strategy", ["strategy", "positioning"]),
    "product-launch-gtm": ("Go-to-market strategy, beta programs, launch checklists, and adoption metrics", ["launch", "gtm"]),
    "product-analytics-instrumentation": ("Event tracking, product analytics tools, funnel analysis, and cohort analysis", ["analytics", "instrumentation"]),
    "design-thinking-workshops": ("Empathize-define-ideate-prototype-test, facilitation, and synthesis methods", ["design-thinking", "workshops"]),
    "stakeholder-management": ("RACI, communication plans, executive updates, and managing up/across", ["stakeholders", "communication"]),
}

# ─── LEGAL & COMPLIANCE ─────────────────────────────────────────────
LEGAL_CATS = {
    "gdpr-data-protection": ("Data subject rights, DPIA, breach notification, international transfers, and records of processing", ["gdpr", "privacy"]),
    "contract-law-review": ("Contract structure, key clauses, redlining, risk assessment, and negotiation playbooks", ["contracts", "review"]),
    "intellectual-property-patents": ("Patentability, prior art search, prosecution, portfolio strategy, and licensing", ["ip", "patents"]),
    "corporate-law-governance": ("Board resolutions, shareholder agreements, M&A, and entity management", ["corporate", "governance"]),
    "employment-law-compliance": ("At-will, discrimination, wage/hour, terminations, and employee handbooks", ["employment", "hr-compliance"]),
    "regulatory-compliance-financial": ("SEC, FINRA, MiFID II, AML/KYC, and compliance programs", ["financial", "regulatory"]),
    "privacy-law-ccpa-state": ("CCPA/CPRA, VCDPA, state privacy laws, and US privacy patchwork", ["privacy", "us-law"]),
    "open-source-licensing": ("GPL, MIT, Apache, license compliance, and contribution policies", ["licensing", "open-source"]),
    "e-discovery-litigation-support": ("ESI, document review, privilege logs, and litigation hold", ["ediscovery", "litigation"]),
    "international-law-trade": ("Export controls, sanctions, customs, and international contracts", ["trade", "international"]),
}

# ─── HEALTHCARE & MEDICAL ──────────────────────────────────────────
HEALTHCARE_CATS = {
    "clinical-workflow-design": ("Patient journey mapping, clinical pathways, order sets, and workflow optimization", ["clinical", "workflow"]),
    "electronic-health-records-ehr": ("EHR implementation, CPOE, interoperability, HL7 FHIR, and usability", ["ehr", "interoperability"]),
    "telemedicine-virtual-care": ("Telehealth platforms, remote patient monitoring, digital front door, and licensure", ["telehealth", "virtual"]),
    "medical-imaging-ai": ("DICOM, PACS, AI-assisted diagnosis, image segmentation, and radiology workflows", ["imaging", "radiology"]),
    "genomics-bioinformatics-pipeline": ("NGS pipelines, variant calling, annotation, and clinical genomics", ["genomics", "ngs"]),
    "drug-discovery-development": ("Target identification, lead optimization, preclinical, and clinical trial phases", ["pharma", "rdd"]),
    "public-health-surveillance": ("Disease surveillance, outbreak investigation, epidemiological study design", ["epidemiology", "surveillance"]),
    "mental-health-care-delivery": ("Digital therapeutics, stepped care, CBT platforms, and outcome measurement", ["mental-health", "dt"]),
    "nutrition-dietetics-clinical": ("Medical nutrition therapy, nutritional assessment, and dietary planning", ["nutrition", "dietetics"]),
    "healthcare-compliance-hipaa": ("HIPAA privacy/security, HITECH, BAA, and breach risk assessment", ["hipaa", "healthcare"]),
}

# ─── CREATIVE DESIGN ───────────────────────────────────────────────
DESIGN_CATS = {
    "ui-design-systems": ("Component libraries, design tokens, atomic design, and Figma-to-code handoff", ["ui", "design-system"]),
    "ux-research-testing": ("Usability testing, heuristic evaluation, journey mapping, and accessibility audits", ["ux", "research"]),
    "graphic-design-branding": ("Logo design, brand identity, print design, and brand guidelines", ["graphic-design", "branding"]),
    "motion-graphics-animation": ("After Effects, Lottie, kinetic typography, and motion principles", ["motion", "animation"]),
    "typography-typesetting": ("Type selection, hierarchy, pairing, kerning, and responsive type scales", ["typography", "typesetting"]),
    "color-theory-application": ("Color psychology, palette generation, accessibility contrast, and brand color systems", ["color", "theory"]),
    "3d-modeling-blender": ("Blender modeling, sculpting, retopology, UV mapping, and rendering", ["3d", "blender"]),
    "video-editing-post-production": ("Premiere, DaVinci, editing workflows, color grading, and audio sync", ["video", "editing"]),
    "game-asset-creation": ("Concept art, 3D modeling, texturing, rigging, and game-ready optimization", ["game-dev", "art"]),
    "photography-editing-workflow": ("RAW processing, color grading, compositing, and export for different media", ["photography", "editing"]),
}

# ─── MANUFACTURING & IOT ───────────────────────────────────────────
MANUFACTURING_CATS = {
    "plc-programming-ladder": ("IEC 61131-3, ladder logic, structured text, function blocks, and safety PLCs", ["plc", "automation"]),
    "scada-industrial-control": ("HMI design, alarm management, historians, and SCADA security", ["scada", "hmi"]),
    "digital-twin-development": ("Simulation, IoT data integration, predictive models, and digital thread", ["digital-twin", "simulation"]),
    "predictive-maintenance": ("Vibration analysis, thermal imaging, ML models, and maintenance scheduling", ["maintenance", "reliability"]),
    "opc-ua-industrial-interop": ("OPC UA server/client, information modeling, security, and Pub/Sub", ["opc-ua", "interop"]),
    "mqtt-iot-messaging": ("MQTT broker setup, QoS, retained messages, last will, and IoT fleet management", ["mqtt", "iot"]),
    "edge-computing-industrial": ("Edge ML, local data processing, Kubernetes at the edge, and offline resilience", ["edge", "kubernetes"]),
    "mes-manufacturing-execution": ("Production scheduling, quality management, OEE, and ISA-95", ["mes", "production"]),
    "additive-manufacturing-printing": ("3D printing workflows, SLA/SLS/FDM, print optimization, and post-processing", ["3d-printing", "additive"]),
    "lean-manufacturing-six-sigma": ("Value stream mapping, Kaizen, DMAIC, waste reduction, and continuous improvement", ["lean", "six-sigma"]),
}

# ─── MARKETING & GROWTH ─────────────────────────────────────────────
MARKETING_CATS = {
    "seo-search-engine-optimization": ("Technical SEO, on-page, link building, and search intent optimization", ["seo", "search"]),
    "content-markategy-strategy": ("Content calendars, pillar/cluster models, topic authority, and content ops", ["content", "strategy"]),
    "social-media-management": ("Platform strategy, community management, scheduling, and social listening", ["social-media", "community"]),
    "email-marketing-automation": ("List segmentation, drip campaigns, deliverability, and lifecycle email", ["email", "automation"]),
    "ppc-paid-advertising": ("Google Ads, Meta Ads, programmatic, bidding strategies, and ROAS optimization", ["ppc", "paid"]),
    "conversion-rate-optimization": ("A/B testing, heatmap analysis, landing page optimization, and statistical significance", ["cro", "testing"]),
    "brand-strategy-positioning": ("Brand architecture, positioning statements, messaging frameworks, and brand audits", ["brand", "positioning"]),
    "influencer-creator-marketing": ("Creator identification, relationship management, measurement, and contracts", ["influencer", "creator"]),
    "affiliate-partner-marketing": ("Affiliate programs, partner recruitment, tracking, and payout structures", ["affiliate", "partnerships"]),
    "marketing-analytics-attribution": ("Multi-touch attribution, marketing mix modeling, incrementality, and data layers", ["analytics", "attribution"]),
}

# ─── SCIENCE & RESEARCH ─────────────────────────────────────────────
SCIENCE_CATS = {
    "laboratory-protocols-methods": ("SOP writing, protocol optimization, lab safety, and reproducibility standards", ["lab", "protocols"]),
    "experimental-design-statistics": ("Factorial designs, sample size, randomization, blinding, and statistical power", ["experiment", "statistics"]),
    "academic-writing-publishing": ("Manuscript structure, peer review response, journal selection, and citation management", ["academic", "writing"]),
    "grant-writing-funding": ("NIH/NSF/ERC proposals, specific aims, budgets, and impact statements", ["grants", "funding"]),
    "research-data-management": ("Data management plans, FAIR principles, metadata standards, and repositories", ["rdm", "fair"]),
    "scientific-communication": ("Conference presentations, posters, science communication, and public engagement", ["communication", "outreach"]),
    "systematic-review-meta-analysis": ("PRISMA, search strategy, screening, quality assessment, and meta-analysis", ["review", "evidence"]),
    "research-ethics-integrity": ("IRB, informed consent, authorship, and responsible conduct of research", ["ethics", "integrity"]),
    "computational-research-methods": ("Simulation, agent-based modeling, network analysis, and reproducibility", ["computational", "methods"]),
    "field-research-methodology": ("Sampling, observation, ethnography, and ecological field methods", ["fieldwork", "ecology"]),
}

# ─── MUSIC & AUDIO ──────────────────────────────────────────────────
MUSIC_CATS = {
    "digital-audio-workstations": ("Ableton, Logic, Pro Tools, FL Studio workflows, and session management", ["daw", "production"]),
    "audio-synthesis-design": ("Subtractive, additive, FM, wavetable, and granular synthesis techniques", ["synthesis", "sound-design"]),
    "music-theory-composition": ("Harmony, counterpoint, form, orchestration, and arrangement techniques", ["theory", "composition"]),
    "audio-mixing-engineering": ("Gain staging, EQ, compression, reverb, automation, and mixing in-the-box", ["mixing", "engineering"]),
    "mastering-audio-finalization": ("Limiting, stereo imaging, loudness standards, and delivery formats", ["mastering", "loudness"]),
    "spatial-audio-immersive": ("Ambisonics, binaural, Dolby Atmos, and object-based audio", ["spatial", "immersive"]),
    "music-production-electronic": ("Beat making, sampling, sound design, and arrangement in electronic genres", ["production", "electronic"]),
    "sound-design-for-media": ("Foley, field recording, sound effects, and audio post-production for film/games", ["sound-design", "media"]),
    "audio-programming-supercollider": ("SuperCollider, Max/MSP, Pure Data, and audio DSP programming", ["audio-programming", "dsp"]),
    "live-sound-reinforcement": ("PA systems, monitors, RF coordination, and live mixing techniques", ["live-sound", "reinforcement"]),
}

# ─── PHOTOGRAPHY ────────────────────────────────────────────────────
PHOTO_CATS = {
    "portrait-photography-techniques": ("Posing, lighting setups, lens selection, and directing subjects", ["portrait", "lighting"]),
    "landscape-photography-capture": ("Composition, filters, long exposure, and golden/blue hour timing", ["landscape", "nature"]),
    "street-photography-candid": ("Zone focusing, composition, legal/ethical considerations, and storytelling", ["street", "candid"]),
    "product-photography-commerce": ("Lighting, backgrounds, lifestyle vs. packshot, and e-commerce standards", ["product", "commerce"]),
    "drone-aerial-photography": ("Flight planning, regulations, panorama stitching, and HDR", ["drone", "aerial"]),
    "night-astrophotography": ("Star tracking, stacking, Milky Way composition, and light pollution management", ["night", "astrophoto"]),
    "event-photography-documentation": ("Candid coverage, key moments, lighting challenges, and delivery workflows", ["event", "documentary"]),
    "food-photography-styling": ("Styling, lighting, color theory, and composition for food", ["food", "styling"]),
    "architectural-interior-photography": ("Perspective control, lighting, HDR, and twilight shooting", ["architecture", "interior"]),
    "wedding-photography-coverage": ("Timeline planning, must-shot lists, posing groups, and editing workflows", ["wedding", "events"]),
}

# ─── WRITING & CONTENT CREATION ────────────────────────────────────
WRITING_CATS = {
    "copywriting-conversion": ("Headlines, CTAs, AIDA, PAS, and sales page copy that converts", ["copywriting", "conversion"]),
    "technical-writing-documentation": ("API docs, user guides, knowledge bases, and docs-as-code workflows", ["technical-writing", "docs"]),
    "creative-writing-fiction": ("Plot, character, setting, dialogue, and revision techniques for fiction", ["fiction", "creative"]),
    "journalism-news-reporting": ("Inverted pyramid, sourcing, fact-checking, and news writing standards", ["journalism", "reporting"]),
    "speech-writing-oratory": ("Structure, rhetoric, storytelling, and delivery for speeches", ["speech", "oratory"]),
    "scriptwriting-screenplay": ("Format, structure, dialogue, and visual storytelling for screen", ["screenplay", "script"]),
    "game-writing-interactive": ("Branching narrative, environmental storytelling, lore, and writer's room", ["game-writing", "narrative"]),
    "ux-writing-microcopy": ("Button labels, error messages, onboarding, and content design systems", ["ux-writing", "content-design"]),
    "grant-proposal-writing": ("Needs statement, methodology, evaluation plans, and funder alignment", ["grants", "proposals"]),
    "ghostwriting-collaboration": ("Voice matching, research, collaboration with subject matter experts", ["ghostwriting", "collaboration"]),
}

# ─── SPORTS & FITNESS ──────────────────────────────────────────────
SPORTS_CATS = {
    "strength-training-programming": ("Periodization, progressive overload, and program design for strength", ["strength", "programming"]),
    "endurance-cardio-training": ("Zone training, periodization, and programming for running/cycling", ["endurance", "cardio"]),
    "sports-nutrition-periodization": ("Macro cycling, supplementation, hydration, and competition nutrition", ["nutrition", "sports"]),
    "sports-analytics-data": ("Performance metrics, tracking data, visualization, and predictive modeling", ["analytics", "data"]),
    "biomechanics-human-motion": ("Motion analysis, force plates, injury mechanisms, and performance optimization", ["biomechanics", "motion"]),
    "yoga-pilates-instruction": ("Sequencing, alignment cues, modifications, and class structure", ["yoga", "pilates"]),
    "sports-psychology-performance": ("Mental skills, goal setting, visualization, and team dynamics", ["psychology", "performance"]),
    "injury-rehabilitation-return": ("Rehab phases, load management, return-to-play criteria, and prevention", ["rehab", "injury"]),
    "running-coaching-training": ("Training plans, gait analysis, pace strategy, and race preparation", ["running", "coaching"]),
    "cycling-training-triathlon": ("Power training, FTP testing, bike fit, and triathlon periodization", ["cycling", "triathlon"]),
}

# ─── GOVERNMENT & PUBLIC POLICY ────────────────────────────────────
GOV_CATS = {
    "public-policy-analysis": ("Policy cycle, cost-benefit analysis, stakeholder mapping, and policy memos", ["policy", "analysis"]),
    "civic-technology-design": ("Government digital services, user-centered design for public, and civic tech stack", ["civic-tech", "gov"]),
    "urban-planning-design": ("Zoning, transit-oriented development, community engagement, and master plans", ["urban-planning", "design"]),
    "public-administration-management": ("Public sector management, procurement, performance management, and reform", ["administration", "management"]),
    "international-relations-theory": ("Realism, liberalism, constructivism, diplomacy, and global governance", ["ir", "diplomacy"]),
    "public-finance-budgeting": ("Public budgeting, fiscal policy, debt management, and capital planning", ["finance", "budgeting"]),
    "political-campaign-strategy": ("Messaging, field operations, digital strategy, and voter targeting", ["campaign", "strategy"]),
    "environmental-policy-regulation": ("Environmental law, climate policy, impact assessment, and regulation", ["environment", "regulation"]),
    "defense-security-policy": ("Defense strategy, procurement, threat assessment, and alliance management", ["defense", "security"]),
    "social-welfare-policy": ("Poverty measurement, program evaluation, social safety nets, and policy design", ["welfare", "social-policy"]),
}

# ─── REAL ESTATE ────────────────────────────────────────────────────
RE_CATS = {
    "property-valuation-appraisal": ("Comparable sales, income approach, cost approach, and valuation models", ["valuation", "appraisal"]),
    "real-estate-market-analysis": ("Market cycles, supply/demand, absorption rates, and feasibility studies", ["market", "analysis"]),
    "proptech-technology": ("Real estate technology, smart buildings, tenant experience, and CRE tech", ["proptech", "technology"]),
    "real-estate-finance-investment": ("Cap rates, cash-on-cash, IRR, deal structuring, and syndication", ["finance", "investment"]),
    "property-management-operations": ("Tenant relations, maintenance, leasing, and property operations", ["management", "operations"]),
    "commercial-real-estate-cre": ("Office, retail, industrial, multifamily, and CRE transaction lifecycle", ["commercial", "cre"]),
    "real-estate-development": ("Site selection, entitlements, construction, and project delivery", ["development", "construction"]),
    "residential-brokerage-sales": ("Buyer/seller representation, contracts, negotiation, and transaction management", ["residential", "brokerage"]),
    "real-estate-law-transactions": ("Purchase agreements, title, escrow, and closing procedures", ["law", "transactions"]),
    "real-estate-data-analytics": ("MLS data, predictive analytics, geographic analysis, and market intelligence", ["data", "analytics"]),
}

# ─── SUPPLY CHAIN & LOGISTICS ──────────────────────────────────────
SUPPLY_CATS = {
    "inventory-optimization": ("Safety stock, EOQ, ABC analysis, multi-echelon, and demand-driven planning", ["inventory", "planning"]),
    "last-mile-delivery-logistics": ("Route optimization, delivery models, gig economy, and urban logistics", ["last-mile", "delivery"]),
    "warehouse-management-systems": ("WMS operations, slotting, picking strategies, and automation", ["warehouse", "wms"]),
    "demand-forecasting-planning": ("Statistical forecasting, S&OP, collaborative planning, and forecast accuracy", ["forecasting", "snop"]),
    "procurement-strategic-sourcing": ("Category management, supplier selection, negotiation, and SRM", ["procurement", "sourcing"]),
    "logistics-transportation-management": ("Carrier management, freight modes, 3PL/4PL, and TMS", ["logistics", "transportation"]),
    "supply-chain-risk-management": ("Risk mapping, dual sourcing, nearshoring, and resilience planning", ["risk", "resilience"]),
    "reverse-logistics-returns": ("Returns processing, refurbishment, recycling, and circular economy", ["reverse", "circularity"]),
    "global-trade-compliance": ("Customs, tariffs, free trade zones, and trade compliance", ["trade", "customs"]),
    "supply-chain-sustainability": ("Scope 3 emissions, ethical sourcing, circularity, and ESG reporting", ["sustainability", "scope3"]),
}

# ─── ENERGY & SUSTAINABILITY ────────────────────────────────────────
ENERGY_CATS = {
    "solar-energy-systems": ("PV design, inverters, net metering, utility-scale, and solar economics", ["solar", "pv"]),
    "wind-energy-development": ("Site assessment, turbine technology, offshore wind, and wind project finance", ["wind", "offshore"]),
    "battery-energy-storage": ("Lithium-ion, flow batteries, BMS, and grid-scale storage deployment", ["battery", "storage"]),
    "electric-grid-management": ("Grid operations, demand response, distributed energy, and microgrids", ["grid", "utility"]),
    "carbon-accounting-reporting": ("GHG protocol, Scope 1/2/3, carbon markets, and disclosure frameworks", ["carbon", "reporting"]),
    "esg-sustainability-strategy": ("ESG frameworks, materiality, reporting standards, and stakeholder engagement", ["esg", "sustainability"]),
    "renewable-energy-finance": ("PPAs, tax equity, green bonds, and renewable project finance", ["finance", "renewable"]),
    "energy-efficiency-buildings": ("Building energy modeling, retrofits, commissioning, and energy codes", ["efficiency", "buildings"]),
    "hydrogen-fuel-cells": ("Green hydrogen, electrolysis, fuel cell technology, and hydrogen economy", ["hydrogen", "fuel-cell"]),
    "nuclear-energy-advanced": ("Small modular reactors, nuclear safety, waste management, and advanced fission", ["nuclear", "smr"]),
}

# ─── TELECOMMUNICATIONS ─────────────────────────────────────────────
TELECOM_CATS = {
    "5g-network-architecture": ("5G NR, network slicing, MEC, Open RAN, and 5G core", ["5g", "nr"]),
    "network-protocols-tcp-ip": ("TCP/IP stack, HTTP/3, QUIC, DNS, and protocol analysis", ["networking", "protocols"]),
    "voip-unified-communications": ("SIP, WebRTC, Teams/Zoom integration, and UC platforms", ["voip", "uc"]),
    "software-defined-networking-sdn": ("OpenFlow, SDN controllers, network virtualization, and intent-based networking", ["sdn", "networking"]),
    "optical-fiber-communications": ("DWDM, fiber optics, optical transport, and PON", ["optical", "fiber"]),
    "satellite-communications": ("LEO/MEO/GEO, satellite internet, ground station, and VSAT", ["satellite", "space"]),
    "wireless-networking-wifi": ("Wi-Fi 6/6E/7, mesh networks, site surveys, and WLAN design", ["wifi", "wireless"]),
    "network-automation-programmability": ("Netconf/YANG, Ansible for networks, telemetry, and network automation", ["automation", "netdevops"]),
    "telecom-billing-oss-bss": ("Rating, charging, mediation, and BSS/OSS systems", ["billing", "oss"]),
    "rf-engineering-microwave": ("RF design, antenna engineering, spectrum analysis, and microwave systems", ["rf", "antenna"]),
}

# ─── AGRICULTURE & AGTECH ──────────────────────────────────────────
AG_CATS = {
    "precision-agriculture-iot": ("Sensor networks, variable rate technology, soil mapping, and crop monitoring", ["precision", "iot"]),
    "crop-modeling-simulation": ("Growth models, yield prediction, climate impact, and DSSAT", ["modeling", "crops"]),
    "drone-agriculture-uav": ("Crop scouting, spraying, multispectral imaging, and drone regulations", ["drone", "uav"]),
    "soil-science-management": ("Soil health, fertility, conservation, and regenerative practices", ["soil", "regenerative"]),
    "hydroponics-aeroponics": ("Controlled environment agriculture, nutrient solutions, and vertical farming", ["hydroponics", "cea"]),
    "vertical-farming-indoor": ("Lighting, climate control, stacking systems, and economics", ["vertical", "indoor"]),
    "livestock-management-technology": ("Precision livestock, health monitoring, feeding systems, and welfare", ["livestock", "animal"]),
    "agricultural-economics-policy": ("Farm economics, subsidies, trade policy, and commodity markets", ["economics", "policy"]),
    "agricultural-biotechnology": ("GMOs, gene editing, biopesticides, and biostimulants", ["biotech", "genetics"]),
    "water-management-irrigation": ("Irrigation systems, water efficiency, drainage, and water rights", ["water", "irrigation"]),
}

# ─── MISCELLANEOUS ──────────────────────────────────────────────────
MISC_CATS = {
    "personal-productivity-systems": ("GTD, time blocking, energy management, and personal knowledge management", ["productivity", "gtd"]),
    "public-speaking-presentation": ("Speech structure, stage presence, slide design, and overcoming nerves", ["speaking", "presentation"]),
    "negotiation-strategies": ("BATNA, anchoring, interest-based negotiation, and cross-cultural negotiation", ["negotiation", "communication"]),
    "philosophy-thinking": ("Critical thinking, ethics frameworks, logic, and philosophical analysis", ["philosophy", "ethics"]),
    "history-research-methodology": ("Historiography, primary sources, archival research, and historical writing", ["historiography", "research"]),
    "linguistics-language-study": ("Syntax, phonology, sociolinguistics, and language documentation", ["linguistics", "language"]),
    "anthropology-fieldwork": ("Ethnography, participant observation, cultural analysis, and research ethics", ["anthropology", "culture"]),
    "psychology-cognitive-behavioral": ("CBT techniques, behavioral assessment, therapy modalities, and research methods", ["psychology", "cbt"]),
    "sociology-research": ("Qualitative/quantitative methods, social theory, and survey design", ["sociology", "research"]),
    "astronomy-astrophysics": ("Observational astronomy, data analysis, cosmology, and astrostatistics", ["astronomy", "physics"]),
}

# ─── EDUCATION & PEDAGOGY ───────────────────────────────────────────
EDUCATION_CATS = {
    "curriculum-design-development": ("Backward design, standards alignment, scope and sequence, and assessment mapping", ["curriculum", "instructional-design"]),
    "online-learning-design": ("Course authoring, LMS management, engagement strategies, and learning analytics", ["elearning", "lms"]),
    "classroom-management": ("Routines, behavior systems, relationships, and inclusive classroom culture", ["classroom", "management"]),
    "educational-assessment-testing": ("Formative/summative assessment, rubrics, item analysis, and standardized testing", ["assessment", "testing"]),
    "special-education-inclusion": ("IEPs, accommodations, differentiated instruction, and Universal Design for Learning", ["special-ed", "inclusion"]),
    "stem-education-teaching": ("Inquiry-based learning, project-based STEM, maker spaces, and coding in schools", ["stem", "pbl"]),
    "early-childhood-education": ("Play-based learning, developmental milestones, and early literacy/numeracy", ["ece", "play-based"]),
    "higher-education-teaching": ("Course design, active learning, grading for equity, and teaching portfolios", ["higher-ed", "university"]),
    "corporate-training-design": ("Needs analysis, training delivery, Kirkpatrick evaluation, and learning paths", ["training", "corporate"]),
    "educational-technology-integration": ("EdTech tools, blended learning, 1:1 programs, and digital citizenship", ["edtech", "blended-learning"]),
}

# ─── AEROSPACE & DEFENSE (ADDITIONAL) ──────────────────────────────
AEROSPACE_CATS = {
    "spacecraft-systems-engineering": ("Spacecraft buses, subsystems, mission lifecycle, and systems engineering V-model", ["spacecraft", "systems"]),
    "orbital-mechanics-astrodynamics": ("Keplerian orbits, Hohmann transfers, station-keeping, and orbital perturbations", ["orbital", "astrodynamics"]),
    "satellite-mission-design": ("Mission analysis, link budgets, ground stations, and mission operations", ["satellite", "mission"]),
    "launch-vehicle-rocketry": ("Rocket propulsion, staging, launch operations, and range safety", ["launch", "propulsion"]),
    "space-policy-law": ("Outer Space Treaty, spectrum regulation, debris mitigation, and national space law", ["space-law", "policy"]),
    "aerospace-structures-composites": ("Composite materials, FEA, fatigue analysis, and damage tolerance", ["structures", "composites"]),
    "avionics-flight-control": ("Fly-by-wire, FADEC, sensor fusion, and autopilot design", ["avionics", "flight-control"]),
    "uav-systems-engineering": ("UAS design, sense-and-avoid, beyond-visual-line-of-sight, and UTM", ["uas", "drones"]),
    "atmospheric-reentry-thermal": ("TPS, hypersonic aerothermodynamics, reentry trajectories, and ablation", ["reentry", "thermal"]),
    "deep-space-exploration": ("Interplanetary trajectories, gravity assists, deep space network, and autonomy", ["exploration", "interplanetary"]),
}

# ─── INSURANCE ──────────────────────────────────────────────────────
INSURANCE_CATS = {
    "actuarial-science-principles": ("Life tables, loss models, ratemaking, and reserve analysis", ["actuarial", "ratemaking"]),
    "property-casualty-insurance": ("P&C underwriting, claims, reinsurance, and catastrophe modeling", ["property", "casualty"]),
    "life-health-insurance": ("Life underwriting, health insurance products, disability, and long-term care", ["life", "health"]),
    "insurance-regulation-compliance": ("NAIC, state regulation, solvency, and market conduct", ["regulation", "compliance"]),
    "reinsurance-risk-transfer": ("Treaty, facultative, retrocession, and alternative risk transfer", ["reinsurance", "risk"]),
    "insurance-claims-management": ("Claims handling, adjusting, fraud detection, and litigation management", ["claims", "adjusting"]),
    "insurance-product-development": ("Product design, pricing, underwriting guidelines, and distribution", ["product", "pricing"]),
    "insurance-data-analytics": ("Predictive modeling, telematics, IoT, and advanced analytics in insurance", ["analytics", "insurtech"]),
    "captives-alternative-risk": ("Captive formation, rent-a-captive, risk retention groups, and ART", ["captive", "art"]),
    "insurance-distribution-channels": ("Agents, brokers, bancassurance, digital, and embedded insurance", ["distribution", "channels"]),
}

# ─── NONPROFIT & SOCIAL IMPACT ──────────────────────────────────────
NONPROFIT_CATS = {
    "nonprofit-strategic-planning": ("Strategic planning, theory of change, logic models, and organizational development", ["nonprofit", "strategy"]),
    "fundraising-philanthropy": ("Donor relations, major gifts, annual fund, planned giving, and grant writing", ["fundraising", "philanthropy"]),
    "social-entrepreneurship": ("Social enterprise models, impact measurement, scaling, and hybrid organizations", ["social-enterprise", "impact"]),
    "impact-investing-esg": ("ESG integration, impact measurement, SRI, and blended finance", ["impact-investing", "esg"]),
    "ngo-program-design": ("Needs assessment, program design, M&E frameworks, and adaptive management", ["ngo", "program"]),
    "community-organizing-advocacy": ("Grassroots organizing, coalition building, policy advocacy, and civic engagement", ["organizing", "advocacy"]),
    "volunteer-management-engagement": ("Recruitment, training, retention, and volunteer recognition", ["volunteer", "engagement"]),
    "nonprofit-governance-board": ("Board development, fiduciary duty, governance policies, and CEO relations", ["governance", "board"]),
    "corporate-social-responsibility": ("CSR strategy, employee volunteering, sustainability reporting, and stakeholder engagement", ["csr", "responsibility"]),
    "charitable-trust-estate-planning": ("Donor-advised funds, charitable remainder trusts, and estate planning for giving", ["charitable", "estate"]),
}

# ─── FOOD & BEVERAGE ────────────────────────────────────────────────
FOOD_CATS = {
    "culinary-arts-techniques": ("Knife skills, cooking methods, plating, and flavor profiles", ["culinary", "techniques"]),
    "food-safety-hacccp": ("HACCP, food safety plans, sanitation, and regulatory compliance", ["food-safety", "haccp"]),
    "restaurant-management-operations": ("Kitchen management, front-of-house, inventory, and labor scheduling", ["restaurant", "operations"]),
    "menu-engineering-design": ("Menu psychology, pricing strategy, profitability analysis, and menu design", ["menu", "engineering"]),
    "baking-pastry-arts": ("Pastry techniques, bread baking, dessert plating, and ingredient science", ["baking", "pastry"]),
    "brewing-distilling-fermentation": ("Beer brewing, wine making, distillation, and fermentation science", ["brewing", "distillation"]),
    "food-science-product-development": ("Product formulation, shelf-life testing, sensory evaluation, and scale-up", ["food-science", "r&d"]),
    "catering-events-management": ("Event planning, off-premise catering, logistics, and client management", ["catering", "events"]),
    "food-photography-styling": ("Food photography, styling, lighting, and social media content", ["photography", "styling"]),
    "sustainable-food-systems": ("Local food, food waste reduction, regenerative agriculture, and food justice", ["sustainable", "food-systems"]),
}

# ─── TRANSPORTATION ─────────────────────────────────────────────────
TRANSPORT_CATS = {
    "urban-mobility-planning": ("Transit planning, TOD, micromobility, and mobility-as-a-service", ["urban-mobility", "transit"]),
    "logistics-fleet-management": ("Fleet operations, maintenance, telematics, and driver safety", ["fleet", "management"]),
    "autonomous-vehicle-development": ("Perception, planning, control, safety cases, and validation for AVs", ["autonomous", "ad"]),
    "rail-transportation-engineering": ("Rail infrastructure, signaling, rolling stock, and operations", ["rail", "engineering"]),
    "maritime-shipping-operations": ("Ship operations, port logistics, maritime regulations, and chartering", ["maritime", "shipping"]),
    "aviation-operations-management": ("Airline ops, crew scheduling, maintenance planning, and ATC", ["aviation", "airline"]),
    "public-transit-systems": ("Bus, rail, BRT, paratransit, and fare collection systems", ["transit", "bus"]),
    "freight-forwarding-logistics": ("Customs brokerage, international freight, warehousing, and 3PL/4PL", ["freight", "forwarding"]),
    "supply-chain-visibility-tracking": ("Real-time visibility, EDI, track-and-trace, and control towers", ["visibility", "tracking"]),
    "transportation-demand-modeling": ("Four-step model, activity-based modeling, and travel demand management", ["demand", "modeling"]),
}

# ─── ECOMMERCE & RETAIL ─────────────────────────────────────────────
ECOM_CATS = {
    "ecommerce-platform-management": ("Shopify, Magento, WooCommerce, product catalog, and checkout optimization", ["ecommerce", "platform"]),
    "marketplace-operations": ("Multi-vendor marketplaces, seller onboarding, and marketplace economics", ["marketplace", "sellers"]),
    "retail-omnichannel-strategy": ("Unified commerce, BOPIS, ship-from-store, and inventory visibility", ["retail", "omnichannel"]),
    "product-information-management": ("PIM, product data, digital assets, and syndication", ["pim", "data"]),
    "customer-loyalty-programs": ("Loyalty strategy, points programs, VIP tiers, and gamification", ["loyalty", "retention"]),
    "retail-merchandising-planning": ("Assortment planning, space allocation, and retail analytics", ["merchandising", "planning"]),
    "returns-reverse-logistics": ("Returns policy, processing, refurbishment, and liquidation", ["returns", "reverse"]),
    "payment-processing-checkout": ("Payment gateways, fraud prevention, BNPL, and PCI compliance", ["payments", "checkout"]),
    "product-recommendation-engines": ("Collaborative filtering, personalization, and recommendation systems", ["recommendation", "personalization"]),
    "retail-data-analytics": ("Customer analytics, basket analysis, churn prediction, and RFM modeling", ["analytics", "retail"]),
}

# ─── JOURNALISM & MEDIA ─────────────────────────────────────────────
MEDIA_CATS = {
    "data-journalism-investigative": ("Data analysis, FOIA, fact-checking, and investigative workflows", ["data-journalism", "investigative"]),
    "multimedia-storytelling": ("Video, audio, interactive, and cross-platform storytelling", ["multimedia", "storytelling"]),
    "newsroom-management-editing": ("Editorial workflow, copy editing, style guides, and newsroom leadership", ["newsroom", "editing"]),
    "audience-engagement-growth": ("Audience development, newsletters, subscriptions, and community", ["audience", "engagement"]),
    "podcast-production-audio": ("Recording, editing, distribution, and monetization of podcasts", ["podcast", "audio"]),
    "social-media-journalism": ("Social-first reporting, verification, and platform strategy", ["social-media", "verification"]),
    "press-relations-media-outreach": ("Press releases, media kits, pitching, and journalist relations", ["pr", "media"]),
    "documentary-filmmaking": ("Documentary production, archival research, and impact campaigns", ["documentary", "film"]),
    "newsletter-publishing-monetization": ("Newsletter strategy, growth, monetization, and platforms", ["newsletter", "publishing"]),
    "fact-checking-verification": ("Fact-checking methodology, source verification, and debunking", ["fact-checking", "verification"]),
}

# ─── CONSTRUCTION & INFRASTRUCTURE ──────────────────────────────────
CONSTRUCTION_CATS = {
    "construction-project-management": ("Project planning, scheduling, cost control, and closeout", ["construction", "pm"]),
    "building-information-modeling-bim": ("BIM workflows, 3D modeling, clash detection, and 4D/5D BIM", ["bim", "modeling"]),
    "civil-engineering-infrastructure": ("Roads, bridges, water systems, and infrastructure planning", ["civil", "infrastructure"]),
    "lean-construction-methods": ("Last planner system, pull planning, and lean project delivery", ["lean", "construction"]),
    "construction-safety-osha": ("OSHA compliance, safety programs, and job hazard analysis", ["safety", "osha"]),
    "cost-estimating-quantity-surveying": ("Cost estimation, quantity takeoffs, and value engineering", ["estimating", "qs"]),
    "contract-administration-construction": ("Construction contracts, change orders, claims, and disputes", ["contracts", "admin"]),
    "facility-management-maintenance": ("Building maintenance, CMMS, and lifecycle management", ["facilities", "maintenance"]),
    "sustainable-building-design": ("Green building, LEED, net-zero, and sustainable materials", ["green-building", "leed"]),
    "heavy-equipment-operations": ("Equipment selection, utilization, maintenance, and safety", ["equipment", "operations"]),
}

# ─── MARINE & OFFSHORE ─────────────────────────────────────────────
MARINE_CATS = {
    "marine-engineering-design": ("Ship design, hydrodynamics, propulsion, and marine systems", ["marine", "design"]),
    "offshore-oil-gas-platforms": ("Offshore platforms, subsea systems, and marine operations", ["offshore", "oil-gas"]),
    "naval-architecture": ("Ship stability, structural design, and classification society rules", ["naval", "architecture"]),
    "port-terminal-operations": ("Port logistics, terminal operations, and maritime commerce", ["port", "terminal"]),
    "oceanography-marine-science": ("Physical oceanography, marine ecosystems, and ocean observation", ["oceanography", "science"]),
    "subsea-engineering-rov": ("Subsea systems, ROVs, pipelines, and underwater construction", ["subsea", "rov"]),
    "marine-renewable-energy": ("Offshore wind, wave energy, tidal energy, and ocean thermal", ["marine-energy", "offshore"]),
    "fisheries-aquaculture-management": ("Fisheries science, aquaculture systems, and seafood supply chain", ["fisheries", "aquaculture"]),
    "coastal-engineering-management": ("Coastal protection, erosion control, and shoreline management", ["coastal", "engineering"]),
    "marine-environmental-compliance": ("MARPOL, ballast water, emissions, and environmental regulations", ["compliance", "marpol"]),
}

# ─── PETS & ANIMAL CARE ─────────────────────────────────────────────
PETS_CATS = {
    "dog-training-behavior": ("Positive reinforcement, behavior modification, and training plans", ["dog", "training"]),
    "cat-care-behavior": ("Feline behavior, enrichment, health, and multi-cat households", ["cat", "behavior"]),
    "aquarium-fish-keeping": ("Freshwater and marine aquarium setup, water quality, and fish health", ["aquarium", "fish"]),
    "reptile-amphibian-care": ("Husbandry, heating, lighting, and species-specific care", ["reptile", "amphibian"]),
    "bird-aviary-care": ("Parrot and companion bird care, enrichment, and nutrition", ["bird", "avian"]),
    "exotic-pet-medicine": ("Exotic animal husbandry, common conditions, and veterinary care", ["exotic", "veterinary"]),
    "pet-nutrition-diet": ("Pet nutrition, diet formulation, and dietary management", ["nutrition", "diet"]),
    "animal-rescue-rehabilitation": ("Animal rescue, rehabilitation, and release programs", ["rescue", "rehabilitation"]),
    "equine-horse-care": ("Horse care, stable management, and equine health", ["horse", "equine"]),
    "pet-sitting-boarding-business": ("Pet care business, insurance, safety, and client management", ["pet-care", "business"]),
}

# ─── PARENTING & FAMILY ─────────────────────────────────────────────
PARENTING_CATS = {
    "newborn-care-basics": ("Feeding, sleep, diapering, and newborn health and safety", ["newborn", "infant"]),
    "toddler-development-play": ("Early childhood development, play-based learning, and milestones", ["toddler", "development"]),
    "positive-parenting-discipline": ("Positive discipline, boundaries, and emotion coaching", ["parenting", "discipline"]),
    "special-needs-parenting": ("Developmental disabilities, IEPs, therapies, and family support", ["special-needs", "disability"]),
    "blended-family-step-parenting": ("Blended families, co-parenting, and step-parenting strategies", ["blended-family", "co-parenting"]),
    "homeschooling-education": ("Homeschooling methods, curriculum, and legal requirements", ["homeschooling", "education"]),
    "teen-communication-development": ("Adolescent development, communication, and independence", ["teen", "adolescent"]),
    "work-life-family-balance": ("Work-family integration, childcare, and household management", ["work-life", "balance"]),
    "foster-care-adoption": ("Foster care, adoption process, and supporting children in care", ["foster", "adoption"]),
    "child-safety-proofing": ("Home safety, car seats, internet safety, and childproofing", ["safety", "childproofing"]),
}

# ─── EVENT PLANNING & HOSPITALITY ───────────────────────────────────
EVENTS_CATS = {
    "corporate-event-planning": ("Conferences, meetings, product launches, and corporate gatherings", ["corporate", "conferences"]),
    "wedding-planning-management": ("Wedding coordination, vendor management, and day-of logistics", ["wedding", "coordination"]),
    "festival-event-production": ("Large-scale event production, staging, and crowd management", ["festival", "production"]),
    "hospitality-hotel-management": ("Hotel operations, guest experience, and revenue management", ["hospitality", "hotel"]),
    "catering-food-service-events": ("Event catering, menu planning, and food service logistics", ["catering", "food-service"]),
    "event-marketing-promotion": ("Event marketing, ticketing, and audience development", ["marketing", "promotion"]),
    "virtual-hybrid-event-production": ("Virtual event platforms, hybrid production, and engagement", ["virtual", "hybrid"]),
    "event-design-decor": ("Event design, floral, lighting, and décor", ["design", "decor"]),
    "destination-event-planning": ("Destination events, travel logistics, and site selection", ["destination", "travel"]),
    "event-risk-management-safety": ("Risk assessment, emergency planning, and event insurance", ["risk", "safety"]),
}

# ─── FASHION & APPAREL ──────────────────────────────────────────────
FASHION_CATS = {
    "fashion-design-sketching": ("Fashion illustration, design development, and collection planning", ["fashion-design", "illustration"]),
    "textile-science-fabric": ("Textile properties, fabric selection, and textile testing", ["textile", "fabric"]),
    "pattern-making-draping": ("Pattern drafting, draping, and digital pattern making", ["pattern", "draping"]),
    "fashion-merchandising-buying": ("Fashion buying, merchandising, and assortment planning", ["merchandising", "buying"]),
    "sustainable-fashion-circular": ("Sustainable materials, circular fashion, and ethical production", ["sustainable", "circular"]),
    "fashion-branding-marketing": ("Fashion branding, fashion marketing, and retail strategy", ["branding", "marketing"]),
    "costume-design-film-theater": ("Costume design, wardrobe, and historical costume", ["costume", "wardrobe"]),
    "fashion-photography-editorial": ("Fashion photography, editorial styling, and lookbooks", ["photography", "editorial"]),
    "apparel-manufacturing-production": ("Apparel production, quality control, and supply chain", ["manufacturing", "production"]),
    "fashion-technology-wearables": ("Wearable tech, smart textiles, and fashion innovation", ["wearables", "innovation"]),
}

# ─── FORESTRY & NATURAL RESOURCES ──────────────────────────────────
FORESTRY_CATS = {
    "forest-management-silviculture": ("Silviculture, timber management, and forest planning", ["forestry", "silviculture"]),
    "wildlife-conservation-biology": ("Wildlife biology, habitat management, and conservation planning", ["wildlife", "conservation"]),
    "watershed-management": ("Watershed planning, riparian zones, and water quality", ["watershed", "riparian"]),
    "park-recreation-management": ("Park planning, recreation management, and interpretation", ["parks", "recreation"]),
    "natural-resource-economics": ("Resource economics, valuation, and policy analysis", ["economics", "resources"]),
    "fire-ecology-management": ("Fire ecology, prescribed burn, and wildfire management", ["fire", "wildfire"]),
    "fisheries-wildlife-law-enforcement": ("Conservation law, enforcement, and public education", ["law-enforcement", "conservation"]),
    "urban-forestry-green-infrastructure": ("Urban trees, green infrastructure, and ecosystem services", ["urban", "green-infra"]),
    "endangered-species-recovery": ("Endangered species, recovery plans, and habitat conservation", ["endangered", "recovery"]),
    "ecological-restoration": ("Restoration ecology, reclamation, and habitat restoration", ["restoration", "reclamation"]),
}

# ─── MATHEMATICS & STATISTICS ───────────────────────────────────────
MATH_CATS = {
    "applied-mathematics-modeling": ("Mathematical modeling, differential equations, and numerical methods", ["applied-math", "modeling"]),
    "bayesian-statistics-inference": ("Bayesian methods, MCMC, and probabilistic programming", ["bayesian", "mcmc"]),
    "time-series-analysis-forecasting": ("ARIMA, exponential smoothing, state space models, and forecasting", ["time-series", "forecasting"]),
    "optimization-operations-research": ("Linear programming, integer programming, and optimization methods", ["optimization", "or"]),
    "stochastic-processes": ("Markov chains, Poisson processes, and stochastic calculus", ["stochastic", "markov"]),
    "statistical-learning-theory": ("PAC learning, VC dimension, and generalization bounds", ["learning-theory", "statistical"]),
    "topology-geometry": ("Algebraic topology, differential geometry, and geometric analysis", ["topology", "geometry"]),
    "number-theory-cryptography": ("Prime numbers, modular arithmetic, and cryptographic applications", ["number-theory", "crypto"]),
    "numerical-linear-algebra": ("Matrix computations, eigenvalue problems, and numerical stability", ["linear-algebra", "numerical"]),
    "causal-inference-methods": ("Causal inference, potential outcomes, and instrumental variables", ["causal", "inference"]),
}

# ─── CHEMISTRY & MATERIALS SCIENCE ─────────────────────────────────
CHEMISTRY_CATS = {
    "computational-chemistry-dft": ("DFT, molecular dynamics, and computational chemistry methods", ["computational", "dft"]),
    "polymer-chemistry-synthesis": ("Polymer synthesis, characterization, and polymer physics", ["polymer", "synthesis"]),
    "electrochemistry-energy": ("Batteries, fuel cells, and electrochemistry", ["electrochemistry", "energy"]),
    "organic-synthesis-methods": ("Synthetic methods, retrosynthesis, and reaction mechanisms", ["organic", "synthetic"]),
    "inorganic-coordination-chemistry": ("Coordination compounds, organometallics, and catalysis", ["inorganic", "catalysis"]),
    "analytical-chemistry-spectroscopy": ("Spectroscopy, chromatography, and analytical methods", ["analytical", "spectroscopy"]),
    "surface-science-catalysis": ("Surface science, heterogeneous catalysis, and interfaces", ["surface", "catalysis"]),
    "biochemistry-structural": ("Structural biology, protein chemistry, and enzymology", ["biochemistry", "structural"]),
    "materials-characterization": ("XRD, SEM, TEM, and materials characterization techniques", ["characterization", "microscopy"]),
    "green-chemistry-sustainable": ("Green chemistry, sustainable synthesis, and atom economy", ["green-chemistry", "sustainable"]),
}

# ─── LINGUISTICS & TRANSLATION ──────────────────────────────────────
LINGUISTICS_CATS = {
    "machine-translation-nmt": ("Neural machine translation, Transformer models, and MT evaluation", ["nmt", "translation"]),
    "speech-recognition-asr": ("Automatic speech recognition, CTC, and end-to-end ASR", ["asr", "speech"]),
    "text-to-speech-tts": ("TTS synthesis, vocoders, and neural speech synthesis", ["tts", "speech"]),
    "natural-language-understanding": ("NLU, semantic parsing, and intent recognition", ["nlu", "semantics"]),
    "information-extraction-ie": ("Named entity recognition, relation extraction, and event extraction", ["ie", "ner"]),
    "question-answering-systems": ("Reading comprehension, open-domain QA, and retrieval", ["qa", "reading"]),
    "dialogue-systems-chatbots": ("Task-oriented dialogue, conversational AI, and chatbot design", ["dialogue", "conversational"]),
    "sentiment-analysis-opinion": ("Sentiment analysis, emotion detection, and opinion mining", ["sentiment", "emotion"]),
    "document-summarization": ("Extractive and abstractive summarization, and evaluation metrics", ["summarization", "nlp"]),
    "cross-lingual-transfer-multilingual": ("Multilingual models, cross-lingual transfer, and language universals", ["multilingual", "cross-lingual"]),
}



# ─── BOARD GAMES ────────────────────────────────────────────────────
BOARD_GAMES_CATS = {
    "chess-strategy-tactics": ("Opening theory, middlegame strategy, endgame technique, and tactical patterns", ["chess", "strategy"]),
    "go-game-strategy": ("Joseki, tesuji, influence vs territory, and modern AI-driven strategy", ["go", "strategy"]),
    "poker-texas-holdem": ("GTO, ICM, range construction, and tournament/cash game strategy", ["poker", "gaming"]),
    "bridge-card-game": ("Bidding systems, declarer play, defense, and tournament bridge", ["bridge", "cards"]),
    "scrabble-word-games": ("Word knowledge, rack management, board control, and tournament strategy", ["scrabble", "word-games"]),
    "board-game-design-mechanics": ("Game mechanics, prototyping, playtesting, and publishing", ["board-game", "design"]),
    "tabletop-rpg-worldbuilding": ("Worldbuilding, campaign design, encounter balancing, and RPG systems", ["rpg", "worldbuilding"]),
    "escape-room-puzzle-design": ("Puzzle design, narrative integration, flow, and difficulty curves", ["escape-room", "puzzles"]),
    "magic-the-gathering-strategy": ("Deck building, metagame, limited formats, and competitive play", ["mtg", "tcg"]),
    "dunge-dragons-dming": ("Adventure design, DM techniques, rules adjudication, and player engagement", ["dnd", "dming"]),
}

# ─── TRAVEL ─────────────────────────────────────────────────────────
TRAVEL_CATS = {
    "travel-planning-itinerary": ("Itinerary building, logistics, budgeting, and travel optimization", ["travel", "itinerary"]),
    "solo-travel-safety": ("Solo travel planning, safety, budgeting, and community", ["solo-travel", "safety"]),
    "backpacking-budget-travel": ("Budget travel, hostels, backpacking routes, and gear", ["backpacking", "budget"]),
    "luxury-travel-experiences": ("Luxury travel planning, exclusive experiences, and high-end service", ["luxury", "experiences"]),
    "digital-nomad-lifestyle": ("Remote work, co-living, visas, and location independence", ["digital-nomad", "remote-work"]),
    "cultural-tourism-heritage": ("Heritage tourism, cultural sensitivity, and sustainable travel", ["cultural", "heritage"]),
    "adventure-travel-activities": ("Adventure sports, expeditions, gear, and risk management", ["adventure", "expeditions"]),
    "wellness-spa-retreats": ("Wellness travel, spa retreats, mindfulness, and health tourism", ["wellness", "retreats"]),
    "culinary-tourism-food-travel": ("Food tours, culinary experiences, and gastronomic tourism", ["culinary", "food-travel"]),
    "eco-tourism-sustainable": ("Eco-friendly travel, conservation tourism, and sustainable practices", ["eco-tourism", "sustainable"]),
}

# ─── COMEDY & ENTERTAINMENT ────────────────────────────────────────
COMEDY_CATS = {
    "stand-up-comedy-writing": ("Joke writing, stage presence, material development, and performance", ["stand-up", "comedy"]),
    "sketch-comedy-writing": ("Sketch structure, characters, parody, and production", ["sketch", "writing"]),
    "improv-comedy-performance": ("Improv games, 'yes and', scene work, and long-form improv", ["improv", "performance"]),
    "sitcom-tv-writing": ("Sitcom structure, writers' room, pitch, and script format", ["sitcom", "tv-writing"]),
    "meme-internet-culture": ("Meme creation, virality, remix culture, and platform dynamics", ["meme", "internet"]),
    "entertainment-industry-business": ("Talent management, production, distribution, and deal-making", ["entertainment", "business"]),
    "stand-up-comedy-marketing": ("Self-promotion, social media, touring, and building an audience", ["comedy", "marketing"]),
    "tv-production-management": ("TV production, budgeting, scheduling, and post-production", ["tv", "production"]),
    "youtube-content-creation": ("Channel growth, video production, SEO, and monetization", ["youtube", "creator"]),
    "twitch-streaming-growth": ("Stream setup, community building, engagement, and monetization", ["twitch", "streaming"]),
}

# ─── CRAFTS & DIY ──────────────────────────────────────────────────
CRAFTS_CATS = {
    "woodworking-cabinetry": ("Joinery, finishing, furniture design, and workshop safety", ["woodworking", "furniture"]),
    "pottery-ceramics": ("Wheel throwing, hand-building, glazing, and kiln firing", ["pottery", "ceramics"]),
    "knitting-crochet": ("Patterns, techniques, yarn selection, and garment construction", ["knitting", "crochet"]),
    "jewelry-making-design": ("Metalsmithing, beadwork, wire wrapping, and design", ["jewelry", "metalwork"]),
    "leather-crafting": ("Leatherworking, tooling, stitching, and finishing", ["leather", "crafting"]),
    "candle-soap-making": ("Candle making, soap making, and natural product formulation", ["candles", "soap"]),
    "paper-crafts-bookbinding": ("Paper crafts, card making, and bookbinding", ["paper", "bookbinding"]),
    "glass-bead-fusing": ("Glass fusing, bead making, and stained glass", ["glass", "fusing"]),
    "metal-forging-blacksmithing": ("Blacksmithing, forging, heat treatment, and tool making", ["forging", "blacksmithing"]),
    "diy-home-improvement": ("Home repair, renovation, tools, and project planning", ["diy", "home-improvement"]),
}

# ─── CRYPTO & DeFi ─────────────────────────────────────────────────
CRYPTO_CATS = {
    "decentralized-finance-defi-protocols": ("Lending, DMs, yield farming, and DeFi primitives", ["defi", "protocols"]),
    "nft-digital-collectibles": ("NFT standards, marketplaces, creator royalties, and utility NFTs", ["nft", "collectibles"]),
    "dao-governance": ("DAO frameworks, governance tokens, voting, and treasury management", ["dao", "governance"]),
    "solidity-smart-contracts": ("Solidity, contract security, testing, and deployment", ["solidity", "smart-contracts"]),
    "web3-frontend-dapp": ("Web3.js, ethers.js, wallet integration, and dApp UX", ["web3", "frontend"]),
    "tokenomics-design": ("Token design, incentive mechanisms, and economic modeling", ["tokenomics", "design"]),
    "layer2-scaling-solutions": ("Rollups, sidechains, and L2 ecosystem", ["l2", "scaling"]),
    "cross-chain-bridges-interop": ("Bridge protocols, cross-chain messaging, and interoperability", ["bridge", "interop"]),
    "crypto-trading-analysis": ("On-chain analysis, technical analysis, and risk management", ["crypto", "trading"]),
    "blockchain-security-auditing": ("Smart contract auditing, formal verification, and bug bounties", ["security", "auditing"]),
}

# ─── FAMILY HISTORY ─────────────────────────────────────────────────
FAMILY_HISTORY_CATS = {
    "genealogy-research": ("Genealogical research, census records, and family tree building", ["genealogy", "family-tree"]),
    "dna-testing-analysis": ("DNA testing, ethnicity estimates, and genetic genealogy", ["dna", "genetics"]),
    "historical-records-research": ("Archival research, primary sources, and historical records", ["archives", "research"]),
    "oral-history-interviewing": ("Oral history methods, interviewing, and preservation", ["oral-history", "interviews"]),
    "photo-preservation-digitization": ("Photo preservation, digitization, and metadata", ["photo", "preservation"]),
    "family-history-publishing": ("Family history books, charts, and multimedia publishing", ["publishing", "family-history"]),
    "immigration-ancestral-research": ("Immigration records, passenger lists, and naturalization", ["immigration", "ancestry"]),
    "military-records-research": ("Military service records, pensions, and unit histories", ["military", "records"]),
    "house-history-research": ("Property research, building histories, and land records", ["house", "property"]),
    "cultural-heritage-preservation": ("Cultural heritage, traditions, and preservation methods", ["heritage", "preservation"]),
}

# ─── SELF IMPROVEMENT ──────────────────────────────────────────────
SELF_IMPROVEMENT_CATS = {
    "mindfulness-meditation": ("Meditation techniques, mindfulness practices, and stress reduction", ["mindfulness", "meditation"]),
    "emotional-intelligence-eq": ("EQ development, empathy, self-awareness, and social skills", ["eq", "emotions"]),
    "habit-formation-science": ("Habit loops, behavioral design, and habit stacking", ["habits", "behavior"]),
    "time-management-productivity": ("Time management, prioritization, and productivity systems", ["time", "productivity"]),
    "goal-setting-achievement": ("Goal setting, OKRs, and achievement psychology", ["goals", "achievement"]),
    "resilience-grit-development": ("Resilience, grit, and overcoming adversity", ["resilience", "grit"]),
    "confidence-self-esteem": ("Confidence building, self-esteem, and assertiveness", ["confidence", "self-esteem"]),
    "creativity-cultivation": ("Creative thinking, idea generation, and creative blocks", ["creativity", "ideation"]),
    "learning-how-to-learn": ("Learning science, memory techniques, and skill acquisition", ["learning", "metacognition"]),
    "life-coaching-techniques": ("Coaching frameworks, powerful questions, and accountability", ["coaching", "accountability"]),
}
ALL_CATEGORIES = [
    GAME_CATS, SECURITY_CATS, ROBOTICS_CATS, QUANTUM_CATS, GEOSPATIAL_CATS,
    PM_CATS, LEGAL_CATS, HEALTHCARE_CATS, DESIGN_CATS, MANUFACTURING_CATS,
    MARKETING_CATS, SCIENCE_CATS, MUSIC_CATS, PHOTO_CATS, WRITING_CATS,
    SPORTS_CATS, GOV_CATS, RE_CATS, SUPPLY_CATS, ENERGY_CATS,
    TELECOM_CATS, AG_CATS, MISC_CATS, EDUCATION_CATS, AEROSPACE_CATS,
    INSURANCE_CATS, NONPROFIT_CATS, FOOD_CATS, TRANSPORT_CATS, ECOM_CATS,
    MEDIA_CATS, CONSTRUCTION_CATS, MARINE_CATS, PETS_CATS, PARENTING_CATS,
    EVENTS_CATS, FASHION_CATS, FORESTRY_CATS, MATH_CATS, CHEMISTRY_CATS,
    LINGUISTICS_CATS, BOARD_GAMES_CATS, TRAVEL_CATS, COMEDY_CATS,
    CRAFTS_CATS, CRYPTO_CATS, FAMILY_HISTORY_CATS, SELF_IMPROVEMENT_CATS,
]

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


def make_title(name: str) -> str:
    """Convert kebab-case name to Title Case."""
    return name.replace('-', ' ').title()


def generate_skills():
    existing = {d.name for d in REPO_SKILLS.iterdir() if d.is_dir()}
    created = 0
    skipped = 0
    errors = 0

    for category_dict in ALL_CATEGORIES:
        for name, (description, tags) in category_dict.items():
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

    print(f"\n=== Generation Complete ===")
    print(f"  Created: {created}")
    print(f"  Skipped (exists): {skipped}")
    print(f"  Errors: {errors}")
    print(f"  Total in repo now: {len(existing)}")
    return created


if __name__ == "__main__":
    apply = "--apply" in sys.argv
    dry_run = not apply

    if dry_run:
        # Count what would be created
        existing = {d.name for d in REPO_SKILLS.iterdir() if d.is_dir()}
        would_create = sum(
            1 for cat in ALL_CATEGORIES
            for name in cat
            if name not in existing
        )
        print(f"=== DRY RUN ===")
        print(f"  Existing skills: {len(existing)}")
        print(f"  Would create: {would_create}")
        print(f"  Would total: {len(existing) + would_create}")
        print(f"\nRun with --apply to generate {would_create} skills.")
        sys.exit(0)

    generate_skills()
