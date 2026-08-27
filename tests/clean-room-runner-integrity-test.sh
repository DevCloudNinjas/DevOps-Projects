#!/usr/bin/env sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
cp -a "$root" "$tmp/repository"
rm -rf "$tmp/repository/.git" "$tmp/repository/.cache" "$tmp/repository/node_modules"
PYTHONPATH= "$tmp/repository/scripts/canonical-evidence.sh"
printf '%s\n' 'Clean-room runner integrity test: PASS'
