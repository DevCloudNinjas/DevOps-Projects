# Pull Request

## What Changed

- TBD

## Affected Path

- TBD

## Why This Is Needed

Describe the problem this solves for students, maintainers, or repository safety.

## Validation Performed

Paste the commands you ran and summarize the result:

```bash
make quality
make validate-project PROJECT=project-name
```

Project-specific checks:

```bash
# Add README, Makefile, Terraform, Docker, Kubernetes, or app test commands here.
```

## Safety Review

- [ ] No real credentials, tokens, kubeconfigs, `.env` files, `*.tfvars`, Terraform state, private keys, or sensitive logs are included.
- [ ] Cost risk is documented before any cloud deploy command.
- [ ] Cleanup, rollback, or destroy steps are documented for resources created by this change.
- [ ] Failure behavior is observable through logs, validation output, health checks, or troubleshooting notes.
- [ ] Any live cloud, runner, or account-specific validation that could not be performed is listed below.

## Live Environment Verification Still Needed

- TBD
