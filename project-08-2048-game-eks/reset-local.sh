#!/usr/bin/env sh
set -eu
# Local classroom reset only; no provider, container, or deployment command is used.
root=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
[ "$(basename "$root")" = "project-08-2048-game-eks" ] || exit 1
rm -f "$root/evidence/local-validation.tmp"
printf '%s reset: local-only state cleared\n' 'project-08-2048-game-eks'
