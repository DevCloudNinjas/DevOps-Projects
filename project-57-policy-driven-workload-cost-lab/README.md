# Project 57: policy-driven workload cost

This is a **synthetic, source-only, offline** classroom rehearsal. It never authorizes a live pilot,
deployment, cloud access, production change, or regulatory attestation.

## Workflow and fixtures

Run `sh validate-p2-local.sh`; the validator reads every JSON/CSV fixture under `fixtures/`, computes results,
and emits `evidence/validator-result.json`. Coverage: allow/deny, expiry, public/persistent resources,
ownership, budgets, policy diff. Inputs are deterministic checked-in fixtures; malformed, missing,
contradictory, unsafe, or incomplete records fail closed.

The supported assumption is Python 3.8+ standard library only. Synthetic evidence demonstrates a control
decision, not operational approval. Keep the transcript and machine-readable result with the review packet.
