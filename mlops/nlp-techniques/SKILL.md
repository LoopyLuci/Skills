---
name: nlp-techniques
description: "Use when implementing NLP: tokenization, embeddings, NER, QA."
category: mlops
tags: [nlp, tokenization, embeddings, ner, text-classification]
---
# NLP Techniques

Core NLP techniques for text processing and understanding.

## Text Preprocessing

```python
import re
from typing import List

def clean_text(text: str) -> str:
    """Basic text cleaning pipeline."""
    text = text.lower()
    text = re.sub(r'http\S+', '[URL]', text)      # URLs
    text = re.sub(r'@\w+', '[USER]', text)         # mentions
    text = re.sub(r'#\w+', '[HASHTAG]', text)      # hashtags
    text = re.sub(r'\d+', '[NUM]', text)           # numbers
    text = re.sub(r'[^\w\s\[\]]', '', text)         # punctuation
    text = re.sub(r'\s+', ' ', text).strip()       # extra spaces
    return text

# Language-specific preprocessing
def preprocess_code(text: str) -> str:
    """Preprocess code for NLP (keep structure)."""
    text = re.sub(r'"""[\s\S]*?"""', '[DOCSTRING]', text)  # remove docstrings
    text = re.sub(r'#.*$', '[COMMENT]', text, flags=re.MULTILINE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
```

## Tokenization Strategies

```python
# BPE (Byte-Pair Encoding) — GPT models
# WordPiece — BERT models
# SentencePiece — language-agnostic
# Unigram — T5, XLNet

# HuggingFace tokenizer
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
tokens = tokenizer.tokenize("Hello, world!")
ids = tokenizer.encode("Hello, world!")
decoded = tokenizer.decode(ids)
```

## Named Entity Recognition (NER)

```python
from transformers import pipeline

ner = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
results = ner("Docker was founded by Solomon Hykes in France.")

for entity in results:
    print(f"{entity['word']:15} → {entity['entity']:10} ({entity['score']:.2f})")
```

## Text Classification

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Fast baseline classifier
clf = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=10000, ngram_range=(1, 2))),
    ('clf', MultinomialNB(alpha=0.1)),
])

# Zero-shot classification (no training data)
classifier = pipeline("zero-shot-classification",
    model="facebook/bart-large-mnli")

candidate_labels = ["docker", "kubernetes", "git", "python", "rust"]
result = classifier("How do I mount a volume in a container?", candidate_labels)
print(result['labels'][0], result['scores'][0])  # docker 0.95
```

## Semantic Search

```python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

# Corpus
documents = [
    "Docker containers are lightweight",
    "Kubernetes orchestrates containers",
    "Python is a programming language",
]
doc_embeddings = model.encode(documents, convert_to_tensor=True)

# Query
query = "Container management tool"
query_embedding = model.encode(query, convert_to_tensor=True)

scores = util.cos_sim(query_embedding, doc_embeddings)[0]
best = scores.argmax().item()
print(f"Best match: {documents[best]} (score={scores[best]:.2f})")
```

## Pitfalls

- Tokenization varies by model — don't mix tokenizers
- NER models are domain-specific — medical NER fails on code
- Zero-shot classification is slower but needs no training data
- TF-IDF is bag-of-words — loses word order and semantics
- Sentence-BERT embeddings capture semantics but are slower than TF-IDF
