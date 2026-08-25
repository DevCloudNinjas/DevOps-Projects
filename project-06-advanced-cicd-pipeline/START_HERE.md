# Start Here: project-06-advanced-cicd-pipeline

**Learning focus:** Advanced DevSecOps CI/CD pipeline integration

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

Read README.md and map the twelve numbered Steps documents to the local Dockerfile, Jenkinsfile, Java tests, Kubernetes manifests, and monitoring configuration without running any provisioning or deployment command.

## Checkpoints

1. 1. Produce a local component map showing how Maven tests and the Jenkinsfile stages relate to the Dockerfile and SonarQube/JFrog configuration
2. 2. Trace the artifact path on paper from the Java application and tests through the uniquely tagged container image and the Kubernetes deployment, namespace, and service manifests
3. 3. Verify that the final review checklist accounts for the Prometheus/Grafana monitoring files and the README's unprivileged-container and immutable-tag security claims.

## Hints if you are stuck

1. 1. If the component map feels unclear, start at the Jenkinsfile stage names and match each stage to the adjacent project file before examining the numbered Step notes
2. 2. If the artifact path breaks, compare the image name/tag and registry references across the Jenkinsfile, Dockerfile, and deployment manifest rather than changing credentials
3. 3. If monitoring evidence is missing, inspect the Step-12 description and the service type stated in the README, then record the discrepancy or confirmation without attempting cluster access.

## Evidence to capture

Local annotated pipeline/component map, artifact-flow trace, and a checklist of test, security, deployment-manifest, and monitoring claims

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
