# Start Here: project-52-opentofu-aws-free-tier-lab

**Learning focus:** Beginner OpenTofu/Terraform infrastructure-as-code for small AWS VPC labs

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, copy `terraform.tfvars.example` to `terraform.tfvars` and then run the local-only `make
validate` before considering any cloud operation.

## Checkpoints

1. 1. `make validate` completes after formatting, provider initialization without a backend, and configuration validation
2. 1. A reviewed `tfplan` exists before any apply step and shows only the intended tiny VPC, public subnet, security group, and optional instance changes
3. 1. Local outputs/logs and cleanup evidence show the lab was reviewed and the destroy plan was confirmed, with no student materials modified.

## Hints if you are stuck

1. 1. If the first validation command cannot find `tofu`, check whether the repository supports the documented `TF=terraform` prefix rather than changing the infrastructure files
2. 1. If validation or planning reports configuration problems, compare variable names and values against `terraform.tfvars.example` and inspect formatting before troubleshooting credentials
3. 1. For SSH exposure warnings, verify that `allowed_ssh_cidr` is limited to the learner's own public IP using `/32`, and use the project's logs to inspect reported outputs or stale state.

## Evidence to capture

Terminal transcript or screenshots of local validation, the reviewed plan, relevant outputs/logs, and
confirmed cleanup evidence

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
