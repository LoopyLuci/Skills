---
name: dialogue-systems-conversational-ai
description: "Use when building conversational AI and dialogue systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [dialogue, conversational-ai, chatbots, dialogue-management, NLU, NLG]
    related_skills: [nlp-pipeline-implementation, rag-system-design, agent-framework-design, nlp-techniques]
---

# Dialogue Systems and Conversational AI

Building conversational AI systems — from goal-oriented dialogue (task bots) through open-domain chat to hybrid systems with dialogue management, NLU, and NLG.

## When to Use

- Building customer support chatbots
- Creating voice assistants or conversational interfaces
- Implementing goal-oriented dialogue (booking, ordering, troubleshooting)
- Designing multi-turn conversation management
- Building hybrid retrieval + generative chat systems

## Dialogue System Types

```
Task-Oriented Bots: Specific goals (book flight, order pizza)
Open-Domain Chat: Free-form conversation (companion, entertainment)
Hybrid: Task bot with chitchat capability
Agentic: Autonomous action-taking via conversation
```

## Dialogue Management

### State Machine

```python
from enum import Enum
from typing import Dict, Any, Optional

class DialogueState(Enum):
    GREETING = "greeting"
    COLLECT_INFO = "collect_info"
    CONFIRM = "confirm"
    EXECUTE = "execute"
    CLOSING = "closing"

class DialogueManager:
    """State-machine based dialogue management."""
    
    def __init__(self):
        self.slots: Dict[str, Any] = {}
        self.state = DialogueState.GREETING
        self.turn_count = 0
    
    def process(self, user_input: str, nlu_result: dict) -> dict:
        """Process user input and produce system response."""
        self.turn_count += 1
        
        if self.state == DialogueState.GREETING:
            return self._handle_greeting()
        
        elif self.state == DialogueState.COLLECT_INFO:
            return self._collect_information(nlu_result)
        
        elif self.state == DialogueState.CONFIRM:
            return self._confirm(nlu_result)
        
        elif self.state == DialogueState.EXECUTE:
            return self._execute()
        
        elif self.state == DialogueState.CLOSING:
            return self._closing()
    
    def _handle_greeting(self):
        self.state = DialogueState.COLLECT_INFO
        return {"response": "Welcome! How can I help you today?", "state": self.state.value}
    
    def _collect_information(self, nlu_result):
        # Extract entities and fill slots
        for entity in nlu_result.get('entities', []):
            self.slots[entity['type']] = entity['value']
        
        # Check required slots
        required = ['destination', 'date', 'passengers']
        missing = [s for s in required if s not in self.slots]
        
        if missing:
            return {
                "response": f"I still need: {', '.join(missing)}",
                "missing_slots": missing,
                "state": self.state.value
            }
        
        self.state = DialogueState.CONFIRM
        return self._confirm({})
    
    def _confirm(self, nlu_result):
        if nlu_result.get('intent') == 'confirm':
            self.state = DialogueState.EXECUTE
            return self._execute()
        
        summary = f"Here's your booking: {self.slots}"
        return {"response": f"{summary} Shall I proceed?", "state": self.state.value}
```

## NLU (Natural Language Understanding)

```python
from typing import List, Dict
import re

class IntentClassifier:
    """Classifier with fallback patterns."""
    
    def __init__(self, model=None):
        self.model = model  # Optional ML model
        # Fallback patterns
        self.patterns = {
            'greeting': r'\b(hi|hello|hey|good morning|good evening)\b',
            'goodbye': r'\b(bye|goodbye|see you|talk later)\b',
            'book': r'\b(book|reserve|order|schedule|appointment)\b',
            'cancel': r'\b(cancel|remove|delete|undo)\b',
            'status': r'\b(status|where is|track|check)\b',
            'help': r'\b(help|what can you|how do you)\b',
        }
    
    def classify(self, text: str) -> Dict:
        """Classify intent, using ML first, then pattern fallback."""
        text_lower = text.lower().strip()
        
        # Try ML model
        if self.model:
            intent = self.model.predict([text])[0]
            confidence = self.model.predict_proba([text]).max()
            if confidence > 0.7:
                return {'intent': intent, 'confidence': confidence, 'method': 'ml'}
        
        # Pattern fallback
        for intent, pattern in self.patterns.items():
            if re.search(pattern, text_lower):
                return {'intent': intent, 'confidence': 0.6, 'method': 'pattern'}
        
        return {'intent': 'unknown', 'confidence': 0.0, 'method': 'fallback'}


class EntityExtractor:
    """Extract entities from user input using patterns + NER."""
    
    def __init__(self, ner_model=None):
        self.ner_model = ner_model  # Optional spacy/flair NER
        self.patterns = {
            'date': r'\b(today|tomorrow|next \w+|monday|tuesday|\d{1,2}/\d{1,2})\b',
            'number': r'\b(\d+)\b',
            'location': r'\b(to|from) ([A-Z][a-z]+)\b',
        }
    
    def extract(self, text: str) -> List[Dict]:
        entities = []
        
        # Try NER model first
        if self.ner_model:
            doc = self.ner_model(text)
            for ent in doc.ents:
                entities.append({
                    'type': ent.label_,
                    'value': ent.text,
                    'method': 'ner'
                })
        
        # Pattern extraction for non-entity types
        date_match = re.search(self.patterns['date'], text, re.IGNORECASE)
        if date_match:
            entities.append({
                'type': 'date',
                'value': date_match.group(0),
                'method': 'pattern'
            })
        
        return entities
```

