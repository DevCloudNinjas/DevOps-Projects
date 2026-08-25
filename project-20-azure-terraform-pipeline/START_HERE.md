# Start Here: project-20-azure-terraform-pipeline

**Learning focus:** Terraform infrastructure-as-code and Azure DevOps CI/CD pipeline structure

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

Open `README.md`, `deploy/tfdemo-env01-terraform.yml`, `deploy/templates/terraform-template.yml`, and the `terraform/` files locally, then run only the packet’s stated validation command `terraform -chdir=terraform fmt -check`.

## Checkpoints

1. 1. The learner can identify the root pipeline file, reusable template, Terraform provider/backend configuration, variables, resource definitions, and the packet’s local formatting validation command
2. 2. The learner can trace how `tfdemo-env01-terraform.yml` supplies `rootFolder`, `tfvarsFile`, and `adoEnvironment` to the template and how the template separates `Terraform_Plan` from gated `Terraform_Apply`
3. 3. The learner can explain from the code and README that the Terraform resources are one resource group, one Service Bus namespace, and two queues, while documenting the plan/approval flow without running or approving a cloud deployment.

## Hints if you are stuck

1. 1. If the pipeline structure is unclear, start at the file that calls the template and follow each parameter into the template before inspecting the Terraform files
2. 2. If local validation fails, check formatting and working-directory assumptions first, and compare the command with the `validation.command` recorded in `project.yaml`
3. 3. If authentication or backend details seem confusing, distinguish the Terraform backend settings and variable-group names from resource declarations, and do not place secrets in repository files.

## Evidence to capture

Annotated local file map; successful or explained `terraform fmt -check` result; parameter/data-flow notes linking the env01 pipeline to its template and Terraform inputs; a no-cloud plan/approval sequence diagram or written trace

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
