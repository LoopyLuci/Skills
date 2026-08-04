---
name: eeg-signal-processing
description: "Use when processing EEG signals. Preprocessing, FFT."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [neurotech, eeg, signal-processing, preprocessing, spectral-analysis]
    related_skills: [neural-interface-design, neurofeedback-analysis]
---

# EEG Signal Processing

## Overview
Process EEG signals for brain-computer interfaces (BCIs), neurofeedback, clinical diagnostics, and cognitive state monitoring. Covers signal preprocessing, artifact removal, spectral analysis, and feature extraction from EEG data.

## When to Use
- "Preprocess EEG signals for BCI applications"
- "Remove artifacts from EEG recordings"
- "Analyze EEG power spectra for cognitive states"
- "Extract features for machine learning classification"
- "Detect event-related potentials in EEG"

## Signal Preprocessing Pipeline

### 1. Noise Reduction
```python
import numpy as np
from scipy import signal
import mne

def preprocess_eeg(raw_eeg, sfreq=256):
    """
    Standard EEG preprocessing pipeline
    
    Args:
        raw_eeg: raw EEG data (channels × samples)
        sfreq: sampling frequency (default 256 Hz)
    
    Returns:
        Preprocessed clean EEG data
    """
    # 1. Notch filter (50/60 Hz mains interference)
    notch_freq = 60 if abs(sfreq - 256) < 8 else 50
    clean_data = apply_notch_filter(raw_eeg, notch_freq, sfreq)
    
    # 2. Bandpass filter (0.5-50 Hz)
    clean_data = apply_bandpass_filter(clean_data, 0.5, 50, sfreq)
    
    # 3. Re-reference to average (reduces common-mode noise)
    clean_data = clean_data - np.mean(clean_data, axis=0)
    
    # 4. Artifact removal (ICA)
    clean_data = remove_artifacts_ica(clean_data)
    
    return clean_data

def apply_notch_filter(data, freq, sfreq, quality=30):
    """Apply notch filter at power line frequency"""
    nyquist = sfreq / 2
    w0 = freq / nyquist
    b, a = signal.iirnotch(w0, quality)
    return signal.filtfilt(b, a, data, axis=1)

def apply_bandpass_filter(data, low_freq, high_freq, sfreq):
    """Apply Butterworth bandpass filter"""
    nyquist = sfreq / 2
    low = low_freq / nyquist
    high = high_freq / nyquist
    b, a = signal.butter(4, [low, high], btype='band')
    return signal.filtfilt(b, a, data, axis=1)
```

### 2. Artifact Removal
| Artifact Type | Frequency Range | Removal Method |
|---------------|----------------|----------------|
| Ocular (blinks, eye movement) | 0.1-10 Hz | ICA, regression |
| Muscle (EMG) | 20-100 Hz | ICA, high-pass filter |
| Cardiac (ECG) | 1-3 Hz | ICA, template removal |
| Line noise | 50/60 Hz | Notch filter |
| Motion artifacts | Broadband | Acceleration correction |

### ICA Artifact Removal
```python
def remove_artifacts_ica(eeg_data, n_components='auto'):
    """
    Independent Component Analysis for artifact removal
    """
    from sklearn.decomposition import FastICA
    
    if n_components == 'auto':
        n_components = min(eeg_data.shape[1] // 3, eeg_data.shape[0])
    
    ica = FastICA(n_components=n_components, random_state=42)
    ica_components = ica.fit_transform(eeg_data.T).T
    
    # Identify artifact components
    artifact_indices = identify_artifactual_components(ica_components, eeg_data)
    
    # Remove artifact components
    clean_components = np.delete(ica_components, artifact_indices, axis=0)
    cleaned_eeg = ica.mixing_ @ ica_components
    
    return cleaned_eeg, artifact_indices

def identify_artifactual_components(components, eeg_data):
    """
    Auto-detect artifacts using variance and spatial patterns
    """
    artifacts = []
    for i, component in enumerate(components):
        # Eye blink components have frontal maximum
        frontal_power = np.var(component[:5])
        total_power = np.var(component)
        if frontal_power / total_power > 0.5:
            artifacts.append(i)
    return artifacts
```

## Spectral Analysis & Feature Extraction
```python
def extract_psd_features(eeg_data, sfreq):
    """
    Extract EEG power spectral density features
    """
    from scipy.signal import welch
    
    nperseg = min(sfreq * 4, eeg_data.shape[1])
    freqs, psd = welch(eeg_data, sfreq, nperseg=nperseg, axis=1)
    
    # Standard EEG bands
    bands = {
        'delta': (0.5, 4),    # Deep sleep
        'theta': (4, 8),      # Memory, meditation
        'alpha': (8, 13),     # Relaxed attention
        'beta': (13, 30),     # Active thinking
        'gamma': (30, 45)     # High-level processing
    }
    
    features = {}
    for band_name, (low, high) in bands.items():
        band_mask = (freqs >= low) & (freqs <= high)
        band_power = np.mean(psd[band_mask, :], axis=0)
        features[f'{band_name}_power'] = np.mean(band_power)
    
    return features

# Example: Alpha asymmetry for emotional state
def alpha_asymmetry(eeg_data, sfreq):
    """
    Left > Right frontal alpha = approach motivation
    Right > Left = withdrawal avoidance
    """
    features = extract_psd_features(eeg_data, sfreq)
    left_frontal_alpha = features['alpha_power'][:3]
    right_frontal_alpha = features['alpha_power'][3:6]
    
    alpha_asymmetry_index = (np.log(left_frontal_alpha.mean()) - 
                            np.log(right_frontal_alpha.mean()))
    
    return {
        "asymmetry_index": round(alpha_asymmetry_index, 4),
        "interpretation": "approach" if alpha_asymmetry_index > 0 else "withdrawal"
    }
```

## Common Pitfalls
1. **Notch filter at wrong frequency** — mains varies by country
2. **Over-filtering** — removing real neural signals
3. **Not removing artifacts** — blink/muscle dominate results
4. **Wrong ICA rejection thresholds** — removing neural signals
5. **Not checking channel quality** — bad electrodes corrupt analysis
6. **Incorrect power band boundaries** — varies by field
7. **No consistent referencing** — affects signal morphology
8. **Insufficient downsampling** — oversampled data wastes compute
9. **Not validating preprocessing** — no quality metrics
10. **Ignoring individual differences** — one-size-fits-all

## Verification Checklist
- [ ] Notch filter frequency confirmed (50/60 Hz)
- [ ] Bandpass filter removes artifacts without distorting
- [ ] ICA components validated manually
- [ ] EEG quality checked (impedance <5kΩ)
- [ ] Power band analysis validated against baselines
- [ ] Artifact rejection rate <15%
- [ ] Referencing consistent (average/Cz/Pz)
- [ ] Pre/post comparison shows artifact reduction
- [ ] Sampling rate ≥256 Hz
- [ ] Results reproducible across sessions