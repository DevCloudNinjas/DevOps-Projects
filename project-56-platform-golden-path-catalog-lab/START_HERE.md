# Start Here: project-56-platform-golden-path-catalog-lab

**Learning focus:** Offline platform golden-path governance and fixture validation

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the clean checkout, inspect README.md and the two JSON files in fixtures/ to identify the documented
controls and the positive versus negative template cases before running anything.

## Checkpoints

1. 1. The learner can map ownership, dependencies, and versioning fields in each checked-in fixture and identify deployment_prohibited as a safety control
2. 1. Running sh validate-p2-local.sh produces machine-readable JSON with the command, interpreter, fixture set, computed template and unsafe-template counts, PASS outcome, and negative-case coverage
3. 1. evidence/validator-result.json is updated locally and matches the printed validator result, with evidence retained only as a transcript and result rather than treated as authorization.

## Hints if you are stuck

1. 1. If the validator stops before printing a result, compare each fixture against the required owner, dependencies, version or lifecycle, deployment_prohibited, and positive ttl_hours conditions
2. 1. If the fixture set appears incomplete, check that the command is run from the project checkout and that fixtures/ contains the checked-in JSON records
3. 1. If the negative-case count is surprising, review how the validator defines an unsafe template and distinguish that computed metric from the separately stated missing-owner coverage.

## Evidence to capture

Local command transcript plus matching evidence/validator-result.json showing deterministic fixture set, PASS
outcome, computed metrics, and negative-case coverage

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
