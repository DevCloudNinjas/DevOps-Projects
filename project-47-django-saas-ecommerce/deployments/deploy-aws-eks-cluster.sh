#!/bin/bash

# Variables
KUBECONFIG="/root/.kube/config"
NAMESPACE="prodxcloud-django-web"
DOCKER_IMAGE="joelwembo/prodxcloud-django-web:latest"
DEPLOYMENT_NAME="prodxcloud-django-web"
SERVICE_NAME="mycluster"
PORT=8585

# Set KUBECONFIG environment variable
export KUBECONFIG="$KUBECONFIG"

# Apply Kubernetes manifests
kubectl apply -f deployments/k8s/deployment.yaml

# Update the Docker image in the deployment
kubectl set image deployment/$DEPLOYMENT_NAME $DEPLOYMENT_NAME=$DOCKER_IMAGE -n $NAMESPACE

# Expose the deployment as a service
kubectl expose deployment $DEPLOYMENT_NAME --type=LoadBalancer --port=80 --target-port=$PORT -n $NAMESPACE --name=prodxcloud-django-web
