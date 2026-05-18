# Project Catalog

Machine-readable metadata lives in each top-level `project-*` directory as `project.yaml` and follows `project.schema.json`. The catalog distinguishes learning/reference material from projects that are deployable demos or templates, and flags cloud cost risk before anyone runs infrastructure commands.

## Metadata Format

Required fields: `schema_version`, `project.number`, `project.slug`, `project.name`, `classification`, `status`, `deployability`, `stack`, `cloud`, `iac`, `ci_cd`, `cost_risk`, `security_posture`, `validation.command`, and `notes`.

Classification values are `learning` or `deployable`. Cost risk is `low`, `medium`, or `high`. Security posture is `baseline`, `devsecops`, `hardened`, or `needs_review`.

## Projects

| # | Project | Classification | Status | Deployability | Cloud | Cost | Security | Validation |
|---:|---|---|---|---|---|---|---|---|
| 1 | [Java Application on AWS 3-Tier Architecture](project-01-java-aws-3tier/project.yaml) | deployable | cloud_lab | iac_ready | aws | high | baseline | `terraform -chdir=terraform fmt -check` |
| 2 | [Scalable AWS VPC Architecture](project-02-aws-vpc-architecture/project.yaml) | learning | cloud_lab | reference_only | aws | medium | baseline | `test -f README.md` |
| 3 | [Linux Fundamentals for Cloud and DevOps](project-03-linux-fundamentals/project.yaml) | learning | reference | reference_only | none | low | baseline | `test -f README.md` |
| 4 | [Django Application on AWS ECS and ECR](project-04-django-aws-ecs/project.yaml) | deployable | cloud_lab | container_ready | aws | medium | baseline | `python3 -m compileall .` |
| 5 | [Java App with Docker, Jenkins, and Kubernetes](project-05-docker-jenkins-k8s/project.yaml) | deployable | cloud_lab | ci_cd_ready | aws | medium | baseline | `kubectl apply --dry-run=client -f hello-world/regapp-deploy.yml -f hello-world/regapp-service.yml` |
| 6 | [Advanced CI/CD Pipeline with DevOps Tools](project-06-advanced-cicd-pipeline/project.yaml) | deployable | devsecops_lab | ci_cd_ready | aws | medium | devsecops | `mvn -q -DskipTests=false test` |
| 7 | [Azure DevOps Journey with AKS and Terraform](project-07-azure-devops-aks-terraform/project.yaml) | learning | cloud_lab | ci_cd_ready | azure | high | baseline | `test -f README.md` |
| 8 | [2048 Game on Amazon EKS](project-08-2048-game-eks/project.yaml) | deployable | cloud_lab | kubernetes_ready | aws | medium | baseline | `kubectl apply --dry-run=client -f 2048-deployment.yaml -f mygame-svc.yaml` |
| 9 | [Netflix Clone DevSecOps CI/CD with Monitoring](project-09-devsecops-netflix-clone/project.yaml) | deployable | devsecops_lab | ci_cd_ready | aws | medium | devsecops | `test -f jenkinsfile` |
| 10 | [.NET CI/CD with Azure App Service](project-10-dotnet-azure-devops/project.yaml) | learning | reference | reference_only | azure | medium | baseline | `test -f README.md` |
| 11 | [Two-Tier AWS Infrastructure with Terraform](project-11-aws-2tier-terraform/project.yaml) | deployable | cloud_lab | iac_ready | aws | medium | baseline | `terraform fmt -check` |
| 12 | [Super Mario on Kubernetes with Terraform](project-12-super-mario-k8s/project.yaml) | learning | reference | reference_only | aws | medium | baseline | `test -f README.md` |
| 13 | [Zomato Clone Secure DevSecOps Deployment](project-13-zomato-clone-devsecops/project.yaml) | learning | reference | reference_only | aws | medium | devsecops | `test -f README.md` |
| 14 | [Android CI/CD with GitHub Actions](project-14-github-actions-android/project.yaml) | deployable | ci_lab | ci_cd_ready | none | low | baseline | `./android-demo-app/gradlew -p android-demo-app tasks` |
| 15 | [E-Commerce Three-Tier App on EKS with Helm](project-15-ecommerce-eks-helm/project.yaml) | learning | reference | reference_only | aws | high | baseline | `test -f README.md` |
| 16 | [Jenkins and Argo CD Kubernetes Deployment](project-16-jenkins-argocd-k8s/project.yaml) | learning | reference | reference_only | none | medium | baseline | `test -f README.md` |
| 17 | [Deploying an App to AKS with Azure DevOps](project-17-aks-azure-devops/project.yaml) | learning | reference | reference_only | azure | medium | baseline | `test -f README.md` |
| 18 | [Java Full CI/CD with Jenkins, SonarQube, Argo CD, Helm, and Kubernetes](project-18-jenkins-java-full-cicd/project.yaml) | deployable | devsecops_lab | ci_cd_ready | none | medium | devsecops | `mvn -q -f spring-boot-app/pom.xml test` |
| 19 | [EKS Cluster and App Delivery with Jenkins and Terraform](project-19-eks-jenkins-terraform/project.yaml) | deployable | cloud_lab | ci_cd_ready | aws | high | baseline | `terraform -chdir=tf-aws-eks fmt -check` |
| 20 | [Azure DevOps Terraform Pipeline](project-20-azure-terraform-pipeline/project.yaml) | deployable | cloud_lab | ci_cd_ready | azure | medium | baseline | `terraform -chdir=terraform fmt -check` |
| 21 | [AWS CodePipeline Video Streaming App](project-21-aws-codepipeline/project.yaml) | deployable | cloud_lab | ci_cd_ready | aws | medium | baseline | `npm run build` |
| 22 | [AWS Fully Serverless Architecture with CI/CD](project-22-aws-serverless/project.yaml) | deployable | cloud_lab | iac_ready | aws | medium | baseline | `terraform fmt -check` |
| 23 | [Swiggy Clone Blue-Green ECS Deployment](project-23-swiggy-clone-ecs/project.yaml) | deployable | cloud_lab | ci_cd_ready | aws | medium | devsecops | `npm --prefix Swiggy_clone install --package-lock-only --ignore-scripts` |
| 24 | [DotNet Monitoring DevSecOps Pipeline](project-24-dotnet-devsecops/project.yaml) | deployable | devsecops_lab | ci_cd_ready | none | medium | devsecops | `dotnet test DotNet-monitoring` |
| 25 | [Petshop Java DevSecOps Deployment](project-25-petshop-devsecops/project.yaml) | learning | reference | reference_only | none | medium | devsecops | `test -f README.md` |
| 26 | [AWS Infrastructure with Terraform and GitLab CI/CD](project-26-terraform-gitlab-cicd/project.yaml) | deployable | cloud_lab | ci_cd_ready | aws | medium | baseline | `terraform fmt -check -recursive` |
| 27 | [Reddit App on EKS with Argo CD and Monitoring](project-27-reddit-eks-argocd/project.yaml) | learning | reference | reference_only | aws | medium | devsecops | `test -f README.md` |
| 28 | [OpenAI Chatbot UI on EKS with Jenkins and Terraform](project-28-openai-chatbot-eks/project.yaml) | deployable | devsecops_lab | ci_cd_ready | aws | high | devsecops | `npm --prefix Chatbot-UI test` |
| 29 | [Three-Tier Voting App with Argo CD and Azure DevOps](project-29-voting-app-argocd/project.yaml) | learning | reference | reference_only | azure | medium | baseline | `test -f README.md` |
| 30 | [Blog App on EKS with Jenkins and Security Tools](project-30-blog-app-eks/project.yaml) | deployable | devsecops_lab | ci_cd_ready | aws | high | devsecops | `mvn -q -f app/pom.xml test` |
| 31 | [Cloud Native Monitoring App](project-31-cloud-native-monitoring/project.yaml) | deployable | local_validated | container_ready | aws | medium | hardened | `make test` |
| 32 | [Tetris DevSecOps Kubernetes Pipeline](project-32-tetris-devsecops-k8s/project.yaml) | deployable | devsecops_lab | ci_cd_ready | aws | high | devsecops | `npm --prefix Tetris-V1 test --if-present` |
| 33 | [Node CI/CD to EKS with GitHub Actions](project-33-node-cicd-eks-gha/project.yaml) | deployable | local_validated | ci_cd_ready | aws | high | hardened | `make test` |
| 34 | [Node CI/CD to ECS with Terraform and GitHub Actions](project-34-node-cicd-ecs-terraform-gha/project.yaml) | deployable | cloud_lab | ci_cd_ready | aws | medium | baseline | `terraform -chdir=terraform fmt -check` |
| 35 | [Progressive DevSecOps Pipeline Series](project-35-devsecops-pipeline-series/project.yaml) | deployable | devsecops_lab | ci_cd_ready | aws | medium | devsecops | `mvn -q -f step-2-sast-sonarcloud/pom.xml test` |
| 36 | [AWS Real-Time Dev to Pre-Prod to Production Deployment](project-36-aws-realtime-deployment/project.yaml) | deployable | cloud_lab | ci_cd_ready | aws | medium | hardened | `test -f buildspec.yml -a -f appspec.yml` |
| 37 | [Provision EKS Cluster with Terraform](project-37-eks-terraform-provision/project.yaml) | deployable | cloud_lab | iac_ready | aws | high | hardened | `terraform fmt -check` |
| 38 | [Docker and Terraform Three-Tier Architecture](project-38-docker-terraform-3tier/project.yaml) | deployable | cloud_lab | iac_ready | aws | high | hardened | `docker compose config` |
| 39 | [GitHub Actions with AWS and Terraform](project-39-gha-aws-terraform/project.yaml) | deployable | cloud_lab | ci_cd_ready | aws | medium | baseline | `terraform fmt -check` |
| 40 | [Kubernetes Dashboard with Trivy](project-40-k8s-dashboard-trivy/project.yaml) | deployable | local_demo | local_only | none | low | devsecops | `node --check app.js && python3 -m py_compile systeminfo.py` |
| 41 | [Online Boutique Microservices Assignment](project-41-online-boutique-microservices/project.yaml) | deployable | local_lab | kubernetes_ready | none | low | baseline | `kubectl apply --dry-run=client -f deploy` |
| 42 | [Serverless REST API with DynamoDB](project-42-serverless-api-dynamodb/project.yaml) | deployable | cloud_lab | iac_ready | aws | medium | hardened | `terraform -chdir=terraform fmt -check` |
| 43 | [Scalable Web App on ECS Fargate with Terraform](project-43-ecs-fargate-terraform/project.yaml) | deployable | cloud_lab | iac_ready | aws | medium | baseline | `terraform fmt -check` |
| 44 | [DevSecOps 101 Spring Boot Pipeline](project-44-devsecops-101/project.yaml) | deployable | devsecops_lab | ci_cd_ready | aws | medium | devsecops | `./mvnw test` |
| 45 | [Jenkins CI/CD with Argo CD and Vault](project-45-jenkins-cicd-argocd-vault/project.yaml) | deployable | devsecops_lab | ci_cd_ready | aws | medium | devsecops | `test -f Jenkinsfile` |
| 46 | [Advanced EKS Cluster with Terraform Modules](project-46-eks-cluster-terraform-advanced/project.yaml) | deployable | cloud_lab | iac_ready | aws | high | hardened | `terraform fmt -check` |
| 47 | [Django Multitenant SaaS Ecommerce](project-47-django-saas-ecommerce/project.yaml) | deployable | local_validated | container_ready | aws | high | hardened | `make test` |
| 48 | [Terraform AWS EKS Provisioning](project-48-terraform-aws-eks/project.yaml) | deployable | cloud_lab | iac_ready | aws | high | hardened | `terraform fmt -check` |
| 49 | [Text Encryption Cybersecurity Demo](project-49-text-encryption-cybersecurity/project.yaml) | learning | local_demo | local_only | none | low | baseline | `node --check main.js` |

