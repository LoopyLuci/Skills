# ModelMistress Direct API Endpoints Reference

Full reference for ModelMistress API endpoints. Used by ItemForge and the e-commerce-photo-workflow skill.

---

## Chat & Completions

### `/v1/chat/completions`

Chat with a model (JSON format).

```bash
curl -X POST http://127.0.0.1:12345/v1/chat/completions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.5:9b",
    "messages": [
      {"role": "user", "content": "Research this product..."}
    ]
  }'
```

### `/v1/completions`

Text completions (legacy).

```bash
curl -X POST http://127.0.0.1:12345/v1/completions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.5:9b",
    "prompt": "Research this product...",
    "max_tokens": 1000
  }'
```

---

## Vision

### `/v1/vision/classify`

Image classification.

```bash
curl -X POST http://127.0.0.1:12345/v1/vision/classify \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "image": "data:image/jpeg;base64,..."
  }'
```

### `/v1/vision/detect`

Object detection with bounding boxes.

```bash
curl -X POST http://127.0.0.1:12345/v1/vision/detect \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "image": "data:image/jpeg;base64,..."
  }'
```

### `/v1/vision/embed`

Image embeddings for similarity search.

```bash
curl -X POST http://127.0.0.1:12345/v1/vision/embed \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "image": "data:image/jpeg;base64,..."
  }'
```

---

## Embeddings & Reranking

### `/v1/embeddings`

Generate text embeddings.

```bash
curl -X POST http://127.0.0.1:12345/v1/embeddings \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nomic-embed-text-v1.5",
    "input": "Research this item..."
  }'
```

### `/v1/rerank`

Rerank documents by relevance.

```bash
curl -X POST http://127.0.0.1:12345/v1/rerank \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "rerank-model",
    "query": "vintage wine glasses",
    "documents": ["doc1", "doc2", "doc3"]
  }'
```

---

## Audio

### `/v1/audio/transcriptions`

Speech-to-text.

```bash
curl -X POST http://127.0.0.1:12345/v1/audio/transcriptions \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@audio.wav" \
  -F "model=whisper"
```

### `/v1/audio/speech`

Text-to-speech.

```bash
curl -X POST http://127.0.0.1:12345/v1/audio/speech \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-tts",
    "input": "Hello, this is a product description.",
    "voice": "default"
  }'
```

---

## Knowledge Modules

### `/v1/km/load`

Load a knowledge module.

```bash
curl -X POST http://127.0.0.1:12345/v1/km/load \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ecommerce-best-practices",
    "version": "1.0.0"
  }'
```

### `/v1/km/unload`

Unload a knowledge module.

```bash
curl -X POST http://127.0.0.1:12345/v1/km/unload \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ecommerce-best-practices"
  }'
```

---

## Observability

### `/v1/native/traces`

Get traces and monitoring data.

```bash
curl http://127.0.0.1:12345/v1/native/traces \
  -H "Authorization: Bearer $TOKEN"
```
