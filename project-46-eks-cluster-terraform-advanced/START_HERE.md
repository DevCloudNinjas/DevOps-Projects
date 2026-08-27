# Start Here: project-46-eks-cluster-terraform-advanced

**Learning focus:** Terraform modular infrastructure design for AWS EKS, VPC, and Kubernetes configuration

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, read `README.md`, `variables.tf`, `provider.tf`, and the `modules/eks` and
`modules/vpc` variable/output files, then run only the local validation command `terraform fmt -check`.

## Checkpoints

1. 1. `terraform fmt -check` completes locally and the student can identify the root module files plus the separate EKS and VPC module boundaries
2. 1. The student produces a written dependency map showing how root inputs and module outputs connect the VPC, EKS cluster, Kubernetes provider, and declared outputs without applying anything
3. 1. The student explains how the configuration is intended to expose the cluster name and container IP output and records unresolved assumptions or validation errors without contacting AWS.

## Hints if you are stuck

1. 1. If formatting validation fails, compare indentation and block layout across the root files and both module directories before changing Terraform logic
2. 1. If the module relationships are unclear, trace each `module` block's declared inputs against the matching `variables.tf` and then follow the corresponding `outputs.tf`
3. 1. If an output cannot be explained from the packet, distinguish a root output from a module output and mark the missing link rather than inventing a value or running a cloud command.

## Evidence to capture

Local `terraform fmt -check` result, annotated root-to-module dependency map, and a short explanation of the
intended cluster-name/container-IP outputs with noted uncertainties

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