## Validation

Run the parser below from the repository root to verify that every top-level `project-*` directory has valid metadata and that project numbers match directory names:

```bash
python3 - <<'PY'
from pathlib import Path
import re, yaml
projects = sorted(Path('.').glob('project-*'))
seen = set()
for d in projects:
    m = re.match(r'project-(\d{2})-(.+)$', d.name)
    if not m:
        raise SystemExit(f'bad directory name: {d}')
    metadata = d / 'project.yaml'
    if not metadata.exists():
        raise SystemExit(f'missing metadata: {metadata}')
    data = yaml.safe_load(metadata.read_text())
    required = ['schema_version', 'project', 'classification', 'status', 'deployability', 'stack', 'cloud', 'iac', 'ci_cd', 'cost_risk', 'security_posture', 'validation', 'notes']
    missing = [key for key in required if key not in data]
    if missing:
        raise SystemExit(f'{metadata}: missing {missing}')
    number = int(m.group(1))
    if data['schema_version'] != 1 or data['project']['number'] != number or data['project']['slug'] != m.group(2):
        raise SystemExit(f'{metadata}: project identity mismatch')
    if data['classification'] not in {'learning', 'deployable'}:
        raise SystemExit(f'{metadata}: invalid classification')
    if data['cost_risk'] not in {'low', 'medium', 'high'}:
        raise SystemExit(f'{metadata}: invalid cost_risk')
    if data['security_posture'] not in {'baseline', 'devsecops', 'hardened', 'needs_review'}:
        raise SystemExit(f'{metadata}: invalid security_posture')
    if not data['stack'] or not data['validation'].get('command'):
        raise SystemExit(f'{metadata}: stack and validation.command are required')
    seen.add(number)
expected = set(range(1, len(projects) + 1))
if seen != expected:
    raise SystemExit(f'project number gap: expected {sorted(expected)}, got {sorted(seen)}')
print(f'validated {len(projects)} project metadata files')
PY
```
