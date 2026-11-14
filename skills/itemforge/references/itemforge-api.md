# ItemForge API Endpoint Reference

Condensed API reference for the ItemForge platform. Full details in `docs/api.md`.

---

## Endpoint Summary

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

## Request/Response Examples

### Ingest

```bash
curl -X POST http://127.0.0.1:8000/v1/forge/ingest \
  -H "Authorization: Bearer $TOKEN" \
  -F "folder=C:/Users/limpi/OneDrive/Documents/Sell"
```

```json
{
  "folders_created": 12,
  "images_processed": 63,
  "duplicates_removed": 3,
  "items_created": 2,
  "errors": []
}
```

### Research

```bash
curl -X POST http://127.0.0.1:8000/v1/forge/items/{id}/research \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"depth": "deep", "include_web": true}'
```

### Listings

```bash
curl -X POST http://127.0.0.1:8000/v1/forge/items/{id}/listings \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"platforms": ["facebook", "instagram", "ebay", "etsy"]}'
```

### Publish

```bash
curl -X POST http://127.0.0.1:8000/v1/forge/listings/{listings_id}/publish \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "facebook",
    "title": "Optimized title",
    "description": "Optimized description",
    "price": "$12",
    "shipping": "Local pickup only"
  }'
```

---

## Error Format

```json
{
  "detail": {
    "error": {
      "code": 400,
      "message": "Description of the error",
      "type": "validation_error"
    }
  }
}
```

---

## Rate Limits

- **Per minute:** 60 requests (configurable via `config.toml`)
- **Per day:** 1000 requests (configurable via `config.toml`)
- **ModelMistress quota:** Model-specific limits apply

---

## ModelMistress Direct Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/chat/completions` | POST | Chat with a model |
| `/v1/completions` | POST | Text completions |
| `/v1/embeddings` | POST | Generate embeddings |
| `/v1/rerank` | POST | Rerank documents |
| `/v1/vision/classify` | POST | Image classification |
| `/v1/vision/detect` | POST | Object detection |
| `/v1/vision/embed` | POST | Image embeddings |
| `/v1/audio/transcriptions` | POST | Speech-to-text |
| `/v1/audio/speech` | POST | Text-to-speech |
| `/v1/km/load` | POST | Load knowledge module |
| `/v1/km/unload` | POST | Unload knowledge module |
| `/v1/native/traces` | GET | Traces and monitoring |
