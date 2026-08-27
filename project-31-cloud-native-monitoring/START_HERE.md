# Start Here: project-31-cloud-native-monitoring

**Learning focus:** Local Flask monitoring app containerization and Kubernetes deployment concepts

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, read the README's local application section and run the repository's stated validation
command `make test` without configuring AWS, Docker pushes, or an EKS cluster.

## Checkpoints

1. 1. `make test` completes and the healthcheck test passes
2. 1. the learner can identify from `README.md` how `app.py`, `requirements.txt`, `Dockerfile`, and `tests/test_healthcheck.py` fit together for the local Flask app
3. 1. the learner records a local-only explanation of the intended container, ECR, and Kubernetes Deployment/Service flow without executing cloud-provider or cluster commands.

## Hints if you are stuck

1. 1. If the validation command fails, distinguish a test/assertion problem from a missing local dependency before changing application code
2. 1. compare the Flask listen port and healthcheck expectations with the port exposed and published in the Docker instructions
3. 1. when reviewing the Kubernetes examples, check that selectors, labels, service ports, and the image placeholder agree before treating the manifest logic as correct.

## Evidence to capture

Passing `make test` output plus a short local architecture note mapping the Flask app, healthcheck, container
settings, and Kubernetes object relationships

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
