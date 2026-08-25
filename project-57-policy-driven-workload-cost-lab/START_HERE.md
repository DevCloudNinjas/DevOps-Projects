# Start Here: project-57-policy-driven-workload-cost-lab

**Learning focus:** Policy-driven workload cost governance and fail-closed validation

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

From the clean checkout, inspect README.md and the checked-in fixtures, then run `sh validate-p2-local.sh` locally without using any provider CLI, credentials, network, deployment, or teardown.

## Checkpoints

1. 1. Confirm the validator discovers the deterministic `fixtures/plan-*.json` set and prints a machine-readable result
2. 2. Verify the result reports `PASS` with computed plan, allow, and deny counts plus negative-case coverage
3. 3. Preserve the local transcript and `evidence/validator-result.json`, and explain how fixture decisions correspond to allow/deny, expiry, public/persistent resources, ownership, budgets, and policy diff.

## Hints if you are stuck

1. 1. If discovery fails, check that you are in the project root and that the expected `fixtures/` files are present
2. 2. If a result is not passing, compare the fixture records against the documented required fields and fail-closed conditions rather than changing the validator
3. 3. For an unexpected allow or deny, trace one fixture at a time through its control-relevant fields, including lifetime and unsafe-resource flags, and consult `fixtures/policy-diff.md` for the review boundary.

## Evidence to capture

Local command transcript plus `evidence/validator-result.json` showing interpreter, fixture set, computed counts, PASS outcome, and negative-case coverage

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
