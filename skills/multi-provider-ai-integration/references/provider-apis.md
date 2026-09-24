# Provider API Reference

## OpenAI

- **Models endpoint**: `GET https://api.openai.com/v1/models`
- **Auth**: `Authorization: Bearer {api_key}`
- **Response**: `{"data": [{"id": "...", "object": "model", ...}]}`
- **Chat endpoint**: `POST https://api.openai.com/v1/chat/completions`
- **Streaming**: SSE with `data: {...}` lines, ends with `data: [DONE]`

## Anthropic

- **Models endpoint**: `GET https://api.anthropic.com/v1/models`
- **Auth**: `x-api-key: {api_key}` + `anthropic-version: 2023-06-01`
- **Response**: `{"data": [{"id": "...", "display_name": "..."}]}`
- **Chat endpoint**: `POST https://api.anthropic.com/v1/messages`
- **Streaming**: SSE with `event: content_block_delta` + `data: {...}`

## OpenRouter

- **Models endpoint**: `GET https://openrouter.ai/api/v1/models?limit=500`
- **Auth**: `Authorization: Bearer {api_key}`
- **Response**: `{"data": [{"id": "...", "name": "...", "pricing": {"prompt": "...", "completion": "..."}, "context_length": ...}]}`
- **Chat endpoint**: `POST https://openrouter.ai/api/v1/chat/completions`
- **Streaming**: Same as OpenAI (OpenAI-compatible)
- **Free detection**: `pricing.prompt == 0 && pricing.completion == 0`

## xAI Grok

- **Models endpoint**: `GET https://api.x.ai/v1/models`
- **Auth**: `Authorization: Bearer {api_key}`
- **Response**: `{"data": [{"id": "..."}]}`
- **Chat endpoint**: `POST https://api.x.ai/v1/chat/completions`
- **Streaming**: Same as OpenAI (OpenAI-compatible)

## Nous Research

- **Models endpoint**: `GET https://inference-api.nousresearch.com/v1/models`
- **Auth**: `Authorization: Bearer {api_key}`
- **Response**: `{"data": [{"id": "..."}]}`
- **Chat endpoint**: `POST https://inference-api.nousresearch.com/v1/chat/completions`
- **Streaming**: Same as OpenAI (OpenAI-compatible)
- **Note**: All models are free when using Nous API key

## Ollama (Local)

- **Models endpoint**: `GET http://localhost:11434/api/tags`
- **Auth**: None
- **Response**: `{"models": [{"name": "...", "size": ..., "details": {...}}]}`
- **Chat endpoint**: `POST http://localhost:11434/api/chat`
- **Streaming**: NDJSON (one JSON object per line)
- **Note**: No API key needed, runs locally

## LM Studio (Local)

- **Models endpoint**: `GET http://localhost:1234/v1/models`
- **Auth**: None
- **Response**: `{"data": [{"id": "..."}]}` (OpenAI-compatible)
- **Chat endpoint**: `POST http://localhost:1234/v1/chat/completions`
- **Streaming**: Same as OpenAI (OpenAI-compatible)
- **Note**: No API key needed, runs locally

## Error Handling

All providers should handle:
- Network errors (connection refused, timeout)
- HTTP errors (401 Unauthorized, 403 Forbidden, 429 Rate Limited, 500 Server Error)
- Malformed JSON responses
- Empty model lists

```python
try:
    async with session.get(url, headers=headers, timeout=30) as resp:
        if resp.status == 401:
            logger.warning(f"Invalid API key for {provider}")
            return []
        if resp.status == 429:
            logger.warning(f"Rate limited by {provider}")
            return []
        if resp.status != 200:
            logger.warning(f"{provider} returned {resp.status}")
            return []
        data = await resp.json()
except aiohttp.ClientError as e:
    logger.error(f"Network error for {provider}: {e}")
    return []
except Exception as e:
    logger.error(f"Unexpected error for {provider}: {e}")
    return []
```

## Caching

```python
from datetime import datetime, timedelta

class BaseProvider(ABC):
    _models_cache: list[ModelInfo] = []
    _cache_time: Optional[datetime] = None
    _cache_ttl = timedelta(minutes=30)
    
    def has_cached_models(self) -> bool:
        if not self._models_cache or not self._cache_time:
            return False
        return datetime.now() - self._cache_time < self._cache_ttl
    
    async def fetch_models(self) -> list[ModelInfo]:
        if self.has_cached_models():
            return self._models_cache
        models = await self._fetch_models_impl()
        self._models_cache = models
        self._cache_time = datetime.now()
        return models
    
    def clear_cache(self):
        self._models_cache = []
        self._cache_time = None
```

## Free Model Detection

Different providers expose free status differently:

| Provider | Free Detection Method |
|----------|----------------------|
| OpenAI | Model ID matching (`gpt-4o-mini`, `gpt-3.5-turbo`) |
| Anthropic | Model ID matching (`claude-3-5-haiku-*`) |
| OpenRouter | `pricing.prompt == 0` (from API response) |
| xAI | Model ID matching (rarely free) |
| Nous | All models free with Nous key |
| Ollama | All models free (local) |
| LM Studio | All models free (local) |
