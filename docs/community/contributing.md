# Contributing

Contributions are welcome when they make the projects easier to run, safer to learn from, or clearer to review. Keep changes small, reproducible, and honest about prerequisites, cost, and cleanup.

Please follow the root `CODE_OF_CONDUCT.md`.

## Good First Contributions

- Fix a broken command in a project `README.md`.
- Add missing cleanup notes to a project.
- Improve a `project.yaml` with accurate tools, cost risk, prerequisites, or validation metadata.
- Add sanitized screenshots or expected command output.
- Update docs when a project workflow has drifted from the actual files.
- Improve troubleshooting notes for a real failure you reproduced.

## Documentation Changes

Use the existing docs structure:

- Project-specific instructions belong in that project's `README.md`.
- Reusable learner workflow belongs in [runbooks](../runbooks/index.md).
- Reusable security guidance belongs in [security baselines](../security-baselines/index.md).
- New project README structure should follow the [Project README Template](../project-readme-template.md).

Write for someone using their own credentials on their own machine. Avoid private account names, personal tokens, private URLs, and screenshots that reveal sensitive details.

## Project Fixes

For fixes to an existing project:

1. Read the project `README.md`.
2. Read the project `project.yaml`.
3. Run the listed validation command when possible.
4. Make the smallest change that fixes the workflow.
5. Update docs if commands, paths, prerequisites, ports, or cleanup steps changed.

If a cloud deployment cannot be validated locally, say exactly what was validated and what still needs a real account.

## New Projects

New projects should be complete enough for a learner to run and clean up without guessing.

Include:

- A project directory named consistently with the existing `project-XX-name` pattern.
- A `README.md` based on the [Project README Template](../project-readme-template.md).
- A `project.yaml` with accurate metadata.
- Example config files instead of real secrets.
- A validation command that is local, fast, and safe when possible.
- Cleanup instructions for every resource the project creates.

Prefer local-first labs when the learning goal does not require a cloud account.

## Metadata

Project metadata helps the catalog and learning paths stay useful. Keep `project.yaml` accurate when you change a project.

Check these fields especially:

- Difficulty and project type.
- Tools and cloud provider.
- `cost_risk`.
- Deployability.
- Validation command.
- Learning prerequisites, paths, and badges.

Use realistic labels. A project that creates EKS, databases, NAT gateways, or public load balancers should not be described as local-only or zero-cost.

## Quality Commands

From the repository root:

```bash
python3 -m pip install -r tools/requirements.txt
make list-projects
make validate-project PROJECT=project-50-argocd-gitops-home-lab
make quality
```

Replace `project-50-argocd-gitops-home-lab` with the project you changed.

The local quality gate checks project metadata, repository hygiene, syntax issues, and common secret patterns. It does not create cloud resources.

## Pull Request Checklist

Before opening a pull request:

- The change has a clear reason and a focused scope.
- Commands in docs match the repository files.
- New credentials are represented by examples or templates only.
- Cost and cleanup notes are present for cloud resources.
- `project.yaml` metadata matches the project behavior.
- Local quality commands were run, or the PR explains why they could not be run.
- Screenshots and logs are sanitized.
- Security issues are reported through the root `SECURITY.md` policy, not public PR comments.

## Review Expectations

Reviewers should be able to see what changed, how it was validated, and what risk remains. If your change touches deployment, credentials, CI/CD, Terraform, Kubernetes, containers, or security scanning, include the relevant validation output and cleanup notes in the pull request description.
