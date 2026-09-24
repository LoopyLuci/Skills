---
name: text-to-speech-engines
description: Use when building text-to-speech and voice synthesis.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [tts, text-to-speech, voice-synthesis, bark, coqui, tacotron, voice-cloning]
---

# Text-to-Speech Engines

Building text-to-speech — from classical parametric TTS through neural models (Tacotron, FastSpeech, Bark), voice cloning, and expressive speech synthesis.

## When to Use

- Adding voice output to applications
- Building accessibility features (screen readers)
- Creating voice assistants and conversational AI
- Generating audio content at scale

## TTS Methods

```python
TTS_METHODS = {
    'concatenative': 'Unit selection from recorded audio database — natural but limited',
    'parametric': 'Vocoder-based (WaveNet, HiFi-GAN) — flexible, controllable',
    'end_to_end': 'Tacotron/FastSpeech — text → spectrogram → vocoder → audio',
    'zero_shot_cloning': 'Bark, Coqui XTTS — clone voice from 3-second sample',
}

class TTSGenerator:
    def __init__(self, model: str = 'tts_models/en/ljspeech/tacotron2-DDC'):
        from TTS.api import TTS
        self.tts = TTS(model)
    
    def generate(self, text: str, speaker_wav: str = None, 
                 output_path: str = 'output.wav'):
        self.tts.tts_to_file(text=text, file_path=output_path, 
                            speaker_wav=speaker_wav)
        return output_path
```

## Verification Checklist

- [ ] TTS model selected (concatenative, parametric, end-to-end, or zero-shot)
- [ ] Voice quality natural (MOS score > 4.0 target)
- [ ] Latency acceptable for use case (real-time < 500ms)
- [ ] Voice cloning quality with minimal samples
- [ ] Emotion/prosody control (if needed)
- [ ] Multi-language support (if needed)
- [ ] GPU vs CPU inference benchmarked
