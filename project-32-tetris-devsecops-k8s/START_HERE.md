# Start Here: project-32-tetris-devsecops-k8s

**Learning focus:** DevSecOps CI/CD for a React application with Docker, Kubernetes manifests, Jenkins, Terraform, and EKS architecture

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, inspect `Tetris-V1/package.json`, `Tetris-V1/README.md`, and `Manifest-file/deployment-service.yml` to map the React app, its local test command, and its Kubernetes resource definitions without applying any infrastructure.

## Checkpoints

1. 1. The learner can identify Tetris-V1 as the initial React application and locate its package scripts and test file
2. 2. The learner can explain how the Dockerfile, Jenkins pipeline files, and `Manifest-file/deployment-service.yml` connect the application build to container and Kubernetes delivery
3. 3. The learner can run the packet’s validation command `npm --prefix Tetris-V1 test --if-present` locally and capture the result without provisioning AWS, Jenkins, or EKS.

## Hints if you are stuck

1. 1. If the validation command behaves unexpectedly, compare the working directory and the `--prefix` path with the inventory before changing application files
2. 2. If the pipeline flow is unclear, read the Jenkinsfiles alongside the Dockerfile and note which filenames and stages are referenced
3. 3. If the Kubernetes manifest is difficult to interpret, separate the workload fields from the service fields and compare their labels, ports, and image references without deploying them.

## Evidence to capture

A local inspection note or screenshot showing the React package/test entry point, the Docker-to-pipeline-to-manifest relationship, and the captured local test output

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
