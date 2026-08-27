# Start Here: project-41-online-boutique-microservices

**Learning focus:** Local Kubernetes microservices deployment and troubleshooting with Kind

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, run `kubectl apply --dry-run=client -f deploy/` to validate the supplied Kubernetes
manifests before creating or changing a local cluster.

## Checkpoints

1. 1. A local Kind cluster named `qa-cluster` exists and `kubectl get nodes` shows the control-plane and worker nodes as `Ready`
2. 1. After applying `deploy/`, all 11 Online Boutique service Pods reach `Running` and the Services expose the README’s stated service and target ports, with no unresolved scheduling, image, probe, or service-account issue
3. 1. A local port-forwarded frontend loads the Online Boutique home page, a test order completes successfully, and the `qa`-namespace load-generator log contains no failures.

## Hints if you are stuck

1. 1. For a Pod that remains `Pending` or fails to start, compare its scheduling constraints, image reference, events, and requested resources with the nodes in the supplied `kind-config/config.yaml`
2. 1. If the page opens but ordering fails, start with the `frontend` logs and trace the configured service DNS names and ports through the checkout, payment, currency, cart, email, and shipping dependencies
3. 1. If the load test reports errors after the browser flow works, inspect the load-generator namespace, endpoint configuration, and Pod logs before changing any application manifest.

## Evidence to capture

`kubectl get nodes` and `kubectl get all` output, manifest diffs with RCA in `SOLUTION.md`, a local
frontend/order verification record, and failure-free `test/loadgenerator-output.txt`

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
