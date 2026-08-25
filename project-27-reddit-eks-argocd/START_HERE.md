# Start Here: project-27-reddit-eks-argocd

**Learning focus:** DevSecOps GitOps deployment and monitoring with Jenkins, Argo CD, Amazon EKS, Prometheus, and Grafana

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

Read the README locally and create a no-execution flow map linking Jenkins scanning and image tagging to the Kubernetes manifests, Argo CD reconciliation, and Prometheus/Grafana monitoring.

## Checkpoints

1. 1. Produce a labeled diagram or notes that distinguish Jenkins, the immutable build-number image tag, the K8s/ manifest source, Argo CD, EKS, and the Prometheus/Grafana monitoring path
2. 2. Annotate the README's stated handoffs, including the deployment manifest update and the Argo CD application's repoURL, path K8s/, targetRevision HEAD, and default Kubernetes destination
3. 3. Submit a local validation checklist that names the evidence expected at each stage: scan outputs, Argo CD sync and health state, Reddit workload status, and observable monitoring metrics, without running cloud commands.

## Hints if you are stuck

1. 1. If the workflow is confusing, trace the desired state from Git rather than starting with the cluster, and identify which component is described as continuously reconciling it
2. 2. If image-version behavior is unclear, compare the README's warning about latest with its description of the Jenkins build-number tag and locate where that tag is said to be written
3. 3. If monitoring evidence is incomplete, separate Prometheus/Grafana installation, service exposure, data-source configuration, and metric interpretation into distinct checks.

## Evidence to capture

Annotated local workflow map and staged validation checklist covering security scans, immutable image tagging, Argo CD reconciliation, Reddit deployment, and Prometheus/Grafana observations

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
