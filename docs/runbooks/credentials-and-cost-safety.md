# Credentials and Cost Safety

Use this runbook before running any project that asks for cloud access, API keys, kubeconfig files, Terraform variables, or local `.env` values.

The repository does not provide shared credentials, hosted accounts, forms, or private access. Each learner runs projects with their own local tools and their own cloud or service accounts.

## Safety Rules

- Use your own account, IAM user, service principal, or API token.
- Never use credentials from a tutorial, screenshot, classmate, issue, pull request, or copied terminal output.
- Never commit `.env`, `*.tfvars`, kubeconfig files, private keys, token files, or generated secret manifests.
- Start from example files such as `.env.example`, `terraform.tfvars.example`, or `*.template.yaml` only when the project includes them.
- Prefer local-only projects when you are still learning a tool or cannot monitor cloud cost.
- Rotate any credential that was pasted into Git, chat, screenshots, or a public issue.

For the full project workflow, use the [Student Implementation Guide](student-implementation-guide.md).

## Before You Deploy

Confirm the project scope from two places:

1. Read the project `README.md`.
2. Read the project `project.yaml` for `cost_risk`, deployability, tools, prerequisites, and validation command.

Then answer these questions:

| Question | Why It Matters |
|---|---|
| Which account am I using? | Prevents deploying into the wrong personal, school, or work account. |
| Which region will resources use? | Cost, quota, and cleanup views are region-specific. |
| What will be created? | EKS, NAT gateways, databases, load balancers, and storage can create real cost. |
| What is the cleanup command? | Do not deploy until you know how to destroy. |
| What proof will I capture? | Screenshots and command output make the work portfolio-ready. |

## Budget Alerts

Set a budget alert before running cloud labs. Use the cloud provider console if you are not comfortable with CLI billing commands.

Recommended minimum:

- One monthly budget for the account.
- One alert before the budget is exhausted.
- One habit: check the billing dashboard after cleanup.

For AWS labs, also confirm identity and region:

```bash
aws sts get-caller-identity
aws configure get region
```

For Azure labs, confirm the active subscription:

```bash
az account show
```

If the account, subscription, or region is not what you expected, stop before running deploy commands.

## Local Environment Files

Create local config files only from examples that exist in the selected project:

```bash
cp .env.example .env
cp terraform.tfvars.example terraform.tfvars
cp db-secret.template.yaml db-secret.yaml
```

Do not run all three commands blindly. Use only the files named by the project README.

Before committing, check what Git sees:

```bash
git status --short
git diff --cached
```

If a real secret appears in staged files, unstage it and rotate the credential.

## Validation Before Cloud Changes

From the repository root, run the local quality checks:

```bash
python3 -m pip install -r tools/requirements.txt
make quality
```

For one project, run:

```bash
make validate-project PROJECT=project-50-argocd-gitops-home-lab
```

Replace the project path with the project you are using. These checks are local and cloud-independent; they do not prove the deployment will succeed, but they catch many mistakes before cost or security risk is introduced.

## Cloud Cleanup

Every cloud lab needs a cleanup step. Common commands include:

```bash
terraform destroy
tofu destroy
kubectl delete -f <manifest-folder>
docker compose down -v
kind delete cluster --name <cluster-name>
```

Run only the cleanup command that matches the project. After cleanup, verify in the cloud console that billable resources are gone, especially clusters, databases, load balancers, NAT gateways, IP addresses, storage buckets, and container registries.

## Screenshots and Evidence

Capture proof without exposing secrets.

Good evidence:

- App page, service URL, or local dashboard.
- Pipeline run summary.
- `kubectl get pods` output.
- Terraform or OpenTofu outputs with sensitive values hidden.
- Cleanup confirmation from CLI or cloud console.
- Short notes about what failed and how you fixed it.

Bad evidence:

- Access keys, private keys, tokens, cookies, or kubeconfig contents.
- Full `.env` or `terraform.tfvars` files.
- Billing pages showing personal information.
- Screenshots from another learner's account.

Use the learning report template in the [Student Implementation Guide](student-implementation-guide.md) to turn evidence into a portfolio note.

## If Something Goes Wrong

| Problem | Safe Response |
|---|---|
| Wrong account or region | Stop, clean up anything created, then reconfigure the CLI. |
| Unexpected billable resource | Destroy it, confirm in the console, then document the cleanup. |
| Secret committed locally | Remove it from the commit and rotate it before pushing. |
| Secret pushed publicly | Rotate it immediately and follow the root `SECURITY.md` policy. |
| Cleanup command fails | Read the error, check the active account and region, and delete remaining resources in the console if needed. |

When asking for help, share commands, errors, and sanitized screenshots. Do not share private credentials.
