# Project 53: Supply Chain Security Lab

Student-friendly lab for learning image scanning, SBOM generation, and image signing concepts with GitHub Actions, Trivy, Syft, and Cosign.

## What You Learn

- How container images move through a security pipeline
- How to scan for vulnerabilities and secrets
- How to generate an SBOM
- Why image signing matters
- How CI gates protect deployments

## Home Lab Cost

Local only unless you choose to push an image to a registry.

## Prerequisites

- Docker
- Trivy
- Syft
- Cosign, optional for signing

## Local Flow

```bash
docker build -t supply-chain-demo:local ./app
trivy image --severity HIGH,CRITICAL supply-chain-demo:local
syft supply-chain-demo:local -o spdx-json > sbom.spdx.json
cosign generate-key-pair
cosign sign --key cosign.key supply-chain-demo:local
```

For a beginner version, run only the Docker build and Trivy scan first.

## CI Flow

The sample workflow in `.github/workflows/security.yml` builds the image, scans it, and writes an SBOM artifact.

## Student Exercises

- Add a vulnerable dependency and watch Trivy fail.
- Add `.trivyignore` with a documented exception.
- Push the image to GHCR.
- Sign the GHCR image with keyless Cosign.

