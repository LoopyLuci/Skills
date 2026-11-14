# ItemForge Platform Architecture

The complete architecture for the ItemForge all-in-one item listing and sales platform.

---

## Full Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    Desktop GUI (pywebview/WebView2)           │
│  Item Tree │ Photo Preview │ AI Research │ Docs │ Listings   │
└──────────────────────────────────────────────────────────────┘
                              │  Local REST API (JSON)
┌──────────────────────────────────────────────────────────────┐
│              FastAPI Backend (Python)                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│  │ Ingestion    │ │ Research     │ │ Documentation      │ │
│  │ Service      │ │ Service      │ │ Generator          │ │
│  └──────────────┘ └──────────────┘ └──────────────────────┘ │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│  │ Listing      │ │ Schedule/Auto│ │ Platform Integrations│ │
│  │ Writer       │ │ Engine       │ │ (FB, IG, eBay)       │ │
│  └──────────────┘ └──────────────┘ └──────────────────────┘ │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│  │ AI Gateway   │ │ Media Repo   │ │ Storage / DB         │ │
│  │ (ModelMistress│ │ (organized   │ │ (SQLite + Vector DB) │ │
│  │  router)     │ │  photos)     │ │                      │ │
│  └──────────────┘ └──────────────┘ └──────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐    ┌────────▼────────┐    ┌────────▼────────┐
│ ModelMistress  │    │ Local Models    │    │ Web Search      │
│ Hub (Rust)     │    │ (llama.cpp)     │    │ (DuckDuckGo)    │
│ /v1 chat, vision│   │ Qwen3.5-9B      │    │ SerpAPI/DDG     │
│ /v1/vision/*   │    │ Image gen, TTS  │    │                 │
│ /v1/vision/*   │    │ Embeddings,     │    │                 │
│ /v1/km/*       │    │ reranking       │    │                 │
└────────────────┘    └────────────────┘    └─────────────────┘
```

---

## Component Breakdown

| Component | Technology | Role |
|-----------|------------|------|
| **GUI** | pywebview + WebView2 | Native desktop window, vanilla JS frontend |
| **Backend** | FastAPI + Uvicorn | REST API, async processing, admin UI |
| **Database** | SQLite → PostgreSQL | Product catalog, listings, AI logs |
| **Vector DB** | Qdrant or ChromaDB | RAG for product catalog and research |
| **AI Gateway** | ModelMistress API + Python client | Route to local models, fallback, caching |
| **Image Processor** | OpenCV + Pillow | Photo analysis, thumbnails, clustering |
| **OCR** | Tesseract | Read labels, product names from images |
| **Embedding Model** | nomic-embed-text (via ModelMistress) | Product catalog embeddings |
| **Vision Model** | ONNX (via ModelMistress vision) | Product identification |

---

## Data Model

### Products (catalog entities)

```sql
CREATE TABLE products (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    type TEXT,
    subtype TEXT,
    brand TEXT,
    colors TEXT,
    material TEXT,
    condition TEXT,
    features TEXT,
    dimensions_cm TEXT,
    price_range TEXT,
    research_notes TEXT,
    documentation TEXT,
    facebook_listing TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);
```

### Images

```sql
CREATE TABLE images (
    id TEXT PRIMARY KEY,
    product_id TEXT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    relative_path TEXT NOT NULL,
    role TEXT NOT NULL,
    embedding BLOB,
    perceptual_hash TEXT,
    uploaded_at TEXT DEFAULT (datetime('now'))
);
```

### Listings

```sql
CREATE TABLE listings (
    id TEXT PRIMARY KEY,
    product_id TEXT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    platform TEXT NOT NULL,
    title TEXT,
    description TEXT,
    price TEXT,
    status TEXT DEFAULT 'draft',
    published_at TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);
```

### AI Logs

```sql
CREATE TABLE ai_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT NOT NULL,
    task_type TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    latency_ms INTEGER,
    tokens_prompt INTEGER,
    tokens_completion INTEGER,
    error TEXT,
    timestamp TEXT DEFAULT (datetime('now'))
);
```

---

## API Endpoints

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

## Cost Analysis

| Component | Cost |
|-----------|------|
| ModelMistress hub | $0 (open source) |
| Qwen3.5-9B (GGUF) | $0 (download from HF) |
| Vision models (ONNX) | $0 (download from HF) |
| Embedding model | $0 |
| Database (SQLite) | $0 |
| Desktop GUI (pywebview) | $0 |
| Your GPU (RX 7900 XTTX) | $0 (already owned) |
| **Total** | **$0/month** |
