#!/usr/bin/env sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
"$root/scripts/create-canonical-source-packet.sh" "$tmp/source.tar.gz"
mkdir "$tmp/extracted"
tar -xzf "$tmp/source.tar.gz" -C "$tmp/extracted"
[ ! -d "$tmp/extracted/.git" ]
PYTHONPATH= "$tmp/extracted/scripts/canonical-evidence.sh"
printf '%s\n' 'Canonical source-packet test: PASS'
