# Project Picker

Use this page to choose one of the 54 projects by purpose instead of scrolling the whole repository. The root README remains the full catalog; this picker is a student-facing map for deciding what to build next.

## Fast Decision Guide

Start with the smallest project that answers your learning goal. Good public technical docs use clear headings, short tables, and links to deeper pages instead of repeating every detail; this picker follows that pattern so students can decide quickly and then move into the project README.

| If you care most about... | Choose by... | Best first move |
|---|---|---|
| Avoiding surprise bills | `cost_risk: low`, `cloud: []`, or `status: local_lab` | Start with projects 40, 41, 49, 50, 51, 53, or 54. |
| Practicing with real cloud | `cloud: aws` or `cloud: azure` plus `cost_risk` | Use medium-cost labs first; reserve high-cost EKS projects for portfolio work. |
| Having the right access | `cloud`, `iac`, and `ci_cd` fields | Confirm AWS, Azure, GitHub, GitLab, Jenkins, or Azure DevOps credentials before setup. |
| Proving the work is valid | `validation.command` | Run the listed validation before and after changes. Prefer projects with `make validate` or `make test` for repeatable labs. |
| Cleaning up safely | `cost_risk`, `iac`, and project README cleanup notes | For Terraform/OpenTofu projects, identify the destroy command before creating resources. |
| Building a learning path | `deployability` and project purpose | Move from `reference_only` to `local_only`, then containers, Kubernetes, IaC, and CI/CD. |

## How To Choose

1. Pick one section below that matches your current constraint: local-only, beginner, free-tier, security, portfolio, or 2026 lab.
2. Check the project row in the compact table for cost, deployability, and validation.
3. Open the project README and `project.yaml` before running commands.
4. Confirm prerequisites: cloud account, CLI tools, cluster, CI provider, package manager, and any secrets.
5. Run the validation command first. If it fails before you edit anything, fix the local tooling gap or choose a simpler project.
6. For cloud labs, write down the cleanup command before deploy. If cleanup is unclear, treat the project as study-only until the README is improved.

## Recommended Starting Points

| Scenario | Projects | Why these fit |
|---|---|---|
| Local-first, no cloud account | [40](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-40-k8s-dashboard-trivy), [41](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-41-online-boutique-microservices), [49](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-49-text-encryption-cybersecurity), [50](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-50-argocd-gitops-home-lab), [51](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-51-opentelemetry-observability-home-lab), [53](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-53-supply-chain-security-lab), [54](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-54-progressive-delivery-home-lab) | Low cost, no cloud provider in metadata, and good for repeated practice. |
| Beginner-friendly | [03](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-03-linux-fundamentals), [14](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-14-github-actions-android), [40](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-40-k8s-dashboard-trivy), [49](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-49-text-encryption-cybersecurity), [51](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-51-opentelemetry-observability-home-lab) | Lower blast radius and simpler validation than EKS or multi-cloud projects. |
| Free-tier or cloud-aware practice | [11](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-11-aws-2tier-terraform), [22](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-22-aws-serverless), [34](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-34-node-cicd-ecs-terraform-gha), [39](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-39-gha-aws-terraform), [42](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-42-serverless-api-dynamodb), [43](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-43-ecs-fargate-terraform), [52](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-52-opentofu-aws-free-tier-lab) | Cloud practice without starting from the highest-cost EKS catalog entries. Project 52 is the clearest free-tier-oriented lab, but still has `medium` cost risk. |
| Security and DevSecOps | [06](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-06-advanced-cicd-pipeline), [09](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-09-devsecops-netflix-clone), [24](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-24-dotnet-devsecops), [35](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-35-devsecops-pipeline-series), [40](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-40-k8s-dashboard-trivy), [44](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-44-devsecops-101), [45](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-45-jenkins-cicd-argocd-vault), [53](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-53-supply-chain-security-lab) | Metadata marks these as `devsecops` or directly security-focused. |
| Flagship or portfolio-ready | [28](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-28-openai-chatbot-eks), [31](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-31-cloud-native-monitoring), [33](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-33-node-cicd-eks-gha), [35](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-35-devsecops-pipeline-series), [47](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-47-django-saas-ecommerce), [48](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-48-terraform-aws-eks) | Stronger end-to-end story, but several have high cloud cost risk. Validate locally before provisioning. |
| 2026 home labs | [50](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-50-argocd-gitops-home-lab), [51](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-51-opentelemetry-observability-home-lab), [52](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-52-opentofu-aws-free-tier-lab), [53](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-53-supply-chain-security-lab), [54](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-54-progressive-delivery-home-lab) | Modern platform topics: GitOps, observability, OpenTofu, supply-chain security, and progressive delivery. |

