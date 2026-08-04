---
name: compiler-interpreter-basics
description: "Use when building compilers, interpreters, and transpilers."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [compiler, interpreter, parser, lexer, AST, codegen]
    related_skills: [type-system-design-theory, formal-verification-methods, cross-language-design-patterns]
---

# Compiler and Interpreter Basics

Building compilers, interpreters, and transpilers from scratch — from lexing and parsing through semantic analysis, optimization, and code generation.

## When to Use

- Building a domain-specific language (DSL)
- Creating a transpiler (e.g., TypeScript → JavaScript)
- Implementing a programming language interpreter
- Understanding how compilers work internally
- Adding macro or preprocessing to existing languages

## Compiler Pipeline

```
Source → Lexer → Parser → AST → Semantic Analysis → IR → Optimizer → Codegen → Target
          ↑         ↑         ↑          ↑            ↑        ↑          ↑
        Tokens    Syntax    AST      Symbol Table    IR      Optimized   Assembly/
                  Tree                           (SSA)       IR        Bytecode
```

## Stage 1: Lexer (Tokenizer)

```python
import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Token:
    type: str  # 'NUMBER', 'IDENTIFIER', 'KEYWORD', 'OPERATOR', etc.
    value: str
    line: int
    column: int

class Lexer:
    """Tokenize source code into tokens."""
    
    TOKEN_SPEC = [
        ('NUMBER',    r'\d+(\.\d*)?'),          # Integer or decimal
        ('IDENTIFIER', r'[A-Za-z_]\w*'),         # Identifiers
        ('KEYWORD',    r'\b(if|else|while|for|def|return|class|import|from|as|let|const|fn|mut)\b'),
        ('OPERATOR',   r'[+\-*/%=<>!&|^~]+'),   # Operators
        ('STRING',     r'"[^"]*"|\'[^\']*\''),   # String literals
        ('COMMENT',    r'//[^\n]*|/\*.*?\*/'),   # Comments
        ('NEWLINE',    r'\n'),
        ('WHITESPACE', r'[ \t]+'),
        ('LPAREN',     r'\('),
        ('RPAREN',     r'\)'),
        ('LBRACE',     r'\{'),
        ('RBRACE',     r'\}'),
        ('LBRACKET',   r'\['),
        ('RBRACKET',   r'\]'),
        ('SEMICOLON',  r';'),
        ('COLON',      r':'),
        ('COMMA',      r','),
        ('DOT',        r'\.'),
        ('MISMATCH',   r'.'),                    # Any other character
    ]
    
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.pos = 0
        self.line = 1
        self.column = 1
        self._tokenize()
    
    def _tokenize(self):
        """Convert source string to list of tokens."""
        while self.pos < len(self.source):
            token = self._next_token()
            if token and token.type not in ('WHITESPACE', 'COMMENT'):
                self.tokens.append(token)
    
    def _next_token) -> Optional[Token]:
        """Match the next token."""
        for token_type, pattern in self.TOKEN_SPEC:
            regex = re.compile(pattern)
            match = regex.match(self.source, self.pos)
            if match:
                value = match.group(0)
                token = Token(
                    type=token_type,
                    value=value,
                    line=self.line,
                    column=self.column
                )
                # Update position
                lines = value.count('\n')
                if lines > 0:
                    self.line += lines
                    self.column = len(value) - value.rfind('\n')
                else:
                    self.column += len(value)
                self.pos = match.end()
                return token
        return None
```

## Stage 2: Parser (Recursive Descent)

