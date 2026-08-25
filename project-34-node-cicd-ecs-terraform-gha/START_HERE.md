# Start Here: project-34-node-cicd-ecs-terraform-gha

**Learning focus:** Python/Flask container CI/CD with Terraform-managed AWS ECS and GitHub Actions

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

Read `app.py`, `Dockerfile`, `terraform/main.tf`, and the three workflow files locally, then compare their declared runtime, image, and deployment steps without running or applying anything.

## Checkpoints

1. 1. The learner can explain whether the Python/Flask files and Dockerfile agree with the README’s Node.js description
2. 2. `terraform -chdir=terraform fmt -check` passes, showing the infrastructure file meets the packet’s stated local validation
3. 3. The learner can trace the test-to-deploy dependency in the workflow files and identify where OIDC, ECR image publishing, and ECS service updating are configured, without executing a cloud deployment.

## Hints if you are stuck

1. 1. When the project description and active files disagree, compare the actual base image, application entry point, dependencies, and exposed port before changing anything
2. 2. For a formatting-check failure, inspect Terraform whitespace and formatting rather than changing resource behavior
3. 3. If the workflow’s deployment path is unclear, follow job names, `needs` relationships, environment variables, and action inputs from test through image push to ECS update.

## Evidence to capture

A local comparison table or annotated notes covering runtime alignment, Docker build inputs, Terraform formatting, and the workflow test/deploy dependency graph

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
