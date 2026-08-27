# Start Here: project-35-devsecops-pipeline-series

**Learning focus:** Local DevSecOps CI/CD security pipeline analysis

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, read the top-level readme and map the six folders into a local checklist without
running Terraform, cloud, deployment, or teardown commands.

## Checkpoints

1. 1. The learner can label the six stages as infrastructure, SAST, SCA, image build/push, Kubernetes deployment, and DAST/end-to-end from the readme
2. 1. The learner can identify the local validation command in project.yaml and distinguish the EasyBuggy Maven/Docker material from the cloud-dependent Terraform and Kubernetes files
3. 1. The learner can produce a stage-by-stage evidence table linking Jenkinsfiles, pom.xml/Dockerfiles, scan tools, and the final ZAP/end-to-end stage without executing live-cloud steps.

## Hints if you are stuck

1. 1. If the sequence feels unclear, compare the readme architecture arrows with the numbered step folders before opening implementation files
2. 1. If a check appears unsafe or cloud-dependent, first classify it by the project.yaml cloud, IaC, and CI/CD fields and look for a local analogue
3. 1. If the EasyBuggy stage is hard to interpret, use its listed Maven/Docker quick-start artifacts and vulnerability categories to explain what the pipeline is meant to observe, not to reproduce attacks.

## Evidence to capture

A local six-stage pipeline map, dependency/tool classification, and recorded result or rationale for the
project.yaml Maven test validation command

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
