#!/usr/bin/env sh
set -eu
project_root=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
project_name=$(basename "$project_root")
if [ "$project_name" != "project-33-node-cicd-eks-gha" ]; then
  printf '%s
' "ERROR: expected project-33-node-cicd-eks-gha; found $project_name" >&2
  exit 1
fi
for required in README.md START_HERE.md; do
  if [ ! -f "$project_root/$required" ]; then
    printf '%s
' "ERROR: missing required active file: $required" >&2
    exit 1
  fi
done
if grep -R -n -E '(AWS_ACCESS_KEY_ID=|AWS_SECRET_ACCESS_KEY=|client_secret=|private_key=)'   "$project_root/START_HERE.md" >/dev/null 2>&1; then
  printf '%s
' 'ERROR: credential-shaped text in learner guide' >&2
  exit 1
fi
printf '%s local-first validation: PASS
' 'P2 project-33-node-cicd-eks-gha'
