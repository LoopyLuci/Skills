---
name: "itemforge"
title: "ItemForge — All-in-One Item Listing & Sales Platform"
description: "Auto-organize photos, research products, generate documentation, create multi-platform listings using local AI (ModelMistress)."
author: "Hermes Agent"
license: MIT
version: 2.0.0
metadata:
  hermes:
    tags: [e-commerce, photo-organization, item-listing, sales-automation, modelmistress, itemforge, local-ai]
    related_skills: [desktop-dashboard, python-ai-agent-platform, windows-python-shell-interop, model-mistress-desktop-dev]
    references: [itemforge-api.md, modelmistress-endpoints.md]

---

# ItemForge — All-in-One Item Listing & Sales Platform

**Trigger:** Use when organizing photos into item folders, researching products, generating documentation, creating Facebook/Instagram/Ebay/Etsy listings, or designing an all-in-one local AI selling platform.

**Core AI backend:** [ModelMistress](https://github.com/LoopyLuci/ModelMistress) — local model hub (OpenAI-compatible API + Ollama-compatible API + MCP + ACP)

**Platform type:** Desktop-first (pywebview/WebView2 or Tauri shell + FastAPI backend). Not a browser dashboard.

**Guiding principles:**
- Local-first: all processing on your machine (RX 7900 XTTX GPU, Windows 10)
- Zero cloud costs: everything runs locally via ModelMistress
- Modular, composable architecture: swap backends, platforms, themes at runtime
- Production-grade: robust error handling, retry logic, logging, state persistence

**User preferences (standing):**
- Desktop GUI = pywebview/Tauri, never browser dashboard
- Free models sorted to top; paid models hidden by default for Nous/OpenRouter
- Multi-platform listing optimization (title formulas, description formats)
- Full implementation, zero tolerance for bugs
- Use ModelMistress as the local AI backend — zero cloud costs, fully private, fast

---

## Quick Decision Tree

| You have... | Use... |
|-------------|--------|
| 63 photos to organize | ItemForge ingestion + photo organizer |
| 2 items identified (military pail, wine glasses) | ItemForge research + documentation + listings |
| Need AI vision for item ID | ModelMistress `/v1/vision/classify` |
| Need chat research | ModelMistress `/v1/chat/completions` |
| Need embeddings | ModelMistress `/v1/embeddings` |
| Need multi-platform posting | ItemForge listing generator |
| Need desktop GUI | pywebview + FastAPI backend |

---

## Procedure (Step-by-Step)

### Step 1: Install ModelMistress (AI Backend)

```bash
# Clone and build
git submodule update --init --recursive engines/llama.cpp
cargo build --release -p model-mistress --features bundled-engine

# Serve (foreground)
model-mistress serve

# Pull models
model-mistress pull hf.co/unsloth/Qwen3-8B-GGUF:Q4_K_M
model-mistress pull hf.co/nomic-ai/nomic-embed-text-v1.5-Q5_0

# Install vision models (classification/detection)
# Copy .onnx + .json sidecar into <home>/vision/
```

### Step 2: Start the ItemForge Platform (FastAPI Backend)

```bash
cd itemforge
uvicorn app.main:app --reload
```

### Step 3: Ingest Photos

```bash
# Import photos from Sell folder
curl -X POST http://127.0.0.1:8000/v1/forge/ingest \
  -H "Authorization: Bearer $TOKEN" \
  -F "folder=C:/Users/limpi/OneDrive/Documents/Sell"
```

**Response:**
```json
{
  "folders_created": 12,
  "images_processed": 63,
  "duplicates_removed": 3,
  "items_created": 2,
  "errors": []
}
```

### Step 4: Identify Items

**Preferred — Local Vision (ModelMistress):**
```python
import aiohttp, base64

async def identify_item(image_path: str) -> dict:
    async with aiohttp.ClientSession() as s:
        async with s.post(
            "http://127.0.0.1:12345/v1/vision/classify",
            headers={"Authorization": f"Bearer {token}"},
            json={"image": f"data:image/jpeg;base64,{base64_encode(image_path)}"}
        ) as resp:
            return await resp.json()
```

**Fallback — Local VLM (ModelMistress chat):**
```python
async def describe_item(image_path: str) -> str:
    prompt = f"Describe this product in detail. What is it? Key features, brand, condition, colors, any labels or packaging."
    async with aiohttp.ClientSession() as s:
        async with s.post(
            "http://127.0.0.1:12345/v1/chat/completions",
            headers={"Authorization": f"Bearer {token}"},
            json={"model": "qwen3.5:9b", "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_encode(image_path)}"}}]}]}
        ) as resp:
            return await resp.json()
```

### Step 5: Generate Research

```bash
# Research item 1 (military pail)
curl -X POST http://127.0.0.1:8000/v1/forge/items/{id}/research \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"depth": "deep", "include_web": true}'
```

### Step 6: Generate Documentation

```bash
# Generate markdown documentation
curl -X POST http://127.0.0.1:8000/v1/forge/items/{id}/docs \
  -H "Authorization: Bearer $TOKEN"
```

### Step 7: Generate Listings

```bash
# Generate multi-platform listings (Facebook, Instagram, eBay, Etsy)
curl -X POST http://127.0.0.1:8000/v1/forge/items/{id}/listings \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"platforms": ["facebook", "instagram", "ebay", "etsy"]}'
```

### Step 8: Publish

```bash
# Publish to Facebook Marketplace
curl -X POST http://127.0.0.1:8000/v1/forge/listings/{listings_id}/publish \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"platform": "facebook", "title": "Optimized title", "description": "Optimized description", "price": "$12", "shipping": "Local pickup only"}'
```

---

## ItemForge Project Structure

```text
Z:\Projects\ModelMistress\
├── itemforge/                    # New: ItemForge platform
│   ├── app/                      # FastAPI backend
│   │   ├── main.py               # FastAPI app entry
│   │   ├── config.py             # Settings
│   │   ├── models.py             # Pydantic schemas
│   │   ├── database.py           # SQLite/PostgreSQL
│   │   ├── services/
│   │   │   ├── ingestion.py      # Photo organizer
│   │   │   ├── research.py       # AI research
│   │   │   ├── docs.py           # Documentation generator
│   │   │   ├── listings.py       # Listing writer
│   │   │   └── ai_gateway.py     # ModelMistress router
│   │   └── routes/
│   │       ├── items.py
│   │       ├── listings.py
│   │       └── status.py
│   ├── docs/
│   │   ├── acp.md               # ACP protocol documentation
│   │   ├── api.md               # API reference
│   │   └── platform-design.md   # Full architecture
│   └── README.md                # This file
└── README.md                     # ModelMistress overview
```

---

## ItemForge API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/forge/ingest` | Upload photos / add folder |
| `GET` | `/v1/forge/items` | List all items with thumbnails |
| `GET` | `/v1/forge/items/{id}` | Get product entity |
| `POST` | `/v1/forge/items/{id}/research` | Run AI research |
| `POST` | `/v1/forge/items/{id}/docs` | Generate documentation |
| `POST` | `/v1/forge/items/{id}/listings` | Generate multi-platform listings |
| `GET` | `/v1/forge/listings` | List generated listings |
| `POST` | `/v1/forge/listings/{id}/publish` | Approve & publish |
| `GET` | `/v1/forge/status` | Health check |
| `GET` | `/v1/forge/ai/status` | ModelMistress connection status |

---

## ModelMistress Integration Points

| Platform Feature | ModelMistress Endpoint |
|------------------|------------------------|
| **Photo ID** | `POST /v1/vision/classify` |
| **Item research** | `POST /v1/chat/completions` |
| **Documentation** | `POST /v1/chat/completions` |
| **Facebook listing** | `POST /v1/chat/completions` |
| **Product search** | `POST /v1/embeddings` |
| **Smart search** | `POST /v1/rerank` |
| **Voice input** | `POST /v1/audio/transcriptions` |
| **Voice output** | `POST /v1/audio/speech` |
| **Knowledge base** | `/v1/km/...` |
| **Observability** | `/v1/native/traces` |

See `references/modelmistress-endpoints.md` for the full ModelMistress endpoint reference.

---

## Four Interface Types

### 1. API (HTTP REST)
- `/v1/forge/*` — ItemForge REST API
- `/v1/*` — ModelMistress OpenAI-compatible API
- `/api/*` — ModelMistress control API

### 2. CLI (Command-Line)
```bash
model-mistress serve              # HTTP server
model-mistress chat qwen3 "hi"    # REPL chat
model-mistress models             # List models
model-mistress pull ...           # Download model
model-mistress mcp                # MCP over stdio
model-mistress vision resnet50 img.jpg  # Vision analysis
model-mistress transcribe audio.wav   # Speech-to-text
model-mistress speak "hi" --out out.wav  # Text-to-speech
model-mistress km load ecommerce-best-practices  # Knowledge module
```

### 3. MCP (Model Context Protocol)
- `mcp-server` — Bidirectional agent communication
- Tools: `list_models`, `chat`, `health`, `identify_item`, `research_item`, `generate_documentation`, `generate_facebook_listing`, `list_products`, `search_products`, `get_product`
- Used by Hermes Agent and other agents

### 4. ACP (Agent Client Protocol)
- `/api/acp/*` — Agent-to-agent communication
- Capability negotiation, health check, model registry, tool invocation
- Enables Hermes Agent to control ItemForge and vice versa

---

## Model Routing Table

| Task | Preferred Model | Fallback | Backup |
|------|-------------------|----------|--------|
| **Image identification** | Vision ONNX (ResNet-50, CLIP) | Chat Qwen3.5-9B | Chat Qwen3.5-7B |
| **Item research** | Qwen3.5-9B (Q4_K_M) | Qwen3.5-7B | Qwen3-3B |
| **Documentation generation** | Qwen3.5-9B | Qwen3.5-7B | Qwen3-3B |
| **Facebook listing generation** | Qwen3.5-9B | Qwen3.5-7B | Qwen3-3B |
| **Embeddings** | nomic-embed-text (via ModelMistress) | sentence-transformers | — |
| **OCR/labels** | Tesseract (local) | — | — |
| **Text-to-speech** | llama-tts (via ModelMistress) | — | — |
| **Web search** | DuckDuckGo (free) | SerpAPI (paid) | — |

---

## Performance & Scalability

| Component | Strategy |
|-----------|----------|
| **Image processing** | OpenCV + Pillow; batch processing; GPU acceleration |
| **AI inference** | ModelMistress serves local models via llama.cpp; GPU if available |
| **Caching** | LRU (50 entries, 5-min TTL); embedding cache (1000 entries, 24-hr) |
| **Circuit breaker** | 5 failures → 60s open → retry |
| **Rate limiting** | Per-model concurrency limits (ModelMistress handles this) |
| **Vector DB** | Qdrant/ChromaDB; HNSW index for fast similarity search |
| **Database** | SQLite for dev; PostgreSQL for prod (connection pooling) |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| ModelMistress not connecting | Check `<home>/control.json` for URL and token |
| Vision not working | Install ONNX models in `<home>/vision/` |
| Embeddings not working | Pull `nomic-embed-text-v1.5` |
| Quota exceeded | Reset via `model-mistress keys rotate` |
| Rate limited | Use `model-mistress schedule` to queue requests |
| CLI not found | Run `cargo build --release -p model-mistress --features bundle-engine` |
| Vision API rate limit (429) | Wait 40-45 min, or use local AI fallback |

---

## User Preferences Embedded

- **Desktop GUI = pywebview/Tauri, never browser dashboard**
- **Free models sorted to top; paid models hidden by default** for Nous/OpenRouter
- **Multi-platform listing optimization** (title formulas, description formats)
- **Full implementation, zero tolerance for bugs**
- **Use ModelMistress as the local AI backend** — zero cloud costs, fully private, fast
- **ItemForge name** — "Forging items into listings" (create + document + publish in one place)

---

## References

- `references/itemforge-api.md` — Condensed ItemForge API endpoint reference
- `references/modelmistress-endpoints.md` — Full ModelMistress direct API endpoint reference
- `Z:\Projects\ModelMistress\README.md` — ModelMistress overview, quick start, API reference
- `Z:\Projects\ModelMistress\DESIGN.md` — ModelMistress architecture
- `Z:\Projects\ModelMistress\CLAUDE.md` — Notes for agents
- `Z:\Projects\ModelMistress\itemforge\README.md` — ItemForge platform documentation
- `Z:\Projects\ModelMistress\itemforge\docs\acp.md` — ACP protocol documentation
- `Z:\Projects\ModelMistress\itemforge\docs\api.md` — API reference
- `Z:\Projects\ModelMistress\src\mcp\` — MCP server implementation
- `Z:\Projects\ModelMistress\src\protocol\` — Internal protocol and capability negotiation
- `Z:\Projects\ModelMistress\src\hub\` — HTTP server implementation
- `X:\Dev\hermes\skills\e-commerce-photo-workflow\SKILL.md` — Photography workflow skill
