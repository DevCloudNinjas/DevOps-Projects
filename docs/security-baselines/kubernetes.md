# Kubernetes Security Baseline

Use this checklist for Kubernetes manifests, Helm charts, Kustomize overlays, and deployment runbooks.

## Workload Identity and Access

- [ ] Service accounts are explicit; workloads do not rely on the namespace default service account.
- [ ] RBAC permissions are scoped to the namespace and verbs/resources the workload actually needs.
- [ ] Cloud IAM bindings use workload identity, IRSA, or the provider equivalent instead of static access keys.
- [ ] Privileged workloads are documented with a clear reason and owner.

## Pod and Container Security

- [ ] `securityContext` sets `runAsNonRoot: true` where the image supports it.
- [ ] Containers drop Linux capabilities unless a specific capability is required.
- [ ] `allowPrivilegeEscalation: false` is set for application containers.
- [ ] Root filesystems are read-only where practical.
- [ ] Host namespaces, host paths, and privileged mode are avoided unless the workload is infrastructure-level.

## Images and Supply Chain

- [ ] Images are pinned to immutable digests or tightly controlled tags.
- [ ] Images come from trusted registries.
- [ ] Image scanning is part of CI/CD or the release checklist.
- [ ] Pull secrets are namespace-scoped and not shared broadly.

## Networking

- [ ] Services expose only required ports.
- [ ] Public `LoadBalancer` or ingress resources have an owner, purpose, and expected source audience.
- [ ] NetworkPolicies restrict ingress and egress for sensitive namespaces.
- [ ] Admin endpoints, dashboards, and metrics are private or authenticated.

## Reliability and Abuse Resistance

- [ ] CPU and memory requests are set for every container.
- [ ] Limits are set where runaway usage would affect shared clusters.
- [ ] Readiness and liveness probes match real application health.
- [ ] Pod disruption behavior is considered for multi-replica services.

## Secrets and Configuration

- [ ] Secret manifests in git are templates only; rendered values are ignored.
- [ ] ConfigMaps do not contain credentials, tokens, private keys, or connection strings with passwords.
- [ ] External secret managers or sealed/encrypted secrets are used for real deployments.
- [ ] Rotation steps are documented for any credential consumed by the workload.

## Validation

Run local checks when the required tools are available:

```bash
kubectl apply --dry-run=client -f <manifest-or-directory>
kubectl kustomize <overlay-directory>
helm template <release-name> <chart-directory>
```
