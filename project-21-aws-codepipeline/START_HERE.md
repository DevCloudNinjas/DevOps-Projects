# Start Here: project-21-aws-codepipeline

**Learning focus:** AWS DevOps CI/CD for a Dockerized React/Vite video-streaming application

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials,
provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, read the readme and inspect `project.yaml`, `buildspec.yaml`, `appspec.yml`,
`Dockerfile`, and `package.json` before making any changes or attempting cloud access.

## Checkpoints

1. 1. You can identify the local React/Vite application entry points and explain the roles of `Dockerfile`, `buildspec.yaml`, `appspec.yml`, and `project.yaml`
2. 1. `npm run build` completes locally and produces the Vite build output without changing deployment configuration
3. 1. You can trace the documented source-to-build-to-deploy flow from CodeCommit through CodeBuild and DockerHub/S3 artifacts to CodeDeploy and an EC2 target, while noting where System Manager parameters are used.

## Hints if you are stuck

1. 1. If the local build fails, compare the command and dependency declarations in `package.json` with the project’s installed Node/npm environment before changing application code
2. 1. For a pipeline-file question, check whether the relevant behavior belongs to the Docker image, the CodeBuild phases, or the CodeDeploy lifecycle configuration
3. 1. When a stage cannot be reasoned about locally, use the filenames and readme headings to map its inputs and outputs rather than inventing AWS resource values or credentials.

## Evidence to capture

Local build output plus a short annotated pipeline map covering source, build, image/artifact, deployment, and
secret-parameter roles

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence
you already collected. Your instructor can release the next hint or use the instructor solution guide during a
debrief.
