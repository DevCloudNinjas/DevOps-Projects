# L2 pilot contract — source-only supply-chain CI

Purpose: Project 53 is the sole selected pilot for the first governed rehearsal; this document validates a narrow, disposable source contract before any optional cloud rehearsal. Target: source digest, SBOM, provenance and attestation verification; no push or cloud login. Scope: one disposable artifact/verification target only when separately approved; no registry by default; region: one approved region supplied in authorization; lifetime: maximum 2 hours. Required tags are `owner`, `request_id`, `expires_at`, and `managed_by=l2-cloud-pilot`. No public ingress, persistent user data, shared state, unmanaged IP, cluster, database, NAT gateway, load balancer, or production dependency is allowed.

Teardown must complete before expiry, followed by an independent inventory and cost check. Source gates are local-only and never apply, destroy, publish, or log in. Any cloud execution remains separately authorized and environment-protected.
