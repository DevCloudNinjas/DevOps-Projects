# Dockerfile Security Baseline

Use this checklist for Dockerfiles, compose files, image build scripts, and container release notes.

## Base Images

- [ ] Base images come from trusted publishers.
- [ ] Base images are pinned to a specific version; use digests for release-critical images.
- [ ] Minimal runtime images are used where practical.
- [ ] End-of-life language runtimes and operating systems are avoided.

## Build Hygiene

- [ ] Multi-stage builds keep compilers and build tools out of runtime images.
- [ ] Package manager caches are removed in the same layer where packages are installed.
- [ ] Dependency lockfiles are copied and installed before application source when it improves repeatability.
- [ ] `.dockerignore` excludes `.git`, local env files, test artifacts, build output, and secrets.

## Dependencies and Supply Chain

- [ ] Dependencies are installed from official registries or approved mirrors.
- [ ] Package versions are pinned or controlled by lockfiles.
- [ ] Image scanning is run before publishing or deployment.
- [ ] Build arguments do not carry secrets into image history.

## Runtime Safety

- [ ] The container runs as a non-root user when the application supports it.
- [ ] Only required ports are exposed.
- [ ] Entrypoints fail fast and do not hide application errors.
- [ ] Health checks are present for long-running services where the orchestrator uses them.
- [ ] Writable paths are limited and documented.

## Secrets and Configuration

- [ ] No credentials, tokens, private keys, or `.env` files are copied into the image.
- [ ] Runtime configuration is supplied through environment variables, mounted files, or secret managers.
- [ ] Example env files use safe placeholders.

## Validation

Run local checks when the tools are available:

```bash
docker build --no-cache -t local/security-check .
docker history local/security-check
trivy image local/security-check
```
