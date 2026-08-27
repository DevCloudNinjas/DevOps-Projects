# Start Here: project-22-aws-serverless

**Learning focus:** AWS serverless API architecture, Terraform IaC, and CI/CD

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, run `terraform fmt -check` and inspect the README’s local `serverless-api`
prerequisites before considering any cloud-related action.

## Checkpoints

1. 1. The formatting check reports the Terraform files are correctly formatted
2. 1. In `serverless-api`, the learner can identify the Node.js entry point, route definitions, controllers, models, and service layer and can explain how `/healthz` differs from the user and product routes
3. 1. After following the documented local setup in a non-cloud environment, the learner records the test result or a clearly identified dependency/configuration blocker without attempting `terraform apply`.

## Hints if you are stuck

1. 1. If the formatting check fails, compare the reported files with the expected Terraform formatting rather than changing infrastructure behavior
2. 1. If the local Node.js process or tests fail, verify that dependencies were installed from the existing `package.json` and that the command is being run inside `serverless-api`
3. 1. If an API route behaves unexpectedly, trace the path from `routes.js` through its controller and service/model dependencies before changing code.

## Evidence to capture

Terraform format-check output; a brief local component-and-route map; local test or startup output with any
blocker and supporting error text

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
