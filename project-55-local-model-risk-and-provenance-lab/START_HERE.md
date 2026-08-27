# Start Here: project-55-local-model-risk-and-provenance-lab

**Learning focus:** MLOps model-risk controls and artifact provenance

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, inspect README.md and the checked-in fixtures, then run only the permitted offline
command `sh validate-p2-local.sh` with Python 3.8+ available.

## Checkpoints

1. 1. The validator reads the complete listed fixture set, including model.bin, without requesting credentials, network access, containers, or services
2. 1. The local output reports the provenance hash and evaluation metric while showing PASS for the positive control
3. 1. The generated evidence/validator-result.json records both tampered-model-hash rejection and incomplete-approval rejection, alongside the command and fixture set.

## Hints if you are stuck

1. 1. If the fixture assertion fails, confirm you are at the project root and that every named file under fixtures/ is present
2. 1. If the provenance check fails, compare the recorded model hash with the bytes of fixtures/model.bin rather than editing the result
3. 1. If a control decision fails, inspect the relevant risk-register.json, approval.json, and evaluation.json fields and check for missing, contradictory, or incomplete values.

## Evidence to capture

Local command transcript plus evidence/validator-result.json showing PASS, computed accuracy and model
SHA-256, fixture set, and both negative-case checks

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
