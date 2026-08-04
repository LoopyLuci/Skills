---
name: cognitive-state-monitoring
description: "Use when monitoring cognitive states. EEG, fNIRS."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [neurotech, cognitive-monitoring, eeg, fnirs, ml]
    related_skills: [eeg-signal-processing, mental-health-monitoring]
---

# Cognitive State Monitoring

## Overview
Monitor and classify cognitive states (attention, fatigue, workload, stress) using EEG, fNIRS, and physiological signals. Combine signal processing with machine learning classification for real-time cognitive monitoring in healthcare, automotive, aviation, and workplace safety applications.

## When to Use
- "Detect driver fatigue using EEG signals"
- "Monitor pilot cognitive workload during flight"
- "Assess attention levels in classroom learning"
- "Implement real-time mental fatigue detection"
- "Monitor patient cognitive states in clinical settings"

## Physiological Signal Sources

### EEG-Based Monitoring
| Cognitive State | Frequency Band | Key Metrics | Typical Accuracy |
|-----------------|---------------|-------------|-----------------|
| Alert/Fatigue | Alpha (8-13Hz) | Alpha/Theta ratio ↑ | 85-90% |
| Attention | Beta/Alpha ratio | Beta ↑, Alpha ↓ | 80-85% |
| Workload | Theta/Beta ratio | Theta ↑ with workload | 75-85% |
| Stress | Asymmetry (L/R) | Frontal alpha asymmetry | 70-80% |

### fNIRS-Based Monitoring
| State | Channel Region | Signal | Accuracy |
|-------|---------------|--------|----------|
| Cognitive Load | DLPFC (Forehead) | Oxy-Hb increase | 80-85% |
| Mental Fatigue | Multiple regions | Oxy-Hb ↓, Deoxy-Hb ↑ | 75-80% |
| Stress | Prefrontal cortex | Asymmetry changes | 70-80% |

## Signal Processing Pipeline
```python
import numpy as np
from scipy import signal
from sklearn.ensemble import RandomForestClassifier

def cognitive_state_pipeline(eeg_data, sampling_rate=256):
    """
    Complete pipeline for cognitive state classification
    """
    # 1. Preprocessing
    clean_data = apply_filtering(eeg_data, sampling_rate)
    
    # 2. Artifact removal
    clean_data = remove_artifacts_ica(clean_data)
    
    # 3. Feature extraction
    features = extract_cognitive_features(clean_data, sampling_rate)
    
    # 4. Classification
    classifier = load_trained_model('cognitive_state_classifier.pkl')
    prediction = classifier.predict([features])
    confidence = classifier.predict_proba([features]).max()
    
    return {
        "state": prediction[0],
        "confidence": round(confidence, 3),
        "features": features
    }

def extract_cognitive_features(eeg_data, sfreq):
    """
    Extract cognitive state features from EEG
    """
    # Power spectral density in standard bands
    bands = {
        'delta': (0.5, 4), 'theta': (4, 8),
        'alpha': (8, 13), 'beta': (13, 30), 'gamma': (30, 45)
    }
    
    features = {}
    for band_name, (low, high) in bands.items():
        band_power = compute_band_power(eeg_data, sfreq, low, high)
        features[f'{band_name}_power'] = np.mean(band_power)
        
        # Frontality and asymmetry
        if band_name in ['alpha', 'beta', 'theta']:
            features[f'{band_name}_frontality'] = compute_frontality(band_power)
            features[f'{band_name}_asymmetry'] = compute_asymmetry(band_power)
    
    # Derived cognitive metrics
    features['theta_beta_ratio'] = features['theta_power'] / (features['beta_power'] + 1e-10)
    features['alpha_asymmetry'] = features['alpha_asymmetry']
    features['fatigue_index'] = (features['alpha_power'] + features['theta_power']) / features['beta_power']
    
    return features

def compute_frontality(channel_powers):
    """Compute frontal vs posterior power ratio"""
    frontal = np.mean(channel_powers['frontal_channels'])
    posterior = np.mean(channel_powers['posterior_channels'])
    return frontal / (posterior + 1e-10)
```

## Real-time Classification

### Machine Learning Approaches
```python
def train_cognitive_classifier(training_data, labels):
    """
    Train a classifier for cognitive state detection
    """
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import cross_val_score
    
    # Feature scaling
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(training_data)
    
    # Train classifier
    clf = GradientBoostingClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    )
    clf.fit(scaled_features, labels)
    
    # Cross-validation accuracy
    cv_scores = cross_val_score(clf, scaled_features, labels, cv=5)
    
    return {
        "classifier": clf,
        "scaler": scaler,
        "cv_accuracy": round(np.mean(cv_scores), 3),
        "feature_importance": dict(zip(get_feature_names(), clf.feature_importances_))
    }

# Feature importance ranking for cognitive states
FEATURE_IMPORTANCE = {
    "fatigue_detection": {
        "alpha_theta_ratio": 0.25,
        "beta_suppression": 0.20,
        "frontal_alpha": 0.15,
        "reaction_time_variability": 0.12
    },
    "attention_monitoring": {
        "beta_alpha_ratio": 0.30,
        "frontal_theta": 0.20,
        "pupil_dilation": 0.15,
        "blink_rate": 0.10
    },
    "workload_assessment": {
        "theta_beta_ratio": 0.28,
        "p300_amplitude": 0.22,
        "frontal_midline_theta": 0.18,
        "pupil_brightness": 0.12
    }
}
```

## Application Domains

### Automotive Safety
| State | Detection | Response |
|-------|-----------|----------|
| Fatigue (30% eyelid closure) | PERCLOS, EEG alpha | Alert system, seat vibration |
| Distraction (low attention) | EEG beta, eye tracking | Steering wheel feedback |
| High workload | EEG theta/beta ratio | Simplify interface |

### Healthcare Monitoring
- **ICU sedation**: EEG burst-suppression monitoring
- **Epilepsy**: Seizure prediction using spectral features
- **Dementia**: Cognitive decline tracking over time
- **Anesthesia**: Consciousness level monitoring (BIS)

### Workplace Safety
| Industry | Monitored States | Technology |
|----------|------------------|------------|
| Aviation | Pilot workload, fatigue | EEG headset |
| Manufacturing | Operator vigilance | Eye tracking + EEG |
| Transportation | Driver alertness | PERCLOS + EEG |
| Healthcare | Surgeon fatigue | EEG + eye tracking |

## Common Pitfalls
1. **Poor electrode contact** — dry electrodes have high impedance
2. **Motion artifacts** — movement corrupts EEG signals during real use
3. **Individual variability** — one model doesn't fit all users well
4. **Not validating in real environments** — lab accuracy doesn't transfer
5. **Overfitting to specific tasks** — models fail on new cognitive states
6. **Ignoring signal quality** — garbage in, garbage out
7. **Not accounting for adaptation** — users learn to "cheat" classifiers
8. **Privacy concerns** — neural data collection requires explicit consent
9. **Latency issues** — real-time monitoring needs fast processing
10. **False alarm fatigue** — too many alerts reduce effectiveness

## Verification Checklist
- [ ] EEG signal quality >10:1 SNR for target frequency bands
- [ ] Artifact rejection rate <15% during real-world use
- [ ] Classifier cross-validation accuracy >75% on unseen data
- [ ] Individual calibration (5-10 minutes) completed per user
- [ ] Real-time latency <500ms for safety-critical applications
- [ ] Battery life ≥8 hours continuous operation
- [ ] Electromagnetic interference (EMI) tested
- [ ] Privacy and consent protocols implemented
- [ ] False positive/negative rates <10% in field testing
- [ ] User comfort and wearability validated