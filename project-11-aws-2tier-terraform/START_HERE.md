# Start Here: project-11-aws-2tier-terraform

**Learning focus:** Modular AWS two-tier infrastructure as code with Terraform

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, read `README.md`, `project.yaml`, `variables.tf`, and the module filenames to map how
the VPC, security groups, ALB/target group, autoscaling, RDS, IAM, WAF, CDN, ACM, and Route 53 components are
organized before running any Terraform command.

## Checkpoints

1. 1. You can draw or annotate the dependency flow from the VPC and security-group modules to the ALB/autoscaling and RDS components
2. 1. You can identify in the readme the two stated hardening changes—web-tier ingress limited to the ALB security group and RDS storage encryption enabled—and locate the corresponding active module files
3. 1. You can produce a local review showing the Terraform configuration is formatted according to the packet's stated validation command without applying or destroying infrastructure.

## Hints if you are stuck

1. 1. If the module relationships are unclear, start at `main.tf` and follow each module call into its `variables.tf` rather than inspecting files in arbitrary order
2. 1. For an input or reference error, compare variable names and required values across the root files and the module-specific variable files
3. 1. For the security review, trace the source security group on web-tier ports and the RDS encryption setting, checking that the configuration matches the README's stated 2026 enhancements.

## Evidence to capture

Annotated local module-dependency map plus a non-destructive Terraform formatting-check result and notes tying
the two security enhancements to their module files

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
