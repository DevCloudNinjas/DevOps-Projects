# Start Here: project-39-gha-aws-terraform

**Learning focus:** Terraform-based AWS infrastructure and GitHub Actions CI/CD for container deployment

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

Read the README and inspect the Terraform and workflow filenames locally, then run the repository's stated validation command `terraform fmt -check` without applying or destroying anything.

## Checkpoints

1. 1. The learner can identify the stated stack and AWS components from the README and project metadata
2. 2. `terraform fmt -check` completes locally and any formatting issue is recorded without changing infrastructure
3. 3. The learner can map the Terraform files, ECS/VPC modules, Docker files, and GitHub Actions workflows to their roles in the intended CI/CD path without triggering a workflow.

## Hints if you are stuck

1. 1. Start by separating configuration files from the two reusable Terraform module directories and note which files define inputs, outputs, and resources
2. 2. If formatting validation fails, inspect the reported file and compare its layout with Terraform's formatting conventions rather than changing deployment settings
3. 3. When tracing the workflow, follow references between ECR image building, Terraform apply, and Terraform destroy, and check required names or variables locally before considering any cloud action.

## Evidence to capture

Local `terraform fmt -check` result, a file-to-role map, and a short annotated diagram or notes tracing the GitHub Actions/ECR/Terraform workflow

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
