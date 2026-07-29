---
name: multi-modal-models-vision-language
description: "Use when building multi-modal vision-language AI models."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [multi-modal, vision-language, VLM, CLIP, image-captioning, visual-qa]
    related_skills: [custom-neural-architecture-design, computer-vision-techniques, nlp-techniques, transformer-architectures]
---

# Multi-Modal Vision-Language Models

Building multi-modal AI models that process both images and text — from CLIP-style embeddings through image captioning, visual question answering, and multimodal generation.

## When to Use

- Building models that understand both images and text
- Implementing image captioning or visual Q&A
- Creating text-to-image or image-to-text systems
- Building multimodal search (search images by text)
- Training vision-language models for accessibility or content moderation

## Architecture Overview

```python
MODALITY_ENCODERS = {
    'vision': ['ViT', 'ResNet', 'ConvNeXt', 'SigLIP'],
    'text': ['BERT', 'RoBERTa', 'T5', 'LLaMA', 'Gemma'],
    'fusion': ['Cross-attention', 'Co-attention', 'Concat projection', 'Q-Former'],
}
```

## CLIP-Style Dual Encoder

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class CLIPModel(nn.Module):
    """Dual-encoder vision-language model (CLIP-style).
    
    Encodes images and text into shared embedding space.
    Contrastive loss aligns matched pairs."""
    
    def __init__(self, image_encoder, text_encoder, embed_dim=512, temperature=0.07):
        super().__init__()
        self.image_encoder = image_encoder  # ViT or CNN
        self.text_encoder = text_encoder    # Transformer
        self.temperature = temperature
        
        # Projection heads
        self.vision_proj = nn.Linear(image_encoder.output_dim, embed_dim)
        self.text_proj = nn.Linear(text_encoder.output_dim, embed_dim)
    
    def forward(self, images, input_ids, attention_mask=None):
        # Encode modalities
        image_features = self.vision_proj(self.image_encoder(images))
        text_features = self.text_proj(self.text_encoder(input_ids, attention_mask))
        
        # Normalize
        image_features = F.normalize(image_features, dim=1)
        text_features = F.normalize(text_features, dim=1)
        
        # Contrastive loss
        logits = image_features @ text_features.T / self.temperature
        batch_size = logits.shape[0]
        labels = torch.arange(batch_size, device=logits.device)
        
        loss_i = F.cross_entropy(logits, labels)  # Image→Text
        loss_t = F.cross_entropy(logits.T, labels)  # Text→Image
        loss = (loss_i + loss_t) / 2
        
        return loss, image_features, text_features
    
    @torch.no_grad()
    def similarity(self, images, texts):
        """Compute image-text similarity scores."""
        img_feats = F.normalize(self.vision_proj(self.image_encoder(images)), dim=1)
        txt_feats = F.normalize(self.text_proj(self.text_encoder(texts)), dim=1)
        return img_feats @ txt_feats.T


class FrozenCLIPEmbedder:
    """Use pre-trained CLIP for zero-shot classification or retrieval."""
    
    def __init__(self, model_name='openai/clip-vit-base-patch32'):
        from transformers import CLIPProcessor, CLIPModel
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.model = CLIPModel.from_pretrained(model_name)
    
    def classify_image(self, image, candidate_labels: List[str]) -> Dict:
        inputs = self.processor(text=candidate_labels, images=image, 
                                return_tensors="pt", padding=True)
        outputs = self.model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = F.softmax(logits_per_image, dim=1).squeeze()
        
        return {
            candidate_labels[i]: round(probs[i].item(), 3)
            for i in range(len(candidate_labels))
        }
```

## Image Captioning (Encoder-Decoder)

```python
class ImageCaptioner(nn.Module):
    """Vision Encoder + Text Decoder for image captioning."""
    
    def __init__(self, vision_encoder, text_decoder, embed_dim=768):
        super().__init__()
        self.vision_encoder = vision_encoder
        self.text_decoder = text_decoder
        
        # Vision-to-text projection
        self.vision_proj = nn.Linear(vision_encoder.output_dim, embed_dim)
        self.text_embeddings = text_decoder.get_input_embeddings()
    
    def forward(self, images, caption_ids, caption_mask=None):
        # Get image features
        image_features = self.vision_proj(self.vision_encoder(images))
        
        # Teacher-forcing: pass image features as prefix to decoder
        decoder_input = self.text_embeddings(caption_ids)
        # Concatenate image features as first token
        decoder_input = torch.cat([image_features.unsqueeze(1), decoder_input[:, :-1]], dim=1)
        
        outputs = self.text_decoder(inputs_embeds=decoder_input, 
                                    attention_mask=caption_mask)
        return outputs
    
    @torch.no_grad()
    def generate_caption(self, image, max_length=30):
        """Generate caption for an image."""
        image_features = self.vision_proj(self.vision_encoder(image.unsqueeze(0)))
        
        # Autoregressive generation
        generated = [self.text_decoder.config.bos_token_id]
        for _ in range(max_length):
            decoder_embeds = self.text_embeddings(torch.tensor([generated]))
            decoder_embeds = torch.cat([image_features.unsqueeze(1), decoder_embeds], dim=1)
            
            logits = self.text_decoder(inputs_embeds=decoder_embeds).logits
            next_token = logits[0, -1].argmax().item()
            generated.append(next_token)
            if next_token == self.text_decoder.config.eos_token_id:
                break
        
        return generated
```

## Common Pitfalls

1. **Modality gap** — CLIP embeddings for images and text can live in different clusters; fine-tune on domain data
2. **Catastrophic forgetting** — fine-tuning a frozen CLIP on specific tasks may overfit
3. **Resolution mismatch** — ViTs often train on 224×224 but production images vary; handle resizing
4. **Caption quality** — image caption models generate generic captions; use CIDEr optimization
5. **Computational cost** — running both vision and language models is expensive; use quantization

## Verification Checklist

- [ ] Vision encoder handles target image resolutions
- [ ] Text encoder tokenizer configured correctly
- [ ] Contrastive loss working (matched pairs have higher similarity)
- [ ] Zero-shot classification accuracy acceptable
- [ ] Caption generation produces relevant descriptions
- [ ] Inference optimized (quantization, batching, caching)

## See Also

- custom-neural-architecture-design — custom multi-modal architectures
- computer-vision-techniques — vision encoder backbones
- nlp-techniques — text encoder backbones
- transformer-architectures — cross-attention for fusion
