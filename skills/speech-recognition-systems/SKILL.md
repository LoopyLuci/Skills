---
name: speech-recognition-systems
description: Use when building speech recognition and ASR systems.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [speech-recognition, asr, whisper, wav2vec, ctc, transducers, audio]
---

# Speech Recognition Systems

Building automatic speech recognition (ASR) systems — from acoustic models and feature extraction through end-to-end models (Whisper, wav2vec), language models, and deployment.

## When to Use

- Transcribing audio to text
- Building voice-controlled applications
- Implementing real-time captioning
- Custom ASR for domain-specific vocabulary

## ASR Pipeline

```python
ASR_APPROACHES = {
    'classical': 'Acoustic model → Language model → Decoder (WFST) — Kaldi, DeepSpeech',
    'end_to_end': 'Whisper, wav2vec 2.0 — single neural net, audio → text',
    'ctc': 'Connectionist Temporal Classification — frame-level alignment, no segment boundaries',
    'transducer': 'RNN-T — streaming-friendly, used in mobile ASR',
}

class ASRPipeline:
    def __init__(self, model_name: str = 'openai/whisper-small'):
        from transformers import pipeline
        self.asr = pipeline('automatic-speech-recognition', model=model_name)
    
    def transcribe(self, audio_path: str, language: str = 'en') -> Dict:
        result = self.asr(audio_path, generate_kwargs={'language': language})
        return {'text': result['text'], 'confidence': result.get('confidence', 0)}
```

## Verification Checklist

- [ ] ASR approach selected (end-to-end, CTC, transducer)
- [ ] Model handles target languages and accents
- [ ] Real-time streaming (if needed) with low latency
- [ ] Custom vocabulary/phrase boosting for domain terms
- [ ] Word-level timestamps for alignment
- [ ] Noise robustness tested (background, multiple speakers)
