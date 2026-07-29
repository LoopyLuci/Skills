---
name: code-generation-tools
description: "Use when implementing code generation tools."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [code-generation, scaffolding, codegen, templates, AST, DSL]
    related_skills: [project-scaffolding, monorepo-management, prompt-engineering-for-code, frontend-bootstrap]
---

# Code Generation Tools

Implementing code generation tools — from template-based scaffolding through AST manipulation, DSL parsing, and AI-assisted code generation.

## When to Use

- Auto-generating boilerplate code for repetitive patterns
- Building project scaffolding generators
- Creating domain-specific language (DSL) compilers
- Implementing code transformation and migration tools

## Code Generation Patterns

```python
import ast, json

class CodeGenerator:
    """Generate code from templates and models."""
    
    def generate_from_template(self, template: str, variables: Dict) -> str:
        for k, v in variables.items():
            template = template.replace(f'{{{{ {k} }}}}', v)
        return template
    
    def generate_class_from_schema(self, schema: Dict) -> str:
        imports = []
        fields = []
        for field_name, field_type in schema.get('fields', {}).items():
            fields.append(f"    {field_name}: {field_type}")
            if '=' in field_type:
                import_name = field_type.split('=')[0].strip()
                if import_name not in imports:
                    imports.append(import_name)
        
        code = 'from dataclasses import dataclass\n'
        if imports: code += f'from typing import {", ".join(set(imports))}\n'
        code += f'\n\n@dataclass\nclass {schema["name"]}:\n'
        code += '\n'.join(fields) if fields else '    pass'
        return code
```

## Verification Checklist

- [ ] Template variables properly escaped and substituted
- [ ] Generated code is syntactically valid
- [ ] Code formatting matches project standards
- [ ] Generators are deterministic (same input → same output)
- [ ] Error handling for missing variables or invalid schemas
