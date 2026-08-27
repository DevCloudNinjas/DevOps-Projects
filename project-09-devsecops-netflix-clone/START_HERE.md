# Start Here: project-09-devsecops-netflix-clone

**Learning focus:** DevSecOps CI/CD pipeline security and observability for a containerized Netflix clone

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

Read the local README’s Project Overview and 2026 DevSecOps Enhancements, then make a short checklist of the
Jenkins credentials, build-number image tag, and Trivy gate that the lab is meant to demonstrate.

## Checkpoints

1. 1. Produce a local architecture/checklist showing how Jenkins, Docker, the clone app, Kubernetes, Prometheus, Grafana, Node Exporter, SonarQube, and Trivy fit together
2. 1. Trace the README’s pipeline sequence and identify where the `tmdb-api-key` credential, `${BUILD_NUMBER}` image tag, and mandatory Trivy scan belong without using real credentials or cloud services
3. 1. Validate the intended monitoring evidence locally by documenting the Prometheus targets and metric paths for Node Exporter and Jenkins, plus the Grafana data-source/dashboard checks described in the packet.

## Hints if you are stuck

1. 1. If the pipeline design is unclear, compare the three 2026 enhancements with the older numbered steps and distinguish secret injection from ordinary application configuration
2. 1. If a monitoring target does not appear, check the target address, metric path, and whether the Prometheus configuration passes `promtool check config` before considering a reload
3. 1. If a security gate behaves unexpectedly, inspect the exact image tag and scan threshold used by the pipeline rather than changing the gate or exposing a secret.

## Evidence to capture

Annotated local pipeline diagram/checklist, redacted Jenkinsfile stage-to-enhancement mapping, Prometheus
target/config validation notes, and screenshots or logs from a safe local/mock run

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
