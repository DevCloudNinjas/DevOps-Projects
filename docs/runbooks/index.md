# Runbooks

Runbooks are repeatable procedures for validating or operating repository examples without requiring production credentials.

Available runbooks:

- [Student Implementation Guide](student-implementation-guide.md): safe step-by-step workflow for students using their own credentials.
- [Credentials and Cost Safety](credentials-and-cost-safety.md): account ownership, local secrets, budget alerts, evidence, and cleanup checks for cloud or credentialed labs.
- [IaC and Kubernetes Example Runbook](../iac-kubernetes-solid-runbook.md): Terraform formatting, Terraform validation, and Kubernetes dry-run checks for EKS/Terraform examples.

Runbook conventions:

- Keep commands local and cloud-independent unless the runbook clearly marks the required account, region, permissions, and expected cost.
- Prefer validation, dry-run, and formatting commands before deployment commands.
- Include rollback or cleanup notes for any command that creates cloud resources.
- Link to the relevant [security baseline](../security-baselines/index.md) when the runbook touches infrastructure, containers, CI/CD, or secrets.
