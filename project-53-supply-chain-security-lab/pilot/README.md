# L2 pilot contract — source-only supply-chain CI

Project 53 is the sole selected pilot for the first governed rehearsal. This
document validates a narrow, disposable source contract before any optional
cloud rehearsal.

The target is source digest, SBOM, provenance, and attestation verification. It
allows no push or cloud login. The scope is one disposable artifact or
verification target, and only when separately approved. A registry is not used
by default. The region is one approved region supplied in authorization. The
maximum lifetime is two hours.

Required tags are `owner`, `request_id`, `expires_at`, and
`managed_by=l2-cloud-pilot`. Public ingress, persistent user data, shared state,
unmanaged IP, cluster, database, NAT gateway, load balancer, and production
dependency are not allowed.

Teardown must complete before expiry, followed by an independent inventory and
cost check. Source gates are local-only and never apply, destroy, publish, or
log in. Any cloud execution remains separately authorized and
environment-protected.