## Learning Path Ladder

| Step | Goal | Suggested projects |
|---|---|---|
| 1 | Fundamentals and local validation | [03](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-03-linux-fundamentals), [49](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-49-text-encryption-cybersecurity) |
| 2 | Containers and app packaging | [04](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-04-django-aws-ecs), [31](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-31-cloud-native-monitoring), [51](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-51-opentelemetry-observability-home-lab) |
| 3 | Kubernetes delivery | [41](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-41-online-boutique-microservices), [50](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-50-argocd-gitops-home-lab), [54](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-54-progressive-delivery-home-lab) |
| 4 | Infrastructure as code | [11](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-11-aws-2tier-terraform), [42](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-42-serverless-api-dynamodb), [52](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-52-opentofu-aws-free-tier-lab) |
| 5 | CI/CD and GitOps | [14](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-14-github-actions-android), [18](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-18-jenkins-java-full-cicd), [33](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-33-node-cicd-eks-gha) |
| 6 | Security and portfolio capstone | [35](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-35-devsecops-pipeline-series), [47](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-47-django-saas-ecommerce), [53](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-53-supply-chain-security-lab) |

## Purpose Filters

| Purpose | Good fit projects |
|---|---|
| First DevOps practice | [03](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-03-linux-fundamentals), [04](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-04-django-aws-ecs), [10](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-10-dotnet-azure-devops), [49](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-49-text-encryption-cybersecurity) |
| Local-first home labs | [40](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-40-k8s-dashboard-trivy), [41](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-41-online-boutique-microservices), [50](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-50-argocd-gitops-home-lab), [51](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-51-opentelemetry-observability-home-lab), [53](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-53-supply-chain-security-lab), [54](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-54-progressive-delivery-home-lab) |
| AWS infrastructure | [01](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-01-java-aws-3tier), [02](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-02-aws-vpc-architecture), [11](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-11-aws-2tier-terraform), [37](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-37-eks-terraform-provision), [43](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-43-ecs-fargate-terraform), [46](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-46-eks-cluster-terraform-advanced), [48](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-48-terraform-aws-eks), [52](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-52-opentofu-aws-free-tier-lab) |
| Kubernetes application delivery | [05](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-05-docker-jenkins-k8s), [08](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-08-2048-game-eks), [16](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-16-jenkins-argocd-k8s), [27](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-27-reddit-eks-argocd), [29](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-29-voting-app-argocd), [41](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-41-online-boutique-microservices), [50](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-50-argocd-gitops-home-lab), [54](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-54-progressive-delivery-home-lab) |
| CI/CD practice | [14](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-14-github-actions-android), [18](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-18-jenkins-java-full-cicd), [21](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-21-aws-codepipeline), [26](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-26-terraform-gitlab-cicd), [33](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-33-node-cicd-eks-gha), [34](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-34-node-cicd-ecs-terraform-gha), [39](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-39-gha-aws-terraform) |
| DevSecOps and supply chain | [06](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-06-advanced-cicd-pipeline), [09](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-09-devsecops-netflix-clone), [13](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-13-zomato-clone-devsecops), [24](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-24-dotnet-devsecops), [35](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-35-devsecops-pipeline-series), [44](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-44-devsecops-101), [45](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-45-jenkins-cicd-argocd-vault), [53](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-53-supply-chain-security-lab) |

## Compact Project Table

