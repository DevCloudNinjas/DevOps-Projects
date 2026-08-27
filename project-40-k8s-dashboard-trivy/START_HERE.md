# Start Here: project-40-k8s-dashboard-trivy

**Learning focus:** Local Kubernetes dashboard observability and DevSecOps image scanning

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, run the documented local validation command `node --check app.js && python3 -m
py_compile systeminfo.py` before attempting to launch the dashboard.

## Checkpoints

1. 1. Both `app.js` and `systeminfo.py` pass the syntax checks without errors
2. 1. The Flask dashboard opens at the documented local address and displays its system-metrics area
3. 1. A selected namespace shows Kubernetes resource counts and a test image scan produces a visible Trivy report in the dashboard.

## Hints if you are stuck

1. 1. If the first checkpoint fails, inspect the reported file and line number before changing behavior
2. 1. If the page loads but data is missing, check whether the local process has access to the expected Kubernetes context and namespace
3. 1. If scanning does not return a report, verify the image identifier and that the local Trivy command is available, then capture the exact error rather than broadening permissions.

## Evidence to capture

Validation output, local dashboard screenshot, namespace resource-count view, and Trivy scan report or
captured diagnostic error

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
