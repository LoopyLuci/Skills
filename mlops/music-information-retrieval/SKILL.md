---
name: music-information-retrieval
description: "Use when implementing music information retrieval."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [music-IR, MIR, audio-analysis, chord-detection, tempo, genre-classification, music-recommendation]
    related_skills: [audio-processing-deep-learning, speech-recognition-systems, timeseries-foundation-models, recommender-systems-building]
---

# Music Information Retrieval

Implementing music information retrieval (MIR) — from feature extraction (chroma, tempo, beat tracking) through genre classification, chord detection, and music recommendation.

## When to Use

- Analyzing musical audio (tempo, key, chords, beats)
- Building music recommendation systems
- Automatic music transcription
- Music similarity search
- Playlist generation

## MIR Features

```python
class MIRFeatureExtractor:
    """Extract musical features from audio."""
    
    @staticmethod
    def chroma_features(waveform, sr: int = 22050) -> np.array:
        """Chroma (pitch class) features — 12-bin per octave."""
        import librosa
        return librosa.feature.chroma_stft(y=waveform, sr=sr)
    
    @staticmethod
    def beat_tracking(waveform, sr: int = 22050) -> Dict:
        import librosa
        tempo, beats = librosa.beat.beat_track(y=waveform, sr=sr)
        return {'tempo_bpm': round(tempo, 1), 'n_beats': len(beats)}
    
    @staticmethod
    def spectral_features(waveform, sr: int = 22050) -> Dict:
        import librosa
        return {
            'centroid': float(librosa.feature.spectral_centroid(y=waveform, sr=sr).mean()),
            'bandwidth': float(librosa.feature.spectral_bandwidth(y=waveform, sr=sr).mean()),
            'rolloff': float(librosa.feature.spectral_rolloff(y=waveform, sr=sr).mean()),
            'zcr': float(librosa.feature.zero_crossing_rate(waveform).mean()),
        }
```

## Verification Checklist

- [ ] Audio format standardized (sample rate, channels, duration)
- [ ] Feature extraction (chroma, tempo, spectral, MFCC) working
- [ ] Beat tracking accuracy tested on varied genres
- [ ] Key/chord detection validated against labeled dataset
- [ ] Genre classification accuracy benchmarked
- [ ] Music similarity metric defined and tested
- [ ] Real-time processing for interactive applications
