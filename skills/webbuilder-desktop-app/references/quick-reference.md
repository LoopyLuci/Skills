# WebBuilder Desktop App — Quick Reference

## Project Structure

```
C:\Users\Server\Desktop\WebBuilder\
├── desktop_app.py       # Main PyQt5 application (1,650+ lines)
├── components.py        # Custom widgets
├── output/              # Flask backend + frontend
│   ├── app.py
│   └── index.html
└── test_integration.py  # 12 integration tests
```

## Running

```bash
cd C:\Users\Server\Desktop\WebBuilder
python desktop_app.py
```

## Providers (12 total)

### Cloud (9)
- OpenAI (GPT-4o, GPT-4o-mini, o1-preview, etc.)
- Anthropic (Claude 3.5 Sonnet, Claude 3.5 Haiku, Claude 3 Opus)
- Google AI (Gemini 1.5 Pro, Gemini 1.5 Flash)
- OpenRouter (Claude, GPT-4, Llama from 100+ models)
- Groq (LLaMA, Mixtral)
- OpenCode Zen (opencode-zen-1, opencode-zen-2)
- OpenCode Go (opencode-go-1, opencode-go-2)
- Grok/xAI (grok-2, grok-1, grok-beta)
- Nous Research (Hermes, LLaMA)

### Local (3)
- Ollama (llama3.2, llama3.1, mistral, codellama, phi3, gemma2, qwen2)
- Unsloth (llama-3-8b-Instruct optimized)
- LM Studio / LLM Studio (phi-3-mini, qwen2.5-7b)

## Key Classes

| Class | File | Purpose |
|-------|------|---------|
| `Config` | desktop_app.py | All providers, models, settings |
| `ConfigManager` | desktop_app.py | Save/load settings + API keys |
| `HTMLExporter` | desktop_app.py | Generate production HTML |
| `ModelRouter` | desktop_app.py | Route to models, sort free-first |
| `APIKeyManager` | desktop_app.py | Key management |
| `WebBuilderApp` | desktop_app.py | Main app (QMainWindow) |
| `ProviderCard` | components.py | UI card for provider |
| `ModelSelector` | components.py | Dropdown with free-first |
| `SectionWidget` | components.py | Canvas section widget |

## Testing

```bash
# Integration tests (12 tests)
cd C:\Users\Server\Desktop\WebBuilder
python test_integration.py

# Core tests (23 tests)
cd C:\Projects\WebBuilder
python -m pytest test_suite.py -v
```

## Common Commands

| Action | Command |
|--------|---------|
| Start app | `python desktop_app.py` |
| Start Flask | Auto-starts from app |
| Export HTML | Ctrl+E or Export button |
| Generate project | Ctrl+G or 🚀 Generate button |
| Configure provider | 🔑 Providers tab → click card |
| Toggle chat | Ctrl+Shift+C |
| Save | Ctrl+S |

## File Locations

| What | Path |
|------|------|
| Desktop entry | `C:\Users\Server\Desktop\WebBuilder\webbuilder_desktop.py` |
| Main window | `webbuilder\gui\__init__.py` |
| Chat window | `webbuilder\gui\chat_window.py` |
| Properties window | `webbuilder\gui\properties_window.py` |
| Terminal CLI | `webbuilder\gui\terminal_cli.py` |
| Activity log | `webbuilder\gui\activity_log.py` |
| Training dashboard | `webbuilder\gui\training_dashboard.py` |
| ML models | `webbuilder\ml_engine\models.py` |
| Self-learning | `webbuilder\ml_engine\self_learning.py` |
| Post-quantum crypto | `webbuilder\security\post_quantum.py` |
| Trait system | `webbuilder\abi.py` |
| Crash reports | `logs\crashes\` |
| Logs | `logs\app.log`, `logs\app_rotating.log` |
