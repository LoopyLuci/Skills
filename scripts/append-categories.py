#!/usr/bin/env python3
"""Append additional niche categories to generate-missing-skills.py"""
import re

path = r"Z:\Projects\Skills\LoopyLuci-skills\scripts\generate-missing-skills.py"
with open(path, encoding='utf-8') as f:
    content = f.read()

extra_cats = '''

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
'''

# Insert the new category blocks before the ALL_CATEGORIES list
marker = "ALL_CATEGORIES = ["
if marker not in content:
    print(f"ERROR: '{marker}' not found")
    exit(1)

content = content.replace(marker, extra_cats + marker)

# Update the ALL_CATEGORIES list
old_end = "    LINGUISTICS_CATS,\n]"
new_end = "    LINGUISTICS_CATS, BOARD_GAMES_CATS, TRAVEL_CATS, COMEDY_CATS,\n    CRAFTS_CATS, CRYPTO_CATS, FAMILY_HISTORY_CATS, SELF_IMPROVEMENT_CATS,\n]"

content = content.replace(old_end, new_end)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
total = content.count("_CATS = {")
print(f"Appended. Total category blocks: {total}")
