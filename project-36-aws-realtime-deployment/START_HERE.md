# Start Here: project-36-aws-realtime-deployment

**Learning focus:** AWS DevSecOps CI/CD deployment with environment isolation

> This is a learner guide. It gives a safe first step, checkpoints, and troubleshooting hints; it intentionally does not contain the complete worked answer.

## Before you begin

Read this project’s `README.md`, stay within the local-first classroom path, and do not use cloud credentials, provider commands, deployment commands, or destructive actions.

## First safe action

Open the local README.md, project.yaml, appspec.yml, and buildspec.yml together and annotate how the HTML artifact is intended to move through isolated Dev, Pre-Prod, and Production stages without connecting to AWS.

## Checkpoints

1. 1. A local inventory confirms the HTML entry point, Nginx install/start scripts, appspec.yml, and buildspec.yml are present
2. 2. A learner-produced diagram or notes trace the intended CodeBuild-to-CodeDeploy/CodePipeline flow and identify separate environments or accounts/VPCs as the isolation boundary
3. 3. A local validation record shows the packet's required files satisfy `test -f buildspec.yml -a -f appspec.yml` without performing deployment or teardown.

## Hints if you are stuck

1. 1. Compare the filenames referenced by the deployment configuration with the actual repository paths, including both scripts under `scripts/`
2. 2. If the pipeline stages are unclear, separate the questions of what builds the HTML package, what installs or starts Nginx, and what promotes between environments
3. 3. Treat the README's environment-isolation claim as an architecture requirement and check whether your notes distinguish Dev, Pre-Prod, and Production rather than collapsing them into one target.

## Evidence to capture

Annotated local file map, environment-isolation deployment-flow sketch, and captured local file-presence validation

## When to ask for help

Share the checkpoint number you reached, the exact local validator output or error message, and the evidence you already collected. Your instructor can release the next hint or use the instructor solution guide during a debrief.
