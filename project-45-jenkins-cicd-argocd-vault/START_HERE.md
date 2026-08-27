# Start Here: project-45-jenkins-cicd-argocd-vault

**Learning focus:** DevSecOps CI/CD pipeline integration with Jenkins, Docker, Kubernetes, Argo CD, and Vault

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

Read the readme pipeline-flow section and trace the existing Jenkinsfile and application files locally,
without installing tools, contacting cloud services, or changing credentials.

## Checkpoints

1. 1. Identify and record the local application, Maven test, Dockerfile, Jenkinsfile, and project.yaml roles, then map them to the README's CI/CD stages
2. 1. Explain the expected handoff from a Jenkins build and test through SonarQube/Trivy checks and image publication using the README's stated sequence, without running it
3. 1. Produce a local dry-run review showing where a successful pipeline would update a Kubernetes image tag and where Argo CD would observe the resulting manifest change, without deploying to Kubernetes.

## Hints if you are stuck

1. 1. If the project flow seems unclear, compare the numbered readme pipeline steps with the stage names and commands in Jenkinsfile rather than starting from the cloud prerequisites
2. 1. If a stage's input or output is ambiguous, inspect the neighboring Maven, Dockerfile, Java source, application.properties, and project.yaml files for names and paths
3. 1. If you encounter a credentials or endpoint question, mark it as an instructor-controlled configuration dependency and do not substitute real AWS, Docker Hub, Slack, SonarQube, Artifactory, Jenkins, Argo CD, or Vault secrets.

## Evidence to capture

Annotated local pipeline map, file-to-stage trace, and a dry-run explanation of build/test, security checks,
image-tag update, pull request, and Argo CD handoff

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
