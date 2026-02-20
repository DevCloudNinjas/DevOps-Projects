# End-to-End CI/CD Pipeline for Simple Node App Deployment on EKS using GitHub Actions

![github-actions](https://imgur.com/Ctznv2m.png)

## Table of Contents

- [End-to-End CI/CD Pipeline for Simple Node App Deployment on EKS using GitHub Actions](#end-to-end-cicd-pipeline-for-simple-node-app-deployment-on-eks-using-github-actions)
  - [Table of Contents](#table-of-contents)
  - [Repository Structure](#repository-structure)
  - [CI/CD Workflow](#cicd-workflow)
      - [Build Job](#build-job)
      - [Deployment Job](#deployment-job)
  - [Infrastructure Details](#infrastructure-details)
  - [Notifications](#notifications)
  - [GitOps Principles](#gitops-principles)
- [Hit the Star! ⭐](#hit-the-star-)
      - [Author by DevCloud Ninjas](#author-by-devcloud-ninjas)

## Repository Structure

The repository is organized into several key directories:

```
├── app
│   ├── app.py
│   ├── calculator.js
│   ├── calculator.test.js
│   ├── Dockerfile
│   ├── Dockerfile-python
│   ├── index.js
│   └── package.json
├── kustomize
│   ├── base
│   │   ├── deploy.yaml
│   │   ├── ingress.yaml
│   │   ├── kustomization.yaml
│   │   └── svc.yaml
│   └── overlays
│       ├── dev
│       │   ├── deploy-dev.yaml
│       │   ├── ingress-dev.yaml
│       │   ├── kustomization.yaml
│       │   └── svc-dev.yaml
│       ├── prod
│       │   ├── deploy-prod.yaml
│       │   ├── ingress-prod.yaml
│       │   ├── kustomization.yaml
│       │   └── svc-prod.yaml
│       └── staging
│           ├── deploy-staging.yaml
│           ├── ingress-staging.yaml
│           ├── kustomization.yaml
│           └── svc-staging.yaml
├── README.md
├── terraform
│   ├── ingress-nginx.tf
│   ├── main.tf
│   ├── outputs.tf
│   ├── terraform.tf
│   └── variables.tf
└── VERSION
```


## CI/CD Workflow

#### Build Job

The `build` job performs several key tasks:

1. **Environment Setup**: Node.js environment is set up and dependencies are installed.
2. **Run Tests**: Executes unit tests for the application.
3. **Determine Version Increment**: Checks the commit message to determine if the version needs to be incremented using Semantic Versioning scheme.
4. **Docker Build and Push**: Builds a Docker image and pushes it to a registry.

#### Deployment Job

The `deployment` job handles the following:

1. **Terraform Setup**: Initializes Terraform and sets up the backend with different state files.
2. **Terraform Plan and Apply**: Executes `terraform plan` and `terraform apply` to provision environment specific infrastructure.
3. **Kubernetes Configuration**: Configures `kubectl` to interact with the Kubernetes cluster.
4. **Ingress Controller Setup**: Uses Helm to install the ingress controller.
5. **Application Deployment**: Uses `kubectl` to deploy the `Kustomized` application manifests.

## Infrastructure Details

- **Dev Environment**: Uses `t3.small` EC2 instances and deploys a single replica.
- **Staging Environment**: Uses `t3.medium` EC2 instances and deploys three replicas.
- **Prod Environment**: Uses `t3.large` EC2 instances and deploys three replicas.

DNS for all environments is automatically managed via Cloudflare and environment-specific subdomains are assigned and pointed to their respective LB hostname (using CNAME) ie., `dev.afraz.dev`, `staging.afraz.dev` and `prod.afraz.dev`.

## Notifications

Slack notifications are configured to send updates at the end of each job. This provides immediate feedback on the success or failure of the pipeline and also updates on the DNS changes if applicable.

## GitOps Principles

The pipeline adheres to GitOps principles, where Git serves as the single source of truth. Any change to the application or infrastructure is expected to be made through a Git commit.

# Hit the Star! ⭐
***If you are planning to use this repo for learning, please hit the star. Thanks!***

#### Author by [DevCloud Ninjas](https://github.com/DevCloudNinjas)
