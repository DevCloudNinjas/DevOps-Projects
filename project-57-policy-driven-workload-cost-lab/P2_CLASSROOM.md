# Project 57 Classroom Record

This record defines a local-only, offline rehearsal for policy-driven workload cost. Learning objectives are to inspect the checked-in synthetic fixtures, apply the documented controls, and reproduce computed positive and negative decisions. Prerequisite: Python 3.8+ and a clean checkout; no provider CLI, SDK, credential, network, container, deployment, teardown, or live-service behavior is permitted.

Run `sh validate-p2-local.sh`. The fixture-to-control mapping is `allow/deny, expiry, public/persistent resources, ownership, budgets, policy diff`. Expected output is a machine-readable JSON result containing interpreter, command, fixture set, computed metrics, PASS outcome, and negative-case coverage. Evidence retention is limited to the generated local transcript and result; it is not an authorization or production record.
