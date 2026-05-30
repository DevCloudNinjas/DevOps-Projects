# Contributing

Thanks for improving DevOps & Cloud Portfolio Lab. This repository is for practical DevOps learning, so contributions should make projects safer, clearer, easier to validate, or easier for students to reproduce with their own accounts.

## Good Contributions

- Fix unclear instructions, broken commands, outdated screenshots, or missing cleanup steps.
- Improve a project README using `docs/project-readme-template.md`.
- Add or correct `project.yaml` metadata so students can judge cost, deployability, prerequisites, and validation.
- Harden examples without requiring paid services or private credentials.
- Improve local validation, security checks, or troubleshooting notes.

## Before You Start

1. Read the root `README.md`, `PROJECTS.md`, and the project README you plan to change.
2. Check `docs/runbooks/student-implementation-guide.md` for the expected student workflow.
3. Review `SECURITY.md` and the relevant baseline in `docs/security-baselines/` before changing infrastructure, containers, CI/CD, Kubernetes, or secret handling.
4. Keep changes focused. One pull request should cover one project or one clear repository-wide improvement.

## Project Requirements

New or substantially improved projects should include:

- A clear README with goal, architecture, cost warning, prerequisites, credentials/config, quick start, validation, deploy, observe, cleanup, troubleshooting, and stretch goals.
- A valid `project.yaml` that follows `project.schema.json`.
- Example config files such as `.env.example`, `terraform.tfvars.example`, or `*.template.yaml` instead of real secrets.
- A local or dry-run validation command that does not require exposing private credentials.
- Cleanup instructions for cloud, Kubernetes, Docker, Terraform, OpenTofu, or local resources.

## Credential Safety

Never commit real credentials, tokens, kubeconfigs, private keys, `.env` files, `*.tfvars`, generated Terraform state, or cloud account identifiers that should stay private.

Use placeholders and example files:

```bash
cp .env.example .env
cp terraform.tfvars.example terraform.tfvars
```

If you accidentally commit a secret, rotate it first, then open a security report through `SECURITY.md`. Do not paste live secrets into issues, pull requests, logs, screenshots, or build artifacts.

## Quality Gates

Run the repository checks before opening a pull request:

```bash
python3 -m pip install -r tools/requirements.txt
make quality
```

For a specific project, run:

```bash
make validate-project PROJECT=project-name
```

If a project has its own `Makefile`, README validation command, Terraform fmt check, Docker Compose config check, or Kubernetes dry run, run that too and include the result in the pull request.

## Pull Request Flow

1. Create a branch from `master`.
2. Make focused edits with no unrelated formatting churn.
3. Run the quality gates.
4. Open a pull request using the template.
5. Explain what changed, what you validated, and what still needs live cloud verification.
6. Respond to review comments with either a follow-up commit or a clear reason for not changing the implementation.

## Style

- Write for students who are learning by doing.
- Prefer short, direct steps and copyable commands.
- Call out cost risk before deploy commands.
- Show how to observe success and how to roll back or clean up.
- Keep private values out of examples.
