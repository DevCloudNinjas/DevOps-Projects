#!/usr/bin/env sh
set -eu
root=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
output=${1:-"$root/.tmp/canonical-source-packet.tar.gz"}
mkdir -p "$(dirname -- "$output")"
(
  cd "$root"
  tar \
    --exclude=.git \
    --exclude=.cache \
    --exclude=node_modules \
    --exclude=__pycache__ \
    --exclude=.pytest_cache \
    --exclude=.tmp \
    -czf "$output" .
)
printf 'Canonical source packet created: %s\n' "$output"
