# Start Here: project-33-node-cicd-eks-gha

**Learning focus:** Node.js CI/CD and DevSecOps pipeline configuration with Docker, Kustomize, Terraform, GitHub Actions, and EKS

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

From the repository root, read `README.md` and inspect `app/package.json`, `Makefile`, and `.github/workflows/e2ecicd.yaml` to map the local test/build flow before changing any files or invoking cloud deployment steps.

## Checkpoints

1. 1. The student can identify the Node application entry points and test files under `app/` and explain that `make test` is the packet's local validation command
2. 2. The student can trace the workflow's build stages from dependency installation and unit tests through semantic-version handling and Docker image publication without running the deployment job
3. 3. The student can compare the `dev`, `staging`, and `prod` Kustomize overlays and point to the corresponding Terraform and workflow sections that provision and deploy each environment, while keeping this comparison local-only.

## Hints if you are stuck

1. 1. If the starting point is unclear, follow the README's repository structure and CI/CD Workflow headings, then open the named files rather than guessing commands
2. 2. If local validation does not behave as expected, check the `app/package.json` scripts and the Makefile target against the test files listed in `app/`
3. 3. If the environment comparison is confusing, inspect each overlay's `kustomization.yaml` together with its deployment, service, and ingress patches, and distinguish those files from the Terraform and GitHub Actions layers.

## Evidence to capture

A local inspection note or diff-free report containing the successful `make test` result, a build-job flow diagram or annotated trace, and a dev/staging/prod overlay comparison

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
