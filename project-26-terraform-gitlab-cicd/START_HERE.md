# Start Here: project-26-terraform-gitlab-cicd

**Learning focus:** AWS infrastructure as code with Terraform modules and GitLab CI/CD

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, read `README.md`, `.gitlab-ci.yml`, and the Terraform file inventory, then sketch how
the `vpc` and `web` modules connect without running any cloud or deployment command.

## Checkpoints

1. 1. The learner can label the root Terraform files and distinguish the `vpc` module from the `web` module using the project structure
2. 1. A local `terraform fmt -check -recursive` run reports whether the configuration meets the validation command recorded in `project.yaml`
3. 1. The learner can explain the CI/CD stage order (`validate`, `plan`, `apply`, `destroy`) and identify that `apply` and `destroy` are manual gates in the documented pipeline.

## Hints if you are stuck

1. 1. If the file layout is unclear, trace inputs and outputs between the root configuration and the `vpc` and `web` directories before changing resource blocks
2. 1. If formatting validation fails, compare the reported paths with Terraform's formatting conventions and make only local, reviewable edits
3. 1. If the pipeline sequence is confusing, follow the stages in `.gitlab-ci.yml` and separate checks and planning from the two explicitly manual operations.

## Evidence to capture

Annotated module/data-flow sketch, local formatting-check output, and a short explanation of the CI stage
order and manual gates

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
