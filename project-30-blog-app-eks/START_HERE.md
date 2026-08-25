# Start Here: project-30-blog-app-eks

**Learning focus:** DevSecOps CI/CD for a Spring Boot blogging app on Kubernetes/EKS

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, inspect `app/pom.xml`, `app/Dockerfile`, `app/Jenkinsfile`, `app/deployment-service.yml`, and `app/EKS_Terraform/main.tf` locally, then write down how source code, image build, pipeline stages, Kubernetes resources, and Terraform infrastructure connect before running anything.

## Checkpoints

1. 1. The student can identify the Spring Boot/Maven build entry point and explain what the Dockerfile packages without changing the files
2. 2. The student can trace the Jenkins pipeline stages from checkout and Maven compilation through Trivy/SonarQube checks and image publication, noting the required tool and credential names
3. 3. The student can map `deployment-service.yml` and `RBAC.md` to the `webapps` namespace, Jenkins service account permissions, application deployment, and service exposure, and relate the Terraform files to EKS infrastructure without applying them.

## Hints if you are stuck

1. 1. If the pipeline structure is unclear, compare the stage names and configured tool labels in `app/Jenkinsfile` with the Maven project metadata in `app/pom.xml`
2. 2. If Kubernetes resources do not seem to fit together, check namespace, service-account, selector, labels, image, and container-port fields across `app/RBAC.md` and `app/deployment-service.yml`
3. 3. If Terraform variables or outputs are confusing, trace each referenced variable and output across `app/EKS_Terraform/main.tf`, `variables.tf`, and `output.tf` before considering any command execution.

## Evidence to capture

Annotated local dependency map plus a dry-run pipeline/Kubernetes flow diagram and a short explanation of the relevant files, stages, namespaces, selectors, ports, credentials, and Terraform inputs/outputs

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
