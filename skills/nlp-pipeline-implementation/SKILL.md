---
name: nlp-pipeline-implementation
description: "Use when building end-to-end NLP processing pipelines."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [nlp, pipeline, text-processing, tokenization, NER, parsing, classification]
    related_skills: [nlp-techniques, rag-system-design, text-summarization-systems, question-answering-systems]
---

# End-to-End NLP Pipeline Implementation

Building production NLP pipelines — from text preprocessing and tokenization through named entity recognition, relation extraction, sentiment analysis, and text classification.

## When to Use

- Processing large volumes of text (documents, social media, support tickets)
- Building information extraction systems from unstructured text
- Implementing multi-stage NLP workflows (preprocess → analyze → extract)
- Deploying NLP models in production with batching and caching
- Combining multiple NLP tasks (NER + sentiment + classification)

## Pipeline Architecture

```
Raw Text → Preprocessing → Tokenization → Feature Extraction → Task Models → Post-processing → Output
```

## Preprocessing

```python
import re
import unicodedata

class TextPreprocessor:
    """Text cleaning and normalization pipeline."""
    
    @staticmethod
    def clean(text: str) -> str:
        """Clean and normalize text."""
        # Normalize unicode
        text = unicodedata.normalize('NFKD', text)
        
        # Collapse whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove control characters
        text = ''.join(c for c in text if unicodedata.category(c)[0] != 'C' or c in '\n\t')
        
        # Strip leading/trailing whitespace
        return text.strip()
    
    @staticmethod
    def normalize_for_search(text: str) -> str:
        """Normalize for search/indexing (lowercase, no punctuation)."""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

# Language detection
def detect_language(text: str) -> str:
    """Detect language using fastText or langdetect."""
    from langdetect import detect
    try:
        return detect(text)
    except:
        return 'unknown'
```

## Named Entity Recognition (NER)

```python
import spacy

class NERExtractor:
    """Extract named entities from text using spaCy or custom models."""
    
    def __init__(self, model='en_core_web_lg'):
        self.nlp = spacy.load(model)
    
    def extract(self, text: str):
        """Extract entities with types and positions."""
        doc = self.nlp(text)
        
        entities = []
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char,
                'description': spacy.explain(ent.label_)
            })
        
        return entities
    
    def extract_relations(self, text: str):
        """Simple relation extraction using dependency parsing.
        Subject - verb - object triples."""
        doc = self.nlp(text)
        relations = []
        
        for token in doc:
            if token.dep_ == 'ROOT' and token.pos_ == 'VERB':
                subject = [w for w in token.lefts if w.dep_ in ('nsubj', 'nsubjpass')]
                objects = [w for w in token.rights if w.dep_ in ('dobj', 'pobj', 'attr')]
                
                for subj in subject:
                    for obj in objects:
                        relations.append({
                            'subject': self._get_entity_text(subj),
                            'relation': token.text,
                            'object': self._get_entity_text(obj)
                        })
        
        return relations
    
    def _get_entity_text(self, token):
        """Get full entity text for a token (handles compound entities)."""
        span = token.doc[token.subtree]
        return span.text
```

## Text Classification

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import numpy as np

class TextClassifier:
    """Text classification pipeline with TF-IDF + Linear model."""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=50000, ngram_range=(1, 2),
            sublinear_tf=True, stop_words='english'
        )
        self.classifier = LogisticRegression(
            C=1.0, max_iter=1000, multi_class='multinomial'
        )
    
    def train(self, texts, labels):
        X = self.vectorizer.fit_transform(texts)
        self.classifier.fit(X, labels)
    
    def predict(self, texts):
        X = self.vectorizer.transform(texts)
        return self.classifier.predict(X)
    
    def predict_proba(self, texts):
        X = self.vectorizer.transform(texts)
        return self.classifier.predict_proba(X)
    
    def explain(self, text, top_n=5):
        """Explain prediction: top features per class."""
        X = self.vectorizer.transform([text])
        feature_names = self.vectorizer.get_feature_names_out()
        
        explanations = {}
        for i, class_name in enumerate(self.classifier.classes_):
            coef = self.classifier.coef_[i] if self.classifier.coef_.shape[0] > 1 else self.classifier.coef_[0]
            # Top features for this class
            top_indices = np.argsort(X.toarray()[0] * coef)[-top_n:]
            explanations[class_name] = [
                (feature_names[idx], coef[idx])
                for idx in top_indices
            ]
        
        return explanations
