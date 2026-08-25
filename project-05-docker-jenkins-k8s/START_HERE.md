# Start Here: project-05-docker-jenkins-k8s

**Learning focus:** Java web application containerization and CI/CD with Docker, Jenkins, Maven, and Kubernetes

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

In the local project copy, inspect `hello-world/Dockerfile`, `hello-world/pom.xml`, and the two Kubernetes manifests, then write down how the Maven artifact, container image, deployment, and service connect before running anything.

## Checkpoints

1. 1. The student can identify the Java/Maven modules and the expected WAR artifact, and explain the Dockerfile's base image, restricted user, and artifact-copy steps
2. 2. A local, non-cloud validation shows the Kubernetes deployment and service YAML parses successfully with the stated CPU and memory bounds
3. 3. The student can trace the intended Jenkins flow from source checkout through Maven build and Docker image publication to Kubernetes deployment, with evidence mapped to the relevant files and without changing the supplied materials.

## Hints if you are stuck

1. 1. If the project structure is unclear, start with the two `pom.xml` files and follow which module produces the web application artifact
2. 2. If a manifest validation fails, compare its names, selectors, ports, image reference, and resource fields with the labels and container definition rather than changing several fields at once
3. 3. If the CI/CD flow does not line up, distinguish Jenkins build steps, Docker image contents, and Kubernetes runtime settings, and inspect one boundary at a time.

## Evidence to capture

Annotated local file map plus a dry-run validation result for both Kubernetes manifests and a concise Jenkins-to-Docker-to-Kubernetes flow trace

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
