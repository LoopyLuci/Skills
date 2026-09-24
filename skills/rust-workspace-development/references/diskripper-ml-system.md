# ML Content Identification System

DiskRipper includes a comprehensive ML system for identifying and organizing ripped content. This is a **custom, self-learning system** — not just API wrappers.

## ML Module Structure

```
diskripper-core/src/ml/
├── pipeline.rs              # Main orchestrator (audio/video identification)
├── audio_fingerprint.rs     # Custom audio fingerprinting (AcoustID replacement)
├── music_identification.rs  # Hybrid music ID with confidence scoring
├── video_fingerprint.rs     # Video perceptual hashing + temporal fingerprinting
├── content_classifier.rs    # Genre/type classification
├── hybrid_identifier.rs     # Multi-signal identification with confidence
├── self_learning.rs         # User feedback → training batches → model updates
├── data_management.rs       # Training data collection + augmentation
├── model_versioning.rs      # Model versioning, rollback, A/B testing
├── inference.rs             # Neural network inference (MLP/CNN)
├── training.rs              # Backpropagation training loop
├── feature_extraction.rs    # MFCCs, chroma, spectral features, video features
└── organizer.rs             # Auto-organize ripped content
```

## Audio Fingerprinting (AcoustID Replacement)

Custom fingerprinting that works entirely locally:

```rust
pub struct AudioFingerprinter {
    fingerprint_db: HashMap<u64, KnownFingerprint>,
    model_dir: PathBuf,
}

impl AudioFingerprinter {
    pub fn generate(&self, audio_data: &[i16], sample_rate: u32) -> Result<AudioFingerprint, DiskRipperError> {
        // 1. Compute spectrogram via FFT
        // 2. Find spectral peaks (local maxima)
        // 3. Create combinatorial hash from peak pairs
    }
    
    pub fn match_fingerprint(&self, fingerprint: &AudioFingerprint) -> Option<FingerprintMatch> {
        // Jaccard similarity + duration-aware confidence
    }
}
```

**Key design decisions:**
- Spectral peaks stored as (frequency, time) tuples
- Combinatorial hashing for compact fingerprints
- Jaccard similarity for matching
- Duration similarity weighted into confidence score

## Training Pipeline

Full backpropagation training with:

```rust
pub struct Trainer {
    config: TrainingConfig,
    model_dir: PathBuf,
}

impl Trainer {
    pub fn train(&self, model: &mut NeuralNetwork, dataset: &Dataset) -> Result<TrainingHistory, DiskRipperError> {
        // Mini-batch gradient descent
        // Backpropagation with cross-entropy loss
        // Validation and early stopping
        // Model checkpointing (best model saved)
    }
}
```

**Training features:**
- Configurable learning rate, batch size, epochs
- Early stopping with patience
- Best model checkpointing
- Training history serialization

## Self-Learning from User Feedback

The system improves from user corrections:

```rust
pub struct SelfLearning {
    model_dir: PathBuf,
    feedback_dir: PathBuf,
}

impl SelfLearning {
    pub fn load_unused_feedback(&self) -> Result<Vec<FeedbackEntry>, DiskRipperError> {
        // Load feedback not yet used for training
    }
    
    pub fn create_training_batch(&self) -> Result<Option<TrainingBatch>, DiskRipperError> {
        // Create batch when >= 10 unused feedback entries exist
    }
    
    pub fn update_accuracy(&self, model_name: &str, correct: bool) -> Result<(), DiskRipperError> {
        // Track prediction accuracy over time
    }
}
```

## Feature Extraction

Audio features extracted for ML models:
- MFCCs (13 coefficients, simplified mel-scale)
- Chroma (12 pitch classes)
- Spectral features (8 frequency bands)
- Zero-crossing rate
- RMS energy
- Basic statistics (mean, std, min, max)

Video features:
- Average brightness per frame
- Scene change detection (frame differences)
- Color histograms (8 bins per channel)
- Motion estimation

## Smart Content Organization

Automatic folder structure based on ML identification:

```
Music/Artist/Album/Track.ext
Movies/Title (Year)/Title.ext
TV Shows/Title/Title.ext
Software/Title/Title.ext
Games/Title/Title.ext
Other/Title.ext
```

Plus NFO file generation for media center compatibility.

## Model Versioning

```rust
pub struct ModelVersioning {
    model_dir: PathBuf,
}

impl ModelVersioning {
    pub fn save_version(&self, name: &str, version: &str, accuracy: f64, training_samples: usize) -> Result<(), DiskRipperError> {
        // Save model version with metadata
    }
    
    pub fn rollback(&self, name: &str, version: &str) -> Result<(), DiskRipperError> {
        // Rollback to previous version
    }
}
```

## Hybrid Identification Strategy

The system combines multiple signals for maximum accuracy:

1. **Audio fingerprinting** (local, no network needed)
2. **Content classification** (genre, type detection)
3. **Metadata lookup** (when network available)
4. **User feedback** (corrections improve future predictions)

Each signal has a confidence score; the highest-confidence result is used.

## User Preference: Build, Don't Just Integrate

**Critical learning from session:** When the user asks for ML models, they want **custom-built models with training pipelines** — not just API wrappers around AcoustID/MusicBrainz/TMDB.

**Correct approach:**
- Build custom audio fingerprinting (AcoustID replacement)
- Build neural network inference engine
- Build training pipeline with backpropagation
- Build self-learning from user feedback
- Build smart organization
- Use APIs only as fallback/enhancement, not primary

**Anti-pattern that triggers user frustration:**
- "Let's integrate AcoustID API" — NO
- "Let's use MusicBrainz lookup" — NO (unless as fallback)
- "Let's train a model on real data" — YES
- "Let's build a self-learning pipeline" — YES

## Dependencies Added

```toml
# Cargo.toml
rand = "0.8"        # Xavier weight initialization, random sampling
fastrand = "2.0"    # Efficient shuffling for training data
```

## References

- `references/diskripper-workspace-patterns.md` — DiskRipper-specific patterns
- `references/windows-toolchain-fixes.md` — concrete error codes and fixes
- `references/tauri2-schema.md` — Tauri 2 config field mapping
- `references/git-windows-init.md` — non-interactive git initialization
- `references/frontend-ipc-wiring.md` — React/Tauri IPC wiring
