# Start Here: project-08-2048-game-eks

**Learning focus:** Kubernetes workload deployment and service exposure for a 2048 web app

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

From the project directory, inspect README.md, 2048-deployment.yaml, and mygame-svc.yaml, then run the listed client-side validation command `kubectl apply --dry-run=client -f 2048-deployment.yaml -f mygame-svc.yaml` without contacting a cluster.

## Checkpoints

1. 1. The dry-run completes without manifest or schema errors for both the Deployment and Service
2. 2. The Deployment manifest visibly defines one `deployment-2048` replica with matching `app: 2048-ws` selector/template labels and container port 80
3. 3. The Service manifest visibly selects `app: 2048-ws`, maps port 80 to targetPort 80, and declares type `LoadBalancer`.

## Hints if you are stuck

1. 1. If the dry-run reports a YAML problem, compare indentation and key nesting against the nearby manifest examples in README.md
2. 2. If the workload and Service do not connect conceptually, check that the Service selector exactly matches the Pod-template label rather than only the resource names
3. 3. If validation cannot run locally, first verify that `kubectl` is installed and that both referenced YAML files are in the current directory, without switching to cluster creation.

## Evidence to capture

Terminal output showing a successful client-side dry run plus annotated excerpts or screenshots of the Deployment labels/port and Service selector/port/type

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
