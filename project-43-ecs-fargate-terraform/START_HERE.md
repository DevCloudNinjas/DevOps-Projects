# Start Here: project-43-ecs-fargate-terraform

**Learning focus:** Terraform-based AWS ECS Fargate container deployment and cloud networking/IAM architecture

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the project directory, read README.md and inspect main.tf, variables.tf, providers.tf, outputs.tf, and
project.yaml without configuring credentials or running any apply command.

## Checkpoints

1. 1. `terraform fmt -check` reports whether the local Terraform files match the repository's stated validation command
2. 1. The student can trace, on paper or in a local diagram, the declared flow from container image/ECR through ECS Fargate, VPC subnets/security groups, and the application load balancer
3. 1. The student can identify in the Terraform files where the task execution role, task role, image reference, networking, and `alb_dns_name` output are defined, without applying infrastructure.

## Hints if you are stuck

1. 1. If formatting validation fails, compare indentation and block layout across all `.tf` files before changing resource behavior
2. 1. If the architecture is unclear, follow references from variables and provider configuration into the ECS task definition and service, then outward to networking and load-balancer resources
3. 1. If the two IAM roles seem interchangeable, use the README's distinction between ECS agent operations and permissions used by application code as the comparison criterion.

## Evidence to capture

A local validation result, annotated architecture sketch, and file/line references for image, IAM roles,
network wiring, and ALB output

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