| # | Project | Purpose | Deployability | Cost |
|---|---|---|---|---|
| 01 | [Java Application on AWS 3-Tier Architecture](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-01-java-aws-3tier) | AWS, Terraform, app infrastructure | `iac_ready` | high |
| 02 | [Scalable AWS VPC Architecture](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-02-aws-vpc-architecture) | AWS networking reference | `reference_only` | medium |
| 03 | [Linux Fundamentals for Cloud and DevOps](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-03-linux-fundamentals) | Linux and shell basics | `reference_only` | low |
| 04 | [Django Application on AWS ECS and ECR](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-04-django-aws-ecs) | Containers on AWS | `container_ready` | medium |
| 05 | [Java App with Docker, Jenkins, and Kubernetes](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-05-docker-jenkins-k8s) | Jenkins and Kubernetes delivery | `ci_cd_ready` | medium |
| 06 | [Advanced CI/CD Pipeline with DevOps Tools](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-06-advanced-cicd-pipeline) | Jenkins, Kubernetes, SonarQube | `ci_cd_ready` | medium |
| 07 | [Azure DevOps Journey with AKS and Terraform](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-07-azure-devops-aks-terraform) | Azure, AKS, Terraform | `ci_cd_ready` | high |
| 08 | [2048 Game on Amazon EKS](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-08-2048-game-eks) | Simple EKS workload | `kubernetes_ready` | medium |
| 09 | [Netflix Clone DevSecOps CI/CD with Monitoring](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-09-devsecops-netflix-clone) | DevSecOps pipeline | `ci_cd_ready` | medium |
| 10 | [.NET CI/CD with Azure App Service](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-10-dotnet-azure-devops) | Azure App Service CI/CD | `reference_only` | medium |
| 11 | [Two-Tier AWS Infrastructure with Terraform](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-11-aws-2tier-terraform) | Terraform AWS infrastructure | `iac_ready` | medium |
| 12 | [Super Mario on Kubernetes with Terraform](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-12-super-mario-k8s) | Kubernetes deployment guide | `reference_only` | medium |
| 13 | [Zomato Clone Secure DevSecOps Deployment](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-13-zomato-clone-devsecops) | DevSecOps reference | `reference_only` | medium |
| 14 | [Android CI/CD with GitHub Actions](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-14-github-actions-android) | GitHub Actions basics | `ci_cd_ready` | low |
| 15 | [E-Commerce Three-Tier App on EKS with Helm](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-15-ecommerce-eks-helm) | EKS and Helm reference | `reference_only` | high |
| 16 | [Jenkins and Argo CD Kubernetes Deployment](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-16-jenkins-argocd-k8s) | GitOps delivery reference | `reference_only` | medium |
| 17 | [Deploying an App to AKS with Azure DevOps](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-17-aks-azure-devops) | AKS delivery reference | `reference_only` | medium |
| 18 | [Java Full CI/CD with Jenkins, SonarQube, Argo CD, Helm, and Kubernetes](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-18-jenkins-java-full-cicd) | Full Jenkins delivery | `ci_cd_ready` | medium |
| 19 | [EKS Cluster and App Delivery with Jenkins and Terraform](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-19-eks-jenkins-terraform) | EKS, Jenkins, Terraform | `ci_cd_ready` | high |
| 20 | [Azure DevOps Terraform Pipeline](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-20-azure-terraform-pipeline) | Azure Terraform pipeline | `ci_cd_ready` | medium |
| 21 | [AWS CodePipeline Video Streaming App](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-21-aws-codepipeline) | AWS native CI/CD | `ci_cd_ready` | medium |
| 22 | [AWS Fully Serverless Architecture with CI/CD](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-22-aws-serverless) | Serverless Terraform | `iac_ready` | medium |
| 23 | [Swiggy Clone Blue-Green ECS Deployment](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-23-swiggy-clone-ecs) | ECS blue-green delivery | `ci_cd_ready` | medium |
| 24 | [DotNet Monitoring DevSecOps Pipeline](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-24-dotnet-devsecops) | Monitoring and DevSecOps | `ci_cd_ready` | medium |
| 25 | [Petshop Java DevSecOps Deployment](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-25-petshop-devsecops) | DevSecOps study guide | `reference_only` | medium |
| 26 | [AWS Infrastructure with Terraform and GitLab CI/CD](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-26-terraform-gitlab-cicd) | GitLab CI and Terraform | `ci_cd_ready` | medium |
| 27 | [Reddit App on EKS with Argo CD and Monitoring](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-27-reddit-eks-argocd) | EKS GitOps reference | `reference_only` | medium |
| 28 | [OpenAI Chatbot UI on EKS with Jenkins and Terraform](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-28-openai-chatbot-eks) | Flagship DevSecOps platform delivery | `ci_cd_ready` | high |
| 29 | [Three-Tier Voting App with Argo CD and Azure DevOps](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-29-voting-app-argocd) | Azure GitOps reference | `reference_only` | medium |
| 30 | [Blog App on EKS with Jenkins and Security Tools](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-30-blog-app-eks) | EKS security pipeline | `ci_cd_ready` | high |
| 31 | [Cloud Native Monitoring App](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-31-cloud-native-monitoring) | Observability app | `container_ready` | medium |
| 32 | [Tetris DevSecOps Kubernetes Pipeline](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-32-tetris-devsecops-k8s) | Kubernetes DevSecOps | `ci_cd_ready` | high |
| 33 | [Node CI/CD to EKS with GitHub Actions](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-33-node-cicd-eks-gha) | GitHub Actions to EKS | `ci_cd_ready` | high |
| 34 | [Node CI/CD to ECS with Terraform and GitHub Actions](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-34-node-cicd-ecs-terraform-gha) | GitHub Actions to ECS | `ci_cd_ready` | medium |
| 35 | [Progressive DevSecOps Pipeline Series](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-35-devsecops-pipeline-series) | Multi-stage DevSecOps | `ci_cd_ready` | medium |
| 36 | [AWS Real-Time Dev to Pre-Prod to Production Deployment](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-36-aws-realtime-deployment) | AWS environment promotion | `ci_cd_ready` | medium |
| 37 | [Provision EKS Cluster with Terraform](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-37-eks-terraform-provision) | EKS provisioning | `iac_ready` | high |
| 38 | [Docker and Terraform Three-Tier Architecture](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-38-docker-terraform-3tier) | Docker plus Terraform | `iac_ready` | high |
| 39 | [GitHub Actions with AWS and Terraform](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-39-gha-aws-terraform) | Terraform automation | `ci_cd_ready` | medium |
| 40 | [Kubernetes Dashboard with Trivy](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-40-k8s-dashboard-trivy) | Local Kubernetes security dashboard | `local_only` | low |
| 41 | [Online Boutique Microservices Assignment](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-41-online-boutique-microservices) | Local microservices on Kubernetes | `kubernetes_ready` | low |
| 42 | [Serverless REST API with DynamoDB](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-42-serverless-api-dynamodb) | Serverless API IaC | `iac_ready` | medium |
| 43 | [Scalable Web App on ECS Fargate with Terraform](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-43-ecs-fargate-terraform) | ECS Fargate IaC | `iac_ready` | medium |
| 44 | [DevSecOps 101 Spring Boot Pipeline](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-44-devsecops-101) | Intro DevSecOps pipeline | `ci_cd_ready` | medium |
| 45 | [Jenkins CI/CD with Argo CD and Vault](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-45-jenkins-cicd-argocd-vault) | Jenkins, Argo CD, Vault | `ci_cd_ready` | medium |
| 46 | [Advanced EKS Cluster with Terraform Modules](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-46-eks-cluster-terraform-advanced) | Advanced EKS IaC | `iac_ready` | high |
| 47 | [Django Multitenant SaaS Ecommerce](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-47-django-saas-ecommerce) | SaaS app platform | `container_ready` | high |
| 48 | [Terraform AWS EKS Provisioning](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-48-terraform-aws-eks) | EKS IaC flagship | `iac_ready` | high |
| 49 | [Text Encryption Cybersecurity Demo](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-49-text-encryption-cybersecurity) | Security coding basics | `local_only` | low |
| 50 | [ArgoCD GitOps Home Lab](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-50-argocd-gitops-home-lab) | Local GitOps | `kubernetes_ready` | low |
| 51 | [OpenTelemetry Observability Home Lab](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-51-opentelemetry-observability-home-lab) | Local observability | `container_ready` | low |
| 52 | [OpenTofu AWS Free-Tier Lab](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-52-opentofu-aws-free-tier-lab) | Free-tier IaC practice | `iac_ready` | medium |
| 53 | [Supply Chain Security Lab](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-53-supply-chain-security-lab) | SBOM, Trivy, Cosign | `ci_cd_ready` | low |
| 54 | [Progressive Delivery Home Lab](https://github.com/DevCloudNinjas/DevOps-Projects/tree/master/project-54-progressive-delivery-home-lab) | Canary delivery | `kubernetes_ready` | low |

## Reading the Fields

| Field | How to use it |
|---|---|
| `reference_only` | Study first; good for architecture, screenshots, or tool sequence learning. |
| `local_only` | Safest for quick practice without cloud spend. |
| `container_ready` | Best when learning Docker, Compose, image builds, or app packaging. |
| `kubernetes_ready` | Best when learning manifests, services, GitOps, and cluster behavior. |
| `iac_ready` | Best when learning Terraform, OpenTofu, VPCs, EKS, ECS, and serverless infrastructure. |
| `ci_cd_ready` | Best when learning Jenkins, GitHub Actions, GitLab CI, Azure DevOps, Argo CD, or CodePipeline. |
