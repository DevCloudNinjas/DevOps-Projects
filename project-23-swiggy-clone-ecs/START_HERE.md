# Start Here: project-23-swiggy-clone-ecs

**Learning focus:** DevSecOps CI/CD for Dockerized React deployment with AWS ECS blue-green releases

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

From the project root, inspect `Swiggy_clone/package.json`, `Swiggy_clone/Dockerfile`, `Swiggy_clone/buildspec.yaml`, and `Swiggy_clone/appspec.yaml`, then record the app port, build stages, scan gates, image tag convention, and ECS deployment references without changing them.

## Checkpoints

1. 1. The learner can identify the React entry point and explain how `public/index.html` and `src/` contribute to the Swiggy application
2. 2. The learner can trace the local container/build flow from `Dockerfile` through the non-root production runtime and connect it to the `buildspec.yaml` security checks and numbered image tagging
3. 3. The learner can annotate how `appspec.yaml` maps the ECS task definition, `swiggy` container, and port 3000 to a blue/green target-service update, without creating cloud resources.

## Hints if you are stuck

1. 1. If the file relationships are unclear, start with the package scripts and follow each referenced filename before interpreting the deployment YAML
2. 2. If the container flow seems inconsistent, compare the port exposed by the application configuration with the port named in the Dockerfile and `appspec.yaml`
3. 3. If the pipeline stages are hard to follow, separate source/build/security/deploy responsibilities and look for where credentials, SonarQube, Trivy, and the build-number tag are referenced rather than treating them as one command.

## Evidence to capture

A local architecture trace with annotated file excerpts, a port-and-image-tag table, and a short blue/green deployment sequence diagram or written equivalent

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
