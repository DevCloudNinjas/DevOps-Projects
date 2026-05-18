# Project 54: Progressive Delivery Home Lab

Local Kubernetes lab for learning canary releases and automated rollback with Argo Rollouts.

## What You Learn

- Why progressive delivery is safer than all-at-once deploys
- How canary steps work
- How service selectors route traffic during rollout
- How to pause, promote, and abort a rollout

## Home Lab Cost

Local only. No cloud account required.

## Prerequisites

- Docker
- Kind or Minikube
- `kubectl`
- Argo Rollouts kubectl plugin, optional but recommended

## Quick Start

```bash
kind create cluster --name rollout-lab
kubectl create namespace argo-rollouts
kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml
kubectl wait --for=condition=available --timeout=180s deployment/argo-rollouts -n argo-rollouts
kubectl apply -f rollouts/
kubectl argo rollouts get rollout demo-rollout -n progressive-delivery --watch
```

Change the image tag in `rollouts/rollout.yaml`, apply it again, and watch the canary steps.

## Clean Up

```bash
kind delete cluster --name rollout-lab
```

## Student Exercises

- Add an analysis template.
- Introduce a bad image tag and abort the rollout.
- Change canary weights.
- Compare this with a normal Kubernetes Deployment.

