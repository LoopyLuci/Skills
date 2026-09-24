---
name: terraform-module-patterns
description: Write reusable Terraform modules with remote state
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [terraform, module, patterns]
---

# Terraform Module Patterns

## Module Structure
```hcl
modules/
  vpc/
    main.tf
    variables.tf
    outputs.tf
```

## Reusable Module
```hcl
variable "name" { type = string }
variable "cidr" { type = string }

resource "aws_vpc" "this" {
  cidr_block = var.cidr
  tags = { Name = var.name }
}
```

## Remote State
```hcl
terraform {
  backend "s3" {
    bucket = "my-state-bucket"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}
```

## Trigger

Activate this skill when the user mentions:
- terraform, module, patterns workflows or issues
- Building, fixing, or optimizing terraform module patterns


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
