# Project 50: ArgoCD GitOps Home Lab

Student-friendly GitOps lab for running a simple Kubernetes app locally with Kind or Minikube and deploying it through ArgoCD.

## What You Learn

- How GitOps differs from manual `kubectl apply`
- How ArgoCD watches Git and reconciles cluster state
- How to structure app manifests for dev/staging style promotion
- How sync, drift, rollback, and health checks work

## Home Lab Cost

Local only. No cloud account required.

## Prerequisites

- Docker
- Kind or Minikube
- `kubectl`
- ArgoCD CLI, optional but useful

## Lab Flow

1. Create a local cluster.
2. Install ArgoCD.
3. Apply the sample app manifests once to understand the app.
4. Apply the ArgoCD `Application` manifest.
5. Change the image tag or replica count in Git.
6. Watch ArgoCD reconcile the cluster.

## Quick Start

```bash
kind create cluster --name gitops-lab
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl wait --for=condition=available --timeout=180s deployment/argocd-server -n argocd
kubectl apply -f argocd/application.yaml
kubectl get applications -n argocd
```

Update `argocd/application.yaml` so `repoURL` points to your fork before using it with a real GitHub repo.

## Local Manifest Check

```bash
kubectl apply --dry-run=client -f k8s/
```

## Clean Up

```bash
kind delete cluster --name gitops-lab
```

## Stretch Goals

- Add a `staging` overlay.
- Add ArgoCD sync waves.
- Add image automation.
- Break the deployment and use ArgoCD rollback.

