#!/usr/bin/env sh
set -eu
root=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
python3 "$root/tools/validate_active_integrity.py"
python3 "$root/.github/scripts/p2_classroom_check.py"
"$root/scripts/validate-p2-portfolio.sh"
printf '%s\n' 'Canonical local evidence: PASS'
