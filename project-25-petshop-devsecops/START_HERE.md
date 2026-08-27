# Start Here: project-25-petshop-devsecops

**Learning focus:** Java application DevSecOps CI/CD with Docker, Kubernetes, security scanning, and
infrastructure automation

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the project folder, read the readme and make a local checklist mapping the Petshop pipeline stages—Maven
build/test, Docker image, SonarQube/Trivy checks, and Kubernetes manifests—without applying the Terraform or
cloud commands.

## Checkpoints

1. 1. The learner can identify and explain the intended flow from Java source through Maven, Jenkins, Docker, security gates, and Kubernetes using a labeled local diagram or checklist
2. 1. The learner can show a local, non-cloud build/test or configuration review with the relevant Maven/Jenkins/Docker/Kubernetes names and placeholders preserved rather than real credentials
3. 1. The learner can inspect the README's hardened-pipeline claims and produce evidence that the proposed image uses an unprivileged Tomcat runtime, an immutable BUILD_NUMBER tag, and a Trivy vulnerability gate, while explicitly marking any unverified runtime result.

## Hints if you are stuck

1. 1. If the starting point is unclear, begin with the README's Pipeline Overview and compare each numbered stage with the later detailed sections before changing anything
2. 1. If a Jenkins example does not line up with the described pipeline, check tool names, stage order, repository placeholders, and environment variables for consistency
3. 1. If a security or deployment claim cannot be demonstrated locally, separate configuration evidence from execution evidence and record the missing prerequisite instead of opening the AWS or public-IP steps.

## Evidence to capture

Annotated local pipeline map, sanitized configuration review, and a short verification log distinguishing
readme claims from locally observed results

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
