---
name: tool-augmented-models-training
description: "Use when training models for tool-use and function calling."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [tool-use, function-calling, training, fine-tuning, agents]
    related_skills: [tool-augmented-agents, agentic-models-from-scratch, rlhf-implementation-guide, agent-framework-design]
---

# Training Models for Tool Use and Function Calling

Strategies for training language models to use tools effectively — from data generation through fine-tuning to evaluation of tool-calling ability.

## When to Use

- Fine-tuning a model specifically for tool-use capability
- Generating synthetic tool-use training data
- Evaluating tool-calling accuracy and robustness
- Improving an existing agent's ability to select and use tools
- Building models that can handle dynamic, user-defined tools

## Training Data Generation

### Synthetic Data Pipeline

```python
import json
import random

class ToolUseDataGenerator:
    """Generate synthetic training data for tool-use behavior.
    
    Data format: conversation with interleaved tool calls.
    {
        "messages": [
            {"role": "system", "content": "You have access to tools..."},
            {"role": "user", "content": "What's the weather in Paris?"},
            {"role": "assistant", "content": "Let me check.", "tool_calls": [...]},
            {"role": "tool", "content": "72°F, sunny", "tool_call_id": "..."},
            {"role": "assistant", "content": "The weather in Paris is 72°F and sunny."}
        ]
    }
    """
    
    def __init__(self, tools, num_examples=10000):
        self.tools = tools
        self.num_examples = num_examples
    
    def generate_dataset(self):
        """Generate diverse tool-use examples."""
        examples = []
        
        # Pattern 1: Simple single-tool call
        for tool in self.tools:
            for _ in range(self.num_examples // len(self.tools) // 3):
                examples.append(self._single_tool_example(tool))
        
        # Pattern 2: Multi-tool chaining
        for _ in range(self.num_examples // 3):
            tools = random.sample(self.tools, min(3, len(self.tools)))
            examples.append(self._chained_tool_example(tools))
        
        # Pattern 3: Conditional tool use
        for _ in range(self.num_examples // 6):
            examples.append(self._conditional_tool_example())
        
        # Pattern 4: Error recovery
        for _ in range(self.num_examples // 6):
            examples.append(self._error_recovery_example())
        
        return examples
    
    def _single_tool_example(self, tool):
        """Generate a simple tool-use conversation."""
        user_intent = self._generate_user_intent(tool)
        return {
            "messages": [
                {"role": "system", "content": self._system_prompt()},
                {"role": "user", "content": user_intent},
                {"role": "assistant", "content": self._thinking_trace(tool), 
                 "tool_calls": [self._generate_tool_call(tool)]},
                {"role": "tool", "content": self._generate_tool_response(tool), 
                 "tool_call_id": "call_1"},
                {"role": "assistant", "content": self._final_response(tool)}
            ]
        }
    
    def _chained_tool_example(self, tools):
        """Generate multi-tool chain conversation."""
        messages = [{"role": "system", "content": self._system_prompt()}]
        messages.append({"role": "user", "content": f"Use {', '.join(t.name for t in tools)} to accomplish this task."})
        
        for i, tool in enumerate(tools):
            messages.append({
                "role": "assistant",
                "content": f"Using {tool.name}.", 
                "tool_calls": [self._generate_tool_call(tool)]
            })
            messages.append({
                "role": "tool",
                "content": self._generate_tool_response(tool),
                "tool_call_id": f"call_{i}"
            })
        
        messages.append({"role": "assistant", "content": "Task complete."})
        return {"messages": messages}
    
    def _system_prompt(self):
        tool_descriptions = "\n".join(
            f"- {t.name}: {t.description}" for t in self.tools
        )
        return f"""You are a helpful assistant with access to tools.
Available tools:
{tool_descriptions}

When you need to use a tool, output a JSON tool call.
After receiving the result, provide a helpful response."""
```

### Tool Definition Format

```python
TOOL_SCHEMA_TEMPLATE = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name, e.g., Paris, France"
                },
                "units": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "default": "celsius"
                }
            },
            "required": ["location"]
        }
    }
}
```

## Fine-Tuning Strategies

### Full Fine-Tuning

