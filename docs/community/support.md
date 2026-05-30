# Support

Use public repository channels for help unless the issue is security-sensitive. Do not share private credentials, tokens, keys, kubeconfig files, billing details, or personal account screenshots.

## Where To Ask

| Need | Best Place |
|---|---|
| A project command fails | GitHub Issue |
| You want to discuss an approach | GitHub Discussion, if enabled |
| You found a docs typo or broken command | Pull Request or GitHub Issue |
| You have a project improvement | Pull Request |
| You found a vulnerability or leaked secret | Follow the root `SECURITY.md` policy |
| You need conduct help | Follow the root `CODE_OF_CONDUCT.md` |

If Discussions are not enabled, use an issue with a clear title and enough context to reproduce the problem.

## Good Support Request Format

Use this structure:

```text
Project:
Goal:
Command I ran:
Expected result:
Actual result:
Error output:
What I already tried:
Environment:
Cleanup status:
```

For environment, include only non-sensitive details:

- Operating system.
- Tool versions, such as Docker, Python, Node.js, Terraform, OpenTofu, `kubectl`, AWS CLI, or Azure CLI.
- Local cluster tool, such as Kind or Minikube.
- Cloud provider and region, if relevant.

## What To Include

Helpful:

- The exact project path, such as `project-54-progressive-delivery-home-lab`.
- The command copied from the README.
- The shortest useful error output.
- Sanitized screenshots.
- Whether you ran `make validate-project PROJECT=<project-path>`.
- Whether resources were cleaned up.

Not helpful:

- "It does not work" without commands or output.
- Screenshots that hide the actual error.
- Full logs containing tokens or account identifiers.
- Private credentials sent to maintainers.

## Credential Safety

Before posting, remove:

- API keys, access keys, private keys, tokens, cookies, and passwords.
- `.env`, `terraform.tfvars`, kubeconfig, and generated secret contents.
- Personal billing information.
- Account IDs if you do not want them public.
- Internal company URLs or private repository names.

If a credential was exposed publicly, rotate it first, then ask for help if needed.

## Response Expectations

This repository is a learning resource, not a managed support service. Maintainers and contributors can help fastest when a request is reproducible, scoped to one project, and clear about what was already tried.

For setup and cleanup habits, start with the [Student Implementation Guide](../runbooks/student-implementation-guide.md) and [Credentials and Cost Safety](../runbooks/credentials-and-cost-safety.md).
