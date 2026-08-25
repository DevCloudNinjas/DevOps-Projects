# Project 53 L2 Live Pilot Execution Pack

**Document version:** 1.0.0
**Owner:** ____________________
**Pilot ID:** `project-53-supply-chain-security-lab`
**Project 53 commit SHA:** ____________________
**Created (ISO 8601 with timezone):** 2026-08-24T____:____±__:__
**Updated (ISO 8601 with timezone):** ____________________
**Reviewer:** ____________________
**Approval state:** DRAFT — NOT AUTHORIZATION UNTIL SIGNED

> **Boundary:** This is a source-only governance pack. It does not establish authorization, GitHub configuration, cloud access, deployment, rollback, teardown, or residual-cost clearance. No live operation may begin from this repository alone.

## Scope

Project 53 is the sole selected pilot. Project 52 (`project-52-opentofu-aws-free-tier-lab`) is retained only as reusable source-only pattern material and must not be selected, deployed, or treated as evidence for this pilot. Any drift in project, repository, ref, commit, provider, region, account, identity, or resource scope is a stop condition.

## Use sequence

Complete [EXTERNAL_PREREQUISITES.md](EXTERNAL_PREREQUISITES.md), then [AUTHORIZATION_RECORD.md](AUTHORIZATION_RECORD.md), [ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md), and [PREFLIGHT_CHECKLIST.md](PREFLIGHT_CHECKLIST.md). During a separately approved window, a human operator follows [PILOT_RUNBOOK.md](PILOT_RUNBOOK.md) and records lifecycle evidence using [EVIDENCE_INDEX.md](EVIDENCE_INDEX.md) and [EVIDENCE_RECORD_TEMPLATE.md](EVIDENCE_RECORD_TEMPLATE.md). Use [RISK_ROLLBACK_GUIDANCE.md](RISK_ROLLBACK_GUIDANCE.md) for decisions, [TEARDOWN_AND_RESIDUAL_COST_CHECKLIST.md](TEARDOWN_AND_RESIDUAL_COST_CHECKLIST.md) for closure, [RACI.md](RACI.md) for accountability, and [CLOSURE_RECORD.md](CLOSURE_RECORD.md) for final review.

## Source-only operating rules

Do not add credentials, account identifiers, real endpoints, tokens, secrets, executable provider commands, deployment scripts, teardown scripts, containers, or network-dependent validators to this pack. Record a human-executed provider or GitHub path as evidence metadata only. A screenshot without date, target, reviewer, and provenance is insufficient. Local validation proves only the checked-in source contract; it cannot prove external controls.

## References

[1]: https://docs.github.com/en/actions/reference/security/secure-use "GitHub Docs: Secure use reference"
[2]: https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/setting-permissions-for-jobs-in-a-workflow "GitHub Docs: Setting permissions for jobs in a workflow"
[3]: https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect "GitHub Docs: About security hardening with OpenID Connect"
[4]: https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html "AWS Budgets: Managing your costs"
[5]: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html "AWS IAM: Security best practices"
[6]: https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_permissions_least_privileges.html "AWS Well-Architected: Grant least privilege"
[7]: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions "GitHub Actions workflow syntax"

Provider-specific behavior, pricing, quotas, and policy must be reverified by accountable owners immediately before any future pilot.
