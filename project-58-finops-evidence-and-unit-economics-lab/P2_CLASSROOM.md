# Project 58 Classroom Record

This record defines a local-only, offline rehearsal for FinOps evidence and unit economics. Learning
objectives are to inspect the checked-in synthetic fixtures, apply the documented controls, and
reproduce computed positive and negative decisions. Prerequisite: Python 3.8+ and a clean checkout;
no provider CLI, SDK, credential, network, container, deployment, teardown, or live-service behavior
is permitted.

Run `sh validate-p2-local.sh`. The fixture-to-control mapping is `ledger reconciliation, allocation
gaps, forecast variance, unit metric, owner/due date, closure evidence`. Expected output is a
machine-readable JSON result containing interpreter, command, fixture set, computed metrics, PASS
outcome, and negative-case coverage. Evidence retention is limited to the generated local transcript
and result; it is not an authorization or production record.
