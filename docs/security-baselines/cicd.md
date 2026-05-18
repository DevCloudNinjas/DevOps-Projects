# CI/CD Security Baseline

Use this checklist for GitHub Actions, GitLab CI, Jenkins, Azure DevOps, CodeBuild, and deployment automation.

## Permissions and Trust Boundaries

- [ ] Pipeline tokens use least privilege.
- [ ] GitHub Actions workflows set explicit `permissions`.
- [ ] Pull request workflows from forks do not receive deployment credentials.
- [ ] Deployment jobs require protected branches, environments, or manual approval for shared infrastructure.
- [ ] Long-lived cloud keys are replaced with OIDC or short-lived credentials where supported.

## Secrets Handling

- [ ] Secrets are stored in the platform secret store, not repository files.
- [ ] Logs mask secrets and avoid printing full environment dumps.
- [ ] Build artifacts do not include `.env`, kubeconfigs, Terraform state, or private keys.
- [ ] Secret rotation is documented for credentials used by the pipeline.

## Dependencies and Tools

- [ ] Actions, plugins, and reusable workflows are pinned to versions or commit SHAs based on risk.
- [ ] Tool versions are explicit for Terraform, kubectl, Helm, language runtimes, and scanners.
- [ ] Dependency install steps use lockfiles where available.
- [ ] Cache keys cannot be poisoned across trust boundaries.

## Build, Test, and Scan Gates

- [ ] Unit, syntax, and formatting checks run before build or deploy jobs.
- [ ] Secret scanning runs before artifacts are published.
- [ ] Container, IaC, and dependency scans run for matching project types.
- [ ] Scan failures have a documented handling path; exceptions include owner, reason, and expiry.

## Deployment Guardrails

- [ ] Production or shared lab deployments are separated from validation jobs.
- [ ] Terraform plans are reviewed before apply for shared resources.
- [ ] Rollback or cleanup commands are documented.
- [ ] Deployment jobs identify target account, cluster, namespace, region, and application.

## Validation

Run local checks that do not require credentials:

```bash
python3 -m tools.quality_gate .
```
