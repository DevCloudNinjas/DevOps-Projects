# Start Here: project-17-aks-azure-devops

**Learning focus:** AKS container deployment and Azure DevOps CI/CD pipeline integration

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

Open the local README.md and annotate the architecture paragraph by labeling GitHub, Azure DevOps, ACR, AKS, and Azure Active Directory as source, pipeline, registry, runtime, and identity components.

## Checkpoints

1. 1. Produce a local component map that connects GitHub source to Azure DevOps, ACR, AKS, and the Azure identity/service-principal role
2. 2. Trace the README’s documented sequence from project setup through image build/push and Kubernetes deployment without running any cloud commands
3. 3. Mark every placeholder, credential-bearing step, and resource-name inconsistency in the README, including the differing ACR names, and explain why each requires instructor review.

## Hints if you are stuck

1. 1. Compare each command’s resource group, cluster, registry, organization, project, and repository names with the names introduced earlier
2. 2. Treat PATs, service-principal output, passwords, and account access as sensitive prerequisites rather than values to invent or commit
3. 3. Use the architecture and Summary sections to check whether your component map explains both the container image path and the Kubernetes service’s external access.

## Evidence to capture

Annotated local README component/sequence map plus a flagged list of placeholders, sensitive inputs, and naming inconsistencies

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
