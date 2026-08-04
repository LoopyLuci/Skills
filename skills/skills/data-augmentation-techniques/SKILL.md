---
name: data-augmentation-techniques
description: "Use when applying data augmentation for vision, text, audio."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [data-augmentation, computer-vision, nlp, audio, deep-learning]
    related_skills: [computer-vision-techniques, nlp-techniques, self-supervised-learning, custom-training-loops]
---

# Data Augmentation Techniques

Data augmentation strategies for vision, text, and audio — from basic transformations through learned augmentations and generative methods.

## When to Use

- Small dataset that needs to be expanded (few hundred to few thousand examples)
- Improving model generalization and reducing overfitting
- Building robustness to real-world variations (lighting, noise, occlusions)
- Creating synthetic training data for rare scenarios
- Balancing class distributions by augmenting minority classes

## Image Augmentation

### Basic Transforms

```python
import torchvision.transforms as T
import torchvision.transforms.functional as F
import random

class ImageAugmentation:
    """Standard image augmentations for computer vision."""
    
    @staticmethod
    def train_transform(img_size=224):
        """Typical ImageNet-style training augmentation."""
        return T.Compose([
            T.RandomResizedCrop(img_size, scale=(0.08, 1.0)),
            T.RandomHorizontalFlip(p=0.5),
            T.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
            T.RandomGrayscale(p=0.1),
            T.RandomApply([T.GaussianBlur(kernel_size=3)], p=0.2),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
    
    @staticmethod
    def strong_augment(img_size=224):
        """Stronger augmentation for small datasets."""
        return T.Compose([
            T.RandomResizedCrop(img_size),
            T.RandomHorizontalFlip(),
            T.RandomApply([T.ColorJitter(0.4, 0.4, 0.4, 0.1)], p=0.8),
            T.RandomGrayscale(p=0.2),
            T.RandomApply([T.GaussianBlur(kernel_size=3)], p=0.5),
            T.RandomApply([T.RandomRotation(30)], p=0.3),
            T.RandomAffine(degrees=0, translate=(0.1, 0.1), scale=(0.9, 1.1)),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
```

### Advanced Augmentations

```python
import albumentations as A
import cv2
import numpy as np

class AdvancedImageAug:
    """Albumentations-based augmentations with spatial-level transforms."""
    
    @classmethod
    def segmentation_aug(cls):
        """Augmentations that preserve pixel-level labels."""
        return A.Compose([
            A.RandomResizedCrop(512, 512, scale=(0.5, 1.0)),
            A.HorizontalFlip(p=0.5),
            A.OneOf([
                A.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
                A.HueSaturationValue(hue_shift_limit=20, sat_shift_limit=30),
                A.RGBShift(r_shift_limit=20, g_shift_limit=20, b_shift_limit=20),
            ], p=0.8),
            A.OneOf([
                A.GaussianBlur(blur_limit=(3, 7)),
                A.MotionBlur(blur_limit=7),
                A.MedianBlur(blur_limit=5),
            ], p=0.3),
            A.OneOf([
                A.GridDistortion(num_steps=5, distort_limit=0.3),
                A.ElasticTransform(alpha=1, sigma=50, alpha_affine=50),
                A.OpticalDistortion(distort_limit=0.3),
            ], p=0.3),
            A.CoarseDropout(max_holes=8, max_height=32, max_width=32, p=0.3),
        ], additional_targets={'mask': 'mask'})
    
    @classmethod
    def cutmix(cls, images, targets, alpha=1.0):
        """CutMix: mix two images by cutting and pasting patches."""
        batch_size = images.shape[0]
        indices = torch.randperm(batch_size)
        
        lam = np.random.beta(alpha, alpha)
        bbx1, bby1, bbx2, bby2 = rand_bbox(images.shape, lam)
        
        mixed_images = images.clone()
        mixed_images[:, :, bbx1:bbx2, bby1:bby2] = images[indices, :, bbx1:bbx2, bby1:bby2]
        lam = 1 - ((bbx2 - bbx1) * (bby2 - bby1) / (images.shape[-1] * images.shape[-2]))
        
        return mixed_images, targets, targets[indices], lam
```

### MixUp

```python
def mixup(images, targets, alpha=0.2):
    """MixUp: convex combination of images and labels."""
    lam = np.random.beta(alpha, alpha)
    batch_size = images.shape[0]
    indices = torch.randperm(batch_size)
    
    mixed_images = lam * images + (1 - lam) * images[indices]
    mixed_targets = (targets, targets[indices], lam)
    
    return mixed_images, mixed_targets
```

## Text Augmentation

