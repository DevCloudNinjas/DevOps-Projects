# Start Here: project-53-supply-chain-security-lab

**Learning focus:** Container supply-chain security: vulnerability scanning, SBOMs, signing, and CI security gates

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, run `make validate` to syntax-check the Node app and parse the GitHub Actions workflow locally before building or scanning an image.

## Checkpoints

1. 1. `make validate` completes successfully, including `node --check app/server.js` and workflow parsing when PyYAML is available
2. 2. `docker build -t supply-chain-demo:local ./app` completes and the local app is reachable at `http://localhost:8080` after `make up`
3. 3. `trivy image --severity HIGH,CRITICAL supply-chain-demo:local` produces a scan result and `syft supply-chain-demo:local -o spdx-json > sbom.spdx.json` creates the SBOM artifact.

## Hints if you are stuck

1. 1. If validation fails, separate a Node syntax issue from a workflow-parsing issue and inspect the named file before changing anything
2. 2. If the container does not start or the URL is unavailable, check the local Docker engine and use `make logs` to identify whether the app process is running
3. 3. If a security command is unavailable, confirm the corresponding Trivy or Syft prerequisite and continue with the explicitly supported beginner validation/run path rather than attempting a cloud workflow.

## Evidence to capture

Successful validation output, local image/app observation, Trivy scan output, and generated `sbom.spdx.json`

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
