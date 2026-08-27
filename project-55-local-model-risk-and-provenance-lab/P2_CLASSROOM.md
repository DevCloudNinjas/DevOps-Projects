# Project 55 Classroom Record

This record defines a local-only, offline rehearsal for MLOps model risk and provenance. Learning
objectives are to inspect the checked-in synthetic fixtures, apply the documented controls, and
reproduce computed positive and negative decisions. Prerequisite: Python 3.8+ and a clean checkout;
no provider CLI, SDK, credential, network, container, deployment, teardown, or live-service behavior
is permitted.

Run `sh validate-p2-local.sh`. The fixture-to-control mapping is `provenance/model-card/risk
evidence; tampered hash and incomplete approval`. Expected output is a machine-readable JSON result
containing interpreter, command, fixture set, computed metrics, PASS outcome, and negative-case
coverage. Evidence retention is limited to the generated local transcript and result; it is not an
authorization or production record.

## Learning and assessment

Students evaluate a synthetic model artifact, approval record, and provenance evidence without a remote model service. The observable outcome is a local validator result that reports the model hash, evaluation result, and rejection of a tampered or incomplete fixture. The instructor criterion is that the learner explains which artifact and approval controls support a trustworthy release decision. The project-local validator and checked-in fixtures demonstrate this competency without cloud credentials or deployment.
