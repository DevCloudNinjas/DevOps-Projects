#!/usr/bin/env sh
set -eu
root=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
python3 "$root/tools/validate_active_integrity.py"
python3 "$root/.github/scripts/p2_classroom_check.py"
count=0
for project in "$root"/project-*; do
  [ -d "$project" ] || continue
  python3 "$root/tools/validate_project_containment.py" "$project"
  if [ -x "$project/validate-p2-local.sh" ]; then
    "$project/validate-p2-local.sh"
  else
    printf '%s\n' "ERROR: missing executable validator: $project/validate-p2-local.sh" >&2
    exit 1
  fi
  count=$((count + 1))
done
printf 'P2 portfolio validation: PASS (%s projects)\n' "$count"
