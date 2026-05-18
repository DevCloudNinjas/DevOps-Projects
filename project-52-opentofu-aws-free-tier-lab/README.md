# Project 52: OpenTofu AWS Free-Tier Lab

Beginner-friendly infrastructure-as-code lab that creates a tiny AWS VPC, public subnet, security group, and optional free-tier EC2 instance with OpenTofu or Terraform.

## What You Learn

- How OpenTofu/Terraform plans and applies infrastructure
- How providers, variables, outputs, and state work
- Why tags and destroy steps matter for cost control
- How to keep cloud labs small and reviewable

## Cost Warning

This lab can create AWS resources. Use free-tier eligible instance types, confirm your region, and destroy everything when done.

## Prerequisites

- AWS account
- AWS CLI configured
- OpenTofu or Terraform

## Quick Start

```bash
tofu init
tofu plan -out tfplan
tofu apply tfplan
tofu destroy
```

Terraform works too:

```bash
terraform init
terraform plan -out tfplan
terraform apply tfplan
terraform destroy
```

## Student Exercises

- Add an S3 backend for remote state.
- Add a second subnet in another Availability Zone.
- Add a budget alarm.
- Convert the EC2 instance into a reusable module.

