#!/usr/bin/env sh
set -eu
root=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
if [ "$(basename "$root")" != "project-14-github-actions-android" ]; then
  printf '%s\n' 'ERROR: project root mismatch' >&2
  exit 1
fi
for required in README.md START_HERE.md P2_CLASSROOM.md P2_EVIDENCE.md P2_LOCAL_PILOT.md; do
  [ -f "$root/$required" ] || { printf '%s\n' "ERROR: missing $required" >&2; exit 1; }
done
if grep -R -n -E '(AWS_ACCESS_KEY_ID=|AWS_SECRET_ACCESS_KEY=|client_secret=|private_key=)' \
  "$root/START_HERE.md" >/dev/null 2>&1; then
  printf '%s\n' 'ERROR: credential-shaped text in learner guide' >&2
  exit 1
fi
printf '%s local-only control: PASS (%s)\n' 'project-14-github-actions-android' 'negative-quarantine-probe.sh'
