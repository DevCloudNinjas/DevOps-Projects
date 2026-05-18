# Security Policy

## Supported Versions

Currently, the `main` branch of `devops-projects` is the only supported version.

| Version | Supported          |
| ------- | ------------------ |
| `main`    | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within this repository, please do not disclose it publicly.

Instead, please send an email to the repository owner or open a private security advisory via GitHub. We will address the issue as promptly as possible.

## Security Tools Used in this Repository

This repository serves as a learning resource and implements modern DevSecOps practices. We heavily feature the following **free** security tools that students can use in their own projects:

- **[TruffleHog](https://github.com/trufflesecurity/trufflehog):** Scans for exposed secrets, passwords, and API keys.
- **[Trivy](https://aquasecurity.github.io/trivy/):** A comprehensive and versatile security scanner for containers, Infrastructure as Code (IaC), and software dependencies.
- **[SonarQube Community](https://www.sonarqube.org/):** Used for static application security testing (SAST) and code quality analysis.
- **[Checkov](https://www.checkov.io/):** Static code analysis tool for infrastructure-as-code.
- **[Super-Linter](https://github.com/github/super-linter):** GitHub's versatile linting framework.

## Local Security and Hygiene Gate

Use the repo-local gate for fast checks that do not require cloud accounts:

```bash
python3 -m pip install -r tools/requirements.txt
python3 -m tools.quality_gate .
```

The gate flags tracked ignored files, common credential patterns, YAML/shell/Python
syntax issues, and practical Node lockfile problems. Secret scanner fixtures and
templated training files are excluded deliberately so real findings stay visible.

## Reusable Security Baselines

Before changing infrastructure, containers, pipelines, or secret-handling examples,
use the reusable checklists in [docs/security-baselines/](docs/security-baselines/):

- [Kubernetes baseline](docs/security-baselines/kubernetes.md)
- [Terraform baseline](docs/security-baselines/terraform.md)
- [Dockerfile baseline](docs/security-baselines/dockerfile.md)
- [CI/CD baseline](docs/security-baselines/cicd.md)
- [Secrets baseline](docs/security-baselines/secrets.md)
