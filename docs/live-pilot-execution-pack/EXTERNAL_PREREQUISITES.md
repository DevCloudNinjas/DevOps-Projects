# External Prerequisites — Project 53

**Status:** Source-only checklist; not authorization.

A live pilot may not start until accountable humans verify every item below outside
this repository. GitHub and cloud controls remain external human verifications.
Record evidence IDs and reviewers in
[AUTHORIZATION_RECORD.md](AUTHORIZATION_RECORD.md).

## Required external controls

| Control | Required human evidence |
|---|---|
| Source protection | Protected branch, required checks, and review rule verified. |
| Environment protection | Approved environment, named approvers, and audit visibility verified. |
| Identity | Short-lived least-privilege identity and trust policy independently reviewed. |
| Target | Disposable account, project, subscription, region, and resource scope approved. |
| Cost | Budget ceiling, alerts, notifications, and cost owner approved. |
| Window | Start/end window, operator, reviewer, and escalation route approved. |
| Observability | Logs, health signals, alerts, and evidence retention route verified. |
| Teardown | Teardown owner, deadline, residual inventory, and cost review assigned. |

If any control is missing, stale, disputed, or not independently reviewable,
mark the authorization record **BLOCKED**. This document does not configure,
grant, or verify any external control.
