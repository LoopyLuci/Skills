---
name: terraform-module-patterns
description: "Write reusable Terraform modules with remote state"
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
