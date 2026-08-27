# Start Here: project-42-serverless-api-dynamodb

**Learning focus:** Infrastructure as code for a Node.js serverless REST API backed by DynamoDB

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, read README.md and list the local Terraform and SAM files to map the API, Lambda, and
DynamoDB components before changing anything.

## Checkpoints

1. 1. You can point to the README's stated Lambda/API Gateway/DynamoDB stack and match it to the listed SAM and Terraform files
2. 1. You can run the packet's local validation command `terraform -chdir=terraform fmt -check` and record whether the Terraform formatting passes
3. 1. You can produce a local architecture note showing the GET and PUT controllers, shared helper layer, API definition, and sample product-import script without provisioning resources.

## Hints if you are stuck

1. 1. If the file map feels unclear, group the paths by runtime code, shared helpers, infrastructure definitions, and scripts before tracing relationships
2. 1. If the validation check fails, inspect formatting in the Terraform directory rather than changing application logic
3. 1. If you cannot explain a request path, compare the API definition with the names of the GET and PUT controller files and note the remaining question for the instructor.

## Evidence to capture

Local file-to-component map, recorded Terraform format-check result, and a short request/data-flow diagram or
written trace

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
