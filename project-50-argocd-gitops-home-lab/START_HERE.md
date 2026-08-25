# Start Here: project-50-argocd-gitops-home-lab

**Learning focus:** Local Kubernetes GitOps with ArgoCD reconciliation

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, run `make validate` to locally parse the Kubernetes and ArgoCD YAML before creating a cluster.

## Checkpoints

1. 1. `make validate` completes as a local YAML check without requiring a cluster or ArgoCD CRD
2. 2. After the local Kind workflow is started, the `gitops-lab` cluster and ArgoCD installation become available and `argocd/application.yaml` can be applied
3. 3. `kubectl get applications -n argocd` shows the Application resource progressing toward a healthy, synchronized `hello-gitops` Deployment and Service.

## Hints if you are stuck

1. 1. If validation or application creation fails, first distinguish a YAML parsing issue from the absence of the ArgoCD Application CRD
2. 2. If synchronization cannot reach the repository, inspect the `repoURL` and branch in `argocd/application.yaml` rather than changing the Kubernetes workload first
3. 3. If the application namespace is absent, check whether the manifest still requests automatic namespace creation and whether the local cluster context is the intended one.

## Evidence to capture

Validation output plus terminal captures of ArgoCD Application status and the reconciled hello-gitops Deployment/Service in the local cluster

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
