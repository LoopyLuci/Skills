---
name: audio-processing-deep-learning
description: "Use when applying deep learning to audio processing."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [audio-processing, deep-learning, spectrogram, mel, STFT, audio-classification]
    related_skills: [speech-recognition-systems, text-to-speech-engines, music-information-retrieval, multi-modal-models-vision-language]
---

# Audio Processing with Deep Learning

Applying deep learning to audio — from spectrograms and mel-frequency features through audio classification, source separation, and audio generation.

## When to Use

- Classifying audio (speech, music, environmental sounds)
- Separating audio sources (vocals from instruments)
- Audio generation and enhancement
- Feature extraction for audio ML pipelines

## Audio Feature Pipeline

```python
import torch
import torchaudio
import torchaudio.functional as F

class AudioProcessor:
    """Extract features from audio for deep learning."""
    
    @staticmethod
    def mel_spectrogram(waveform: torch.Tensor, sample_rate: int = 16000) -> torch.Tensor:
        mel = torchaudio.transforms.MelSpectrogram(
            sample_rate=sample_rate,
            n_fft=1024, hop_length=512, n_mels=128,
        )
        spec = mel(waveform)
        return torchaudio.transforms.AmplitudeToDB()(spec)
    
    @staticmethod
    def mfcc(waveform: torch.Tensor, sample_rate: int = 16000, n_mfcc: int = 13):
        mfcc = torchaudio.transforms.MFCC(sample_rate, n_mfcc=n_mfcc)
        return mfcc(waveform)

class AudioClassifier(nn.Module):
    """CNN for audio classification on mel-spectrograms."""
    def __init__(self, n_classes: int, n_mels: int = 128):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=2)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=2)
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(64, n_classes)
    
    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = self.pool(x).squeeze(-1).squeeze(-1)
        return self.fc(x)
```

## Verification Checklist

- [ ] Audio format standardized (sample rate, channels, bit depth)
- [ ] Feature extraction (mel-spectrogram, MFCC) tested
- [ ] Data augmentation (speed, pitch, noise, SpecAugment)
- [ ] Model architecture suitable for audio (CNN, CRNN, Transformer)
- [ ] Audio classification/regression metrics (accuracy, MSE, MOS)
- [ ] Real-time inference latency benchmarked