## Response Generation (NLG)

```python
import random

class ResponseGenerator:
    """Template-based and generative response generation."""
    
    def __init__(self, generative_model=None):
        self.generative = generative_model  # Optional LLM
        self.templates = {
            'greeting': [
                "Hello! How can I assist you today?",
                "Hi there! What can I help you with?",
                "Welcome! I'm here to help.",
            ],
            'goodbye': [
                "Goodbye! Have a great day!",
                "See you later!",
                "Take care!",
            ],
            'confirmation': [
                "I've noted that. Is there anything else?",
                "Got it! What's next?",
                "Done! Can I help with anything else?",
            ],
            'error': [
                "I'm sorry, I didn't understand that.",
                "Could you rephrase that?",
                "I'm not sure I follow. Can you be more specific?",
            ],
        }
    
    def generate(self, intent: str, slots: Dict = None, context: Dict = None) -> str:
        # Generative (for open-domain)
        if self.generative and intent == 'open_domain':
            prompt = f"User context: {context}\nGenerate a helpful response:"
            return self.generative.generate(prompt)
        
        # Template-based
        templates = self.templates.get(intent, self.templates['error'])
        response = random.choice(templates)
        
        # Slot fill
        if slots:
            response = response.format(**slots)
        
        return response


# Slot-filling template example
TEMPLATES_WITH_SLOTS = {
    'booking': 'I have booked {destination} for {passengers} on {date}.',
    'status': 'Your order #{order_id} is currently {status}.',
}
```

## Hybrid Architecture

```python
class HybridDialogueSystem:
    """Combines retrieval (FAQ) + generative (LLM) responses."""
    
    def __init__(self, faq_retriever, generative_model, dialogue_manager):
        self.faq = faq_retriever  # Retrieval from knowledge base
        self.llm = generative_model  # LLM for generation
        self.dm = dialogue_manager  # State tracking
    
    def respond(self, user_input: str) -> str:
        # 1. NLU
        intent = IntentClassifier().classify(user_input)
        entities = EntityExtractor().extract(user_input)
        
        # 2. Dialogue state update
        dm_result = self.dm.process(user_input, {
            'intent': intent['intent'],
            'entities': entities
        })
        
        # 3. Check FAQ first (for known questions)
        faq_answer = self.faq.search(user_input)
        if faq_answer and faq_answer['score'] > 0.85:
            # High confidence FAQ match
            return faq_answer['answer']
        
        # 4. For task-oriented flows, use dialogue manager
        if dm_result.get('state') != 'open_domain':
            return dm_result['response']
        
        # 5. For open-domain, use LLM
        return self.llm.generate(user_input)
```

## Common Pitfalls

1. **Dialogue state explosion** — slot combinations grow exponentially; use compact representations
2. **Error recovery** — user input will be misclassified; design graceful recovery flows
3. **Repetition** — template-based bots repeat responses; add variability via multiple templates
4. **Context length** — LLMs have limited context; summarize or forget old turns
5. **Persona consistency** — LLMs can contradict themselves; use persona embeddings
6. **Evaluation difficulty** — open-domain dialogue has no single correct answer; use human eval

## Verification Checklist

- [ ] Dialogue manager handles all states (greeting → info → confirm → execute)
- [ ] Intent classifier works for all supported intents
- [ ] Entity extraction captures required slot values
- [ ] Failure recovery tested (input out of domain, entity not found)
- [ ] Response variability confirmed (not always the same template)
- [ ] Multi-turn context maintained correctly
- [ ] Latency acceptable for interactive conversation

## See Also

- nlp-pipeline-implementation — NLU preprocessing pipeline
- rag-system-design — retrieval for FAQ/context
- agent-framework-design — integrating dialogue with agents
- nlp-techniques — foundational NLP concepts