```

## Sentiment Analysis

```python
from transformers import pipeline

class SentimentAnalyzer:
    """Sentiment analysis using transformer models."""
    
    def __init__(self, model="distilbert-base-uncased-finetuned-sst-2-english"):
        self.pipeline = pipeline("sentiment-analysis", model=model)
    
    def analyze(self, texts):
        results = self.pipeline(texts, truncation=True)
        for r in results:
            r['score'] = round(r['score'], 4)
        return results
    
    def analyze_batch(self, texts, batch_size=32):
        return self.pipeline(texts, batch_size=batch_size, truncation=True)


# Aspect-based sentiment (more detailed)
class AspectSentiment:
    """Extract sentiment toward specific aspects/entities."""
    
    def extract_aspects(self, doc):
        aspects = []
        for chunk in doc.noun_chunks:
            # Check if chunk has sentiment-bearing modifiers
            sentiment_words = [w for w in chunk.subtree 
                             if w.pos_ in ('ADJ', 'ADV')]
            if sentiment_words:
                aspects.append({
                    'aspect': chunk.text,
                    'modifiers': [w.text for w in sentiment_words],
                })
        return aspects
```

## Full Pipeline Assembly

```python
class NLPPipeline:
    """Composable NLP pipeline with stages."""
    
    def __init__(self):
        self.stages = []
    
    def add_stage(self, name, func, input_key='text'):
        self.stages.append((name, func, input_key))
    
    def process(self, text: str) -> dict:
        result = {'text': text}
        current = text
        
        for name, func, input_key in self.stages:
            try:
                output = func(current)
                result[name] = output
            except Exception as e:
                result[name] = {'error': str(e)}
        
        return result
    
    def process_batch(self, texts, batch_size=32):
        return [self.process(t) for t in texts]


# Example: build a pipeline
pipeline = NLPPipeline()
pipeline.add_stage('preprocessed', lambda t: TextPreprocessor.clean(t))
pipeline.add_stage('entities', lambda t: NERExtractor().extract(t))
pipeline.add_stage('sentiment', lambda t: SentimentAnalyzer().analyze([t])[0])
pipeline.add_stage('classified', lambda t: TextClassifier().predict([t])[0])
```

## Common Pitfalls

1. **Tokenization mismatches** — pre-tokenizing differently than the model expects; use model's tokenizer
2. **Encoding issues** — UTF-8 vs Latin-1, byte order marks; normalize early
3. **Language-specific preprocessing** — stemming works for English, not for Chinese
4. **Pipeline stage coupling** — one stage's failure should not crash the whole pipeline; handle errors per stage
5. **Batching overhead** — processing texts one by one is slow; batch where possible
6. **Model memory** — loading multiple NLP models into memory simultaneously; use model dispatching

## Verification Checklist

- [ ] Text cleaning handles Unicode, HTML entities, and encoding issues
- [ ] NER correctly identifies entities in test documents
- [ ] Classification accuracy meets minimum threshold
- [ ] Pipeline handles batch processing efficiently
- [ ] Error handling prevents single-stage failures from cascading
- [ ] Preprocessing results preserved for debugging
- [ ] Models dispatched efficiently (loaded/unloaded as needed)

## See Also

- nlp-techniques — foundational NLP concepts
- rag-system-design — using NLP for retrieval pipelines
- text-summarization-systems — summarization as a pipeline stage
- question-answering-systems — QA as a pipeline stage
