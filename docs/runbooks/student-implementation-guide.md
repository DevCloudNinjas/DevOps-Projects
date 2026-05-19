# Student Implementation Guide

Use this guide before starting any project in this repository. It gives every learner the same safe path: understand the scope, prepare credentials, validate locally, deploy only when ready, and clean up resources.

## 1. Choose the Right Project

Start with the project metadata and README:

- `project.yaml` tells you whether a project is `learning` or `deployable`.
- `cost_risk` tells you whether it may create billable cloud resources.
- `validation.command` gives you the first command to check the project.
- The README explains the project-specific workflow.

Good beginner-friendly paths:

- Local only: projects 50, 51, 53, and 54.
- AWS free-tier style: project 52.
- Portfolio examples: projects 28, 31, 41, 47, and 48.

## 2. Prerequisites Checklist

Install only what the selected project needs:

- Git
- Docker and Docker Compose
- Python 3
- Node.js, when the project has a Node app
- `kubectl`, Kind, or Minikube for local Kubernetes labs
- AWS CLI or Azure CLI for cloud labs
- Terraform or OpenTofu for infrastructure-as-code labs

Check the project README before installing extra tools.

## 3. Credentials and Secrets

Every learner must use their own credentials. Do not use credentials from tutorials, screenshots, commits, videos, or classmates.

Rules:

- Never commit `.env`, `*.tfvars`, kubeconfig files, private keys, or cloud credentials.
- Start from `.env.example`, `terraform.tfvars.example`, or `*.template.yaml` files.
- Store real values locally in ignored files.
- Prefer short-lived cloud credentials where possible.
- Rotate any credential accidentally pasted into Git.

Common files to create locally:

```bash
cp .env.example .env
cp terraform.tfvars.example terraform.tfvars
cp db-secret.template.yaml db-secret.yaml
```

Only do this when the project includes those example files.

## 4. Cost Safety

Before running any cloud command, answer these questions:

- Which cloud account am I using?
- Which region will resources be created in?
- What resources will be created?
- Is there a cleanup command?
- Can I afford the worst-case cost if I forget to destroy it for a day?

For AWS or Azure projects:

```bash
aws sts get-caller-identity
aws configure get region
```

or:

```bash
az account show
```

If you are unsure, use a local-only project first.

## 5. Standard Implementation Flow

Use this order for most projects:

1. Read the project README completely.
2. Read `project.yaml`.
3. Install prerequisites.
4. Create local config files from examples.
5. Run validation or dry-run commands.
6. Deploy locally or to your own cloud account.
7. Observe the app, logs, pipeline, or infrastructure.
8. Write down what broke and how you fixed it.
9. Run cleanup commands.
10. Confirm resources are gone.

## 6. Validation Commands

From the repo root:

```bash
make list-projects
make validate-project PROJECT=project-50-argocd-gitops-home-lab
make quality
```

From an individual project, use the local README or `Makefile` when present:

```bash
make validate
```

Validation commands are not always full deployments. They are quick checks to catch mistakes before expensive or risky steps.

## 7. Cleanup

Always clean up cloud and local resources.

Common cleanup commands:

```bash
docker compose down -v
kind delete cluster --name <cluster-name>
terraform destroy
tofu destroy
kubectl delete -f <manifest-folder>
```

After cloud labs, confirm in the cloud console that resources are gone.

## 8. Troubleshooting

Common issue patterns:

| Symptom | What To Check |
|---|---|
| `AccessDenied` | Cloud identity, IAM permissions, account/region |
| `NoCredentialProviders` | AWS CLI configuration or environment variables |
| `ImagePullBackOff` | Image name, tag, registry login, architecture |
| `CrashLoopBackOff` | App logs, env vars, health checks |
| Terraform state error | Backend config, lock table, workspace, stale local state |
| Port already in use | Existing local service using the same port |
| ArgoCD out of sync | Git path, branch, repo URL, namespace |

Useful commands:

```bash
kubectl get pods -A
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace>
docker compose logs
terraform plan
tofu plan
```

## 9. Learning Report Template

After finishing a project, write a short report:

```text
Project:
Goal:
Tools used:
What I deployed:
What failed:
How I fixed it:
Security or cost lesson:
Cleanup proof:
What I would improve next:
```

This turns a tutorial into portfolio evidence.

