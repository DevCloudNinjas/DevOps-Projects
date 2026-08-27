# Source Hardening Record — TERRAFORM + AWS + EKS

## Local-first controls

The active classroom route uses checked-in source, documentation, fixtures, and deterministic validation.
Unsafe, credential-dependent, provider-mutating, or destructive operations are outside the student path and
require separate human authorization.

## Review checklist

- Confirm the project documentation explains the safe starting point.
- Confirm expected evidence can be generated locally.
- Confirm validators are deterministic and fail closed on missing required files.
- Confirm no local result is described as a production or cloud-release approval.
