# Start Here: project-16-jenkins-argocd-k8s

**Learning focus:** Jenkins CI/CD integration with SonarQube, Docker, Kubernetes, and Argo CD deployment concepts

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

Read the README locally and make a three-column map of the intended Jenkins-Master, Jenkins-Agent, and EKS-Bootstrap roles without launching servers or changing any files.

## Checkpoints

1. 1. Produce a role-and-stage map that connects Jenkins controller/agent setup to the pipeline, SonarQube, Docker image, and Kubernetes/Argo CD stages named in the README
2. 2. Annotate the README with a local inventory of required inputs such as repository URL, credentials, host addresses, ports, and configuration values, marking each as a placeholder rather than supplying secrets
3. 3. Submit a short dry-run explanation of how a change would move from the register-app repository through Jenkins quality/build steps toward Kubernetes deployment, identifying which observations would confirm each handoff.

## Hints if you are stuck

1. 1. If the stages seem unclear, separate the README's named machines and services before trying to connect them into one flow
2. 2. When a handoff fails conceptually, check whether the required address, credential identifier, port, or plugin/tool configuration is present in the packet
3. 3. Treat commands, screenshots, and version-specific settings as claims to verify in a controlled lab rather than as permission to use AWS, expose ports, or paste real tokens.

## Evidence to capture

Annotated local stage/role diagram, placeholder-and-dependency inventory, and a dry-run CI/CD handoff narrative

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