```python
class ASTNode:
    """Base class for all AST nodes."""
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class FunctionDef(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class IfStatement(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class Parser:
    """Recursive descent parser. Grammar (simplified):
    
    program      → statement*
    statement    → expr_statement | if_statement | function_def
    expr         → term (('+' | '-') term)*
    term         → factor (('*' | '/') factor)*
    factor       → NUMBER | IDENTIFIER | '(' expr ')'
    """
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def parse(self) -> Program:
        """Parse the entire token stream."""
        statements = []
        while not self._is_at_end():
            statements.append(self._statement())
        return Program(statements)
    
    def _statement(self):
        """Parse a single statement."""
        if self._match('KEYWORD', 'if'):
            return self._if_statement()
        elif self._match('KEYWORD', 'def') or self._match('KEYWORD', 'fn'):
            return self._function_def()
        elif self._match('KEYWORD', 'let') or self._match('KEYWORD', 'const'):
            return self._variable_decl()
        else:
            return self._expression_statement()
    
    def _if_statement(self):
        """if (condition) { then } else { else }"""
        self._consume('LPAREN', "Expected '(' after 'if'")
        condition = self._expression()
        self._consume('RPAREN', "Expected ')' after condition")
        then_branch = self._block()
        else_branch = None
        if self._match('KEYWORD', 'else'):
            else_branch = self._block()
        return IfStatement(condition, then_branch, else_branch)
    
    def _expression(self):
        """Parse expression (handles operator precedence)."""
        left = self._term()
        while self._match('OPERATOR', '+') or self._match('OPERATOR', '-'):
            op = self._previous().value
            right = self._term()
            left = BinaryOp(left, op, right)
        return left
    
    def _term(self):
        """Parse term (multiplication/division)."""
        left = self._factor()
        while self._match('OPERATOR', '*') or self._match('OPERATOR', '/'):
            op = self._previous().value
            right = self._factor()
            left = BinaryOp(left, op, right)
        return left
    
    def _factor(self):
        """Parse factor (atoms)."""
        if self._match('NUMBER'):
            return Number(float(self._previous().value))
        if self._match('IDENTIFIER'):
            return Identifier(self._previous().value)
        if self._match('LPAREN'):
            expr = self._expression()
            self._consume('RPAREN', "Expected ')' after expression")
            return expr
        raise SyntaxError(f"Unexpected token at line {self._peek().line}")
```

## Stage 3: Interpreter

```python
class Environment:
    """Variable scope for interpreter."""
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent
    
    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Undefined variable: {name}")
    
    def set(self, name, value):
        self.variables[name] = value


class Interpreter:
    """AST-walking interpreter."""
    
    def __init__(self):
        self.global_env = Environment()
    
    def interpret(self, program: Program):
        result = None
        for statement in program.statements:
            result = self._evaluate(statement, self.global_env)
        return result
    
    def _evaluate(self, node, env):
        if isinstance(node, Number):
            return node.value
        
        elif isinstance(node, Identifier):
            return env.get(node.name)
        
        elif isinstance(node, BinaryOp):
            left = self._evaluate(node.left, env)
            right = self._evaluate(node.right, env)
            
            if node.op == '+': return left + right
            elif node.op == '-': return left - right
            elif node.op == '*': return left * right
            elif node.op == '/': return left / right
```

## Stage 4: Code Generation (to LLVM IR concept)

```python
class CodeGenerator:
    """Generate target code from AST.
    
    Example: generate Python code from our AST as a transpiler."""
    
    def generate(self, node, indent=0):
        if isinstance(node, Program):
            return '\n'.join(self.generate(stmt, indent) for stmt in node.statements)
        
        elif isinstance(node, BinaryOp):
            left = self.generate(node.left, indent)
            right = self.generate(node.right, indent)
            return f"({left} {node.op} {right})"
        
        elif isinstance(node, Number):
            return str(node.value)
        
        elif isinstance(node, FunctionDef):
            params = ', '.join(node.params)
            body = '\n'.join(self.generate(s, indent + 1) for s in node.body)
            return f"def {node.name}({params}):\n{'  ' * (indent + 1)}{body}"
        
        return ""
```

## Common Pitfalls

1. **Left recursion** — A → A + B causes infinite recursion; use iterative parsing or left-associative rewriting
2. **Operator precedence** — without precedence climbing or Pratt parsing, expressions parse wrong
3. **Error recovery** — one syntax error shouldn't stop the entire parse; implement panic-mode recovery
4. **Unicode/encoding** — source files come in various encodings; normalize to UTF-8 at the lexer level
5. **Memory management** — ASTs can be large (100K+ nodes); use arenas or reference counting
6. **Semantic analysis** — parsing validates syntax, but semantic analysis validates meaning; don't skip it

## Verification Checklist

- [ ] Lexer tokenizes all valid inputs correctly
- [ ] Parser produces correct AST for valid inputs
- [ ] Parser reports meaningful errors for invalid inputs
- [ ] Interpreter produces correct results for test programs
- [ ] Code generator produces valid target code
- [ ] Handles edge cases: empty programs, deeply nested expressions, Unicode
- [ ] Performance: compiles 10K LOC in < 1 second

## See Also

- type-system-design-theory — designing type systems for languages
- formal-verification-methods — verifying compiler correctness
- cross-language-design-patterns — multi-language patterns
