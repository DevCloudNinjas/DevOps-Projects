# IaC and Kubernetes Example Runbook

Use this runbook for the EKS/Terraform examples in:

- `project-37-eks-terraform-provision`
- `project-38-docker-terraform-3tier/terraform-configs`
- `project-46-eks-cluster-terraform-advanced`
- `project-48-terraform-aws-eks`

## Before Planning

1. Replace documentation CIDRs such as `203.0.113.0/24` with your own `/32` or trusted admin range.
2. Keep backend placeholders local until the S3 bucket and DynamoDB lock table exist.
3. Do not commit rendered secret files such as `db-secret.yaml`; keep only `*.template.yaml` in source.

## Local Validation

Run formatting and syntax checks before opening a PR:

```bash
terraform fmt -check -recursive project-37-eks-terraform-provision
terraform fmt -check -recursive project-38-docker-terraform-3tier/terraform-configs
terraform fmt -check -recursive project-46-eks-cluster-terraform-advanced
terraform fmt -check -recursive project-48-terraform-aws-eks

terraform -chdir=project-37-eks-terraform-provision validate
terraform -chdir=project-38-docker-terraform-3tier/terraform-configs validate
terraform -chdir=project-46-eks-cluster-terraform-advanced validate
terraform -chdir=project-48-terraform-aws-eks validate

kubectl apply --dry-run=client -f project-48-terraform-aws-eks/db-secret.template.yaml
kubectl apply --dry-run=client -f project-48-terraform-aws-eks/deployment.yaml
kubectl apply --dry-run=client -f project-48-terraform-aws-eks/service.yaml
```

If provider plugins are not already initialized, run `terraform init -backend=false` in the target folder first. Avoid `terraform plan` or `terraform apply` in CI unless cloud credentials and cost controls are explicitly configured.