```python
def train_tool_use(model, dataset, tokenizer, epochs=3, lr=1e-5):
    """Fine-tune model on tool-use conversations."""
    from transformers import TrainingArguments, Trainer
    
    training_args = TrainingArguments(
        output_dir="./tool-model",
        per_device_train_batch_size=8,
        gradient_accumulation_steps=4,
        learning_rate=lr,
        num_train_epochs=epochs,
        logging_steps=10,
        save_steps=500,
        fp16=True,
    )
    
    def tokenize_function(examples):
        # Format messages into training sequences
        texts = []
        for conversation in examples['messages']:
            text = tokenizer.apply_chat_template(
                conversation,
                tokenize=False,
                add_generation_prompt=False
            )
            texts.append(text)
        
        return tokenizer(texts, truncation=True, padding=True, max_length=4096)
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset.map(tokenize_function, batched=True),
    )
    
    trainer.train()
    return model
```

### LoRA Fine-Tuning

```python
from peft import LoraConfig, get_peft_model, TaskType

def lora_tune_tool_use(base_model):
    """Parameter-efficient fine-tuning for tool use.
    Only trains a small subset of parameters."""
    
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
        lora_dropout=0.1,
        bias="none",
        task_type=TaskType.CAUSAL_LM
    )
    
    model = get_peft_model(base_model, lora_config)
    model.print_trainable_parameters()  # ~0.5% of params
    return model
```

### Multi-Task Training

```python
class ToolUseTrainer:
    """Multi-objective training for tool use.
    Balances: general LM loss + tool-call accuracy + response quality."""
    
    def compute_loss(self, model, batch):
        outputs = model(**batch)
        
        # Standard LM loss
        lm_loss = outputs.loss
        
        # Tool-call specific loss (masked: only on tool-call tokens)
        if 'tool_labels' in batch:
            tool_logits = outputs.logits[batch['tool_mask']]
            tool_loss = F.cross_entropy(tool_logits, batch['tool_labels'])
        else:
            tool_loss = 0
        
        return lm_loss + 0.5 * tool_loss
```

## Evaluation

```python
class ToolUseEvaluator:
    """Evaluates tool-calling accuracy across multiple dimensions."""
    
    def __init__(self, test_cases):
        self.test_cases = test_cases
    
    def evaluate(self, model):
        results = {
            'tool_selection_accuracy': 0,
            'parameter_fidelity': 0,
            'error_recovery_rate': 0,
            'response_quality': 0
        }
        
        for case in self.test_cases:
            # Test: model selects the right tool
            prediction = model.generate(case['prompt'])
            results['tool_selection_accuracy'] += self._check_tool_selection(prediction, case)
            
            # Test: parameters are correctly formatted
            results['parameter_fidelity'] += self._check_parameters(prediction, case)
            
            # Test: handles errors gracefully
            if case.get('error_scenario'):
                results['error_recovery_rate'] += self._check_error_recovery(prediction, case)
        
        n = len(self.test_cases)
        return {k: v / n for k, v in results.items()}
    
    def _check_tool_selection(self, prediction, case):
        """Verify correct tool was chosen."""
        return 1.0 if case['expected_tool'] in prediction else 0.0
    
    def _check_parameters(self, prediction, case):
        """Verify parameters match expected format."""
        import json, re
        calls = re.findall(r'\{[^}]+\}', prediction)
        if not calls:
            return 0.0
        
        try:
            call = json.loads(calls[0])
            expected = case['expected_params']
            matching = sum(1 for k, v in expected.items() 
                         if call.get(k) == v)
            return matching / len(expected) if expected else 1.0
        except:
            return 0.0
```

## Common Pitfalls

1. **Tool hallucination** — model invokes non-existent tools; always validate tool names server-side
2. **Parameter hallucination** — invents parameter names; train with strict schema adherence
3. **Forgetting to call tools** — model describes what it would do without actually calling; use system prompt pressure
4. **Over-reliance on tools** — model calls tools for questions it could answer directly; train for selective use
5. **Tool call formatting** — model produces near-valid but incorrect JSON; use constrained decoding
6. **Multi-turn state loss** — model forgets previous tool results; train with long contexts

## Verification Checklist

- [ ] Model selects correct tool for each test case
- [ ] Parameters match tool schema (names, types, required fields)
- [ ] Model correctly handles tool output in subsequent response
- [ ] Error handling graceful (malformed tool output doesn't crash)
- [ ] No tool hallucination (never calls unlisted tools)
- [ ] Multi-turn consistency (remembers previous tool results)
- [ ] Generic vs. specific tool distinction (chooses right granularity)

## See Also

- tool-augmented-agents — wrapping tool-use models in agent frameworks
- agentic-models-from-scratch — building models with native tool-awareness
- agent-framework-design — integrating tool calls in agent architecture
- rlhf-implementation-guide — aligning tool-use behavior