```python
import random
import nltk
from nltk.corpus import wordnet

class TextAugmentation:
    """Text augmentation techniques for NLP."""
    
    @staticmethod
    def synonym_replacement(text, n=2):
        """Replace n words with their synonyms."""
        words = text.split()
        new_words = words.copy()
        
        # Choose random words that have synonyms
        candidates = [i for i, w in enumerate(words) if 
                     wordnet.synsets(w) and w.isalpha()]
        random.shuffle(candidates)
        
        replaced = 0
        for idx in candidates:
            if replaced >= n:
                break
            synonyms = wordnet.synsets(words[idx])
            if synonyms:
                lemma = random.choice(synonyms).lemmas()[0].name()
                if lemma != words[idx]:
                    new_words[idx] = lemma.replace('_', ' ')
                    replaced += 1
        
        return ' '.join(new_words)
    
    @staticmethod
    def random_insertion(text, n=1):
        """Insert random synonyms of existing words."""
        words = text.split()
        for _ in range(n):
            word = random.choice(words)
            synsets = wordnet.synsets(word)
            if synsets:
                synonym = random.choice(synsets).lemmas()[0].name()
                pos = random.randint(0, len(words))
                words.insert(pos, synonym.replace('_', ' '))
        return ' '.join(words)
    
    @staticmethod
    def random_swap(text, n=2):
        """Swap random pairs of words."""
        words = text.split()
        for _ in range(n):
            i, j = random.sample(range(len(words)), 2)
            words[i], words[j] = words[j], words[i]
        return ' '.join(words)
    
    @staticmethod
    def back_translate(text, source_lang='en', target_lang='fr'):
        """Translate text to another language and back.
        Produces more natural variations than word-level methods."""
        # Uses a translation model (e.g., MarianMT)
        from transformers import MarianMTModel, MarianTokenizer
        
        model_name = f'Helsinki-NLP/opus-mt-{source_lang}-{target_lang}'
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        
        # Translate to target language
        inputs = tokenizer(text, return_tensors="pt", padding=True)
        translated = model.generate(**inputs)
        target_text = tokenizer.decode(translated[0], skip_special_tokens=True)
        
        # Translate back to source language
        back_model = f'Helsinki-NLP/opus-mt-{target_lang}-{source_lang}'
        back_tokenizer = MarianTokenizer.from_pretrained(back_model)
        back_model = MarianMTModel.from_pretrained(back_model)
        
        inputs = back_tokenizer(target_text, return_tensors="pt", padding=True)
        back_translated = back_model.generate(**inputs)
        return back_tokenizer.decode(back_translated[0], skip_special_tokens=True)
```

## Audio Augmentation

```python
import torchaudio
import torch
import numpy as np

class AudioAugmentation:
    """Audio augmentations for speech/music models."""
    
    @staticmethod
    def add_noise(waveform, noise_level=0.005):
        """Add gaussian noise."""
        noise = torch.randn_like(waveform) * noise_level
        return waveform + noise
    
    @staticmethod
    def time_stretch(waveform, rate=1.1):
        """Stretch time without changing pitch."""
        # Requires torchaudio's sox effects
        effects = [
            ['tempo', f'{rate}'],
        ]
        augmented, _ = torchaudio.sox_effects.apply_effects_tensor(
            waveform, 16000, effects
        )
        return augmented
    
    @staticmethod
    def pitch_shift(waveform, sample_rate=16000, n_steps=2):
        """Shift pitch up or down."""
        effects = [
            ['pitch', f'{n_steps*100}'],  # cents
            ['rate', f'{sample_rate}'],
        ]
        augmented, _ = torchaudio.sox_effects.apply_effects_tensor(
            waveform, sample_rate, effects
        )
        return augmented
    
    @staticmethod
    def spec_augment(mel_spec, freq_mask_param=15, time_mask_param=30):
        """SpecAugment: mask frequency and time bands.
        Standard augmentation for ASR models."""
        from torchaudio.transforms import FrequencyMasking, TimeMasking
        
        freq_masking = FrequencyMasking(freq_mask_param)
        time_masking = TimeMasking(time_mask_param)
        
        augmented = freq_masking(mel_spec)
        augmented = time_masking(augmented)
        
        return augmented
```

## Common Pitfalls

1. **Test-time augmentation mismatch** — applying augments at test time that hurt accuracy; always validate
2. **Label-preserving vs altering** — some augments change the label (e.g., 6→9 rotation); avoid or handle
3. **Compute cost** — heavy augments slow training significantly; use on-the-fly GPU augmentation
4. **Domain-inappropriate augments** — medical images shouldn't be horizontally flipped (left/right matters)
5. **Over-augmenting small datasets** — too much augmentation distorts beyond recognition; use progressive strength
6. **Augmentation not matching deployment** — training with Gaussian blur when deployment has motion blur won't help

## Verification Checklist

- [ ] Augmentations preserve label information (or label is adjusted accordingly)
- [ ] Augmented samples visually/audibly look realistic
- [ ] Validation accuracy improvement > 1% over baseline without augmentation
- [ ] Training throughput acceptable with augmentation overhead
- [ ] Test-time augmentation (TTA) evaluated separately
- [ ] Domain-specific constraints respected (medical, satellite, etc.)

## See Also

- computer-vision-techniques — vision-specific augmentation
- nlp-techniques — text augmentation for NLP
- self-supervised-learning — using augmentation for SSL
- custom-training-loops — integrating augmentation into training
