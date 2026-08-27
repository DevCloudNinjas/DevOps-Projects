# Start Here: project-58-finops-evidence-and-unit-economics-lab

**Learning focus:** FinOps evidence controls and unit-economics reconciliation using synthetic local fixtures

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the clean checkout, inspect README.md and the files under fixtures/ to identify the six documented
controls before running the offline validator.

## Checkpoints

1. 1. Confirm the learner can map the fixtures to ledger reconciliation, allocation gaps, forecast variance, unit metric, owner/due date, and closure evidence
2. 1. Run sh validate-p2-local.sh and observe a machine-readable PASS result with computed metrics and negative-case coverage
3. 1. Verify that evidence/validator-result.json records the command, interpreter, fixture set, computed values, and PASS outcome without treating it as operational approval.

## Hints if you are stuck

1. 1. If the validator does not start, check that Python 3.8+ is available and that the command is run from the project checkout
2. 1. If a control check fails, compare the relevant JSON or CSV field names and values with the documented fixture-to-control mapping
3. 1. If the result is unexpected, inspect for missing, malformed, contradictory, unsafe, or incomplete fixture records and preserve the local transcript for comparison.

## Evidence to capture

Local validator transcript plus evidence/validator-result.json showing computed metrics, PASS outcome, and
negative-case coverage

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
