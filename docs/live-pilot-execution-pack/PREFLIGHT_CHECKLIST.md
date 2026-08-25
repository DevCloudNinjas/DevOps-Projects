# Pre-flight Checklist — Fail-Closed Gate

**Document version:** 1.0.0  **Owner:** __________  **Pilot ID:** `project-53-supply-chain-security-lab`  **Commit:** __________  **Created/updated:** __________ / __________  **Reviewer:** __________  **Approval state:** NOT AUTHORIZATION UNTIL SIGNED

Mark `[x]` only with evidence ID and reviewer initials. **One unchecked critical item blocks START.** All GitHub, provider, identity, budget, and monitoring gates are **external** human verifications; this source-only checklist neither configures nor proves them.

| Gate | Critical check | Evidence ID | [x]/Initials |
|---|---|---|---|
| Governance | Signed authorization, independent approver, named owners, approved window/timezone | | |
| Source integrity | Project 53 exact SHA/ref frozen; Project 52 explicitly not selected | | |
| GitHub | Narrow token permissions, immutable action references, branch/environment protections, audit access | | |
| Identity | Short-lived least-privilege identity, reviewed trust, operator/approver separation, no static key | | |
| Network/data | Provider/region/target, exposure, encryption/logging, allowed data, retention decision | | |
| Cost | Maximum budget, alert thresholds/routes, tags/labels, spending authority and monitoring | | |
| Safety | Disposable target, quotas, incident contact, no unapproved scope or command | | |
| Observability | Health/log/permission/alert access tested and baseline recorded | | |
| Rollback | Last-known-good state and human sequence source-shaped rehearsed; trigger and owner named | | |
| Teardown | Teardown owner, deadline, inventory procedure, residual-scan owner, billing review timing | | |

**Two-person review:** Reviewer 1 __________ date/time __________; Reviewer 2 __________ date/time __________
**Gate decision:** [ ] PASS  [ ] BLOCKED  [ ] EXCEPTION (must be approved and linked)
**START authorization signature:** __________ timestamp __________

## Mandatory stop rule

If any critical check is unchecked, disputed, stale, or not independently reviewable, do not start, do not widen scope, and escalate to the approver. This checklist proves document review only; it does not prove live controls.
