# Start Here: project-44-devsecops-101

**Learning focus:** Local DevSecOps CI/CD for a Spring Boot application

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, inspect README.md, Jenkinsfile, Dockerfile, and spring-boot-deployment.yaml, then run
the packet's local validation command ./mvnw test without configuring Jenkins, AWS, Docker Hub, Vault, Slack,
or Kubernetes.

## Checkpoints

1. 1. ./mvnw test completes and produces the Maven test output for DemoApplicationTests
2. 1. The student can trace the Jenkinsfile stages from Git checkout through Maven/JUnit, SonarQube, Docker/Trivy, report upload, image push, and Kubernetes deployment
3. 1. The student can match Dockerfile and spring-boot-deployment.yaml to the intended Spring Boot image-and-service flow without using external credentials or live infrastructure.

## Hints if you are stuck

1. 1. If the first check fails, distinguish a Maven/dependency or Java-version problem from a test assertion failure by reading the earliest actionable error and the surefire output path
2. 1. For a pipeline-reading mismatch, compare each stage name and shell command with the pipeline-flow sequence in README.md
3. 1. For manifest or image questions, check whether the image reference, container port, service type, and declared application settings agree across Dockerfile, spring-boot-deployment.yaml, and application.properties.

## Evidence to capture

Local ./mvnw test result plus annotated stage-to-file mapping and a reviewed Docker/Kubernetes configuration
comparison

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
