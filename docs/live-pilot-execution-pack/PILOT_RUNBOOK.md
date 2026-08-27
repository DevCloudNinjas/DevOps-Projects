# Pilot Runbook — Project 53

**Status:** Human-operated template; not a deployment script.

Use this runbook only after every external prerequisite and authorization field is
approved. Record evidence metadata, not credentials, commands, endpoints, or
account identifiers.

## Human sequence

1. Confirm the exact repository ref, Project 53 commit, approved target, and
   approved time window match the signed authorization record.
2. Confirm the operator has the approved short-lived identity and that the
   independent reviewer can observe the evidence route.
3. Capture baseline evidence for identity, cost, target inventory, and
   observability before any external activity.
4. Perform only the separately approved external procedure. Stop immediately if
   scope, cost, identity, target, or evidence differs from authorization.
5. Capture evidence metadata for each approved lifecycle checkpoint.
6. Follow the teardown and residual-cost checklist before the authorization
   expires.
7. Complete the closure record with an independent reviewer.

## Stop conditions

Stop and escalate for a missing approval, changed commit, unexpected resource,
identity error, target mismatch, budget alert, missing evidence, or inability to
complete teardown. This source-only runbook contains no provider command.
