#!/usr/bin/env bash
set -euo pipefail

IMAGE="${IMAGE:-supply-chain-demo:local}"

docker build -t "$IMAGE" app
trivy image --severity HIGH,CRITICAL "$IMAGE"
syft "$IMAGE" -o spdx-json > sbom.spdx.json

