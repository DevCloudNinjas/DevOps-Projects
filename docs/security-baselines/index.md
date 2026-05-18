# Security Baselines

These baselines are reusable review checklists for DevOps lab work. They are intentionally provider-neutral where possible and should be applied before opening a pull request.

Baselines:

- [Kubernetes](kubernetes.md): workload, network, RBAC, and manifest hygiene.
- [Terraform](terraform.md): state, inputs, providers, IAM, and review controls.
- [Dockerfile](dockerfile.md): image provenance, dependency hygiene, least privilege, and runtime safety.
- [CI/CD](cicd.md): pipeline permissions, secrets handling, dependency controls, and deployment guardrails.
- [Secrets](secrets.md): detection, storage, rotation, examples, and incident response.

Suggested review flow:

1. Identify the touched surface area: manifests, Terraform, containers, workflows, scripts, or docs.
2. Apply each matching baseline.
3. Run the repository local quality gate from [SECURITY.md](https://github.com/DevCloudNinjas/DevOps-Projects/blob/main/SECURITY.md).
4. Document any accepted risk in the PR description or the affected project README.

These checklists complement automated tools. Passing a scanner does not replace review of permissions, data exposure, and operational blast radius.
