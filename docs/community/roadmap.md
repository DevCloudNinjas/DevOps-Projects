# Roadmap

This roadmap focuses on making the repository easier to learn from, safer to run, and stronger as a DevOps portfolio. It is intentionally concise so contributors can pick useful work without needing a private planning document.

## Current Direction

The site is moving toward a clean documentation system with four jobs:

- Help learners choose the right project.
- Make setup, validation, and cleanup predictable.
- Show trust signals for security and repository quality.
- Turn completed labs into portfolio evidence.

## Near-Term Priorities

### Project Detail Pages

Add focused docs pages for high-signal projects, starting with flagship and 2026 home labs.

Each page should include:

- What the project teaches.
- Prerequisites.
- Cost and credential notes.
- Validation command.
- Cleanup command.
- Evidence to capture.
- Link back to the project `README.md`.

### Screenshots and Expected Output

Add sanitized screenshots and short expected-output snippets where they reduce confusion.

Best targets:

- Working app pages.
- Kubernetes pod status.
- Pipeline success summaries.
- Observability dashboards.
- Cleanup confirmation.

Do not include credentials, personal account details, private URLs, or full billing pages.

### OpenSSF Scorecard and Trust Signals

Improve repository trust signals by tracking practical security hygiene:

- Branch protection and review expectations.
- Dependency and workflow hygiene.
- Secret scanning habits.
- Security policy visibility.
- Clear contribution and support paths.

The goal is not a badge-only score. The goal is safer day-to-day contribution.

### Astro Starlight Search

Keep improving the Astro Starlight experience where it clearly improves navigation, search, internal project discovery, and copyable commands.

Desired improvements:

- Better search across project docs.
- Navigation sections that scale beyond 54 projects.
- Copy buttons for command blocks.
- Privacy-conscious configuration.
- Offline-friendly behavior where practical.

Keep the site fast and readable. Avoid adding features that make the docs feel heavier than the projects.

## 2026 Learning Priorities

### Platform Engineering Labs

Add more labs that teach internal developer platform patterns:

- Golden paths for app delivery.
- Reusable CI/CD templates.
- Developer portals and service catalogs.
- Kubernetes platform guardrails.
- Secrets and environment management.
- Observability defaults.

### More Local-First Labs

Prefer local-first versions of expensive cloud workflows when the learning goal allows it.

Good candidates:

- Local GitOps.
- Local progressive delivery.
- Local observability stacks.
- Local supply-chain scanning.
- Local policy-as-code checks.

Cloud projects should still exist, but they need clear account, region, cost, and cleanup guidance.

### Project Metadata Quality

Keep improving `project.yaml` files so the catalog can stay accurate.

Focus on:

- Cost risk.
- Deployability.
- Validation commands.
- Prerequisites.
- Learning paths.
- Badges.

Metadata should describe the project as it behaves today, not what the project might become later.

## Contribution Guidance

Roadmap work should stay small and reviewable. A strong contribution usually improves one project, one runbook, one metadata pattern, or one docs workflow at a time.

Before contributing, read [Contributing](contributing.md), [Support](support.md), and the [Project README Template](../project-readme-template.md).
