# DevSecOps Pipeline Series — Progressive CI/CD with Security

A 6-step progressive DevSecOps pipeline built with Jenkins, Terraform, Kubernetes, and security scanning tools.

Each step builds on the previous one, adding more security and deployment capabilities.

## Steps

| Step | Folder | Topic | Tools Added |
|------|--------|-------|-------------|
| 1 | [step-1-infra-creation](./step-1-infra-creation) | AWS Infrastructure with Terraform | Terraform, Jenkins, EC2, K8s |
| 2 | [step-2-sast-sonarcloud](./step-2-sast-sonarcloud) | Static Application Security Testing | SonarCloud |
| 3 | [step-3-sca-snyk](./step-3-sca-snyk) | Software Composition Analysis | Snyk |
| 4 | [step-4-docker-ecr](./step-4-docker-ecr) | Docker Build & Push to ECR | Docker, AWS ECR |
| 5 | [step-5-deploy-k8s](./step-5-deploy-k8s) | Deploy to Kubernetes | K8s Deployment |
| 6 | [step-6-dast-zap-e2e](./step-6-dast-zap-e2e) | Dynamic Testing & E2E | OWASP ZAP, E2E Tests |

## Architecture

```
Code Commit → Jenkins Pipeline
  → Step 1: Provision Infrastructure (Terraform)
  → Step 2: SAST Scan (SonarCloud)
  → Step 3: SCA Scan (Snyk)
  → Step 4: Docker Build & Push (ECR)
  → Step 5: Deploy to K8s
  → Step 6: DAST Scan (ZAP) + E2E Tests
```

## Difficulty
🔴 Advanced

## Key Technologies
Jenkins, Terraform, Kubernetes, Docker, SonarCloud, Snyk, OWASP ZAP, AWS ECR, AWS EKS
