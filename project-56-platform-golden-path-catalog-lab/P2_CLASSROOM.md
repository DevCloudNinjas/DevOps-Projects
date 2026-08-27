# Project 56 Classroom Record

This record defines a local-only, offline rehearsal for platform golden-path catalog. Learning
objectives are to inspect the checked-in synthetic fixtures, apply the documented controls, and
reproduce computed positive and negative decisions. Prerequisite: Python 3.8+ and a clean checkout;
no provider CLI, SDK, credential, network, container, deployment, teardown, or live-service behavior
is permitted.

Run `sh validate-p2-local.sh`. The fixture-to-control mapping is `ownership, dependencies,
versioning; unsafe or incomplete template`. Expected output is a machine-readable JSON result
containing interpreter, command, fixture set, computed metrics, PASS outcome, and negative-case
coverage. Evidence retention is limited to the generated local transcript and result; it is not an
authorization or production record.

## Learning and assessment

Students assemble and review a local golden-path catalog entry that expresses ownership, delivery
expectations, and operational metadata. The observable outcome is a validator result confirming the required
catalog fields and rejection of an incomplete entry. The instructor criterion is that the learner can connect
catalog metadata to an observable platform-engineering responsibility. The project-local validator and
synthetic catalog fixtures demonstrate the competency without operating a platform service.
