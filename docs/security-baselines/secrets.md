# Secrets Security Baseline

Use this checklist for credentials, private keys, tokens, certificates, env files, sample configs, and secret-handling docs.

## Storage Rules

- [ ] Real secrets are never committed to git.
- [ ] Example files use placeholders such as `REPLACE_ME`, `example.invalid`, or documentation CIDRs.
- [ ] `.env`, `.tfvars`, kubeconfigs, private keys, and generated secret manifests are ignored.
- [ ] Secret scanner fixtures are isolated and clearly marked when they are intentionally committed.

## Runtime Delivery

- [ ] Applications read secrets from environment variables, mounted secret files, or managed secret stores.
- [ ] Kubernetes workloads use Secret templates, sealed/encrypted secrets, or external secret managers for real values.
- [ ] Terraform receives secrets through CI secret stores or local untracked files.
- [ ] CI/CD jobs avoid writing secrets to workspace files unless the files are removed in the same job.

## Access and Rotation

- [ ] Secrets have an owner and documented purpose.
- [ ] Credentials use least privilege and scoped lifetimes.
- [ ] Rotation steps are documented for cloud keys, deploy tokens, database passwords, and webhook secrets.
- [ ] Removed or exposed credentials are revoked, not just deleted from git.

## Detection and Response

- [ ] Run the local quality gate before opening a pull request.
- [ ] Use a dedicated secret scanner for broad history or release checks.
- [ ] Treat public commits as exposed even if deleted later.
- [ ] Record remediation steps in the PR or incident notes when a real secret is found.

## Safe Examples

Prefer this pattern for examples:

```dotenv
DATABASE_URL=postgres://app_user:REPLACE_ME@example.invalid:5432/app
API_TOKEN=REPLACE_ME
```

Avoid realistic-looking keys, tokens, account IDs, or private key blocks in documentation unless they are scanner fixtures stored in a clearly labeled test path.
