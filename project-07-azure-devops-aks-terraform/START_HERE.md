# Start Here: project-07-azure-devops-aks-terraform

**Learning focus:** Azure DevOps CI/CD, Terraform infrastructure as code, Docker/AKS delivery, testing, and monitoring

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

Start locally by reading `README.md` and `prerequisites.md`, then trace the numbered lab sequence and open `labs/1-Initial-Setup/README.md` without running any Azure, Terraform, or deployment command.

## Checkpoints

1. 1. Produce a one-page local map linking labs 1–7 to their stated outputs, including remote Terraform state, AKS/ACR infrastructure, application delivery, CI/CD, Inspec tests, and monitoring
2. 2. Annotate the provided `lab2pipeline.yaml`, Terraform modules, and later pipeline/manifests to identify inputs, module boundaries, and hand-offs without changing them
3. 3. Build and run the sample ASP.NET application only through the packet’s local Docker exercise and record the resulting image/container observations as a dry-run readiness artifact, stopping before any provider-backed action.

## Hints if you are stuck

1. 1. If the lab sequence feels unclear, compare each numbered lab’s README with the root README’s learning objectives and named prerequisites
2. 2. If a pipeline or Terraform file is difficult to follow, first mark where variables, modules, service connections, and output values cross file boundaries
3. 3. If the local Docker check does not behave as expected, verify that the command is being run from the directory containing the referenced `Dockerfile` and distinguish image creation from container execution.

## Evidence to capture

Local lab-sequence map, annotated dependency/data-flow notes, and a local Docker image/container observation log

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
