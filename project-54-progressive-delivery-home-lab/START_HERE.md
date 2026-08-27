# Start Here: project-54-progressive-delivery-home-lab

**Learning focus:** Local Kubernetes progressive delivery with Argo Rollouts canary releases and rollback

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

Run `make validate` from the project root to locally parse the namespace, service, and rollout YAML before
creating a cluster or changing any manifest.

## Checkpoints

1. 1. `make validate` completes successfully and confirms the three YAML manifests parse locally
2. 1. After the local workflow is started, the sample `demo-rollout` and its service are applied in the `progressive-delivery` namespace and can be observed
3. 1. After changing only the image tag in `rollouts/rollout.yaml` and reapplying it, the rollout visibly pauses at a canary step so the student can distinguish pause, promotion, and abort behavior.

## Hints if you are stuck

1. 1. If validation fails, identify whether the error is in `rollouts/namespace.yaml`, `rollouts/service.yaml`, or `rollouts/rollout.yaml` before changing anything
2. 1. If the rollout does not progress, inspect pod readiness and confirm that the image tag in `rollouts/rollout.yaml` names an available image
3. 1. If the Argo Rollouts plugin is unavailable, use the basic rollout status view with `kubectl get rollout -n progressive-delivery` and compare what it shows with the expected canary state.

## Evidence to capture

Successful `make validate` output, terminal evidence of demo-rollout canary progression and pause/status, and
a before/after manifest diff showing the image-tag experiment plus the resulting promotion or abort
observation.

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
