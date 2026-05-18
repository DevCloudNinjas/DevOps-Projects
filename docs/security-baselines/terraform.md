# Terraform Security Baseline

Use this checklist for Terraform modules, root modules, examples, and CI/CD plans.

## State and Backends

- [ ] Remote state uses encryption at rest.
- [ ] State locking is enabled for shared environments.
- [ ] State buckets or storage accounts block public access.
- [ ] State access is limited to the CI role and maintainers who need it.
- [ ] State files, plan files, and local `.terraform/` directories are not committed.

## Providers and Modules

- [ ] Provider versions are pinned with clear constraints.
- [ ] External modules are pinned to immutable versions or commits.
- [ ] Provider aliases and regions are explicit when multiple accounts or regions are involved.
- [ ] Required providers are declared in each reusable module where appropriate.

## Inputs and Secrets

- [ ] Sensitive variables use `sensitive = true`.
- [ ] Example `.tfvars` files contain placeholders only.
- [ ] Real `.tfvars`, private keys, generated kubeconfigs, and credentials are ignored.
- [ ] Defaults do not create public exposure, broad IAM, or expensive resources unexpectedly.

## IAM and Network Exposure

- [ ] IAM policies avoid wildcard actions and resources unless justified.
- [ ] Security groups and firewall rules avoid `0.0.0.0/0` for admin ports.
- [ ] Public endpoints are intentional and documented.
- [ ] Databases and control planes are private unless the lab explicitly teaches public access.

## Review and Plan Safety

- [ ] `terraform fmt -check -recursive` passes.
- [ ] `terraform validate` passes after `terraform init -backend=false` where possible.
- [ ] Plans are reviewed before apply in shared or cloud-backed environments.
- [ ] Destructive changes are called out before merge.
- [ ] Cost-impacting resources are documented in the project README or runbook.

## Validation

Run local checks from the target Terraform directory:

```bash
terraform init -backend=false
terraform fmt -check -recursive
terraform validate
```
